"""Initial user service database schema

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('first_name', sa.String(length=255), nullable=False),
        sa.Column('last_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('postal_code', sa.String(length=10), nullable=True),
        sa.Column('gender', sa.String(length=10), nullable=True),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('date_of_birth', sa.DateTime(timezone=True), nullable=True),
        sa.Column('password_hash', sa.String(length=255), nullable=True),
        sa.Column('email_verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('phone_verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('two_factor_enabled', sa.Boolean(), nullable=False, default=False),
        sa.Column('two_factor_secret', sa.String(length=255), nullable=True),
        sa.Column('role', sa.Enum('NORMAL', 'ENTERPRISE', 'REPRESENTATIVE', 'MODERATOR', 'ADMIN', name='userrole'), nullable=False, default='NORMAL'),
        sa.Column('account_type', sa.Enum('CONSUMER', 'INTERNAL', 'TEST', name='accounttype'), nullable=False, default='CONSUMER'),
        sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'SUSPENDED', 'DELETED', name='userstatus'), nullable=False, default='ACTIVE'),
        sa.Column('avatar_url', sa.String(length=500), nullable=True),
        sa.Column('profile_picture', sa.Text(), nullable=True),
        sa.Column('preferences', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('account_deletion_reason', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_phone', 'users', ['phone'], unique=True)
    op.create_index('ix_users_role', 'users', ['role'])
    op.create_index('ix_users_status', 'users', ['status'])
    op.create_index('ix_users_created_at', 'users', ['created_at'])
    
    # Create OTPs table
    op.create_table('otps',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('otp', sa.String(length=10), nullable=False),
        sa.Column('otp_type', sa.String(length=20), nullable=False, default='sms'),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('used', sa.Boolean(), nullable=False, default=False),
        sa.Column('attempts', sa.Integer(), nullable=False, default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('used_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for OTPs
    op.create_index('ix_otps_phone', 'otps', ['phone'])
    op.create_index('ix_otps_expires_at', 'otps', ['expires_at'])
    
    # Create user_sessions table
    op.create_table('user_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('session_token', sa.String(length=500), nullable=False),
        sa.Column('refresh_token', sa.String(length=500), nullable=True),
        sa.Column('token_type', sa.String(length=20), nullable=False, default='jwt'),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('device_type', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for user_sessions
    op.create_index('ix_user_sessions_user_id', 'user_sessions', ['user_id'])
    op.create_index('ix_user_sessions_session_token', 'user_sessions', ['session_token'], unique=True)
    op.create_index('ix_user_sessions_refresh_token', 'user_sessions', ['refresh_token'], unique=True)
    
    # Create user engagement tables
    op.create_table('bill_votes_cast',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('bill_id', sa.String(length=255), nullable=False),
        sa.Column('vote_type', sa.String(length=50), nullable=False),
        sa.Column('vote_reason', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('saved_bills',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('bill_id', sa.String(length=255), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('representative_issues',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('representative_id', sa.String(length=255), nullable=False),
        sa.Column('issue_type', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, default='open'),
        sa.Column('priority', sa.String(length=20), nullable=False, default='medium'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('user_postal_code_history',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('postal_code', sa.String(length=10), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('province', sa.String(length=50), nullable=True),
        sa.Column('country', sa.String(length=50), nullable=True, default='Canada'),
        sa.Column('changed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('user_profile_pictures',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('image_data', sa.Text(), nullable=False),
        sa.Column('file_name', sa.String(length=255), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('mime_type', sa.String(length=100), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('user_account_deletions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('deletion_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for engagement tables
    op.create_index('ix_bill_votes_cast_user_id', 'bill_votes_cast', ['user_id'])
    op.create_index('ix_bill_votes_cast_bill_id', 'bill_votes_cast', ['bill_id'])
    op.create_index('ix_saved_bills_user_id', 'saved_bills', ['user_id'])
    op.create_index('ix_saved_bills_bill_id', 'saved_bills', ['bill_id'])
    op.create_index('ix_representative_issues_user_id', 'representative_issues', ['user_id'])
    op.create_index('ix_representative_issues_status', 'representative_issues', ['status'])
    op.create_index('ix_user_postal_code_history_user_id', 'user_postal_code_history', ['user_id'])
    op.create_index('ix_user_profile_pictures_user_id', 'user_profile_pictures', ['user_id'])
    op.create_index('ix_user_account_deletions_user_id', 'user_account_deletions', ['user_id'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('user_account_deletions')
    op.drop_table('user_profile_pictures')
    op.drop_table('user_postal_code_history')
    op.drop_table('representative_issues')
    op.drop_table('saved_bills')
    op.drop_table('bill_votes_cast')
    op.drop_table('user_sessions')
    op.drop_table('otps')
    op.drop_table('users')
    
    # Drop enums
    op.execute('DROP TYPE userrole')
    op.execute('DROP TYPE accounttype')
    op.execute('DROP TYPE userstatus')
