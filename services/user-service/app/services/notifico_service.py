"""
Notifico Integration Service

Notifico is an open-source notification server built with Rust that supports:
- Email, SMS, Slack, Telegram, WhatsApp Business
- No-code configuration
- Powerful templating language
- Admin interface for management
- Webhook support for easy integration

This gives us enterprise-grade notifications with zero monthly costs!
"""

import httpx
from typing import Dict, List, Optional
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)


class NotificoService:
    """Integration with Notifico notification server."""
    
    def __init__(self):
        self.base_url = settings.NOTIFICO_URL or "http://localhost:8083"
        self.api_key = settings.NOTIFICO_API_KEY
        self.webhook_url = f"{self.base_url}/webhook"
    
    async def send_notification(
        self,
        channel: str,
        recipient: str,
        template: str,
        data: Dict,
        priority: str = "normal"
    ) -> bool:
        """
        Send notification through Notifico.
        
        Args:
            channel: Notification channel (email, sms, slack, telegram, whatsapp)
            recipient: Recipient identifier (email, phone, user_id)
            template: Template name to use
            data: Template variables
            priority: Priority level (low, normal, high, urgent)
        """
        try:
            payload = {
                "channel": channel,
                "recipient": recipient,
                "template": template,
                "data": data,
                "priority": priority,
                "metadata": {
                    "source": "openpolicy",
                    "service": "user-service"
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.webhook_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Notifico notification sent successfully: {result.get('id')}")
                    return True
                else:
                    logger.error(f"Notifico failed: {response.status_code} - {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Notifico service error: {e}")
            return False
    
    async def send_email(
        self,
        to_email: str,
        template: str,
        data: Dict,
        priority: str = "normal"
    ) -> bool:
        """Send email notification."""
        return await self.send_notification(
            channel="email",
            recipient=to_email,
            template=template,
            data=data,
            priority=priority
        )
    
    async def send_sms(
        self,
        to_phone: str,
        template: str,
        data: Dict,
        priority: str = "high"
    ) -> bool:
        """Send SMS notification."""
        return await self.send_notification(
            channel="sms",
            recipient=to_phone,
            template=template,
            data=data,
            priority=priority
        )
    
    async def send_slack(
        self,
        channel: str,
        template: str,
        data: Dict,
        priority: str = "normal"
    ) -> bool:
        """Send Slack notification."""
        return await self.send_notification(
            channel="slack",
            recipient=channel,
            template=template,
            data=data,
            priority=priority
        )
    
    async def send_telegram(
        self,
        chat_id: str,
        template: str,
        data: Dict,
        priority: str = "normal"
    ) -> bool:
        """Send Telegram notification."""
        return await self.send_notification(
            channel="telegram",
            recipient=chat_id,
            template=template,
            data=data,
            priority=priority
        )
    
    async def send_whatsapp(
        self,
        to_phone: str,
        template: str,
        data: Dict,
        priority: str = "high"
    ) -> bool:
        """Send WhatsApp Business notification."""
        return await self.send_notification(
            channel="whatsapp",
            recipient=to_phone,
            template=template,
            data=data,
            priority=priority
        )
    
    async def send_otp(
        self,
        recipient: str,
        otp_code: str,
        user_name: str = "User",
        channels: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        if channels is None:
            channels = ["email", "sms"]
        """Send OTP through multiple channels."""
        data = {
            "otp_code": otp_code,
            "user_name": user_name,
            "expiry_minutes": 10
        }
        
        results = {}
        for channel in channels:
            if channel == "email":
                results["email"] = await self.send_email(
                    recipient, "otp_verification", data, "high"
                )
            elif channel == "sms":
                results["sms"] = await self.send_sms(
                    recipient, "otp_verification", data, "high"
                )
            elif channel == "whatsapp":
                results["whatsapp"] = await self.send_whatsapp(
                    recipient, "otp_verification", data, "high"
                )
        
        return results
    
    async def send_parliamentary_alert(
        self,
        recipient: str,
        alert_type: str,
        alert_data: Dict,
        channels: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        if channels is None:
            channels = ["email", "push"]
        """Send parliamentary alert (like OpenParliament)."""
        data = {
            "alert_type": alert_type,
            "alert_title": alert_data.get("title", ""),
            "alert_description": alert_data.get("description", ""),
            "bill_title": alert_data.get("bill_title", ""),
            "politician_name": alert_data.get("politician_name", ""),
            "date": alert_data.get("date", ""),
            "priority": alert_data.get("priority", "normal")
        }
        
        results = {}
        for channel in channels:
            if channel == "email":
                results["email"] = await self.send_email(
                    recipient, "parliamentary_alert", data, "normal"
                )
            elif channel == "push":
                results["push"] = await self.send_notification(
                    "push", recipient, "parliamentary_alert", data, "normal"
                )
            elif channel == "slack":
                results["slack"] = await self.send_slack(
                    recipient, "parliamentary_alert", data, "normal"
                )
        
        return results
    
    async def send_welcome(
        self,
        recipient: str,
        user_name: str,
        channels: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        if channels is None:
            channels = ["email", "sms"]
        """Send welcome notification."""
        data = {
            "user_name": user_name,
            "welcome_message": f"Welcome to OpenPolicy, {user_name}!",
            "features": [
                "Track legislation and bills",
                "Connect with representatives", 
                "Stay informed about government activities",
                "Participate in democratic processes"
            ]
        }
        
        results = {}
        for channel in channels:
            if channel == "email":
                results["email"] = await self.send_email(
                    recipient, "welcome", data, "normal"
                )
            elif channel == "sms":
                results["sms"] = await self.send_sms(
                    recipient, "welcome", data, "normal"
                )
        
        return results
    
    async def get_notification_status(self, notification_id: str) -> Optional[Dict]:
        """Get notification delivery status."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/notifications/{notification_id}",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Failed to get notification status: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting notification status: {e}")
            return None
    
    async def get_delivery_stats(self) -> Optional[Dict]:
        """Get notification delivery statistics."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/stats",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"Failed to get delivery stats: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting delivery stats: {e}")
            return None


# Global Notifico service instance
notifico_service = NotificoService()
