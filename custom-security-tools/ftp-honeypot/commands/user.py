class UserCommand():
    def execute(self, session, args):
        if not args:
            return "501 Missing username."

        session.username = args[0]
        return "331 Password required."        