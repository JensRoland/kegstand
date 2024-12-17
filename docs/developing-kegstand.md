# Developing the Kegstand CLI tool

The Kegstand CLI is published on PyPI as [kegstandcli](https://pypi.org/project/kegstandcli/). It is a Python package that provides a command-line interface for creating and deploying Kegstand services.

## Publish a new package version

To publish a new version of the Kegstand CLI, follow these steps:

1. Update the version number in `pyproject.toml` according to SemVer
2. Commit and push
3. Create a new release on GitHub (manually, with the same version number)
4. The `release-python` workflow will automatically build and publish the new version to PyPI
