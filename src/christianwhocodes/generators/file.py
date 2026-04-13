"""Configuration file generators for common developer tools."""

from dataclasses import dataclass
from pathlib import Path

from ..io.console import Text, cprint
from ..utils.enums import PostgresFilename
from ..utils.platform import Platform

__all__: list[str] = [
    "FileSpec",
    "get_pg_service_spec",
    "get_pgpass_spec",
    "get_ssh_config_spec",
    "FileGenerator",
]


@dataclass
class FileSpec:
    """Defines the path, content, and security requirements of a config file."""

    path: Path
    content: str
    chmod_mode: int | None = None


def _pg_base_path() -> Path:
    """Return the platform-specific base directory for PostgreSQL config files."""
    from os import getenv

    if Platform().os_name == "windows":
        appdata = getenv("APPDATA", str(Path.home()))
        return Path(appdata) / "postgresql"
    return Path.home()


def get_pg_service_spec() -> FileSpec:
    """Return the FileSpec for a PostgreSQL service connection file."""
    content = (
        "# Read more: https://www.postgresql.org/docs/current/libpq-pgservice.html\n\n"
        "[mydb]\n"
        "host=localhost\n"
        "port=5432\n"
        "dbname=postgres\n"
        "user=postgres\n"
    )
    return FileSpec(
        path=_pg_base_path() / PostgresFilename.PGSERVICE.value, content=content
    )


def get_pgpass_spec() -> FileSpec:
    """Return the FileSpec for a PostgreSQL password file."""
    from stat import S_IRUSR, S_IWUSR

    is_win = Platform().os_name == "windows"
    filename = PostgresFilename.PGPASS.value
    content = "# Read more: https://www.postgresql.org/docs/current/libpq-pgpass.html\n\n# hostname:port:database:username:password\n"
    mode = None if is_win else (S_IRUSR | S_IWUSR)
    return FileSpec(path=_pg_base_path() / filename, content=content, chmod_mode=mode)


def get_ssh_config_spec() -> FileSpec:
    """Return the FileSpec for an SSH client configuration file."""
    content = (
        "# Read more: https://linux.die.net/man/5/ssh_config\n\n"
        "Host my_host_alias\n"
        "    IdentityFile ~/.ssh/id_rsa\n"
        "    User my_user\n"
        "    HostName my_domain_or_ip_address\n"
    )
    return FileSpec(path=Path.home() / ".ssh" / "config", content=content)


class FileGenerator:
    """Write a :class:`FileSpec` to disk, applying permissions if specified."""

    def __init__(self, spec: FileSpec, verbose: bool = False) -> None:
        """Create a generator for the given *spec*."""
        self.spec = spec
        self.verbose = verbose

    def create(self, overwrite: bool = False) -> None:
        """Write the file to disk, applying permissions if specified."""
        if not self._file_needs_content():
            if not self._confirm_overwrite(overwrite):
                if self.verbose:
                    cprint(
                        f"Skipped {self.spec.path} (exists and overwrite declined).",
                        Text.INFO,
                    )
                return
            if self.verbose:
                cprint(f"Overwriting existing file: {self.spec.path}", Text.WARNING)
        else:
            if self.verbose:
                cprint(f"Creating new file: {self.spec.path}", Text.INFO)

        self.spec.path.parent.mkdir(parents=True, exist_ok=True)
        self.spec.path.write_text(self.spec.content, encoding="utf-8")

        if self.verbose:
            cprint(f"✓ File written to {self.spec.path}", Text.SUCCESS)

        if self.spec.chmod_mode is not None:
            try:
                self.spec.path.chmod(self.spec.chmod_mode)
                octal_mode = oct(self.spec.chmod_mode)[2:]
                if self.verbose:
                    cprint(
                        f"✓ Permissions secured for {self.spec.path} ({octal_mode})",
                        Text.SUCCESS,
                    )
            except Exception as e:
                cprint(
                    f"Error: could not set permissions on {self.spec.path}: {e}",
                    Text.ERROR,
                )

    def _file_needs_content(self) -> bool:
        """Return True if the file does not exist or is empty."""
        return not self.spec.path.exists() or self.spec.path.stat().st_size == 0

    def _confirm_overwrite(self, overwrite: bool) -> bool:
        """Return True if it is safe to overwrite an existing non-empty file."""
        if overwrite:
            return True

        for _ in range(3):
            cprint(f"'{self.spec.path}' exists and is not empty", Text.WARNING)
            resp = input("overwrite? [y/N]: ").strip().lower()
            if resp in ("y", "yes"):
                return True
            if resp in ("n", "no", ""):
                cprint("Aborted.", Text.WARNING)
                return False
            cprint("Please answer with 'y' or 'n'.", Text.INFO)

        cprint("Too many invalid responses. Aborted.", Text.WARNING)
        return False
