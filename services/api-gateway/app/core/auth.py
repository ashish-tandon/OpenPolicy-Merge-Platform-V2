"""
Core Authentication Service

Handles JWT tokens, password hashing, and authentication logic.
Implements FEAT-014 Authentication System (P0 priority).
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
from uuid import UUID
import secrets
import hashlib
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.config import settings
from app.models.users import User
from app.models.auth import Role, Permission, APIKey
from app.schemas.auth import TokenPayload, UserCreate, UserResponse
from app.core.exceptions import AuthenticationError, AuthorizationError
import logging

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS


class AuthService:
    """Core authentication service."""
    
    def __init__(self, db: Session):
        self.db = db
    
    # Password management
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    # JWT token management
    @staticmethod
    def create_access_token(
        subject: str, 
        roles: List[str] = None, 
        permissions: List[str] = None,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT access token."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode = {
            "sub": subject,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access",
            "roles": roles or [],
            "permissions": permissions or []
        }
        
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(subject: str) -> str:
        """Create a JWT refresh token."""
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode = {
            "sub": subject,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> TokenPayload:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
            return TokenPayload(**payload)
        except JWTError as e:
            raise AuthenticationError(f"Invalid token: {str(e)}")
    
    # User authentication
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user by username/email and password."""
        # Check if username is email or username
        user = self.db.query(User).filter(
            or_(User.email == username, User.username == username)
        ).first()
        
        if not user:
            return None
        
        if not self.verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            raise AuthenticationError("User account is disabled")
        
        # Update last login
        user.last_login = datetime.utcnow()
        self.db.commit()
        
        return user
    
    def get_user_permissions(self, user: User) -> List[str]:
        """Get all permissions for a user based on their roles."""
        permissions = set()
        
        for role in user.roles:
            if role.name == "superuser":
                # Superuser has all permissions
                all_perms = self.db.query(Permission).all()
                return [p.name for p in all_perms]
            
            for permission in role.permissions:
                permissions.add(permission.name)
        
        return list(permissions)
    
    def create_user_tokens(self, user: User) -> Tuple[str, str]:
        """Create access and refresh tokens for a user."""
        roles = [role.name for role in user.roles]
        permissions = self.get_user_permissions(user)
        
        access_token = self.create_access_token(
            subject=str(user.id),
            roles=roles,
            permissions=permissions
        )
        refresh_token = self.create_refresh_token(subject=str(user.id))
        
        return access_token, refresh_token
    
    # API key management
    @staticmethod
    def generate_api_key() -> Tuple[str, str, str]:
        """Generate a new API key.
        
        Returns:
            Tuple of (full_key, key_hash, prefix)
        """
        # Generate random key
        key_bytes = secrets.token_bytes(32)
        key_hex = key_bytes.hex()
        
        # Create prefix for identification
        prefix = f"op_{key_hex[:8]}"
        
        # Full key includes prefix
        full_key = f"{prefix}_{key_hex}"
        
        # Hash the full key for storage
        key_hash = hashlib.sha256(full_key.encode()).hexdigest()
        
        return full_key, key_hash, prefix
    
    def authenticate_api_key(self, api_key: str) -> Optional[APIKey]:
        """Authenticate using an API key."""
        # Hash the provided key
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Find the API key
        api_key_obj = self.db.query(APIKey).filter(
            APIKey.key_hash == key_hash
        ).first()
        
        if not api_key_obj:
            return None
        
        if not api_key_obj.is_active:
            raise AuthenticationError("API key is disabled")
        
        if api_key_obj.is_expired():
            raise AuthenticationError("API key has expired")
        
        # Update last used timestamp
        api_key_obj.last_used_at = datetime.utcnow()
        self.db.commit()
        
        return api_key_obj
    
    # Permission checking
    def check_permission(
        self, 
        user: User, 
        resource: str, 
        action: str
    ) -> bool:
        """Check if a user has permission to perform an action on a resource."""
        # Superuser has all permissions
        if any(role.name == "superuser" for role in user.roles):
            return True
        
        # Check each role
        for role in user.roles:
            if role.has_permission(resource, action):
                return True
        
        return False
    
    def require_permission(
        self, 
        user: User, 
        resource: str, 
        action: str
    ) -> None:
        """Require a user to have permission (raises exception if not)."""
        if not self.check_permission(user, resource, action):
            raise AuthorizationError(
                f"User lacks permission: {resource}.{action}"
            )
    
    # User registration
    def register_user(
        self, 
        user_data: UserCreate,
        initial_roles: List[str] = None
    ) -> User:
        """Register a new user."""
        # Check if user already exists
        existing_user = self.db.query(User).filter(
            or_(
                User.email == user_data.email,
                User.username == user_data.username
            )
        ).first()
        
        if existing_user:
            if existing_user.email == user_data.email:
                raise ValueError("Email already registered")
            else:
                raise ValueError("Username already taken")
        
        # Create user
        user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=self.hash_password(user_data.password),
            is_active=user_data.is_active,
            preferences=user_data.preferences or {}
        )
        
        # Assign default role if no roles specified
        if not initial_roles:
            initial_roles = ["user"]
        
        # Assign roles
        roles = self.db.query(Role).filter(Role.name.in_(initial_roles)).all()
        user.roles = roles
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        logger.info(f"New user registered: {user.email}")
        
        return user
    
    # Session management
    def get_current_user(self, token: str) -> User:
        """Get the current user from a token."""
        payload = self.decode_token(token)
        
        if payload.type != "access":
            raise AuthenticationError("Invalid token type")
        
        user = self.db.query(User).filter(User.id == payload.sub).first()
        
        if not user:
            raise AuthenticationError("User not found")
        
        if not user.is_active:
            raise AuthenticationError("User account is disabled")
        
        return user
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """Generate a new access token from a refresh token."""
        payload = self.decode_token(refresh_token)
        
        if payload.type != "refresh":
            raise AuthenticationError("Invalid token type")
        
        user = self.db.query(User).filter(User.id == payload.sub).first()
        
        if not user:
            raise AuthenticationError("User not found")
        
        if not user.is_active:
            raise AuthenticationError("User account is disabled")
        
        # Create new access token
        roles = [role.name for role in user.roles]
        permissions = self.get_user_permissions(user)
        
        return self.create_access_token(
            subject=str(user.id),
            roles=roles,
            permissions=permissions
        )


# Dependency injection helpers
def get_auth_service(db: Session) -> AuthService:
    """Get an auth service instance."""
    return AuthService(db)