"""
Feedback API endpoints.

Implements FEAT-003 Feedback Collection (P1 priority).
Provides endpoints for submitting and managing user feedback.
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user_optional, get_current_user, require_permission
from app.core.feedback import FeedbackService, get_feedback_service
from app.models.users import User
from app.schemas.feedback import (
    FeedbackCreate, FeedbackUpdate, FeedbackResponse, FeedbackListResponse,
    FeedbackAssign, FeedbackFilter, FeedbackStats, FeedbackTrends,
    AttachmentCreate, AttachmentResponse,
    ResponseCreate, ResponseUpdate, ResponseItem,
    VoteCreate, VoteResponse,
    TemplateCreate, TemplateUpdate, TemplateResponse,
    FeedbackType, FeedbackStatus, FeedbackPriority, FeedbackCategory
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Public endpoints (no auth required)
@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    feedback_data: FeedbackCreate,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    Submit new feedback.
    
    Can be submitted anonymously or by authenticated users.
    Anonymous users can provide email and name for follow-up.
    """
    service = get_feedback_service(db)
    feedback = service.create_feedback(feedback_data, current_user)
    
    # Get additional data
    response = FeedbackResponse.from_orm(feedback)
    response.attachment_count = len(feedback.attachments)
    response.response_count = len(feedback.responses)
    response.vote_score = sum(v.vote_type for v in feedback.votes)
    
    return response


