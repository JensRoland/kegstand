import os
import subprocess

import click

@click.command()
@click.pass_context
@click.option('--region', default='eu-west-1', help='AWS region to deploy to')
@click.option('--hotswap', is_flag=True, default=False, help='Attempt to deploy without creating a new CloudFormation stack')
def deploy(ctx, region, hotswap):
    project_dir = ctx.obj['project_dir']

    # Get the dir of the ProustCLI package (one level up from here)
    proustcli_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

    subprocess.run(command, cwd=proustcli_dir, check=True)
