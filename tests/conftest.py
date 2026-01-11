"""
Pytest configuration and fixtures.
"""

import pytest


@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "test_input": "sample input data",
        "test_bucket": "test-bucket",
        "test_key": "test/path/to/file.txt",
    }


@pytest.fixture
def mock_aws_credentials(monkeypatch):
    """Mock AWS credentials for testing."""
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
