# commands/cwd_cmd.py

class CwdCommand():
    def execute(self, session, args):
        if not args:
            return "501 Missing directory argument."

        target = args[0]

        if target == "..":
            if session.cwd == "/":
                # already at root, nowhere to go up to
                session.cwd = "/"
            else:
                session.cwd = "/"
            return f'250 CWD command successful. "{session.cwd}"'

        elif target == "logs" and session.cwd == "/":
            session.cwd = "/logs"
            return f'250 CWD command successful. "{session.cwd}"'

        else:
            return "550 Failed to change directory: no such directory."