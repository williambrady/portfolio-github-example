"""
Unit tests for the main application module.
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from main import DataProcessor, parse_arguments  # noqa: E402


class TestDataProcessor:
    """Test suite for DataProcessor class."""

    def test_initialization(self):
        """Test DataProcessor initialization."""
        processor = DataProcessor(environment="dev")
        assert processor.environment == "dev"
        assert processor.s3_client is None
        assert processor.cloudwatch_client is None

    def test_initialization_with_environment(self):
        """Test DataProcessor initialization with different environments."""
        for env in ["dev", "staging", "prod"]:
            processor = DataProcessor(environment=env)
            assert processor.environment == env

    @patch("boto3.client")
    def test_setup_aws_clients_success(self, mock_boto_client):
        """Test successful AWS client setup."""
        processor = DataProcessor()
        processor.setup_aws_clients()

        assert mock_boto_client.call_count == 2
        assert processor.s3_client is not None
        assert processor.cloudwatch_client is not None

    @patch("boto3.client")
    def test_setup_aws_clients_failure(self, mock_boto_client):
        """Test AWS client setup failure."""
        mock_boto_client.side_effect = ClientError(
            {"Error": {"Code": "AccessDenied", "Message": "Access denied"}},
            "GetObject",
        )

        processor = DataProcessor()
        with pytest.raises(ClientError):
            processor.setup_aws_clients()

    def test_process_data(self):
        """Test data processing."""
        processor = DataProcessor(environment="dev")
        result = processor.process_data("test_input")

        assert result["status"] == "success"
        assert result["input"] == "test_input"
        assert result["output"] == "Processed: test_input"
        assert result["environment"] == "dev"

    def test_save_to_s3_without_client(self):
        """Test S3 save without initialized client."""
        processor = DataProcessor()
        result = processor.save_to_s3("test-bucket", "test-key", "test-data")
        assert result is False

    @patch("boto3.client")
    def test_save_to_s3_success(self, mock_boto_client):
        """Test successful S3 save."""
        mock_s3 = MagicMock()
        mock_boto_client.return_value = mock_s3

        processor = DataProcessor()
        processor.s3_client = mock_s3

        result = processor.save_to_s3("test-bucket", "test-key", "test-data")

        assert result is True
        mock_s3.put_object.assert_called_once_with(Bucket="test-bucket", Key="test-key", Body="test-data")

    @patch("boto3.client")
    def test_save_to_s3_failure(self, mock_boto_client):
        """Test S3 save failure."""
        mock_s3 = MagicMock()
        mock_s3.put_object.side_effect = ClientError(
            {"Error": {"Code": "NoSuchBucket", "Message": "Bucket not found"}},
            "PutObject",
        )
        mock_boto_client.return_value = mock_s3

        processor = DataProcessor()
        processor.s3_client = mock_s3

        result = processor.save_to_s3("test-bucket", "test-key", "test-data")
        assert result is False

    def test_log_to_cloudwatch_without_client(self):
        """Test CloudWatch logging without initialized client."""
        processor = DataProcessor()
        result = processor.log_to_cloudwatch("log-group", "log-stream", "message")
        assert result is False


class TestArgumentParsing:
    """Test suite for command line argument parsing."""

    @patch("sys.argv", ["main.py"])
    def test_default_arguments(self):
        """Test default argument values."""
        args = parse_arguments()
        assert args.environment == "dev"
        assert args.input is None
        assert args.s3_bucket is None
        assert args.verbose is False

    @patch("sys.argv", ["main.py", "--environment", "prod"])
    def test_environment_argument(self):
        """Test environment argument."""
        args = parse_arguments()
        assert args.environment == "prod"

    @patch("sys.argv", ["main.py", "--input", "test_data"])
    def test_input_argument(self):
        """Test input argument."""
        args = parse_arguments()
        assert args.input == "test_data"

    @patch("sys.argv", ["main.py", "--s3-bucket", "my-bucket"])
    def test_s3_bucket_argument(self):
        """Test S3 bucket argument."""
        args = parse_arguments()
        assert args.s3_bucket == "my-bucket"

    @patch("sys.argv", ["main.py", "--verbose"])
    def test_verbose_argument(self):
        """Test verbose argument."""
        args = parse_arguments()
        assert args.verbose is True

    @patch(
        "sys.argv",
        [
            "main.py",
            "--environment",
            "staging",
            "--input",
            "data",
            "--s3-bucket",
            "bucket",
            "--verbose",
        ],
    )
    def test_all_arguments(self):
        """Test all arguments together."""
        args = parse_arguments()
        assert args.environment == "staging"
        assert args.input == "data"
        assert args.s3_bucket == "bucket"
        assert args.verbose is True
