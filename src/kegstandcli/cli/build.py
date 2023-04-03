import os
import subprocess
import shutil

import click

from kegstandcli.cli.config import get_kegstand_config

@click.command()
@click.pass_context
def build(ctx):
    project_dir = ctx.obj['project_dir']
    build_command(project_dir)


def build_command(project_dir):
    config = get_kegstand_config(project_dir)

    # Create a directory to hold the build artifacts, and make sure it is empty
    build_dir = create_empty_folder(project_dir, 'dist')

    # Handle the different types ('modules') of build
    if "api" in config:
        build_api(config, project_dir, create_empty_folder(build_dir, 'api_src'))


def build_api(config: dict, project_dir: str, module_build_dir: str):
    # Copy everything in the project_dir/src folder to the module_build_dir
    src_dir = os.path.join(project_dir, 'src')
    shutil.copytree(src_dir, module_build_dir, dirs_exist_ok=True)

    # Export the dependencies to a requirements.txt file
    subprocess.run([
        'poetry',
        'export',
        '-o', f'{module_build_dir}/requirements.txt',
        '--without', 'dev',
        '--without', 'lambda-builtins',
        '--without-hashes'
    ], cwd=project_dir, check=True)

    # Install the dependencies to the build folder using pip
    subprocess.run([
        f'pip',
        'install',
        '-r', f'{module_build_dir}/requirements.txt',
        '-t', module_build_dir
    ], check=True)


def create_empty_folder(parent_folder: str, folder_name: str):
    if folder_name == '':
        raise ValueError('folder_name cannot be empty')

    folder_path = os.path.join(parent_folder, folder_name)
    shutil.rmtree(folder_path, ignore_errors=True)
    os.makedirs(folder_path, exist_ok=True)

    return folder_path

