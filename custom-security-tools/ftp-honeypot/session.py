#session.py

class Session:
    def __init__(self, client, ip):
        self.client = client
        self.ip = ip
        self.username = None
        self.password = None
        self.logged_in = False
        self.connected = False
        self.cwd = "/"
        self.data_ip = None
        self.data_port = None
        self.data_mode = None      # "PORT" or "PASV"
        self.pasv_socket = None    # listening socket, only used in PASV mode