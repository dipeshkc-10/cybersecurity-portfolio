class TypeCommand():
    def execute(self, session, args):
        if not args:
            return "501 Missing type argument."
        t = args[0].upper()
        if t == "I":
            return "200 Switching to Binary mode."
        elif t == "A":
            return "200 Switching to ASCII mode."
        else:
            return f"504 Type {t} not supported."