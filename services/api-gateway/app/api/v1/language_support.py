"""
Language Support API for OpenPolicy V2

Comprehensive bilingual language support system for legal compliance and accessibility.
Implements P1 priority feature for French/English language toggle and content localization.
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Path, Body, Request
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_, or_, desc, func
from typing import Optional
from datetime import datetime
import math

from app.database import get_db
from app.models.language_support import (
    Language, Translation, UserLanguagePreference, LanguageAnalytics
)
from app.models.users import User
from app.schemas.language_support import (
    LanguageResponse, TranslationResponse, UserLanguagePreferenceResponse,
    LanguageListResponse, TranslationListResponse,
    UserLanguagePreferenceListResponse,
    LanguageCreateRequest, LanguageUpdateRequest, TranslationCreateRequest,
    UserLanguagePreferenceCreateRequest,
    UserLanguagePreferenceUpdateRequest,
    LanguageToggleRequest, TranslationSearchRequest,
    LanguageStatistics, LanguageCodeEnum
)
from app.api.v1.auth import get_current_user
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter()


# ============================================================================
# LANGUAGE MANAGEMENT
# ============================================================================

@router.post("/languages", response_model=LanguageResponse)
async def create_language(
    language_data: LanguageCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new supported language.
    
    This creates a new language configuration for the system.
    """
    # Check if language code already exists
    existing_language = db.query(Language).filter(
        Language.language_code == language_data.language_code
    ).first()
    
    if existing_language:
        raise HTTPException(
            status_code=400,
            detail=f"Language with code '{language_data.language_code}' already exists"
        )
    
    # If this is set as default, unset other defaults
    if language_data.is_default:
        db.query(Language).filter(Language.is_default == True).update({"is_default": False})
    
    # Create new language
    language = Language(**language_data.dict())
    db.add(language)
    db.commit()
    db.refresh(language)
    
    logger.info(f"Language created: {current_user.username} - {language_data.language_code}")
    
    return LanguageResponse(
        id=str(language.id),
        language_code=language.language_code,
        language_name=language.language_name,
        language_name_native=language.language_name_native,
        is_active=language.is_active,
        is_default=language.is_default,
        direction=language.direction,
        date_format=language.date_format,
        time_format=language.time_format,
        number_format=language.number_format,
        currency_code=language.currency_code,
        created_at=language.created_at,
        updated_at=language.updated_at
    )


