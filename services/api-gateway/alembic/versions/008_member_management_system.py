"""
Member Management System

Revision ID: 008_member_management_system
Revises: 007_authentication_system
Create Date: 2025-08-23 20:00:00

Implements FEAT-015 Member Management (P0 priority).
Creates enhanced tables for comprehensive member management.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '008_member_management_system'
down_revision = '007_authentication_system'
branch_labels = None
depends_on = None


def upgrade():
    """Create member management tables."""
    
    # Create member_audits table
    op.create_table(
        'member_audits',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('member_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('changes', postgresql.JSONB(), nullable=True),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(), nullable=True),
        sa.ForeignKeyConstraint(['member_id'], ['openpolicy.members.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_member_audit_member_id', 'member_audits', ['member_id'])
    op.create_index('idx_member_audit_user_id', 'member_audits', ['user_id'])
    op.create_index('idx_member_audit_timestamp', 'member_audits', ['timestamp'])
    op.create_index('idx_member_audit_action', 'member_audits', ['action'])
    
    # Create member_imports table
    op.create_table(
        'member_imports',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('import_source', sa.String(100), nullable=False),
        sa.Column('import_type', sa.String(50), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('total_records', sa.Integer(), nullable=True),
        sa.Column('processed_records', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('updated_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('error_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('errors', postgresql.JSONB(), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create member_contacts table
    op.create_table(
        'member_contacts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('member_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('contact_type', sa.String(50), nullable=False),
        sa.Column('address_line1', sa.String(200), nullable=True),
        sa.Column('address_line2', sa.String(200), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('province', sa.String(50), nullable=True),
        sa.Column('postal_code', sa.String(20), nullable=True),
        sa.Column('country', sa.String(100), server_default='Canada', nullable=False),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('fax', sa.String(50), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('hours', postgresql.JSONB(), nullable=True),
        sa.Column('is_primary', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['member_id'], ['openpolicy.members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_member_contact_member_id', 'member_contacts', ['member_id'])
    op.create_index('idx_member_contact_type', 'member_contacts', ['contact_type'])
    
    # Create member_social_media table
    op.create_table(
        'member_social_media',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('member_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('platform', sa.String(50), nullable=False),
        sa.Column('handle', sa.String(100), nullable=False),
        sa.Column('url', sa.String(500), nullable=True),
        sa.Column('verified', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('follower_count', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('last_verified', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['member_id'], ['openpolicy.members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_member_social_member_id', 'member_social_media', ['member_id'])
    op.create_index('idx_member_social_platform', 'member_social_media', ['platform'])
    
    # Create member_education table
    op.create_table(
        'member_education',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('member_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('institution', sa.String(200), nullable=False),
        sa.Column('degree', sa.String(200), nullable=True),
        sa.Column('field_of_study', sa.String(200), nullable=True),
        sa.Column('start_year', sa.Integer(), nullable=True),
        sa.Column('end_year', sa.Integer(), nullable=True),
        sa.Column('graduated', sa.Boolean(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), server_default='0', nullable=False),
        sa.ForeignKeyConstraint(['member_id'], ['openpolicy.members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_member_education_member_id', 'member_education', ['member_id'])
    
    # Create member_professions table
    op.create_table(
        'member_professions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('member_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('organization', sa.String(200), nullable=True),
        sa.Column('industry', sa.String(100), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('is_current', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), server_default='0', nullable=False),
        sa.ForeignKeyConstraint(['member_id'], ['openpolicy.members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_member_profession_member_id', 'member_professions', ['member_id'])
    
    # Create member_tags table
    op.create_table(
        'member_tags',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('color', sa.String(7), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('idx_member_tag_name', 'member_tags', ['name'])
    op.create_index('idx_member_tag_category', 'member_tags', ['category'])
    
    # Create member_tag_associations table
    op.create_table(
        'member_tag_associations',
        sa.Column('member_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tag_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('tagged_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('tagged_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['member_id'], ['openpolicy.members.id'], ),
        sa.ForeignKeyConstraint(['tag_id'], ['member_tags.id'], ),
        sa.ForeignKeyConstraint(['tagged_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('member_id', 'tag_id')
    )
    
    # Create member_metrics table
    op.create_table(
        'member_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('member_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('bills_sponsored', sa.Integer(), server_default='0', nullable=False),
        sa.Column('bills_cosponsored', sa.Integer(), server_default='0', nullable=False),
        sa.Column('votes_total', sa.Integer(), server_default='0', nullable=False),
        sa.Column('votes_yea', sa.Integer(), server_default='0', nullable=False),
        sa.Column('votes_nay', sa.Integer(), server_default='0', nullable=False),
        sa.Column('votes_abstain', sa.Integer(), server_default='0', nullable=False),
        sa.Column('attendance_rate', sa.Float(), nullable=True),
        sa.Column('speeches_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('questions_asked', sa.Integer(), server_default='0', nullable=False),
        sa.Column('committee_memberships', sa.Integer(), server_default='0', nullable=False),
        sa.Column('twitter_followers', sa.Integer(), nullable=True),
        sa.Column('facebook_likes', sa.Integer(), nullable=True),
        sa.Column('social_engagement_score', sa.Float(), nullable=True),
        sa.Column('activity_score', sa.Float(), nullable=True),
        sa.Column('influence_score', sa.Float(), nullable=True),
        sa.Column('transparency_score', sa.Float(), nullable=True),
        sa.Column('last_calculated', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['member_id'], ['openpolicy.members.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('member_id')
    )
    op.create_index('idx_member_metrics_member_id', 'member_metrics', ['member_id'])
    op.create_index('idx_member_metrics_activity_score', 'member_metrics', ['activity_score'])
    op.create_index('idx_member_metrics_influence_score', 'member_metrics', ['influence_score'])
    
    # Insert default tags
    from sqlalchemy.sql import table, column
    import uuid
    
    tags_table = table(
        'member_tags',
        column('id', postgresql.UUID),
        column('name', sa.String),
        column('category', sa.String),
        column('description', sa.Text),
        column('color', sa.String)
    )
    
    default_tags = [
        # Roles
        {'id': uuid.uuid4(), 'name': 'Cabinet Minister', 'category': 'role', 'description': 'Member of the Cabinet', 'color': '#FF6B6B'},
        {'id': uuid.uuid4(), 'name': 'Parliamentary Secretary', 'category': 'role', 'description': 'Parliamentary Secretary', 'color': '#4ECDC4'},
        {'id': uuid.uuid4(), 'name': 'Committee Chair', 'category': 'role', 'description': 'Chairs a committee', 'color': '#45B7D1'},
        {'id': uuid.uuid4(), 'name': 'Party Leader', 'category': 'role', 'description': 'Leader of a political party', 'color': '#96CEB4'},
        {'id': uuid.uuid4(), 'name': 'Whip', 'category': 'role', 'description': 'Party Whip', 'color': '#FECA57'},
        
        # Topics
        {'id': uuid.uuid4(), 'name': 'Environment', 'category': 'topic', 'description': 'Environmental issues', 'color': '#26A69A'},
        {'id': uuid.uuid4(), 'name': 'Healthcare', 'category': 'topic', 'description': 'Healthcare policy', 'color': '#EF5350'},
        {'id': uuid.uuid4(), 'name': 'Economy', 'category': 'topic', 'description': 'Economic policy', 'color': '#42A5F5'},
        {'id': uuid.uuid4(), 'name': 'Education', 'category': 'topic', 'description': 'Education policy', 'color': '#AB47BC'},
        {'id': uuid.uuid4(), 'name': 'Indigenous Affairs', 'category': 'topic', 'description': 'Indigenous issues', 'color': '#FF7043'},
        
        # Other
        {'id': uuid.uuid4(), 'name': 'Rookie', 'category': 'other', 'description': 'First-term member', 'color': '#78909C'},
        {'id': uuid.uuid4(), 'name': 'Veteran', 'category': 'other', 'description': 'Long-serving member', 'color': '#5C6BC0'},
        {'id': uuid.uuid4(), 'name': 'Rising Star', 'category': 'other', 'description': 'Promising new member', 'color': '#FFD54F'}
    ]
    
    op.bulk_insert(tags_table, default_tags)


def downgrade():
    """Drop member management tables."""
    
    # Drop tables in reverse order due to foreign key constraints
    op.drop_index('idx_member_metrics_influence_score', table_name='member_metrics')
    op.drop_index('idx_member_metrics_activity_score', table_name='member_metrics')
    op.drop_index('idx_member_metrics_member_id', table_name='member_metrics')
    op.drop_table('member_metrics')
    
    op.drop_table('member_tag_associations')
    
    op.drop_index('idx_member_tag_category', table_name='member_tags')
    op.drop_index('idx_member_tag_name', table_name='member_tags')
    op.drop_table('member_tags')
    
    op.drop_index('idx_member_profession_member_id', table_name='member_professions')
    op.drop_table('member_professions')
    
    op.drop_index('idx_member_education_member_id', table_name='member_education')
    op.drop_table('member_education')
    
    op.drop_index('idx_member_social_platform', table_name='member_social_media')
    op.drop_index('idx_member_social_member_id', table_name='member_social_media')
    op.drop_table('member_social_media')
    
    op.drop_index('idx_member_contact_type', table_name='member_contacts')
    op.drop_index('idx_member_contact_member_id', table_name='member_contacts')
    op.drop_table('member_contacts')
    
    op.drop_table('member_imports')
    
    op.drop_index('idx_member_audit_action', table_name='member_audits')
    op.drop_index('idx_member_audit_timestamp', table_name='member_audits')
    op.drop_index('idx_member_audit_user_id', table_name='member_audits')
    op.drop_index('idx_member_audit_member_id', table_name='member_audits')
    op.drop_table('member_audits')