"""Project creation command for Kegstand CLI."""

import shutil
from pathlib import Path
from typing import Any

import click
from copier import run_copy


@click.command()
@click.pass_context
@click.argument("project_dir", type=click.Path(exists=False))
def new(ctx: click.Context, project_dir: str) -> None:
    """Create a new Kegstand project.

    Args:
        ctx: Click context
        project_dir: Path to create the new project in
    """
    verbose = ctx.obj["verbose"]
    new_command(verbose, project_dir)


def new_command(verbose: bool, project_dir: str) -> None:
    """Execute the project creation process.

    Args:
        verbose: Whether to show verbose output
        project_dir: Path to create the new project in

    Raises:
        click.ClickException: If the project directory already exists
        click.Abort: If there is an error creating the project
    """
    project_path = Path(project_dir)
    project_name = project_path.name
    project_parent_dir = str(project_path.parent)

    if project_path.exists():
        raise click.ClickException(f"Folder {project_name} already exists")

    try:
        # Copy all the files from the template folder to the project folder
        template_path = "gh:JensRoland/kegstand-project-template.git"
        run_copy(
            src_path=template_path,
            dst_path=project_parent_dir,
            data={"project_name": project_name},
            quiet=not verbose,
        )
        click.echo(f"Successfully created a new Kegstand project: {project_name}")

    except Exception as err:
        click.echo(f"Error creating project: {err}", err=True)
        if project_path.exists():
            shutil.rmtree(project_path)
        raise click.Abort() from err
