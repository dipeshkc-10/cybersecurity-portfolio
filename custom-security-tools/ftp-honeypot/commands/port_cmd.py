class PortCommand():
    def execute(self, session, args):
        if not args:
            return "501 Syntax error in PORT command."

        try:
            nums = args[0].split(",")
            ip = ".".join(nums[:4])
            port = int(nums[4]) * 256 + int(nums[5])
        except (ValueError, IndexError):
            return "501 Syntax error in PORT command."

        # clean up any leftover PASV listener since we're switching to active mode
        if session.pasv_socket:
            session.pasv_socket.close()
            session.pasv_socket = None

        session.data_mode = "PORT"
        session.data_ip = ip
        session.data_port = port

        return "200 PORT command successful."
