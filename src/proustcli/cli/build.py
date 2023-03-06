import os
import subprocess
import shutil
import zipfile

import click

from proustcli.cli.config import get_proust_config

@click.command()
@click.pass_context
def build(ctx):
    project_dir = ctx.obj['project_dir']
    config = get_proust_config(project_dir)

    # Create a directory to hold the package, and make sure it's empty
    build_dir = os.path.join(project_dir, 'dist')
    shutil.rmtree(build_dir, ignore_errors=True)
    os.makedirs(build_dir, exist_ok=True)

    # Copy everything in the project_dir/src folder to the build_dir
    src_dir = os.path.join(project_dir, 'src')
    shutil.copytree(src_dir, build_dir, dirs_exist_ok=True)

    # Export the dependencies to a requirements.txt file
    subprocess.run([
        'poetry',
        'export',
        '-o', f'{build_dir}/requirements.txt',
        '--without', 'dev',
        '--without', 'lambda-builtins',
        '--without-hashes'
    ], cwd=project_dir, check=True)

    # Install the dependencies to the build folder using pip
    subprocess.run([
        f'pip',
        'install',
        '-r', f'{build_dir}/requirements.txt',
        '-t', build_dir
    ], check=True)
