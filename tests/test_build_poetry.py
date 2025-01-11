"""Tests for the build command on Poetry-based projects."""

from pathlib import Path

from kegstandcli.cli.build import build_command


def test_build_command_creates_build_directory(project_simple_poetry: Path) -> None:
    """Test build_command creates build directory."""
    config: dict[str, dict] = {}
    build_command(False, str(project_simple_poetry), config)
    assert (project_simple_poetry / "build").exists()


def test_build_api_gateway(project_simple_poetry: Path, assert_files_exist) -> None:
    """Test build_api_gateway creates necessary files."""
    config: dict[str, dict] = {"api_gateway": {}}
    build_command(False, str(project_simple_poetry), config)

    # Verify files were created
    assert_files_exist(project_simple_poetry / "build" / "api_gw_src", ["api/lambda.py"])


def test_build_api(project_simple_poetry: Path, assert_files_exist) -> None:
    """Test build_api creates necessary files."""
    config = {"api": {"entrypoint": "api.lambda.handler"}}
    build_command(True, str(project_simple_poetry), config)

    # DisplayTree(project_simple_poetry, maxDepth=3)

    # Verify files were created
    assert_files_exist(
        project_simple_poetry / "build" / "api_src", ["api/lambda.py", "requirements.txt"]
    )

    # Read the requirements.txt file and verify that it includes expected dependencies
    # and not dev dependencies
    with open(project_simple_poetry / "build" / "api_src" / "requirements.txt") as f:
        requirements = f.read()
        assert "kegstand==" in requirements
        assert "kegstandcli==" not in requirements


def test_build_command_with_multiple_modules(
    project_simple_poetry: Path, assert_files_exist
) -> None:
    """Test build_command handles multiple modules."""
    config = {"api": {"entrypoint": "api.lambda.handler"}, "api_gateway": {}}
    build_command(True, str(project_simple_poetry), config)

    # DisplayTree(project_simple_poetry, maxDepth=3)

    # Verify files were created
    assert_files_exist(
        project_simple_poetry / "build",
        ["api_src/api/lambda.py", "api_src/requirements.txt", "api_gw_src/api/lambda.py"],
    )
