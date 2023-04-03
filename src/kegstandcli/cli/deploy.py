import os
import subprocess

import click

from kegstandcli.cli.build import build_command

@click.command()
@click.pass_context
@click.option('--region', default='eu-west-1', help='AWS region to deploy to')
@click.option('--hotswap', is_flag=True, default=False, help='Attempt to deploy without creating a new CloudFormation stack')
@click.option('--skip-build', is_flag=True, default=False, help='Skip building the project before deploying')
def deploy(ctx, region, hotswap, skip_build):
    project_dir = ctx.obj['project_dir']
    if not skip_build:
        build_command(project_dir)
    deploy_command(project_dir, region, hotswap)


def deploy_command(project_dir, region, hotswap):
    # Get the dir of the kegstandcli package (one level up from here)
    kegstandcli_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    command = [
        'cdk',
        'deploy',
        '--app', 'python infra/app.py',
        '--output', f'{project_dir}/cdk.out',
        '--all',
        '--context', f'region={region}',
        '--context', f'project_dir={project_dir}',
        '--require-approval', 'never'
    ]
    if hotswap:
        command.append('--hotswap')

    subprocess.run(command, cwd=kegstandcli_dir, check=True)
