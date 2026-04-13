"""Version management and retrieval utilities."""

from typing import Literal, NamedTuple

from .enums import ExitCode

__all__: list[str] = ["Version", "VersionResult", "print_version"]


class VersionResult(NamedTuple):
    """Holds a version string and an optional error message."""

    version: str
    error: str


class Version:
    """Look up installed package versions via ``importlib.metadata``."""

    @staticmethod
    def placeholder() -> Literal["X.Y.Z"]:
        """Return a placeholder string for unknown versions."""
        return "X.Y.Z"

    @staticmethod
    def get(package: str) -> VersionResult:
        """Return the installed version of *package*, or a placeholder on failure."""
        try:
            from importlib.metadata import version

            return VersionResult(version(package), "")
        except Exception as e:
            return VersionResult(
                Version.placeholder(), f"Could not determine version\n{e}"
            )


def print_version(package: str) -> ExitCode:
    """Print the version of *package* and return an appropriate exit code."""
    from ..io.console import cprint

    version_string, error_msg = Version.get(package)
    if version_string != Version.placeholder():
        cprint(version_string)
        return ExitCode.SUCCESS
    else:
        cprint(
            f"{version_string}: Could not determine version for package '{package}'."
        )
        if error_msg:
            cprint(error_msg)
        return ExitCode.ERROR
