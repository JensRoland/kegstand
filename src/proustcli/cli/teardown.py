import os
import subprocess

import click

@click.command()
@click.pass_context
@click.option('--stack-name', default='my-stack', help='Name of the CloudFormation stack')
@click.option('--region', default='eu-west-1', help='AWS region to deploy to')
def teardown(ctx, stack_name, region):
    project_dir = ctx.obj['project_dir']

    # Get the dir of the Proust CLI package (one level up from here)
    proustcli_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    subprocess.run([
        'cdk',
        'destroy',
        '--app', 'python infra/app.py',
        '--output', f'{project_dir}/cdk.out',
        '--context', f'stack_name={stack_name}',
        '--context', f'region={region}',
        '--context', f'project_dir={project_dir}',
        '--force'
    ], cwd=proustcli_dir, check=True)

