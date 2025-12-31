"""
Email service using Resend
"""
from typing import Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Try to import Resend, fallback to SMTP if not available
try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False
    logger.warning("Resend not installed. Email functionality will be limited.")


async def send_email(
    to: str,
    subject: str,
    html: str,
    text: Optional[str] = None
) -> bool:
    """
    Send email using Resend or SMTP fallback
    
    Args:
        to: Recipient email address
        subject: Email subject
        html: HTML email content
        text: Plain text email content (optional)
    
    Returns:
        True if email sent successfully, False otherwise
    """
    if settings.USE_SMTP and settings.SMTP_HOST:
        return await _send_email_smtp(to, subject, html, text)
    
    if settings.RESEND_API_KEY and RESEND_AVAILABLE:
        return await _send_email_resend(to, subject, html, text)
    
    logger.warning("No email service configured. Email not sent.")
    return False


async def _send_email_resend(
    to: str,
    subject: str,
    html: str,
    text: Optional[str] = None
) -> bool:
    """Send email using Resend"""
    try:
        resend.api_key = settings.RESEND_API_KEY
        
        params = {
            "from": settings.EMAIL_FROM,
            "to": [to],
            "subject": subject,
            "html": html,
        }
        
        if text:
            params["text"] = text
        
        email = resend.Emails.send(params)
        
        if email and hasattr(email, 'id'):
            logger.info(f"Email sent successfully to {to} via Resend")
            return True
        else:
            logger.error(f"Failed to send email to {to} via Resend")
            return False
            
    except Exception as e:
        logger.error(f"Error sending email via Resend: {str(e)}")
        return False


async def _send_email_smtp(
    to: str,
    subject: str,
    html: str,
    text: Optional[str] = None
) -> bool:
    """Send email using SMTP (fallback)"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_FROM
        msg['To'] = to
        
        if text:
            part1 = MIMEText(text, 'plain')
            msg.attach(part1)
        
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email sent successfully to {to} via SMTP")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email via SMTP: {str(e)}")
        return False


async def send_verification_email(to: str, verification_token: str) -> bool:
    """Send email verification email"""
    verification_url = f"{settings.CORS_ORIGINS[0] if settings.CORS_ORIGINS else 'http://localhost:3000'}/verify-email?token={verification_token}"
    
    html = f"""
    <html>
        <body>
            <h2>Verify Your Email Address</h2>
            <p>Please click the link below to verify your email address:</p>
            <p><a href="{verification_url}">Verify Email</a></p>
            <p>Or copy this link: {verification_url}</p>
            <p>This link will expire in 24 hours.</p>
        </body>
    </html>
    """
    
    return await send_email(
        to=to,
        subject="Verify Your Email - Credit Check",
        html=html,
        text=f"Please visit {verification_url} to verify your email address."
    )


async def send_password_reset_email(to: str, reset_token: str) -> bool:
    """Send password reset email"""
    reset_url = f"{settings.CORS_ORIGINS[0] if settings.CORS_ORIGINS else 'http://localhost:3000'}/reset-password?token={reset_token}"
    
    html = f"""
    <html>
        <body>
            <h2>Reset Your Password</h2>
            <p>You requested to reset your password. Click the link below:</p>
            <p><a href="{reset_url}">Reset Password</a></p>
            <p>Or copy this link: {reset_url}</p>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request this, please ignore this email.</p>
        </body>
    </html>
    """
    
    return await send_email(
        to=to,
        subject="Reset Your Password - Credit Check",
        html=html,
        text=f"Please visit {reset_url} to reset your password."
    )

