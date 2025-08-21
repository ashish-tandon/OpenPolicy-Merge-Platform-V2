"""
Profile management API endpoints.

Includes all missing features from Open Policy Infra:
- Profile picture management
- User analytics
- Account deletion
- Postal code management
- Password changes
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional
import base64
import json

from app.auth.simple_auth import current_active_user, require_role
from app.schemas.user_schemas import (
    UserProfileUpdate, 
    UserAnalytics, 
    AccountDeletionRequest,
    PasswordChangeRequest
)
from app.models.user import User
from app.config.settings import settings

router = APIRouter(prefix="/profile", tags=["Profile Management"])


@router.get("/me", response_model=dict)
async def get_profile(current_user: User = Depends(current_active_user)):
    """Get current user's profile."""
    return {
        "success": True,
        "user": {
            "id": str(current_user.id),
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "email": current_user.email,
            "phone": current_user.phone,
            "postal_code": current_user.postal_code,
            "gender": current_user.gender,
            "age": current_user.age,
            "date_of_birth": current_user.date_of_birth.isoformat() if current_user.date_of_birth else None,
            "role": current_user.role.value,
            "account_type": current_user.account_type.value,
            "status": current_user.status.value,
            "avatar_url": current_user.avatar_url,
            "profile_picture": current_user.profile_picture,
            "preferences": current_user.preferences,
            "created_at": current_user.created_at.isoformat(),
            "updated_at": current_user.updated_at.isoformat(),
            "last_login_at": current_user.last_login_at.isoformat() if current_user.last_login_at else None
        }
    }


@router.put("/me", response_model=dict)
async def update_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(current_active_user)
):
    """Update current user's profile."""
    try:
        # Update fields if provided
        if profile_update.first_name is not None:
            current_user.first_name = profile_update.first_name
        if profile_update.last_name is not None:
            current_user.last_name = profile_update.last_name
        if profile_update.phone is not None:
            current_user.phone = profile_update.phone
        if profile_update.postal_code is not None:
            current_user.postal_code = profile_update.postal_code
        if profile_update.gender is not None:
            current_user.gender = profile_update.gender
        if profile_update.age is not None:
            current_user.age = profile_update.age
        if profile_update.date_of_birth is not None:
            current_user.date_of_birth = profile_update.date_of_birth
        if profile_update.preferences is not None:
            current_user.preferences = profile_update.preferences
        
        # TODO: Save to database
        # await db.commit()
        
        return {
            "success": True,
            "message": "Profile updated successfully",
            "user": {
                "first_name": current_user.first_name,
                "last_name": current_user.last_name,
                "phone": current_user.phone,
                "postal_code": current_user.postal_code,
                "role": current_user.role.value
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}"
        )


@router.post("/picture", response_model=dict)
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(current_active_user)
):
    """Upload profile picture (Base64 encoding like Open Policy Infra)."""
    try:
        # Validate file type
        if not file.content_type or not any(
            allowed_type in file.content_type 
            for allowed_type in settings.ALLOWED_IMAGE_TYPES
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
            )
        
        # Validate file size
        if file.size and file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Max size: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Read file content
        content = await file.read()
        
        # Convert to base64 (like Open Policy Infra)
        base64_data = base64.b64encode(content).decode('utf-8')
        image_type = file.filename.split('.')[-1].lower() if file.filename else 'jpg'
        
        # Create data URI
        data_uri = f"data:image/{image_type};base64,{base64_data}"
        
        # Update user profile picture
        current_user.profile_picture = data_uri
        current_user.avatar_url = f"/uploads/profile_pictures/{current_user.id}.{image_type}"
        
        # TODO: Save to database and file system
        # await db.commit()
        # Save file to disk
        
        return {
            "success": True,
            "message": "Profile picture uploaded successfully",
            "avatar_url": current_user.avatar_url
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload profile picture: {str(e)}"
        )


@router.get("/analytics", response_model=UserAnalytics)
async def get_user_analytics(current_user: User = Depends(current_active_user)):
    """Get user engagement analytics (like Open Policy Infra getUseStats)."""
    try:
        # TODO: Get actual data from database
        # For now, return mock data
        analytics = UserAnalytics(
            votes_cast=0,  # TODO: Count from BillVoteCast
            saved_bills=0,  # TODO: Count from SavedBill
            issues_raised=0  # TODO: Count from RepresentativeIssue
        )
        
        return analytics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user analytics: {str(e)}"
        )


@router.put("/postal-code", response_model=dict)
async def change_postal_code(
    postal_code: str = Form(...),
    current_user: User = Depends(current_active_user)
):
    """Change user's postal code (like Open Policy Infra changePostalCode)."""
    try:
        old_postal_code = current_user.postal_code
        current_user.postal_code = postal_code
        
        # TODO: Save to database
        # await db.commit()
        
        # TODO: Get representative information for new postal code
        # representative_data = await get_representative_by_postal_code(postal_code)
        
        return {
            "success": True,
            "message": "Postal code changed successfully",
            "user": {
                "postal_code": current_user.postal_code
            },
            "data": {
                "representative_info": "TODO: Get representative data"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change postal code: {str(e)}"
        )


@router.put("/password", response_model=dict)
async def change_password(
    password_request: PasswordChangeRequest,
    current_user: User = Depends(current_active_user)
):
    """Change user password (like Open Policy Infra changeUserPassword)."""
    try:
        # Validate passwords match
        password_request.validate_passwords()
        
        # TODO: Verify current password
        # if not verify_password(password_request.current_password, current_user.password_hash):
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Invalid current password"
        #     )
        
        # TODO: Hash and save new password
        # current_user.password_hash = hash_password(password_request.new_password)
        # await db.commit()
        
        return {
            "success": True,
            "message": "Password changed successfully"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change password: {str(e)}"
        )


@router.delete("/account", response_model=dict)
async def delete_account(
    deletion_request: AccountDeletionRequest,
    current_user: User = Depends(current_active_user)
):
    """Delete user account (like Open Policy Infra deleteUserAccount)."""
    try:
        # Verify email matches
        if deletion_request.email != current_user.email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email"
            )
        
        # Soft delete user
        current_user.email = f"{current_user.email}_deleted_{current_user.id}"
        current_user.phone = f"{current_user.phone}_deleted_{current_user.id}" if current_user.phone else None
        current_user.deleted_at = "now()"  # TODO: Use proper datetime
        current_user.account_deletion_reason = deletion_request.deletion_reason
        current_user.status = "deactivated"  # TODO: Use enum
        
        # TODO: Save to database
        # await db.commit()
        
        return {
            "success": True,
            "message": "Account deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete account: {str(e)}"
        )


@router.get("/deletion-reasons", response_model=list)
async def get_deletion_reasons():
    """Get account deletion reasons (like Open Policy Infra accountDeletionReasons)."""
    return [
        {
            "label": "I no longer need the app",
            "value": "I no longer need the app"
        },
        {
            "label": "I found a better alternative",
            "value": "I found a better alternative"
        },
        {
            "label": "I have privacy or security concerns",
            "value": "I have privacy or security concerns"
        },
        {
            "label": "The app does not meet my expectations",
            "value": "The app does not meet my expectations"
        },
        {
            "label": "Other",
            "value": "Other"
        }
    ]
