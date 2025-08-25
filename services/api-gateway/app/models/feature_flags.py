"""
Feature Flags Models for OpenPolicy V2

Unified feature flag system for managing feature toggles, A/B testing,
gradual rollouts, and environment-specific configurations.
Implements FEAT-004 (P0 priority).
"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, ForeignKey, Index, UniqueConstraint, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime

from app.database import Base


class FeatureFlag(Base):
    """Model for feature flag configurations."""
    
    __tablename__ = "feature_flags"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic flag information
    feature_name = Column(String(200), nullable=False, unique=True)  # Unique feature identifier
    feature_description = Column(Text, nullable=True)  # Feature description
    flag_type = Column(String(50), default="feature", nullable=False)  # feature, experiment, operational, permission
    
    # Status and configuration
    is_enabled = Column(Boolean, default=False, nullable=False)  # Global on/off switch
    rollout_percentage = Column(Integer, default=0, nullable=False)  # Percentage rollout (0-100)
    
    # Targeting and rules
    targeting_rules = Column(JSONB, nullable=True)  # Complex targeting rules
    user_overrides = Column(JSONB, nullable=True)  # User-specific overrides
    environments = Column(JSONB, default=["all"], nullable=False)  # Enabled environments
    
    # Feature configuration
    feature_config = Column(JSONB, nullable=True)  # Feature-specific configuration
    dependencies = Column(JSONB, nullable=True)  # Other flags this depends on
    
    # Time-based controls
    start_date = Column(DateTime, nullable=True)  # When to start showing feature
    end_date = Column(DateTime, nullable=True)  # When to stop showing feature
    
    # Legacy PWA support (optional)
    manifest_id = Column(UUID(as_uuid=True), ForeignKey("pwa_manifests.id"), nullable=True)
    browser_support = Column(JSONB, nullable=True)  # Browser support matrix
    platform_support = Column(JSONB, nullable=True)  # Platform support matrix
    
    # Metadata
    created_by = Column(String(100), nullable=True)  # Who created the flag
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    evaluations = relationship("FeatureEvaluation", back_populates="flag", cascade="all, delete-orphan")
    changes = relationship("FeatureFlagChange", back_populates="flag", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_feature_flags_feature_name', 'feature_name'),
        Index('ix_feature_flags_is_enabled', 'is_enabled'),
        Index('ix_feature_flags_flag_type', 'flag_type'),
        Index('ix_feature_flags_rollout_percentage', 'rollout_percentage'),
        Index('ix_feature_flags_start_date', 'start_date'),
        Index('ix_feature_flags_end_date', 'end_date'),
        Index('ix_feature_flags_manifest_id', 'manifest_id'),
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "id": str(self.id),
            "feature_name": self.feature_name,
            "feature_description": self.feature_description,
            "flag_type": self.flag_type,
            "is_enabled": self.is_enabled,
            "rollout_percentage": self.rollout_percentage,
            "targeting_rules": self.targeting_rules,
            "environments": self.environments,
            "feature_config": self.feature_config,
            "dependencies": self.dependencies,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


class FeatureEvaluation(Base):
    """Model for tracking feature flag evaluations."""
    
    __tablename__ = "feature_evaluations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flag_id = Column(UUID(as_uuid=True), ForeignKey("feature_flags.id"), nullable=False)
    user_id = Column(String(255), nullable=True)  # User identifier
    evaluation_result = Column(Boolean, nullable=False)  # Evaluation result
    evaluation_context = Column(JSONB, nullable=True)  # Context used for evaluation
    evaluated_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    flag = relationship("FeatureFlag", back_populates="evaluations")
    
    # Indexes
    __table_args__ = (
        Index('ix_feature_evaluations_flag_id', 'flag_id'),
        Index('ix_feature_evaluations_user_id', 'user_id'),
        Index('ix_feature_evaluations_evaluated_at', 'evaluated_at'),
    )


class FeatureFlagChange(Base):
    """Model for auditing feature flag changes."""
    
    __tablename__ = "feature_flag_changes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flag_id = Column(UUID(as_uuid=True), ForeignKey("feature_flags.id"), nullable=False)
    changed_by = Column(String(255), nullable=False)  # Who made the change
    change_type = Column(String(50), nullable=False)  # create, update, delete, toggle
    old_value = Column(JSONB, nullable=True)  # Previous state
    new_value = Column(JSONB, nullable=True)  # New state
    changed_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    flag = relationship("FeatureFlag", back_populates="changes")
    
    # Indexes
    __table_args__ = (
        Index('ix_feature_flag_changes_flag_id', 'flag_id'),
        Index('ix_feature_flag_changes_changed_by', 'changed_by'),
        Index('ix_feature_flag_changes_changed_at', 'changed_at'),
    )