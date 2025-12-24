"""SQS service for consuming messages from LocalStack."""

import json
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from config import Settings
from utils import get_logger

logger = get_logger(__name__)


class SQSService:
    """Service for accessing SQS (LocalStack) to consume messages."""
    
    def __init__(self, settings: Settings):
        """
        Initialize SQS service.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.client = boto3.client(
            'sqs',
            endpoint_url=settings.aws_endpoint_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
    
    def get_queue_url(self, queue_name: str) -> str:
        """
        Get SQS queue URL by name.
        
        Args:
            queue_name: Name of the queue
            
        Returns:
            Queue URL
            
        Raises:
            ClientError: If queue does not exist or operation fails
        """
        try:
            response = self.client.get_queue_url(QueueName=queue_name)
            queue_url = response['QueueUrl']
            logger.info(f"Retrieved queue URL for {queue_name}")
            return queue_url
        except ClientError as e:
            logger.error(f"Error getting queue URL for {queue_name}: {e}")
            raise
    
    def receive_message(self, queue_url: str, max_messages: int = 1) -> Optional[dict]:
        """
        Receive a message from SQS queue.
        
        Args:
            queue_url: SQS queue URL
            max_messages: Maximum number of messages to receive (default: 1)
            
        Returns:
            Message dictionary with 'Body', 'ReceiptHandle', etc., or None if no messages
            
        Raises:
            ClientError: If SQS operation fails
            json.JSONDecodeError: If message body is not valid JSON
        """
        try:
            response = self.client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_messages
            )
            
            if 'Messages' in response and len(response['Messages']) > 0:
                message = response['Messages'][0]
                # Parse message body as JSON
                try:
                    message['Body'] = json.loads(message['Body'])
                except json.JSONDecodeError:
                    # If body is not JSON, keep as string
                    pass
                
                logger.info("Received message from SQS queue")
                return message
            
            logger.info("No messages in queue")
            return None
            
        except ClientError as e:
            logger.error(f"Error receiving message from queue: {e}")
            raise
    
    def delete_message(self, queue_url: str, receipt_handle: str) -> bool:
        """
        Delete a message from SQS queue.
        
        Args:
            queue_url: SQS queue URL
            receipt_handle: Message receipt handle
            
        Returns:
            True if message was deleted successfully, False otherwise
            
        Raises:
            ClientError: If SQS operation fails
        """
        try:
            self.client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            logger.info("Message deleted from SQS queue")
            return True
        except ClientError as e:
            logger.error(f"Error deleting message from queue: {e}")
            raise

