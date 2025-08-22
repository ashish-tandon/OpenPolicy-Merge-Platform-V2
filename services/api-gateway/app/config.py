"""
Configuration settings for Merge V2 API Gateway
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Application settings
    APP_NAME: str = "Merge V2 API Gateway"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "dev_secret_key_change_in_production"
    
    # Security settings
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Web frontend
        "http://localhost:3001",  # Admin frontend
        "http://localhost:8000",  # API Gateway
        "http://localhost:8001",  # ETL Service
        "http://localhost:8002",  # User Service
    ]
    
    # Database settings
    DATABASE_URL: str = "postgresql://merge_v2_user:merge_v2_password@localhost:5432/merge_v2_dev"
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379"
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Merge V2"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    API_WORKERS: int = 1
    
    # Security settings
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Monitoring
    ENABLE_METRICS: bool = True
    
    # External APIs
    OPENPARLIAMENT_API_KEY: str = ""
    CIVIC_SCRAPER_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Override with environment variables if present
if os.getenv("DATABASE_URL"):
    settings.DATABASE_URL = os.getenv("DATABASE_URL")
if os.getenv("REDIS_URL"):
    settings.REDIS_URL = os.getenv("REDIS_URL")
if os.getenv("SECRET_KEY"):
    settings.SECRET_KEY = os.getenv("SECRET_KEY")
if os.getenv("DEBUG"):
    settings.DEBUG = os.getenv("DEBUG").lower() == "true"
if os.getenv("LOG_LEVEL"):
    settings.LOG_LEVEL = os.getenv("LOG_LEVEL")
