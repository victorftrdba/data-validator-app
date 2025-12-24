"""Application settings and configuration."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    """Application configuration settings."""
    
    # AWS LocalStack Configuration
    aws_endpoint_url: str
    s3_bucket_name: str
    sqs_queue_name: str
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    
    # Email Configuration (Mailpit)
    smtp_server: str
    smtp_port: int
    email_from: str
    email_to: str
    
    @classmethod
    def from_env(cls) -> 'Settings':
        """Create settings from environment variables."""
        return cls(
            aws_endpoint_url=os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566"),
            s3_bucket_name=os.getenv("S3_BUCKET_NAME", "projeto-cloud-brasil-bucket"),
            sqs_queue_name=os.getenv("SQS_QUEUE_NAME", "projeto-cloud-brasil-queue"),
            aws_region=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
            smtp_server=os.getenv("SMTP_SERVER", "localhost"),
            smtp_port=int(os.getenv("SMTP_PORT", "1025")),
            email_from=os.getenv("EMAIL_FROM", "analista@cloudbrasil.com.br"),
            email_to=os.getenv("EMAIL_TO", "seu-email@exemplo.com"),
        )


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings.from_env()

