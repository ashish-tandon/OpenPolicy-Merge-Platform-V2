"""
OpenParliament SQLAlchemy Models

Models for federal parliamentary data from the actual OpenParliament Django app.
These models are adapted from the working legacy codebase to work with SQLAlchemy.

Following FUNDAMENTAL RULE: Extended with municipal models using existing patterns
"""

from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, Text, ForeignKey, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func

from app.database import Base


class Party(Base):
    """Political party information."""
    
    __tablename__ = "core_party"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    name_en = Column(String(100), nullable=False)
    slug = Column(String(10), nullable=False)
    short_name_en = Column(String(100), nullable=False)
    name_fr = Column(String(100), nullable=False)
    short_name_fr = Column(String(100), nullable=False)
    
    # Relationships
    elected_members: Mapped[List["ElectedMember"]] = relationship("ElectedMember", back_populates="party")
    
    def __repr__(self):
        return f"<Party(name='{self.name_en}', slug='{self.slug}')>"


class Politician(Base):
    """Core politician information."""
    
    __tablename__ = "core_politician"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    name_given = Column(String(50), nullable=False)
    name_family = Column(String(50), nullable=False)
    dob = Column(Date)
    gender = Column(String(1), nullable=False)
    headshot = Column(String(100))
    slug = Column(String(30), unique=True, nullable=False)
    headshot_thumbnail = Column(String(100))
    
    # Relationships
    elected_members: Mapped[List["ElectedMember"]] = relationship("ElectedMember", back_populates="politician")
    sponsored_bills: Mapped[List["Bill"]] = relationship("Bill", back_populates="sponsor_politician", foreign_keys="Bill.sponsor_politician_id")
    statements: Mapped[List["Statement"]] = relationship("Statement", back_populates="politician")
    # member_votes: Mapped[List["MemberVote"]] = relationship("MemberVote", back_populates="politician")
    
    def __repr__(self):
        return f"<Politician(name='{self.name}', slug='{self.slug}')>"


class Riding(Base):
    """Electoral district/riding information."""
    
    __tablename__ = "core_riding"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    name_en = Column(String(200), nullable=False)
    province = Column(String(2), nullable=False)
    slug = Column(String(60), unique=True, nullable=False)
    edid = Column(Integer)
    name_fr = Column(String(200), nullable=False)
    current = Column(Boolean, nullable=False)
    
    # Relationships
    elected_members: Mapped[List["ElectedMember"]] = relationship("ElectedMember", back_populates="riding")
    
    def __repr__(self):
        return f"<Riding(name='{self.name_en}', province='{self.province}')>"


class ElectedMember(Base):
    """Elected member of Parliament (MP)."""
    
    __tablename__ = "core_electedmember"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    politician_id = Column(Integer, ForeignKey("public.core_politician.id"), nullable=False)
    riding_id = Column(Integer, ForeignKey("public.core_riding.id"), nullable=False)
    party_id = Column(Integer, ForeignKey("public.core_party.id"), nullable=False)
    end_date = Column(Date)
    start_date = Column(Date, nullable=False)
    
    # Relationships
    politician: Mapped["Politician"] = relationship("Politician", back_populates="elected_members")
    riding: Mapped["Riding"] = relationship("Riding", back_populates="elected_members")
    party: Mapped["Party"] = relationship("Party", back_populates="elected_members")
    member_votes: Mapped[List["MemberVote"]] = relationship("MemberVote", back_populates="member")
    statements: Mapped[List["Statement"]] = relationship("Statement", back_populates="member")
    
    def __repr__(self):
        return f"<ElectedMember(politician_id={self.politician_id}, riding_id={self.riding_id})>"


class Bill(Base):
    """Federal bill information."""
    
    __tablename__ = "bills_bill"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    number = Column(String(20), nullable=False)
    name_en = Column(String(500), nullable=False)
    name_fr = Column(String(500), nullable=False)
    short_title_en = Column(String(200))
    short_title_fr = Column(String(200))
    summary_en = Column(Text)
    summary_fr = Column(Text)
    text_en = Column(Text)
    text_fr = Column(Text)
    status = Column(String(50), nullable=False)
    introduced = Column(Date)
    sponsor_politician_id = Column(Integer, ForeignKey("public.core_politician.id"))
    sponsor_member_id = Column(Integer, ForeignKey("public.core_electedmember.id"))
    sponsor_name = Column(String(100))
    sponsor_riding = Column(String(100))
    sponsor_party = Column(String(100))
    session = Column(String(20))
    law = Column(String(20))
    
    # Relationships
    sponsor_politician: Mapped["Politician"] = relationship("Politician", back_populates="sponsored_bills")
    vote_questions: Mapped[List["VoteQuestion"]] = relationship("VoteQuestion", back_populates="bill")
    
    def __repr__(self):
        return f"<Bill(number='{self.number}', name='{self.name_en}')>"


class VoteQuestion(Base):
    """Vote question on a bill."""
    
    __tablename__ = "bills_votequestion"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey("public.bills_bill.id"), nullable=False)
    date = Column(Date, nullable=False)
    number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    result = Column(String(50), nullable=False)
    
    # Relationships
    bill: Mapped["Bill"] = relationship("Bill", back_populates="vote_questions")
    member_votes: Mapped[List["MemberVote"]] = relationship("MemberVote", back_populates="vote_question")
    party_votes: Mapped[List["PartyVote"]] = relationship("PartyVote", back_populates="vote_question")
    
    def __repr__(self):
        return f"<VoteQuestion(bill_id={self.bill_id}, number={self.number}, date={self.date})>"


