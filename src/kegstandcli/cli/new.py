import os
import shutil

import click

from copier import run_copy

@click.command()
@click.argument('project_dir')
def new(project_dir):
    new_command(project_dir)


def new_command(project_dir):
    project_name = os.path.basename(project_dir)
    project_parent_dir = os.path.dirname(project_dir)

    if os.path.exists(project_dir):
        raise click.ClickException(f'Folder {project_name} already exists')

    try:
        # Copy all the files from the template folder to the project folder
        template_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'template')
        run_copy(src_path=template_dir, dst_path=project_parent_dir, data={
            'project_name': project_name,
        }, quiet=True)

        click.echo(f'Created new Kegstand project: {project_name}')

    except Exception as e:
        click.echo(f'Error creating project: {e}')
        shutil.rmtree(project_dir)
        raise click.Abort()
