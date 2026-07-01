import socket
import posixpath


LISTINGS = {
    "/": (
        "total 4\r\n"
        "drwxr-xr-x 2 d1ph3x d1ph3x 4096 Jun 28 18:03 logs\r\n"
    ),
    "/logs": (
        "total 140\r\n"
        "-r--r--r-- 1 d1ph3x d1ph3x 108653 Apr 11  2021 access.log\r\n"
        "-r--r--r-- 1 d1ph3x d1ph3x  22671 Apr 11  2021 auth.log\r\n"
        "-rw-r--r-- 1 d1ph3x d1ph3x     97 Jun 28 18:03 README.txt\r\n"
        "-r--r--r-- 1 d1ph3x d1ph3x   3213 Apr 11  2021 vsftpd.log\r\n"
    ),
}


class ListCommand():
    def execute(self, session, args):
        if session.data_mode is None:
            return "425 Use PORT or PASV first."

        # resolve target directory
        if args:
            # args[0] might be "logs", "logs/", "/logs", ".." etc.
            # resolve it relative to cwd, then normalise
            raw = args[0].rstrip("/")               # strip trailing slash
            target = posixpath.normpath(
                posixpath.join(session.cwd, raw)    # handles "..", absolute paths, etc.
            )
        else:
            target = session.cwd

        if target not in LISTINGS:
            return f"550 No such directory: {target}"

        try:
            data_socket = self._open_data_connection(session)
        except (socket.timeout, OSError) as e:
            return f"425 Can't open data connection: {e}"

        session.client.send(b"150 Opening data connection for file list.\r\n")

        try:
            data_socket.sendall(LISTINGS[target].encode())
            result = "226 Transfer complete."
        except OSError as e:
            result = f"426 Connection closed; transfer aborted: {e}"
        finally:
            data_socket.close()
            if session.data_mode == "PASV" and session.pasv_socket:
                session.pasv_socket.close()
                session.pasv_socket = None

        return result

    def _open_data_connection(self, session):
        if session.data_mode == "PORT":
            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.settimeout(10)
            data_socket.connect((session.data_ip, session.data_port))
            return data_socket

        elif session.data_mode == "PASV":
            if session.pasv_socket is None:
                raise OSError("No PASV listener open.")
            conn, _addr = session.pasv_socket.accept()
            return conn

        else:
            raise OSError("No data mode set.")