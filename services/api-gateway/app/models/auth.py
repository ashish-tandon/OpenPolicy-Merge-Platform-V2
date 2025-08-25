"""
Authentication and Authorization Models

Models for Role-Based Access Control (RBAC) system.
Implements FEAT-014 Authentication System (P0 priority).
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from typing import List, Dict, Any
from datetime import datetime


# Association tables
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE')),
    Column('permission_id', UUID(as_uuid=True), ForeignKey('permissions.id', ondelete='CASCADE')),
    Column('created_at', DateTime, server_default=func.now())
)

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE')),
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE')),
    Column('granted_at', DateTime, server_default=func.now()),
    Column('granted_by', UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'))
)


class Role(Base):
    """Model for user roles."""
    
    __tablename__ = "roles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_system = Column(Boolean, default=False, nullable=False, index=True)  # System roles can't be deleted
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    users = relationship("User", secondary=user_roles, back_populates="roles")
    
    def has_permission(self, resource: str, action: str) -> bool:
        """Check if role has specific permission."""
        for permission in self.permissions:
            if permission.resource == resource and permission.action == action:
                return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "is_system": self.is_system,
            "permissions": [p.to_dict() for p in self.permissions],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class Permission(Base):
    """Model for permissions."""
    
    __tablename__ = "permissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False, index=True)
    resource = Column(String(100), nullable=False, index=True)  # e.g., 'bills', 'members', 'users'
    action = Column(String(50), nullable=False, index=True)  # e.g., 'read', 'write', 'delete', 'admin'
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('resource', 'action', name='uq_permission_resource_action'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "resource": self.resource,
            "action": self.action,
            "description": self.description,
            "created_at": self.created_at.isoformat()
        }


class APIKey(Base):
    """Model for API keys used in service-to-service authentication."""
    
    __tablename__ = "api_keys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)  # Descriptive name
    key_hash = Column(String(255), unique=True, nullable=False)  # Hashed API key
    prefix = Column(String(20), nullable=False, index=True)  # Key prefix for identification
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    service_name = Column(String(100), nullable=True, index=True)  # For service accounts
    scopes = Column(JSONB, nullable=True)  # List of allowed scopes/permissions
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], backref="api_keys")
    creator = relationship("User", foreign_keys=[created_by])
    
    def is_expired(self) -> bool:
        """Check if API key is expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    def has_scope(self, scope: str) -> bool:
        """Check if API key has specific scope."""
        if not self.scopes:
            return True  # No scopes means full access
        return scope in self.scopes
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (safe for API responses)."""
        return {
            "id": str(self.id),
            "name": self.name,
            "prefix": self.prefix,
            "user_id": str(self.user_id) if self.user_id else None,
            "service_name": self.service_name,
            "scopes": self.scopes,
            "is_active": self.is_active,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "created_at": self.created_at.isoformat()
        }


# Default roles and permissions
DEFAULT_ROLES = [
    {
        "name": "superuser",
        "description": "Full system access",
        "is_system": True
    },
    {
        "name": "admin",
        "description": "Administrative access",
        "is_system": True
    },
    {
        "name": "moderator",
        "description": "Content moderation access",
        "is_system": True
    },
    {
        "name": "user",
        "description": "Regular user access",
        "is_system": True
    }
]

DEFAULT_PERMISSIONS = [
    # User management
    {"name": "users.read", "resource": "users", "action": "read", "description": "View users"},
    {"name": "users.write", "resource": "users", "action": "write", "description": "Create/update users"},
    {"name": "users.delete", "resource": "users", "action": "delete", "description": "Delete users"},
    {"name": "users.admin", "resource": "users", "action": "admin", "description": "Full user management"},
    
    # Bills
    {"name": "bills.read", "resource": "bills", "action": "read", "description": "View bills"},
    {"name": "bills.write", "resource": "bills", "action": "write", "description": "Create/update bills"},
    {"name": "bills.delete", "resource": "bills", "action": "delete", "description": "Delete bills"},
    
    # Members
    {"name": "members.read", "resource": "members", "action": "read", "description": "View members"},
    {"name": "members.write", "resource": "members", "action": "write", "description": "Create/update members"},
    {"name": "members.delete", "resource": "members", "action": "delete", "description": "Delete members"},
    
    # Votes
    {"name": "votes.read", "resource": "votes", "action": "read", "description": "View votes"},
    {"name": "votes.write", "resource": "votes", "action": "write", "description": "Create/update votes"},
    
    # Feature Flags
    {"name": "feature_flags.read", "resource": "feature_flags", "action": "read", "description": "View feature flags"},
    {"name": "feature_flags.write", "resource": "feature_flags", "action": "write", "description": "Manage feature flags"},
    
    # System
    {"name": "system.admin", "resource": "system", "action": "admin", "description": "System administration"}
]

# Role-Permission mappings
DEFAULT_ROLE_PERMISSIONS = {
    "superuser": ["*"],  # All permissions
    "admin": [
        "users.read", "users.write", "users.admin",
        "bills.read", "bills.write", "bills.delete",
        "members.read", "members.write", "members.delete",
        "votes.read", "votes.write",
        "feature_flags.read", "feature_flags.write"
    ],
    "moderator": [
        "users.read",
        "bills.read", "bills.write",
        "members.read", "members.write",
        "votes.read", "votes.write"
    ],
    "user": [
        "bills.read",
        "members.read",
        "votes.read"
    ]
}

# Set up the User relationship after models are defined
# This avoids circular import issues
def setup_user_relationship():
    """Set up the relationship between User and Role models."""
    from app.models.users import User
    User.roles = relationship("Role", secondary=user_roles, back_populates="users")