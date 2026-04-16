"""Configuration file parsing utilities."""

from pathlib import Path
from typing import Any

__all__: list[str] = ["PyProject"]


class PyProject:
    """Read-only view of data from a ``pyproject.toml`` file."""

    def __init__(self, toml_path: Path) -> None:
        """Parse *toml_path* and expose its ``[project]`` section."""
        from tomllib import load

        self._toml_path = toml_path

        with open(toml_path, "rb") as f:
            full_data = load(f)
        self._data: dict[str, Any] = full_data

    @property
    def name(self) -> str:
        """Return the project name."""
        return self._data["project"]["name"]

    @property
    def version(self) -> str:
        """Return the project version."""
        return self._data["project"]["version"]

    @property
    def description(self) -> str | None:
        """Return the project description, if any."""
        return self._data["project"].get("description")

    @property
    def authors(self) -> list[dict[str, str]]:
        """Return the list of project authors."""
        return self._data["project"].get("authors", [])

    @property
    def dependencies(self) -> list[str]:
        """Return the list of project dependencies."""
        return self._data["project"].get("dependencies", [])

    @property
    def python_requires(self) -> str | None:
        """Return the required Python version specifier."""
        return self._data["project"].get("requires-python")

    @property
    def data(self) -> dict[str, Any]:
        """Return the full parsed TOML data."""
        return self._data

    @property
    def path(self) -> Path:
        """Return the path to the parsed ``pyproject.toml`` file."""
        return self._toml_path
