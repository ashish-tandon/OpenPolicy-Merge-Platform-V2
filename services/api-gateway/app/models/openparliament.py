"""
OpenParliament SQLAlchemy Models

Models for federal parliamentary data from the actual OpenParliament Django app.
These models are adapted from the working legacy codebase to work with SQLAlchemy.
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
    sponsored_bills: Mapped[List["Bill"]] = relationship("Bill", back_populates="sponsor_member", foreign_keys="Bill.sponsor_member_id")
    member_votes: Mapped[List["MemberVote"]] = relationship("MemberVote", back_populates="member")
    statements: Mapped[List["Statement"]] = relationship("Statement", back_populates="member")
    
    def __repr__(self):
        return f"<ElectedMember(id={self.id}, politician_id={self.politician_id})>"


class Bill(Base):
    """Federal legislation and bills."""
    
    __tablename__ = "bills_bill"
    __table_args__ = {"schema": "public"}
    
    id = Column(Integer, primary_key=True)
    name_en = Column(Text, nullable=False)
    number = Column(String(10), nullable=False)
    number_only = Column(Integer, nullable=False)
    sponsor_member_id = Column(Integer, ForeignKey("public.core_electedmember.id"))
    privatemember = Column(Boolean)
    sponsor_politician_id = Column(Integer, ForeignKey("public.core_politician.id"))
    law = Column(Boolean)
    added = Column(Date, nullable=False)
    institution = Column(String(1), nullable=False)
    name_fr = Column(Text, nullable=False)
    short_title_en = Column(Text, nullable=False)
    short_title_fr = Column(Text, nullable=False)
    status_date = Column(Date)
    introduced = Column(Date)
    text_docid = Column(Integer)
    status_code = Column(String(50), nullable=False)
    billstages_json = Column(Text)
    legisinfo_id = Column(Integer)
    library_summary_available = Column(Boolean, nullable=False)
    session_id = Column(String(4), nullable=False)  # This is a string like "45-1", not a foreign key
    latest_debate_date = Column(Date)
    
    # Relationships
    sponsor_member: Mapped[Optional["ElectedMember"]] = relationship("ElectedMember", back_populates="sponsored_bills", foreign_keys=[sponsor_member_id])
    sponsor_politician: Mapped[Optional["Politician"]] = relationship("Politician", back_populates="sponsored_bills", foreign_keys=[sponsor_politician_id])
    vote_questions: Mapped[List["VoteQuestion"]] = relationship("VoteQuestion", back_populates="bill")
    # Note: statements relationship removed since bill_debated_id is not a foreign key
    
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
