"""Console output utilities for rich-formatted text."""

from contextlib import contextmanager
from enum import StrEnum
from typing import Generator

from rich.console import Console
from rich.markup import escape
from rich.theme import Theme

__all__: list[str] = ["Text", "cprint", "status"]


class Text(StrEnum):
    """Semantic color codes for styled console output."""

    ERROR = "error"
    WARNING = "warning"
    SUCCESS = "success"
    INFO = "info"
    DEBUG = "debug"
    HIGHLIGHT = "highlight"


_THEME = Theme(
    {
        Text.ERROR: "bold red",
        Text.WARNING: "bold yellow",
        Text.SUCCESS: "bold green",
        Text.INFO: "bold cyan",
        Text.DEBUG: "bold magenta",
        Text.HIGHLIGHT: "bold blue",
    }
)

_console = Console(theme=_THEME)


def cprint(
    text: str | list[tuple[str, str | None]], color: str | None = None, end: str = "\n"
) -> None:
    """Print colored text to the console using rich formatting.

    *text* can be a plain string or a list of ``(text, color)`` segments
    for mixed-colour output.
    """
    if isinstance(text, list):
        output = ""
        for segment_text, segment_color in text:
            if segment_color:
                output += f"[{segment_color}]{escape(segment_text)}[/{segment_color}]"
            else:
                output += escape(segment_text)
        _console.print(output, end=end)
    else:
        if color:
            _console.print(f"[{color}]{escape(text)}[/{color}]", end=end)
        else:
            _console.print(text, end=end)


@contextmanager
def status(message: str, spinner: str = "dots") -> Generator[None, None, None]:
    """Display a spinner with *message* while the wrapped block executes."""
    with _console.status(message, spinner=spinner):
        yield
