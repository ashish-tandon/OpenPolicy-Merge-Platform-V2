from sqlalchemy import Column, String, DateTime, Boolean, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid

class DataSource(Base):
    """Model for storing data source configurations."""
    
    __tablename__ = "data_sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)  # parliamentary, municipal, civic
    config = Column(JSON, nullable=False)  # Connection and configuration details
    is_active = Column(Boolean, default=True, nullable=False)
    last_sync = Column(DateTime(timezone=True), nullable=True)
    sync_frequency = Column(String(50), default="daily", nullable=False)  # daily, weekly, monthly
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Create indexes for efficient queries
    __table_args__ = (
        Index('idx_source_name', 'name'),
        Index('idx_source_type', 'type'),
        Index('idx_source_active', 'is_active'),
        Index('idx_source_last_sync', 'last_sync'),
    )
    
    def __repr__(self):
        return f"<DataSource(id={self.id}, name='{self.name}', type='{self.type}')>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "type": self.type,
            "config": self.config,
            "is_active": self.is_active,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "sync_frequency": self.sync_frequency,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
