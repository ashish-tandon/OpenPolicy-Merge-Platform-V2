"""
Our Own Mail Server Service

Like OpenParliament, we can run our own mail server using:
1. Postfix (SMTP server) - FREE
2. Dovecot (IMAP/POP3) - FREE  
3. SpamAssassin (Spam filtering) - FREE
4. ClamAV (Virus scanning) - FREE

This gives us:
- 100% control over email delivery
- No monthly costs
- Professional email addresses
- Custom domain support
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)


class OwnMailServer:
    """Our own mail server service using Postfix/SMTP."""
    
    def __init__(self):
        self.smtp_host = settings.OWN_SMTP_HOST or "localhost"
        self.smtp_port = settings.OWN_SMTP_PORT or 587
        self.smtp_user = settings.OWN_SMTP_USER
        self.smtp_password = settings.OWN_SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL or "noreply@openpolicy.me"
        self.use_tls = settings.OWN_SMTP_USE_TLS or True
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """Send email using our own mail server."""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    await self._add_attachment(msg, file_path)
            
            # Send email
            if self.smtp_user and self.smtp_password:
                # Authenticated SMTP
                return await self._send_authenticated(msg)
            else:
                # Local SMTP (no auth required)
                return await self._send_local(msg)
                
        except Exception as e:
            logger.error(f"Mail server error: {e}")
            return False
    
    async def send_otp_email(
        self,
        to_email: str,
        otp_code: str,
        user_name: str = "User"
    ) -> bool:
        """Send OTP email with professional template."""
        subject = "Your OpenPolicy Verification Code"
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Verification Code</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">OpenPolicy Verification</h2>
                <p>Hello {user_name},</p>
                <p>Your verification code is:</p>
                <div style="background: #f8f9fa; padding: 20px; text-align: center; border-radius: 8px; margin: 20px 0;">
                    <h1 style="color: #3498db; font-size: 32px; margin: 0; letter-spacing: 5px;">{otp_code}</h1>
                </div>
                <p>This code will expire in 10 minutes.</p>
                <p>If you didn't request this code, please ignore this email.</p>
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="color: #7f8c8d; font-size: 12px;">
                    This is an automated message from OpenPolicy. Please do not reply.
                </p>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def send_parliamentary_alert(
        self,
        to_email: str,
        user_name: str,
        alert_type: str,
        alert_data: dict
    ) -> bool:
        """Send parliamentary alert email (like OpenParliament)."""
        subject = f"Parliamentary Alert: {alert_type}"
        
        if alert_type == "bill_update":
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Bill Update Alert</title>
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c3e50;">Bill Update Alert</h2>
                    <p>Hello {user_name},</p>
                    <p>There's been an update to a bill you're following:</p>
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3>{alert_data.get('bill_title', 'Unknown Bill')}</h3>
                        <p><strong>Status:</strong> {alert_data.get('status', 'Unknown')}</p>
                        <p><strong>Update:</strong> {alert_data.get('description', 'No description available')}</p>
                        <p><strong>Date:</strong> {alert_data.get('date', 'Unknown')}</p>
                    </div>
                    <p>View the full details on OpenPolicy.ca</p>
                    <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                    <p style="color: #7f8c8d; font-size: 12px;">
                        This is an automated alert from OpenPolicy. To unsubscribe, visit your account settings.
                    </p>
                </div>
            </body>
            </html>
            """
        else:
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Parliamentary Alert</title>
            </head>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c3e50;">Parliamentary Alert</h2>
                    <p>Hello {user_name},</p>
                    <p>You have a new parliamentary alert:</p>
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3>{alert_type.replace('_', ' ').title()}</h3>
                        <p>{alert_data.get('description', 'No description available')}</p>
                    </div>
                    <p>View the full details on OpenPolicy.ca</p>
                    <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                    <p style="color: #7f8c8d; font-size: 12px;">
                        This is an automated alert from OpenPolicy. To unsubscribe, visit your account settings.
                    </p>
                </div>
            </body>
            </html>
            """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def _send_authenticated(self, msg: MIMEMultipart) -> bool:
        """Send email using authenticated SMTP."""
        try:
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls(context=context)
                
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
                
            logger.info(f"Email sent successfully via authenticated SMTP")
            return True
            
        except Exception as e:
            logger.error(f"Authenticated SMTP error: {e}")
            return False
    
    async def _send_local(self, msg: MIMEMultipart) -> bool:
        """Send email using local SMTP (no auth required)."""
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    context = ssl.create_default_context()
                    server.starttls(context=context)
                
                server.send_message(msg)
                
            logger.info(f"Email sent successfully via local SMTP")
            return True
            
        except Exception as e:
            logger.error(f"Local SMTP error: {e}")
            return False
    
    async def _add_attachment(self, msg: MIMEMultipart, file_path: str) -> None:
        """Add file attachment to email."""
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {file_path.split("/")[-1]}'
            )
            msg.attach(part)
            
        except Exception as e:
            logger.error(f"Failed to add attachment {file_path}: {e}")


# Global mail server instance
own_mail_server = OwnMailServer()
