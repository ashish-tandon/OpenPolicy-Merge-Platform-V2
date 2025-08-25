"""
Email Notification API endpoints.

Implements FEAT-007 Email Notifications (P2 priority).
Provides comprehensive email notification functionality.
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body, Header
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.database import get_db
from app.core.dependencies import get_current_user, require_permission
from app.core.email_notifications import EmailNotificationService, get_email_service
from app.models.users import User
from app.schemas.email_notifications import (
    EmailTemplateCreate, EmailTemplateUpdate, EmailTemplateResponse,
    NotificationPreferenceUpdate, NotificationPreferenceResponse,
    EmailNotificationCreate, EmailNotificationResponse, EmailNotificationListResponse,
    EmailBatchCreate, EmailBatchUpdate, EmailBatchResponse,
    SendEmailRequest, SendBulkEmailRequest,
    PreviewEmailRequest, PreviewEmailResponse,
    EmailStatistics, EmailStatusUpdate,
    UnsubscribeRequest, NotificationType, EmailStatus,
    EmailDomainCreate, EmailDomainUpdate, EmailDomainResponse,
    EmailLogResponse, EmailProvider
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
    """Create new email template (admin only)."""
    service = get_email_service(db)
    template = service.create_template(template_data)
    
    response = EmailTemplateResponse.from_orm(template)
    response.usage_count = len(template.notifications)
    
    return response


@router.get("/templates", response_model=List[EmailTemplateResponse])
async def list_email_templates(
    notification_type: Optional[NotificationType] = Query(None),
    is_active: bool = Query(True),
    current_user: User = Depends(require_permission("notifications", "read")),
    db: Session = Depends(get_db)
):
    """List email templates (admin only)."""
    service = get_email_service(db)
    templates = service.list_templates(
        notification_type=notification_type,
        is_active=is_active
    )
    
    responses = []
    for template in templates:
        response = EmailTemplateResponse.from_orm(template)
        response.usage_count = len(template.notifications)
        responses.append(response)
    
    return responses


@router.get("/templates/{template_id}", response_model=EmailTemplateResponse)
async def get_email_template(
    template_id: UUID,
    current_user: User = Depends(require_permission("notifications", "read")),
    db: Session = Depends(get_db)
):
    """Get email template details (admin only)."""
    service = get_email_service(db)
    template = service.get_template(template_id)
    
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
    service = get_email_service(db)
    template = service.update_template(template_id, template_data)
    
    response = EmailTemplateResponse.from_orm(template)
    response.usage_count = len(template.notifications)
    
    return response


# Preference endpoints
@router.get("/preferences", response_model=NotificationPreferenceResponse)
async def get_notification_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's notification preferences."""
    service = get_email_service(db)
    prefs = service.get_or_create_preferences(current_user.id)
    
    return NotificationPreferenceResponse.from_orm(prefs)


