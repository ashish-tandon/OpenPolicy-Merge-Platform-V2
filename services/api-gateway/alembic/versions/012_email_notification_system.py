"""
Email Notification System

Revision ID: 012_email_notification_system
Revises: 011_data_dashboard_system
Create Date: 2025-08-24 00:00:00

Implements FEAT-007 Email Notifications (P2 priority).
Creates tables for comprehensive email notification management.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '012_email_notification_system'
down_revision = '011_data_dashboard_system'
branch_labels = None
depends_on = None


def upgrade():
    """Create email notification tables."""
    
    # Create email_templates table
    op.create_table(
        'email_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('template_key', sa.String(100), nullable=False),
        sa.Column('version', sa.Integer(), server_default='1', nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('subject_template', sa.Text(), nullable=False),
        sa.Column('html_template', sa.Text(), nullable=False),
        sa.Column('text_template', sa.Text(), nullable=True),
        sa.Column('notification_type', sa.Enum('alert', 'digest', 'welcome', 'verification', 'password_reset', 'report', 'invitation', 'reminder', 'announcement', 'custom', name='notificationtype'), nullable=False),
        sa.Column('variables', postgresql.JSONB(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('is_default', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('language', sa.String(10), server_default='en', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for email_templates
    op.create_index('idx_template_key_version', 'email_templates', ['template_key', 'version'], unique=True)
    op.create_index('idx_template_type', 'email_templates', ['notification_type'])
    op.create_index('idx_template_active', 'email_templates', ['is_active'])
    op.create_index('idx_template_language', 'email_templates', ['language'])
    
    # Create notification_preferences table
    op.create_table(
        'notification_preferences',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email_enabled', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('unsubscribe_token', sa.String(100), nullable=True),
        sa.Column('preferences', postgresql.JSONB(), server_default='{}', nullable=False),
        sa.Column('quiet_hours_enabled', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('quiet_hours_start', sa.String(5), nullable=True),
        sa.Column('quiet_hours_end', sa.String(5), nullable=True),
        sa.Column('quiet_hours_timezone', sa.String(50), server_default='UTC', nullable=False),
        sa.Column('digest_enabled', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('digest_frequency', sa.String(20), server_default='daily', nullable=False),
        sa.Column('digest_day', sa.Integer(), nullable=True),
        sa.Column('digest_time', sa.String(5), server_default='09:00', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('unsubscribe_token')
    )
    
    # Create indexes for notification_preferences
    op.create_index('idx_pref_user', 'notification_preferences', ['user_id'], unique=True)
    op.create_index('idx_pref_token', 'notification_preferences', ['unsubscribe_token'])
    
    # Create email_notifications table
    op.create_table(
        'email_notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('recipient_email', sa.String(255), nullable=False),
        sa.Column('recipient_name', sa.String(200), nullable=True),
        sa.Column('template_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('notification_type', sa.Enum('alert', 'digest', 'welcome', 'verification', 'password_reset', 'report', 'invitation', 'reminder', 'announcement', 'custom', name='notificationtype'), nullable=False),
        sa.Column('subject', sa.Text(), nullable=False),
        sa.Column('template_variables', postgresql.JSONB(), nullable=True),
        sa.Column('priority', sa.Enum('low', 'medium', 'high', 'urgent', name='notificationpriority'), server_default='medium', nullable=False),
        sa.Column('reference_id', sa.String(100), nullable=True),
        sa.Column('tags', postgresql.JSONB(), nullable=True),
        sa.Column('scheduled_for', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.Enum('pending', 'sending', 'sent', 'delivered', 'failed', 'bounced', 'complained', name='emailstatus'), server_default='pending', nullable=False),
        sa.Column('attempts', sa.Integer(), server_default='0', nullable=False),
        sa.Column('last_attempt_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('provider', sa.Enum('smtp', 'sendgrid', 'mailgun', 'postmark', 'resend', 'aws_ses', name='emailprovider'), nullable=True),
        sa.Column('provider_message_id', sa.String(255), nullable=True),
        sa.Column('provider_response', postgresql.JSONB(), nullable=True),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('delivered_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('opened_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('clicked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('error_details', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['template_id'], ['email_templates.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for email_notifications
    op.create_index('idx_notification_user', 'email_notifications', ['user_id'])
    op.create_index('idx_notification_status', 'email_notifications', ['status'])
    op.create_index('idx_notification_scheduled', 'email_notifications', ['scheduled_for'])
    op.create_index('idx_notification_created', 'email_notifications', ['created_at'])
    op.create_index('idx_notification_reference', 'email_notifications', ['reference_id'])
    op.create_index('idx_notification_provider_id', 'email_notifications', ['provider_message_id'])
    
    # Create email_events table
    op.create_table(
        'email_events',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('notification_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('event_data', postgresql.JSONB(), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('occurred_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['notification_id'], ['email_notifications.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for email_events
    op.create_index('idx_event_notification', 'email_events', ['notification_id'])
    op.create_index('idx_event_type', 'email_events', ['event_type'])
    op.create_index('idx_event_occurred', 'email_events', ['occurred_at'])
    
    # Create email_attachments table
    op.create_table(
        'email_attachments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('notification_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('content_type', sa.String(100), nullable=False),
        sa.Column('size_bytes', sa.Integer(), nullable=False),
        sa.Column('storage_path', sa.String(500), nullable=True),
        sa.Column('content_base64', sa.Text(), nullable=True),
        sa.Column('checksum', sa.String(64), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['notification_id'], ['email_notifications.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index for email_attachments
    op.create_index('idx_attachment_notification', 'email_attachments', ['notification_id'])
    
    # Create email_batches table
    op.create_table(
        'email_batches',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('batch_type', sa.String(50), nullable=False),
        sa.Column('template_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('recipient_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('recipient_criteria', postgresql.JSONB(), nullable=True),
        sa.Column('status', sa.String(50), server_default='draft', nullable=False),
        sa.Column('scheduled_for', sa.DateTime(timezone=True), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('sent_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('failed_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('opened_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('clicked_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['template_id'], ['email_templates.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for email_batches
    op.create_index('idx_batch_status', 'email_batches', ['status'])
    op.create_index('idx_batch_scheduled', 'email_batches', ['scheduled_for'])
    op.create_index('idx_batch_created_by', 'email_batches', ['created_by'])
    
    # Create notification_queue table
    op.create_table(
        'notification_queue',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('notification_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('priority', sa.Integer(), server_default='0', nullable=False),
        sa.Column('status', sa.String(50), server_default='pending', nullable=False),
        sa.Column('processor_id', sa.String(100), nullable=True),
        sa.Column('retry_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('retry_after', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['notification_id'], ['email_notifications.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for notification_queue
    op.create_index('idx_queue_status', 'notification_queue', ['status'])
    op.create_index('idx_queue_priority', 'notification_queue', ['priority', 'created_at'])
    op.create_index('idx_queue_retry', 'notification_queue', ['retry_after'])
    
    # Create email_providers table
    op.create_table(
        'email_providers',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('provider_type', sa.Enum('smtp', 'sendgrid', 'mailgun', 'postmark', 'resend', 'aws_ses', name='emailprovider'), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('is_default', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('config', postgresql.JSONB(), nullable=False),
        sa.Column('rate_limit_per_second', sa.Integer(), nullable=True),
        sa.Column('rate_limit_per_day', sa.Integer(), nullable=True),
        sa.Column('total_sent', sa.Integer(), server_default='0', nullable=False),
        sa.Column('total_failed', sa.Integer(), server_default='0', nullable=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('provider_type')
    )
    
    # Create indexes for email_providers
    op.create_index('idx_provider_active', 'email_providers', ['is_active'])
    op.create_index('idx_provider_default', 'email_providers', ['is_default'])
    
    # Insert default email templates
    from sqlalchemy.sql import table, column
    import uuid
    
    templates_table = table(
        'email_templates',
        column('id', postgresql.UUID),
        column('template_key', sa.String),
        column('name', sa.String),
        column('description', sa.Text),
        column('subject_template', sa.Text),
        column('html_template', sa.Text),
        column('text_template', sa.Text),
        column('notification_type', sa.String),
        column('variables', postgresql.JSONB),
        column('language', sa.String)
    )
    
    default_templates = [
        {
            'id': uuid.uuid4(),
            'template_key': 'welcome',
            'name': 'Welcome Email',
            'description': 'Sent to new users after registration',
            'subject_template': 'Welcome to {{ app_name }}, {{ user_name }}!',
            'html_template': '''
                <h1>Welcome to {{ app_name }}!</h1>
                <p>Hi {{ user_name }},</p>
                <p>Thank you for joining OpenPolicy. We're excited to have you on board!</p>
                <p>Get started by exploring:</p>
                <ul>
                    <li><a href="{{ app_url }}/bills">Current Bills</a></li>
                    <li><a href="{{ app_url }}/members">Members of Parliament</a></li>
                    <li><a href="{{ app_url }}/votes">Recent Votes</a></li>
                </ul>
                <p>Best regards,<br>The {{ app_name }} Team</p>
            ''',
            'text_template': '''
                Welcome to {{ app_name }}!
                
                Hi {{ user_name }},
                
                Thank you for joining OpenPolicy. We're excited to have you on board!
                
                Get started by exploring:
                - Current Bills: {{ app_url }}/bills
                - Members of Parliament: {{ app_url }}/members
                - Recent Votes: {{ app_url }}/votes
                
                Best regards,
                The {{ app_name }} Team
            ''',
            'notification_type': 'welcome',
            'variables': [
                {'name': 'user_name', 'type': 'string', 'required': True},
                {'name': 'app_name', 'type': 'string', 'required': True},
                {'name': 'app_url', 'type': 'string', 'required': True}
            ],
            'language': 'en'
        },
        {
            'id': uuid.uuid4(),
            'template_key': 'password_reset',
            'name': 'Password Reset',
            'description': 'Password reset request email',
            'subject_template': 'Reset your {{ app_name }} password',
            'html_template': '''
                <h2>Password Reset Request</h2>
                <p>Hi {{ user_name }},</p>
                <p>We received a request to reset your password. Click the link below to create a new password:</p>
                <p><a href="{{ reset_link }}" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
                <p>This link will expire in {{ expiry_hours }} hours.</p>
                <p>If you didn't request this, please ignore this email.</p>
                <p>Best regards,<br>The {{ app_name }} Team</p>
            ''',
            'text_template': '''
                Password Reset Request
                
                Hi {{ user_name }},
                
                We received a request to reset your password. Visit the link below to create a new password:
                
                {{ reset_link }}
                
                This link will expire in {{ expiry_hours }} hours.
                
                If you didn't request this, please ignore this email.
                
                Best regards,
                The {{ app_name }} Team
            ''',
            'notification_type': 'password_reset',
            'variables': [
                {'name': 'user_name', 'type': 'string', 'required': True},
                {'name': 'reset_link', 'type': 'string', 'required': True},
                {'name': 'expiry_hours', 'type': 'number', 'required': True}
            ],
            'language': 'en'
        },
        {
            'id': uuid.uuid4(),
            'template_key': 'bill_update',
            'name': 'Bill Update Alert',
            'description': 'Notification about bill status changes',
            'subject_template': 'Update on Bill {{ bill_number }}: {{ bill_title }}',
            'html_template': '''
                <h2>Bill Update</h2>
                <p>Hi {{ user_name }},</p>
                <p>There's been an update to a bill you're following:</p>
                <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0;">
                    <h3>{{ bill_number }}: {{ bill_title }}</h3>
                    <p><strong>Status:</strong> {{ new_status }}</p>
                    <p><strong>Update:</strong> {{ update_description }}</p>
                    <p><a href="{{ bill_url }}">View Bill Details</a></p>
                </div>
                <p>Best regards,<br>The {{ app_name }} Team</p>
            ''',
            'notification_type': 'alert',
            'variables': [
                {'name': 'user_name', 'type': 'string', 'required': True},
                {'name': 'bill_number', 'type': 'string', 'required': True},
                {'name': 'bill_title', 'type': 'string', 'required': True},
                {'name': 'new_status', 'type': 'string', 'required': True},
                {'name': 'update_description', 'type': 'string', 'required': True},
                {'name': 'bill_url', 'type': 'string', 'required': True}
            ],
            'language': 'en'
        },
        {
            'id': uuid.uuid4(),
            'template_key': 'daily_digest',
            'name': 'Daily Digest',
            'description': 'Daily summary of parliamentary activity',
            'subject_template': 'Your {{ app_name }} Daily Digest - {{ date }}',
            'html_template': '''
                <h1>Daily Parliamentary Digest</h1>
                <p>Hi {{ user_name }},</p>
                <p>Here's what happened in Parliament today:</p>
                
                {% if bills_updated %}
                <h2>📋 Bill Updates</h2>
                <ul>
                {% for bill in bills_updated %}
                    <li><a href="{{ bill.url }}">{{ bill.number }}: {{ bill.title }}</a> - {{ bill.status }}</li>
                {% endfor %}
                </ul>
                {% endif %}
                
                {% if votes_held %}
                <h2>🗳️ Votes Held</h2>
                <ul>
                {% for vote in votes_held %}
                    <li><a href="{{ vote.url }}">{{ vote.title }}</a> - {{ vote.result }}</li>
                {% endfor %}
                </ul>
                {% endif %}
                
                {% if committee_meetings %}
                <h2>🏛️ Committee Meetings</h2>
                <ul>
                {% for meeting in committee_meetings %}
                    <li>{{ meeting.committee }} - {{ meeting.topic }}</li>
                {% endfor %}
                </ul>
                {% endif %}
                
                <p><a href="{{ app_url }}/dashboard">View Full Dashboard</a></p>
                <p>Best regards,<br>The {{ app_name }} Team</p>
            ''',
            'notification_type': 'digest',
            'variables': [
                {'name': 'user_name', 'type': 'string', 'required': True},
                {'name': 'date', 'type': 'string', 'required': True},
                {'name': 'bills_updated', 'type': 'array', 'required': False},
                {'name': 'votes_held', 'type': 'array', 'required': False},
                {'name': 'committee_meetings', 'type': 'array', 'required': False}
            ],
            'language': 'en'
        }
    ]
    
    op.bulk_insert(templates_table, default_templates)
    
    # Insert default SMTP provider
    providers_table = table(
        'email_providers',
        column('id', postgresql.UUID),
        column('provider_type', sa.String),
        column('name', sa.String),
        column('is_active', sa.Boolean),
        column('is_default', sa.Boolean),
        column('config', postgresql.JSONB)
    )
    
    default_provider = {
        'id': uuid.uuid4(),
        'provider_type': 'smtp',
        'name': 'Default SMTP',
        'is_active': True,
        'is_default': True,
        'config': {
            'host': 'localhost',
            'port': 1025,
            'use_tls': False,
            'username': '',
            'password': '',
            'from_email': 'noreply@openpolicy.ca'
        }
    }
    
    op.bulk_insert(providers_table, [default_provider])


def downgrade():
    """Drop email notification tables."""
    
    # Drop tables in reverse order due to foreign key constraints
    op.drop_index('idx_provider_default', table_name='email_providers')
    op.drop_index('idx_provider_active', table_name='email_providers')
    op.drop_table('email_providers')
    
    op.drop_index('idx_queue_retry', table_name='notification_queue')
    op.drop_index('idx_queue_priority', table_name='notification_queue')
    op.drop_index('idx_queue_status', table_name='notification_queue')
    op.drop_table('notification_queue')
    
    op.drop_index('idx_batch_created_by', table_name='email_batches')
    op.drop_index('idx_batch_scheduled', table_name='email_batches')
    op.drop_index('idx_batch_status', table_name='email_batches')
    op.drop_table('email_batches')
    
    op.drop_index('idx_attachment_notification', table_name='email_attachments')
    op.drop_table('email_attachments')
    
    op.drop_index('idx_event_occurred', table_name='email_events')
    op.drop_index('idx_event_type', table_name='email_events')
    op.drop_index('idx_event_notification', table_name='email_events')
    op.drop_table('email_events')
    
    op.drop_index('idx_notification_provider_id', table_name='email_notifications')
    op.drop_index('idx_notification_reference', table_name='email_notifications')
    op.drop_index('idx_notification_created', table_name='email_notifications')
    op.drop_index('idx_notification_scheduled', table_name='email_notifications')
    op.drop_index('idx_notification_status', table_name='email_notifications')
    op.drop_index('idx_notification_user', table_name='email_notifications')
    op.drop_table('email_notifications')
    
    op.drop_index('idx_pref_token', table_name='notification_preferences')
    op.drop_index('idx_pref_user', table_name='notification_preferences')
    op.drop_table('notification_preferences')
    
    op.drop_index('idx_template_language', table_name='email_templates')
    op.drop_index('idx_template_active', table_name='email_templates')
    op.drop_index('idx_template_type', table_name='email_templates')
    op.drop_index('idx_template_key_version', table_name='email_templates')
    op.drop_table('email_templates')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS notificationtype')
    op.execute('DROP TYPE IF EXISTS notificationpriority')
    op.execute('DROP TYPE IF EXISTS emailstatus')
    op.execute('DROP TYPE IF EXISTS emailprovider')