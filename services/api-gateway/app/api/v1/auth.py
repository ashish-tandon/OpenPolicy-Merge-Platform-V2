"""
Authentication API endpoints for OpenPolicy V2

Provides endpoints for user authentication, registration, and password reset.
This implements the complete authentication system required by checklist items 5.7, 10.1.
"""

import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_
from pydantic import BaseModel, EmailStr, Field
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.database import get_db
from app.models.users import User, PasswordResetToken, UserSession, OAuthAccount
from app.config import settings
import logging
import requests
from urllib.parse import urlencode

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()

# JWT Configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# Password reset configuration
PASSWORD_RESET_TOKEN_EXPIRE_HOURS = 1  # 1 hour
PASSWORD_RESET_RATE_LIMIT = 3  # Max 3 requests per hour per IP


class PasswordResetRequest(BaseModel):
    """Request model for password reset."""
    email: EmailStr = Field(..., description="Email address of the user")


class PasswordResetConfirm(BaseModel):
    """Request model for password reset confirmation."""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password (minimum 8 characters)")


class PasswordResetResponse(BaseModel):
    """Response model for password reset request."""
    message: str = Field(..., description="Success message")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class PasswordResetConfirmResponse(BaseModel):
    """Response model for password reset confirmation."""
    message: str = Field(..., description="Success message")


class UserLogin(BaseModel):
    """Request model for user login."""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="User password")


class UserRegister(BaseModel):
    """Request model for user registration."""
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    email: EmailStr = Field(..., description="Email address")
    full_name: str = Field(..., min_length=2, max_length=255, description="Full name")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")


class Token(BaseModel):
    """Response model for authentication token."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type (bearer)")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: dict = Field(..., description="User information")


class UserProfile(BaseModel):
    """Response model for user profile."""
    id: str = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    full_name: str = Field(..., description="Full name")
    is_active: bool = Field(..., description="Account active status")
    is_verified: bool = Field(..., description="Email verification status")
    created_at: str = Field(..., description="Account creation date")


class GoogleOAuthRequest(BaseModel):
    """Request model for Google OAuth login."""
    code: str = Field(..., description="Authorization code from Google")


class GoogleOAuthResponse(BaseModel):
    """Response model for Google OAuth login."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type (bearer)")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: dict = Field(..., description="User information")
    oauth_provider: str = Field(..., description="OAuth provider (google)")
    message: str = Field(..., description="Success message")


def generate_reset_token() -> str:
    """Generate a secure password reset token."""
    # Generate a random token using secrets module for cryptographic security
    token = secrets.token_urlsafe(32)
    return token


def hash_password(password: str) -> str:
    """Hash a password using bcrypt for security."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme), db: DBSession = Depends(get_db)) -> User:
    """Get the current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user


def send_password_reset_email(email: str, token: str, user_name: str):
    """
    Send password reset email to user.
    
    This is a placeholder implementation - in production would use
    email service like SendGrid, AWS SES, or SMTP server.
    """
    reset_url = f"https://openpolicy.ca/reset-password?token={token}"
    
    # Email template (Item 30.3)
    email_template = f"""
    Subject: Reset Your OpenPolicy Account Password
    
    Hello {user_name},
    
    We received a request to reset your password for your OpenPolicy account.
    
    To reset your password, click the link below:
    {reset_url}
    
    This link will expire in {PASSWORD_RESET_TOKEN_EXPIRE_HOURS} hour(s).
    
    If you didn't request this password reset, please ignore this email.
    Your password will remain unchanged.
    
    For security reasons, this link can only be used once.
    
    Best regards,
    The OpenPolicy Team
    
    ---
    This is an automated message. Please do not reply to this email.
    For support, contact us at support@openpolicy.ca
    """
    
    # In production, this would send the actual email
    logger.info(f"Password reset email would be sent to {email}")
    logger.info(f"Reset URL: {reset_url}")
    logger.info(f"Email content: {email_template}")


def check_rate_limit(request: Request, db: DBSession) -> bool:
    """
    Check rate limiting for password reset requests.
    
    Implements Item 30.6: Add rate limiting to password reset.
    """
    client_ip = request.client.host if request.client else "unknown"
    
    # Check how many reset requests from this IP in the last hour
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    
    recent_requests = db.query(PasswordResetToken).filter(
        and_(
            PasswordResetToken.ip_address == client_ip,
            PasswordResetToken.created_at >= one_hour_ago
        )
    ).count()
    
    if recent_requests >= PASSWORD_RESET_RATE_LIMIT:
        logger.warning(f"Rate limit exceeded for IP {client_ip}: {recent_requests} requests in last hour")
        return False
    
    return True