@router.get("/templates", response_model=List[TemplateResponse])
async def get_feedback_templates(
    type: Optional[FeedbackType] = Query(None),
    category: Optional[FeedbackCategory] = Query(None),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get available feedback templates."""
    service = get_feedback_service(db)
    templates = service.get_templates(type, category, active_only)
    return templates


# Authenticated endpoints
@router.get("/my-feedback", response_model=FeedbackListResponse)
async def get_my_feedback(
    status: Optional[FeedbackStatus] = Query(None),
    type: Optional[FeedbackType] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get feedback submitted by the current user."""
    filter_params = FeedbackFilter(
        user_id=current_user.id,
        status=status,
        type=type,
        page=page,
        page_size=page_size
    )
    
    service = get_feedback_service(db)
    feedback_items, total_count = service.search_feedback(filter_params)
    
    # Build response
    results = []
    for feedback in feedback_items:
        response = FeedbackResponse.from_orm(feedback)
        response.attachment_count = len(feedback.attachments)
        response.response_count = len(feedback.responses)
        response.vote_score = sum(v.vote_type for v in feedback.votes)
        results.append(response)
    
    return FeedbackListResponse(
        results=results,
        pagination={
            "page": page,
            "page_size": page_size,
            "total": total_count,
            "total_pages": (total_count + page_size - 1) // page_size
        },
        filters={
            "status": status,
            "type": type
        }
    )


@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(
    feedback_id: UUID,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get feedback details."""
    service = get_feedback_service(db)
    feedback = service.get_feedback(feedback_id)
    
    # Check permissions for internal responses
    is_admin = current_user and hasattr(current_user, 'is_admin') and current_user.is_admin
    is_owner = current_user and feedback.user_id == current_user.id
    
    # Build response
    response = FeedbackResponse.from_orm(feedback)
    response.attachment_count = len(feedback.attachments)
    response.response_count = len([r for r in feedback.responses if not r.is_internal or is_admin or is_owner])
    response.vote_score = sum(v.vote_type for v in feedback.votes)
    
    return response


@router.put("/{feedback_id}", response_model=FeedbackResponse)
async def update_feedback(
    feedback_id: UUID,
    feedback_data: FeedbackUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update feedback (owner or admin only)."""
    service = get_feedback_service(db)
    feedback = service.get_feedback(feedback_id)
    
    # Check permissions
    if feedback.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this feedback"
        )
    
    updated_feedback = service.update_feedback(feedback_id, feedback_data, current_user)
    
    # Build response
    response = FeedbackResponse.from_orm(updated_feedback)
    response.attachment_count = len(updated_feedback.attachments)
    response.response_count = len(updated_feedback.responses)
    response.vote_score = sum(v.vote_type for v in updated_feedback.votes)
    
    return response


@router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feedback(
    feedback_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete feedback (owner or admin only)."""
    service = get_feedback_service(db)
    service.delete_feedback(feedback_id, current_user)


# Voting endpoints
@router.post("/{feedback_id}/vote", response_model=VoteResponse)
async def vote_on_feedback(
    feedback_id: UUID,
    vote_data: VoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Vote on feedback (upvote or downvote)."""
    service = get_feedback_service(db)
    vote_stats = service.vote_feedback(feedback_id, vote_data, current_user)
    return VoteResponse(**vote_stats)


# Response endpoints
@router.get("/{feedback_id}/responses", response_model=List[ResponseItem])
async def get_feedback_responses(
    feedback_id: UUID,
    include_internal: bool = Query(False),
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get responses for feedback."""
    service = get_feedback_service(db)
    feedback = service.get_feedback(feedback_id)
    
    # Filter responses based on permissions
    is_admin = current_user and hasattr(current_user, 'is_admin') and current_user.is_admin
    is_owner = current_user and feedback.user_id == current_user.id
    
    responses = []
    for response in feedback.responses:
        if not response.is_internal or (include_internal and (is_admin or is_owner)):
            item = ResponseItem.from_orm(response)
            item.user_name = response.user.full_name if response.user else "System"
            responses.append(item)
    
    return responses


@router.post("/{feedback_id}/responses", response_model=ResponseItem, status_code=status.HTTP_201_CREATED)
async def add_feedback_response(
    feedback_id: UUID,
    response_data: ResponseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add response to feedback."""
    service = get_feedback_service(db)
    response = service.add_response(feedback_id, response_data, current_user)
    
    item = ResponseItem.from_orm(response)
    item.user_name = current_user.full_name
    
    return item


@router.put("/responses/{response_id}", response_model=ResponseItem)
async def update_feedback_response(
    response_id: UUID,
    response_data: ResponseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update feedback response."""
    service = get_feedback_service(db)
    response = service.update_response(response_id, response_data.message, current_user)
    
    item = ResponseItem.from_orm(response)
    item.user_name = response.user.full_name if response.user else "System"
    
    return item


# Attachment endpoints
@router.post("/{feedback_id}/attachments", response_model=AttachmentResponse, status_code=status.HTTP_201_CREATED)
async def add_feedback_attachment(
    feedback_id: UUID,
    attachment_data: AttachmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add attachment to feedback."""
    service = get_feedback_service(db)
    attachment = service.add_attachment(feedback_id, attachment_data, current_user)
    
    return AttachmentResponse.from_orm(attachment)


@router.delete("/attachments/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feedback_attachment(
    attachment_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete feedback attachment."""
    service = get_feedback_service(db)
    service.delete_attachment(attachment_id, current_user)


# Admin endpoints
@router.get("/admin/all", response_model=FeedbackListResponse)
async def get_all_feedback(
    filter_params: FeedbackFilter = Depends(),
    current_user: User = Depends(require_permission("feedback", "read")),
    db: Session = Depends(get_db)
):
    """Get all feedback (admin only)."""
    service = get_feedback_service(db)
    feedback_items, total_count = service.search_feedback(filter_params)
    
    # Build response
    results = []
    for feedback in feedback_items:
        response = FeedbackResponse.from_orm(feedback)
        response.attachment_count = len(feedback.attachments)
        response.response_count = len(feedback.responses)
        response.vote_score = sum(v.vote_type for v in feedback.votes)
        results.append(response)
    
    return FeedbackListResponse(
        results=results,
        pagination={
            "page": filter_params.page,
            "page_size": filter_params.page_size,
            "total": total_count,
            "total_pages": (total_count + filter_params.page_size - 1) // filter_params.page_size
        },
        filters=filter_params.dict(exclude={'page', 'page_size', 'sort_by', 'sort_order'})
    )


@router.post("/{feedback_id}/assign", response_model=FeedbackResponse)
async def assign_feedback(
    feedback_id: UUID,
    assign_data: FeedbackAssign,
    current_user: User = Depends(require_permission("feedback", "write")),
    db: Session = Depends(get_db)
):
    """Assign feedback to a user (admin only)."""
    service = get_feedback_service(db)
    feedback = service.assign_feedback(feedback_id, assign_data, current_user)
    
    # Build response
    response = FeedbackResponse.from_orm(feedback)
    response.attachment_count = len(feedback.attachments)
    response.response_count = len(feedback.responses)
    response.vote_score = sum(v.vote_type for v in feedback.votes)
    
    return response


# Template management (admin)
@router.post("/templates", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_feedback_template(
    template_data: TemplateCreate,
    current_user: User = Depends(require_permission("feedback", "write")),
    db: Session = Depends(get_db)
):
    """Create feedback template (admin only)."""
    service = get_feedback_service(db)
    template = service.create_template(template_data)
    return TemplateResponse.from_orm(template)


@router.put("/templates/{template_id}", response_model=TemplateResponse)
async def update_feedback_template(
    template_id: UUID,
    template_data: TemplateUpdate,
    current_user: User = Depends(require_permission("feedback", "write")),
    db: Session = Depends(get_db)
):
    """Update feedback template (admin only)."""
    service = get_feedback_service(db)
    template = service.update_template(template_id, template_data)
    return TemplateResponse.from_orm(template)


# Analytics endpoints
@router.get("/analytics/stats", response_model=FeedbackStats)
async def get_feedback_statistics(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    current_user: User = Depends(require_permission("feedback", "read")),
    db: Session = Depends(get_db)
):
    """Get feedback statistics (admin only)."""
    from datetime import datetime
    
    start = datetime.fromisoformat(start_date) if start_date else None
    end = datetime.fromisoformat(end_date) if end_date else None
    
    service = get_feedback_service(db)
    stats = service.get_feedback_stats(start, end)
    
    return stats


@router.get("/analytics/trends", response_model=FeedbackTrends)
async def get_feedback_trends(
    period: str = Query("daily", regex="^(daily|weekly|monthly)$"),
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(require_permission("feedback", "read")),
    db: Session = Depends(get_db)
):
    """Get feedback trends over time (admin only)."""
    service = get_feedback_service(db)
    trends = service.get_feedback_trends(period, days)
    
    return trends