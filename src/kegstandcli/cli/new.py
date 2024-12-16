"""Project creation command for Kegstand CLI."""

import json
import shutil
from pathlib import Path

import click
from copier import run_copy


@click.command()
@click.pass_context
@click.argument("project_dir", type=click.Path(exists=False))
@click.option("--data-file", type=click.Path(exists=True), help="Path to a Copier input data file")
def new(ctx: click.Context, project_dir: str, data_file: Path) -> None:
    """Create a new Kegstand project.

    Args:
        ctx: Click context
        project_dir: Path to create the new project in
        data_file: Path to a Copier input data file
    """
    verbose = ctx.obj["verbose"]
    copier_data: dict = json.loads(data_file.read_text()) if data_file else {}
    new_command(verbose, project_dir, copier_data)


def new_command(verbose: bool, project_dir: str, copier_data: dict | None = None) -> None:
    """Execute the project creation process.

    Args:
        verbose: Whether to show verbose output
        project_dir: Path to create the new project in
        data_file: Path to a Copier input data file

    Raises:
        click.ClickException: If the project directory already exists
        click.Abort: If there is an error creating the project
    """
    if not copier_data:
        copier_data = {}
    project_path = Path(project_dir)
    project_name = copier_data.get("project_name", project_path.name)
    project_parent_dir = str(project_path.parent)

    if project_path.exists():
        raise click.ClickException(f"Folder {project_name} already exists")

    try:
        # Copy all the files from the template folder to the project folder
        template_path = "gh:JensRoland/kegstand-project-template.git"
        input_data = {"project_name": project_name, **copier_data}
        run_copy(
            src_path=template_path,
            dst_path=project_parent_dir,
            data=input_data,
            quiet=not verbose,
        )
        click.echo(f"Successfully created a new Kegstand project: {project_name}")

    except Exception as err:
        click.echo(f"Error creating project: {err}", err=True)
        if project_path.exists():
            shutil.rmtree(project_path)
        raise click.Abort() from err
