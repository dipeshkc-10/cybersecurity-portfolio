import sys
import os
import socket
import logging
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor

# Suppress Scapy's annoying startup warnings (like IPv6 routing issues)
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import IP, TCP, sr1, send, conf

# Keep Scapy quiet in the background
conf.verb = 0 

def scan_port_scapy(ip, port):
    """Perform a stealth SYN scan using Scapy on a specific port."""
    try:
        # Craft the SYN packet
        syn_packet = IP(dst=ip) / TCP(dport=port, flags='S')
        
        # Send the packet and wait for 1 response. Timeout is 1 second.
        response = sr1(syn_packet, timeout=1.0, verbose=0)
        
        if response is not None:
            # Check if the response is a TCP packet and has the SYN-ACK flags (0x12)
            if response.haslayer(TCP) and response.getlayer(TCP).flags == 0x12:
                print(colored(f"[+] Port {port} is OPEN", "green"))
                
                # Send a RST packet to gracefully (and stealthily) close the half-open connection
                rst_packet = IP(dst=ip) / TCP(dport=port, flags='R')
                send(rst_packet, verbose=0)
                
            # If we get a RST-ACK (0x14), the port is closed. We silently ignore it.
    except Exception:
        pass # Silently drop errors to keep output clean

def scan_target(target, start_port, end_port):
    """Resolve domain to IP and kick off the threaded Scapy scan."""
    try:
        ip = socket.gethostbyname(target)
        print(colored(f"\n[*] Stealth Scanning Target: {target} ({ip})", "cyan", attrs=['bold']))
        print(colored(f"[*] Scanning Ports {start_port} to {end_port}...", "cyan"))
        print("-" * 50)
    except socket.gaierror:
        print(colored(f"\n[-] Couldn't resolve host: {target}", "red", attrs=['bold']))
        return

    # Threading with Scapy can drop packets if we go too fast. 
    # 50 workers is a safer sweet spot for raw sockets than 100.
    with ThreadPoolExecutor(max_workers=50) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port_scapy, ip, port)

def main():
    # Check for root privileges before running
    if os.name == 'posix' and os.geteuid() != 0:
        print(colored("[-] Bro, you need root privileges to run Scapy. Use sudo!", "red", attrs=['bold']))
        sys.exit(1)

    os.system('clear' if os.name == 'posix' else 'cls')
    print(colored("=== Broski's Stealth SYN Scanner (Scapy Edition) ===", "yellow", attrs=['bold']))

    target_input = input("Enter a target (Domain, IP) or path to a .txt file: ").strip()

    try:
        start_port = int(input("Enter starting port (e.g., 1): "))
        end_port = int(input("Enter ending port (e.g., 1000): "))
    except ValueError:
        print(colored("[-] Gotta enter actual numbers for the ports, man.", "red"))
        sys.exit(1)

    if os.path.isfile(target_input):
        print(colored(f"\n[*] Reading targets from file: {target_input}...", "blue", attrs=['bold']))
        with open(target_input, 'r') as file:
            targets = [line.strip() for line in file if line.strip()]
        
        for target in targets:
            scan_target(target, start_port, end_port)
    else:
        scan_target(target_input, start_port, end_port)

    print(colored("\n[*] Stealth scan complete! Stay off the radar.", "yellow", attrs=['bold']))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n[-] Scan interrupted by user. Exiting...", "red"))
        sys.exit(0)
