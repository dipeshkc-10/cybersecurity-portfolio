#server

import socket
from session import Session
from cmd_handler import CommandHandler
import threading
from logger import log

class FTPServer:
    def __init__(self, host="0.0.0.0", port=2121):
        self.host = host
        self.port = port

    def handle_client(self, client, address):
        session = Session(client, address[0])
        session.connected = True
        print(f"[+] {session.ip} connected")
        client.send(b"220 FTP Server Ready\r\n")

        handler = CommandHandler()

        while session.connected:
            data = client.recv(1024)

            if not data:
                break

            command = data.decode().strip()
            print(repr(command))
            print(f"{session.ip}: {command}")

            #if command.split()[0].upper() != "USER" or command.split()[0].upper() != "PASS":
            # client.send(b"200 ok\r\n")

            response = handler.handle(session, command)
            log(session.ip, command, response)
            client.send((response+"\r\n").encode())

            # parts = command.split()
            # cmd = parts[0].upper()
            # args = parts[1:]

            # if cmd == "USER":
            #     session.username = args[0]
            #     client.send(b"331 Password required\r\n")

            # elif cmd == "PASS":
            #     session.logged_in = True
            #     client.send(b"230 Login successful\r\n")

            # elif cmd == "QUIT":
            #     # client.send(b"221 goodbye\r\n")
            #     break
        
        session.connected = False
        client.close()
        print(f"[-] {address[0]} disconnected")

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind((self.host, self.port))
        server.listen()

        print(f"Listening on {self.host}:{self.port}")

        

        while True:
            conn, address = server.accept()

#            session = Session(address[0])

            thread = threading.Thread(
                target=self.handle_client, 
                args=(conn, address),
                daemon=True
            )

            thread.start()