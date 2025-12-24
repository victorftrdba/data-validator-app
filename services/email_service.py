"""Email service for sending notifications via SMTP."""

import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from config import Settings
from models import Statistics
from utils import get_logger

logger = get_logger(__name__)


class EmailService:
    """Service for sending emails via SMTP (Mailpit)."""
    
    def __init__(self, settings: Settings):
        """
        Initialize email service.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.email_from = settings.email_from
        self.email_to = settings.email_to
    
    def _send_email(self, subject: str, body: str) -> bool:
        """
        Send an email via SMTP.
        
        Args:
            subject: Email subject
            body: Email body (HTML)
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        msg = MIMEMultipart()
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.send_message(msg)
            logger.info("Email sent successfully to Mailpit")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def send_error_email(self, error_message: str) -> bool:
        """
        Send error notification email.
        
        Args:
            error_message: Error message to include in email
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        date_str = datetime.now().strftime('%d/%m/%Y')
        subject = f"📊 Processing Error - {date_str}"
        
        body = f"""
        <h2>Processing Error</h2>
        <p>{error_message}</p>
        <br>
        <p><i>Automatically sent by your Kubernetes Pipeline.</i></p>
        """
        
        return self._send_email(subject, body)
    
    def send_empty_queue_email(self) -> bool:
        """
        Send empty queue notification email.
        
        Returns:
            True if email was sent successfully, False otherwise
        """
        date_str = datetime.now().strftime('%d/%m/%Y')
        subject = f"📊 Empty Queue - {date_str}"
        
        body = """
        <h2>Empty Queue</h2>
        <p>The queue is empty.</p>
        <br>
        <p><i>Automatically sent by your Kubernetes Pipeline.</i></p>
        """
        
        return self._send_email(subject, body)
    
    def send_validation_report(self, statistics: Statistics) -> bool:
        """
        Send data validation report email.
        
        Args:
            statistics: Validation statistics
            
        Returns:
            True if email was sent successfully, False otherwise
        """
        date_str = datetime.now().strftime('%d/%m/%Y')
        subject = f"📊 Data Quality Report - {date_str}"
        
        body = f"""
        <h2>Data Validation Report</h2>
        <p>The pipeline successfully processed a new Parquet file.</p>
        <ul>
            <li><b>Total Rows:</b> {statistics.rows}</li>
            <li><b>Total Value:</b> ${statistics.total_value:.2f}</li>
            <li><b>Average Price:</b> ${statistics.average_value:.2f}</li>
            <li><b>Schema Status:</b> ✅ OK</li>
        </ul>
        <br>
        <p><i>Automatically sent by your Kubernetes Pipeline.</i></p>
        """
        
        return self._send_email(subject, body)