@router.post("/register", response_model=UserProfile)
async def register_user(
    user_data: UserRegister,
    db: DBSession = Depends(get_db)
):
    """
    Register a new user account.
    
    Implements checklist item 5.7: User registration endpoint
    """
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        is_active=True,
        is_verified=False  # Email verification would be implemented separately
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"New user registered: {new_user.username}")
    
    return UserProfile(
        id=str(new_user.id),
        username=new_user.username,
        email=new_user.email,
        full_name=new_user.full_name,
        is_active=new_user.is_active,
        is_verified=new_user.is_verified,
        created_at=new_user.created_at.isoformat() if new_user.created_at else None
    )


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: DBSession = Depends(get_db)
):
    """
    Authenticate user and return access token.
    
    Implements checklist item 5.7: User login endpoint
    Implements checklist item 10.1: JWT authentication
    """
    # Try to find user by username or email
    user = db.query(User).filter(
        (User.username == form_data.username) | (User.email == form_data.username)
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Create user session
    session = UserSession(
        user_id=user.id,
        session_token=access_token,
        expires_at=datetime.utcnow() + access_token_expires,
        ip_address=None,  # Could be extracted from request
        user_agent=None   # Could be extracted from request
    )
    db.add(session)
    db.commit()
    
    logger.info(f"User logged in: {user.username}")
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user.to_dict()
    )


