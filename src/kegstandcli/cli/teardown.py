"""Teardown command for Kegstand CLI."""

import subprocess  # nosec
from operator import itemgetter
from pathlib import Path

import click


@click.command()
@click.pass_context
@click.option("--region", default="eu-west-1", help="AWS region the stack is deployed to")
def teardown(ctx: click.Context, region: str) -> None:
    """Teardown the deployed AWS resources.

    Args:
        ctx: Click context
        region: AWS region where the stack is deployed
    """
    project_dir, config_file, verbose = itemgetter("project_dir", "config_file", "verbose")(ctx.obj)
    teardown_command(verbose, project_dir, config_file, region)


def teardown_command(verbose: bool, project_dir: str, config_file: str, region: str) -> None:
    """Execute the teardown process.

    Args:
        verbose: Whether to show verbose output
        project_dir: Path to the project directory
        config_file: Path to the configuration file
        region: AWS region where the stack is deployed
    """
    # Get the dir of the Kegstand CLI package itself (one level up from here)
    kegstandcli_dir = Path(__file__).parent.parent

    # Validate paths
    project_path = Path(project_dir)
    config_path = Path(config_file)
    if not project_path.is_dir():
        raise click.ClickException(f"Project directory not found: {project_dir}")
    if not config_path.is_file():
        raise click.ClickException(f"Config file not found: {config_file}")

    command = [
        "cdk",
        "destroy",
        "--app",
        "python infra/app.py",
        "--output",
        str(project_path / "cdk.out"),
        "--all",
        "--context",
        f"region={region}",
        "--context",
        f"project_dir={project_dir}",
        "--context",
        f"config_file={config_file}",
        "--context",
        f"verbose={verbose}",
        "--force",
    ]

    # Validate command
    if not all(isinstance(arg, str) for arg in command):
        raise click.ClickException("Invalid command arguments")

    # We use a fixed command list with validated paths, so we can safely ignore S603
    subprocess.run(  # noqa: S603
        command,
        cwd=str(kegstandcli_dir),
        check=True,
        shell=False,
    )
