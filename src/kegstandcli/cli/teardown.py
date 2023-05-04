import os
import subprocess  # nosec
from operator import itemgetter

import click


@click.command()
@click.pass_context
@click.option(
    "--region", default="eu-west-1", help="AWS region the stack is deployed to"
)
def teardown(ctx, region):
    project_dir, config_file, verbose = itemgetter(
        "project_dir", "config_file", "verbose"
    )(ctx.obj)
    teardown_command(verbose, project_dir, config_file, region)


def teardown_command(verbose, project_dir, config_file, region):
    # Get the dir of the Kegstand CLI package itself (one level up from here)
    kegstandcli_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    subprocess.run(
        [  # pylint: disable=duplicate-code
            "cdk",
            "destroy",
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
            "--force",
        ],
        cwd=kegstandcli_dir,
        check=True,
    )  # nosec B603, B607
