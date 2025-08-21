"""
Simplified Multi-Level Government Data Models for OpenParliament.ca V2
Following FUNDAMENTAL RULE: Extended existing schema with government level tracking

This is a simplified version that avoids complex SQLAlchemy relationships
to get the API working quickly.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from typing import List

Base = declarative_base()

# ============================================================================
# GOVERNMENT LEVEL TRACKING
# ============================================================================

class GovernmentLevel(Base):
    """Government level classification (Federal, Provincial, Municipal)"""
    __tablename__ = "government_levels"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)  # federal, provincial, municipal
    description = Column(Text)
    level_order = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Jurisdiction(Base):
    """Specific government jurisdictions within each level"""
    __tablename__ = "jurisdictions"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    code = Column(String(100), nullable=False)
    government_level_id = Column(Integer, ForeignKey("public.government_levels.id"), nullable=False)
    province = Column(String(50))  # For municipal jurisdictions
    jurisdiction_type = Column(String(100))  # parliament, legislature, city_council, etc.
    website = Column(String(500))
    extras = Column(JSONB)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('ix_jurisdictions_government_level_id', 'government_level_id'),
        Index('ix_jurisdictions_code', 'code'),
        Index('ix_jurisdictions_province', 'province'),
    )

# ============================================================================
# REPRESENTATIVES (Unified across all government levels)
# ============================================================================

class Representative(Base):
    """Unified representative model for all government levels"""
    __tablename__ = "representatives"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    jurisdiction_id = Column(Integer, ForeignKey("public.jurisdictions.id"), nullable=False)
    party = Column(String(200))
    position = Column(String(100))  # mp, mla, mpp, mayor, councillor, etc.
    riding = Column(String(200))  # Electoral district, ward, etc.
    email = Column(String(200))
    phone = Column(String(100))
    website = Column(String(500))
    extras = Column(JSONB)
    metadata_json = Column(JSONB)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('ix_representatives_jurisdiction_id', 'jurisdiction_id'),
        Index('ix_representatives_name', 'name'),
        Index('ix_representatives_party', 'party'),
        Index('ix_representatives_position', 'position'),
    )

class Office(Base):
    """Contact information and office details for representatives"""
    __tablename__ = "offices"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    jurisdiction_id = Column(Integer, ForeignKey("public.jurisdictions.id"), nullable=False)
    office_type = Column(String(50), nullable=False)  # constituency, parliamentary, city_hall, etc.
    location = Column(String(500))
    phone = Column(String(100))
    email = Column(String(200))
    extras = Column(JSONB)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('ix_offices_jurisdiction_id', 'jurisdiction_id'),
        Index('ix_offices_office_type', 'office_type'),
    )

# ============================================================================
# BILLS (Unified across all government levels)
# ============================================================================

class Bill(Base):
    """Unified bill model for all government levels"""
    __tablename__ = "bills"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    jurisdiction_id = Column(Integer, ForeignKey("public.jurisdictions.id"), nullable=False)
    bill_number = Column(String(100), nullable=False)
    summary = Column(Text)
    status = Column(String(100))  # introduced, passed, defeated, etc.
    introduced_date = Column(DateTime)
    sponsor_id = Column(Integer, ForeignKey("public.representatives.id"))
    extras = Column(JSONB)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('ix_bills_jurisdiction_id', 'jurisdiction_id'),
        Index('ix_bills_bill_number', 'bill_number'),
        Index('ix_bills_status', 'status'),
        Index('ix_bills_sponsor_id', 'sponsor_id'),
    )

# ============================================================================
# VOTING (Unified across all government levels)
# ============================================================================

class Vote(Base):
    """Vote events for bills across all government levels"""
    __tablename__ = "votes"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey("public.bills.id"), nullable=False)
    representative_id = Column(Integer, ForeignKey("public.representatives.id"), nullable=False)
    vote_position = Column(String(50), nullable=False)  # yes, no, abstain, absent, paired
    vote_date = Column(DateTime, nullable=False)
    session = Column(String(100))
    extras = Column(JSONB)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('ix_votes_bill_id', 'bill_id'),
        Index('ix_votes_representative_id', 'representative_id'),
        Index('ix_votes_vote_position', 'vote_position'),
        Index('ix_votes_vote_date', 'vote_date'),
    )

# ============================================================================
# DATA SOURCES AND INGESTION TRACKING
# ============================================================================

class DataSource(Base):
    """Data source tracking for all government levels"""
    __tablename__ = "data_sources"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    jurisdiction_id = Column(Integer, ForeignKey("public.jurisdictions.id"), nullable=False)
    source_type = Column(String(100), nullable=False)  # api, scraper, manual, etc.
    url = Column(String(500))
    legacy_module = Column(String(100))
    legacy_class = Column(String(100))
    last_updated = Column(DateTime)
    extras = Column(JSONB)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('ix_data_sources_jurisdiction_id', 'jurisdiction_id'),
        Index('ix_data_sources_source_type', 'source_type'),
        Index('ix_data_sources_legacy_module', 'legacy_module'),
    )

class IngestionLog(Base):
    """Log of data ingestion operations"""
    __tablename__ = "ingestion_logs"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    data_source_id = Column(Integer, ForeignKey("public.data_sources.id"), nullable=False)
    ingestion_type = Column(String(100), nullable=False)  # full, incremental, update
    status = Column(String(50), nullable=False)  # success, failed, partial
    records_processed = Column(Integer, default=0)
    records_created = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    error_message = Column(Text)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime)
    extras = Column(JSONB)
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('ix_ingestion_logs_data_source_id', 'data_source_id'),
        Index('ix_ingestion_logs_status', 'status'),
        Index('ix_ingestion_logs_started_at', 'started_at'),
    )
