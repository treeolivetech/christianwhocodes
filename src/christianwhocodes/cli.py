"""CLI entry point for the christianwhocodes package."""

from argparse import ArgumentParser, Namespace
from sys import exit

from christianwhocodes.commands import CopyCommand, DeleteCommand, PlatformCommand, RandomStringCommand
from christianwhocodes.io.console import Text, cprint
from christianwhocodes.utils.enums import ExitCode
from christianwhocodes.utils.version import Version

_random_cmd = RandomStringCommand()
_copy_cmd = CopyCommand()
_platform_cmd = PlatformCommand()
_delete_cmd = DeleteCommand()


def handle_default(args: Namespace) -> ExitCode:
    """Handle default command when no subcommand is specified."""
    cprint("...but the people who know their God shall be strong and do exploits. — Daniel 11:32")
    return ExitCode.SUCCESS


def main() -> None:
    """Parse command-line arguments and execute the appropriate handler."""
    parser = ArgumentParser(prog="christianwhocodes", description="Dev Utilities")

    # 1. Global Metadata
    parser.add_argument("-v", "--version", action="version", version=Version.get("christianwhocodes")[0])
    parser.add_argument("-p", "--platform", action="store_true", default=False, help="Display platform information")
    parser.set_defaults(func=handle_default)  # Default if no subcommand

    subparsers = parser.add_subparsers(dest="command")

    # 2. Random String Command
    rand = subparsers.add_parser("random", aliases=["rand", "randomstring"], help=_random_cmd.help)
    _random_cmd.add_arguments(rand)
    rand.set_defaults(func=_random_cmd.handle)

    # 3. Copy Command
    copy = subparsers.add_parser("copy", help=_copy_cmd.help)
    _copy_cmd.add_arguments(copy)
    copy.set_defaults(func=_copy_cmd.handle)

    # 4. Delete Command
    delete = subparsers.add_parser("cleanup", aliases=["delete", "rm"], help=_delete_cmd.help)
    _delete_cmd.add_arguments(delete)
    delete.set_defaults(func=_delete_cmd.handle)

    # --- Execution Logic ---
    args = parser.parse_args()

    try:
        if args.platform:
            exit_code = _platform_cmd.handle(args)
        else:
            exit_code = args.func(args)
    except KeyboardInterrupt:
        cprint("\nOperation cancelled.", Text.WARNING)
        exit_code = ExitCode.ERROR
    except Exception as e:
        cprint(f"Error: {e}", Text.ERROR)
        exit_code = ExitCode.ERROR

    exit(exit_code)


if __name__ == "__main__":
    main()
