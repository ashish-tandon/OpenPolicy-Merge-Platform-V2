"""
FREE Email Service using Resend.com

Resend.com offers:
- 100 emails/day FREE
- 3,000 emails/month FREE
- Professional email delivery
- No credit card required
- Simple API
"""

import httpx
from typing import Optional, List
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)


class ResendEmailService:
    """FREE email service using Resend.com API."""
    
    def __init__(self):
        self.api_key = settings.RESEND_API_KEY
        self.base_url = "https://api.resend.com"
        self.from_email = settings.FROM_EMAIL or "noreply@openpolicy.me"
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send email using Resend.com FREE API."""
        try:
            if not self.api_key:
                logger.warning("Resend API key not configured, using mock email")
                return await self._mock_send_email(to_email, subject, html_content)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/emails",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "from": self.from_email,
                        "to": [to_email],
                        "subject": subject,
                        "html": html_content,
                        "text": text_content or self._html_to_text(html_content)
                    }
                )
                
                if response.status_code == 200:
                    logger.info(f"Email sent successfully to {to_email}")
                    return True
                else:
                    logger.error(f"Failed to send email: {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Email service error: {e}")
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
    
    async def send_welcome_email(
        self,
        to_email: str,
        user_name: str
    ) -> bool:
        """Send welcome email to new users."""
        subject = "Welcome to OpenPolicy!"
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Welcome to OpenPolicy</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Welcome to OpenPolicy!</h2>
                <p>Hello {user_name},</p>
                <p>Thank you for joining OpenPolicy! We're excited to have you on board.</p>
                <p>With OpenPolicy, you can:</p>
                <ul>
                    <li>Track legislation and bills</li>
                    <li>Connect with representatives</li>
                    <li>Stay informed about government activities</li>
                    <li>Participate in democratic processes</li>
                </ul>
                <p>Get started by exploring our platform!</p>
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="color: #7f8c8d; font-size: 12px;">
                    This is an automated message from OpenPolicy. Please do not reply.
                </p>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def send_password_reset_email(
        self,
        to_email: str,
        reset_token: str,
        user_name: str = "User"
    ) -> bool:
        """Send password reset email."""
        subject = "Reset Your OpenPolicy Password"
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Password Reset</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Password Reset Request</h2>
                <p>Hello {user_name},</p>
                <p>We received a request to reset your password.</p>
                <p>Click the button below to reset your password:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" style="background: #3498db; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">Reset Password</a>
                </div>
                <p>If the button doesn't work, copy and paste this link:</p>
                <p style="word-break: break-all; color: #3498db;">{reset_url}</p>
                <p>This link will expire in 1 hour.</p>
                <p>If you didn't request this reset, please ignore this email.</p>
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="color: #7f8c8d; font-size: 12px;">
                    This is an automated message from OpenPolicy. Please do not reply.
                </p>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    def _html_to_text(self, html: str) -> str:
        """Convert HTML to plain text."""
        import re
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    async def _mock_send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str
    ) -> bool:
        """Mock email service for development/testing."""
        logger.info(f"MOCK EMAIL SENT:")
        logger.info(f"  To: {to_email}")
        logger.info(f"  Subject: {subject}")
        logger.info(f"  Content: {html_content[:100]}...")
        return True


# Global email service instance
email_service = ResendEmailService()

