"""
JWT Authentication Handler for User Service.

Handles JWT token creation, validation, and refresh.
Separate from legislative data authentication.
"""

import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.settings import settings
from app.models.user import User

# Security scheme for FastAPI
security = HTTPBearer()


class JWTHandler:
    """JWT token management for user authentication."""
    
    @classmethod
    def create_access_token(cls, data: Dict[str, Any]) -> str:
        """Create a new access token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({
            "exp": expire,
            "type": "access",
            "iat": datetime.utcnow()
        })
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    @classmethod
    def create_refresh_token(cls, data: Dict[str, Any]) -> str:
        """Create a new refresh token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({
            "exp": expire,
            "type": "refresh",
            "iat": datetime.utcnow()
        })
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    @classmethod
    def verify_token(cls, token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    @classmethod
    def create_user_tokens(cls, user: User) -> Dict[str, str]:
        """Create both access and refresh tokens for a user."""
        user_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role.value,
            "account_type": user.account_type.value
        }
        
        access_token = cls.create_access_token(user_data)
        refresh_token = cls.create_refresh_token(user_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    
    @classmethod
    def refresh_access_token(cls, refresh_token: str) -> str:
        """Create a new access token using a valid refresh token."""
        try:
            payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type"
                )
            
            # Create new access token
            user_data = {
                "sub": payload.get("sub"),
                "email": payload.get("email"),
                "role": payload.get("role"),
                "account_type": payload.get("account_type")
            }
            
            return cls.create_access_token(user_data)
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )


class JWTAuthDependency:
    """Dependency for JWT authentication in FastAPI routes."""
    
    @staticmethod
    async def get_current_user(credentials: HTTPAuthorizationCredentials = security) -> User:
        """Get current authenticated user from JWT token."""
        token = credentials.credentials
        payload = JWTHandler.verify_token(token)
        
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # TODO: Get user from database
        # For now, return a mock user
        from app.models.user import UserRole, AccountType, UserStatus
        user = User(
            id=user_id,
            first_name="Mock",
            last_name="User",
            email=payload.get("email", "mock@example.com"),
            role=UserRole(payload.get("role", "normal")),
            account_type=AccountType(payload.get("account_type", "consumer")),
            status=UserStatus.ACTIVE
        )
        
        return user
    
    @staticmethod
    async def get_current_active_user(current_user: User = security) -> User:
        """Get current authenticated and active user."""
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return current_user
    
    @staticmethod
    async def require_role(required_role: str, current_user: User = security) -> User:
        """Require a specific role for access."""
        if current_user.role.value != required_role and current_user.role.value != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {required_role} required"
            )
        return current_user
