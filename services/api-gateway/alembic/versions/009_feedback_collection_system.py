"""
Feedback Collection System

Revision ID: 009_feedback_collection_system
Revises: 008_member_management_system
Create Date: 2025-08-23 21:00:00

Implements FEAT-003 Feedback Collection (P1 priority).
Creates tables for comprehensive feedback management.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '009_feedback_collection_system'
down_revision = '008_member_management_system'
branch_labels = None
depends_on = None


def upgrade():
    """Create feedback collection tables."""
    
    # Create feedback table
    op.create_table(
        'feedback',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('user_email', sa.String(255), nullable=True),
        sa.Column('user_name', sa.String(200), nullable=True),
        sa.Column('type', sa.Enum('bug_report', 'feature_request', 'general_feedback', 'complaint', 'suggestion', 'question', name='feedbacktype'), nullable=False),
        sa.Column('category', sa.Enum('ui_ux', 'performance', 'data_quality', 'functionality', 'documentation', 'security', 'accessibility', 'other', name='feedbackcategory'), nullable=False),
        sa.Column('subject', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('page_url', sa.String(1000), nullable=True),
        sa.Column('browser_info', postgresql.JSONB(), nullable=True),
        sa.Column('session_data', postgresql.JSONB(), nullable=True),
        sa.Column('status', sa.Enum('pending', 'in_review', 'in_progress', 'resolved', 'closed', 'rejected', 'duplicate', name='feedbackstatus'), nullable=False),
        sa.Column('priority', sa.Enum('low', 'medium', 'high', 'critical', name='feedbackpriority'), nullable=False),
        sa.Column('assigned_to', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.Column('tags', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for feedback table
    op.create_index('idx_feedback_user_id', 'feedback', ['user_id'])
    op.create_index('idx_feedback_status', 'feedback', ['status'])
    op.create_index('idx_feedback_priority', 'feedback', ['priority'])
    op.create_index('idx_feedback_type', 'feedback', ['type'])
    op.create_index('idx_feedback_category', 'feedback', ['category'])
    op.create_index('idx_feedback_created_at', 'feedback', ['created_at'])
    op.create_index('idx_feedback_assigned_to', 'feedback', ['assigned_to'])
    
    # Create feedback_attachments table
    op.create_table(
        'feedback_attachments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('feedback_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('file_type', sa.String(100), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('file_url', sa.String(1000), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('uploaded_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['feedback_id'], ['feedback.id'], ),
        sa.ForeignKeyConstraint(['uploaded_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_attachment_feedback_id', 'feedback_attachments', ['feedback_id'])
    
    # Create feedback_responses table
    op.create_table(
        'feedback_responses',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('feedback_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('is_internal', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['feedback_id'], ['feedback.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_response_feedback_id', 'feedback_responses', ['feedback_id'])
    op.create_index('idx_response_user_id', 'feedback_responses', ['user_id'])
    op.create_index('idx_response_created_at', 'feedback_responses', ['created_at'])
    
    # Create feedback_votes table
    op.create_table(
        'feedback_votes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('feedback_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('vote_type', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['feedback_id'], ['feedback.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_vote_feedback_id', 'feedback_votes', ['feedback_id'])
    op.create_index('idx_vote_user_id', 'feedback_votes', ['user_id'])
    op.create_index('idx_vote_feedback_user', 'feedback_votes', ['feedback_id', 'user_id'], unique=True)
    
    # Create feedback_templates table
    op.create_table(
        'feedback_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('type', sa.Enum('bug_report', 'feature_request', 'general_feedback', 'complaint', 'suggestion', 'question', name='feedbacktype'), nullable=False),
        sa.Column('category', sa.Enum('ui_ux', 'performance', 'data_quality', 'functionality', 'documentation', 'security', 'accessibility', 'other', name='feedbackcategory'), nullable=False),
        sa.Column('fields', postgresql.JSONB(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('requires_auth', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('idx_template_name', 'feedback_templates', ['name'])
    op.create_index('idx_template_type', 'feedback_templates', ['type'])
    op.create_index('idx_template_active', 'feedback_templates', ['is_active'])
    
    # Insert default templates
    from sqlalchemy.sql import table, column
    import uuid
    
    templates_table = table(
        'feedback_templates',
        column('id', postgresql.UUID),
        column('name', sa.String),
        column('type', sa.String),
        column('category', sa.String),
        column('fields', postgresql.JSONB),
        column('is_active', sa.Boolean),
        column('requires_auth', sa.Boolean)
    )
    
    default_templates = [
        {
            'id': uuid.uuid4(),
            'name': 'Bug Report Form',
            'type': 'bug_report',
            'category': 'functionality',
            'fields': {
                'steps_to_reproduce': {
                    'type': 'textarea',
                    'label': 'Steps to Reproduce',
                    'required': True,
                    'placeholder': 'Please describe the steps to reproduce the issue'
                },
                'expected_behavior': {
                    'type': 'textarea',
                    'label': 'Expected Behavior',
                    'required': True
                },
                'actual_behavior': {
                    'type': 'textarea',
                    'label': 'Actual Behavior',
                    'required': True
                },
                'severity': {
                    'type': 'select',
                    'label': 'Severity',
                    'options': ['Low', 'Medium', 'High', 'Critical'],
                    'required': True
                }
            },
            'is_active': True,
            'requires_auth': False
        },
        {
            'id': uuid.uuid4(),
            'name': 'Feature Request Form',
            'type': 'feature_request',
            'category': 'functionality',
            'fields': {
                'feature_description': {
                    'type': 'textarea',
                    'label': 'Feature Description',
                    'required': True,
                    'placeholder': 'Describe the feature you would like to see'
                },
                'use_case': {
                    'type': 'textarea',
                    'label': 'Use Case',
                    'required': True,
                    'placeholder': 'How would this feature help you?'
                },
                'priority': {
                    'type': 'select',
                    'label': 'Priority',
                    'options': ['Nice to have', 'Important', 'Critical'],
                    'required': True
                }
            },
            'is_active': True,
            'requires_auth': False
        },
        {
            'id': uuid.uuid4(),
            'name': 'General Feedback Form',
            'type': 'general_feedback',
            'category': 'other',
            'fields': {
                'feedback_text': {
                    'type': 'textarea',
                    'label': 'Your Feedback',
                    'required': True,
                    'placeholder': 'Share your thoughts, suggestions, or comments'
                },
                'rating': {
                    'type': 'rating',
                    'label': 'Overall Experience',
                    'min': 1,
                    'max': 5,
                    'required': False
                }
            },
            'is_active': True,
            'requires_auth': False
        }
    ]
    
    op.bulk_insert(templates_table, default_templates)


def downgrade():
    """Drop feedback collection tables."""
    
    # Drop tables in reverse order due to foreign key constraints
    op.drop_index('idx_template_active', table_name='feedback_templates')
    op.drop_index('idx_template_type', table_name='feedback_templates')
    op.drop_index('idx_template_name', table_name='feedback_templates')
    op.drop_table('feedback_templates')
    
    op.drop_index('idx_vote_feedback_user', table_name='feedback_votes')
    op.drop_index('idx_vote_user_id', table_name='feedback_votes')
    op.drop_index('idx_vote_feedback_id', table_name='feedback_votes')
    op.drop_table('feedback_votes')
    
    op.drop_index('idx_response_created_at', table_name='feedback_responses')
    op.drop_index('idx_response_user_id', table_name='feedback_responses')
    op.drop_index('idx_response_feedback_id', table_name='feedback_responses')
    op.drop_table('feedback_responses')
    
    op.drop_index('idx_attachment_feedback_id', table_name='feedback_attachments')
    op.drop_table('feedback_attachments')
    
    op.drop_index('idx_feedback_assigned_to', table_name='feedback')
    op.drop_index('idx_feedback_created_at', table_name='feedback')
    op.drop_index('idx_feedback_category', table_name='feedback')
    op.drop_index('idx_feedback_type', table_name='feedback')
    op.drop_index('idx_feedback_priority', table_name='feedback')
    op.drop_index('idx_feedback_status', table_name='feedback')
    op.drop_index('idx_feedback_user_id', table_name='feedback')
    op.drop_table('feedback')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS feedbacktype')
    op.execute('DROP TYPE IF EXISTS feedbackstatus')
    op.execute('DROP TYPE IF EXISTS feedbackpriority')
    op.execute('DROP TYPE IF EXISTS feedbackcategory')