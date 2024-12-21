"""Utility functions for Kegstand CLI."""

from enum import Enum as PythonEnum
from pathlib import Path
from typing import Any

import click
from aws_cdk import aws_lambda as lambda_
from tomlkit import loads as parse_toml


class PackageManager(str, PythonEnum):
    """Package manager types."""

    POETRY = "Poetry"
    UV = "uv"

    def __str__(self) -> str:
        return self.value


class LambdaRuntime(str, PythonEnum):
    """Lambda runtime types."""

    PYTHON_3_10 = "python3.10"
    PYTHON_3_11 = "python3.11"
    PYTHON_3_12 = "python3.12"
    PYTHON_3_13 = "python3.13"

    def __str__(self) -> str:
        return self.value

    def to_lambda_runtime(self) -> lambda_.Runtime:
        return {
            LambdaRuntime.PYTHON_3_10: lambda_.Runtime.PYTHON_3_10,
            LambdaRuntime.PYTHON_3_11: lambda_.Runtime.PYTHON_3_11,
            LambdaRuntime.PYTHON_3_12: lambda_.Runtime.PYTHON_3_12,
            LambdaRuntime.PYTHON_3_13: lambda_.Runtime.PYTHON_3_13,
        }[self]


def find_resource_modules(api_src_dir: str) -> list[dict[str, Any]]:
    """Find API resource modules in the source directory.

    Expects a folder structure like this:
        api/
            [resource_name].py which exposes a resource object named `api`
        api/public/
            [resource_name].py which exposes a resource object named `api`

    Args:
        api_src_dir: Path to the API source directory

    Returns:
        list: List of dictionaries containing resource module information
    """
    resources = []

    api_folders = [
        {"name": "api", "resources_are_public": False},
        {"name": "api/public", "resources_are_public": True},
    ]

    # Loop over folders in api_src_dir and list the resource modules
    for api_folder in api_folders:
        api_folder_path = Path(api_src_dir) / str(api_folder["name"])
        if not api_folder_path.is_dir():
            click.echo(f"API source folder {api_folder_path} does not exist, skipping...")
            continue

        for file_path in api_folder_path.iterdir():
            # Ignore folders, only look at files
            if file_path.is_dir():
                continue

            # Skip dotfiles and special files
            if file_path.name.startswith((".", "__")) or file_path.name == "lambda.py":
                continue

            resource_name = file_path.stem
            resources.append(
                {
                    "name": resource_name,
                    "module_path": f"{str(api_folder['name']).replace('/', '.')}.{resource_name}",
                    "fromlist": [resource_name],
                    "is_public": api_folder["resources_are_public"],
                }
            )
    return resources


def hosted_zone_from_domain(domain: str) -> str:
    """Extract the hosted zone name from a domain.

    Args:
        domain: Full domain name (e.g., api.example.com)

    Returns:
        str: Hosted zone name (e.g., example.com)
    """
    return ".".join(domain.split(".")[-2:])


def get_pyproject_config(project_path: Path) -> dict[str, Any]:
    """Load and parse the pyproject.toml file.

    Args:
        project_path (Path): Path to the project directory

    Returns:
        dict: The parsed configuration
    """
    pyproject_path = project_path / "pyproject.toml"
    if not pyproject_path.exists():
        raise FileNotFoundError(f"pyproject.toml file not found in {project_path}")

    parsed_toml_config = parse_toml(pyproject_path.read_text(encoding="utf-8"))
    return parsed_toml_config


def identify_package_manager(project_path) -> PackageManager:
    """Identify the package manager used in the project.

    Args:
        project_path (Path): Path to the project directory

    Returns:
        PackageManager: The package manager used in the project (poetry or uv)
    """
    pyproject_config = get_pyproject_config(project_path)
    # If the pyproject.toml file contains a [tool.poetry] section, we assume
    # the project uses Poetry as the package manager
    if "tool" in pyproject_config and "poetry" in pyproject_config["tool"]:
        return PackageManager.POETRY

    return PackageManager.UV
