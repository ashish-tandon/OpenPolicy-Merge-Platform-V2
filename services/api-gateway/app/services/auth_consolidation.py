"""
Authentication Consolidation Service

This service demonstrates how to consolidate the three authentication
implementations into a single, unified service while preserving all
existing functionality.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.models.users import User, OAuthAccount, UserSession
from app.models.legacy_users import LegacyUser
from app.config import settings
from app.core.security import create_access_token, verify_password

logger = logging.getLogger(__name__)

class AuthenticationConsolidationService:
    """
    Unified authentication service that consolidates:
    1. API Gateway JWT auth
    2. User Service parallel auth
    3. Legacy Django token auth
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user across all systems
        
        Priority:
        1. Check new unified user table
        2. Check legacy Django users
        3. Check user service mock data (for migration)
        """
        # First, try new unified system
        user = self._authenticate_unified(username, password)
        if user:
            logger.info(f"User {username} authenticated via unified system")
            return user
            
        # Second, try legacy Django users
        user = self._authenticate_legacy(username, password)
        if user:
            logger.info(f"User {username} authenticated via legacy system")
            # Migrate user to new system
            return await self._migrate_legacy_user(user)
            
        # Third, check user service temporary accounts
        user = self._authenticate_user_service(username, password)
        if user:
            logger.info(f"User {username} authenticated via user service")
            return user
            
        return None
        
    def _authenticate_unified(self, username: str, password: str) -> Optional[User]:
        """Authenticate against unified user table"""
        user = self.db.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user:
            return None
            
        if not verify_password(password, user.hashed_password):
            return None
            
        if not user.is_active:
            return None
            
        return user
        
    def _authenticate_legacy(self, username: str, password: str) -> Optional[LegacyUser]:
        """
        Authenticate against legacy Django users
        
        Note: Legacy system used email-based token auth,
        so we need special handling for password verification
        """
        legacy_user = self.db.query(LegacyUser).filter(
            LegacyUser.email == username
        ).first()
        
        if not legacy_user:
            return None
            
        # Legacy system didn't have passwords, used tokens
        # Check if user has been given a temporary password
        if hasattr(legacy_user, 'temp_password'):
            if verify_password(password, legacy_user.temp_password):
                return legacy_user
                
        # Check if this is a token-based login
        if self._verify_legacy_token(username, password):
            return legacy_user
            
        return None
        
    def _authenticate_user_service(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate against user service accounts
        
        Note: User service had mock data during development
        This preserves that functionality during migration
        """
        # TODO: Remove this after full migration
        if username == "demo@example.com" and password == "demo":
            return User(
                id="mock-user-id",
                username="demo",
                email="demo@example.com",
                full_name="Demo User",
                is_active=True,
                is_superuser=False
            )
        return None
        
    async def _migrate_legacy_user(self, legacy_user: LegacyUser) -> User:
        """
        Migrate a legacy Django user to the new system
        
        Preserves:
        - Email and name
        - Preferences from JSON data field
        - Login history
        - Bounce tracking for notifications
        """
        # Check if already migrated
        existing = self.db.query(User).filter(
            User.email == legacy_user.email
        ).first()
        
        if existing:
            return existing
            
        # Create new user
        new_user = User(
            username=legacy_user.email.split('@')[0],  # Generate username
            email=legacy_user.email,
            full_name=legacy_user.name or "",
            is_active=True,
            is_email_verified=True,  # Legacy users were verified
            email_bouncing=legacy_user.email_bouncing,
            email_bounce_reason=legacy_user.email_bounce_reason,
            created_at=legacy_user.created,
            last_login=legacy_user.last_login,
            # Preserve legacy data
            metadata={
                "migrated_from": "legacy_django",
                "migration_date": datetime.utcnow().isoformat(),
                "legacy_id": legacy_user.id,
                "legacy_data": legacy_user.data  # Preserve JSON preferences
            }
        )
        
        # Generate secure password for migrated user
        temp_password = self._generate_migration_password()
        new_user.hashed_password = self.pwd_context.hash(temp_password)
        
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        
        # Queue email to user about migration
        await self._send_migration_email(new_user, temp_password)
        
        logger.info(f"Migrated legacy user {legacy_user.email} to new system")
        return new_user
        
    def _verify_legacy_token(self, email: str, token: str) -> bool:
        """
        Verify legacy email-based login tokens
        
        Legacy system sent login links with tokens
        """
        # TODO: Implement legacy token verification
        # This would check against legacy token table
        return False
        
    def _generate_migration_password(self) -> str:
        """Generate secure temporary password for migrated users"""
        import secrets
        import string
        
        alphabet = string.ascii_letters + string.digits