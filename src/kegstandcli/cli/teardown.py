import os
import subprocess  # nosec

import click


@click.command()
@click.pass_context
@click.option("--region", default="eu-west-1", help="AWS region the stack is deployed to")
def teardown(ctx, region):
    project_dir = ctx.obj["project_dir"]
    teardown_command(project_dir, region)


def teardown_command(project_dir, region):
    # Get the dir of the Kegstand CLI package itself (one level up from here)
    kegstandcli_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    subprocess.run(
        [
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
            "--force",
        ],
        cwd=kegstandcli_dir,
        check=True,
    )  # nosec B603, B607
