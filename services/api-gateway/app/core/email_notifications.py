"""
Core Email Notification Service

Business logic for enhanced email notification functionality.
Implements FEAT-007 Email Notifications (P2 priority).
"""

from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import hashlib
import base64
import secrets
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_, and_, desc
from fastapi import HTTPException, status
from jinja2 import Template, Environment, BaseLoader
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from app.models.email_notifications import (
    EmailTemplate, NotificationPreference, EmailNotification,
    EmailEvent, EmailAttachment, EmailBatch, NotificationQueue,
    EmailProvider as EmailProviderModel,
    EmailStatus, NotificationType, NotificationPriority, EmailProvider
)
from app.models.users import User
from app.schemas.email_notifications import (
    EmailTemplateCreate, EmailTemplateUpdate,
    PreferenceUpdate, EmailNotificationCreate,
    EmailBatchCreate, EmailBatchUpdate,
    SendEmailRequest, SendBulkEmailRequest,
    AttachmentCreate, UnsubscribeRequest
)
from app.core.cache import cache_service
from app.config import settings
import logging
import asyncio
from collections import defaultdict

logger = logging.getLogger(__name__)


class EmailNotificationService:
    """Service for managing email notifications."""
    
    def __init__(self, db: Session):
        self.db = db
        self.jinja_env = Environment(loader=BaseLoader())
        self.providers = {}
        self._init_providers()
    
    def _init_providers(self):
        """Initialize email providers from database."""
        providers = self.db.query(EmailProviderModel).filter(
            EmailProviderModel.is_active == True
        ).all()
        
        for provider in providers:
            self.providers[provider.provider_type] = provider
    
    # Template management
    def create_template(self, template_data: EmailTemplateCreate) -> EmailTemplate:
        """Create email template."""
        # Check for existing template with same key
        existing = self.db.query(EmailTemplate).filter(
            EmailTemplate.template_key == template_data.template_key,
            EmailTemplate.is_active == True
        ).first()
        
        version = 1
        if existing:
            # Create new version
            max_version = self.db.query(func.max(EmailTemplate.version)).filter(
                EmailTemplate.template_key == template_data.template_key
            ).scalar()
            version = (max_version or 0) + 1
            
            # Deactivate old versions
            self.db.query(EmailTemplate).filter(
                EmailTemplate.template_key == template_data.template_key
            ).update({"is_active": False, "is_default": False})
        
        template = EmailTemplate(
            **template_data.dict(),
            version=version
        )
        
        # Validate template syntax
        try:
            self.jinja_env.from_string(template.subject_template)
            self.jinja_env.from_string(template.html_template)
            if template.text_template:
                self.jinja_env.from_string(template.text_template)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid template syntax: {str(e)}"
            )
        
        self.db.add(template)
        self.db.commit()
        
        logger.info(f"Created email template: {template.template_key} v{version}")
        return template
    
    def get_template(
        self,
        template_key: str,
        version: Optional[int] = None,
        language: str = "en"
    ) -> EmailTemplate:
        """Get email template by key."""
        query = self.db.query(EmailTemplate).filter(
            EmailTemplate.template_key == template_key,
            EmailTemplate.language == language
        )
        
        if version:
            query = query.filter(EmailTemplate.version == version)
        else:
            query = query.filter(EmailTemplate.is_active == True)
        
        template = query.first()
        
        if not template:
            # Try default language
            template = self.db.query(EmailTemplate).filter(
                EmailTemplate.template_key == template_key,
                EmailTemplate.is_active == True,
                EmailTemplate.language == "en"
            ).first()
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template not found: {template_key}"
            )
        
        return template
    
    # Preference management
    def get_or_create_preferences(self, user_id: UUID) -> NotificationPreference:
        """Get or create user notification preferences."""
        prefs = self.db.query(NotificationPreference).filter(
            NotificationPreference.user_id == user_id
        ).first()
        
        if not prefs:
            # Create default preferences
            prefs = NotificationPreference(
                user_id=user_id,
                unsubscribe_token=secrets.token_urlsafe(32),
                preferences={
                    "alert": {"enabled": True, "frequency": "realtime"},
                    "digest": {"enabled": True, "frequency": "daily"},
                    "announcement": {"enabled": True, "frequency": "immediate"}
                }
            )
            self.db.add(prefs)
            self.db.commit()
        
        return prefs
    
    def update_preferences(
        self,
        user_id: UUID,
        pref_data: PreferenceUpdate
    ) -> NotificationPreference:
        """Update user notification preferences."""
        prefs = self.get_or_create_preferences(user_id)
        
        for field, value in pref_data.dict(exclude_unset=True).items():
            if field == "preferences" and value:
                # Merge preferences
                current_prefs = prefs.preferences or {}
                for notif_type, settings in value.items():
                    current_prefs[notif_type] = settings.dict()
                prefs.preferences = current_prefs
            else:
                setattr(prefs, field, value)
        
        self.db.commit()
        return prefs
    
    # Send email
    async def send_email(self, request: SendEmailRequest, user: Optional[User] = None) -> List[EmailNotification]:
        """Send email to recipients."""
        notifications = []
        
        for recipient_email in request.to:
            # Check if user wants to receive emails
            if user:
                prefs = self.get_or_create_preferences(user.id)
                if not prefs.email_enabled:
                    logger.info(f"User {user.id} has disabled email notifications")
                    continue
            
            # Create notification record
            notification = EmailNotification(
                user_id=user.id if user else None,
                recipient_email=recipient_email,
                recipient_name=user.full_name if user else None,
                template_id=request.template_id,
                notification_type=NotificationType.CUSTOM,
                subject=request.subject,
                template_variables=request.template_variables,
                priority=request.priority,
                reference_id=request.reference_id,
                tags=request.tags,
                status=EmailStatus.PENDING
            )
            
            self.db.add(notification)
            notifications.append(notification)
            
            # Add attachments if provided
            if request.attachments:
                for attach_data in request.attachments:
                    content = base64.b64decode(attach_data.content_base64)
                    attachment = EmailAttachment(
                        notification_id=notification.id,
                        filename=attach_data.filename,
                        content_type=attach_data.content_type,
                        size_bytes=len(content),
                        content_base64=attach_data.content_base64,
                        checksum=hashlib.sha256(content).hexdigest()
                    )
                    self.db.add(attachment)
        
        self.db.flush()
        
        # Queue for sending
        for notification in notifications:
            queue_item = NotificationQueue(
                notification_id=notification.id,
                priority=self._get_priority_value(notification.priority),
                status="pending"
            )
            self.db.add(queue_item)
        
        self.db.commit()
        
        # Process immediately if high priority
        if request.priority in [NotificationPriority.HIGH, NotificationPriority.URGENT]:
            await self._process_notifications(notifications)
        
        return notifications
    
    async def send_templated_email(
        self,
        user: User,
        template_key: str,
        variables: Dict[str, Any],
        notification_type: NotificationType = NotificationType.CUSTOM,
        priority: NotificationPriority = NotificationPriority.MEDIUM
    ) -> EmailNotification:
        """Send templated email to user."""
        # Get user preferences
        prefs = self.get_or_create_preferences(user.id)
        
        # Check if user wants this type of notification
        pref_key = notification_type.value
        if pref_key in prefs.preferences:
            if not prefs.preferences[pref_key].get("enabled", True):
                logger.info(f"User {user.id} has disabled {notification_type} notifications")
                return None
        
        # Get template
        template = self.get_template(template_key)
        
        # Render subject and content
        subject = self._render_template(template.subject_template, variables)
        html_content = self._render_template(template.html_template, variables)
        text_content = None
        if template.text_template:
            text_content = self._render_template(template.text_template, variables)
        
        # Create notification
        notification = EmailNotification(
            user_id=user.id,
            recipient_email=user.email,
            recipient_name=user.full_name,
            template_id=template.id,
            notification_type=notification_type,
            subject=subject,
            template_variables=variables,
            priority=priority,
            status=EmailStatus.PENDING
        )
        
        self.db.add(notification)
        self.db.flush()
        
        # Queue for sending
        queue_item = NotificationQueue(
            notification_id=notification.id,
            priority=self._get_priority_value(priority),
            status="pending"
        )
        self.db.add(queue_item)
        
        self.db.commit()
        
        # Process immediately if urgent
        if priority == NotificationPriority.URGENT:
            await self._process_notifications([notification])
        
        logger.info(f"Queued templated email for user {user.id}: {template_key}")
        return notification
    
    # Batch operations
    def create_batch(
        self,
        batch_data: EmailBatchCreate,
        user: User
    ) -> EmailBatch:
        """Create email batch."""
        # Get template
        template = self.db.query(EmailTemplate).filter(
            EmailTemplate.id == batch_data.template_id
        ).first()
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )
        
        # Count recipients based on criteria
        recipient_count = self._count_batch_recipients(batch_data.recipient_criteria)
        
        batch = EmailBatch(
            **batch_data.dict(),
            recipient_count=recipient_count,
            created_by=user.id,
            status="draft"
        )
        
        self.db.add(batch)
        self.db.commit()
        
        logger.info(f"Created email batch: {batch.name} with {recipient_count} recipients")
        return batch
    
    async def send_batch(self, batch_id: UUID) -> EmailBatch:
        """Send email batch."""
        batch = self.db.query(EmailBatch).filter(
            EmailBatch.id == batch_id
        ).first()
        
        if not batch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Batch not found"
            )
        
        if batch.status not in ["draft", "scheduled"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot send batch in status: {batch.status}"
            )
        
        # Update status
        batch.status = "sending"
        batch.started_at = datetime.utcnow()
        self.db.commit()
        
        # Get recipients
        recipients = self._get_batch_recipients(batch.recipient_criteria)
        
        # Create notifications for each recipient
        notifications = []
        for user in recipients:
            # Check preferences
            prefs = self.get_or_create_preferences(user.id)
            if not prefs.email_enabled:
                continue
            
            # Create notification
            notification = EmailNotification(
                user_id=user.id,
                recipient_email=user.email,
                recipient_name=user.full_name,
                template_id=batch.template_id,
                notification_type=NotificationType.from_batch_type(batch.batch_type),
                subject="",  # Will be rendered from template
                template_variables={"batch_id": str(batch.id)},
                priority=NotificationPriority.LOW,
                status=EmailStatus.PENDING
            )
            
            self.db.add(notification)
            notifications.append(notification)
        
        self.db.flush()
        
        # Queue all notifications
        for notification in notifications:
            queue_item = NotificationQueue(
                notification_id=notification.id,
                priority=0,  # Low priority for batch
                status="pending"
            )
            self.db.add(queue_item)
        
        batch.recipient_count = len(notifications)
        self.db.commit()
        
        logger.info(f"Queued {len(notifications)} emails for batch: {batch.name}")
        return batch
    
    # Process queue
    async def process_queue(self, limit: int = 100) -> int:
        """Process pending notifications from queue."""
        # Get pending items
        queue_items = self.db.query(NotificationQueue).filter(
            NotificationQueue.status == "pending",
            or_(
                NotificationQueue.retry_after.is_(None),
                NotificationQueue.retry_after <= datetime.utcnow()
            )
        ).order_by(
            desc(NotificationQueue.priority),
            NotificationQueue.created_at
        ).limit(limit).all()
        
        if not queue_items:
            return 0
        
        # Mark as processing
        queue_ids = [item.id for item in queue_items]
        self.db.query(NotificationQueue).filter(
            NotificationQueue.id.in_(queue_ids)
        ).update({
            "status": "processing",
            "processor_id": f"worker-{uuid4()}"
        })
        self.db.commit()
        
        # Process notifications
        processed = 0
        for queue_item in queue_items:
            try:
                notification = queue_item.notification
                await self._send_notification(notification)
                
                # Mark as completed
                queue_item.status = "completed"
                queue_item.processed_at = datetime.utcnow()
                processed += 1
                
            except Exception as e:
                logger.error(f"Failed to send notification {queue_item.notification_id}: {str(e)}")
                
                # Handle retry
                queue_item.retry_count += 1
                if queue_item.retry_count < 3:
                    queue_item.status = "pending"
                    queue_item.retry_after = datetime.utcnow() + timedelta(
                        minutes=5 * queue_item.retry_count
                    )
                else:
                    queue_item.status = "failed"
                    notification.status = EmailStatus.FAILED
                    notification.error_message = str(e)
        
        self.db.commit()
        
        logger.info(f"Processed {processed} notifications from queue")
        return processed
    
    # Unsubscribe
    def unsubscribe(self, request: UnsubscribeRequest) -> Dict[str, Any]:
        """Process unsubscribe request."""
        # Find preference by token
        prefs = self.db.query(NotificationPreference).filter(
            NotificationPreference.unsubscribe_token == request.token
        ).first()
        
        if not prefs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid unsubscribe token"
            )
        
        unsubscribed_types = []
        
        if request.notification_types:
            # Unsubscribe from specific types
            for notif_type in request.notification_types:
                if notif_type.value in prefs.preferences:
                    prefs.preferences[notif_type.value]["enabled"] = False
                    unsubscribed_types.append(notif_type.value)
        else:
            # Unsubscribe from all
            prefs.email_enabled = False
            unsubscribed_types.append("all")
        
        self.db.commit()
        
        logger.info(f"User {prefs.user_id} unsubscribed from: {unsubscribed_types}")
        
        return {
            "success": True,
            "message": "Successfully unsubscribed",
            "unsubscribed_types": unsubscribed_types
        }
    
    # Analytics
    def get_analytics(
        self,
        start_date: datetime,
        end_date: datetime,
        user_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """Get email analytics."""
        query = self.db.query(EmailNotification).filter(
            EmailNotification.created_at >= start_date,
            EmailNotification.created_at <= end_date
        )
        
        if user_id:
            query = query.filter(EmailNotification.user_id == user_id)
        
        notifications = query.all()
        
        # Calculate metrics
        total_sent = len([n for n in notifications if n.status in [
            EmailStatus.SENT, EmailStatus.DELIVERED
        ]])
        total_delivered = len([n for n in notifications if n.status == EmailStatus.DELIVERED])
        total_opened = len([n for n in notifications if n.opened_at])
        total_clicked = len([n for n in notifications if n.clicked_at])
        total_bounced = len([n for n in notifications if n.status == EmailStatus.BOUNCED])
        total_complained = len([n for n in notifications if n.status == EmailStatus.COMPLAINED])
        
        # Calculate rates
        delivery_rate = (total_delivered / total_sent * 100) if total_sent > 0 else 0
        open_rate = (total_opened / total_delivered * 100) if total_delivered > 0 else 0
        click_rate = (total_clicked / total_opened * 100) if total_opened > 0 else 0
        bounce_rate = (total_bounced / total_sent * 100) if total_sent > 0 else 0
        complaint_rate = (total_complained / total_delivered * 100) if total_delivered > 0 else 0
        
        # By type breakdown
        by_type = defaultdict(lambda: {
            "sent": 0, "delivered": 0, "opened": 0, "clicked": 0
        })
        
        for notification in notifications:
            notif_type = notification.notification_type.value
            if notification.status in [EmailStatus.SENT, EmailStatus.DELIVERED]:
                by_type[notif_type]["sent"] += 1
            if notification.status == EmailStatus.DELIVERED:
                by_type[notif_type]["delivered"] += 1
            if notification.opened_at:
                by_type[notif_type]["opened"] += 1
            if notification.clicked_at:
                by_type[notif_type]["clicked"] += 1
        
        return {
            "period": f"{start_date.date()} to {end_date.date()}",
            "total_sent": total_sent,
            "total_delivered": total_delivered,
            "total_opened": total_opened,
            "total_clicked": total_clicked,
            "total_bounced": total_bounced,
            "total_complained": total_complained,
            "delivery_rate": round(delivery_rate, 2),
            "open_rate": round(open_rate, 2),
            "click_rate": round(click_rate, 2),
            "bounce_rate": round(bounce_rate, 2),
            "complaint_rate": round(complaint_rate, 2),
            "by_type": dict(by_type)
        }
    
    # Helper methods
    def _render_template(self, template_str: str, variables: Dict[str, Any]) -> str:
        """Render Jinja2 template with variables."""
        template = self.jinja_env.from_string(template_str)
        
        # Add default variables
        default_vars = {
            "app_name": "OpenPolicy",
            "app_url": settings.APP_URL,
            "current_year": datetime.utcnow().year
        }
        
        return template.render(**{**default_vars, **variables})
    
    def _get_priority_value(self, priority: NotificationPriority) -> int:
        """Convert priority enum to numeric value."""
        priority_map = {
            NotificationPriority.LOW: 0,
            NotificationPriority.MEDIUM: 5,
            NotificationPriority.HIGH: 10,
            NotificationPriority.URGENT: 15
        }
        return priority_map.get(priority, 5)
    
    def _count_batch_recipients(self, criteria: Dict[str, Any]) -> int:
        """Count recipients based on criteria."""
        query = self.db.query(User).filter(User.is_active == True)
        
        # Apply filters based on criteria
        # This is simplified - in production would be more complex
        
        return query.count()
    
    def _get_batch_recipients(self, criteria: Dict[str, Any]) -> List[User]:
        """Get recipients based on criteria."""
        query = self.db.query(User).filter(User.is_active == True)
        
        # Apply filters based on criteria
        # This is simplified - in production would be more complex
        
        return query.all()
    
    async def _process_notifications(self, notifications: List[EmailNotification]):
        """Process notifications immediately."""
        for notification in notifications:
            try:
                await self._send_notification(notification)
            except Exception as e:
                logger.error(f"Failed to send notification {notification.id}: {str(e)}")
                notification.status = EmailStatus.FAILED
                notification.error_message = str(e)
        
        self.db.commit()
    
    async def _send_notification(self, notification: EmailNotification):
        """Send individual notification."""
        try:
            # Update status
            notification.status = EmailStatus.SENDING
            notification.attempts += 1
            notification.last_attempt_at = datetime.utcnow()
            self.db.commit()
            
            # Prepare content
            if notification.template_id:
                template = notification.template
                subject = self._render_template(
                    template.subject_template,
                    notification.template_variables or {}
                )
                html_content = self._render_template(
                    template.html_template,
                    notification.template_variables or {}
                )
                text_content = None
                if template.text_template:
                    text_content = self._render_template(
                        template.text_template,
                        notification.template_variables or {}
                    )
            else:
                subject = notification.subject
                html_content = notification.template_variables.get("html_content", "")
                text_content = notification.template_variables.get("text_content", "")
            
            # Get provider
            provider = self._get_best_provider()
            
            # Send based on provider type
            if provider.provider_type == EmailProvider.SMTP:
                await self._send_smtp_email(
                    provider,
                    notification.recipient_email,
                    subject,
                    html_content,
                    text_content,
                    notification.attachments
                )
            else:
                # Other providers would be implemented here
                raise NotImplementedError(f"Provider {provider.provider_type} not implemented")
            
            # Update status
            notification.status = EmailStatus.SENT
            notification.sent_at = datetime.utcnow()
            notification.provider = provider.provider_type
            
            # Log event
            event = EmailEvent(
                notification_id=notification.id,
                event_type="sent",
                event_data={"provider": provider.provider_type.value}
            )
            self.db.add(event)
            
            # Update provider stats
            provider.total_sent += 1
            provider.last_used_at = datetime.utcnow()
            
            self.db.commit()
            
            logger.info(f"Sent email {notification.id} via {provider.provider_type}")
            
        except Exception as e:
            logger.error(f"Failed to send email {notification.id}: {str(e)}")
            notification.status = EmailStatus.FAILED
            notification.error_message = str(e)
            
            if hasattr(provider, 'total_failed'):
                provider.total_failed += 1
            
            self.db.commit()
            raise
    
    def _get_best_provider(self) -> EmailProviderModel:
        """Get best available email provider."""
        # For now, return default provider
        default_provider = self.db.query(EmailProviderModel).filter(
            EmailProviderModel.is_default == True,
            EmailProviderModel.is_active == True
        ).first()
        
        if not default_provider:
            # Return first active provider
            default_provider = self.db.query(EmailProviderModel).filter(
                EmailProviderModel.is_active == True
            ).first()
        
        if not default_provider:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No email providers configured"
            )
        
        return default_provider
    
    async def _send_smtp_email(
        self,
        provider: EmailProviderModel,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str],
        attachments: List[EmailAttachment]
    ):
        """Send email via SMTP."""
        config = provider.config
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = config.get('from_email', 'noreply@openpolicy.ca')
        msg['To'] = to_email
        
        # Add text and HTML parts
        if text_content:
            text_part = MIMEText(text_content, 'plain')
            msg.attach(text_part)
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Add attachments
        for attachment in attachments:
            if attachment.content_base64:
                content = base64.b64decode(attachment.content_base64)
                
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(content)
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{attachment.filename}"'
                )
                msg.attach(part)
        
        # Send email
        with smtplib.SMTP(config['host'], config['port']) as server:
            if config.get('use_tls'):
                server.starttls()
            if config.get('username'):
                server.login(config['username'], config['password'])
            
            server.send_message(msg)


# Dependency injection helper
def get_email_notification_service(db: Session) -> EmailNotificationService:
    """Get email notification service instance."""
    return EmailNotificationService(db)