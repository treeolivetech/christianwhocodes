"""uv Publish to PyPI or TestPyPI action workflow trigger.

This reads the version from pyproject.toml, creates a git tag, and pushes it to the origin repository.
The tag is expected to trigger the uv publish workflow, which will handle the actual publishing to PyPI or TestPyPI based on the tag and branch conditions defined in that workflow.
"""

from pathlib import Path
from subprocess import CalledProcessError, run
from sys import exit, stderr

from christianwhocodes import ExitCode, PyProject

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


def tag_and_push() -> None:
    """Execute the extraction, tagging, and pushing sequence."""
    pyproject_path = ROOT_DIR / "pyproject.toml"

    if not pyproject_path.exists():
        print(f"Error: {pyproject_path.name} not found.", file=stderr)
        exit(ExitCode.ERROR)

    # Get the version
    project = PyProject(pyproject_path)
    version = project.version
    tag = f"v{version}"

    print("Fetching remote tags to sync local tag state...")
    try:
        run(["git", "fetch", "--tags", "--prune"], check=True)
    except CalledProcessError:
        print("Error: Failed to fetch and prune tags from origin.", file=stderr)
        exit(ExitCode.ERROR)

    print(f"Read version '{version}' from pyproject.toml")
    print(f"Creating git tag: {tag}")

    try:
        # Create the git tag
        run(["git", "tag", tag], check=True)
    except CalledProcessError:
        print(
            f"Error: Failed to create git tag '{tag}'. Does it already exist?",
            file=stderr,
        )
        exit(ExitCode.ERROR)

    print(f"Pushing tag '{tag}' to origin...")
    try:
        # Push the tag online
        run(["git", "push", "origin", tag], check=True)
        print("Successfully pushed tag!")
    except CalledProcessError:
        print(f"Error: Failed to push tag '{tag}' to origin.", file=stderr)
        exit(ExitCode.ERROR)


if __name__ == "__main__":
    tag_and_push()
