"""
Configuration settings for the OpenPolicy API Gateway.

Uses Pydantic settings management with environment variable support.
"""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Merge V2 API Gateway"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "dev_secret_key_change_in_production"
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8080"
    ]
    
    # Database settings
    DATABASE_URL: str = "postgresql://merge_v2_user:merge_v2_password@localhost:5432/merge_v2_dev"

    # Redis settings
    REDIS_URL: str = "redis://localhost:6379"

    # API settings
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
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()
