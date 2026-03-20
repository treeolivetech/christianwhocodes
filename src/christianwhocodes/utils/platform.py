"""Platform and architecture detection utilities."""

from platform import machine, system
from typing import Final

__all__: list[str] = ["Platform"]


class Platform:
    """Detect and expose the current OS and CPU architecture.

    Raises :class:`OSError` for unsupported operating systems and
    :class:`ValueError` for unsupported architectures.
    """

    _PLATFORM_MAP: Final[dict[str, str]] = {"darwin": "macos", "linux": "linux", "windows": "windows", "android": "android"}
    _ARCH_MAP: Final[dict[str, str]] = {
        "x86_64": "x64",
        "amd64": "x64",
        "x64": "x64",
        "arm64": "arm64",
        "aarch64": "arm64",
        "armv8": "arm64",
        "armv7l": "arm",
        "armv7": "arm",
        "armv6l": "arm",
    }

    def __init__(self) -> None:
        """Detect the current OS and architecture."""
        self.os_name = self._detect_os()
        self.architecture = self._detect_architecture()

    def _detect_os(self) -> str:
        system_platform = system().lower()
        platform_name = self._PLATFORM_MAP.get(system_platform)
        if not platform_name:
            supported = ", ".join(dict.fromkeys(self._PLATFORM_MAP.values()))
            raise OSError(f"Unsupported operating system: {system_platform}. Supported: {supported}")
        return platform_name

    def _detect_architecture(self) -> str:
        machine_platform = machine().lower()
        architecture = self._ARCH_MAP.get(machine_platform)
        if not architecture:
            raise ValueError(
                f"Unsupported architecture: {machine_platform}. Supported: {', '.join(set(self._ARCH_MAP.values()))}"
            )
        return architecture

    def __str__(self) -> str:
        """Return ``os_name-architecture`` string."""
        return f"{self.os_name}-{self.architecture}"

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"Platform(os_name={self.os_name!r}, architecture={self.architecture!r})"

    def __eq__(self, other: object) -> bool:
        """Check equality by OS name and architecture."""
        if not isinstance(other, Platform):
            return NotImplemented
        return self.os_name == other.os_name and self.architecture == other.architecture

    def __hash__(self) -> int:
        """Return a hash based on OS name and architecture."""
        return hash((self.os_name, self.architecture))
