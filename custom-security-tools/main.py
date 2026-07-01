#main

from server import FTPServer

print("""
====================================================
                  FTP-HONEYPOT
             Developed by Dipesh KC
====================================================
""")

server = FTPServer()
server.start()
