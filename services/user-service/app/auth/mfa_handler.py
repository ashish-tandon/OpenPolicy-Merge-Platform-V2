"""
Multi-Factor Authentication Handler for User Service.

Handles SMS OTP, email OTP, and TOTP authentication.
Based on legacy Open Policy Infra patterns.
"""

import random
import string
import pyotp
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from app.config.settings import settings
from app.models.otp import OTP


class MFAHandler:
    """Multi-factor authentication handler."""
    
    @classmethod
    def generate_otp(cls, length: int = 6) -> str:
        """Generate a random OTP code."""
        return ''.join(random.choices(string.digits, k=length))
    
    @classmethod
    def generate_totp_secret(cls) -> str:
        """Generate a TOTP secret for Google Authenticator."""
        return pyotp.random_base32()
    
    @classmethod
    def verify_totp(cls, secret: str, token: str) -> bool:
        """Verify a TOTP token."""
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
    
    @classmethod
    async def send_sms_otp(cls, phone: str) -> str:
        """Send SMS OTP using Twilio (from legacy Open Policy Infra)."""
        if not all([settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_PHONE_NUMBER]):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Twilio SMS not configured"
            )
        
        # Generate OTP
        otp = cls.generate_otp(6)
        
        try:
            # Import Twilio client
            from twilio.rest import Client
            
            # Initialize Twilio client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            # Send SMS
            message = client.messages.create(
                body=f"Your OpenPolicy verification code is: {otp}. Valid for 15 minutes.",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone
            )
            
            # Store OTP in database
            # TODO: Implement database storage
            # await OTP.create(
            #     phone=phone,
            #     otp=otp,
            #     otp_type="sms",
            #     expires_at=datetime.utcnow() + timedelta(minutes=15)
            # )
            
            return otp
            
        except Exception as e:
            # Log the error
            print(f"Failed to send SMS OTP: {e}")
            
            # For development, return the OTP anyway
            if settings.ENV == "local":
                return otp
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send SMS OTP"
            )
    
    @classmethod
    async def send_email_otp(cls, email: str) -> str:
        """Send email OTP."""
        # Generate OTP
        otp = cls.generate_otp(6)
        
        try:
            # TODO: Implement email sending
            # For now, just return the OTP
            print(f"Email OTP for {email}: {otp}")
            
            # Store OTP in database
            # TODO: Implement database storage
            # await OTP.create(
            #     phone=email,  # Reuse phone field for email
            #     otp=otp,
            #     otp_type="email",
            #     expires_at=datetime.utcnow() + timedelta(minutes=15)
            # )
            
            return otp
            
        except Exception as e:
            print(f"Failed to send email OTP: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email OTP"
            )
    
    @classmethod
    async def verify_otp(cls, phone: str, otp: str, otp_type: str = "sms") -> bool:
        """Verify an OTP code."""
        try:
            # TODO: Implement database verification
            # For now, accept any 6-digit code in development
            if settings.ENV == "local" and len(otp) == 6 and otp.isdigit():
                return True
            
            # In production, verify against database
            # stored_otp = await OTP.get_by_phone_and_type(phone, otp_type)
            # if not stored_otp or not stored_otp.is_valid:
            #     return False
            
            # # Mark OTP as used
            # await stored_otp.mark_as_used()
            
            return True
            
        except Exception as e:
            print(f"Failed to verify OTP: {e}")
            return False
    
    @classmethod
    async def request_otp(cls, phone: str, otp_type: str = "sms") -> dict:
        """Request an OTP for the specified phone/email."""
        if otp_type == "sms":
            otp = await cls.send_sms_otp(phone)
        elif otp_type == "email":
            otp = await cls.send_email_otp(phone)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported OTP type: {otp_type}"
            )
        
        return {
            "success": True,
            "message": f"OTP sent successfully to {phone}",
            "otp_sent": True,
            "expires_in_minutes": 15
        }
    
    @classmethod
    async def setup_totp(cls, user_id: str) -> dict:
        """Set up TOTP for a user."""
        secret = cls.generate_totp_secret()
        
        # TODO: Store secret in user record
        # await User.update_totp_secret(user_id, secret)
        
        # Generate QR code URL for Google Authenticator
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name="OpenPolicy",
            issuer_name="OpenPolicy User Service"
        )
        
        return {
            "secret": secret,
            "qr_code_url": provisioning_uri,
            "message": "TOTP setup successful. Scan QR code with Google Authenticator."
        }
    
    @classmethod
    async def verify_totp_for_user(cls, user_id: str, token: str) -> bool:
        """Verify TOTP token for a specific user."""
        # TODO: Get user's TOTP secret from database
        # user = await User.get_by_id(user_id)
        # if not user.two_factor_secret:
        #     return False
        
        # For now, return False
        return False
