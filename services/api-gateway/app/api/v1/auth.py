"""
Authentication API endpoints for OpenPolicy V2

Provides endpoints for user authentication, registration, and password reset.
This implements the password reset functionality required by checklist items 30.1-30.6.
"""

import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_
from pydantic import BaseModel, EmailStr, Field
from app.database import get_db
from app.models.users import User, PasswordResetToken
from app.core.middleware import RateLimitMiddleware
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()

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


def generate_reset_token() -> str:
    """Generate a secure password reset token."""
    # Generate a random token using secrets module for cryptographic security
    token = secrets.token_urlsafe(32)
    return token


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 (simplified for demo - use bcrypt in production)."""
    return hashlib.sha256(password.encode()).hexdigest()


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
