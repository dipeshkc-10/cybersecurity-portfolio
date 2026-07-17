# Stealth SYN Port Scanner

A lightweight, multithreaded TCP SYN (half-open) port scanner written in Python using Scapy. 

Unlike standard full-connect TCP scanners that complete the 3-way handshake (leaving a distinct footprint in target logs), this tool sends a SYN packet and waits for a SYN-ACK. If an open port is detected, it immediately drops the connection with an RST (Reset) packet, making the scan significantly quieter.

## Features
* **Stealthy (SYN Scan):** Performs TCP half-open scans to reduce logging footprints on target systems.
* **Multithreaded:** Utilizes Python's `ThreadPoolExecutor` for concurrent scanning.
* **Batch Target Support:** Scan a single domain/IP or pass a `.txt` file containing a list of targets.
* **Graceful Teardown:** Automatically sends RST packets to close half-open connections.
* **Cross-Platform:** Works on Linux and macOS (requires root/sudo for raw socket access).

## Prerequisites
* Python 3.7+
* `root` or `sudo` privileges (required by Scapy to craft raw packets)

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/stealth-syn-scanner.git](https://github.com/yourusername/stealth-syn-scanner.git)
   cd stealth-syn-scanner
