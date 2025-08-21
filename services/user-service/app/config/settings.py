"""
Configuration settings for the User Service.

Separate from main application settings to maintain clean architecture.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Service Configuration
    SERVICE_NAME: str = "user-service"
    SERVICE_PORT: int = 8081
    DEBUG: bool = False
    
    # Database Configuration
    USER_DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/openpolicy_users"
    
    # JWT Configuration
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # OAuth Configuration
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/1"
    
    # File Storage Configuration
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_IMAGE_TYPES: list = ["jpg", "jpeg", "png", "gif"]
    
    # Frontend URL (for password reset links)
    FRONTEND_URL: str = "http://localhost:3000"
    
    # ===== FREE EMAIL SERVICES =====
    
    # Option 1: Resend.com (100 emails/day FREE)
    RESEND_API_KEY: Optional[str] = None
    FROM_EMAIL: str = "noreply@openpolicy.me"
    
    # Option 2: Our Own Mail Server (100% FREE)
    OWN_SMTP_HOST: Optional[str] = None  # e.g., "localhost" or "mail.openpolicy.me"
    OWN_SMTP_PORT: int = 587
    OWN_SMTP_USER: Optional[str] = None
    OWN_SMTP_PASSWORD: Optional[str] = None
    OWN_SMTP_USE_TLS: bool = True
    
    # Option 3: Legacy SMTP (for compatibility)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # ===== FREE PUSH NOTIFICATION SERVICES =====
    
    # Option 1: Web Push API (100% FREE, no limits)
    VAPID_PUBLIC_KEY: Optional[str] = None
    VAPID_PRIVATE_KEY: Optional[str] = None
    
    # Option 2: Firebase Cloud Messaging (100% FREE, no limits)
    FCM_SERVER_KEY: Optional[str] = None
    
    # Option 3: OneSignal (10,000 notifications/month FREE)
    ONESIGNAL_APP_ID: Optional[str] = None
    ONESIGNAL_REST_API_KEY: Optional[str] = None
    
    # ===== FREE SMS SERVICES =====
    
    # Option 1: Twilio (Free trial, then pay-per-use)
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    
    # Option 2: Our Own SMS Gateway (100% FREE with hardware)
    OWN_SMS_GATEWAY_URL: Optional[str] = None
    OWN_SMS_API_KEY: Optional[str] = None
    
    # ===== NOTIFICO - OPEN SOURCE NOTIFICATION SERVER =====
    
    # Notifico Configuration (Rust-based, 100% FREE)
    NOTIFICO_URL: str = "http://localhost:8083"
    NOTIFICO_API_KEY: Optional[str] = None
    NOTIFICO_WEBHOOK_SECRET: Optional[str] = None
    
    # ===== APPRISE - PYTHON-NATIVE NOTIFICATION LIBRARY =====
    
    # Apprise Configuration (Python-native, 100% FREE, 80+ services)
    # Slack Integration
    SLACK_WEBHOOK_URL: Optional[str] = None
    
    # Discord Integration  
    DISCORD_WEBHOOK_URL: Optional[str] = None
    
    # Telegram Integration
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None
    
    # WhatsApp Business Integration
    WHATSAPP_ACCESS_TOKEN: Optional[str] = None
    WHATSAPP_PHONE_ID: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
