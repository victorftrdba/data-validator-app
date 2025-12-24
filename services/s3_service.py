"""S3 service for reading Parquet files from LocalStack."""

import io
from typing import Optional

import boto3
import pandas as pd
from botocore.exceptions import ClientError

from config import Settings
from utils import get_logger

logger = get_logger(__name__)


class S3Service:
    """Service for accessing S3 (LocalStack) to read Parquet files."""
    
    def __init__(self, settings: Settings):
        """
        Initialize S3 service.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.client = boto3.client(
            's3',
            endpoint_url=settings.aws_endpoint_url,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
    
    def get_parquet_file(self, bucket: str, key: str) -> Optional[pd.DataFrame]:
        """
        Read a Parquet file from S3 and return as DataFrame.
        
        Args:
            bucket: S3 bucket name
            key: S3 object key (file path)
            
        Returns:
            DataFrame with the Parquet file data, or None if error occurs
            
        Raises:
            ClientError: If S3 operation fails
            ValueError: If file cannot be read as Parquet
        """
        try:
            logger.info(f"Reading Parquet file from s3://{bucket}/{key}")
            response = self.client.get_object(Bucket=bucket, Key=key)
            parquet_data = response['Body'].read()
            
            df = pd.read_parquet(io.BytesIO(parquet_data))
            logger.info(f"Successfully read {len(df)} rows from Parquet file")
            return df
            
        except ClientError as e:
            logger.error(f"S3 error reading file s3://{bucket}/{key}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error reading Parquet file: {e}")
            raise ValueError(f"Failed to read Parquet file: {e}") from e
    
    def extract_key_from_s3_path(self, s3_path: str, bucket: str) -> str:
        """
        Extract S3 key from full S3 path.
        
        Args:
            s3_path: Full S3 path (e.g., s3://bucket/key)
            bucket: Bucket name
            
        Returns:
            S3 key (file path without bucket)
        """
        prefix = f"s3://{bucket}/"
        if s3_path.startswith(prefix):
            return s3_path.replace(prefix, "")
        return s3_path

