"""Cryptographically secure random string generation."""

from string import ascii_letters, digits

__all__: list[str] = ["generate_random_string"]


def generate_random_string(
    length: int = 32, charset: str = ascii_letters + digits
) -> str:
    """Generate a cryptographically secure random string.

    Uses :mod:`secrets` for secure randomness.
    """
    if length <= 0:
        raise ValueError("length must be positive")

    from secrets import choice

    return "".join(choice(charset) for _ in range(length))
