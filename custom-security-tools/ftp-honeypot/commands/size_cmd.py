import posixpath
import os

FTP_ROOT = "/home/d1ph3x/ftp_files"

class SizeCommand():
    def execute(self, session, args):
        if not args:
            return "501 Missing filename."

        virtual_path = posixpath.normpath(posixpath.join(session.cwd, args[0]))
        real_path = os.path.normpath(FTP_ROOT + virtual_path)

        if not real_path.startswith(FTP_ROOT):
            return "550 Permission denied."

        if not os.path.isfile(real_path):
            return f"550 No such file: {args[0]}"

        size = os.path.getsize(real_path)
        return f"213 {size}"