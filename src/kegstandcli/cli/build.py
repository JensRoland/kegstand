"""Build command for Kegstand CLI."""

import shutil
import subprocess  # nosec
from operator import itemgetter
from pathlib import Path
from typing import Any

import click

from kegstandcli.utils import PackageManager, identify_package_manager


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
    lambda_file = Path(module_build_dir) / "api" / "lambda.py"
    shutil.copyfile(
        Path(__file__).parent / "rest_api_gateway_health_check.py.tmpl",
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
    src_dir = Path(project_dir) / "src"
    shutil.copytree(src_dir, module_build_dir, dirs_exist_ok=True)

    # If using the default entrypoint but the lambda.py file doesn't exist,
    # we inject it (this is just a convenience for the user)
    if config["api"]["entrypoint"] == "api.lambda.handler":
        lambda_file = Path(module_build_dir) / "api" / "lambda.py"
        if not lambda_file.exists():
            if verbose:
                click.echo("No lambda.py file in api folder, using default")
            shutil.copyfile(
                Path(__file__).parent / "default_lambda.py.tmpl",
                lambda_file,
            )

    # Export the dependencies to a requirements.txt file
    package_manager: PackageManager = identify_package_manager(Path(project_dir))
    click.echo(
        f"Exporting service dependencies to requirements.txt file using {package_manager}..."
    )
    requirements_file: Path
    if package_manager == PackageManager.POETRY:
        requirements_file = _compile_requirements_with_poetry(
            project_dir, module_build_dir, verbose
        )
    elif package_manager == PackageManager.UV:
        requirements_file = _compile_requirements_with_uv(project_dir, module_build_dir, verbose)
    else:
        raise ValueError(f"Invalid package manager: {package_manager}")

    # Install the dependencies to the build folder using pip
    click.echo("Installing dependencies in module build folder...")
    install_command: list[str]
    if package_manager == PackageManager.POETRY:
        install_command = _format_install_command_with_poetry(module_build_dir, requirements_file)
    elif package_manager == PackageManager.UV:
        install_command = _format_install_command_with_uv(module_build_dir, requirements_file)
    else:
        raise ValueError(f"Invalid package manager: {package_manager}")

    subprocess.run(  # noqa: S603
        install_command,
        check=True,
        shell=False,
        stdout=subprocess.DEVNULL if not verbose else None,
        cwd=project_dir,
    )


def _compile_requirements_with_uv(project_dir: str, module_build_dir: str, verbose: bool) -> Path:
    """Compile the project dependencies to a requirements.txt file.

    Args:
        project_dir: Path to the project directory
        module_build_dir: Path to the module build directory (e.g. `/dist/api_src/`)
        verbose: Whether to show verbose output

    Returns:
        Path: Path to the requirements.txt file
    """
    requirements_file = Path(module_build_dir) / "requirements.txt"
    export_command = [
        "uv",
        "pip",
        "compile",
        str(Path(project_dir) / "pyproject.toml"),
        "-o",
        str(requirements_file),
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

    return requirements_file


def _compile_requirements_with_poetry(
    project_dir: str, module_build_dir: str, verbose: bool
) -> Path:
    """Compile the project dependencies to a requirements.txt file using Poetry.

    Args:
        project_dir: Path to the project directory
        module_build_dir: Path to the module build directory (e.g. `/dist/api_src/`)
        verbose: Whether to show verbose output

    Returns:
        Path: Path to the requirements.txt file
    """
    requirements_file = Path(module_build_dir) / "requirements.txt"
    export_command = [
        "poetry",
        "export",
        "-o",
        str(requirements_file),
        # "--without=dev",
        # "--without=lambda-builtins",
        "--without-hashes",
    ]
    if verbose:
        export_command.append("-vv")
    else:
        export_command.append("-q")

    subprocess.run(  # noqa: S603
        export_command,
        check=True,
        cwd=project_dir,
    )

    return requirements_file


def _format_install_command_with_uv(module_build_dir: str, requirements_file: Path) -> list[str]:
    return [
        "uv",
        "pip",
        "install",
        "-r",
        str(requirements_file),
        "--target",
        module_build_dir,
    ]


def _format_install_command_with_poetry(
    module_build_dir: str, requirements_file: Path
) -> list[str]:
    return [
        "pip",
        "install",
        "-r",
        str(requirements_file),
        "-t",
        module_build_dir,
    ]


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

    folder_path = Path(parent_folder) / folder_name
    if folder_path.exists():
        shutil.rmtree(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)

    return str(folder_path)
