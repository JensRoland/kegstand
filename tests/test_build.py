"""Tests for the build command."""

import tempfile
from pathlib import Path

import pytest
from directory_tree import DisplayTree  # type: ignore

from kegstandcli.cli.build import build_command, create_empty_folder


@pytest.fixture
def mock_templates_path() -> Path:
    """Create mock template files that would normally be in the CLI package."""
    with tempfile.TemporaryDirectory() as temp_dir:
        templates_path = Path(temp_dir)

        # Create mock template files
        (templates_path / "default_lambda.py.tmpl").write_text(
            "def handler(event, context): return {'statusCode': 200}"
        )
        (templates_path / "rest_api_gateway_health_check.py.tmpl").write_text(
            "def handler(event, context): return {'statusCode': 200}"
        )

        return templates_path


def test_create_empty_folder() -> None:
    """Test create_empty_folder creates and cleans directories correctly."""
    # Test creating a new folder
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        folder_path = Path(create_empty_folder(str(temp_path), "new_folder"))
        assert folder_path.exists()
        assert folder_path.is_dir()

        # Test recreating an existing folder (should clean it)
        test_file = folder_path / "test.txt"
        test_file.write_text("test")
        folder_path = Path(create_empty_folder(str(temp_path), "new_folder"))
        assert not test_file.exists()
        assert folder_path.exists()

        # Test empty folder name
        with pytest.raises(ValueError):
            create_empty_folder(str(temp_path), "")


def test_build_command_creates_dist_directory(project_simple: Path) -> None:
    """Test build_command creates dist directory."""
    config: dict[str, dict] = {}
    build_command(False, str(project_simple), config)
    assert (project_simple / "dist").exists()


def test_build_api_gateway(project_simple: Path, assert_files_exist) -> None:
    """Test build_api_gateway creates necessary files."""
    config: dict[str, dict] = {"api_gateway": {}}
    build_command(False, str(project_simple), config)

    DisplayTree(project_simple, maxDepth=3)

    # Verify files were created
    assert_files_exist(project_simple / "dist" / "api_gw_src", ["api/lambda.py"])


def test_build_api(project_simple: Path, assert_files_exist) -> None:
    """Test build_api creates necessary files."""
    config = {"api": {"entrypoint": "api.lambda.handler"}}
    build_command(False, str(project_simple), config)

    DisplayTree(project_simple, maxDepth=3)

    # Verify files were created
    assert_files_exist(project_simple / "dist" / "api_src", ["api/lambda.py", "requirements.txt"])


def test_build_command_with_multiple_modules(project_simple: Path, assert_files_exist) -> None:
    """Test build_command handles multiple modules."""
    config = {"api": {"entrypoint": "api.lambda.handler"}, "api_gateway": {}}
    build_command(False, str(project_simple), config)

    DisplayTree(project_simple, maxDepth=3)

    # Verify files were created
    assert_files_exist(
        project_simple / "dist",
        ["api_src/api/lambda.py", "api_src/requirements.txt", "api_gw_src/api/lambda.py"],
    )
