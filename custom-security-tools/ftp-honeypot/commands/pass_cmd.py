class PassCommand():
    def execute(self, session, args):
        return f'230 "{session.cwd}"'