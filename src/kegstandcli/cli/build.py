"""Build command for Kegstand CLI."""

import os
import shutil
import subprocess  # nosec
from operator import itemgetter
from typing import Any

import click


@click.command()
@click.pass_context
def build(ctx: click.Context) -> None:
    """Build the project for deployment."""
    project_dir, config, verbose = itemgetter("project_dir", "config", "verbose")(ctx.obj)
    build_command(verbose, project_dir, config)


def build_command(verbose: bool, project_dir: str, config: dict[str, Any]) -> None:
    """Execute the build process for the project.

    Args:
        verbose: Whether to show verbose output
        project_dir: Path to the project directory
        config: Project configuration dictionary
    """
    # Create a directory to hold the build artifacts, and make sure it is empty
    build_dir = create_empty_folder(project_dir, "dist")

    # Handle the different types ('modules') of build
    if "api_gateway" in config:
        build_api_gateway(
            config, verbose, project_dir, create_empty_folder(build_dir, "api_gw_src")
        )
    if "api" in config:
        build_api(config, verbose, project_dir, create_empty_folder(build_dir, "api_src"))
    click.echo("Finished building application!")


def build_api_gateway(
    config: dict[str, Any],  # noqa: ARG001
    verbose: bool,  # noqa: ARG001
    project_dir: str,  # noqa: ARG001
    module_build_dir: str,
) -> None:
    """Build the API Gateway module.

    Args:
        config: Project configuration dictionary
        verbose: Whether to show verbose output
        project_dir: Path to the project directory
        module_build_dir: Directory to build the module in
    """
    create_empty_folder(module_build_dir, "api")

    # Inject health check endpoint
    lambda_file = os.path.join(module_build_dir, "api", "lambda.py")
    shutil.copyfile(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "rest_api_gateway_health_check.py.tmpl",
        ),
        lambda_file,
    )


def build_api(
    config: dict[str, Any], verbose: bool, project_dir: str, module_build_dir: str
) -> None:
    """Build the API module.

    Args:
        config: Project configuration dictionary
        verbose: Whether to show verbose output
        project_dir: Path to the project directory
        module_build_dir: Directory to build the module in
    """
    # Copy everything in the project_dir/src folder to the module_build_dir
    src_dir = os.path.join(project_dir, "src")
    shutil.copytree(src_dir, module_build_dir, dirs_exist_ok=True)

    # If using the default entrypoint but the lambda.py file doesn't exist,
    # we inject it (this is just a convenience for the user)
    if config["api"]["entrypoint"] == "api.lambda.handler":
        lambda_file = os.path.join(module_build_dir, "api", "lambda.py")
        if not os.path.exists(lambda_file):
            if verbose:
                click.echo("No lambda.py file in api folder, using default")
            shutil.copyfile(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "default_lambda.py.tmpl"),
                lambda_file,
            )

    # Export the dependencies to a requirements.txt file
    click.echo("Exporting service dependencies to requirements.txt file...")
    export_command = [
        "uv",
        "pip",
        "compile",
        "--exclude-extras",
        "dev",
        "--exclude-extras",
        "lambda-builtins",
        "-o",
        f"{module_build_dir}/requirements.txt",
        ".",
    ]
    if verbose:
        export_command.append("--verbose")

    subprocess.run(  # noqa: S603
        export_command,
        check=True,
        shell=False,
        stdout=subprocess.DEVNULL if not verbose else None,
        cwd=project_dir,
    )

    # Install the dependencies to the build folder using pip
    click.echo("Installing dependencies in module build folder...")
    install_command = [
        "uv",
        "pip",
        "install",
        "-r",
        f"{module_build_dir}/requirements.txt",
        "--target",
        module_build_dir,
    ]
    subprocess.run(  # noqa: S603
        install_command,
        check=True,
        shell=False,
        stdout=subprocess.DEVNULL if not verbose else None,
        cwd=project_dir,
    )


def create_empty_folder(parent_folder: str, folder_name: str) -> str:
    """Create an empty folder, removing it first if it exists.

    Args:
        parent_folder: Path to the parent directory
        folder_name: Name of the folder to create

    Returns:
        str: Path to the created folder

    Raises:
        ValueError: If folder_name is empty
    """
    if folder_name == "":
        raise ValueError("folder_name cannot be empty")

    folder_path = os.path.join(parent_folder, folder_name)
    shutil.rmtree(folder_path, ignore_errors=True)
    os.makedirs(folder_path, exist_ok=True)

    return folder_path