@router.get("/me", response_model=UserProfile)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user profile.
    
    Implements checklist item 5.7: User profile endpoint
    """
    return UserProfile(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at.isoformat() if current_user.created_at else None
    )


@router.post("/logout")
async def logout_user(current_user: User = Depends(get_current_user), db: DBSession = Depends(get_db)):
    """
    Logout user and invalidate session.
    
    Implements checklist item 5.7: User logout endpoint
    """
    # Remove user session
    db.query(UserSession).filter(UserSession.user_id == current_user.id).delete()
    db.commit()
    
    logger.info(f"User logged out: {current_user.username}")
    
    return {"message": "Successfully logged out"}


@router.post("/reset-password", response_model=PasswordResetResponse)
async def request_password_reset(
    request: Request,
    reset_request: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: DBSession = Depends(get_db)
):
    """
    Request password reset for a user account.
    
    Implements checklist item 30.1: Create password reset endpoint /api/v1/auth/reset-password
    Implements checklist item 30.2: Implement password reset token generation
    Implements checklist item 30.6: Add rate limiting to password reset
    """
    
    # Check rate limiting
    if not check_rate_limit(request, db):
        raise HTTPException(
            status_code=429,
            detail=f"Too many password reset requests. Maximum {PASSWORD_RESET_RATE_LIMIT} requests per hour allowed."
        )
    
    # Find user by email
    user = db.query(User).filter(User.email == reset_request.email).first()
    
    if not user:
        # For security, always return success even if user doesn't exist
        # This prevents email enumeration attacks
        logger.info(f"Password reset requested for non-existent email: {reset_request.email}")
        return PasswordResetResponse(
            message="If an account with that email exists, a password reset link has been sent.",
            expires_in=PASSWORD_RESET_TOKEN_EXPIRE_HOURS * 3600
        )
    
    if not user.is_active:
        # Don't allow password reset for inactive accounts
        logger.warning(f"Password reset requested for inactive user: {user.email}")
        return PasswordResetResponse(
            message="If an account with that email exists, a password reset link has been sent.",
            expires_in=PASSWORD_RESET_TOKEN_EXPIRE_HOURS * 3600
        )
    
    # Generate reset token
    token = generate_reset_token()
    expires_at = datetime.now(timezone.utc) + timedelta(hours=PASSWORD_RESET_TOKEN_EXPIRE_HOURS)
    
    # Invalidate any existing reset tokens for this user
    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id
    ).delete()
    
    # Create new reset token
    reset_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=expires_at,
        ip_address=request.client.host if request.client else None
    )
    
    db.add(reset_token)
    db.commit()
    
    # Send email in background (Item 30.3: Create password reset email template)
    background_tasks.add_task(
        send_password_reset_email,
        user.email,
        token,
        user.full_name
    )
    
    logger.info(f"Password reset token generated for user {user.email}")
    
    return PasswordResetResponse(
        message="If an account with that email exists, a password reset link has been sent.",
        expires_in=PASSWORD_RESET_TOKEN_EXPIRE_HOURS * 3600
    )


@router.post("/confirm-reset-password", response_model=PasswordResetConfirmResponse)
async def confirm_password_reset(
    request: Request,
    reset_confirm: PasswordResetConfirm,
    db: DBSession = Depends(get_db)
):
    """
    Confirm password reset and update user password.
    
    This endpoint completes the password reset flow by validating the token
    and updating the user's password.
    """
    
    # Find the reset token
    reset_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == reset_confirm.token
    ).first()
    
    if not reset_token:
        logger.warning(f"Invalid reset token used: {reset_confirm.token[:8]}...")
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token."
        )
    
    # Check if token is valid
    if not reset_token.is_valid():
        logger.warning(f"Expired or used reset token: {reset_confirm.token[:8]}...")
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token."
        )
    
    # Get the user
    user = db.query(User).filter(User.id == reset_token.user_id).first()
    
    if not user or not user.is_active:
        logger.error(f"Reset token belongs to non-existent or inactive user: {reset_token.user_id}")
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token."
        )
    
    # Update user password
    user.hashed_password = hash_password(reset_confirm.new_password)
    user.updated_at = datetime.now(timezone.utc)
    
    # Mark token as used
    reset_token.used_at = datetime.now(timezone.utc)
    
    # Invalidate all user sessions for security
    # Note: This would require session management implementation
    
    db.commit()
    
    logger.info(f"Password successfully reset for user {user.email}")
    
    return PasswordResetConfirmResponse(
        message="Password has been successfully reset. You can now log in with your new password."
    )


@router.get("/reset-password/validate/{token}")
async def validate_reset_token(
    token: str,
    db: DBSession = Depends(get_db)
):
    """
    Validate a password reset token without consuming it.
    
    This endpoint can be used by the frontend to check if a reset token
    is valid before showing the password reset form.
    """
    
    reset_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token
    ).first()
    
    if not reset_token or not reset_token.is_valid():
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token."
        )
    
    # Get user info (without sensitive data)
    user = db.query(User).filter(User.id == reset_token.user_id).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token."
        )
    
    return {
        "valid": True,
        "email": user.email,
        "expires_at": reset_token.expires_at.isoformat(),
        "time_remaining": int((reset_token.expires_at - datetime.now(timezone.utc)).total_seconds())
    }


@router.get("/google/authorize")
async def google_oauth_authorize():
    """
    Redirect user to Google OAuth authorization page.
    
    Implements BUG-002: OAuth Integration (Google OAuth backend)
    """
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Google OAuth not configured"
        )
    
    # Build Google OAuth authorization URL
    params = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'consent'
    }
    
    auth_url = f"{settings.GOOGLE_AUTHORIZATION_URL}?{urlencode(params)}"
    
    return {"authorization_url": auth_url}


@router.post("/google/callback", response_model=GoogleOAuthResponse)
async def google_oauth_callback(
    oauth_data: GoogleOAuthRequest,
    db: DBSession = Depends(get_db)
):
    """
    Handle Google OAuth callback and authenticate user.
    
    Implements BUG-002: OAuth Integration (Google OAuth backend)
    """
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Google OAuth not configured"
        )
    
    try:
        # Exchange authorization code for access token
        token_data = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'code': oauth_data.code,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.GOOGLE_REDIRECT_URI
        }
        
        token_response = requests.post(settings.GOOGLE_TOKEN_URL, data=token_data)
        token_response.raise_for_status()
        token_info = token_response.json()
        
        access_token = token_info.get('access_token')
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to obtain access token from Google"
            )
        
        # Get user information from Google
        headers = {'Authorization': f'Bearer {access_token}'}
        userinfo_response = requests.get(settings.GOOGLE_USERINFO_URL, headers=headers)
        userinfo_response.raise_for_status()
        user_info = userinfo_response.json()
        
        # Extract user details
        google_user_id = user_info.get('id')
        email = user_info.get('email')
        given_name = user_info.get('given_name', '')
        family_name = user_info.get('family_name', '')
        full_name = user_info.get('name', f"{given_name} {family_name}".strip())
        picture = user_info.get('picture')
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not provided by Google"
            )
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        
        if existing_user:
            user = existing_user
            # Check if OAuth account exists
            oauth_account = db.query(OAuthAccount).filter(
                OAuthAccount.user_id == user.id,
                OAuthAccount.provider == 'google'
            ).first()
            
            if not oauth_account:
                # Create OAuth account for existing user
                oauth_account = OAuthAccount(
                    user_id=user.id,
                    provider='google',
                    provider_account_id=google_user_id,
                    access_token=access_token,
                    scope='openid email profile'
                )
                db.add(oauth_account)
        else:
            # Create new user
            username = f"google_{google_user_id[:8]}"
            # Ensure username is unique
            counter = 1
            original_username = username
            while db.query(User).filter(User.username == username).first():
                username = f"{original_username}_{counter}"
                counter += 1
            
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                hashed_password="",  # OAuth users don't have passwords
                is_active=True,
                is_verified=True  # Google accounts are pre-verified
            )
            db.add(user)
            db.flush()  # Get the user ID
            
            # Create OAuth account
            oauth_account = OAuthAccount(
                user_id=user.id,
                provider='google',
                provider_account_id=google_user_id,
                access_token=access_token,
                scope='openid email profile'
            )
            db.add(oauth_account)
        
        # Commit all changes
        db.commit()
        
        # Generate JWT token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        jwt_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )
        
        # Create user session
        session = UserSession(
            user_id=user.id,
            session_token=jwt_token,
            expires_at=datetime.now(timezone.utc) + access_token_expires
        )
        db.add(session)
        db.commit()
        
        return GoogleOAuthResponse(
            access_token=jwt_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=user.to_dict(),
            oauth_provider="google",
            message="Successfully authenticated with Google"
        )
        
    except requests.RequestException as e:
        logger.error(f"Google OAuth request failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to communicate with Google OAuth service"
        )
    except Exception as e:
        logger.error(f"Google OAuth authentication failed: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during Google OAuth authentication"
        )
