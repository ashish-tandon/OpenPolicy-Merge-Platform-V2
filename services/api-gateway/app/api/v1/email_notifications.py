"""
Email Notification API endpoints.

Implements FEAT-007 Email Notifications (P2 priority).
Provides comprehensive email notification management.
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.core.dependencies import get_current_user, require_permission
from app.core.email_notifications import EmailNotificationService, get_email_notification_service
from app.models.users import User
from app.schemas.email_notifications import (
    EmailTemplateCreate, EmailTemplateUpdate, EmailTemplateResponse,
    PreferenceUpdate, PreferenceResponse,
    EmailNotificationCreate, EmailNotificationResponse, EmailNotificationListResponse,
    EmailEventResponse, AttachmentResponse,
    EmailBatchCreate, EmailBatchUpdate, EmailBatchResponse,
    SendEmailRequest, SendBulkEmailRequest,
    EmailAnalytics, ProviderStats,
    WebhookEvent, UnsubscribeRequest, UnsubscribeResponse,
    EmailStatus, NotificationType, NotificationPriority
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Template endpoints
@router.post("/templates", response_model=EmailTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_email_template(
    template_data: EmailTemplateCreate,
    current_user: User = Depends(require_permission("notifications", "write")),
    db: Session = Depends(get_db)
):
    """Create a new email template (admin only)."""
    service = get_email_notification_service(db)
    template = service.create_template(template_data)
    
    response = EmailTemplateResponse.from_orm(template)
    response.usage_count = len(template.notifications)
    
    return response


@router.get("/templates", response_model=List[EmailTemplateResponse])
async def list_email_templates(
    notification_type: Optional[NotificationType] = Query(None),
    is_active: bool = Query(True),
    language: str = Query("en"),
    db: Session = Depends(get_db)
):
    """List available email templates."""
    from app.models.email_notifications import EmailTemplate
    
    query = db.query(EmailTemplate).filter(
        EmailTemplate.is_active == is_active,
        EmailTemplate.language == language
    )
    
    if notification_type:
        query = query.filter(EmailTemplate.notification_type == notification_type)
    
    templates = query.order_by(EmailTemplate.template_key, EmailTemplate.version.desc()).all()
    
    responses = []
    for template in templates:
        response = EmailTemplateResponse.from_orm(template)
        response.usage_count = len(template.notifications)
        responses.append(response)
    
    return responses


@router.get("/templates/{template_id}", response_model=EmailTemplateResponse)
async def get_email_template(
    template_id: UUID,
    db: Session = Depends(get_db)
):
    """Get email template details."""
    from app.models.email_notifications import EmailTemplate
    
    template = db.query(EmailTemplate).filter(
        EmailTemplate.id == template_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    response = EmailTemplateResponse.from_orm(template)
    response.usage_count = len(template.notifications)
    
    return response


@router.put("/templates/{template_id}", response_model=EmailTemplateResponse)
async def update_email_template(
    template_id: UUID,
    template_data: EmailTemplateUpdate,
    current_user: User = Depends(require_permission("notifications", "write")),
    db: Session = Depends(get_db)
):
    """Update email template (admin only)."""
    from app.models.email_notifications import EmailTemplate
    
    template = db.query(EmailTemplate).filter(
        EmailTemplate.id == template_id
    ).first()
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    for field, value in template_data.dict(exclude_unset=True).items():
        setattr(template, field, value)
    
    db.commit()
    
    response = EmailTemplateResponse.from_orm(template)
    response.usage_count = len(template.notifications)
    
    return response


# Preference endpoints
@router.get("/preferences", response_model=PreferenceResponse)
async def get_notification_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's notification preferences."""
    service = get_email_notification_service(db)
    preferences = service.get_or_create_preferences(current_user.id)
    
    return PreferenceResponse.from_orm(preferences)


