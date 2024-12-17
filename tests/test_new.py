"""Tests for the new command."""

from pathlib import Path
from unittest import mock

import click
import pytest

from kegstandcli.cli.new import new_command


def test_new_command_creates_project_mocked(temp_path: Path) -> None:
    """Test that new_command creates a project successfully."""
    project_name = "test-project"
    project_path = temp_path / project_name

    with mock.patch("kegstandcli.cli.new.run_copy") as mock_run_copy:
        new_command(verbose=False, project_dir=str(project_path))

        # Verify run_copy was called with correct arguments
        mock_run_copy.assert_called_once_with(
            src_path="gh:JensRoland/kegstand-project-template.git",
            dst_path=str(temp_path),
            data={"project_name": project_name},
            defaults=False,
            quiet=True,
        )


def test_new_command_passes_copier_data(temp_path: Path) -> None:
    """Test that new_command creates a project successfully."""
    project_name = "test-project"
    project_path = temp_path / project_name

    with mock.patch("kegstandcli.cli.new.run_copy") as mock_run_copy:
        copier_data = {"foo": "bar"}
        new_command(verbose=False, project_dir=str(project_path), copier_data=copier_data)

        # Verify run_copy was called with correct arguments
        mock_run_copy.assert_called_once_with(
            src_path="gh:JensRoland/kegstand-project-template.git",
            dst_path=str(temp_path),
            data={"project_name": project_name, **copier_data},
            defaults=False,
            quiet=True,
        )


def test_new_command_creates_project_real(temp_path: Path, assert_files_exist) -> None:
    """Test that new_command creates a project successfully."""
    project_name = "test-project"
    project_path = temp_path / project_name
    new_command(verbose=False, project_dir=str(project_path), defaults=True)

    # Verify the project directory was created
    assert project_path.exists()
    assert_files_exist(
        project_path,
        [
            "pyproject.toml",
            ".gitignore",
            "src/api/__init__.py",
            "src/api/public/__init__.py",
            "src/api/public/hello.py",
        ],
    )


def test_new_command_fails_if_directory_exists(temp_path: Path) -> None:
    """Test that new_command fails if the project directory already exists."""
    project_name = "existing-project"
    project_path = temp_path / project_name
    project_path.mkdir(parents=True)

    with pytest.raises(click.ClickException) as exc_info:
        new_command(verbose=False, project_dir=str(project_path))

    assert f"Folder {project_name} already exists" in str(exc_info.value)


def test_new_command_cleans_up_on_error(temp_path: Path) -> None:
    """Test that new_command cleans up if project creation fails."""
    project_name = "failed-project"
    project_path = temp_path / project_name

    with mock.patch("kegstandcli.cli.new.run_copy") as mock_run_copy:
        # Simulate an error during project creation
        mock_run_copy.side_effect = Exception("Template error")

        with pytest.raises(click.Abort):
            new_command(verbose=False, project_dir=str(project_path))

        # Verify the directory was cleaned up
        assert not project_path.exists()


def test_new_command_with_verbose_output(temp_path: Path) -> None:
    """Test that new_command handles verbose flag correctly."""
    project_name = "verbose-project"
    project_path = temp_path / project_name

    with mock.patch("kegstandcli.cli.new.run_copy") as mock_run_copy:
        new_command(verbose=True, project_dir=str(project_path))

        # Verify quiet=False was passed when verbose=True
        mock_run_copy.assert_called_once_with(
            src_path="gh:JensRoland/kegstand-project-template.git",
            dst_path=str(temp_path),
            data={"project_name": project_name},
            defaults=False,
            quiet=False,
        )
