# uv Publishing Guide

This document outlines the process for publishing the package to [PyPI](https://pypi.org/) and [TestPyPI](https://test.pypi.org/) using [`uv`](https://docs.astral.sh/uv/guides/package/) and [GitHub Actions Trusted Publishing](https://docs.pypi.org/trusted-publishers/adding-a-publisher/).

## Prerequisites: Trusted Publishing Setup

Instead of using hardcoded API tokens or passwords, this project uses **OpenID Connect (OIDC) Trusted Publishing**.

1. **GitHub Environments**: You need two environments configured in your GitHub repository settings (Settings > Environments):
   - `pypi`
   - `testpypi`
2. **PyPI / TestPyPI Setup**:
   - Go to your project on PyPI and TestPyPI.
   - Navigate to **Publishing** -> **Add a Trusted Publisher**.
   - Input the following details:
     - **Publisher Type**: GitHub
     - **Owner**: `<personal account / organization username>`
     - **Repository name**: `<repo name>`
     - **Workflow name**: `uv_publish.yaml` (or leave empty if allowing all workflows)
     - **Environment name**: Use exactly `pypi` for PyPI and `testpypi` for TestPyPI.

## Publishing Process

Publishing works entirely from your `pyproject.toml` version.

### 1. Bump the Version

Before publishing, ensure the application code is ready and update the version in `pyproject.toml`.
You can use `uv version` to bump the version automatically:

```bash
uv version --bump patch  # e.g., 1.5.1 -> 1.5.2
uv version --bump minor  # e.g., 1.5.1 -> 1.6.0
uv version --bump major --bump dev  # e.g., 1.6.0 -> 2.0.0.dev1
uv version 2.0.0         # Set explicitly
```

Commit this change and push it to GitHub:

```bash
git add pyproject.toml
git commit -m "Bump version to 1.5.2"
git push
```

### 2. Trigger the Workflow

The `uv Publish to PyPI or TestPyPI` GitHub Action workflow (`.github/workflows/uv_publish.yaml`) dictates how builds propagate:

#### Option A: Manual Release (Recommended for TestPyPI)

You can manually trigger a release from the **Actions** tab on GitHub:

1. Go to the Actions tab and select **uv Publish to PyPI or TestPyPI**.
2. Click **Run workflow**.
3. Select your desired branch (usually `main`).
4. Select the target index: `pypi` or `testpypi`.
5. Click **Run workflow**.

_(Note: We highly recommend publishing to `testpypi` first via this method whenever introducing major changes, just to ensure the package builds right!)_

When you manually choose either `pypi` or `testpypi`, the workflow checks your `pyproject.toml` version, computes the corresponding tag (`v<version>`), and pushes that tag only if it does not already exist on `origin`.
The workflow then continues to build and publish in the same run.

Because this tag push happens from inside GitHub Actions, it is not expected to retrigger a second workflow run when using the default GitHub token.

#### Option B: Automatic Release (on Push/Tag)

The workflow is also configured to run automatically and publish to PyPI if you push a version tag matching `v*.*.*`. Note that development releases (tags matching `v*.*.*.dev*`) are explicitly ignored and will not be published.

We have provided an automated script that uses the project's internal tools to read your version and trigger the entire tagging process:

```bash
# When run from the root directory
uv run .github/triggers/uv_publish.py
```

Before running the local trigger script, sync remote tags so your local tag state is current:

```bash
git fetch --tags --prune
```

The trigger script now also performs this `git fetch --tags --prune` step automatically before creating the version tag, but running the command manually is still a good habit when preparing a release.

This tiny Python script will locally grab your version matching your currently committed `pyproject.toml`, tag it, and instantly upload that tag to trigger the publishing pipeline.

Whenever triggered automatically via this automation script, the workflow defaults to using the **`pypi`** environment and publishes directly to the official PyPI registry.

### 3. Verification

Once the action succeeds:

- **PyPI**: View your package at `https://pypi.org/project/<package_name>/`
- **TestPyPI**: View your package at `https://test.pypi.org/project/<package_name>/`

To test installing your newly published package from TestPyPI:

```bash
uv pip install -i https://test.pypi.org/simple/ package_name
```
