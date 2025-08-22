"""
Email Alert System API for OpenPolicy V2

Comprehensive email notification system for parliamentary updates and user engagement.
This implements a P1 priority feature identified in the priority analysis.
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Path, Body
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_
from typing import Optional
from datetime import datetime, timedelta
import math
import secrets

from app.database import get_db
from app.models.email_alerts import EmailAlert, EmailTemplate, EmailCampaign, UnsubscribeToken
from app.models.users import User
from app.schemas.email_alerts import (
    EmailAlertResponse, EmailTemplateResponse, EmailCampaignResponse,
    EmailAlertListResponse, EmailTemplateListResponse, EmailCampaignListResponse,
    EmailAnalyticsResponse, EmailAlertStatsResponse, EmailNotificationResponse,
    EmailAlertCreateRequest, EmailAlertUpdateRequest, EmailTemplateCreateRequest, EmailTemplateUpdateRequest,
    EmailCampaignCreateRequest, EmailCampaignUpdateRequest,
    EmailNotificationRequest, NotificationContent
)
from app.api.v1.auth import get_current_user
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter()


# ============================================================================
# EMAIL ALERTS
# ============================================================================

@router.post("/alerts", response_model=EmailAlertResponse)
async def create_email_alert(
    alert_data: EmailAlertCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new email alert subscription.
    
    Users can subscribe to various types of parliamentary updates.
    """
    # Check if user already has this alert type
    existing_alert = db.query(EmailAlert).filter(
        and_(
            EmailAlert.user_id == current_user.id,
            EmailAlert.alert_type == alert_data.alert_type
        )
    ).first()
    
    if existing_alert:
        raise HTTPException(
            status_code=400,
            detail=f"User already has an active {alert_data.alert_type} alert"
        )
    
    # Create new alert
    alert = EmailAlert(
        user_id=current_user.id,
        alert_type=alert_data.alert_type,
        frequency=alert_data.frequency,
        is_active=alert_data.is_active,
        include_summary=alert_data.include_summary,
        include_links=alert_data.include_links,
        include_analytics=alert_data.include_analytics,
        filters=alert_data.filters
    )
    
    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    logger.info(f"Email alert created: {current_user.username} - {alert_data.alert_type}")
    
    return EmailAlertResponse(
        id=str(alert.id),
        user_id=str(alert.user_id),
        alert_type=alert.alert_type,
        frequency=alert.frequency,
        is_active=alert.is_active,
        include_summary=alert.include_summary,
        include_links=alert.include_links,
        include_analytics=alert.include_analytics,
        filters=alert.filters,
        created_at=alert.created_at,
        updated_at=alert.updated_at,
        last_sent=alert.last_sent
    )


