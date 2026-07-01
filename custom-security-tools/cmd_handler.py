from commands.user import UserCommand
from commands.pass_cmd import PassCommand
from commands.quit import QuitCommand
from commands.pwd import PwdCommand
from commands.list_cmd import ListCommand
from commands.port_cmd import PortCommand
from commands.pasv_cmd import PasvCommand
from commands.cwd_cmd import CwdCommand
from commands.retr_cmd import RetrCommand
from commands.type_cmd import TypeCommand
from commands.size_cmd import SizeCommand


class CommandHandler:
    def __init__(self):
        self.commands = {
            "USER": UserCommand(),
            "PASS": PassCommand(),
            "QUIT": QuitCommand(),
            "PWD": PwdCommand(),
            "LS": ListCommand(),
            "DIR": ListCommand(),
            "LIST": ListCommand(),
            "PORT": PortCommand(),
            "PASV": PasvCommand(),
            "CWD": CwdCommand(),
            "RETR": RetrCommand(),
            "TYPE": TypeCommand(),
            "SIZE": SizeCommand(),
        }

    def handle(self, session, line):
        parts = line.strip().split()

        if not parts:
            return "500 Invalid command."

        cmd = parts[0].upper()
        args = parts[1:]

        command = self.commands.get(cmd)

        if command:
            return command.execute(session, args)

        return "502 Command not implemented."