class QuitCommand():
    def execute(self, session, args):
        session.connected = False
        return "221 Goodbye."
