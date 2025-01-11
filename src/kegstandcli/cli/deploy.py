"""Deploy command for Kegstand CLI."""

import subprocess  # nosec
from operator import itemgetter
from pathlib import Path

import click

from kegstandcli.cli.build import build_command


@click.command()
@click.pass_context
@click.option("--region", default="eu-west-1", help="AWS region to deploy to")
@click.option(
    "--hotswap",
    is_flag=True,
    default=False,
    help="Attempt to deploy without creating a new CloudFormation stack",
)
@click.option(
    "--skip-build",
    is_flag=True,
    default=False,
    help="Skip building the project before deploying",
)
def deploy(ctx: click.Context, region: str, hotswap: bool, skip_build: bool) -> None:
    """Deploy the project to AWS.

    Args:
        ctx: Click context
        region: AWS region to deploy to
        hotswap: Whether to attempt deployment without creating a new CloudFormation stack
        skip_build: Whether to skip building the project before deploying
    """
    project_dir, config_file, config, verbose = itemgetter(
        "project_dir", "config_file", "config", "verbose"
    )(ctx.obj)
    if config is None:
        click.Abort("Config file not found.")

    if not skip_build:
        build_command(verbose, project_dir, config)

    deploy_command(verbose, project_dir, config_file, region, hotswap)


def deploy_command(
    verbose: bool, project_dir: str, config_file: str, region: str, hotswap: bool
) -> None:
    """Execute the deployment process.

    Args:
        verbose: Whether to show verbose output
        project_dir: Path to the project directory
        config_file: Path to the configuration file
        region: AWS region to deploy to
        hotswap: Whether to attempt deployment without creating a new CloudFormation stack
    """
    # Get the dir of the kegstandcli package (one level up from here)
    kegstandcli_dir = Path(__file__).parent.parent

    # Validate paths
    project_path = Path(project_dir)
    config_path = Path(config_file)
    if not project_path.is_dir():
        raise click.ClickException(f"Project directory not found: {project_dir}")
    if not config_path.is_file():
        raise click.ClickException(f"Config file not found: {config_file}")

    click.echo("Deploying...")
    command = [
        "cdk",
        "deploy",
        "--app",
        "python infra/app.py",
        "--output",
        str(project_path / "cdk.out"),
        "--all",
        "--outputs-file",
        str(project_path / ".stack-outputs.json"),
        "--context",
        f"region={region}",
        "--context",
        f"project_dir={project_path.absolute()}",
        "--context",
        f"config_file={config_file}",
        "--context",
        f"verbose={verbose}",
        "--require-approval",
        "never",
    ]
    if hotswap:
        command.append("--hotswap")
    if verbose:
        command.append("--verbose")

    # Validate command
    if not all(isinstance(arg, str) for arg in command):
        raise click.ClickException("Invalid command arguments")

    # We use a fixed command list with validated paths, so we can safely ignore S603
    subprocess.run(  # noqa: S603
        command,
        cwd=str(kegstandcli_dir),
        check=True,
        shell=False,
        stdout=subprocess.DEVNULL if not verbose else None,
    )
    click.echo("Finished deploying application!")
