"""
Notification Orchestrator

Intelligently routes notifications through the best available FREE service:
1. Email: Resend.com (100/day free) → Our Mail Server (100% free)
2. Push: Web Push API (100% free) → FCM (100% free) → OneSignal (10k/month free)
3. SMS: Our SMS Gateway (100% free) → Twilio (pay-per-use)

This gives us professional notifications with zero monthly costs!
"""

from typing import Dict, List, Optional
from app.services.email_service import email_service
from app.services.own_mail_server import own_mail_server
from app.services.push_notification_service import push_service
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)


class NotificationOrchestrator:
    """Intelligent notification routing through FREE services."""
    
    def __init__(self):
        self.email_services = [
            ("resend", email_service),
            ("own_mail", own_mail_server)
        ]
        self.push_services = [
            ("web_push", "web_push"),
            ("fcm", "fcm"),
            ("onesignal", "onesignal")
        ]
    
    async def send_notification(
        self,
        user_id: str,
        notification_type: str,
        title: str,
        message: str,
        data: Optional[Dict] = None,
        channels: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """
        Send notification through multiple channels intelligently.
        
        Args:
            user_id: User to notify
            notification_type: Type of notification (otp, alert, welcome, etc.)
            title: Notification title
            message: Notification message
            data: Additional data
            channels: Specific channels to use (email, push, sms)
        """
        if not channels:
            channels = ["email", "push"]  # Default channels
        
        results = {}
        
        # Send through each requested channel
        for channel in channels:
            if channel == "email":
                results["email"] = await self._send_email_notification(
                    user_id, notification_type, title, message, data
                )
            elif channel == "push":
                results["push"] = await self._send_push_notification(
                    user_id, title, message, data
                )
            elif channel == "sms":
                results["sms"] = await self._send_sms_notification(
                    user_id, title, message, data
                )
        
        return results
    
    async def send_parliamentary_alert(
        self,
        user_id: str,
        alert_type: str,
        alert_data: dict,
        channels: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """Send parliamentary alert (like OpenParliament)."""
        title = f"Parliamentary Alert: {alert_type.replace('_', ' ').title()}"
        message = alert_data.get('description', 'No description available')
        
        return await self.send_notification(
            user_id, "parliamentary_alert", title, message, alert_data, channels
        )
    
    async def send_otp(
        self,
        user_id: str,
        otp_code: str,
        user_name: str = "User",
        channels: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """Send OTP through multiple channels."""
        title = "Your OpenPolicy Verification Code"
        message = f"Your verification code is: {otp_code}"
        data = {"otp_code": otp_code, "user_name": user_name}
        
        return await self.send_notification(
            user_id, "otp", title, message, data, channels
        )
    
    async def send_welcome(
        self,
        user_id: str,
        user_name: str,
        channels: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """Send welcome notification."""
        title = "Welcome to OpenPolicy!"
        message = f"Hello {user_name}, welcome to OpenPolicy!"
        data = {"user_name": user_name}
        
        return await self.send_notification(
            user_id, "welcome", title, message, data, channels
        )
    
    async def _send_email_notification(
        self,
        user_id: str,
        notification_type: str,
        title: str,
        message: str,
        data: Optional[Dict] = None
    ) -> bool:
        """Send email notification through best available service."""
        try:
            # Get user's email address
            user_email = await self._get_user_email(user_id)
            if not user_email:
                logger.warning(f"No email found for user {user_id}")
                return False
            
            # Try each email service in order
            for service_name, service in self.email_services:
                try:
                    if service_name == "resend" and settings.RESEND_API_KEY:
                        # Use Resend.com (100 emails/day free)
                        if notification_type == "otp":
                            success = await service.send_otp_email(
                                user_email, data.get("otp_code", ""), data.get("user_name", "User")
                            )
                        elif notification_type == "welcome":
                            success = await service.send_welcome_email(
                                user_email, data.get("user_name", "User")
                            )
                        elif notification_type == "parliamentary_alert":
                            success = await service.send_parliamentary_alert(
                                user_email, data.get("user_name", "User"),
                                data.get("alert_type", ""), data
                            )
                        else:
                            success = await service.send_email(
                                user_email, title, message
                            )
                        
                        if success:
                            logger.info(f"Email sent via {service_name}")
                            return True
                    
                    elif service_name == "own_mail":
                        # Use our own mail server (100% free)
                        if notification_type == "otp":
                            success = await service.send_otp_email(
                                user_email, data.get("otp_code", ""), data.get("user_name", "User")
                            )
                        elif notification_type == "parliamentary_alert":
                            success = await service.send_parliamentary_alert(
                                user_email, data.get("user_name", "User"),
                                data.get("alert_type", ""), data
                            )
                        else:
                            success = await service.send_email(
                                user_email, title, message
                            )
                        
                        if success:
                            logger.info(f"Email sent via {service_name}")
                            return True
                
                except Exception as e:
                    logger.error(f"Email service {service_name} failed: {e}")
                    continue
            
            logger.error("All email services failed")
            return False
            
        except Exception as e:
            logger.error(f"Email notification error: {e}")
            return False
    
    async def _send_push_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        data: Optional[Dict] = None
    ) -> bool:
        """Send push notification through best available service."""
        try:
            # Try each push service in order
            for service_name, service_type in self.push_services:
                try:
                    success = await push_service.send_notification(
                        user_id, title, message, data, service_type
                    )
                    
                    if success:
                        logger.info(f"Push notification sent via {service_name}")
                        return True
                
                except Exception as e:
                    logger.error(f"Push service {service_name} failed: {e}")
                    continue
            
            logger.error("All push services failed")
            return False
            
        except Exception as e:
            logger.error(f"Push notification error: {e}")
            return False
    
    async def _send_sms_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        data: Optional[Dict] = None
    ) -> bool:
        """Send SMS notification (placeholder for future implementation)."""
        # TODO: Implement SMS service
        logger.info(f"SMS notification requested for user {user_id}: {title} - {message}")
        return False
    
    async def _get_user_email(self, user_id: str) -> Optional[str]:
        """Get user's email address from database."""
        # TODO: Implement database lookup
        # For now, return a mock email
        return f"user{user_id}@example.com"
    
    async def send_bulk_notification(
        self,
        user_ids: List[str],
        notification_type: str,
        title: str,
        message: str,
        data: Optional[Dict] = None,
        channels: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, bool]]:
        """Send notification to multiple users."""
        results = {}
        
        for user_id in user_ids:
            user_results = await self.send_notification(
                user_id, notification_type, title, message, data, channels
            )
            results[user_id] = user_results
        
        return results


# Global notification orchestrator instance
notification_orchestrator = NotificationOrchestrator()
