"""Pytest configuration and shared fixtures."""

import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture
def mock_aws(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock AWS-related functionality to prevent actual AWS calls.

    This includes mocking:
    - boto3 for AWS API calls
    - aws_cdk for infrastructure definition
    - Any AWS credentials/config checks

    Args:
        monkeypatch: pytest's monkeypatch fixture
    """

    # Mock boto3 client and resource
    class MockBoto3Client:
        def __init__(self):
            self.calls = []

        def __call__(self, *args, **kwargs):
            self.calls.append(("client", args, kwargs))
            return self

        def __getattr__(self, name):
            def method(*args, **kwargs):
                self.calls.append((name, args, kwargs))
                return {}

            return method

    class MockBoto3Resource:
        def __init__(self):
            self.calls = []

        def __call__(self, *args, **kwargs):
            self.calls.append(("resource", args, kwargs))
            return self

        def __getattr__(self, name):
            def method(*args, **kwargs):
                self.calls.append((name, args, kwargs))
                return self

            return method

    mock_client = MockBoto3Client()
    mock_resource = MockBoto3Resource()

    monkeypatch.setattr("boto3.client", mock_client)
    monkeypatch.setattr("boto3.resource", mock_resource)

    # Mock AWS credentials
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")


@pytest.fixture(scope="function")
def temp_path() -> Generator[Path, None, None]:
    """Create a temporary directory for project files and clean it up after the test.

    Yields:
        Path: Path to the temporary directory
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture(scope="function")
def project_simple() -> Generator[Path, None, None]:
    """Create a temporary directory with a simple Kegstand project.

    Yields:
        Path: Path to the temporary project directory
    """
    # Copy files from tests/test_data/simple_project to a temporary directory
    test_project_path = Path("tests/test_data/simple_project")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_project_path = Path(temp_dir) / "simple_project"
        shutil.copytree(test_project_path, temp_project_path)

        yield temp_project_path


@pytest.fixture
def assert_files_exist():
    """Create a helper function to verify generated files.

    Returns:
        callable: Function to check file existence and optionally content
    """

    def _assert_files_exist(
        directory: Path, expected_files: list[str], content_checks: dict[str, str] | None = None
    ):
        """Assert that expected files exist and optionally check their content.

        Args:
            directory: Base directory to check files in
            expected_files: List of relative paths that should exist
            content_checks: Optional dict mapping file paths to strings that should appear in them
        """
        for file_path in expected_files:
            full_path = directory / file_path
            assert full_path.exists(), f"Expected file {file_path} does not exist"

            if content_checks and file_path in content_checks:
                content = full_path.read_text()
                expected_content = content_checks[file_path]
                assert expected_content in content, f"Expected content not found in {file_path}"

    return _assert_files_exist
