from sqlalchemy import Column, String, DateTime, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid

class EntityAuditLog(Base):
    """Model for tracking changes to parliamentary entities."""
    
    __tablename__ = "entity_audit_log"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False, index=True)
    action = Column(String(50), nullable=False, index=True)  # create, update, delete
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    changes = Column(JSON, nullable=True)  # Store what changed
    context_data = Column(JSON, nullable=True)  # Additional context
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Create indexes for efficient queries
    __table_args__ = (
        Index('idx_audit_entity_id', 'entity_id'),
        Index('idx_audit_entity_type', 'entity_type'),
        Index('idx_audit_action', 'action'),
        Index('idx_audit_user_id', 'user_id'),
        Index('idx_audit_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<EntityAuditLog(id={self.id}, entity_id={self.entity_id}, action='{self.action}')>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "entity_id": str(self.entity_id),
            "entity_type": self.entity_type,
            "action": self.action,
            "user_id": str(self.user_id) if self.user_id else None,
            "changes": self.changes,
            "context_data": self.context_data,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
