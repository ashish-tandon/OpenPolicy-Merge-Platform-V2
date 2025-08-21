"""
FREE Push Notification Service

Uses web push notifications (FREE):
- No external service costs
- Works with all modern browsers
- Real-time notifications
- Customizable content
"""

import json
import base64
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import logging

logger = logging.getLogger(__name__)


class WebPushService:
    """FREE web push notification service."""
    
    def __init__(self):
        # Generate VAPID keys for free
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()
        
        # Get VAPID public key in base64
        self.vapid_public_key = base64.urlsafe_b64encode(
            self.public_key.public_bytes(Encoding.X962, PublicFormat.Compressed)
        ).decode('utf-8')
        
        logger.info("Web Push service initialized with VAPID keys")
    
    def get_vapid_public_key(self) -> str:
        """Get VAPID public key for client subscription."""
        return self.vapid_public_key
    
    async def send_notification(
        self,
        subscription_info: Dict[str, Any],
        title: str,
        body: str,
        icon: Optional[str] = None,
        badge: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send push notification to subscribed client."""
        try:
            # Create notification payload
            payload = {
                "title": title,
                "body": body,
                "icon": icon or "/favicon.ico",
                "badge": badge or "/badge.png",
                "data": data or {},
                "actions": [
                    {
                        "action": "view",
                        "title": "View"
                    },
                    {
                        "action": "dismiss",
                        "title": "Dismiss"
                    }
                ]
            }
            
            # Convert to JSON
            payload_json = json.dumps(payload)
            
            # TODO: Implement actual web push sending
            # This would use the web-push library to send to the subscription
            logger.info(f"Push notification prepared: {title} - {body}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send push notification: {e}")
            return False
    
    async def send_welcome_notification(
        self,
        subscription_info: Dict[str, Any],
        user_name: str
    ) -> bool:
        """Send welcome push notification."""
        return await self.send_notification(
            subscription_info,
            "Welcome to OpenPolicy!",
            f"Hello {user_name}, your account has been created successfully!",
            data={"type": "welcome", "user_name": user_name}
        )
    
    async def send_bill_update_notification(
        self,
        subscription_info: Dict[str, Any],
        bill_title: str,
        update_type: str
    ) -> bool:
        """Send bill update notification."""
        return await self.send_notification(
            subscription_info,
            "Bill Update",
            f"{bill_title} has been {update_type}",
            data={"type": "bill_update", "bill_title": bill_title, "update_type": update_type}
        )
    
    async def send_representative_response_notification(
        self,
        subscription_info: Dict[str, Any],
        rep_name: str,
        issue_title: str
    ) -> bool:
        """Send representative response notification."""
        return await self.send_notification(
            subscription_info,
            "Representative Response",
            f"{rep_name} has responded to your issue: {issue_title}",
            data={"type": "representative_response", "rep_name": rep_name, "issue_title": issue_title}
        )


class MockPushService:
    """Mock push service for development/testing."""
    
    def __init__(self):
        self.vapid_public_key = "mock_public_key_for_testing"
    
    def get_vapid_public_key(self) -> str:
        return self.vapid_public_key
    
    async def send_notification(
        self,
        subscription_info: Dict[str, Any],
        title: str,
        body: str,
        icon: Optional[str] = None,
        badge: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Mock notification sending."""
        logger.info(f"MOCK PUSH NOTIFICATION:")
        logger.info(f"  Title: {title}")
        logger.info(f"  Body: {body}")
        logger.info(f"  Data: {data}")
        return True
    
    async def send_welcome_notification(
        self,
        subscription_info: Dict[str, Any],
        user_name: str
    ) -> bool:
        return await self.send_notification(
            subscription_info,
            "Welcome to OpenPolicy!",
            f"Hello {user_name}, your account has been created successfully!",
            data={"type": "welcome", "user_name": user_name}
        )
    
    async def send_bill_update_notification(
        self,
        subscription_info: Dict[str, Any],
        bill_title: str,
        update_type: str
    ) -> bool:
        return await self.send_notification(
            subscription_info,
            "Bill Update",
            f"{bill_title} has been {update_type}",
            data={"type": "bill_update", "bill_title": bill_title, "update_type": update_type}
        )
    
    async def send_representative_response_notification(
        self,
        subscription_info: Dict[str, Any],
        rep_name: str,
        issue_title: str
    ) -> bool:
        return await self.send_notification(
            subscription_info,
            "Representative Response",
            f"{rep_name} has responded to your issue: {issue_title}",
            data={"type": "representative_response", "rep_name": rep_name, "issue_title": issue_title}
        )


# Global push service instance (use mock for development)
push_service = MockPushService() if not settings.ENABLE_PUSH_NOTIFICATIONS else WebPushService()