@router.get("/alerts", response_model=EmailAlertListResponse)
async def list_user_alerts(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    alert_type: Optional[str] = Query(None, description="Filter by alert type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all email alerts for the current user.
    """
    # Build base query
    query = db.query(EmailAlert).filter(EmailAlert.user_id == current_user.id)
    
    # Apply filters
    if alert_type:
        query = query.filter(EmailAlert.alert_type == alert_type)
    
    if is_active is not None:
        query = query.filter(EmailAlert.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get alerts
    alerts = query.order_by(EmailAlert.created_at.desc()).offset(offset).limit(page_size).all()
    
    # Convert to response format
    alert_responses = []
    for alert in alerts:
        alert_responses.append(EmailAlertResponse(
            id=str(alert.id),
            user_id=str(alert.user_id),
            alert_type=alert.alert_type,
            frequency=alert.frequency,
            is_active=alert.is_active,
            include_summary=alert.include_summary,
            include_links=alert.include_links,
            include_analytics=alert.include_analytics,
            filters=alert.filters,
            created_at=alert.created_at,
            updated_at=alert.updated_at,
            last_sent=alert.last_sent
        ))
    
    return EmailAlertListResponse(
        alerts=alert_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


@router.get("/alerts/{alert_id}", response_model=EmailAlertResponse)
async def get_email_alert(
    alert_id: str = Path(..., description="Alert ID"),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific email alert by ID.
    
    Users can only view their own alerts.
    """
    alert = db.query(EmailAlert).filter(
        and_(
            EmailAlert.id == alert_id,
            EmailAlert.user_id == current_user.id
        )
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Email alert not found")
    
    return EmailAlertResponse(
        id=str(alert.id),
        user_id=str(alert.user_id),
        alert_type=alert.alert_type,
        frequency=alert.frequency,
        is_active=alert.is_active,
        include_summary=alert.include_summary,
        include_links=alert.include_links,
        include_analytics=alert.include_analytics,
        filters=alert.filters,
        created_at=alert.created_at,
        updated_at=alert.updated_at,
        last_sent=alert.last_sent
    )


@router.put("/alerts/{alert_id}", response_model=EmailAlertResponse)
async def update_email_alert(
    alert_id: str = Path(..., description="Alert ID"),
    alert_data: EmailAlertUpdateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an email alert.
    
    Users can only update their own alerts.
    """
    alert = db.query(EmailAlert).filter(
        and_(
            EmailAlert.id == alert_id,
            EmailAlert.user_id == current_user.id
        )
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Email alert not found")
    
    # Update alert fields
    update_data = alert_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(alert, field):
            setattr(alert, field, value)
    
    alert.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(alert)
    
    logger.info(f"Email alert updated: {current_user.username} - {alert.alert_type}")
    
    return EmailAlertResponse(
        id=str(alert.id),
        user_id=str(alert.user_id),
        alert_type=alert.alert_type,
        frequency=alert.frequency,
        is_active=alert.is_active,
        include_summary=alert.include_summary,
        include_links=alert.include_links,
        include_analytics=alert.include_analytics,
        filters=alert.filters,
        created_at=alert.created_at,
        updated_at=alert.updated_at,
        last_sent=alert.last_sent
    )


@router.delete("/alerts/{alert_id}")
async def delete_email_alert(
    alert_id: str = Path(..., description="Alert ID"),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an email alert.
    
    Users can only delete their own alerts.
    """
    alert = db.query(EmailAlert).filter(
        and_(
            EmailAlert.id == alert_id,
            EmailAlert.user_id == current_user.id
        )
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="Email alert not found")
    
    db.delete(alert)
    db.commit()
    
    logger.info(f"Email alert deleted: {current_user.username} - {alert.alert_type}")
    
    return {"message": "Email alert deleted successfully"}


# ============================================================================
# EMAIL TEMPLATES
# ============================================================================

@router.get("/templates", response_model=EmailTemplateListResponse)
async def list_email_templates(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    template_type: Optional[str] = Query(None, description="Filter by template type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List email templates.
    
    Only active templates are returned.
    """
    # Build base query
    query = db.query(EmailTemplate).filter(EmailTemplate.is_active == True)
    
    # Apply filters
    if template_type:
        query = query.filter(EmailTemplate.template_type == template_type)
    
    if is_active is not None:
        query = query.filter(EmailTemplate.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get templates
    templates = query.order_by(EmailTemplate.template_name).offset(offset).limit(page_size).all()
    
    # Convert to response format
    template_responses = []
    for template in templates:
        template_responses.append(EmailTemplateResponse(
            id=str(template.id),
            template_name=template.template_name,
            template_type=template.template_type,
            subject_template=template.subject_template,
            html_template=template.html_template,
            text_template=template.text_template,
            description=template.description,
            variables=template.variables,
            is_active=template.is_active,
            created_at=template.created_at,
            updated_at=template.updated_at
        ))
    
    return EmailTemplateListResponse(
        templates=template_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


@router.get("/templates/{template_id}", response_model=EmailTemplateResponse)
async def get_email_template(
    template_id: str = Path(..., description="Template ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific email template by ID.
    """
    template = db.query(EmailTemplate).filter(
        and_(
            EmailTemplate.id == template_id,
            EmailTemplate.is_active == True
        )
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="Email template not found")
    
    return EmailTemplateResponse(
        id=str(template.id),
        template_name=template.template_name,
        template_type=template.template_type,
        subject_template=template.subject_template,
        html_template=template.html_template,
        text_template=template.text_template,
        description=template.description,
        variables=template.variables,
        is_active=template.is_active,
        created_at=template.created_at,
        updated_at=template.updated_at
    )


# ============================================================================
# EMAIL CAMPAIGNS
# ============================================================================

@router.post("/campaigns", response_model=EmailCampaignResponse)
async def create_email_campaign(
    campaign_data: EmailCampaignCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new email campaign.
    
    This is typically used by administrators for bulk communications.
    """
    # Create new campaign
    campaign = EmailCampaign(
        campaign_name=campaign_data.campaign_name,
        campaign_type=campaign_data.campaign_type,
        subject=campaign_data.subject,
        html_content=campaign_data.html_content,
        text_content=campaign_data.text_content,
        target_audience=campaign_data.target_audience,
        scheduled_at=campaign_data.scheduled_at,
        is_active=campaign_data.is_active
    )
    
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    
    logger.info(f"Email campaign created: {current_user.username} - {campaign_data.campaign_name}")
    
    return EmailCampaignResponse(
        id=str(campaign.id),
        campaign_name=campaign.campaign_name,
        campaign_type=campaign.campaign_type,
        subject=campaign.subject,
        html_content=campaign.html_content,
        text_content=campaign.text_content,
        target_audience=campaign.target_audience,
        scheduled_at=campaign.scheduled_at,
        is_active=campaign.is_active,
        total_recipients=campaign.total_recipients,
        sent_count=campaign.sent_count,
        delivered_count=campaign.delivered_count,
        opened_count=campaign.opened_count,
        clicked_count=campaign.clicked_count,
        bounced_count=campaign.bounced_count,
        created_at=campaign.created_at,
        updated_at=campaign.updated_at,
        started_at=campaign.started_at,
        completed_at=campaign.completed_at
    )


@router.get("/campaigns", response_model=EmailCampaignListResponse)
async def list_email_campaigns(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    campaign_type: Optional[str] = Query(None, description="Filter by campaign type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List email campaigns.
    """
    # Build base query
    query = db.query(EmailCampaign)
    
    # Apply filters
    if campaign_type:
        query = query.filter(EmailCampaign.campaign_type == campaign_type)
    
    if is_active is not None:
        query = query.filter(EmailCampaign.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get campaigns
    campaigns = query.order_by(EmailCampaign.created_at.desc()).offset(offset).limit(page_size).all()
    
    # Convert to response format
    campaign_responses = []
    for campaign in campaigns:
        campaign_responses.append(EmailCampaignResponse(
            id=str(campaign.id),
            campaign_name=campaign.campaign_name,
            campaign_type=campaign.campaign_type,
            subject=campaign.subject,
            html_content=campaign.html_content,
            text_content=campaign.text_content,
            target_audience=campaign.target_audience,
            scheduled_at=campaign.scheduled_at,
            is_active=campaign.is_active,
            total_recipients=campaign.total_recipients,
            sent_count=campaign.sent_count,
            delivered_count=campaign.delivered_count,
            opened_count=campaign.opened_count,
            clicked_count=campaign.clicked_count,
            bounced_count=campaign.bounced_count,
            created_at=campaign.created_at,
            updated_at=campaign.updated_at,
            started_at=campaign.started_at,
            completed_at=campaign.completed_at
        ))
    
    return EmailCampaignListResponse(
        campaigns=campaign_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


# ============================================================================
# EMAIL ANALYTICS
# ============================================================================

@router.get("/analytics", response_model=EmailAnalyticsResponse)
async def get_email_analytics(
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get comprehensive email analytics.
    
    This provides insights into email performance and engagement.
    """
    # Build base query
    query = db.query(EmailLog)
    
    # Apply date filters
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
            query = query.filter(EmailLog.created_at >= date_from_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
            query = query.filter(EmailLog.created_at <= date_to_obj)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    # Get email counts by status
    total_sent = query.filter(EmailLog.status.in_(["sent", "delivered", "opened", "clicked"])).count()
    total_delivered = query.filter(EmailLog.status.in_(["delivered", "opened", "clicked"])).count()
    total_opened = query.filter(EmailLog.status == "opened").count()
    total_clicked = query.filter(EmailLog.status == "clicked").count()
    total_bounced = query.filter(EmailLog.status == "bounced").count()
    total_failed = query.filter(EmailLog.status == "failed").count()
    
    # Calculate rates
    delivery_rate = (total_delivered / total_sent * 100) if total_sent > 0 else 0
    open_rate = (total_opened / total_delivered * 100) if total_delivered > 0 else 0
    click_rate = (total_clicked / total_delivered * 100) if total_delivered > 0 else 0
    bounce_rate = (total_bounced / total_sent * 100) if total_sent > 0 else 0
    
    # Get time-based analytics (last 30 days if no date range specified)
    if not date_from and not date_to:
        date_from_obj = datetime.utcnow() - timedelta(days=30)
        date_to_obj = datetime.utcnow()
    else:
        date_from_obj = date_from_obj if date_from else datetime.utcnow() - timedelta(days=30)
        date_to_obj = date_to_obj if date_to else datetime.utcnow()
    
    # Get emails by day
    emails_by_day = {}
    opens_by_day = {}
    clicks_by_day = {}
    
    current_date = date_from_obj
    while current_date <= date_to_obj:
        date_str = current_date.strftime("%Y-%m-%d")
        emails_by_day[date_str] = 0
        opens_by_day[date_str] = 0
        clicks_by_day[date_str] = 0
        current_date += timedelta(days=1)
    
    # Get campaign performance
    campaign_performance = []
    campaigns = db.query(EmailCampaign).filter(EmailCampaign.is_active == True).all()
    
    for campaign in campaigns:
        campaign_logs = query.filter(EmailCampaign.id == campaign.id).all()
        if campaign_logs:
            campaign_performance.append({
                "campaign_id": str(campaign.id),
                "campaign_name": campaign.campaign_name,
                "total_sent": len(campaign_logs),
                "delivered": len([log for log in campaign_logs if log.status in ["delivered", "opened", "clicked"]]),
                "opened": len([log for log in campaign_logs if log.status == "opened"]),
                "clicked": len([log for log in campaign_logs if log.status == "clicked"]),
                "bounced": len([log for log in campaign_logs if log.status == "bounced"])
            })
    
    return EmailAnalyticsResponse(
        total_emails_sent=total_sent,
        total_emails_delivered=total_delivered,
        total_emails_opened=total_opened,
        total_emails_clicked=total_clicked,
        total_emails_bounced=total_bounced,
        total_emails_failed=total_failed,
        delivery_rate=round(delivery_rate, 2),
        open_rate=round(open_rate, 2),
        click_rate=round(click_rate, 2),
        bounce_rate=round(bounce_rate, 2),
        emails_by_day=emails_by_day,
        opens_by_day=opens_by_day,
        clicks_by_day=clicks_by_day,
        campaign_performance=campaign_performance,
        generated_at=datetime.utcnow()
    )


@router.get("/alerts/stats", response_model=EmailAlertStatsResponse)
async def get_user_alert_stats(
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get email alert statistics for the current user.
    """
    # Get user's alerts
    user_alerts = db.query(EmailAlert).filter(
        and_(
            EmailAlert.user_id == current_user.id,
            EmailAlert.is_active == True
        )
    ).all()
    
    # Get user's email logs
    user_logs = db.query(EmailLog).filter(EmailLog.user_id == current_user.id).all()
    
    # Calculate statistics
    total_alerts = len(user_alerts)
    alerts_by_type = {}
    alerts_by_frequency = {}
    
    for alert in user_alerts:
        alerts_by_type[alert.alert_type] = alerts_by_type.get(alert.alert_type, 0) + 1
        alerts_by_frequency[alert.frequency] = alerts_by_frequency.get(alert.frequency, 0) + 1
    
    # Get last alert sent
    last_alert_sent = None
    if user_alerts:
        last_alert_sent = max([alert.last_sent for alert in user_alerts if alert.last_sent])
    
    # Calculate email engagement
    total_emails_received = len(user_logs)
    emails_opened = len([log for log in user_logs if log.status == "opened"])
    emails_clicked = len([log for log in user_logs if log.status == "clicked"])
    engagement_rate = (emails_opened / total_emails_received * 100) if total_emails_received > 0 else 0
    
    return EmailAlertStatsResponse(
        user_id=str(current_user.id),
        total_alerts=total_alerts,
        alerts_by_type=alerts_by_type,
        alerts_by_frequency=alerts_by_frequency,
        last_alert_sent=last_alert_sent,
        total_emails_received=total_emails_received,
        emails_opened=emails_opened,
        emails_clicked=emails_clicked,
        engagement_rate=round(engagement_rate, 2),
        generated_at=datetime.utcnow()
    )


# ============================================================================
# EMAIL NOTIFICATIONS
# ============================================================================

@router.post("/notifications/send", response_model=EmailNotificationResponse)
async def send_email_notification(
    notification_data: EmailNotificationRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Send an email notification.
    
    This endpoint is used to trigger immediate email notifications.
    """
    # Get user
    user = db.query(User).filter(User.id == notification_data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's email alert preferences
    alert = db.query(EmailAlert).filter(
        and_(
            EmailAlert.user_id == notification_data.user_id,
            EmailAlert.alert_type == notification_data.alert_type,
            EmailAlert.is_active == True
        )
    ).first()
    
    if not alert:
        raise HTTPException(status_code=400, detail="User does not have active alerts for this type")
    
    # Get appropriate template
    template = db.query(EmailTemplate).filter(
        and_(
            EmailTemplate.template_type == notification_data.alert_type,
            EmailTemplate.is_active == True
        )
    ).first()
    
    if not template:
        # Use default template
        template = db.query(EmailTemplate).filter(
            and_(
                EmailTemplate.template_name == "default",
                EmailTemplate.is_active == True
            )
        ).first()
    
    try:
        # In a real implementation, this would send the actual email
        # For now, we'll just log it and create a log entry
        
        # Create email log entry
        email_log = EmailLog(
            user_id=notification_data.user_id,
            email_type="alert",
            recipient_email=user.email,
            subject=f"OpenPolicy Update: {notification_data.content.title}",
            status="sent",
            sent_at=datetime.utcnow()
        )
        
        db.add(email_log)
        db.commit()
        
        logger.info(f"Email notification sent: {user.email} - {notification_data.content.title}")
        
        return EmailNotificationResponse(
            success=True,
            message_id=str(email_log.id),
            sent_at=email_log.sent_at
        )
        
    except Exception as e:
        logger.error(f"Failed to send email notification: {str(e)}")
        
        # Create failed log entry
        email_log = EmailLog(
            user_id=notification_data.user_id,
            email_type="alert",
            recipient_email=user.email,
            subject=f"OpenPolicy Update: {notification_data.content.title}",
            status="failed",
            error_message=str(e)
        )
        
        db.add(email_log)
        db.commit()
        
        return EmailNotificationResponse(
            success=False,
            error_message=str(e),
            sent_at=datetime.utcnow()
        )


# ============================================================================
# UNSUBSCRIBE MANAGEMENT
# ============================================================================

@router.post("/unsubscribe/generate")
async def generate_unsubscribe_token(
    alert_type: Optional[str] = Body(None, description="Specific alert type to unsubscribe from"),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate an unsubscribe token for the current user.
    """
    # Generate unique token
    token = secrets.token_urlsafe(32)
    
    # Create unsubscribe token
    unsubscribe_token = UnsubscribeToken(
        user_id=current_user.id,
        email=current_user.email,
        token=token,
        alert_type=alert_type,
        expires_at=datetime.utcnow() + timedelta(days=30)  # 30 day expiration
    )
    
    db.add(unsubscribe_token)
    db.commit()
    
    # In a real implementation, this would send an email with the unsubscribe link
    unsubscribe_url = f"https://openpolicy.ca/unsubscribe?token={token}"
    
    logger.info(f"Unsubscribe token generated: {current_user.email} - {token}")
    
    return {
        "message": "Unsubscribe token generated successfully",
        "unsubscribe_url": unsubscribe_url,
        "expires_at": unsubscribe_token.expires_at.isoformat()
    }


@router.post("/unsubscribe/{token}")
async def unsubscribe_user(
    token: str = Path(..., description="Unsubscribe token"),
    db: DBSession = Depends(get_db)
):
    """
    Unsubscribe a user using a token.
    """
    # Find the unsubscribe token
    unsubscribe_token = db.query(UnsubscribeToken).filter(
        and_(
            UnsubscribeToken.token == token,
            UnsubscribeToken.is_active == True,
            UnsubscribeToken.used_at.is_(None)
        )
    ).first()
    
    if not unsubscribe_token:
        raise HTTPException(status_code=400, detail="Invalid or expired unsubscribe token")
    
    # Check if token has expired
    if unsubscribe_token.expires_at and unsubscribe_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Unsubscribe token has expired")
    
    # Mark token as used
    unsubscribe_token.used_at = datetime.utcnow()
    unsubscribe_token.is_active = False
    
    # Handle unsubscribe based on token type
    if unsubscribe_token.alert_type:
        # Unsubscribe from specific alert type
        alert = db.query(EmailAlert).filter(
            and_(
                EmailAlert.user_id == unsubscribe_token.user_id,
                EmailAlert.alert_type == unsubscribe_token.alert_type
            )
        ).first()
        
        if alert:
            alert.is_active = False
            alert.updated_at = datetime.utcnow()
    else:
        # Unsubscribe from all alerts
        alerts = db.query(EmailAlert).filter(
            and_(
                EmailAlert.user_id == unsubscribe_token.user_id,
                EmailAlert.is_active == True
            )
        ).all()
        
        for alert in alerts:
            alert.is_active = False
            alert.updated_at = datetime.utcnow()
    
    db.commit()
    
    logger.info(f"User unsubscribed: {unsubscribe_token.email} - {unsubscribe_token.alert_type or 'all'}")
    
    return {
        "message": "Successfully unsubscribed",
        "unsubscribed_from": unsubscribe_token.alert_type or "all alerts"
    }
