import os
import shutil

import click

from copier import run_copy

@click.command()
@click.pass_context
@click.argument('project_dir', type=click.Path(exists=False))
def new(ctx, project_dir):
    verbose = ctx.obj['verbose']
    new_command(verbose, project_dir)


def new_command(verbose: bool, project_dir: str):
    project_name = os.path.basename(project_dir)
    project_parent_dir = os.path.dirname(project_dir)

    if os.path.exists(project_dir):
        raise click.ClickException(f'Folder {project_name} already exists')

    try:
        # Copy all the files from the template folder to the project folder
        template_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'template')
        run_copy(src_path=template_dir, dst_path=project_parent_dir, data={
            'project_name': project_name,
        }, quiet=not verbose)

        click.echo(f'Successfully created a new Kegstand project: {project_name}')

    except Exception as e:
        click.echo(f'Error creating project: {e}', err=True)
        shutil.rmtree(project_dir)
        raise click.Abort()
