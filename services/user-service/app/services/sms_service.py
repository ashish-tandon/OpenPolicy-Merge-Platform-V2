"""
FREE SMS Service with Multiple Options

Available FREE SMS services:
1. Twilio (FREE trial - $15 credit)
2. Vonage (FREE trial - $2 credit)
3. Plivo (FREE trial - $20 credit)
4. Mock SMS (for development)
"""

import httpx
from typing import Optional
from app.config.settings import settings
import logging
import random

logger = logging.getLogger(__name__)


class TwilioSMSService:
    """Twilio SMS service (FREE trial with $15 credit)."""
    
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.phone_number = settings.TWILIO_PHONE_NUMBER
        self.base_url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}"
    
    async def send_sms(self, to_phone: str, message: str) -> bool:
        """Send SMS using Twilio."""
        try:
            if not all([self.account_sid, self.auth_token, self.phone_number]):
                logger.warning("Twilio credentials not configured")
                return False
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/Messages.json",
                    auth=(self.account_sid, self.auth_token),
                    data={
                        "From": self.phone_number,
                        "To": to_phone,
                        "Body": message
                    }
                )
                
                if response.status_code == 201:
                    logger.info(f"SMS sent successfully to {to_phone}")
                    return True
                else:
                    logger.error(f"Failed to send SMS: {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Twilio SMS error: {e}")
            return False


class VonageSMSService:
    """Vonage SMS service (FREE trial with $2 credit)."""
    
    def __init__(self):
        self.api_key = settings.VONAGE_API_KEY
        self.api_secret = settings.VONAGE_API_SECRET
        self.from_name = settings.VONAGE_FROM_NAME or "OpenPolicy"
        self.base_url = "https://rest.nexmo.com/sms/json"
    
    async def send_sms(self, to_phone: str, message: str) -> bool:
        """Send SMS using Vonage."""
        try:
            if not all([self.api_key, self.api_secret]):
                logger.warning("Vonage credentials not configured")
                return False
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    data={
                        "api_key": self.api_key,
                        "api_secret": self.api_secret,
                        "from": self.from_name,
                        "to": to_phone,
                        "text": message
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("messages", [{}])[0].get("status") == "0":
                        logger.info(f"SMS sent successfully to {to_phone}")
                        return True
                    else:
                        logger.error(f"Failed to send SMS: {data}")
                        return False
                else:
                    logger.error(f"Failed to send SMS: {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Vonage SMS error: {e}")
            return False


class PlivoSMSService:
    """Plivo SMS service (FREE trial with $20 credit)."""
    
    def __init__(self):
        self.auth_id = settings.PLIVO_AUTH_ID
        self.auth_token = settings.PLIVO_AUTH_TOKEN
        self.from_phone = settings.PLIVO_FROM_PHONE
        self.base_url = "https://api.plivo.com/v1/Account"
    
    async def send_sms(self, to_phone: str, message: str) -> bool:
        """Send SMS using Plivo."""
        try:
            if not all([self.auth_id, self.auth_token, self.from_phone]):
                logger.warning("Plivo credentials not configured")
                return False
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/{self.auth_id}/Message/",
                    auth=(self.auth_id, self.auth_token),
                    json={
                        "src": self.from_phone,
                        "dst": to_phone,
                        "text": message
                    }
                )
                
                if response.status_code == 202:
                    logger.info(f"SMS sent successfully to {to_phone}")
                    return True
                else:
                    logger.error(f"Failed to send SMS: {response.text}")
                    return False
                    
        except Exception as e:
            logger.error(f"Plivo SMS error: {e}")
            return False


class MockSMSService:
    """Mock SMS service for development/testing."""
    
    async def send_sms(self, to_phone: str, message: str) -> bool:
        """Mock SMS sending."""
        logger.info(f"MOCK SMS SENT:")
        logger.info(f"  To: {to_phone}")
        logger.info(f"  Message: {message}")
        return True


class MultiSMSService:
    """Multi-provider SMS service with fallback."""
    
    def __init__(self):
        self.services = []
        
        # Add available services
        if settings.TWILIO_ACCOUNT_SID:
            self.services.append(TwilioSMSService())
        if settings.VONAGE_API_KEY:
            self.services.append(VonageSMSService())
        if settings.PLIVO_AUTH_ID:
            self.services.append(PlivoSMSService())
        
        # Always add mock service as fallback
        self.services.append(MockSMSService())
        
        logger.info(f"Initialized SMS service with {len(self.services)} providers")
    
    async def send_sms(self, to_phone: str, message: str) -> bool:
        """Send SMS using available services with fallback."""
        for service in self.services:
            try:
                if await service.send_sms(to_phone, message):
                    return True
            except Exception as e:
                logger.warning(f"SMS service {service.__class__.__name__} failed: {e}")
                continue
        
        logger.error("All SMS services failed")
        return False
    
    async def send_otp_sms(
        self,
        to_phone: str,
        otp_code: str,
        user_name: str = "User"
    ) -> bool:
        """Send OTP SMS with professional message."""
        message = f"OpenPolicy: Your verification code is {otp_code}. Valid for 10 minutes. Don't share this code."
        return await self.send_sms(to_phone, message)
    
    async def send_welcome_sms(
        self,
        to_phone: str,
        user_name: str
    ) -> bool:
        """Send welcome SMS to new users."""
        message = f"Welcome to OpenPolicy, {user_name}! Your account has been created successfully. Start exploring our platform!"
        return await self.send_sms(to_phone, message)


# Global SMS service instance
sms_service = MultiSMSService()

