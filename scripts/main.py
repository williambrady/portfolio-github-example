"""
Main application entry point for portfolio data processing.

This is a template application that demonstrates:
- Argument parsing
- Logging setup
- AWS service integration
- Data processing pipeline
"""

import argparse
import logging
import sys
from typing import Optional

import boto3
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Main data processing class.

    This class handles data processing, AWS interactions,
    and business logic for the portfolio application.
    """

    def __init__(self, environment: str = "dev"):
        """
        Initialize the data processor.

        Args:
            environment: The environment (dev, staging, prod)
        """
        self.environment = environment
        self.s3_client: Optional[boto3.client] = None
        self.cloudwatch_client: Optional[boto3.client] = None
        logger.info(f"Initializing DataProcessor for environment: {environment}")

    def setup_aws_clients(self) -> None:
        """Initialize AWS service clients."""
        try:
            self.s3_client = boto3.client("s3")
            self.cloudwatch_client = boto3.client("logs")
            logger.info("AWS clients initialized successfully")
        except ClientError as e:
            logger.error(f"Failed to initialize AWS clients: {e}")
            raise

    def process_data(self, input_data: str) -> dict:
        """
        Process input data and return results.

        Args:
            input_data: The data to process

        Returns:
            Dictionary containing processing results
        """
        logger.info(f"Processing data: {input_data}")

        # Example processing logic
        result = {
            "status": "success",
            "input": input_data,
            "output": f"Processed: {input_data}",
            "environment": self.environment,
        }

        logger.info("Data processing completed successfully")
        return result

    def save_to_s3(self, bucket: str, key: str, data: str) -> bool:
        """
        Save data to S3 bucket.

        Args:
            bucket: S3 bucket name
            key: Object key
            data: Data to save

        Returns:
            True if successful, False otherwise
        """
        if not self.s3_client:
            logger.error("S3 client not initialized")
            return False

        try:
            self.s3_client.put_object(Bucket=bucket, Key=key, Body=data)
            logger.info(f"Successfully saved data to s3://{bucket}/{key}")
            return True
        except ClientError as e:
            logger.error(f"Failed to save to S3: {e}")
            return False

    def log_to_cloudwatch(self, log_group: str, log_stream: str, message: str) -> bool:
        """
        Send log message to CloudWatch.

        Args:
            log_group: CloudWatch log group name
            log_stream: CloudWatch log stream name
            message: Log message

        Returns:
            True if successful, False otherwise
        """
        if not self.cloudwatch_client:
            logger.error("CloudWatch client not initialized")
            return False

        try:
            # Create log stream if it doesn't exist
            try:
                self.cloudwatch_client.create_log_stream(logGroupName=log_group, logStreamName=log_stream)
            except ClientError:
                pass  # Stream might already exist

            # Send log event
            import time

            self.cloudwatch_client.put_log_events(
                logGroupName=log_group,
                logStreamName=log_stream,
                logEvents=[
                    {
                        "timestamp": int(time.time() * 1000),
                        "message": message,
                    }
                ],
            )
            logger.info(f"Successfully logged to CloudWatch: {log_group}/{log_stream}")
            return True
        except ClientError as e:
            logger.error(f"Failed to log to CloudWatch: {e}")
            return False


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Portfolio Data Processing Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--environment",
        "-e",
        choices=["dev", "staging", "prod"],
        default="dev",
        help="Environment to run in (default: dev)",
    )

    parser.add_argument(
        "--input",
        "-i",
        type=str,
        help="Input data to process",
    )

    parser.add_argument(
        "--s3-bucket",
        type=str,
        help="S3 bucket for data storage",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    return parser.parse_args()


def main() -> int:
    """
    Main application entry point.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    args = parse_arguments()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info("Starting Portfolio Data Processing Application")
    logger.info(f"Environment: {args.environment}")

    try:
        # Initialize processor
        processor = DataProcessor(environment=args.environment)

        # Setup AWS clients if S3 bucket is specified
        if args.s3_bucket:
            processor.setup_aws_clients()

        # Process data if input provided
        if args.input:
            result = processor.process_data(args.input)
            logger.info(f"Processing result: {result}")

            # Save to S3 if bucket specified
            if args.s3_bucket:
                processor.save_to_s3(
                    bucket=args.s3_bucket,
                    key=f"results/{args.environment}/output.txt",
                    data=str(result),
                )
        else:
            logger.warning("No input data provided. Use --input to specify data to process.")

        logger.info("Application completed successfully")
        return 0

    except Exception as e:
        logger.error(f"Application failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