@router.get("/languages", response_model=LanguageListResponse)
async def list_languages(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_default: Optional[bool] = Query(None, description="Filter by default status"),
    search: Optional[str] = Query(None, description="Search in language names"),
    db: DBSession = Depends(get_db)
):
    """
    List supported languages with filtering and pagination.
    """
    # Build base query
    query = db.query(Language)
    
    # Apply filters
    if is_active is not None:
        query = query.filter(Language.is_active == is_active)
    
    if is_default is not None:
        query = query.filter(Language.is_default == is_default)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Language.language_name.ilike(search_term),
                Language.language_name_native.ilike(search_term),
                Language.language_code.ilike(search_term)
            )
        )
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get languages
    languages = query.order_by(Language.language_code).offset(offset).limit(page_size).all()
    
    # Convert to response format
    language_responses = []
    for language in languages:
        language_responses.append(LanguageResponse(
            id=str(language.id),
            language_code=language.language_code,
            language_name=language.language_name,
            language_name_native=language.language_name_native,
            is_active=language.is_active,
            is_default=language.is_default,
            direction=language.direction,
            date_format=language.date_format,
            time_format=language.time_format,
            number_format=language.number_format,
            currency_code=language.currency_code,
            created_at=language.created_at,
            updated_at=language.updated_at
        ))
    
    return LanguageListResponse(
        languages=language_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


@router.get("/languages/{language_id}", response_model=LanguageResponse)
async def get_language(
    language_id: str = Path(..., description="Language ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific language by ID.
    """
    language = db.query(Language).filter(Language.id == language_id).first()
    
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    
    return LanguageResponse(
        id=str(language.id),
        language_code=language.language_code,
        language_name=language.language_name,
        language_name_native=language.language_name_native,
        is_active=language.is_active,
        is_default=language.is_default,
        direction=language.direction,
        date_format=language.date_format,
        time_format=language.time_format,
        number_format=language.number_format,
        currency_code=language.currency_code,
        created_at=language.created_at,
        updated_at=language.updated_at
    )


@router.put("/languages/{language_id}", response_model=LanguageResponse)
async def update_language(
    language_id: str = Path(..., description="Language ID"),
    language_data: LanguageUpdateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a language configuration.
    """
    language = db.query(Language).filter(Language.id == language_id).first()
    
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    
    # If setting as default, unset other defaults
    if language_data.is_default:
        db.query(Language).filter(Language.is_default == True).update({"is_default": False})
    
    # Update language fields
    update_data = language_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(language, field):
            setattr(language, field, value)
    
    language.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(language)
    
    logger.info(f"Language updated: {current_user.username} - {language.language_code}")
    
    return LanguageResponse(
        id=str(language.id),
        language_code=language.language_code,
        language_name=language.language_name,
        language_name_native=language.language_name_native,
        is_active=language.is_active,
        is_default=language.is_default,
        direction=language.direction,
        date_format=language.date_format,
        time_format=language.time_format,
        number_format=language.number_format,
        currency_code=language.currency_code,
        created_at=language.created_at,
        updated_at=language.updated_at
    )


# ============================================================================
# TRANSLATION MANAGEMENT
# ============================================================================

@router.post("/translations", response_model=TranslationResponse)
async def create_translation(
    translation_data: TranslationCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new translation.
    """
    # Verify language exists
    language = db.query(Language).filter(Language.id == translation_data.language_id).first()
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    
    # Check if translation key already exists for this language and version
    existing_translation = db.query(Translation).filter(
        and_(
            Translation.language_id == translation_data.language_id,
            Translation.translation_key == translation_data.translation_key,
            Translation.version == translation_data.version
        )
    ).first()
    
    if existing_translation:
        raise HTTPException(
            status_code=400,
            detail=f"Translation with key '{translation_data.translation_key}' already exists for this language and version"
        )
    
    # Create new translation
    translation = Translation(**translation_data.dict())
    db.add(translation)
    db.commit()
    db.refresh(translation)
    
    logger.info(f"Translation created: {current_user.username} - {translation_data.translation_key}")
    
    return TranslationResponse(
        id=str(translation.id),
        language_id=str(translation.language_id),
        translation_key=translation.translation_key,
        translation_value=translation.translation_value,
        translation_context=translation.translation_context,
        translation_notes=translation.translation_notes,
        is_approved=translation.is_approved,
        approved_by=translation.approved_by,
        approved_at=translation.approved_at,
        version=translation.version,
        created_at=translation.created_at,
        updated_at=translation.updated_at
    )


@router.get("/translations", response_model=TranslationListResponse)
async def list_translations(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    language_id: Optional[str] = Query(None, description="Filter by language ID"),
    translation_key: Optional[str] = Query(None, description="Filter by translation key"),
    context: Optional[str] = Query(None, description="Filter by context"),
    is_approved: Optional[bool] = Query(None, description="Filter by approval status"),
    search: Optional[str] = Query(None, description="Search in translation values"),
    db: DBSession = Depends(get_db)
):
    """
    List translations with filtering and pagination.
    """
    # Build base query
    query = db.query(Translation)
    
    # Apply filters
    if language_id:
        query = query.filter(Translation.language_id == language_id)
    
    if translation_key:
        query = query.filter(Translation.translation_key == translation_key)
    
    if context:
        query = query.filter(Translation.translation_context == context)
    
    if is_approved is not None:
        query = query.filter(Translation.is_approved == is_approved)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Translation.translation_value.ilike(search_term),
                Translation.translation_key.ilike(search_term),
                Translation.translation_context.ilike(search_term)
            )
        )
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get translations
    translations = query.order_by(Translation.translation_key).offset(offset).limit(page_size).all()
    
    # Convert to response format
    translation_responses = []
    for translation in translations:
        translation_responses.append(TranslationResponse(
            id=str(translation.id),
            language_id=str(translation.language_id),
            translation_key=translation.translation_key,
            translation_value=translation.translation_value,
            translation_context=translation.translation_context,
            translation_notes=translation.translation_notes,
            is_approved=translation.is_approved,
            approved_by=translation.approved_by,
            approved_at=translation.approved_at,
            version=translation.version,
            created_at=translation.created_at,
            updated_at=translation.updated_at
        ))
    
    return TranslationListResponse(
        translations=translation_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


@router.get("/translations/{translation_id}", response_model=TranslationResponse)
async def get_translation(
    translation_id: str = Path(..., description="Translation ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific translation by ID.
    """
    translation = db.query(Translation).filter(Translation.id == translation_id).first()
    
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    
    return TranslationResponse(
        id=str(translation.id),
        language_id=str(translation.language_id),
        translation_key=translation.translation_key,
        translation_value=translation.translation_value,
        translation_context=translation.translation_context,
        translation_notes=translation.translation_notes,
        is_approved=translation.is_approved,
        approved_by=translation.approved_by,
        approved_at=translation.approved_at,
        version=translation.version,
        created_at=translation.created_at,
        updated_at=translation.updated_at
    )


# ============================================================================
# USER LANGUAGE PREFERENCES
# ============================================================================

@router.post("/users/preferences", response_model=UserLanguagePreferenceResponse)
async def create_user_language_preference(
    preference_data: UserLanguagePreferenceCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create or update user language preference.
    """
    # Verify language exists
    language = db.query(Language).filter(Language.id == preference_data.language_id).first()
    if not language:
        raise HTTPException(status_code=404, detail="Language not found")
    
    # Check if preference already exists
    existing_preference = db.query(UserLanguagePreference).filter(
        and_(
            UserLanguagePreference.user_id == current_user.id,
            UserLanguagePreference.language_id == preference_data.language_id
        )
    ).first()
    
    if existing_preference:
        # Update existing preference
        update_data = preference_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(existing_preference, field):
                setattr(existing_preference, field, value)
        
        existing_preference.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_preference)
        
        logger.info(f"User language preference updated: {current_user.username} - {language.language_code}")
        
        return UserLanguagePreferenceResponse(
            id=str(existing_preference.id),
            user_id=str(existing_preference.user_id),
            language_id=str(existing_preference.language_id),
            is_primary=existing_preference.is_primary,
            is_secondary=existing_preference.is_secondary,
            proficiency_level=existing_preference.proficiency_level,
            created_at=existing_preference.created_at,
            updated_at=existing_preference.updated_at
        )
    
    # Create new preference
    preference = UserLanguagePreference(**preference_data.dict())
    preference.user_id = current_user.id
    db.add(preference)
    db.commit()
    db.refresh(preference)
    
    logger.info(f"User language preference created: {current_user.username} - {language.language_code}")
    
    return UserLanguagePreferenceResponse(
        id=str(preference.id),
        user_id=str(preference.user_id),
        language_id=str(preference.language_id),
        is_primary=preference.is_primary,
        is_secondary=preference.is_secondary,
        proficiency_level=preference.proficiency_level,
        created_at=preference.created_at,
        updated_at=preference.updated_at
    )


@router.get("/users/preferences", response_model=UserLanguagePreferenceListResponse)
async def get_user_language_preferences(
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's language preferences.
    """
    preferences = db.query(UserLanguagePreference).filter(
        UserLanguagePreference.user_id == current_user.id
    ).all()
    
    preference_responses = []
    for preference in preferences:
        preference_responses.append(UserLanguagePreferenceResponse(
            id=str(preference.id),
            user_id=str(preference.user_id),
            language_id=str(preference.language_id),
            is_primary=preference.is_primary,
            is_secondary=preference.is_secondary,
            proficiency_level=preference.proficiency_level,
            created_at=preference.created_at,
            updated_at=preference.updated_at
        ))
    
    return UserLanguagePreferenceListResponse(
        preferences=preference_responses,
        total=len(preference_responses),
        page=1,
        page_size=len(preference_responses),
        total_pages=1,
        has_next=False,
        has_prev=False
    )


# ============================================================================
# LANGUAGE TOGGLE AND SWITCHING
# ============================================================================

@router.post("/toggle")
async def toggle_user_language(
    toggle_data: LanguageToggleRequest = Body(...),
    request: Request = None,
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Toggle user's interface language.
    
    This is the main endpoint for the French/English language toggle feature.
    """
    # Get language by code
    language = db.query(Language).filter(
        and_(
            Language.language_code == toggle_data.language_code,
            Language.is_active == True
        )
    ).first()
    
    if not language:
        raise HTTPException(
            status_code=404,
            detail=f"Language '{toggle_data.language_code}' not found or not active"
        )
    
    # Update or create user preference
    existing_preference = db.query(UserLanguagePreference).filter(
        and_(
            UserLanguagePreference.user_id == current_user.id,
            UserLanguagePreference.language_id == language.id
        )
    ).first()
    
    if existing_preference:
        # Update existing preference
        existing_preference.is_primary = True
        existing_preference.updated_at = datetime.utcnow()
        
        # Set other preferences as secondary
        db.query(UserLanguagePreference).filter(
            and_(
                UserLanguagePreference.user_id == current_user.id,
                UserLanguagePreference.id != existing_preference.id
            )
        ).update({"is_primary": False, "is_secondary": True})
    else:
        # Create new preference
        new_preference = UserLanguagePreference(
            user_id=current_user.id,
            language_id=language.id,
            is_primary=True,
            is_secondary=False,
            proficiency_level="fluent"
        )
        db.add(new_preference)
        
        # Set other preferences as secondary
        db.query(UserLanguagePreference).filter(
            UserLanguagePreference.user_id == current_user.id
        ).update({"is_primary": False, "is_secondary": True})
    
    db.commit()
    
    # Track language usage analytics
    _track_language_usage(db, language.id, current_user.id)
    
    logger.info(f"User language toggled: {current_user.username} - {toggle_data.language_code}")
    
    return {
        "message": f"Language switched to {language.language_name_native}",
        "language_code": language.language_code,
        "language_name": language.language_name,
        "language_name_native": language.language_name_native,
        "direction": language.direction,
        "date_format": language.date_format,
        "time_format": language.time_format,
        "number_format": language.number_format,
        "currency_code": language.currency_code
    }


@router.get("/current")
async def get_current_user_language(
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get current user's active language preference.
    """
    # Get primary language preference
    primary_preference = db.query(UserLanguagePreference).filter(
        and_(
            UserLanguagePreference.user_id == current_user.id,
            UserLanguagePreference.is_primary == True
        )
    ).first()
    
    if not primary_preference:
        # Get default language
        default_language = db.query(Language).filter(Language.is_default == True).first()
        if not default_language:
            default_language = db.query(Language).filter(Language.language_code == "en").first()
        
        return {
            "language_code": default_language.language_code,
            "language_name": default_language.language_name,
            "language_name_native": default_language.language_name_native,
            "is_default": True,
            "direction": default_language.direction,
            "date_format": default_language.date_format,
            "time_format": default_language.time_format,
            "number_format": default_language.number_format,
            "currency_code": default_language.currency_code
        }
    
    # Get language details
    language = db.query(Language).filter(Language.id == primary_preference.language_id).first()
    
    return {
        "language_code": language.language_code,
        "language_name": language.language_name,
        "language_name_native": language.language_name_native,
        "is_default": language.is_default,
        "direction": language.direction,
        "date_format": language.date_format,
        "time_format": language.time_format,
        "number_format": language.number_format,
        "currency_code": language.currency_code,
        "proficiency_level": primary_preference.proficiency_level
    }


# ============================================================================
# TRANSLATION UTILITIES
# ============================================================================

@router.get("/translate/{translation_key}")
async def get_translation_by_key(
    translation_key: str = Path(..., description="Translation key"),
    language_code: LanguageCodeEnum = Query(..., description="Language code"),
    context: Optional[str] = Query(None, description="Translation context"),
    db: DBSession = Depends(get_db)
):
    """
    Get translation by key for a specific language.
    
    This is used by the frontend to get translated text.
    """
    # Get language
    language = db.query(Language).filter(
        and_(
            Language.language_code == language_code,
            Language.is_active == True
        )
    ).first()
    
    if not language:
        raise HTTPException(status_code=404, detail=f"Language '{language_code}' not found")
    
    # Build query for translation
    query = db.query(Translation).filter(
        and_(
            Translation.language_id == language.id,
            Translation.translation_key == translation_key,
            Translation.is_approved == True
        )
    )
    
    if context:
        query = query.filter(Translation.translation_context == context)
    
    # Get latest approved version
    translation = query.order_by(desc(Translation.version)).first()
    
    if not translation:
        # Return fallback (usually English)
        fallback_language = db.query(Language).filter(Language.language_code == "en").first()
        if fallback_language:
            fallback_translation = db.query(Translation).filter(
                and_(
                    Translation.language_id == fallback_language.id,
                    Translation.translation_key == translation_key,
                    Translation.is_approved == True
                )
            ).order_by(desc(Translation.version)).first()
            
            if fallback_translation:
                return {
                    "translation_key": translation_key,
                    "translated_value": fallback_translation.translation_value,
                    "language_code": "en",
                    "is_fallback": True,
                    "context": fallback_translation.translation_context
                }
        
        # Return key as fallback
        return {
            "translation_key": translation_key,
            "translated_value": translation_key,
            "language_code": language_code,
            "is_fallback": True,
            "context": context
        }
    
    return {
        "translation_key": translation_key,
        "translated_value": translation.translation_value,
        "language_code": language_code,
        "is_fallback": False,
        "context": translation.translation_context,
        "version": translation.version
    }


@router.post("/translate/search")
async def search_translations(
    search_data: TranslationSearchRequest = Body(...),
    db: DBSession = Depends(get_db)
):
    """
    Search translations by query.
    """
    # Build base query
    query = db.query(Translation)
    
    # Apply filters
    if search_data.language_code:
        language = db.query(Language).filter(Language.language_code == search_data.language_code).first()
        if language:
            query = query.filter(Translation.language_id == language.id)
    
    if search_data.context:
        query = query.filter(Translation.translation_context == search_data.context)
    
    if search_data.is_approved is not None:
        query = query.filter(Translation.is_approved == search_data.is_approved)
    
    # Apply search query
    search_term = f"%{search_data.query}%"
    query = query.filter(
        or_(
            Translation.translation_value.ilike(search_term),
            Translation.translation_key.ilike(search_term),
            Translation.translation_context.ilike(search_term)
        )
    )
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / search_data.page_size)
    offset = (search_data.page - 1) * search_data.page_size
    
    # Get translations
    translations = query.order_by(Translation.translation_key).offset(offset).limit(search_data.page_size).all()
    
    # Convert to response format
    translation_responses = []
    for translation in translations:
        translation_responses.append(TranslationResponse(
            id=str(translation.id),
            language_id=str(translation.language_id),
            translation_key=translation.translation_key,
            translation_value=translation.translation_value,
            translation_context=translation.translation_context,
            translation_notes=translation.translation_notes,
            is_approved=translation.is_approved,
            approved_by=translation.approved_by,
            approved_at=translation.approved_at,
            version=translation.version,
            created_at=translation.created_at,
            updated_at=translation.updated_at
        ))
    
    return TranslationListResponse(
        translations=translation_responses,
        total=total,
        page=search_data.page,
        page_size=search_data.page_size,
        total_pages=total_pages,
        has_next=search_data.page < total_pages,
        has_prev=search_data.page > 1
    )


# ============================================================================
# STATISTICS AND ANALYTICS
# ============================================================================

@router.get("/statistics")
async def get_language_statistics(
    db: DBSession = Depends(get_db)
):
    """
    Get comprehensive language usage statistics.
    """
    # Get all active languages
    languages = db.query(Language).filter(Language.is_active == True).all()
    
    statistics = []
    for language in languages:
        # Count users with this language preference
        user_count = db.query(UserLanguagePreference).filter(
            UserLanguagePreference.language_id == language.id
        ).count()
        
        # Count translations in this language
        translation_count = db.query(Translation).filter(
            Translation.language_id == language.id
        ).count()
        
        # Count approved translations
        approved_count = db.query(Translation).filter(
            and_(
                Translation.language_id == language.id,
                Translation.is_approved == True
            )
        ).count()
        
        # Calculate coverage percentage
        coverage_percentage = (approved_count / max(translation_count, 1)) * 100 if translation_count > 0 else 0
        
        # Get average quality score (mock for now)
        quality_score = 85.0  # This would come from actual quality metrics
        
        # Get user satisfaction (mock for now)
        user_satisfaction = 90.0  # This would come from user feedback
        
        statistics.append(LanguageStatistics(
            language_code=language.language_code,
            language_name=language.language_name,
            total_users=user_count,
            total_translations=translation_count,
            total_content=approved_count,
            coverage_percentage=round(coverage_percentage, 2),
            quality_score=quality_score,
            user_satisfaction=user_satisfaction,
            last_updated=datetime.utcnow()
        ))
    
    return {
        "languages": statistics,
        "total_languages": len(languages),
        "generated_at": datetime.utcnow()
    }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def _track_language_usage(db: DBSession, language_id: str, user_id: str) -> None:
    """Track language usage for analytics."""
    today = datetime.utcnow().date()
    
    # Get or create analytics record for today
    analytics = db.query(LanguageAnalytics).filter(
        and_(
            LanguageAnalytics.language_id == language_id,
            func.date(LanguageAnalytics.analytics_date) == today
        )
    ).first()
    
    if not analytics:
        analytics = LanguageAnalytics(
            language_id=language_id,
            analytics_date=datetime.utcnow(),
            daily_active_users=1
        )
        db.add(analytics)
    else:
        analytics.daily_active_users += 1
    
    db.commit()
