"""Type conversion utilities for common data transformations."""

from pathlib import Path
from typing import Any, Callable, cast

__all__: list[str] = ["TypeConverter"]


class TypeConverter:
    """Utility class for converting between common data types."""

    @staticmethod
    def to_bool(value: str | bool) -> bool:
        """Convert a string or bool to a boolean value."""
        if isinstance(value, bool):
            return value
        return value.lower() in ("true", "1", "yes", "on")

    @staticmethod
    def to_list_of_str(
        value: Any, transform: Callable[[str], str] | None = None
    ) -> list[str]:
        """Convert a value to a list of strings, with optional per-item transform."""
        result: list[str] = []
        if isinstance(value, list):
            list_value = cast(list[Any], value)
            result = [str(item) for item in list_value]
        elif isinstance(value, str):
            result = [item.strip() for item in value.split(",") if item.strip()]
        if transform:
            result = [transform(item) for item in result]
        return result

    @staticmethod
    def to_path(value: str | Path, resolve: bool = True) -> Path:
        """Convert a string or Path to a resolved :class:`~pathlib.Path`."""
        from os.path import expandvars

        if isinstance(value, str):
            path = Path(value)
        else:
            path = value
        if "~" in str(path):
            path = path.expanduser()
        path_str = str(path)
        if "$" in path_str:
            path = Path(expandvars(path_str))
        if resolve:
            path = path.resolve()
        return path