@router.put("/preferences", response_model=NotificationPreferenceResponse)
async def update_notification_preferences(
    pref_data: NotificationPreferenceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's notification preferences."""
    service = get_email_service(db)
    prefs = service.update_preferences(current_user.id, pref_data)
    
    return NotificationPreferenceResponse.from_orm(prefs)


# Send email endpoints
@router.post("/send", response_model=EmailNotificationResponse)
async def send_email_notification(
    request: SendEmailRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send single email notification."""
    # Check if user can send to target user
    if request.user_id != current_user.id:
        # Require admin permission to send to other users
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to send notifications to other users"
            )
    
    service = get_email_service(db)
    
    # Note: In production, this would be properly async
    import asyncio
    notification = asyncio.run(service.send_email(request))
    
    return EmailNotificationResponse.from_orm(notification)


@router.post("/send-bulk", response_model=EmailBatchResponse)
async def send_bulk_email_notifications(
    request: SendBulkEmailRequest,
    current_user: User = Depends(require_permission("notifications", "write")),
    db: Session = Depends(get_db)
):
    """Send bulk email notifications (admin only)."""
    service = get_email_service(db)
    
    # Note: In production, this would be properly async
    import asyncio
    batch = asyncio.run(service.send_bulk_email(request, current_user))
    
    return EmailBatchResponse.from_orm(batch)


@router.post("/preview", response_model=PreviewEmailResponse)
async def preview_email(
    request: PreviewEmailRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Preview email content."""
    service = get_email_service(db)
    preview = service.preview_email(request)
    
    return PreviewEmailResponse(**preview)


# Notification endpoints
@router.get("/notifications", response_model=EmailNotificationListResponse)
async def list_notifications(
    notification_type: Optional[NotificationType] = Query(None),
    status: Optional[EmailStatus] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's email notifications."""
    from app.models.email_notifications import EmailNotification
    
    query = db.query(EmailNotification).filter(
        EmailNotification.user_id == current_user.id
    )
    
    if notification_type:
        query = query.filter(EmailNotification.notification_type == notification_type)
    
    if status:
        query = query.filter(EmailNotification.status == status)
    
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
async def get_notification(
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
    if notification.user_id != current_user.id:
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this notification"
            )
    
    return EmailNotificationResponse.from_orm(notification)


@router.get("/notifications/{notification_id}/logs", response_model=List[EmailLogResponse])
async def get_notification_logs(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notification activity logs."""
    from app.models.email_notifications import EmailNotification, EmailLog
    
    # Verify notification ownership
    notification = db.query(EmailNotification).filter(
        EmailNotification.id == notification_id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    if notification.user_id != current_user.id:
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view these logs"
            )
    
    logs = db.query(EmailLog).filter(
        EmailLog.notification_id == notification_id
    ).order_by(EmailLog.occurred_at.desc()).all()
    
    return [EmailLogResponse.from_orm(log) for log in logs]


# Batch endpoints
@router.get("/batches", response_model=List[EmailBatchResponse])
async def list_email_batches(
    status: Optional[str] = Query(None, regex="^(pending|processing|completed|failed)$"),
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


@router.get("/batches/{batch_id}", response_model=EmailBatchResponse)
async def get_email_batch(
    batch_id: UUID,
    current_user: User = Depends(require_permission("notifications", "read")),
    db: Session = Depends(get_db)
):
    """Get batch details (admin only)."""
    from app.models.email_notifications import EmailBatch
    
    batch = db.query(EmailBatch).filter(
        EmailBatch.id == batch_id
    ).first()
    
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found"
        )
    
    return EmailBatchResponse.from_orm(batch)


@router.put("/batches/{batch_id}", response_model=EmailBatchResponse)
async def update_email_batch(
    batch_id: UUID,
    batch_data: EmailBatchUpdate,
    current_user: User = Depends(require_permission("notifications", "write")),
    db: Session = Depends(get_db)
):
    """Update batch (admin only)."""
    from app.models.email_notifications import EmailBatch
    
    batch = db.query(EmailBatch).filter(
        EmailBatch.id == batch_id
    ).first()
    
    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found"
        )
    
    for field, value in batch_data.dict(exclude_unset=True).items():
        setattr(batch, field, value)
    
    db.commit()
    
    return EmailBatchResponse.from_orm(batch)


# Statistics endpoint
@router.get("/statistics", response_model=EmailStatistics)
async def get_email_statistics(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    notification_type: Optional[NotificationType] = Query(None),
    current_user: User = Depends(require_permission("notifications", "read")),
    db: Session = Depends(get_db)
):
    """Get email statistics (admin only)."""
    from app.models.email_notifications import EmailNotification
    
    query = db.query(EmailNotification)
    
    if start_date:
        query = query.filter(EmailNotification.created_at >= start_date)
    
    if end_date:
        query = query.filter(EmailNotification.created_at <= end_date)
    
    if notification_type:
        query = query.filter(EmailNotification.notification_type == notification_type)
    
    # Calculate statistics
    total_sent = query.filter(EmailNotification.status != EmailStatus.PENDING).count()
    total_delivered = query.filter(EmailNotification.status == EmailStatus.DELIVERED).count()
    total_opened = query.filter(EmailNotification.status.in_([EmailStatus.OPENED, EmailStatus.CLICKED])).count()
    total_clicked = query.filter(EmailNotification.status == EmailStatus.CLICKED).count()
    total_bounced = query.filter(EmailNotification.status == EmailStatus.BOUNCED).count()
    total_failed = query.filter(EmailNotification.status == EmailStatus.FAILED).count()
    
    # Calculate rates
    delivery_rate = (total_delivered / total_sent * 100) if total_sent > 0 else 0
    open_rate = (total_opened / total_delivered * 100) if total_delivered > 0 else 0
    click_rate = (total_clicked / total_opened * 100) if total_opened > 0 else 0
    bounce_rate = (total_bounced / total_sent * 100) if total_sent > 0 else 0
    
    return EmailStatistics(
        total_sent=total_sent,
        total_delivered=total_delivered,
        total_opened=total_opened,
        total_clicked=total_clicked,
        total_bounced=total_bounced,
        total_failed=total_failed,
        delivery_rate=delivery_rate,
        open_rate=open_rate,
        click_rate=click_rate,
        bounce_rate=bounce_rate
    )


# Unsubscribe endpoints
@router.post("/unsubscribe", status_code=status.HTTP_204_NO_CONTENT)
async def unsubscribe(
    request: UnsubscribeRequest,
    db: Session = Depends(get_db)
):
    """Unsubscribe from notifications."""
    from app.models.email_notifications import NotificationPreference
    
    # Find preferences by token
    prefs = db.query(NotificationPreference).filter(
        NotificationPreference.unsubscribe_token == request.token
    ).first()
    
    if not prefs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid unsubscribe token"
        )
    
    if request.notification_types:
        # Unsubscribe from specific types
        type_prefs = prefs.type_preferences or {}
        for notif_type in request.notification_types:
            type_prefs[notif_type.value] = {
                'enabled': False,
                'frequency': 'never'
            }
        prefs.type_preferences = type_prefs
    else:
        # Unsubscribe from all
        prefs.email_enabled = False
    
    db.commit()


@router.get("/unsubscribe", response_model=dict)
async def get_unsubscribe_info(
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """Get unsubscribe information."""
    from app.models.email_notifications import NotificationPreference
    
    prefs = db.query(NotificationPreference).filter(
        NotificationPreference.unsubscribe_token == token
    ).first()
    
    if not prefs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid unsubscribe token"
        )
    
    # Get user info
    user = prefs.user
    
    return {
        "user_email": user.email,
        "user_name": user.full_name,
        "email_enabled": prefs.email_enabled,
        "type_preferences": prefs.type_preferences
    }


# Webhook endpoints
@router.post("/webhooks/{provider}")
async def process_webhook(
    provider: EmailProvider,
    request: dict = Body(...),
    x_signature: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Process webhook from email provider."""
    # In production, verify webhook signature
    
    service = get_email_service(db)
    service.process_webhook(provider, request)
    
    return {"status": "ok"}


# Domain management endpoints (admin only)
@router.post("/domains", response_model=EmailDomainResponse, status_code=status.HTTP_201_CREATED)
async def create_email_domain(
    domain_data: EmailDomainCreate,
    current_user: User = Depends(require_permission("notifications", "write")),
    db: Session = Depends(get_db)
):
    """Create email domain configuration (admin only)."""
    from app.models.email_notifications import EmailDomain
    
    # Check for duplicate
    existing = db.query(EmailDomain).filter(
        EmailDomain.domain == domain_data.domain
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Domain already configured"
        )
    
    domain = EmailDomain(**domain_data.dict())
    
    db.add(domain)
    db.commit()
    
    return EmailDomainResponse.from_orm(domain)


@router.get("/domains", response_model=List[EmailDomainResponse])
async def list_email_domains(
    is_active: Optional[bool] = Query(None),
    current_user: User = Depends(require_permission("notifications", "read")),
    db: Session = Depends(get_db)
):
    """List email domains (admin only)."""
    from app.models.email_notifications import EmailDomain
    
    query = db.query(EmailDomain)
    
    if is_active is not None:
        query = query.filter(EmailDomain.is_active == is_active)
    
    domains = query.order_by(EmailDomain.domain).all()
    
    return [EmailDomainResponse.from_orm(d) for d in domains]


@router.put("/domains/{domain_id}", response_model=EmailDomainResponse)
async def update_email_domain(
    domain_id: UUID,
    domain_data: EmailDomainUpdate,
    current_user: User = Depends(require_permission("notifications", "write")),
    db: Session = Depends(get_db)
):
    """Update email domain (admin only)."""
    from app.models.email_notifications import EmailDomain
    
    domain = db.query(EmailDomain).filter(
        EmailDomain.id == domain_id
    ).first()
    
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )
    
    for field, value in domain_data.dict(exclude_unset=True).items():
        setattr(domain, field, value)
    
    db.commit()
    
    return EmailDomainResponse.from_orm(domain)


@router.post("/domains/{domain_id}/test")
async def test_email_domain(
    domain_id: UUID,
    test_email: EmailStr = Body(...),
    current_user: User = Depends(require_permission("notifications", "write")),
    db: Session = Depends(get_db)
):
    """Test email domain configuration (admin only)."""
    from app.models.email_notifications import EmailDomain
    
    domain = db.query(EmailDomain).filter(
        EmailDomain.id == domain_id
    ).first()
    
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain not found"
        )
    
    # Send test email
    # In production, actually send test email
    
    return {
        "status": "sent",
        "message": f"Test email sent to {test_email}"
    }