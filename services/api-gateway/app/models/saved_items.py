from sqlalchemy import Column, String, DateTime, Text, ARRAY, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database import Base

class SavedItem(Base):
    __tablename__ = "saved_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)
    item_id = Column(String, nullable=False, index=True)
    item_type = Column(String, nullable=False, index=True)  # 'bill', 'mp', 'debate', 'committee', 'vote'
    item_title = Column(String, nullable=False)
    item_url = Column(String, nullable=False)
    saved_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    notes = Column(Text, default="")
    tags = Column(ARRAY(String), default=[])
    
    # Composite index for efficient queries
    __table_args__ = (
        Index('idx_user_item_type', 'user_id', 'item_type'),
        Index('idx_user_item_id_type', 'user_id', 'item_id', 'item_type'),
        Index('idx_saved_at', 'saved_at'),
    )
    
    def __repr__(self):
        return f"<SavedItem(id={self.id}, user_id={self.user_id}, item_type={self.item_type}, item_title={self.item_title})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "item_id": self.item_id,
            "item_type": self.item_type,
            "item_title": self.item_title,
            "item_url": self.item_url,
            "saved_at": self.saved_at.isoformat() if self.saved_at else None,
            "notes": self.notes,
            "tags": self.tags or []
        }
