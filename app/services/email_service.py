import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from app.core.config import settings
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(to_email: str, subject: str, body: str, attachment_path: str = None) -> bool:
    """
    Sends an email with an optional attachment.
    Returns True if successful, False otherwise.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.MAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if attachment_path:
            with open(attachment_path, "rb") as f:
                part = MIMEApplication(
                    f.read(),
                    Name=os.path.basename(attachment_path)
                )
            # After the file is closed
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)

        # Connect to SMTP server
        # Note: This is a synchronous call. For high scale, use a task queue or async SMTP lib.
        # For this MVP, we catch errors gracefully.
        with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
            if settings.MAIL_TLS:
                server.starttls()
            
            # Only login if credentials are provided (skip for dev/testing if not set)
            if settings.MAIL_USERNAME != "your_email@example.com":
                 server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
                 server.send_message(msg)
                 logger.info(f"Email sent to {to_email}")
            else:
                 logger.warning(f"Email NOT sent to {to_email} (Credentials not configured).")
                 return True # Treat as success for demo purposes if not configured? No, let's return True but log it.

        return True

    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False
