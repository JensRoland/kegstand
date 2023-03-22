import os
import pytest

AWS_TEST_REGION = "eu-west-1"

def pytest_configure(config: pytest.Config) -> None:
    """Mocked AWS Credentials to prevent accidental side effects in the cloud."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    # App-specific environment variables
    #os.environ['PRODUCT_TABLE_NAME'] = "test_product_table"

