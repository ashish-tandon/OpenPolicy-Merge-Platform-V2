"""
Apprise Integration Service

Apprise is a Python library that supports 80+ notification services:
- Email, SMS, Slack, Discord, Telegram, WhatsApp
- Push notifications, desktop notifications
- Custom webhooks, form submissions
- 100% FREE with MIT license
- Perfect Python integration

This gives us enterprise-grade notifications with zero costs!
"""

import apprise
from typing import Dict, List, Optional, Union
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)


class AppriseService:
    """Integration with Apprise notification library."""
    
    def __init__(self):
        self.apobj = apprise.Apprise()
        self._setup_default_services()
    
    def _setup_default_services(self):
        """Setup default notification services from config."""
        # Add email service if configured
        if settings.SMTP_HOST and settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
            email_url = f"mailto://{settings.SMTP_USERNAME}:{settings.SMTP_PASSWORD}@{settings.SMTP_HOST}:{settings.SMTP_PORT}"
            self.apobj.add(email_url, tag='email')
            logger.info("Email service configured")
        
        # Add Resend.com if configured
        if settings.RESEND_API_KEY:
            resend_url = f"resend://{settings.RESEND_API_KEY}:{settings.FROM_EMAIL}/"
            self.apobj.add(resend_url, tag='email')
            logger.info("Resend.com service configured")
        
        # Add Slack if configured
        if hasattr(settings, 'SLACK_WEBHOOK_URL') and settings.SLACK_WEBHOOK_URL:
            slack_url = f"slack://{settings.SLACK_WEBHOOK_URL}"
            self.apobj.add(slack_url, tag='slack')
            logger.info("Slack service configured")
        
        # Add Discord if configured
        if hasattr(settings, 'DISCORD_WEBHOOK_URL') and settings.DISCORD_WEBHOOK_URL:
            discord_url = f"discord://{settings.DISCORD_WEBHOOK_URL}"
            self.apobj.add(discord_url, tag='discord')
            logger.info("Discord service configured")
        
        # Add Telegram if configured
        if hasattr(settings, 'TELEGRAM_BOT_TOKEN') and hasattr(settings, 'TELEGRAM_CHAT_ID'):
            telegram_url = f"tgram://{settings.TELEGRAM_BOT_TOKEN}/{settings.TELEGRAM_CHAT_ID}"
            self.apobj.add(telegram_url, tag='telegram')
            logger.info("Telegram service configured")
        
        # Add WhatsApp if configured
        if hasattr(settings, 'WHATSAPP_ACCESS_TOKEN') and hasattr(settings, 'WHATSAPP_PHONE_ID'):
            whatsapp_url = f"whatsapp://{settings.WHATSAPP_ACCESS_TOKEN}@{settings.WHATSAPP_PHONE_ID}/"
            self.apobj.add(whatsapp_url, tag='whatsapp')
            logger.info("WhatsApp service configured")
        
        # Add SMS services if configured
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN and settings.TWILIO_PHONE_NUMBER:
            twilio_url = f"twilio://{settings.TWILIO_ACCOUNT_SID}:{settings.TWILIO_AUTH_TOKEN}@{settings.TWILIO_PHONE_NUMBER}/"
            self.apobj.add(twilio_url, tag='sms')
            logger.info("Twilio SMS service configured")
        
        # Add push notification services
        if hasattr(settings, 'FCM_SERVER_KEY'):
            fcm_url = f"fcm://{settings.FCM_SERVER_KEY}/#TOPIC"
            self.apobj.add(fcm_url, tag='push')
            logger.info("Firebase FCM service configured")
        
        if hasattr(settings, 'ONESIGNAL_APP_ID') and hasattr(settings, 'ONESIGNAL_REST_API_KEY'):
            onesignal_url = f"onesignal://{settings.ONESIGNAL_APP_ID}@{settings.ONESIGNAL_REST_API_KEY}/"
            self.apobj.add(onesignal_url, tag='push')
            logger.info("OneSignal service configured")
    
    def add_service(self, url: str, tag: Optional[str] = None) -> bool:
        """Add a custom notification service."""
        try:
            self.apobj.add(url, tag=tag)
            logger.info(f"Added notification service: {url}")
            return True
        except Exception as e:
            logger.error(f"Failed to add notification service: {e}")
            return False
    
    def send_notification(
        self,
        body: str,
        title: Optional[str] = None,
        notify_type: str = "info",
        tag: Optional[str] = None,
        attach: Optional[Union[str, List[str]]] = None
    ) -> bool:
        """
        Send notification through Apprise.
        
        Args:
            body: Message body
            title: Message title (optional)
            notify_type: Type of notification (info, success, warning, failure)
            tag: Specific service tag to notify
            attach: File attachments (optional)
        """
        try:
            result = self.apobj.notify(
                body=body,
                title=title,
                notify_type=notify_type,
                tag=tag,
                attach=attach
            )
            
            if result:
                logger.info(f"Notification sent successfully via tag: {tag or 'all'}")
                return True
            else:
                logger.error(f"Failed to send notification via tag: {tag or 'all'}")
                return False
                
        except Exception as e:
            logger.error(f"Apprise notification error: {e}")
            return False
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """Send email notification."""
        # For email, we need to add the recipient to the URL
        # This is a limitation of Apprise - we need to create a new instance
        email_apobj = apprise.Apprise()
        
        # Add email service with recipient
        if settings.SMTP_HOST and settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
            email_url = f"mailto://{settings.SMTP_USERNAME}:{settings.SMTP_PASSWORD}@{settings.SMTP_HOST}:{settings.SMTP_PORT}/{to_email}"
            email_apobj.add(email_url)
        elif settings.RESEND_API_KEY:
            email_url = f"resend://{settings.RESEND_API_KEY}:{settings.FROM_EMAIL}/{to_email}"
            email_apobj.add(email_url)
        else:
            logger.error("No email service configured")
            return False
        
        try:
            result = email_apobj.notify(
                body=body,
                title=subject,
                notify_type="info",
                attach=attachments
            )
            
            if result:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email to {to_email}")
                return False
                
        except Exception as e:
            logger.error(f"Email notification error: {e}")
            return False
    
    def send_sms(
        self,
        to_phone: str,
        message: str,
        priority: str = "normal"
    ) -> bool:
        """Send SMS notification."""
        # For SMS, we need to add the recipient to the URL
        sms_apobj = apprise.Apprise()
        
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN and settings.TWILIO_PHONE_NUMBER:
            sms_url = f"twilio://{settings.TWILIO_ACCOUNT_SID}:{settings.TWILIO_AUTH_TOKEN}@{settings.TWILIO_PHONE_NUMBER}/{to_phone}"
            sms_apobj.add(sms_url)
        else:
            logger.error("No SMS service configured")
            return False
        
        try:
            result = sms_apobj.notify(
                body=message,
                notify_type="info"
            )
            
            if result:
                logger.info(f"SMS sent successfully to {to_phone}")
                return True
            else:
                logger.error(f"Failed to send SMS to {to_phone}")
                return False
                
        except Exception as e:
            logger.error(f"SMS notification error: {e}")
            return False
    
    def send_otp(
        self,
        recipient: str,
        otp_code: str,
        user_name: str = "User",
        channels: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """Send OTP through multiple channels."""
        if channels is None:
            channels = ["email", "sms"]
        
        results = {}
        
        for channel in channels:
            if channel == "email":
                subject = "Your OpenPolicy Verification Code"
                body = f"Hello {user_name},\n\nYour verification code is: {otp_code}\n\nThis code will expire in 10 minutes.\n\nIf you didn't request this code, please ignore this email."
                results["email"] = self.send_email(recipient, subject, body)
            
            elif channel == "sms":
                message = f"OpenPolicy: Your verification code is {otp_code}. Valid for 10 minutes. Don't share this code."
                results["sms"] = self.send_sms(recipient, message)
            
            elif channel == "slack":
                body = f"🔐 *OTP Verification*\n\nHello {user_name},\nYour verification code is: `{otp_code}`\n\nThis code will expire in 10 minutes."
                results["slack"] = self.send_notification(body, "OpenPolicy OTP", "info", "slack")
            
            elif channel == "discord":
                body = f"🔐 **OTP Verification**\n\nHello {user_name},\nYour verification code is: `{otp_code}`\n\nThis code will expire in 10 minutes."
                results["discord"] = self.send_notification(body, "OpenPolicy OTP", "info", "discord")
            
            elif channel == "telegram":
                body = f"🔐 OTP Verification\n\nHello {user_name},\nYour verification code is: {otp_code}\n\nThis code will expire in 10 minutes."
                results["telegram"] = self.send_notification(body, "OpenPolicy OTP", "info", "telegram")
        
        return results
    
    def send_parliamentary_alert(
        self,
        recipient: str,
        alert_type: str,
        alert_data: Dict,
        channels: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """Send parliamentary alert (like OpenParliament)."""
        if channels is None:
            channels = ["email", "slack"]
        
        title = f"Parliamentary Alert: {alert_type.replace('_', ' ').title()}"
        body = f"""
🏛️ **{title}**

📋 **Details**: {alert_data.get('description', 'No description available')}
📜 **Bill**: {alert_data.get('bill_title', 'N/A')}
👤 **Politician**: {alert_data.get('politician_name', 'N/A')}
📅 **Date**: {alert_data.get('date', 'N/A')}

Stay informed about government activities with OpenPolicy!
        """.strip()
        
        results = {}
        
        for channel in channels:
            if channel == "email":
                results["email"] = self.send_email(recipient, title, body)
            
            elif channel == "slack":
                results["slack"] = self.send_notification(body, title, "info", "slack")
            
            elif channel == "discord":
                results["discord"] = self.send_notification(body, title, "info", "discord")
            
            elif channel == "telegram":
                results["telegram"] = self.send_notification(body, title, "info", "telegram")
            
            elif channel == "push":
                results["push"] = self.send_notification(body, title, "info", "push")
        
        return results
    
    def send_welcome(
        self,
        recipient: str,
        user_name: str,
        channels: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """Send welcome notification."""
        if channels is None:
            channels = ["email", "slack"]
        
        title = "Welcome to OpenPolicy!"
        body = f"""
🎉 **Welcome to OpenPolicy, {user_name}!**

Your account has been created successfully. Here's what you can do:

✅ Track legislation and bills
✅ Connect with representatives  
✅ Stay informed about government activities
✅ Participate in democratic processes

Start exploring our platform and stay engaged with democracy!
        """.strip()
        
        results = {}
        
        for channel in channels:
            if channel == "email":
                results["email"] = self.send_email(recipient, title, body)
            
            elif channel == "slack":
                results["slack"] = self.send_notification(body, title, "success", "slack")
            
            elif channel == "discord":
                results["discord"] = self.send_notification(body, title, "success", "discord")
            
            elif channel == "telegram":
                results["telegram"] = self.send_notification(body, title, "success", "telegram")
        
        return results
    
    def get_configured_services(self) -> Dict[str, List[str]]:
        """Get list of configured notification services."""
        services = {}
        
        # Get all configured services by tag
        for tag in self.apobj.get_tags():
            services[tag] = []
            for url in self.apobj.get_urls(tag=tag):
                services[tag].append(str(url))
        
        return services
    
    def test_service(self, tag: str) -> bool:
        """Test a specific notification service."""
        try:
            result = self.apobj.notify(
                body="This is a test notification from OpenPolicy",
                title="Service Test",
                notify_type="info",
                tag=tag
            )
            
            if result:
                logger.info(f"Service test successful for tag: {tag}")
                return True
            else:
                logger.error(f"Service test failed for tag: {tag}")
                return False
                
        except Exception as e:
            logger.error(f"Service test error for tag {tag}: {e}")
            return False


# Global Apprise service instance
apprise_service = AppriseService()
