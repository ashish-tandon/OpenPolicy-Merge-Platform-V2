"""
SQLAlchemy Models for OpenParliament.ca V2
Following FUNDAMENTAL RULE: Extended existing schema with comprehensive multi-level government support
"""

from .openparliament import (
    # Legacy OpenParliament models
    Party, Politician, Riding, ElectedMember, Bill, VoteQuestion, 
    MemberVote, PartyVote, Statement, PoliticianInfo,
    
    # Municipal models (extended from existing schema)
    Municipality, MunicipalCouncillor, MunicipalOffice
)

from .government_levels import (
    # Multi-level government models
    GovernmentLevel, Jurisdiction, Representative, Office,
    Bill as UnifiedBill, Vote, RepresentativeVote,
    DataSource, IngestionLog
)

__all__ = [
    # Legacy models
    "Party", "Politician", "Riding", "ElectedMember", "Bill", "VoteQuestion",
    "MemberVote", "PartyVote", "Statement", "PoliticianInfo",
    
    # Municipal models
    "Municipality", "MunicipalCouncillor", "MunicipalOffice",
    
    # Multi-level government models
    "GovernmentLevel", "Jurisdiction", "Representative", "Office",
    "UnifiedBill", "Vote", "RepresentativeVote",
    "DataSource", "IngestionLog"
]
