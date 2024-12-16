"""Utility functions for Kegstand CLI."""

import os
from typing import Any

import click


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
        api_folder_full = os.path.join(api_src_dir, api_folder["name"])
        if not os.path.isdir(api_folder_full):
            click.echo(f"API source folder {api_folder_full} does not exist, skipping...")
            continue

        for file_descriptor in os.listdir(api_folder_full):
            # Ignore folders, only look at files
            if os.path.isdir(os.path.join(api_folder_full, file_descriptor)):
                continue

            # Skip dotfiles and special files
            if file_descriptor.startswith((".", "__")) or file_descriptor == "lambda.py":
                continue

            resource_name = os.path.splitext(file_descriptor)[0]
            resources.append(
                {
                    "name": resource_name,
                    "module_path": f"{api_folder['name'].replace('/', '.')}.{resource_name}",
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
