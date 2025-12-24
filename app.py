"""Main application entry point for data validator."""

from config import get_settings
from models import Statistics
from services import EmailService, S3Service, SQSService
from utils import setup_logger
from validators import DataValidator

# Setup logger
logger = setup_logger(__name__)


def main():
    """Main application entry point."""
    # Load configuration
    settings = get_settings()
    
    # Initialize services
    email_service = EmailService(settings)
    s3_service = S3Service(settings)
    sqs_service = SQSService(settings)
    data_validator = DataValidator()
    
    try:
        # Get queue URL
        queue_url = sqs_service.get_queue_url(settings.sqs_queue_name)
        
        # Receive message from queue
        message = sqs_service.receive_message(queue_url)
        
        if message is None:
            logger.info("Queue is empty")
            email_service.send_empty_queue_email()
            return
        
        # Extract S3 path from message
        message_body = message['Body']
        if isinstance(message_body, str):
            import json
            message_body = json.loads(message_body)
        
        s3_path = message_body.get('s3_path', '')
        if not s3_path:
            raise ValueError("Message body does not contain 's3_path'")
        
        # Extract S3 key from path
        s3_key = s3_service.extract_key_from_s3_path(s3_path, settings.s3_bucket_name)
        
        # Read Parquet file from S3
        df = s3_service.get_parquet_file(settings.s3_bucket_name, s3_key)
        
        if df is None:
            raise ValueError("Failed to read Parquet file from S3")
        
        # Validate and generate statistics
        statistics = data_validator.validate_and_generate_stats(df)
        
        # Send validation report email
        email_service.send_validation_report(statistics)
        
        # Delete message from queue
        receipt_handle = message['ReceiptHandle']
        sqs_service.delete_message(queue_url, receipt_handle)
        
        logger.info("Data validation completed successfully")
        
    except Exception as e:
        logger.error(f"Error during data validation: {e}", exc_info=True)
        email_service.send_error_email(str(e))
        raise


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        raise
