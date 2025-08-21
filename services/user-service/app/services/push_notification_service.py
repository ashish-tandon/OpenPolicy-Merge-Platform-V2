"""
FREE Push Notification Service

Multiple FREE options:
1. Web Push API (Browser-based) - 100% FREE
2. Firebase Cloud Messaging (FCM) - 100% FREE
3. OneSignal - 10,000 notifications/month FREE
4. Pushwoosh - 1,000,000 notifications/month FREE
"""

import json
import asyncio
from typing import Dict, List, Optional, Union
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)


class WebPushService:
    """FREE Web Push API service (100% free, no limits)."""
    
    def __init__(self):
        self.vapid_public_key = settings.VAPID_PUBLIC_KEY
        self.vapid_private_key = settings.VAPID_PRIVATE_KEY
    
    async def send_push_notification(
        self,
        subscription_info: Dict,
        title: str,
        body: str,
        data: Optional[Dict] = None,
        icon: Optional[str] = None,
        badge: Optional[str] = None,
        tag: Optional[str] = None
    ) -> bool:
        """Send push notification using Web Push API."""
        try:
            import pywebpush
            
            payload = {
                "title": title,
                "body": body,
                "icon": icon or "/assets/icons/notification.png",
                "badge": badge or "/assets/icons/badge.png",
                "tag": tag,
                "data": data or {}
            }
            
            response = await pywebpush.webpush(
                subscription_info=subscription_info,
                data=json.dumps(payload),
                vapid_private_key=self.vapid_private_key,
                vapid_claims={
                    "sub": "mailto:notifications@openpolicy.me",
                    "aud": subscription_info.get("endpoint")
                }
            )
            
            if response.status_code == 200:
                logger.info(f"Push notification sent successfully")
                return True
            else:
                logger.error(f"Failed to send push notification: {response.text}")
                return False
                
        except ImportError:
            logger.warning("pywebpush not installed, using mock push")
            return await self._mock_send_push(subscription_info, title, body, data)
        except Exception as e:
            logger.error(f"Push notification error: {e}")
            return False
    
    async def _mock_send_push(
        self,
        subscription_info: Dict,
        title: str,
        body: str,
        data: Optional[Dict] = None
    ) -> bool:
        """Mock push service for development."""
        logger.info(f"MOCK PUSH NOTIFICATION:")
        logger.info(f"  Title: {title}")
        logger.info(f"  Body: {body}")
        logger.info(f"  Data: {data}")
        return True


class FirebaseCloudMessaging:
    """FREE Firebase Cloud Messaging (100% free, no limits)."""
    
    def __init__(self):
        self.server_key = settings.FCM_SERVER_KEY
        self.api_url = "https://fcm.googleapis.com/fcm/send"
    
    async def send_push_notification(
        self,
        fcm_token: str,
        title: str,
        body: str,
        data: Optional[Dict] = None,
        image: Optional[str] = None
    ) -> bool:
        """Send push notification using FCM."""
        try:
            import httpx
            
            payload = {
                "to": fcm_token,
                "notification": {
                    "title": title,
                    "body": body,
                    "image": image
                },
                "data": data or {},
                "priority": "high"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"key={self.server_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success") == 1:
                        logger.info(f"FCM notification sent successfully")
                        return True
                    else:
                        logger.error(f"FCM failed: {result}")
                        return False
                else:
                    logger.error(f"FCM HTTP error: {response.status_code}")
                    return False
                    
        except Exception as e:
            logger.error(f"FCM error: {e}")
            return False


class OneSignalService:
    """FREE OneSignal service (10,000 notifications/month free)."""
    
    def __init__(self):
        self.app_id = settings.ONESIGNAL_APP_ID
        self.rest_api_key = settings.ONESIGNAL_REST_API_KEY
        self.api_url = "https://onesignal.com/api/v1/notifications"
    
    async def send_push_notification(
        self,
        player_ids: List[str],
        title: str,
        message: str,
        data: Optional[Dict] = None,
        url: Optional[str] = None
    ) -> bool:
        """Send push notification using OneSignal."""
        try:
            import httpx
            
            payload = {
                "app_id": self.app_id,
                "include_player_ids": player_ids,
                "headings": {"en": title},
                "contents": {"en": message},
                "data": data or {},
                "url": url
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Basic {self.rest_api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
                
                if response.status_code == 200:
                    logger.info(f"OneSignal notification sent successfully")
                    return True
                else:
                    logger.error(f"OneSignal failed: {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"OneSignal error: {e}")
            return False


class MultiPushService:
    """Multi-provider push notification service."""
    
    def __init__(self):
        self.web_push = WebPushService()
        self.fcm = FirebaseCloudMessaging()
        self.onesignal = OneSignalService()
    
    async def send_notification(
        self,
        user_id: str,
        title: str,
        body: str,
        data: Optional[Dict] = None,
        notification_type: str = "web_push"
    ) -> bool:
        """Send notification using specified provider."""
        try:
            if notification_type == "web_push":
                # Get user's web push subscription
                subscription = await self._get_user_web_push_subscription(user_id)
                if subscription:
                    return await self.web_push.send_push_notification(
                        subscription, title, body, data
                    )
            
            elif notification_type == "fcm":
                # Get user's FCM token
                fcm_token = await self._get_user_fcm_token(user_id)
                if fcm_token:
                    return await self.fcm.send_push_notification(
                        fcm_token, title, body, data
                    )
            
            elif notification_type == "onesignal":
                # Get user's OneSignal player ID
                player_id = await self._get_user_onesignal_id(user_id)
                if player_id:
                    return await self.onesignal.send_push_notification(
                        [player_id], title, body, data
                    )
            
            logger.warning(f"No {notification_type} subscription found for user {user_id}")
            return False
            
        except Exception as e:
            logger.error(f"Push notification error: {e}")
            return False
    
    async def send_bulk_notification(
        self,
        user_ids: List[str],
        title: str,
        body: str,
        data: Optional[Dict] = None,
        notification_type: str = "web_push"
    ) -> Dict[str, bool]:
        """Send notification to multiple users."""
        results = {}
        
        for user_id in user_ids:
            success = await self.send_notification(
                user_id, title, body, data, notification_type
            )
            results[user_id] = success
        
        return results
    
    async def _get_user_web_push_subscription(self, user_id: str) -> Optional[Dict]:
        """Get user's web push subscription from database."""
        # TODO: Implement database lookup
        return None
    
    async def _get_user_fcm_token(self, user_id: str) -> Optional[str]:
        """Get user's FCM token from database."""
        # TODO: Implement database lookup
        return None
    
    async def _get_user_onesignal_id(self, user_id: str) -> Optional[str]:
        """Get user's OneSignal player ID from database."""
        # TODO: Implement database lookup
        return None


# Global push notification service instance
push_service = MultiPushService()
