import os
import subprocess  # nosec
from operator import itemgetter

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
def deploy(ctx, region, hotswap, skip_build):
    project_dir, config_file, verbose = itemgetter(
        "project_dir", "config_file", "verbose"
    )(ctx.obj)
    if not skip_build:
        build_command(verbose, project_dir, config_file)

    deploy_command(verbose, project_dir, config_file, region, hotswap)


def deploy_command(verbose, project_dir, config_file, region, hotswap):
    # Get the dir of the kegstandcli package (one level up from here)
    kegstandcli_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    click.echo("Deploying...")
    command = [  # pylint: disable=duplicate-code
        "cdk",
        "deploy",
        "--app",
        "python infra/app.py",
        "--output",
        f"{project_dir}/cdk.out",
        "--all",
        "--context",
        f"region={region}",
        "--context",
        f"project_dir={project_dir}",
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

    subprocess.run(
        command,
        cwd=kegstandcli_dir,
        check=True,
        stdout=subprocess.DEVNULL if not verbose else None,
    )  # nosec B603
    click.echo("Finished deploying application!")
