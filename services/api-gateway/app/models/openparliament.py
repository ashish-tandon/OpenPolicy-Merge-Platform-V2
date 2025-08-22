"""
OpenParliament SQLAlchemy Models

Models for federal parliamentary data that match the actual database schema.
These models are based on the real database structure, not simplified versions.
"""

from typing import List, Optional
from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, Text, ForeignKey, UUID, ARRAY
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from app.database import Base


class Jurisdiction(Base):
    """Jurisdiction/riding information."""

    __tablename__ = "jurisdictions"
    __table_args__ = {"schema": "openpolicy"}

    id = Column(PostgresUUID(as_uuid=True), primary_key=True)
    name = Column(String(200), nullable=False)
    province = Column(String(2), nullable=False)
    slug = Column(String(60), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    members: Mapped[List["Member"]] = relationship("Member", back_populates="jurisdiction")
    bills: Mapped[List["Bill"]] = relationship("Bill", back_populates="jurisdiction")
    parties: Mapped[List["Party"]] = relationship("Party", back_populates="jurisdiction")

    def __repr__(self):
        return f"<Jurisdiction(name='{self.name}', province='{self.province}')>"


class Party(Base):
    """Political party information."""

    __tablename__ = "parties"
    __table_args__ = {"schema": "openpolicy"}

    id = Column(PostgresUUID(as_uuid=True), primary_key=True)
    jurisdiction_id = Column(PostgresUUID(as_uuid=True), ForeignKey("openpolicy.jurisdictions.id"), nullable=False)
    name = Column(String(200), nullable=False)
    short_name = Column(String(50))
    color = Column(String(7))
    website = Column(String(500))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    jurisdiction: Mapped["Jurisdiction"] = relationship("Jurisdiction", back_populates="parties")
    members: Mapped[List["Member"]] = relationship("Member", back_populates="party")

    def __repr__(self):
        return f"<Party(name='{self.name}', short_name='{self.short_name}')>"


class Session(Base):
    """Parliamentary session information."""

    __tablename__ = "sessions"
    __table_args__ = {"schema": "openpolicy"}

    id = Column(PostgresUUID(as_uuid=True), primary_key=True)
    name = Column(String(200), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    bills: Mapped[List["Bill"]] = relationship("Bill", back_populates="session")

    def __repr__(self):
        return f"<Session(name='{self.name}')>"


class Member(Base):
    """Member of Parliament."""

    __tablename__ = "members"
    __table_args__ = {"schema": "openpolicy"}

    id = Column(PostgresUUID(as_uuid=True), primary_key=True)
    jurisdiction_id = Column(PostgresUUID(as_uuid=True), ForeignKey("openpolicy.jurisdictions.id"), nullable=False)
    party_id = Column(PostgresUUID(as_uuid=True), ForeignKey("openpolicy.parties.id"))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    full_name = Column(String(200))  # Generated column
    email = Column(String(255))
    phone = Column(String(20))
    website = Column(String(500))
    district = Column(String(200))
    role = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    jurisdiction: Mapped["Jurisdiction"] = relationship("Jurisdiction", back_populates="members")
    party: Mapped[Optional["Party"]] = relationship("Party", back_populates="members")

    def __repr__(self):
        return f"<Member(name='{self.full_name or f'{self.first_name} {self.last_name}'}')>"


class Bill(Base):
    """Federal bill information."""

    __tablename__ = "bills"
    __table_args__ = {"schema": "openpolicy"}

    id = Column(PostgresUUID(as_uuid=True), primary_key=True)
    jurisdiction_id = Column(PostgresUUID(as_uuid=True), ForeignKey("openpolicy.jurisdictions.id"), nullable=False)
    session_id = Column(PostgresUUID(as_uuid=True), ForeignKey("openpolicy.sessions.id"), nullable=False)
    bill_number = Column(String(50), nullable=False)
    title = Column(String(500), nullable=False)
    summary = Column(Text)
    full_text = Column(Text)
    status = Column(String(50), nullable=False, default='introduced')
    introduced_date = Column(Date)
    passed_date = Column(Date)
    royal_assent_date = Column(Date)
    sponsors = Column(ARRAY(Text))
    keywords = Column(ARRAY(Text))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    jurisdiction: Mapped["Jurisdiction"] = relationship("Jurisdiction", back_populates="bills")
    session: Mapped["Session"] = relationship("Session", back_populates="bills")
    votes: Mapped[List["Vote"]] = relationship("Vote", back_populates="bill")

    def __repr__(self):
        return f"<Bill(number='{self.bill_number}', title='{self.title}')>"


class Vote(Base):
    """Vote information."""

    __tablename__ = "votes"
    __table_args__ = {"schema": "openpolicy"}

    id = Column(PostgresUUID(as_uuid=True), primary_key=True)
    bill_id = Column(PostgresUUID(as_uuid=True), ForeignKey("openpolicy.bills.id"), nullable=False)
    vote_date = Column(DateTime(timezone=True), nullable=False)
    vote_type = Column(String(50), nullable=False)
    result = Column(String(20), nullable=False)
    yeas = Column(Integer, nullable=False, default=0)
    nays = Column(Integer, nullable=False, default=0)
    abstentions = Column(Integer, nullable=False, default=0)
    absent = Column(Integer, nullable=False, default=0)
    total_votes = Column(Integer)  # Generated column
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    bill: Mapped["Bill"] = relationship("Bill", back_populates="votes")

    def __repr__(self):
        return f"<Vote(bill_id={self.bill_id}, result='{self.result}')>"
