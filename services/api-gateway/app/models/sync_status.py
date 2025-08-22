from sqlalchemy import Column, String, DateTime, Integer, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid

class SyncStatus(Base):
    """Model for tracking data synchronization status."""
    
    __tablename__ = "sync_status"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_name = Column(String(100), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)  # pending, running, completed, failed
    last_sync = Column(DateTime(timezone=True), nullable=True)
    records_processed = Column(Integer, default=0, nullable=False)
    records_added = Column(Integer, default=0, nullable=False)
    records_updated = Column(Integer, default=0, nullable=False)
    records_deleted = Column(Integer, default=0, nullable=False)
    error_message = Column(String(500), nullable=True)
    sync_details = Column(JSON, nullable=True)  # Additional sync details
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Create indexes for efficient queries
    __table_args__ = (
        Index('idx_sync_source_name', 'source_name'),
        Index('idx_sync_status', 'status'),
        Index('idx_sync_last_sync', 'last_sync'),
        Index('idx_sync_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<SyncStatus(id={self.id}, source='{self.source_name}', status='{self.status}')>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "source_name": self.source_name,
            "status": self.status,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "records_processed": self.records_processed,
            "records_added": self.records_added,
            "records_updated": self.records_updated,
            "records_deleted": self.records_deleted,
            "error_message": self.error_message,
            "sync_details": self.sync_details,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
