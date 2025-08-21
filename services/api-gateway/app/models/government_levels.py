"""
Multi-Level Government Data Models for OpenParliament.ca V2
Following FUNDAMENTAL RULE: Extended existing schema with government level tracking

This schema supports:
- Federal (Parliament of Canada)
- Provincial/Territorial (10 provinces + 3 territories)  
- Municipal (100+ cities, towns, regions)
- Data provenance tracking for all levels
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped
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
    display_name = Column(String(100), nullable=False)  # Federal, Provincial/Territorial, Municipal
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Jurisdiction(Base):
    """Specific government jurisdictions within each level"""
    __tablename__ = "jurisdictions"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    level_id = Column(Integer, ForeignKey("public.government_levels.id"), nullable=False)
    name = Column(String(200), nullable=False)  # Canada, Ontario, Toronto, etc.
    short_name = Column(String(50))  # ON, TO, etc.
    ocd_division_id = Column(String(200))  # OpenCivicData division identifier
    census_code = Column(String(20))  # Statistics Canada code
    province_territory = Column(String(50))  # For municipal jurisdictions
    type = Column(String(100))  # country, province, city, town, region, etc.
    url = Column(String(500))  # Official government website
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    level: Mapped["GovernmentLevel"] = relationship("GovernmentLevel")
    representatives: Mapped[List["Representative"]] = relationship("Representative", back_populates="jurisdiction")
    bills: Mapped[List["Bill"]] = relationship("Bill", back_populates="jurisdiction")
    votes: Mapped[List["Vote"]] = relationship("Vote", back_populates="jurisdiction")
    
    __table_args__ = (
        UniqueConstraint('level_id', 'name', name='uq_jurisdiction_level_name'),
        Index('ix_jurisdictions_level_id', 'level_id'),
        Index('ix_jurisdictions_ocd_division_id', 'ocd_division_id'),
        Index('ix_jurisdictions_census_code', 'census_code'),
    )

# ============================================================================
# REPRESENTATIVES (Unified across all government levels)
# ============================================================================

class Representative(Base):
    """Unified representative model for all government levels"""
    __tablename__ = "representatives"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    jurisdiction_id = Column(Integer, ForeignKey("public.jurisdictions.id"), nullable=False)
    name = Column(String(200), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    party = Column(String(200))
    role = Column(String(200))  # MP, MPP, Mayor, Councillor, etc.
    district = Column(String(200))  # Electoral district, ward, etc.
    district_id = Column(String(100))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    gender = Column(String(20))
    photo_url = Column(String(500))
    personal_url = Column(String(500))
    preferred_languages = Column(JSONB)  # Array of language codes
    extras = Column(JSONB)  # Additional metadata
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    jurisdiction: Mapped["Jurisdiction"] = relationship("Jurisdiction", back_populates="representatives")
    offices: Mapped[List["Office"]] = relationship("Office", back_populates="representative")
    votes: Mapped[List["RepresentativeVote"]] = relationship("RepresentativeVote", back_populates="representative")
    
    __table_args__ = (
        Index('ix_representatives_jurisdiction_id', 'jurisdiction_id'),
        Index('ix_representatives_name', 'name'),
        Index('ix_representatives_party', 'party'),
        Index('ix_representatives_role', 'role'),
        Index('ix_representatives_district', 'district'),
        Index('ix_representatives_is_active', 'is_active'),
    )

class Office(Base):
    """Contact information and office details for representatives"""
    __tablename__ = "offices"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    representative_id = Column(Integer, ForeignKey("public.representatives.id"), nullable=False)
    type = Column(String(50), nullable=False)  # email, phone, fax, address, voice
    value = Column(String(500), nullable=False)
    note = Column(String(100))  # legislature, constituency, district, etc.
    label = Column(String(100))
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    representative: Mapped["Representative"] = relationship("Representative", back_populates="offices")
    
    __table_args__ = (
        Index('ix_offices_representative_id', 'representative_id'),
        Index('ix_offices_type', 'type'),
        Index('ix_offices_note', 'note'),
    )

# ============================================================================
# BILLS (Unified across all government levels)
# ============================================================================

class Bill(Base):
    """Unified bill model for all government levels"""
    __tablename__ = "bills"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    jurisdiction_id = Column(Integer, ForeignKey("public.jurisdictions.id"), nullable=False)
    bill_number = Column(String(100), nullable=False)
    title = Column(String(500), nullable=False)
    short_title = Column(String(200))
    summary = Column(Text)
    status = Column(String(100))  # introduced, passed, defeated, etc.
    introduced_date = Column(DateTime)
    passed_date = Column(DateTime)
    sponsor_id = Column(Integer, ForeignKey("public.representatives.id"))
    sponsor_name = Column(String(200))  # Denormalized for performance
    bill_type = Column(String(100))  # government, private member, etc.
    session = Column(String(100))
    parliament = Column(String(100))
    url = Column(String(500))
    extras = Column(JSONB)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    jurisdiction: Mapped["Jurisdiction"] = relationship("Jurisdiction", back_populates="bills")
    sponsor: Mapped["Representative"] = relationship("Representative")
    votes: Mapped[List["Vote"]] = relationship("Vote", back_populates="bill")
    
    __table_args__ = (
        Index('ix_bills_jurisdiction_id', 'jurisdiction_id'),
        Index('ix_bills_bill_number', 'bill_number'),
        Index('ix_bills_status', 'status'),
        Index('ix_bills_sponsor_id', 'sponsor_id'),
        Index('ix_bills_session', 'session'),
        UniqueConstraint('jurisdiction_id', 'bill_number', 'session', name='uq_bills_jurisdiction_number_session'),
    )

# ============================================================================
# VOTING (Unified across all government levels)
# ============================================================================

class Vote(Base):
    """Vote events for bills across all government levels"""
    __tablename__ = "votes"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    jurisdiction_id = Column(Integer, ForeignKey("public.jurisdictions.id"), nullable=False)
    bill_id = Column(Integer, ForeignKey("public.bills.id"))
    vote_number = Column(String(100))
    question = Column(String(500), nullable=False)
    result = Column(String(100))  # passed, defeated, tied
    vote_date = Column(DateTime)
    session = Column(String(100))
    parliament = Column(String(100))
    url = Column(String(500))
    extras = Column(JSONB)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    jurisdiction: Mapped["Jurisdiction"] = relationship("Jurisdiction", back_populates="votes")
    bill: Mapped["Bill"] = relationship("Bill", back_populates="votes")
    representative_votes: Mapped[List["RepresentativeVote"]] = relationship("RepresentativeVote", back_populates="vote")
    
    __table_args__ = (
        Index('ix_votes_jurisdiction_id', 'jurisdiction_id'),
        Index('ix_votes_bill_id', 'bill_id'),
        Index('ix_votes_result', 'result'),
        Index('ix_votes_vote_date', 'vote_date'),
        Index('ix_votes_session', 'session'),
    )

class RepresentativeVote(Base):
    """Individual representative votes on specific votes"""
    __tablename__ = "representative_votes"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    vote_id = Column(Integer, ForeignKey("public.votes.id"), nullable=False)
    representative_id = Column(Integer, ForeignKey("public.representatives.id"), nullable=False)
    vote_position = Column(String(50), nullable=False)  # yes, no, abstain, absent, paired
    vote_date = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    vote: Mapped["Vote"] = relationship("Vote", back_populates="representative_votes")
    representative: Mapped["Representative"] = relationship("Representative", back_populates="votes")
    
    __table_args__ = (
        Index('ix_representative_votes_vote_id', 'vote_id'),
        Index('ix_representative_votes_representative_id', 'representative_id'),
        Index('ix_representative_votes_vote_position', 'vote_position'),
        UniqueConstraint('vote_id', 'representative_id', name='uq_representative_votes_vote_representative'),
    )

# ============================================================================
# DATA PROVENANCE TRACKING
# ============================================================================

class DataSource(Base):
    """Track data sources and ingestion history"""
    __tablename__ = "data_sources"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    url = Column(String(500))
    type = Column(String(100))  # scraper, api, manual, etc.
    jurisdiction_id = Column(Integer, ForeignKey("public.jurisdictions.id"))
    last_updated = Column(DateTime)
    is_active = Column(Boolean, default=True)
    metadata_json = Column(JSONB)  # Scraper config, API keys, etc. (renamed from metadata)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    jurisdiction: Mapped["Jurisdiction"] = relationship("Jurisdiction")
    ingestion_logs: Mapped[List["IngestionLog"]] = relationship("IngestionLog", back_populates="data_source")
    
    __table_args__ = (
        Index('ix_data_sources_jurisdiction_id', 'jurisdiction_id'),
        Index('ix_data_sources_type', 'type'),
        Index('ix_data_sources_is_active', 'is_active'),
    )

class IngestionLog(Base):
    """Log of data ingestion operations"""
    __tablename__ = "ingestion_logs"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    data_source_id = Column(Integer, ForeignKey("public.data_sources.id"), nullable=False)
    operation = Column(String(100), nullable=False)  # scrape, ingest, update, etc.
    status = Column(String(50), nullable=False)  # success, failed, partial
    records_processed = Column(Integer, default=0)
    records_created = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    error_message = Column(Text)
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)
    duration_seconds = Column(Integer)
    metadata_json = Column(JSONB)  # Additional context (renamed from metadata)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    data_source: Mapped["DataSource"] = relationship("DataSource", back_populates="ingestion_logs")
    
    __table_args__ = (
        Index('ix_ingestion_logs_data_source_id', 'data_source_id'),
        Index('ix_ingestion_logs_status', 'status'),
        Index('ix_ingestion_logs_started_at', 'started_at'),
        Index('ix_ingestion_logs_operation', 'operation'),
    )
