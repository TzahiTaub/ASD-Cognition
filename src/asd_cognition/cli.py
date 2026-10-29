import inspect
import sys

USAGE_STRING = "Usage: python cli.py <command> [<key>=<value>]*"


class CliFunction:
    def __init__(self, func):
        self.func = func
        self.sig = inspect.signature(func)


class CommandLineInterface:
    def __init__(self):
        self.functions: dict[str, CliFunction] = {}

    def command(self, f):
        if self.functions.get(f.__name__):
            raise ValueError(
                f"Function {f.__name__} is already registered as a command."
            )

        self.functions[f.__name__] = CliFunction(f)

    def usage_msg(self):
        msg = USAGE_STRING + "\nAvailable commands:\n"
        for command in self.functions:
            msg += f"  {command}\n"
        return msg

    def parse_args(self, argv):
        if len(argv) < 2:
            print(self.usage_msg())
            sys.exit(1)

        command_name = argv[1]
        command = self.functions.get(command_name)
        if not command:
            print(self.usage_msg())
            sys.exit(2)

        try:
            kwargs = dict(arg.split("=") for arg in argv[2:])
        except ValueError:
            print(self.usage_msg())
            print("Invalid argument format. Expected <key>=<value>.")
            sys.exit(3)
        try:
            bound_args = command.sig.bind(**kwargs)
        except TypeError as e:
            print(self.usage_msg())
            print(f"Error: {e}")
            sys.exit(4)
        return command, bound_args

    def main(self):
        command, bound_args = self.parse_args(sys.argv)
        return command.func(*bound_args.args, **bound_args.kwargs)
