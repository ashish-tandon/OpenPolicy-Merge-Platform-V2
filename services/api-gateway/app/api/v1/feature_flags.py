"""
Feature Flags API Endpoints

REST API for managing and evaluating feature flags.
Implements FEAT-004 (P0 priority).
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.database import get_db
from app.models.feature_flags import FeatureFlag, FeatureFlagChange
from app.schemas.feature_flags import (
    FeatureFlagCreate,
    FeatureFlagUpdate,
    FeatureFlagResponse,
    FeatureFlagListResponse,
    FeatureFlagEvaluation,
    EvaluationContext,
    BulkEvaluationRequest,
    BulkEvaluationResponse,
    FeatureFlagChangeResponse,
    FeatureFlagStats
)
from app.core.feature_flags import get_feature_flag_service
from app.core.auth import get_current_user, require_admin

router = APIRouter()


@router.post("/evaluate/{feature_name}", response_model=FeatureFlagEvaluation)
async def evaluate_feature_flag(
    feature_name: str,
    context: Optional[EvaluationContext] = None,
    db: Session = Depends(get_db)
):
    """
    Evaluate a single feature flag.
    
    This endpoint checks if a feature flag is enabled for the given context.
    """
    service = get_feature_flag_service(db)
    is_enabled = await service.evaluate(feature_name, context)
    
    return FeatureFlagEvaluation(
        feature_name=feature_name,
        is_enabled=is_enabled,
        reason="Evaluated based on rules and context"
    )


@router.post("/evaluate", response_model=BulkEvaluationResponse)
async def evaluate_feature_flags_bulk(
    request: BulkEvaluationRequest,
    db: Session = Depends(get_db)
):
    """
    Evaluate multiple feature flags at once.
    
    This is more efficient than making multiple individual calls.
    """
    service = get_feature_flag_service(db)
    flags = await service.evaluate_all(request.context, request.feature_names)
    
    return BulkEvaluationResponse(
        flags=flags,
        context=request.context.dict() if request.context else {},
        evaluated_at=datetime.utcnow()
    )


@router.get("/", response_model=FeatureFlagListResponse)
async def list_feature_flags(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    flag_type: Optional[str] = None,
    is_enabled: Optional[bool] = None,
    environment: Optional[str] = None,
    db: Session = Depends(get_db),
    _: Any = Depends(require_admin)
):
    """
    List all feature flags (admin only).
    
    Supports filtering by type, status, and environment.
    """
    query = db.query(FeatureFlag)
    
    # Apply filters
    if flag_type:
        query = query.filter(FeatureFlag.flag_type == flag_type)
    if is_enabled is not None:
        query = query.filter(FeatureFlag.is_enabled == is_enabled)
    if environment:
        query = query.filter(FeatureFlag.environments.contains([environment]))
    
    # Pagination
    total = query.count()
    offset = (page - 1) * page_size
    flags = query.offset(offset).limit(page_size).all()
    
    return FeatureFlagListResponse(
        flags=[FeatureFlagResponse.from_orm(flag) for flag in flags],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{feature_name}", response_model=FeatureFlagResponse)
async def get_feature_flag(
    feature_name: str,
    db: Session = Depends(get_db),
    _: Any = Depends(require_admin)
):
    """Get details of a specific feature flag (admin only)."""
    flag = db.query(FeatureFlag).filter(
        FeatureFlag.feature_name == feature_name
    ).first()
    
    if not flag:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    
    return FeatureFlagResponse.from_orm(flag)


@router.post("/", response_model=FeatureFlagResponse)
async def create_feature_flag(
    flag_data: FeatureFlagCreate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(require_admin)
):
    """Create a new feature flag (admin only)."""
    # Check if flag already exists
    existing = db.query(FeatureFlag).filter(
        FeatureFlag.feature_name == flag_data.feature_name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Feature flag '{flag_data.feature_name}' already exists"
        )
    
    service = get_feature_flag_service(db)
    created_by = flag_data.created_by or current_user.email
    
    # Convert Pydantic model to dict
    flag_dict = flag_data.dict(exclude={'created_by'})
    if flag_dict.get('targeting_rules'):
        flag_dict['targeting_rules'] = flag_dict['targeting_rules'].dict()
    
    flag = service.create_flag(flag_dict, created_by)
    
    return FeatureFlagResponse.from_orm(flag)


@router.put("/{feature_name}", response_model=FeatureFlagResponse)
async def update_feature_flag(
    feature_name: str,
    updates: FeatureFlagUpdate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(require_admin)
):
    """Update an existing feature flag (admin only)."""
    service = get_feature_flag_service(db)
    
    # Convert updates to dict, excluding None values
    update_dict = {k: v for k, v in updates.dict().items() if v is not None}
    if 'targeting_rules' in update_dict and update_dict['targeting_rules']:
        update_dict['targeting_rules'] = update_dict['targeting_rules'].dict()
    
    flag = service.update_flag(feature_name, update_dict, current_user.email)
    
    if not flag:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    
    return FeatureFlagResponse.from_orm(flag)


@router.delete("/{feature_name}")
async def delete_feature_flag(
    feature_name: str,
    db: Session = Depends(get_db),
    current_user: Any = Depends(require_admin)
):
    """Delete a feature flag (admin only)."""
    service = get_feature_flag_service(db)
    
    if not service.delete_flag(feature_name, current_user.email):
        raise HTTPException(status_code=404, detail="Feature flag not found")
    
    return {"message": f"Feature flag '{feature_name}' deleted successfully"}


@router.post("/{feature_name}/toggle")
async def toggle_feature_flag(
    feature_name: str,
    db: Session = Depends(get_db),
    current_user: Any = Depends(require_admin)
):
    """Toggle a feature flag on/off (admin only)."""
    flag = db.query(FeatureFlag).filter(
        FeatureFlag.feature_name == feature_name
    ).first()
    
    if not flag:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    
    service = get_feature_flag_service(db)
    new_state = not flag.is_enabled
    
    service.update_flag(
        feature_name, 
        {"is_enabled": new_state}, 
        current_user.email
    )
    
    return {
        "feature_name": feature_name,
        "is_enabled": new_state,
        "message": f"Feature flag {'enabled' if new_state else 'disabled'}"
    }


@router.get("/{feature_name}/history", response_model=List[FeatureFlagChangeResponse])
async def get_feature_flag_history(
    feature_name: str,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: Any = Depends(require_admin)
):
    """Get change history for a feature flag (admin only)."""
    flag = db.query(FeatureFlag).filter(
        FeatureFlag.feature_name == feature_name
    ).first()
    
    if not flag:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    
    changes = db.query(FeatureFlagChange).filter(
        FeatureFlagChange.flag_id == flag.id
    ).order_by(FeatureFlagChange.changed_at.desc()).limit(limit).all()
    
    return [
        FeatureFlagChangeResponse(
            **change.__dict__,
            feature_name=feature_name
        ) for change in changes
    ]


@router.get("/{feature_name}/stats", response_model=FeatureFlagStats)
async def get_feature_flag_stats(
    feature_name: str,
    db: Session = Depends(get_db),
    _: Any = Depends(require_admin)
):
    """Get evaluation statistics for a feature flag (admin only)."""
    service = get_feature_flag_service(db)
    stats = service.get_flag_stats(feature_name)
    
    if not stats:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    
    return FeatureFlagStats(**stats)