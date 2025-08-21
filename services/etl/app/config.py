"""
Configuration for OpenParliament.ca V2 ETL Service

Following FUNDAMENTAL RULE: Uses existing configuration patterns
"""

import os
from typing import Optional


def get_database_url() -> str:
    """Get database URL from environment or use default."""
    return os.getenv(
        "DATABASE_URL", 
        "postgresql://ashishtandon@localhost/openpolicy"
    )


def get_etl_config() -> dict:
    """Get ETL service configuration."""
    return {
        "database_url": get_database_url(),
        "batch_size": int(os.getenv("ETL_BATCH_SIZE", "10")),
        "max_workers": int(os.getenv("ETL_MAX_WORKERS", "4")),
        "retry_attempts": int(os.getenv("ETL_RETRY_ATTEMPTS", "3")),
        "retry_delay": int(os.getenv("ETL_RETRY_DELAY", "5")),
    }


# Environment variables
ETL_ENV = os.getenv("ETL_ENV", "development")
DEBUG = ETL_ENV == "development"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
