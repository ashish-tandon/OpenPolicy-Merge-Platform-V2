"""Create email alerts system tables

Revision ID: 004
Revises: 003
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    # Create email_alerts table
    op.create_table('email_alerts',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('alert_type', sa.String(length=50), nullable=False),
        sa.Column('frequency', sa.String(length=20), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('include_summary', sa.Boolean(), nullable=False, default=True),
        sa.Column('include_links', sa.Boolean(), nullable=False, default=True),
        sa.Column('include_analytics', sa.Boolean(), nullable=False, default=False),
        sa.Column('filters', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('last_sent', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for email_alerts
    op.create_index('ix_email_alerts_user_id', 'email_alerts', ['user_id'])
    op.create_index('ix_email_alerts_alert_type', 'email_alerts', ['alert_type'])
    op.create_index('ix_email_alerts_is_active', 'email_alerts', ['is_active'])
    op.create_index('ix_email_alerts_frequency', 'email_alerts', ['frequency'])
    op.create_index('ix_email_alerts_last_sent', 'email_alerts', ['last_sent'])
    
    # Create email_templates table
    op.create_table('email_templates',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('template_name', sa.String(length=100), nullable=False),
        sa.Column('template_type', sa.String(length=50), nullable=False),
        sa.Column('subject_template', sa.String(length=200), nullable=False),
        sa.Column('html_template', sa.Text(), nullable=True),
        sa.Column('text_template', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('variables', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('template_name')
    )
    
    # Create indexes for email_templates
    op.create_index('ix_email_templates_template_type', 'email_templates', ['template_type'])
    op.create_index('ix_email_templates_is_active', 'email_templates', ['is_active'])
    op.create_index('ix_email_templates_template_name', 'email_templates', ['template_name'])
    
    # Create email_campaigns table
    op.create_table('email_campaigns',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('campaign_name', sa.String(length=200), nullable=False),
        sa.Column('campaign_type', sa.String(length=50), nullable=False),
        sa.Column('subject', sa.String(length=200), nullable=False),
        sa.Column('html_content', sa.Text(), nullable=True),
        sa.Column('text_content', sa.Text(), nullable=True),
        sa.Column('target_audience', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('scheduled_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('total_recipients', sa.Integer(), nullable=False, default=0),
        sa.Column('sent_count', sa.Integer(), nullable=False, default=0),
        sa.Column('delivered_count', sa.Integer(), nullable=False, default=0),
        sa.Column('opened_count', sa.Integer(), nullable=False, default=0),
        sa.Column('clicked_count', sa.Integer(), nullable=False, default=0),
        sa.Column('bounced_count', sa.Integer(), nullable=False, default=0),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for email_campaigns
    op.create_index('ix_email_campaigns_campaign_type', 'email_campaigns', ['campaign_type'])
    op.create_index('ix_email_campaigns_is_active', 'email_campaigns', ['is_active'])
    op.create_index('ix_email_campaigns_scheduled_at', 'email_campaigns', ['scheduled_at'])
    op.create_index('ix_email_campaigns_created_at', 'email_campaigns', ['created_at'])
    
    # Create email_logs table
    op.create_table('email_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('campaign_id', sa.UUID(), nullable=True),
        sa.Column('email_type', sa.String(length=50), nullable=False),
        sa.Column('recipient_email', sa.String(length=255), nullable=False),
        sa.Column('subject', sa.String(length=500), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('sent_at', sa.DateTime(), nullable=True),
        sa.Column('delivered_at', sa.DateTime(), nullable=True),
        sa.Column('opened_at', sa.DateTime(), nullable=True),
        sa.Column('clicked_at', sa.DateTime(), nullable=True),
        sa.Column('bounced_at', sa.DateTime(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['campaign_id'], ['email_campaigns.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for email_logs
    op.create_index('ix_email_logs_user_id', 'email_logs', ['user_id'])
    op.create_index('ix_email_logs_campaign_id', 'email_logs', ['campaign_id'])
    op.create_index('ix_email_logs_email_type', 'email_logs', ['email_type'])
    op.create_index('ix_email_logs_status', 'email_logs', ['status'])
    op.create_index('ix_email_logs_recipient_email', 'email_logs', ['recipient_email'])
    op.create_index('ix_email_logs_sent_at', 'email_logs', ['sent_at'])
    op.create_index('ix_email_logs_created_at', 'email_logs', ['created_at'])
    
    # Create unsubscribe_tokens table
    op.create_table('unsubscribe_tokens',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('token', sa.String(length=64), nullable=False),
        sa.Column('alert_type', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('used_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )
    
    # Create indexes for unsubscribe_tokens
    op.create_index('ix_unsubscribe_tokens_user_id', 'unsubscribe_tokens', ['user_id'])
    op.create_index('ix_unsubscribe_tokens_token', 'unsubscribe_tokens', ['token'])
    op.create_index('ix_unsubscribe_tokens_is_active', 'unsubscribe_tokens', ['is_active'])
    op.create_index('ix_unsubscribe_tokens_expires_at', 'unsubscribe_tokens', ['expires_at'])
    
    # Insert default email templates
    op.execute("""
        INSERT INTO email_templates (id, template_name, template_type, subject_template, html_template, text_template, description, variables, is_active)
        VALUES 
        (gen_random_uuid(), 'default', 'general', 'OpenPolicy Update: {{title}}', 
         '<h1>{{title}}</h1><p>{{content}}</p><p><a href="{{link}}">Read More</a></p>', 
         '{{title}}\n\n{{content}}\n\nRead More: {{link}}', 
         'Default template for general notifications', 
         '{"title": "string", "content": "string", "link": "string"}', 
         true),
        (gen_random_uuid(), 'bill_update', 'bill_update', 'Bill Update: {{bill_title}}', 
         '<h2>Bill Update</h2><h3>{{bill_title}}</h3><p>Status: {{status}}</p><p>{{description}}</p>', 
         'Bill Update: {{bill_title}}\nStatus: {{status}}\n\n{{description}}', 
         'Template for bill status updates', 
         '{"bill_title": "string", "status": "string", "description": "string"}', 
         true),
        (gen_random_uuid(), 'vote_reminder', 'vote_reminder', 'Vote Reminder: {{bill_title}}', 
         '<h2>Vote Reminder</h2><h3>{{bill_title}}</h3><p>Voting closes: {{deadline}}</p>', 
         'Vote Reminder: {{bill_title}}\nVoting closes: {{deadline}}', 
         'Template for vote reminders', 
         '{"bill_title": "string", "deadline": "string"}', 
         true)
    """)


def downgrade():
    # Drop tables in reverse order
    op.drop_table('unsubscribe_tokens')
    op.drop_table('email_logs')
    op.drop_table('email_campaigns')
    op.drop_table('email_templates')
    op.drop_table('email_alerts')
