"""
Email Notification System

Revision ID: 012_email_notification_system
Revises: 011_data_dashboard_system
Create Date: 2025-08-24 00:00:00

Implements FEAT-007 Email Notifications (P2 priority).
Creates tables for comprehensive email notification system.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import text

# revision identifiers
revision = '012_email_notification_system'
down_revision = '011_data_dashboard_system'
branch_labels = None
depends_on = None


def upgrade():
    """Create email notification tables."""
    
    # Create email_templates_v2 table (v2 to avoid conflict with existing)
    op.create_table(
        'email_templates_v2',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('slug', sa.String(200), nullable=False),
        sa.Column('notification_type', sa.Enum('bill_update', 'vote_result', 'committee_meeting', 'debate_mention', 'member_activity', 'account_verification', 'password_reset', 'security_alert', 'weekly_digest', 'custom_alert', 'feedback_response', 'dashboard_alert', 'report_ready', 'snapshot_shared', name='notificationtype'), nullable=False),
        sa.Column('subject_template', sa.String(500), nullable=False),
        sa.Column('html_template', sa.Text(), nullable=False),
        sa.Column('text_template', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('variables', postgresql.JSONB(), nullable=True),
        sa.Column('preview_data', postgresql.JSONB(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('is_system', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('requires_unsubscribe', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('language', sa.String(10), server_default='en', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )
    
    # Create indexes for email_templates_v2
    op.create_index('idx_template_slug', 'email_templates_v2', ['slug'])
    op.create_index('idx_template_type', 'email_templates_v2', ['notification_type'])
    op.create_index('idx_template_active', 'email_templates_v2', ['is_active'])
    
    # Create notification_preferences table
    op.create_table(
        'notification_preferences',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email_enabled', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('digest_frequency', sa.String(20), server_default='weekly', nullable=False),
        sa.Column('type_preferences', postgresql.JSONB(), server_default='{}', nullable=False),
        sa.Column('preferred_language', sa.String(10), server_default='en', nullable=False),
        sa.Column('timezone', sa.String(50), server_default='UTC', nullable=False),
        sa.Column('quiet_hours_start', sa.Integer(), nullable=True),
        sa.Column('quiet_hours_end', sa.Integer(), nullable=True),
        sa.Column('unsubscribe_token', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('unsubscribe_token')
    )
    
    # Create indexes for notification_preferences
    op.create_index('idx_pref_user', 'notification_preferences', ['user_id'], unique=True)
    op.create_index('idx_pref_token', 'notification_preferences', ['unsubscribe_token'])
    
    # Create email_batches table
    op.create_table(
        'email_batches',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('notification_type', sa.Enum('bill_update', 'vote_result', 'committee_meeting', 'debate_mention', 'member_activity', 'account_verification', 'password_reset', 'security_alert', 'weekly_digest', 'custom_alert', 'feedback_response', 'dashboard_alert', 'report_ready', 'snapshot_shared', name='notificationtype'), nullable=False),
        sa.Column('total_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('sent_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('failed_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('status', sa.String(50), server_default='pending', nullable=False),
        sa.Column('scheduled_for', sa.DateTime(timezone=True), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('filters', postgresql.JSONB(), nullable=True),
        sa.Column('template_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['template_id'], ['email_templates_v2.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for email_batches
    op.create_index('idx_batch_status', 'email_batches', ['status'])
    op.create_index('idx_batch_scheduled', 'email_batches', ['scheduled_for'])
    
    # Create email_notifications table
    op.create_table(
        'email_notifications',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('recipient_email', sa.String(255), nullable=False),
        sa.Column('recipient_name', sa.String(200), nullable=True),
        sa.Column('notification_type', sa.Enum('bill_update', 'vote_result', 'committee_meeting', 'debate_mention', 'member_activity', 'account_verification', 'password_reset', 'security_alert', 'weekly_digest', 'custom_alert', 'feedback_response', 'dashboard_alert', 'report_ready', 'snapshot_shared', name='notificationtype'), nullable=False),
        sa.Column('template_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('subject', sa.String(500), nullable=False),
        sa.Column('html_content', sa.Text(), nullable=False),
        sa.Column('text_content', sa.Text(), nullable=False),
        sa.Column('template_variables', postgresql.JSONB(), nullable=True),
        sa.Column('reference_id', sa.String(200), nullable=True),
        sa.Column('reference_type', sa.String(100), nullable=True),
        sa.Column('provider', sa.Enum('smtp', 'sendgrid', 'mailgun', 'aws_ses', 'resend', 'brevo', name='emailprovider'), nullable=True),
        sa.Column('provider_message_id', sa.String(255), nullable=True),
        sa.Column('status', sa.Enum('pending', 'sent', 'delivered', 'opened', 'clicked', 'bounced', 'failed', 'spam', name='emailstatus'), server_default='pending', nullable=False),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('delivered_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('opened_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('clicked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('bounced_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('retry_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('max_retries', sa.Integer(), server_default='3', nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('batch_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('priority', sa.Integer(), server_default='5', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['batch_id'], ['email_batches.id'], ),
        sa.ForeignKeyConstraint(['template_id'], ['email_templates_v2.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for email_notifications
    op.create_index('idx_notif_user', 'email_notifications', ['user_id'])
    op.create_index('idx_notif_status', 'email_notifications', ['status'])
    op.create_index('idx_notif_type', 'email_notifications', ['notification_type'])
    op.create_index('idx_notif_created', 'email_notifications', ['created_at'])
    op.create_index('idx_notif_batch', 'email_notifications', ['batch_id'])
    op.create_index('idx_notif_priority', 'email_notifications', ['priority', 'status'])
    
    # Create email_attachments table
    op.create_table(
        'email_attachments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('notification_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('content_type', sa.String(100), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('storage_path', sa.String(500), nullable=False),
        sa.Column('storage_type', sa.String(50), server_default='local', nullable=False),
        sa.Column('is_inline', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('content_id', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['notification_id'], ['email_notifications.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index for email_attachments
    op.create_index('idx_attach_notification', 'email_attachments', ['notification_id'])
    
    # Create email_logs table
    op.create_table(
        'email_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('notification_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('event_data', postgresql.JSONB(), nullable=True),
        sa.Column('provider', sa.Enum('smtp', 'sendgrid', 'mailgun', 'aws_ses', 'resend', 'brevo', name='emailprovider'), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.String(500), nullable=True),
        sa.Column('occurred_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['notification_id'], ['email_notifications.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for email_logs
    op.create_index('idx_log_notification', 'email_logs', ['notification_id'])
    op.create_index('idx_log_event', 'email_logs', ['event_type'])
    op.create_index('idx_log_occurred', 'email_logs', ['occurred_at'])
    
    # Create email_domains table
    op.create_table(
        'email_domains',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('domain', sa.String(255), nullable=False),
        sa.Column('from_name', sa.String(200), nullable=False),
        sa.Column('from_email', sa.String(255), nullable=False),
        sa.Column('reply_to', sa.String(255), nullable=True),
        sa.Column('provider', sa.Enum('smtp', 'sendgrid', 'mailgun', 'aws_ses', 'resend', 'brevo', name='emailprovider'), nullable=False),
        sa.Column('provider_config', postgresql.JSONB(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('is_default', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('daily_limit', sa.Integer(), nullable=True),
        sa.Column('hourly_limit', sa.Integer(), nullable=True),
        sa.Column('is_verified', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('verification_data', postgresql.JSONB(), nullable=True),
        sa.Column('emails_sent_today', sa.Integer(), server_default='0', nullable=False),
        sa.Column('emails_sent_hour', sa.Integer(), server_default='0', nullable=False),
        sa.Column('last_reset_date', sa.Date(), nullable=True),
        sa.Column('last_reset_hour', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('domain')
    )
    
    # Create indexes for email_domains
    op.create_index('idx_domain_active', 'email_domains', ['is_active'])
    op.create_index('idx_domain_default', 'email_domains', ['is_default'])
    
    # Insert default email templates
    from sqlalchemy.sql import table, column
    import uuid
    
    templates_table = table(
        'email_templates_v2',
        column('id', postgresql.UUID),
        column('name', sa.String),
        column('slug', sa.String),
        column('notification_type', sa.String),
        column('subject_template', sa.String),
        column('html_template', sa.Text),
        column('text_template', sa.Text),
        column('description', sa.Text),
        column('is_system', sa.Boolean)
    )
    
    default_templates = [
        {
            'id': uuid.uuid4(),
            'name': 'Bill Update Notification',
            'slug': 'bill-update-notification',
            'notification_type': 'bill_update',
            'subject_template': 'Update on Bill {{ bill_number }}: {{ bill_title }}',
            'html_template': '''<h2>Bill Update</h2>
<p>Hello {{ user_name }},</p>
<p>There has been an update to Bill {{ bill_number }}: {{ bill_title }}</p>
<p><strong>Update:</strong> {{ update_description }}</p>
<p><a href="{{ bill_url }}">View Bill Details</a></p>''',
            'text_template': '''Bill Update

Hello {{ user_name }},

There has been an update to Bill {{ bill_number }}: {{ bill_title }}

Update: {{ update_description }}

View Bill Details: {{ bill_url }}''',
            'description': 'Notification for bill status updates',
            'is_system': True
        },
        {
            'id': uuid.uuid4(),
            'name': 'Vote Result Notification',
            'slug': 'vote-result-notification',
            'notification_type': 'vote_result',
            'subject_template': 'Vote Result: {{ vote_title }}',
            'html_template': '''<h2>Vote Result</h2>
<p>Hello {{ user_name }},</p>
<p>The vote on "{{ vote_title }}" has concluded.</p>
<p><strong>Result:</strong> {{ vote_result }}</p>
<p><strong>Final Count:</strong> Yes: {{ yes_votes }}, No: {{ no_votes }}</p>
<p><a href="{{ vote_url }}">View Full Details</a></p>''',
            'text_template': '''Vote Result

Hello {{ user_name }},

The vote on "{{ vote_title }}" has concluded.

Result: {{ vote_result }}
Final Count: Yes: {{ yes_votes }}, No: {{ no_votes }}

View Full Details: {{ vote_url }}''',
            'description': 'Notification for vote results',
            'is_system': True
        },
        {
            'id': uuid.uuid4(),
            'name': 'Weekly Digest',
            'slug': 'weekly-digest',
            'notification_type': 'weekly_digest',
            'subject_template': 'Your OpenPolicy Weekly Digest - {{ week_of }}',
            'html_template': '''<h2>Your Weekly Parliamentary Update</h2>
<p>Hello {{ user_name }},</p>
<p>Here's what happened in Parliament this week:</p>
<h3>Bills</h3>
{{ bills_summary }}
<h3>Votes</h3>
{{ votes_summary }}
<h3>Committee Activities</h3>
{{ committees_summary }}
<p><a href="{{ dashboard_url }}">View Your Dashboard</a></p>''',
            'text_template': '''Your Weekly Parliamentary Update

Hello {{ user_name }},

Here's what happened in Parliament this week:

BILLS
{{ bills_summary }}

VOTES
{{ votes_summary }}

COMMITTEE ACTIVITIES
{{ committees_summary }}

View Your Dashboard: {{ dashboard_url }}''',
            'description': 'Weekly summary of parliamentary activities',
            'is_system': True
        },
        {
            'id': uuid.uuid4(),
            'name': 'Account Verification',
            'slug': 'account-verification',
            'notification_type': 'account_verification',
            'subject_template': 'Verify your OpenPolicy account',
            'html_template': '''<h2>Welcome to OpenPolicy!</h2>
<p>Hello {{ user_name }},</p>
<p>Please verify your email address to activate your account.</p>
<p><a href="{{ verification_url }}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
<p>Or copy this link: {{ verification_url }}</p>
<p>This link expires in 24 hours.</p>''',
            'text_template': '''Welcome to OpenPolicy!

Hello {{ user_name }},

Please verify your email address to activate your account.

Verify Email: {{ verification_url }}

This link expires in 24 hours.''',
            'description': 'Email verification for new accounts',
            'is_system': True,
            'requires_unsubscribe': False
        },
        {
            'id': uuid.uuid4(),
            'name': 'Dashboard Alert',
            'slug': 'dashboard-alert',
            'notification_type': 'dashboard_alert',
            'subject_template': 'Alert: {{ alert_name }}',
            'html_template': '''<h2>Dashboard Alert</h2>
<p>Hello {{ user_name }},</p>
<p>Your dashboard alert "{{ alert_name }}" has been triggered.</p>
<p><strong>Condition:</strong> {{ condition_description }}</p>
<p><strong>Current Value:</strong> {{ current_value }}</p>
<p><strong>Threshold:</strong> {{ threshold_value }}</p>
<p><a href="{{ dashboard_url }}">View Dashboard</a></p>''',
            'text_template': '''Dashboard Alert

Hello {{ user_name }},

Your dashboard alert "{{ alert_name }}" has been triggered.

Condition: {{ condition_description }}
Current Value: {{ current_value }}
Threshold: {{ threshold_value }}

View Dashboard: {{ dashboard_url }}''',
            'description': 'Alert from dashboard monitoring',
            'is_system': True
        }
    ]
    
    op.bulk_insert(templates_table, default_templates)
    
    # Insert default email domain (SMTP example)
    domains_table = table(
        'email_domains',
        column('id', postgresql.UUID),
        column('domain', sa.String),
        column('from_name', sa.String),
        column('from_email', sa.String),
        column('provider', sa.String),
        column('provider_config', postgresql.JSONB),
        column('is_default', sa.Boolean),
        column('daily_limit', sa.Integer)
    )
    
    default_domain = {
        'id': uuid.uuid4(),
        'domain': 'openpolicy.ca',
        'from_name': 'OpenPolicy',
        'from_email': 'notifications@openpolicy.ca',
        'provider': 'smtp',
        'provider_config': {
            'host': 'smtp.gmail.com',
            'port': 587,
            'username': 'notifications@openpolicy.ca',
            'password': 'encrypted_password_here',
            'use_tls': True
        },
        'is_default': True,
        'daily_limit': 1000
    }
    
    op.bulk_insert(domains_table, [default_domain])


def downgrade():
    """Drop email notification tables."""
    
    # Drop tables in reverse order due to foreign key constraints
    op.drop_index('idx_domain_default', table_name='email_domains')
    op.drop_index('idx_domain_active', table_name='email_domains')
    op.drop_table('email_domains')
    
    op.drop_index('idx_log_occurred', table_name='email_logs')
    op.drop_index('idx_log_event', table_name='email_logs')
    op.drop_index('idx_log_notification', table_name='email_logs')
    op.drop_table('email_logs')
    
    op.drop_index('idx_attach_notification', table_name='email_attachments')
    op.drop_table('email_attachments')
    
    op.drop_index('idx_notif_priority', table_name='email_notifications')
    op.drop_index('idx_notif_batch', table_name='email_notifications')
    op.drop_index('idx_notif_created', table_name='email_notifications')
    op.drop_index('idx_notif_type', table_name='email_notifications')
    op.drop_index('idx_notif_status', table_name='email_notifications')
    op.drop_index('idx_notif_user', table_name='email_notifications')
    op.drop_table('email_notifications')
    
    op.drop_index('idx_batch_scheduled', table_name='email_batches')
    op.drop_index('idx_batch_status', table_name='email_batches')
    op.drop_table('email_batches')
    
    op.drop_index('idx_pref_token', table_name='notification_preferences')
    op.drop_index('idx_pref_user', table_name='notification_preferences')
    op.drop_table('notification_preferences')
    
    op.drop_index('idx_template_active', table_name='email_templates_v2')
    op.drop_index('idx_template_type', table_name='email_templates_v2')
    op.drop_index('idx_template_slug', table_name='email_templates_v2')
    op.drop_table('email_templates_v2')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS notificationtype')
    op.execute('DROP TYPE IF EXISTS emailstatus')
    op.execute('DROP TYPE IF EXISTS emailprovider')