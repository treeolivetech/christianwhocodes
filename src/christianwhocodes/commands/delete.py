"""CLI utility to delete files or folders by name using BaseCommand."""

from __future__ import annotations

import shutil
from argparse import ArgumentParser, Namespace
from pathlib import Path

from ..utils import ExitCode
from . import BaseCommand


class DeleteCommand(BaseCommand):
    """Delete a file or folder from a target directory."""

    prog = "cleanup"
    help = "Delete a file or folder from a directory."
    epilog = "Examples: cleanup --file app.log --recursive | cleanup --folder build --dir ./dist"

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Register CLI arguments for the command."""
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--file", dest="file_name", help="File name/path to delete.")
        group.add_argument(
            "--folder", dest="folder_name", help="Folder name/path to delete."
        )

        parser.add_argument(
            "--dir",
            dest="base_dir",
            default=".",
            help="Directory to search from (default: current working directory).",
        )
        parser.add_argument(
            "--recursive",
            action="store_true",
            help="Search and delete matches inside subdirectories.",
        )
        parser.add_argument(
            "--verbose", action="store_true", help="Print each deleted file or folder."
        )

    def handle(self, args: Namespace) -> ExitCode:
        """Delete the requested target and return the appropriate exit code."""
        base_dir = Path(args.base_dir).resolve()
        if not base_dir.exists() or not base_dir.is_dir():
            print(f"Directory not found: {base_dir}")
            return ExitCode.ERROR

        target = args.file_name or args.folder_name
        assert target is not None
        targets = self._resolve_targets(
            base_dir=base_dir, target=target, recursive=args.recursive
        )

        if args.file_name:
            deleted = self._delete_files(targets, args.verbose)
            target_kind = "file"
        else:
            deleted = self._delete_folders(targets, args.verbose)
            target_kind = "folder"

        if deleted == 0:
            recursive_suffix = " recursively" if args.recursive else ""
            print(
                f"No matching {target_kind} found for '{target}' in {base_dir}{recursive_suffix}."
            )
            return ExitCode.ERROR

        print(f"Deleted {deleted} {target_kind}(s).")
        return ExitCode.SUCCESS

    def _resolve_targets(
        self, base_dir: Path, target: str, recursive: bool
    ) -> list[Path]:
        """Resolve target paths relative to base_dir.

        If target contains path separators, it is treated as a relative path from base_dir.
        Otherwise, it is matched by name in base_dir (or recursively when requested).
        """
        target_path = Path(target)
        if target_path.parts and len(target_path.parts) > 1:
            candidate = (base_dir / target_path).resolve()
            return [candidate] if candidate.exists() else []

        if recursive:
            return [path for path in base_dir.rglob(target) if path.exists()]

        candidate = (base_dir / target).resolve()
        return [candidate] if candidate.exists() else []

    def _delete_files(self, paths: list[Path], verbose: bool) -> int:
        deleted = 0
        for path in paths:
            if path.is_file() or path.is_symlink():
                path.unlink(missing_ok=False)
                if verbose:
                    print(f"Deleted file: {path}")
                deleted += 1
        return deleted

    def _delete_folders(self, paths: list[Path], verbose: bool) -> int:
        deleted = 0
        for path in sorted(paths, key=lambda p: len(p.parts), reverse=True):
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
                if verbose:
                    print(f"Deleted folder: {path}")
                deleted += 1
        return deleted