@router.put("/preferences", response_model=PreferenceResponse)
async def update_notification_preferences(
    pref_data: PreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's notification preferences."""
    service = get_email_notification_service(db)
    preferences = service.update_preferences(current_user.id, pref_data)
    
    return PreferenceResponse.from_orm(preferences)


# Send email endpoints
@router.post("/send", response_model=List[EmailNotificationResponse])
async def send_email(
    request: SendEmailRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send email to recipients."""
    service = get_email_notification_service(db)
    
    # Note: In production, this would be properly async
    import asyncio
    notifications = asyncio.run(service.send_email(request, current_user))
    
    return [EmailNotificationResponse.from_orm(n) for n in notifications]


@router.post("/send-bulk", response_model=EmailBatchResponse)
async def send_bulk_email(
    request: SendBulkEmailRequest,
    current_user: User = Depends(require_permission("notifications", "write")),
    db: Session = Depends(get_db)
):
    """Send bulk emails (admin only)."""
    service = get_email_notification_service(db)
    
    # Create batch
    batch_data = EmailBatchCreate(
        name=request.batch_name,
        batch_type="campaign",
        template_id=request.template_id,
        recipient_criteria={"recipients": request.recipients},
        scheduled_for=request.scheduled_for
    )
    
    batch = service.create_batch(batch_data, current_user)
    
    # Schedule or send immediately
    if not request.scheduled_for or request.scheduled_for <= datetime.utcnow():
        import asyncio
        asyncio.run(service.send_batch(batch.id))
    
    return EmailBatchResponse.from_orm(batch)


# Notification history
@router.get("/history", response_model=EmailNotificationListResponse)
async def get_notification_history(
    status: Optional[EmailStatus] = Query(None),
    notification_type: Optional[NotificationType] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's notification history."""
    from app.models.email_notifications import EmailNotification
    
    query = db.query(EmailNotification).filter(
        EmailNotification.user_id == current_user.id
    )
    
    if status:
        query = query.filter(EmailNotification.status == status)
    
    if notification_type:
        query = query.filter(EmailNotification.notification_type == notification_type)
    
    if start_date:
        query = query.filter(EmailNotification.created_at >= start_date)
    
    if end_date:
        query = query.filter(EmailNotification.created_at <= end_date)
    
    total_count = query.count()
    
    # Order by created date descending
    query = query.order_by(EmailNotification.created_at.desc())
    
    # Pagination
    offset = (page - 1) * page_size
    notifications = query.offset(offset).limit(page_size).all()
    
    return EmailNotificationListResponse(
        results=[EmailNotificationResponse.from_orm(n) for n in notifications],
        pagination={
            "page": page,
            "page_size": page_size,
            "total": total_count,
            "total_pages": (total_count + page_size - 1) // page_size
        }
    )


@router.get("/notifications/{notification_id}", response_model=EmailNotificationResponse)
async def get_notification_details(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notification details."""
    from app.models.email_notifications import EmailNotification
    
    notification = db.query(EmailNotification).filter(
        EmailNotification.id == notification_id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    # Check ownership
    if notification.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this notification"
        )
    
    return EmailNotificationResponse.from_orm(notification)


# Event endpoints
@router.get("/notifications/{notification_id}/events", response_model=List[EmailEventResponse])
async def get_notification_events(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notification events."""
    from app.models.email_notifications import EmailNotification, EmailEvent
    
    # Verify notification exists and user has access
    notification = db.query(EmailNotification).filter(
        EmailNotification.id == notification_id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    if notification.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    events = db.query(EmailEvent).filter(
        EmailEvent.notification_id == notification_id
    ).order_by(EmailEvent.occurred_at).all()
    
    return [EmailEventResponse.from_orm(e) for e in events]


# Batch endpoints
@router.post("/batches", response_model=EmailBatchResponse, status_code=status.HTTP_201_CREATED)
async def create_email_batch(
    batch_data: EmailBatchCreate,
    current_user: User = Depends(require_permission("notifications", "write")),
    db: Session = Depends(get_db)
):
    """Create email batch (admin only)."""
    service = get_email_notification_service(db)
    batch = service.create_batch(batch_data, current_user)
    
    return EmailBatchResponse.from_orm(batch)


@router.get("/batches", response_model=List[EmailBatchResponse])
async def list_email_batches(
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_permission("notifications", "read")),
    db: Session = Depends(get_db)
):
    """List email batches (admin only)."""
    from app.models.email_notifications import EmailBatch
    
    query = db.query(EmailBatch)
    
    if status:
        query = query.filter(EmailBatch.status == status)
    
    # Order by created date descending
    query = query.order_by(EmailBatch.created_at.desc())
    
    # Pagination
    offset = (page - 1) * page_size
    batches = query.offset(offset).limit(page_size).all()
    
    return [EmailBatchResponse.from_orm(b) for b in batches]


@router.post("/batches/{batch_id}/send", response_model=EmailBatchResponse)
async def send_email_batch(
    batch_id: UUID,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(require_permission("notifications", "write")),
    db: Session = Depends(get_db)
):
    """Send email batch (admin only)."""
    service = get_email_notification_service(db)
    
    # Note: In production, this would be properly async
    import asyncio
    batch = asyncio.run(service.send_batch(batch_id))
    
    return EmailBatchResponse.from_orm(batch)


# Analytics endpoints
@router.get("/analytics", response_model=EmailAnalytics)
async def get_email_analytics(
    period: str = Query("week", regex="^(day|week|month)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: User = Depends(require_permission("notifications", "read")),
    db: Session = Depends(get_db)
):
    """Get email analytics (admin only)."""
    service = get_email_notification_service(db)
    
    # Calculate date range based on period
    if not end_date:
        end_date = datetime.utcnow()
    
    if not start_date:
        if period == "day":
            start_date = end_date - timedelta(days=1)
        elif period == "week":
            start_date = end_date - timedelta(weeks=1)
        else:  # month
            start_date = end_date - timedelta(days=30)
    
    analytics = service.get_analytics(start_date, end_date)
    
    return EmailAnalytics(**analytics)


@router.get("/analytics/providers", response_model=List[ProviderStats])
async def get_provider_stats(
    current_user: User = Depends(require_permission("notifications", "read")),
    db: Session = Depends(get_db)
):
    """Get email provider statistics (admin only)."""
    from app.models.email_notifications import EmailProvider as EmailProviderModel
    
    providers = db.query(EmailProviderModel).all()
    
    stats = []
    for provider in providers:
        success_rate = 0
        if provider.total_sent > 0:
            success_rate = ((provider.total_sent - provider.total_failed) / provider.total_sent) * 100
        
        stats.append(ProviderStats(
            provider=provider.provider_type,
            is_active=provider.is_active,
            total_sent=provider.total_sent,
            total_failed=provider.total_failed,
            success_rate=round(success_rate, 2),
            avg_delivery_time=None,  # Would calculate from events
            last_used_at=provider.last_used_at
        ))
    
    return stats


# Webhook endpoints
@router.post("/webhooks/{provider}")
async def handle_webhook(
    provider: str,
    event: WebhookEvent,
    db: Session = Depends(get_db)
):
    """Handle webhooks from email providers."""
    from app.models.email_notifications import EmailNotification, EmailEvent
    
    # Find notification by provider message ID
    notification = db.query(EmailNotification).filter(
        EmailNotification.provider_message_id == event.message_id
    ).first()
    
    if not notification:
        logger.warning(f"Webhook received for unknown message: {event.message_id}")
        return {"status": "ignored"}
    
    # Create event
    email_event = EmailEvent(
        notification_id=notification.id,
        event_type=event.event_type,
        event_data=event.data,
        occurred_at=event.timestamp
    )
    
    db.add(email_event)
    
    # Update notification status based on event
    if event.event_type == "delivered":
        notification.status = EmailStatus.DELIVERED
        notification.delivered_at = event.timestamp
    elif event.event_type == "opened":
        notification.opened_at = event.timestamp
    elif event.event_type == "clicked":
        notification.clicked_at = event.timestamp
    elif event.event_type == "bounced":
        notification.status = EmailStatus.BOUNCED
    elif event.event_type == "complained":
        notification.status = EmailStatus.COMPLAINED
    
    db.commit()
    
    return {"status": "processed"}


# Unsubscribe endpoints
@router.post("/unsubscribe", response_model=UnsubscribeResponse)
async def unsubscribe(
    request: UnsubscribeRequest,
    db: Session = Depends(get_db)
):
    """Process unsubscribe request."""
    service = get_email_notification_service(db)
    result = service.unsubscribe(request)
    
    return UnsubscribeResponse(**result)


@router.get("/unsubscribe/{token}")
async def unsubscribe_page(
    token: str,
    db: Session = Depends(get_db)
):
    """Display unsubscribe page."""
    from app.models.email_notifications import NotificationPreference
    
    # Verify token
    prefs = db.query(NotificationPreference).filter(
        NotificationPreference.unsubscribe_token == token
    ).first()
    
    if not prefs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid unsubscribe link"
        )
    
    # In production, this would return an HTML page
    return {
        "message": "Unsubscribe page",
        "token": token,
        "user_id": str(prefs.user_id),
        "current_preferences": prefs.preferences
    }


# Test endpoints
@router.post("/test")
async def send_test_email(
    template_key: str = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send test email to current user."""
    service = get_email_notification_service(db)
    
    # Test variables
    test_variables = {
        "user_name": current_user.full_name,
        "test_message": "This is a test email from OpenPolicy",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Note: In production, this would be properly async
    import asyncio
    notification = asyncio.run(service.send_templated_email(
        current_user,
        template_key,
        test_variables,
        NotificationType.CUSTOM,
        NotificationPriority.HIGH
    ))
    
    return {
        "status": "sent",
        "notification_id": str(notification.id) if notification else None,
        "recipient": current_user.email
    }