class MemberVote(Base):
    """Individual MP voting record."""
    
    __tablename__ = "bills_membervote"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    votequestion_id = Column(Integer, ForeignKey("public.bills_votequestion.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("public.core_electedmember.id"), nullable=False)
    politician_id = Column(Integer, ForeignKey("public.core_politician.id"), nullable=False)
    vote = Column(String(20), nullable=False)
    
    # Relationships
    vote_question: Mapped["VoteQuestion"] = relationship("VoteQuestion", back_populates="member_votes")
    member: Mapped["ElectedMember"] = relationship("ElectedMember", back_populates="member_votes")
    politician: Mapped["Politician"] = relationship("Politician")
    
    def __repr__(self):
        return f"<MemberVote(member_id={self.member_id}, vote='{self.vote}')>"


class PartyVote(Base):
    """Party voting record."""
    
    __tablename__ = "bills_partyvote"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    votequestion_id = Column(Integer, ForeignKey("public.bills_votequestion.id"), nullable=False)
    party_id = Column(Integer, ForeignKey("public.core_party.id"), nullable=False)
    vote = Column(String(20), nullable=False)
    
    # Relationships
    vote_question: Mapped["VoteQuestion"] = relationship("VoteQuestion", back_populates="party_votes")
    party: Mapped["Party"] = relationship("Party")
    
    def __repr__(self):
        return f"<PartyVote(party_id={self.party_id}, vote='{self.vote}')>"


class Statement(Base):
    """Parliamentary statement/hansard."""
    
    __tablename__ = "hansards_statement"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("public.core_electedmember.id"), nullable=False)
    politician_id = Column(Integer, ForeignKey("public.core_politician.id"), nullable=False)
    sequence = Column(Integer, nullable=False)
    h1_en = Column(Text)  # Main heading in English
    h2_en = Column(Text)  # Sub-heading in English
    h3_en = Column(Text)  # Sub-sub-heading in English
    content_en = Column(Text)  # Main content in English
    time = Column(DateTime(timezone=True))
    bill_debated_id = Column(Integer)  # Reference to debated bill
    
    # Relationships
    member: Mapped["ElectedMember"] = relationship("ElectedMember", back_populates="statements")
    politician: Mapped["Politician"] = relationship("Politician", back_populates="statements")
    # Note: bill_debated_id is not a foreign key, just a reference
    
    def __repr__(self):
        return f"<Statement(member_id={self.member_id}, sequence={self.sequence})>"


class PoliticianInfo(Base):
    """Key-value store for attributes of a Politician."""
    
    __tablename__ = "core_politicianinfo"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    politician_id = Column(Integer, ForeignKey("public.core_politician.id"), nullable=False)
    schema = Column(String(40), nullable=False, index=True)
    value = Column(Text, nullable=False)
    created = Column(DateTime, default=func.now())
    
    # Relationships
    politician: Mapped["Politician"] = relationship("Politician")
    
    def __repr__(self):
        return f"<PoliticianInfo(politician_id={self.politician_id}, schema='{self.schema}')>"


# ============================================================================
# MUNICIPAL MODELS - Following FUNDAMENTAL RULE: Extended existing schema
# ============================================================================

class Municipality(Base):
    """Municipality information from legacy scrapers."""
    
    __tablename__ = "municipalities"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    division_id = Column(String(100))  # OCD division identifier
    division_name = Column(String(200))
    classification = Column(String(50), default="legislature")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    councillors: Mapped[List["MunicipalCouncillor"]] = relationship("MunicipalCouncillor", back_populates="municipality")
    
    def __repr__(self):
        return f"<Municipality(name='{self.name}', division_id='{self.division_id}')>"


class MunicipalCouncillor(Base):
    """Municipal councillor information from legacy scrapers."""
    
    __tablename__ = "municipal_councillors"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    municipality = Column(String(100), ForeignKey("public.municipalities.name"), nullable=False)
    municipality_name = Column(String(200))
    division_id = Column(String(100))
    division_name = Column(String(200))
    classification = Column(String(50), default="legislature")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    municipality_rel: Mapped["Municipality"] = relationship("Municipality", back_populates="councillors")
    offices: Mapped[List["MunicipalOffice"]] = relationship("MunicipalOffice", back_populates="councillor")
    
    def __repr__(self):
        return f"<MunicipalCouncillor(name='{self.name}', municipality='{self.municipality}')>"


class MunicipalOffice(Base):
    """Municipal office/contact information from legacy scrapers."""
    
    __tablename__ = "municipal_offices"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    councillor_id = Column(Integer, ForeignKey("public.municipal_councillors.id"), nullable=False)
    type = Column(String(50), nullable=False)  # email, phone, address, etc.
    value = Column(String(500), nullable=False)  # actual value (email address, phone number, etc.)
    note = Column(String(100))  # office, residence, etc.
    label = Column(String(100))  # additional label
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    councillor: Mapped["MunicipalCouncillor"] = relationship("MunicipalCouncillor", back_populates="offices")
    
    def __repr__(self):
        return f"<MunicipalOffice(type='{self.type}', value='{self.value}')>"
