"""
Core Email Notification Service

Business logic for email notification functionality.
Implements FEAT-007 Email Notifications (P2 priority).
"""

from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import hashlib
import secrets
from jinja2 import Template, Environment, BaseLoader
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_, and_, desc
from fastapi import HTTPException, status
from app.models.email_notifications import (
    EmailTemplate, NotificationPreference, EmailNotification,
    EmailBatch, EmailAttachment, EmailLog, EmailDomain,
    NotificationType, EmailStatus, EmailProvider
)
from app.models.users import User
from app.schemas.email_notifications import (
    EmailTemplateCreate, EmailTemplateUpdate,
    NotificationPreferenceUpdate,
    EmailNotificationCreate, EmailBatchCreate,
    SendEmailRequest, SendBulkEmailRequest,
    PreviewEmailRequest, EmailAttachmentCreate
)
import logging
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
import smtplib
import boto3
import requests

logger = logging.getLogger(__name__)


class EmailNotificationService:
    """Service for managing email notifications."""
    
    def __init__(self, db: Session):
        self.db = db
        self.jinja_env = Environment(loader=BaseLoader())
        self.providers = {}
        self._init_providers()
    
    def _init_providers(self):
        """Initialize email providers."""
        # Get active domains
        domains = self.db.query(EmailDomain).filter(
            EmailDomain.is_active == True
        ).all()
        
        for domain in domains:
            if domain.provider == EmailProvider.SMTP:
                self.providers[domain.id] = SMTPProvider(domain.provider_config)
            elif domain.provider == EmailProvider.AWS_SES:
                self.providers[domain.id] = AWSProvider(domain.provider_config)
            elif domain.provider == EmailProvider.SENDGRID:
                self.providers[domain.id] = SendGridProvider(domain.provider_config)
            # Add more providers as needed
    
    # Template management
    def create_template(
        self,
        template_data: EmailTemplateCreate
    ) -> EmailTemplate:
        """Create email template."""
        # Generate slug
        slug = self._generate_slug(template_data.name)
        
        # Check for duplicate
        existing = self.db.query(EmailTemplate).filter(
            EmailTemplate.slug == slug
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Template with this name already exists"
            )
        
        template = EmailTemplate(
            **template_data.dict(),
            slug=slug
        )
        
        self.db.add(template)
        self.db.commit()
        
        logger.info(f"Created email template: {template.name}")
        return template
    
    def get_template(
        self,
        template_id: UUID
    ) -> EmailTemplate:
        """Get email template by ID."""
        template = self.db.query(EmailTemplate).filter(
            EmailTemplate.id == template_id
        ).first()
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )
        
        return template
    
    def update_template(
        self,
        template_id: UUID,
        template_data: EmailTemplateUpdate
    ) -> EmailTemplate:
        """Update email template."""
        template = self.get_template(template_id)
        
        # Don't allow updating system templates
        if template.is_system:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot modify system templates"
            )
        
        for field, value in template_data.dict(exclude_unset=True).items():
            setattr(template, field, value)
        
        self.db.commit()
        return template
    
    def list_templates(
        self,
        notification_type: Optional[NotificationType] = None,
        is_active: bool = True
    ) -> List[EmailTemplate]:
        """List email templates."""
        query = self.db.query(EmailTemplate)
        
        if notification_type:
            query = query.filter(EmailTemplate.notification_type == notification_type)
        
        query = query.filter(EmailTemplate.is_active == is_active)
        
        return query.order_by(EmailTemplate.name).all()
    
    # Preference management
    def get_or_create_preferences(
        self,
        user_id: UUID
    ) -> NotificationPreference:
        """Get or create user notification preferences."""
        prefs = self.db.query(NotificationPreference).filter(
            NotificationPreference.user_id == user_id
        ).first()
        
        if not prefs:
            # Create default preferences
            prefs = NotificationPreference(
                user_id=user_id,
                unsubscribe_token=secrets.token_urlsafe(32),
                type_preferences=self._get_default_type_preferences()
            )
            self.db.add(prefs)
            self.db.commit()
        
        return prefs
    
    def update_preferences(
        self,
        user_id: UUID,
        pref_data: NotificationPreferenceUpdate
    ) -> NotificationPreference:
        """Update user notification preferences."""
        prefs = self.get_or_create_preferences(user_id)
        
        for field, value in pref_data.dict(exclude_unset=True).items():
            if field == 'type_preferences' and value:
                # Merge type preferences
                current = prefs.type_preferences or {}
                for notif_type, pref in value.items():
                    current[notif_type.value] = pref.dict()
                prefs.type_preferences = current
            else:
                setattr(prefs, field, value)
        
        self.db.commit()
        return prefs
    
    # Send email
    async def send_email(
        self,
        request: SendEmailRequest
    ) -> EmailNotification:
        """Send single email notification."""
        # Get user
        user = self.db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check preferences
        prefs = self.get_or_create_preferences(user.id)
        if not prefs.email_enabled:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User has disabled email notifications"
            )
        
        # Check type-specific preferences
        type_pref = prefs.type_preferences.get(request.notification_type.value, {})
        if not type_pref.get('enabled', True):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User has disabled {request.notification_type.value} notifications"
            )
        
        # Get template
        template = None
        if request.template_id:
            template = self.get_template(request.template_id)
        else:
            # Find default template for type
            template = self.db.query(EmailTemplate).filter(
                and_(
                    EmailTemplate.notification_type == request.notification_type,
                    EmailTemplate.is_active == True,
                    EmailTemplate.is_system == True
                )
            ).first()
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No template found for notification type"
            )
        
        # Render content
        subject, html_content, text_content = self._render_template(
            template,
            request.template_variables,
            user,
            prefs
        )
        
        # Override subject if provided
        if request.subject_override:
            subject = request.subject_override
        
        # Create notification
        notification = EmailNotification(
            user_id=user.id,
            recipient_email=user.email,
            recipient_name=user.full_name,
            notification_type=request.notification_type,
            template_id=template.id,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            template_variables=request.template_variables,
            reference_id=request.template_variables.get('reference_id'),
            reference_type=request.template_variables.get('reference_type'),
            priority=request.priority
        )
        
        self.db.add(notification)
        self.db.flush()
        
        # Add attachments if any
        if request.attachments:
            for attach_data in request.attachments:
                attachment = self._create_attachment(notification.id, attach_data)
                self.db.add(attachment)
        
        self.db.commit()
        
        # Send immediately if requested
        if request.send_immediately:
            await self._send_notification(notification)
        
        return notification
    
    async def send_bulk_email(
        self,
        request: SendBulkEmailRequest,
        created_by: User
    ) -> EmailBatch:
        """Send bulk email notifications."""
        # Get template
        template = self.get_template(request.template_id)
        
        # Create batch
        batch = EmailBatch(
            name=request.batch_name,
            notification_type=request.notification_type,
            template_id=request.template_id,
            filters=request.recipient_filters,
            scheduled_for=request.scheduled_for,
            created_by=created_by.id
        )
        
        self.db.add(batch)
        self.db.flush()
        
        # Get recipients based on filters
        recipients = self._get_recipients(request.recipient_filters)
        batch.total_count = len(recipients)
        
        # Create notifications for each recipient
        for user in recipients:
            # Check preferences
            prefs = self.get_or_create_preferences(user.id)
            if not prefs.email_enabled:
                continue
            
            type_pref = prefs.type_preferences.get(request.notification_type.value, {})
            if not type_pref.get('enabled', True):
                continue
            
            # Merge user-specific variables
            variables = {**request.template_variables}
            variables['user_name'] = user.full_name
            variables['user_email'] = user.email
            
            # Render content
            subject, html_content, text_content = self._render_template(
                template,
                variables,
                user,
                prefs
            )
            
            # Create notification
            notification = EmailNotification(
                user_id=user.id,
                recipient_email=user.email,
                recipient_name=user.full_name,
                notification_type=request.notification_type,
                template_id=template.id,
                subject=subject,
                html_content=html_content,
                text_content=text_content,
                template_variables=variables,
                batch_id=batch.id,
                priority=5  # Default priority for bulk
            )
            
            self.db.add(notification)
        
        self.db.commit()
        
        # Schedule batch processing
        if not request.scheduled_for or request.scheduled_for <= datetime.utcnow():
            # Process immediately
            asyncio.create_task(self._process_batch(batch.id))
        
        return batch
    
    def preview_email(
        self,
        request: PreviewEmailRequest
    ) -> Dict[str, str]:
        """Preview email content."""
        # Get template
        template = self.get_template(request.template_id)
        
        # Get user if provided
        user = None
        prefs = None
        if request.user_id:
            user = self.db.query(User).filter(User.id == request.user_id).first()
            if user:
                prefs = self.get_or_create_preferences(user.id)
        
        # Use dummy data if no user
        if not user:
            user = type('User', (), {
                'full_name': 'John Doe',
                'email': 'john.doe@example.com',
                'id': 'preview-user'
            })
            prefs = type('Prefs', (), {
                'preferred_language': 'en',
                'unsubscribe_token': 'preview-token'
            })
        
        # Render template
        subject, html_content, text_content = self._render_template(
            template,
            request.template_variables,
            user,
            prefs
        )
        
        # Get domain
        domain = self._get_default_domain()
        
        return {
            'subject': subject,
            'html_content': html_content,
            'text_content': text_content,
            'from_email': domain.from_email,
            'from_name': domain.from_name
        }
    
    # Process notifications
    async def _send_notification(
        self,
        notification: EmailNotification
    ) -> bool:
        """Send individual notification."""
        try:
            # Get domain
            domain = self._get_default_domain()
            
            # Check rate limits
            if not self._check_rate_limit(domain):
                notification.status = EmailStatus.FAILED
                notification.error_message = "Rate limit exceeded"
                self.db.commit()
                return False
            
            # Get provider
            provider = self.providers.get(domain.id)
            if not provider:
                raise Exception(f"No provider configured for domain {domain.domain}")
            
            # Prepare message
            message = self._prepare_message(notification, domain)
            
            # Send via provider
            result = await provider.send(
                from_email=domain.from_email,
                from_name=domain.from_name,
                to_email=notification.recipient_email,
                to_name=notification.recipient_name,
                subject=notification.subject,
                html_content=notification.html_content,
                text_content=notification.text_content,
                message_id=str(notification.id),
                attachments=notification.attachments
            )
            
            # Update notification
            notification.status = EmailStatus.SENT
            notification.sent_at = datetime.utcnow()
            notification.provider = domain.provider
            notification.provider_message_id = result.get('message_id')
            
            # Update domain counters
            domain.emails_sent_today += 1
            domain.emails_sent_hour += 1
            
            # Log event
            self._log_event(notification.id, 'sent', result)
            
            self.db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Failed to send notification {notification.id}: {str(e)}")
            
            notification.retry_count += 1
            notification.error_message = str(e)
            
            if notification.retry_count >= notification.max_retries:
                notification.status = EmailStatus.FAILED
            
            self.db.commit()
            return False
    
    async def _process_batch(
        self,
        batch_id: UUID
    ) -> None:
        """Process email batch."""
        batch = self.db.query(EmailBatch).filter(
            EmailBatch.id == batch_id
        ).first()
        
        if not batch:
            return
        
        batch.status = "processing"
        batch.started_at = datetime.utcnow()
        self.db.commit()
        
        # Get notifications
        notifications = self.db.query(EmailNotification).filter(
            EmailNotification.batch_id == batch_id,
            EmailNotification.status == EmailStatus.PENDING
        ).all()
        
        # Send notifications
        for notification in notifications:
            success = await self._send_notification(notification)
            if success:
                batch.sent_count += 1
            else:
                batch.failed_count += 1
            
            # Small delay to avoid overwhelming providers
            await asyncio.sleep(0.1)
        
        batch.status = "completed"
        batch.completed_at = datetime.utcnow()
        self.db.commit()
    
    def process_webhook(
        self,
        provider: EmailProvider,
        data: Dict[str, Any]
    ) -> None:
        """Process webhook from email provider."""
        # Parse webhook based on provider
        if provider == EmailProvider.SENDGRID:
            events = data if isinstance(data, list) else [data]
            for event in events:
                self._process_sendgrid_event(event)
        elif provider == EmailProvider.AWS_SES:
            self._process_ses_event(data)
        # Add more providers as needed
        
        self.db.commit()
    
    # Helper methods
    def _render_template(
        self,
        template: EmailTemplate,
        variables: Dict[str, Any],
        user: User,
        prefs: NotificationPreference
    ) -> Tuple[str, str, str]:
        """Render email template with variables."""
        # Add system variables
        system_vars = {
            'user_name': user.full_name,
            'user_email': user.email,
            'unsubscribe_url': f"/unsubscribe?token={prefs.unsubscribe_token}",
            'current_year': datetime.utcnow().year,
            'app_name': 'OpenPolicy',
            'app_url': 'https://openpolicy.ca'
        }
        
        all_vars = {**system_vars, **variables}
        
        # Render templates
        subject_tmpl = self.jinja_env.from_string(template.subject_template)
        html_tmpl = self.jinja_env.from_string(template.html_template)
        text_tmpl = self.jinja_env.from_string(template.text_template)
        
        subject = subject_tmpl.render(**all_vars)
        html_content = html_tmpl.render(**all_vars)
        text_content = text_tmpl.render(**all_vars)
        
        # Add unsubscribe footer if required
        if template.requires_unsubscribe:
            unsubscribe_html = f'<p style="font-size: 12px; color: #666; margin-top: 40px;">You are receiving this email because you opted in. <a href="{all_vars["unsubscribe_url"]}">Unsubscribe</a></p>'
            unsubscribe_text = f"\n\n--\nUnsubscribe: {all_vars['unsubscribe_url']}"
            
            html_content += unsubscribe_html
            text_content += unsubscribe_text
        
        return subject, html_content, text_content
    
    def _get_recipients(
        self,
        filters: Dict[str, Any]
    ) -> List[User]:
        """Get recipients based on filters."""
        query = self.db.query(User).filter(User.is_active == True)
        
        # Apply filters
        if 'user_ids' in filters:
            query = query.filter(User.id.in_(filters['user_ids']))
        
        if 'roles' in filters:
            # Join with roles
            pass  # Implement based on your role system
        
        if 'created_after' in filters:
            query = query.filter(User.created_at >= filters['created_after'])
        
        # Add more filters as needed
        
        return query.all()
    
    def _get_default_domain(self) -> EmailDomain:
        """Get default email domain."""
        domain = self.db.query(EmailDomain).filter(
            and_(
                EmailDomain.is_active == True,
                EmailDomain.is_default == True
            )
        ).first()
        
        if not domain:
            # Get any active domain
            domain = self.db.query(EmailDomain).filter(
                EmailDomain.is_active == True
            ).first()
        
        if not domain:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No email domain configured"
            )
        
        return domain
    
    def _check_rate_limit(
        self,
        domain: EmailDomain
    ) -> bool:
        """Check if rate limit allows sending."""
        now = datetime.utcnow()
        
        # Reset counters if needed
        if domain.last_reset_date != now.date():
            domain.emails_sent_today = 0
            domain.last_reset_date = now.date()
        
        if domain.last_reset_hour != now.hour:
            domain.emails_sent_hour = 0
            domain.last_reset_hour = now.hour
        
        # Check limits
        if domain.daily_limit and domain.emails_sent_today >= domain.daily_limit:
            return False
        
        if domain.hourly_limit and domain.emails_sent_hour >= domain.hourly_limit:
            return False
        
        return True
    
    def _create_attachment(
        self,
        notification_id: UUID,
        attach_data: EmailAttachmentCreate
    ) -> EmailAttachment:
        """Create email attachment."""
        # Decode content
        content = base64.b64decode(attach_data.content)
        
        # Save to storage
        storage_path = f"attachments/{notification_id}/{attach_data.filename}"
        # In production, save to S3 or similar
        
        attachment = EmailAttachment(
            notification_id=notification_id,
            filename=attach_data.filename,
            content_type=attach_data.content_type,
            file_size=len(content),
            storage_path=storage_path,
            is_inline=attach_data.is_inline,
            content_id=attach_data.content_id
        )
        
        return attachment
    
    def _prepare_message(
        self,
        notification: EmailNotification,
        domain: EmailDomain
    ) -> MIMEMultipart:
        """Prepare MIME message."""
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{domain.from_name} <{domain.from_email}>"
        msg['To'] = f"{notification.recipient_name} <{notification.recipient_email}>"
        msg['Subject'] = notification.subject
        msg['Message-ID'] = f"<{notification.id}@{domain.domain}>"
        
        # Add text and HTML parts
        msg.attach(MIMEText(notification.text_content, 'plain'))
        msg.attach(MIMEText(notification.html_content, 'html'))
        
        # Add attachments
        for attachment in notification.attachments:
            # Load attachment content
            # In production, load from S3 or similar
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(b"attachment content")  # Placeholder
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{attachment.filename}"'
            )
            msg.attach(part)
        
        return msg
    
    def _log_event(
        self,
        notification_id: UUID,
        event_type: str,
        event_data: Dict[str, Any]
    ) -> None:
        """Log email event."""
        log = EmailLog(
            notification_id=notification_id,
            event_type=event_type,
            event_data=event_data,
            occurred_at=datetime.utcnow()
        )
        self.db.add(log)
    
    def _generate_slug(self, text: str) -> str:
        """Generate URL-safe slug from text."""
        import re
        slug = text.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s_-]+', '-', slug)
        slug = re.sub(r'^-+|-+$', '', slug)
        return slug
    
    def _get_default_type_preferences(self) -> Dict[str, Any]:
        """Get default notification type preferences."""
        defaults = {}
        for notif_type in NotificationType:
            defaults[notif_type.value] = {
                'enabled': True,
                'frequency': 'immediate'
            }
        return defaults
    
    def _process_sendgrid_event(self, event: Dict[str, Any]) -> None:
        """Process SendGrid webhook event."""
        message_id = event.get('sg_message_id')
        if not message_id:
            return
        
        # Find notification
        notification = self.db.query(EmailNotification).filter(
            EmailNotification.provider_message_id == message_id
        ).first()
        
        if not notification:
            return
        
        event_type = event.get('event')
        
        if event_type == 'delivered':
            notification.status = EmailStatus.DELIVERED
            notification.delivered_at = datetime.fromtimestamp(event.get('timestamp', 0))
        elif event_type == 'open':
            notification.status = EmailStatus.OPENED
            notification.opened_at = datetime.fromtimestamp(event.get('timestamp', 0))
        elif event_type == 'click':
            notification.status = EmailStatus.CLICKED
            notification.clicked_at = datetime.fromtimestamp(event.get('timestamp', 0))
        elif event_type == 'bounce':
            notification.status = EmailStatus.BOUNCED
            notification.bounced_at = datetime.fromtimestamp(event.get('timestamp', 0))
        elif event_type == 'spam':
            notification.status = EmailStatus.SPAM
        
        self._log_event(notification.id, event_type, event)
    
    def _process_ses_event(self, data: Dict[str, Any]) -> None:
        """Process AWS SES webhook event."""
        # Implement SES event processing
        pass


