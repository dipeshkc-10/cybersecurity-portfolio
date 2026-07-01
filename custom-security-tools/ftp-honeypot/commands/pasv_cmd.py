import socket


class PasvCommand():
    def execute(self, session, args):
        # close out any leftover listener from a previous PASV
        if session.pasv_socket:
            try:
                session.pasv_socket.close()
            except OSError:
                pass
            session.pasv_socket = None

        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(("0.0.0.0", 0))   # let the OS pick a free port
        listener.listen(1)
        listener.settimeout(30)         # don't hang forever waiting for the client to connect

        server_ip = session.client.getsockname()[0]
        port = listener.getsockname()[1]

        session.data_mode = "PASV"
        session.pasv_socket = listener
        session.data_ip = None
        session.data_port = None

        ip_parts = server_ip.split(".")
        p1, p2 = port >> 8, port & 0xFF

        return f"227 Entering Passive Mode ({','.join(ip_parts)},{p1},{p2})."
