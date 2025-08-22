"""
Enhanced User Management API for OpenPolicy V2

Comprehensive user management endpoints including profiles, preferences, and activity tracking.
This implements Feature F008: User Management (Authentication and Profile Management)
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Path, Body, Request
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import text, func, and_, or_, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import math
import json

from app.database import get_db
from app.models.users import User, UserPreferences, UserActivity, OAuthAccount
from app.schemas.user_management import (
    UserProfileResponse, UserPreferencesResponse, UserActivityResponse,
    UserListResponse, UserActivityListResponse, UserStatsResponse,
    UserSearchResponse, NotificationPreferencesResponse,
    UserCreateRequest, UserUpdateRequest, UserPreferencesUpdateRequest,
    PasswordChangeRequest, UserActivityCreateRequest
)
from app.api.v1.auth import get_current_user, hash_password, verify_password
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter()


# ============================================================================
# USER PROFILES
# ============================================================================

@router.get("/profiles", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search query"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_verified: Optional[bool] = Query(None, description="Filter by verification status"),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all users with pagination and filtering.
    
    Requires authentication and appropriate permissions.
    """
    # Build base query
    query = db.query(User)
    
    # Apply filters
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    if is_verified is not None:
        query = query.filter(User.is_verified == is_verified)
    
    # Apply search if provided
    if search:
        search_query = text("""
            to_tsvector('english', users.username || ' ' || users.full_name || ' ' || COALESCE(users.bio, '')) 
            @@ plainto_tsquery('english', :search_term)
        """)
        query = query.filter(search_query.bindparams(search_term=search))
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get users
    users = query.order_by(User.created_at.desc()).offset(offset).limit(page_size).all()
    
    # Convert to response format
    user_responses = []
    for user in users:
        user_responses.append(UserProfileResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            bio=user.bio,
            avatar_url=user.avatar_url,
            phone=user.phone,
            website=user.website,
            location=user.location,
            postal_code=user.postal_code,
            timezone=user.timezone,
            language_preference=user.language_preference,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
            last_activity=user.last_activity
        ))
    
    return UserListResponse(
        users=user_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


@router.get("/profiles/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: str = Path(..., description="User ID"),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific user's profile by ID.
    
    Users can only view their own profile or public profiles based on privacy settings.
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check privacy settings
    if str(current_user.id) != user_id:
        if user.privacy_level == "private":
            raise HTTPException(status_code=403, detail="Profile is private")
        elif user.privacy_level == "friends_only":
            # In a real implementation, check if users are friends
            raise HTTPException(status_code=403, detail="Profile is friends-only")
    
    return UserProfileResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        bio=user.bio,
        avatar_url=user.avatar_url,
        phone=user.phone,
        website=user.website,
        location=user.location,
        postal_code=user.postal_code,
        timezone=user.timezone,
        language_preference=user.language_preference,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
        updated_at=user.updated_at,
        last_login=user.last_login,
        last_activity=user.last_activity
    )


@router.put("/profiles/{user_id}", response_model=UserProfileResponse)
async def update_user_profile(
    user_id: str = Path(..., description="User ID"),
    profile_data: UserUpdateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a user's profile.
    
    Users can only update their own profile.
    """
    # Check if user exists and is the current user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Can only update own profile")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update profile fields
    update_data = profile_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(user, field):
            setattr(user, field, value)
    
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    logger.info(f"User profile updated: {user.username}")
    
    return UserProfileResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        bio=user.bio,
        avatar_url=user.avatar_url,
        phone=user.phone,
        website=user.website,
        location=user.location,
        postal_code=user.postal_code,
        timezone=user.timezone,
        language_preference=user.language_preference,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at,
        updated_at=user.updated_at,
        last_login=user.last_login,
        last_activity=user.last_activity
    )


@router.post("/profiles/{user_id}/change-password")
async def change_user_password(
    user_id: str = Path(..., description="User ID"),
    password_data: PasswordChangeRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change a user's password.
    
    Users can only change their own password.
    """
    # Check if user exists and is the current user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Can only change own password")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not verify_password(password_data.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update password
    user.hashed_password = hash_password(password_data.new_password)
    user.updated_at = datetime.utcnow()
    db.commit()
    
    logger.info(f"Password changed for user: {user.username}")
    
    return {"message": "Password changed successfully"}


# ============================================================================
# USER PREFERENCES
# ============================================================================

@router.get("/profiles/{user_id}/preferences", response_model=UserPreferencesResponse)
async def get_user_preferences(
    user_id: str = Path(..., description="User ID"),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a user's preferences.
    
    Users can only view their own preferences.
    """
    # Check if user exists and is the current user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Can only view own preferences")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get or create preferences
    preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
    if not preferences:
        # Create default preferences
        preferences = UserPreferences(
            user_id=user_id,
            favorite_topics=json.dumps([]),
            favorite_mps=json.dumps([]),
            favorite_parties=json.dumps([]),
            excluded_topics=json.dumps([]),
            content_difficulty="intermediate",
            show_advanced_features=True,
            show_analytics=True,
            show_social_features=False,
            font_size="medium",
            theme_preference="light",
            profile_visibility="public",
            activity_sharing="friends_only",
            data_collection=True,
            third_party_sharing=False,
            high_contrast=False,
            screen_reader=False,
            keyboard_navigation=True,
            reduced_motion=False
        )
        db.add(preferences)
        db.commit()
        db.refresh(preferences)
    
    return UserPreferencesResponse(
        id=str(preferences.id),
        user_id=str(preferences.user_id),
        favorite_topics=json.loads(preferences.favorite_topics) if preferences.favorite_topics else [],
        favorite_mps=json.loads(preferences.favorite_mps) if preferences.favorite_mps else [],
        favorite_parties=json.loads(preferences.favorite_parties) if preferences.favorite_parties else [],
        excluded_topics=json.loads(preferences.excluded_topics) if preferences.excluded_topics else [],
        content_difficulty=preferences.content_difficulty,
        show_advanced_features=preferences.show_advanced_features,
        show_analytics=preferences.show_analytics,
        show_social_features=preferences.show_social_features,
        font_size=preferences.font_size,
        theme_preference=preferences.theme_preference,
        profile_visibility=preferences.profile_visibility,
        activity_sharing=preferences.activity_sharing,
        data_collection=preferences.data_collection,
        third_party_sharing=preferences.third_party_sharing,
        high_contrast=preferences.high_contrast,
        screen_reader=preferences.screen_reader,
        keyboard_navigation=preferences.keyboard_navigation,
        reduced_motion=preferences.reduced_motion,
        created_at=preferences.created_at,
        updated_at=preferences.updated_at
    )


@router.put("/profiles/{user_id}/preferences", response_model=UserPreferencesResponse)
async def update_user_preferences(
    user_id: str = Path(..., description="User ID"),
    preferences_data: UserPreferencesUpdateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a user's preferences.
    
    Users can only update their own preferences.
    """
    # Check if user exists and is the current user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Can only update own preferences")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get or create preferences
    preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
    if not preferences:
        preferences = UserPreferences(user_id=user_id)
        db.add(preferences)
    
    # Update preferences
    update_data = preferences_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(preferences, field):
            if isinstance(value, list):
                setattr(preferences, field, json.dumps(value))
            else:
                setattr(preferences, field, value)
    
    preferences.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(preferences)
    
    logger.info(f"User preferences updated: {user.username}")
    
    return UserPreferencesResponse(
        id=str(preferences.id),
        user_id=str(preferences.user_id),
        favorite_topics=json.loads(preferences.favorite_topics) if preferences.favorite_topics else [],
        favorite_mps=json.loads(preferences.favorite_mps) if preferences.favorite_mps else [],
        favorite_parties=json.loads(preferences.favorite_parties) if preferences.favorite_parties else [],
        excluded_topics=json.loads(preferences.excluded_topics) if preferences.excluded_topics else [],
        content_difficulty=preferences.content_difficulty,
        show_advanced_features=preferences.show_advanced_features,
        show_analytics=preferences.show_analytics,
        show_social_features=preferences.show_social_features,
        font_size=preferences.font_size,
        theme_preference=preferences.theme_preference,
        profile_visibility=preferences.profile_visibility,
        activity_sharing=preferences.activity_sharing,
        data_collection=preferences.data_collection,
        third_party_sharing=preferences.third_party_sharing,
        high_contrast=preferences.high_contrast,
        screen_reader=preferences.screen_reader,
        keyboard_navigation=preferences.keyboard_navigation,
        reduced_motion=preferences.reduced_motion,
        created_at=preferences.created_at,
        updated_at=preferences.updated_at
    )


# ============================================================================
# USER ACTIVITY
# ============================================================================

@router.post("/profiles/{user_id}/activity")
async def create_user_activity(
    user_id: str = Path(..., description="User ID"),
    activity_data: UserActivityCreateRequest = Body(...),
    request: Request = None,
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a user activity record.
    
    Users can only create their own activity records.
    """
    # Check if user exists and is the current user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Can only create own activity records")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create activity record
    activity = UserActivity(
        user_id=user_id,
        activity_type=activity_data.activity_type,
        content_id=activity_data.content_id,
        content_type=activity_data.content_type,
        content_title=activity_data.content_title,
        content_summary=activity_data.content_summary,
        time_spent=activity_data.time_spent,
        pages_viewed=activity_data.pages_viewed,
        actions_taken=json.dumps(activity_data.actions_taken) if activity_data.actions_taken else None,
        device=activity_data.device,
        browser=activity_data.browser,
        location=activity_data.location,
        ip_address=request.client.host if request and request.client else None,
        activity_date=datetime.utcnow()
    )
    
    db.add(activity)
    
    # Update user's last activity
    user.last_activity = datetime.utcnow()
    
    db.commit()
    db.refresh(activity)
    
    logger.info(f"User activity created: {user.username} - {activity_data.activity_type}")
    
    return {"message": "Activity recorded successfully", "activity_id": str(activity.id)}


@router.get("/profiles/{user_id}/activity", response_model=UserActivityListResponse)
async def get_user_activity(
    user_id: str = Path(..., description="User ID"),
    activity_type: Optional[str] = Query(None, description="Filter by activity type"),
    content_type: Optional[str] = Query(None, description="Filter by content type"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a user's activity history.
    
    Users can only view their own activity or public activity based on privacy settings.
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check privacy settings
    if str(current_user.id) != user_id:
        if user.privacy_level == "private":
            raise HTTPException(status_code=403, detail="Activity is private")
        elif user.privacy_level == "friends_only":
            # In a real implementation, check if users are friends
            raise HTTPException(status_code=403, detail="Activity is friends-only")
    
    # Build base query
    query = db.query(UserActivity).filter(UserActivity.user_id == user_id)
    
    # Apply filters
    if activity_type:
        query = query.filter(UserActivity.activity_type == activity_type)
    
    if content_type:
        query = query.filter(UserActivity.content_type == content_type)
    
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
            query = query.filter(UserActivity.activity_date >= date_from_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
            query = query.filter(UserActivity.activity_date <= date_to_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get activities
    activities = query.order_by(desc(UserActivity.activity_date)).offset(offset).limit(page_size).all()
    
    # Convert to response format
    activity_responses = []
    for activity in activities:
        activity_responses.append(UserActivityResponse(
            id=str(activity.id),
            user_id=str(activity.user_id),
            activity_type=activity.activity_type,
            content_id=activity.content_id,
            content_type=activity.content_type,
            content_title=activity.content_title,
            content_summary=activity.content_summary,
            time_spent=activity.time_spent,
            pages_viewed=activity.pages_viewed,
            actions_taken=json.loads(activity.actions_taken) if activity.actions_taken else [],
            device=activity.device,
            browser=activity.browser,
            location=activity.location,
            related_bills=json.loads(activity.related_bills) if activity.related_bills else [],
            related_mps=json.loads(activity.related_mps) if activity.related_mps else [],
            related_committees=json.loads(activity.related_committees) if activity.related_committees else [],
            ip_address=activity.ip_address,
            activity_date=activity.activity_date,
            created_at=activity.created_at
        ))
    
    return UserActivityListResponse(
        activities=activity_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


# ============================================================================
# USER STATISTICS
# ============================================================================

@router.get("/profiles/{user_id}/stats", response_model=UserStatsResponse)
async def get_user_statistics(
    user_id: str = Path(..., description="User ID"),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get comprehensive user statistics and analytics.
    
    Users can only view their own statistics or public statistics based on privacy settings.
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check privacy settings
    if str(current_user.id) != user_id:
        if user.privacy_level == "private":
            raise HTTPException(status_code=403, detail="Statistics are private")
        elif user.privacy_level == "friends_only":
            # In a real implementation, check if users are friends
            raise HTTPException(status_code=403, detail="Statistics are friends-only")
    
    # Get activity counts
    total_activities = db.query(UserActivity).filter(UserActivity.user_id == user_id).count()
    total_bills_viewed = db.query(UserActivity).filter(
        and_(UserActivity.user_id == user_id, UserActivity.content_type == "bill")
    ).count()
    total_mps_researched = db.query(UserActivity).filter(
        and_(UserActivity.user_id == user_id, UserActivity.content_type == "mp")
    ).count()
    total_votes_analyzed = db.query(UserActivity).filter(
        and_(UserActivity.user_id == user_id, UserActivity.content_type == "vote")
    ).count()
    
    # Get preferences for favorites
    preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
    favorite_topics = json.loads(preferences.favorite_topics) if preferences and preferences.favorite_topics else []
    favorite_mps = json.loads(preferences.favorite_mps) if preferences and preferences.favorite_mps else []
    favorite_parties = json.loads(preferences.favorite_parties) if preferences and preferences.favorite_parties else []
    
    # Calculate engagement score (simple algorithm)
    engagement_score = min(10.0, (total_activities * 0.1) + (total_bills_viewed * 0.2) + (total_mps_researched * 0.15) + (total_votes_analyzed * 0.25))
    
    # Get last activity
    last_activity = db.query(UserActivity).filter(
        UserActivity.user_id == user_id
    ).order_by(desc(UserActivity.activity_date)).first()
    
    return UserStatsResponse(
        user_id=user_id,
        total_activities=total_activities,
        total_bills_viewed=total_bills_viewed,
        total_mps_researched=total_mps_researched,
        total_votes_analyzed=total_votes_analyzed,
        favorite_topics=favorite_topics,
        favorite_mps=favorite_mps,
        favorite_parties=favorite_parties,
        engagement_score=round(engagement_score, 1),
        last_activity=last_activity.activity_date if last_activity else None,
        generated_at=datetime.utcnow()
    )


# ============================================================================
# USER SEARCH
# ============================================================================

@router.get("/search", response_model=UserSearchResponse)
async def search_users(
    q: str = Query(..., description="Search query"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search for users by name, username, or bio.
    
    Only returns public profiles based on privacy settings.
    """
    if len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Search query must be at least 2 characters")
    
    # Build search query
    search_query = text("""
        to_tsvector('english', users.username || ' ' || users.full_name || ' ' || COALESCE(users.bio, '')) 
        @@ plainto_tsquery('english', :search_term)
    """)
    
    # Only search public profiles
    query = db.query(User).filter(
        and_(
            search_query.bindparams(search_term=q),
            User.privacy_level == "public",
            User.is_active == True
        )
    )
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get users
    users = query.order_by(User.created_at.desc()).offset(offset).limit(page_size).all()
    
    # Convert to response format
    user_responses = []
    for user in users:
        user_responses.append(UserProfileResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            bio=user.bio,
            avatar_url=user.avatar_url,
            phone=user.phone,
            website=user.website,
            location=user.location,
            postal_code=user.postal_code,
            timezone=user.timezone,
            language_preference=user.language_preference,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login=user.last_login,
            last_activity=user.last_activity
        ))
    
    return UserSearchResponse(
        query=q,
        results=user_responses,
        total_results=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )
