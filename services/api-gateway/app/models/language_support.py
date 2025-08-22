"""
Language Support Models for OpenPolicy V2

Comprehensive models for bilingual (French/English) language support.
Implements P1 priority feature for legal compliance and accessibility.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, ForeignKey, Index, UniqueConstraint, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base


class Language(Base):
    """Model for supported languages."""
    
    __tablename__ = "languages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    language_code = Column(String(10), nullable=False, unique=True)  # en, fr
    language_name = Column(String(100), nullable=False)  # English, Français
    language_name_native = Column(String(100), nullable=False)  # English, Français
    is_active = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    direction = Column(String(10), default="ltr", nullable=False)  # ltr, rtl
    date_format = Column(String(50), default="YYYY-MM-DD", nullable=False)
    time_format = Column(String(50), default="24h", nullable=False)
    number_format = Column(String(50), default="1,234.56", nullable=False)
    currency_code = Column(String(3), default="CAD", nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    translations = relationship("Translation", back_populates="language", cascade="all, delete-orphan")
    user_preferences = relationship("UserLanguagePreference", back_populates="language", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('ix_languages_language_code', 'language_code'),
        Index('ix_languages_is_active', 'is_active'),
        Index('ix_languages_is_default', 'is_default'),
    )


class Translation(Base):
    """Model for storing translations of UI text and content."""
    
    __tablename__ = "translations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id"), nullable=False)
    translation_key = Column(String(500), nullable=False)  # e.g., "bills.title", "navigation.home"
    translation_value = Column(Text, nullable=False)  # The actual translated text
    translation_context = Column(String(200), nullable=True)  # Context for the translation
    translation_notes = Column(Text, nullable=True)  # Notes for translators
    is_approved = Column(Boolean, default=False, nullable=False)  # Translation approval status
    approved_by = Column(String(100), nullable=True)  # Who approved the translation
    approved_at = Column(DateTime, nullable=True)  # When it was approved
    version = Column(Integer, default=1, nullable=False)  # Translation version
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    language = relationship("Language", back_populates="translations")
    
    # Indexes and constraints
    __table_args__ = (
        Index('ix_translations_language_id', 'language_id'),
        Index('ix_translations_translation_key', 'translation_key'),
        Index('ix_translations_is_approved', 'is_approved'),
        Index('ix_translations_version', 'version'),
        UniqueConstraint('language_id', 'translation_key', 'version', name='uq_translation_lang_key_version'),
    )


class UserLanguagePreference(Base):
    """Model for storing user language preferences."""
    
    __tablename__ = "user_language_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id"), nullable=False)
    is_primary = Column(Boolean, default=True, nullable=False)  # Primary language preference
    is_secondary = Column(Boolean, default=False, nullable=False)  # Secondary language preference
    proficiency_level = Column(String(20), default="fluent", nullable=False)  # fluent, intermediate, basic
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    language = relationship("Language", back_populates="user_preferences")
    
    # Indexes and constraints
    __table_args__ = (
        Index('ix_user_language_preferences_user_id', 'user_id'),
        Index('ix_user_language_preferences_language_id', 'language_id'),
        Index('ix_user_language_preferences_is_primary', 'is_primary'),
        UniqueConstraint('user_id', 'language_id', name='uq_user_language_preference'),
    )


class ContentTranslation(Base):
    """Model for storing translations of dynamic content."""
    
    __tablename__ = "content_translations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_type = Column(String(100), nullable=False)  # bill, vote, committee, member, etc.
    content_id = Column(String(100), nullable=False)  # ID of the content being translated
    language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id"), nullable=False)
    field_name = Column(String(100), nullable=False)  # name_en, description_en, summary_en, etc.
    translated_value = Column(Text, nullable=False)  # The translated content
    translation_status = Column(String(20), default="draft", nullable=False)  # draft, in_review, approved, published
    translator_id = Column(String(100), nullable=True)  # Who translated this content
    reviewer_id = Column(String(100), nullable=True)  # Who reviewed this translation
    review_notes = Column(Text, nullable=True)  # Review comments and notes
    translation_quality = Column(String(20), nullable=True)  # excellent, good, fair, poor
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    language = relationship("Language", foreign_keys=[language_id])
    
    # Indexes and constraints
    __table_args__ = (
        Index('ix_content_translations_content_type', 'content_type'),
        Index('ix_content_translations_content_id', 'content_id'),
        Index('ix_content_translations_language_id', 'language_id'),
        Index('ix_content_translations_field_name', 'field_name'),
        Index('ix_content_translations_translation_status', 'translation_status'),
        UniqueConstraint('content_type', 'content_id', 'language_id', 'field_name', name='uq_content_translation_unique'),
    )


class LanguageContext(Base):
    """Model for storing language-specific context and settings."""
    
    __tablename__ = "language_contexts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id"), nullable=False)
    context_key = Column(String(200), nullable=False)  # e.g., "parliament", "government", "legal"
    context_value = Column(JSONB, nullable=False)  # Context-specific settings and data
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    language = relationship("Language", foreign_keys=[language_id])
    
    # Indexes and constraints
    __table_args__ = (
        Index('ix_language_contexts_language_id', 'language_id'),
        Index('ix_language_contexts_context_key', 'context_key'),
        Index('ix_language_contexts_is_active', 'is_active'),
        UniqueConstraint('language_id', 'context_key', name='uq_language_context_unique'),
    )


class TranslationMemory(Base):
    """Model for storing translation memory to improve consistency and efficiency."""
    
    __tablename__ = "translation_memory"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id"), nullable=False)
    target_language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id"), nullable=False)
    source_text = Column(Text, nullable=False)  # Original text
    target_text = Column(Text, nullable=False)  # Translated text
    source_hash = Column(String(64), nullable=False)  # Hash of source text for quick lookup
    context = Column(String(200), nullable=True)  # Context where this translation was used
    domain = Column(String(100), nullable=True)  # Domain/field of the translation
    confidence_score = Column(Integer, default=100, nullable=False)  # Confidence in the translation quality
    usage_count = Column(Integer, default=1, nullable=False)  # How many times this translation was used
    last_used = Column(DateTime, server_default=func.now(), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    source_language = relationship("Language", foreign_keys=[source_language_id])
    target_language = relationship("Language", foreign_keys=[target_language_id])
    
    # Indexes and constraints
    __table_args__ = (
        Index('ix_translation_memory_source_language_id', 'source_language_id'),
        Index('ix_translation_memory_target_language_id', 'target_language_id'),
        Index('ix_translation_memory_source_hash', 'source_hash'),
        Index('ix_translation_memory_confidence_score', 'confidence_score'),
        Index('ix_translation_memory_usage_count', 'usage_count'),
        Index('ix_translation_memory_last_used', 'last_used'),
        UniqueConstraint('source_language_id', 'target_language_id', 'source_hash', name='uq_translation_memory_unique'),
    )


class LanguageAnalytics(Base):
    """Model for tracking language usage and preferences analytics."""
    
    __tablename__ = "language_analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    language_id = Column(UUID(as_uuid=True), ForeignKey("languages.id"), nullable=False)
    analytics_date = Column(DateTime, nullable=False)  # Date of analytics record
    daily_active_users = Column(Integer, default=0, nullable=False)  # Users who used this language today
    daily_page_views = Column(Integer, default=0, nullable=False)  # Page views in this language
    daily_translations_requested = Column(Integer, default=0, nullable=False)  # Translation requests
    daily_content_created = Column(Integer, default=0, nullable=False)  # Content created in this language
    daily_content_updated = Column(Integer, default=0, nullable=False)  # Content updated in this language
    translation_quality_score = Column(Float, default=0.0, nullable=False)  # Average translation quality
    user_satisfaction_score = Column(Float, default=0.0, nullable=False)  # User satisfaction with language
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationships
    language = relationship("Language", foreign_keys=[language_id])
    
    # Indexes
    __table_args__ = (
        Index('ix_language_analytics_language_id', 'language_id'),
        Index('ix_language_analytics_analytics_date', 'analytics_date'),
        Index('ix_language_analytics_daily_active_users', 'daily_active_users'),
    )