# Email provider implementations
class SMTPProvider:
    """SMTP email provider."""
    
    def __init__(self, config: Dict[str, Any]):
        self.host = config.get('host')
        self.port = config.get('port', 587)
        self.username = config.get('username')
        self.password = config.get('password')
        self.use_tls = config.get('use_tls', True)
    
    async def send(self, **kwargs) -> Dict[str, Any]:
        """Send email via SMTP."""
        # Implementation would use smtplib
        return {'message_id': str(uuid4())}


class AWSProvider:
    """AWS SES email provider."""
    
    def __init__(self, config: Dict[str, Any]):
        self.client = boto3.client(
            'ses',
            region_name=config.get('region', 'us-east-1'),
            aws_access_key_id=config.get('access_key'),
            aws_secret_access_key=config.get('secret_key')
        )
    
    async def send(self, **kwargs) -> Dict[str, Any]:
        """Send email via AWS SES."""
        # Implementation would use boto3
        return {'message_id': str(uuid4())}


class SendGridProvider:
    """SendGrid email provider."""
    
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config.get('api_key')
        self.base_url = 'https://api.sendgrid.com/v3'
    
    async def send(self, **kwargs) -> Dict[str, Any]:
        """Send email via SendGrid."""
        # Implementation would use requests or sendgrid library
        return {'message_id': str(uuid4())}


# Dependency injection helper
def get_email_service(db: Session) -> EmailNotificationService:
    """Get email notification service instance."""
    return EmailNotificationService(db)