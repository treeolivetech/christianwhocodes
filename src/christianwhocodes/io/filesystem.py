"""Filesystem operations for copying files and directories."""

from abc import ABC, abstractmethod
from pathlib import Path
from shutil import copy2, copytree, rmtree
from typing import TypeAlias

from .console import Text, cprint, status

__all__: list[str] = ["Copier", "FileCopier", "DirectoryCopier", "copy_path"]

_PathLike: TypeAlias = str | Path


class Copier(ABC):
    """Abstract base class for copy operations."""

    @abstractmethod
    def copy(self, source: Path, destination: Path) -> bool:
        """Copy *source* to *destination*, returning ``True`` on success."""
        ...

    def _validate_source(self, source: Path) -> bool:
        if not source.exists():
            cprint(f"Source path does not exist: {source}", Text.ERROR)
            return False
        return True


class FileCopier(Copier):
    """Copier for individual files."""

    def copy(self, source: Path, destination: Path) -> bool:  # noqa: D102
        if not self._validate_source(source):
            return False
        if not source.is_file():
            cprint(f"Source is not a file: {source}", Text.ERROR)
            return False
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            with status(f"Copying file {source.name}..."):
                copy2(source, destination)
            cprint(
                [
                    ("✓ File copied successfully from ", Text.SUCCESS),
                    (str(source), Text.HIGHLIGHT),
                    (" to ", Text.SUCCESS),
                    (str(destination), Text.HIGHLIGHT),
                ]
            )
            return True
        except PermissionError:
            cprint(
                "Permission denied. Check read/write permissions for source and destination.",
                Text.ERROR,
            )
            return False
        except Exception as e:
            cprint(f"Failed to copy file: {type(e).__name__}: {e}", Text.ERROR)
            return False


class DirectoryCopier(Copier):
    """Copier for directories with all their contents."""

    def copy(self, source: Path, destination: Path) -> bool:  # noqa: D102
        if not self._validate_source(source):
            return False
        if not source.is_dir():
            cprint(f"Source is not a directory: {source}", Text.ERROR)
            return False
        try:
            if destination.exists():
                if not self._prompt_overwrite(destination):
                    cprint("Copy aborted.", Text.WARNING)
                    return False
                rmtree(destination)
            with status(f"Copying directory {source.name}..."):
                copytree(source, destination, dirs_exist_ok=False)
            cprint(
                [
                    ("✓ Directory copied successfully from ", Text.SUCCESS),
                    (str(source), Text.HIGHLIGHT),
                    (" to ", Text.SUCCESS),
                    (str(destination), Text.HIGHLIGHT),
                ]
            )
            return True
        except PermissionError:
            cprint(
                "Permission denied. Check read/write permissions for source and destination.",
                Text.ERROR,
            )
            return False
        except Exception as e:
            cprint(f"Failed to copy directory: {type(e).__name__}: {e}", Text.ERROR)
            return False

    def _prompt_overwrite(self, destination: Path) -> bool:
        cprint(f"\n{destination} already exists.", Text.WARNING)
        response = input("Overwrite? [y/N]: ").strip().lower()
        return response == "y"


def copy_path(source: _PathLike, destination: _PathLike) -> bool:
    """Copy a file or directory from *source* to *destination*.

    Automatically detects whether the source is a file or directory.
    """
    from ..utils.converters import TypeConverter

    source_path = TypeConverter.to_path(source)
    dest_path = TypeConverter.to_path(destination)

    copier: Copier

    if source_path.is_file():
        copier = FileCopier()
    elif source_path.is_dir():
        copier = DirectoryCopier()
    else:
        if not source_path.exists():
            cprint(f"Source path does not exist: {source_path}", Text.ERROR)
        else:
            cprint(
                f"Source is neither a file nor a directory: {source_path}", Text.ERROR
            )
        return False

    return copier.copy(source_path, dest_path)
