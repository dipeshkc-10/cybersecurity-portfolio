import socket
import posixpath
import os


# Root directory on disk that maps to "/" in the FTP session.
# Change this to wherever your actual files live.
FTP_ROOT = "/home/d1ph3x/Desktop/ftp_honeypot2/filesystem"


class RetrCommand():
    def execute(self, session, args):
        if session.data_mode is None:
            return "425 Use PORT or PASV first."

        if not args:
            return "501 Missing filename."

        # resolve the virtual FTP path to a real path on disk
        virtual_path = posixpath.normpath(posixpath.join(session.cwd, args[0]))
        real_path = os.path.normpath(FTP_ROOT + virtual_path)

        print(f"virtual path: {virtual_path}")
        print(f"real_path = {real_path}")

        # make sure the client can't escape FTP_ROOT with something like "../../etc/passwd"
        if not real_path.startswith(FTP_ROOT):
            return "550 Permission denied."

        if not os.path.isfile(real_path):
            return f"550 No such file: {args[0]}"

        try:
            data_socket = self._open_data_connection(session)
        except (socket.timeout, OSError) as e:
            return f"425 Can't open data connection: {e}"

        session.client.send(
            f"150 Opening data connection for {args[0]}.\r\n".encode()
        )

        try:
            with open(real_path, "rb") as f:
                while chunk := f.read(8192):
                    data_socket.sendall(chunk)
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