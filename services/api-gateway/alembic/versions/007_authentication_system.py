"""
Authentication system tables

Revision ID: 007_authentication_system
Revises: 006_feature_flags_system
Create Date: 2025-08-23 19:00:00

Implements FEAT-014 Authentication System (P0 priority).
Creates tables for RBAC (Role-Based Access Control) system.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '007_authentication_system'
down_revision = '006_feature_flags_system'
branch_labels = None
depends_on = None


def upgrade():
    """Create authentication system tables."""
    
    # Create roles table
    op.create_table(
        'roles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_system', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('idx_role_name', 'roles', ['name'])
    op.create_index('idx_role_is_system', 'roles', ['is_system'])
    
    # Create permissions table
    op.create_table(
        'permissions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('resource', sa.String(100), nullable=False),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('resource', 'action', name='uq_permission_resource_action')
    )
    op.create_index('idx_permission_name', 'permissions', ['name'])
    op.create_index('idx_permission_resource', 'permissions', ['resource'])
    op.create_index('idx_permission_action', 'permissions', ['action'])
    
    # Create role_permissions association table
    op.create_table(
        'role_permissions',
        sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('permission_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )
    
    # Create user_roles association table
    op.create_table(
        'user_roles',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('granted_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column('granted_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['granted_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    
    # Create api_keys table
    op.create_table(
        'api_keys',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('key_hash', sa.String(255), nullable=False),
        sa.Column('prefix', sa.String(20), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('service_name', sa.String(100), nullable=True),
        sa.Column('scopes', postgresql.JSONB(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key_hash')
    )
    op.create_index('idx_api_key_prefix', 'api_keys', ['prefix'])
    op.create_index('idx_api_key_user_id', 'api_keys', ['user_id'])
    op.create_index('idx_api_key_service_name', 'api_keys', ['service_name'])
    op.create_index('idx_api_key_is_active', 'api_keys', ['is_active'])
    
    # Add authentication fields to users table
    op.add_column('users', sa.Column('email_verified', sa.Boolean(), server_default='false', nullable=True))
    op.add_column('users', sa.Column('email_verified_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('preferences', postgresql.JSONB(), nullable=True))
    
    # Update existing columns to be not nullable with defaults
    op.alter_column('users', 'email_verified', 
                    existing_type=sa.Boolean(),
                    nullable=False,
                    existing_server_default='false')
    
    # Insert default roles
    from sqlalchemy.sql import table, column
    import uuid
    
    roles_table = table(
        'roles',
        column('id', postgresql.UUID),
        column('name', sa.String),
        column('description', sa.Text),
        column('is_system', sa.Boolean)
    )
    
    default_roles = [
        {
            'id': uuid.uuid4(),
            'name': 'superuser',
            'description': 'Full system access',
            'is_system': True
        },
        {
            'id': uuid.uuid4(),
            'name': 'admin',
            'description': 'Administrative access',
            'is_system': True
        },
        {
            'id': uuid.uuid4(),
            'name': 'moderator',
            'description': 'Content moderation access',
            'is_system': True
        },
        {
            'id': uuid.uuid4(),
            'name': 'user',
            'description': 'Regular user access',
            'is_system': True
        }
    ]
    
    op.bulk_insert(roles_table, default_roles)
    
    # Insert default permissions
    permissions_table = table(
        'permissions',
        column('id', postgresql.UUID),
        column('name', sa.String),
        column('resource', sa.String),
        column('action', sa.String),
        column('description', sa.Text)
    )
    
    default_permissions = [
        # User management
        {'id': uuid.uuid4(), 'name': 'users.read', 'resource': 'users', 'action': 'read', 'description': 'View users'},
        {'id': uuid.uuid4(), 'name': 'users.write', 'resource': 'users', 'action': 'write', 'description': 'Create/update users'},
        {'id': uuid.uuid4(), 'name': 'users.delete', 'resource': 'users', 'action': 'delete', 'description': 'Delete users'},
        {'id': uuid.uuid4(), 'name': 'users.admin', 'resource': 'users', 'action': 'admin', 'description': 'Full user management'},
        
        # Bills
        {'id': uuid.uuid4(), 'name': 'bills.read', 'resource': 'bills', 'action': 'read', 'description': 'View bills'},
        {'id': uuid.uuid4(), 'name': 'bills.write', 'resource': 'bills', 'action': 'write', 'description': 'Create/update bills'},
        {'id': uuid.uuid4(), 'name': 'bills.delete', 'resource': 'bills', 'action': 'delete', 'description': 'Delete bills'},
        
        # Members
        {'id': uuid.uuid4(), 'name': 'members.read', 'resource': 'members', 'action': 'read', 'description': 'View members'},
        {'id': uuid.uuid4(), 'name': 'members.write', 'resource': 'members', 'action': 'write', 'description': 'Create/update members'},
        {'id': uuid.uuid4(), 'name': 'members.delete', 'resource': 'members', 'action': 'delete', 'description': 'Delete members'},
        
        # Votes
        {'id': uuid.uuid4(), 'name': 'votes.read', 'resource': 'votes', 'action': 'read', 'description': 'View votes'},
        {'id': uuid.uuid4(), 'name': 'votes.write', 'resource': 'votes', 'action': 'write', 'description': 'Create/update votes'},
        
        # Feature Flags
        {'id': uuid.uuid4(), 'name': 'feature_flags.read', 'resource': 'feature_flags', 'action': 'read', 'description': 'View feature flags'},
        {'id': uuid.uuid4(), 'name': 'feature_flags.write', 'resource': 'feature_flags', 'action': 'write', 'description': 'Manage feature flags'},
        
        # System
        {'id': uuid.uuid4(), 'name': 'system.admin', 'resource': 'system', 'action': 'admin', 'description': 'System administration'}
    ]
    
    op.bulk_insert(permissions_table, default_permissions)
    
    # Create role_permissions associations
    # This would normally be done programmatically with the actual IDs
    # For now, we'll leave this to be populated by the application


def downgrade():
    """Drop authentication system tables."""
    
    # Remove authentication fields from users table
    op.drop_column('users', 'preferences')
    op.drop_column('users', 'email_verified_at')
    op.drop_column('users', 'email_verified')
    
    # Drop tables in reverse order
    op.drop_index('idx_api_key_is_active', table_name='api_keys')
    op.drop_index('idx_api_key_service_name', table_name='api_keys')
    op.drop_index('idx_api_key_user_id', table_name='api_keys')
    op.drop_index('idx_api_key_prefix', table_name='api_keys')
    op.drop_table('api_keys')
    
    op.drop_table('user_roles')
    op.drop_table('role_permissions')
    
    op.drop_index('idx_permission_action', table_name='permissions')
    op.drop_index('idx_permission_resource', table_name='permissions')
    op.drop_index('idx_permission_name', table_name='permissions')
    op.drop_table('permissions')
    
    op.drop_index('idx_role_is_system', table_name='roles')
    op.drop_index('idx_role_name', table_name='roles')
    op.drop_table('roles')