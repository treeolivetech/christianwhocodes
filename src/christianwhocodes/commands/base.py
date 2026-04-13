"""Base command infrastructure for CLI commands."""

from argparse import ArgumentParser, Namespace

from ..utils.enums import ExitCode

__all__: list[str] = ["BaseCommand"]


class BaseCommand:
    """Base class for all CLI commands.

    Subclass this and implement :attr:`prog`, :attr:`help`,
    :meth:`add_arguments`, and :meth:`handle` to define a command.
    Invoke the command by calling the instance with a list of CLI arguments.

    Example::

        class GreetCommand(BaseCommand):
            prog = "greet"
            help = "Say hello."

            def add_arguments(self, parser: ArgumentParser) -> None:
                parser.add_argument("name", help="Name to greet.")

            def handle(self, args: Namespace) -> ExitCode:
                print(f"Hello, {args.name}!")
                return ExitCode.SUCCESS


        exit_code = GreetCommand()(["Alice"])  # prints "Hello, Alice!"

    """

    prog: str = ""
    help: str = ""
    epilog: str = ""

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Register arguments onto the parser."""

    def create_parser(self) -> ArgumentParser:
        """Construct and return the argument parser."""
        parser = ArgumentParser(
            prog=self.prog, description=self.help, epilog=self.epilog
        )
        self.add_arguments(parser)
        return parser

    def handle(self, args: Namespace) -> ExitCode:
        """Execute the command logic with the parsed arguments."""
        raise NotImplementedError

    def __call__(self, argv: list[str]) -> ExitCode:
        """Parse ``argv`` and run the command."""
        return self.handle(self.create_parser().parse_args(argv))
