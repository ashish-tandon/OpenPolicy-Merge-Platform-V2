from sqlalchemy import Column, String, DateTime, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid

class ParliamentaryEntity(Base):
    """Model for storing parliamentary entities (MPs, bills, votes, etc.)."""
    
    __tablename__ = "parliamentary_entities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(50), nullable=False, index=True)
    data = Column(JSON, nullable=False)
    source = Column(String(100), nullable=False, index=True)
    source_id = Column(String(100), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Create composite index for efficient queries
    __table_args__ = (
        Index('idx_entity_type_source', 'type', 'source'),
        Index('idx_entity_source_id', 'source', 'source_id'),
        Index('idx_entity_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<ParliamentaryEntity(id={self.id}, type='{self.type}', source='{self.source}')>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "type": self.type,
            "data": self.data,
            "source": self.source,
            "source_id": self.source_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
