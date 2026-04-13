"""Random string generation command."""

from argparse import ArgumentParser, Namespace

from ..generators.random import generate_random_string
from ..io.console import Text, cprint, status
from ..utils.enums import ExitCode
from .base import BaseCommand

__all__: list[str] = ["RandomStringCommand"]


class RandomStringCommand(BaseCommand):
    """Generate a cryptographically secure random string.

    Creates a random string of the specified length and optionally copies
    it to the clipboard for easy pasting.

    Example::

        $ christianwhocodes random -l 16
        Generated: aB3dEf7gHi9jKl2m
        Copied to clipboard!

    """

    prog = "random"
    help = "Random string generator"

    def add_arguments(self, parser: ArgumentParser) -> None:  # noqa: D102
        parser.add_argument("-l", "--length", type=int, default=16)
        parser.add_argument(
            "--no-clipboard",
            dest="no_clipboard",
            action="store_true",
            default=False,
            help="Skip copying to clipboard",
        )

    def handle(self, args: Namespace) -> ExitCode:  # noqa: D102
        with status("Generating secure random string..."):
            random_str = generate_random_string(length=args.length)

        cprint([("✓ Generated: ", Text.SUCCESS), (random_str, Text.HIGHLIGHT)])

        if not args.no_clipboard:
            try:
                from pyperclip import copy

                copy(random_str)
                cprint("✓ Copied to clipboard!", Text.SUCCESS)
            except Exception as e:
                cprint(f"Could not copy to clipboard: {e}", Text.WARNING)

        return ExitCode.SUCCESS
