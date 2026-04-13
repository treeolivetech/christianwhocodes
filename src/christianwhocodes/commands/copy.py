"""File and directory copy command."""

from argparse import ArgumentParser, Namespace

from ..io.filesystem import copy_path
from ..utils.enums import ExitCode
from .base import BaseCommand

__all__: list[str] = ["CopyCommand"]


class CopyCommand(BaseCommand):
    """Copy files or directories from source to destination.

    Automatically detects whether the source is a file or directory and
    performs the appropriate copy operation with progress feedback.

    Example::

        $ christianwhocodes copy -i ./src -o ./backup/src
        Directory copied successfully from ./src to ./backup/src

    """

    prog = "copy"
    help = "Copy files/dirs"

    def add_arguments(self, parser: ArgumentParser) -> None:  # noqa: D102
        parser.add_argument("-i", "--input", "--source", dest="source", required=True)
        parser.add_argument(
            "-o", "--output", "--destination", dest="destination", required=True
        )

    def handle(self, args: Namespace) -> ExitCode:  # noqa: D102
        success = copy_path(args.source, args.destination)
        return ExitCode.SUCCESS if success else ExitCode.ERROR
