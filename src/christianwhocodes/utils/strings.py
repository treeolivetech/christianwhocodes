"""String and URL manipulation utilities."""

from typing import Any, Iterable

__all__: list[str] = ["max_length_from_choices", "normalize_url_path"]


def max_length_from_choices(choices: Iterable[tuple[str, Any]]) -> int:
    """Return the maximum string length from a list of choice pairs."""
    return max((len(choice[0]) for choice in choices), default=0)


def normalize_url_path(
    url: str, leading_slash: bool = False, trailing_slash: bool = True
) -> str:
    """Normalize a URL path by ensuring consistent slash usage.

    Collapses duplicate slashes and optionally adds or strips leading and
    trailing slashes.
    """
    if not url:
        return "/"
    while "//" in url:
        url = url.replace("//", "/")
    if leading_slash and not url.startswith("/"):
        url = "/" + url
    elif not leading_slash and url.startswith("/"):
        url = url.lstrip("/")
    if trailing_slash and not url.endswith("/"):
        url = url + "/"
    elif not trailing_slash and url.endswith("/"):
        url = url.rstrip("/")
    return url or "/"
