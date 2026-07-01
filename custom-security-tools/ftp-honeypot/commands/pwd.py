# commands/pwd.py

class PwdCommand():
    def execute(self, session, args):
        return f'257 "{session.cwd}"'   