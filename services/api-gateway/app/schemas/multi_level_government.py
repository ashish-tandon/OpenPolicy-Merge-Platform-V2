"""
Multi-Level Government API Schemas

Schemas for the unified multi-level government data API endpoints.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class GovernmentLevelEnum(str, Enum):
    """Government level enumeration"""
    FEDERAL = "federal"
    PROVINCIAL = "provincial"
    MUNICIPAL = "municipal"


class JurisdictionTypeEnum(str, Enum):
    """Jurisdiction type enumeration"""
    LEGISLATURE = "legislature"
    PARLIAMENT = "parliament"
    CITY_COUNCIL = "city_council"
    TOWN_COUNCIL = "town_council"
    REGIONAL_COUNCIL = "regional_council"
    FIRST_NATIONS = "first_nations"


class RepresentativePositionEnum(str, Enum):
    """Representative position enumeration"""
    MP = "mp"
    MLA = "mla"
    MPP = "mpp"
    MAYOR = "mayor"
    COUNCILLOR = "councillor"
    DEPUTY_MAYOR = "deputy_mayor"
    CHAIR = "chair"
    DEPUTY_CHAIR = "deputy_chair"


class OfficeTypeEnum(str, Enum):
    """Office type enumeration"""
    CONSTITUENCY = "constituency"
    PARLIAMENTARY = "parliamentary"
    CITY_HALL = "city_hall"
    TOWN_HALL = "town_hall"
    REGIONAL_OFFICE = "regional_office"
    LEGISLATIVE = "legislative"


class BillStatusEnum(str, Enum):
    """Bill status enumeration"""
    INTRODUCED = "introduced"
    FIRST_READING = "first_reading"
    SECOND_READING = "second_reading"
    THIRD_READING = "third_reading"
    COMMITTEE = "committee"
    ROYAL_ASSENT = "royal_assent"
    ENACTED = "enacted"
    DEFEATED = "defeated"
    WITHDRAWN = "withdrawn"


class VotePositionEnum(str, Enum):
    """Vote position enumeration"""
    YES = "yes"
    NO = "no"
    ABSTAIN = "abstain"
    ABSENT = "absent"
    PAIRED = "paired"


# Base Models
class GovernmentLevelBase(BaseModel):
    """Base government level model"""
    name: str = Field(..., description="Government level name")
    description: Optional[str] = Field(None, description="Government level description")
    level_order: int = Field(..., description="Ordering of government levels")


class JurisdictionBase(BaseModel):
    """Base jurisdiction model"""
    name: str = Field(..., description="Jurisdiction name")
    code: str = Field(..., description="Jurisdiction code")
    government_level_id: str = Field(..., description="Government level ID")
    province: Optional[str] = Field(None, description="Province/territory name")
    jurisdiction_type: JurisdictionTypeEnum = Field(..., description="Type of jurisdiction")
    website: Optional[str] = Field(None, description="Jurisdiction website")
    extras: Optional[Dict[str, Any]] = Field(None, description="Additional data")


class RepresentativeBase(BaseModel):
    """Base representative model"""
    name: str = Field(..., description="Representative name")
    jurisdiction_id: str = Field(..., description="Jurisdiction ID")
    party: Optional[str] = Field(None, description="Political party")
    position: RepresentativePositionEnum = Field(..., description="Position in government")
    riding: Optional[str] = Field(None, description="Electoral riding/district")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    website: Optional[str] = Field(None, description="Personal website")
    extras: Optional[Dict[str, Any]] = Field(None, description="Additional data")
    metadata_json: Optional[Dict[str, Any]] = Field(None, description="Metadata")


class OfficeBase(BaseModel):
    """Base office model"""
    name: str = Field(..., description="Office name")
    jurisdiction_id: str = Field(..., description="Jurisdiction ID")
    office_type: OfficeTypeEnum = Field(..., description="Type of office")
    location: Optional[str] = Field(None, description="Office location")
    phone: Optional[str] = Field(None, description="Office phone")
    email: Optional[str] = Field(None, description="Office email")
    extras: Optional[Dict[str, Any]] = Field(None, description="Additional data")


class BillBase(BaseModel):
    """Base bill model"""
    title: str = Field(..., description="Bill title")
    jurisdiction_id: str = Field(..., description="Jurisdiction ID")
    bill_number: str = Field(..., description="Bill number")
    summary: Optional[str] = Field(None, description="Bill summary")
    status: BillStatusEnum = Field(..., description="Bill status")
    introduced_date: Optional[datetime] = Field(None, description="Introduction date")
    sponsor_id: Optional[str] = Field(None, description="Sponsor representative ID")
    extras: Optional[Dict[str, Any]] = Field(None, description="Additional data")


class VoteBase(BaseModel):
    """Base vote model"""
    bill_id: str = Field(..., description="Bill ID")
    representative_id: str = Field(..., description="Representative ID")
    vote_position: VotePositionEnum = Field(..., description="Vote position")
    vote_date: datetime = Field(..., description="Vote date")
    session: Optional[str] = Field(None, description="Legislative session")
    extras: Optional[Dict[str, Any]] = Field(None, description="Additional data")


class DataSourceBase(BaseModel):
    """Base data source model"""
    name: str = Field(..., description="Data source name")
    jurisdiction_id: str = Field(..., description="Jurisdiction ID")
    source_type: str = Field(..., description="Type of data source")
    url: Optional[str] = Field(None, description="Source URL")
    legacy_module: Optional[str] = Field(None, description="Legacy module name")
    legacy_class: Optional[str] = Field(None, description="Legacy class name")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")
    extras: Optional[Dict[str, Any]] = Field(None, description="Additional data")


# Response Models
class GovernmentLevelResponse(GovernmentLevelBase):
    """Government level response model"""
    id: str = Field(..., description="Government level ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Federal",
                "description": "Federal government of Canada",
                "level_order": 1,
                "created_at": "2025-08-20T20:00:00Z",
                "updated_at": "2025-08-20T20:00:00Z"
            }
        }


class JurisdictionResponse(JurisdictionBase):
    """Jurisdiction response model"""
    id: str = Field(..., description="Jurisdiction ID")
    government_level: GovernmentLevelResponse = Field(..., description="Government level details")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "name": "House of Commons",
                "code": "federal_house_of_commons",
                "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
                "province": None,
                "jurisdiction_type": "parliament",
                "website": "https://www.ourcommons.ca",
                "extras": {},
                "government_level": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Federal",
                    "description": "Federal government of Canada",
                    "level_order": 1,
                    "created_at": "2025-08-20T20:00:00Z",
                    "updated_at": "2025-08-20T20:00:00Z"
                },
                "created_at": "2025-08-20T20:00:00Z",
                "updated_at": "2025-08-20T20:00:00Z"
            }
        }


class RepresentativeResponse(RepresentativeBase):
    """Representative response model"""
    id: str = Field(..., description="Representative ID")
    jurisdiction: JurisdictionResponse = Field(..., description="Jurisdiction details")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440002",
                "name": "Justin Trudeau",
                "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440001",
                "party": "Liberal Party of Canada",
                "position": "mp",
                "riding": "Papineau",
                "email": "justin.trudeau@parl.gc.ca",
                "phone": "+1-613-992-4211",
                "website": "https://www.justintrudeau.ca",
                "extras": {},
                "metadata_json": {},
                "jurisdiction": {
                    "id": "550e8400-e29b-41d4-a716-446655440001",
                    "name": "House of Commons",
                    "code": "federal_house_of_commons",
                    "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
                    "province": None,
                    "jurisdiction_type": "parliament",
                    "website": "https://www.ourcommons.ca",
                    "extras": {},
                    "government_level": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "Federal",
                        "description": "Federal government of Canada",
                        "level_order": 1,
                        "created_at": "2025-08-20T20:00:00Z",
                        "updated_at": "2025-08-20T20:00:00Z"
                    },
                    "created_at": "2025-08-20T20:00:00Z",
                    "updated_at": "2025-08-20T20:00:00Z"
                },
                "created_at": "2025-08-20T20:00:00Z",
                "updated_at": "2025-08-20T20:00:00Z"
            }
        }


class OfficeResponse(OfficeBase):
    """Office response model"""
    id: str = Field(..., description="Office ID")
    jurisdiction: JurisdictionResponse = Field(..., description="Jurisdiction details")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440003",
                "name": "Papineau Constituency Office",
                "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440001",
                "office_type": "constituency",
                "location": "123 Main Street, Montreal, QC",
                "phone": "+1-514-555-0123",
                "email": "papineau@liberal.ca",
                "extras": {},
                "jurisdiction": {
                    "id": "550e8400-e29b-41d4-a716-446655440001",
                    "name": "House of Commons",
                    "code": "federal_house_of_commons",
                    "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
                    "province": None,
                    "jurisdiction_type": "parliament",
                    "website": "https://www.ourcommons.ca",
                    "extras": {},
                    "government_level": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "Federal",
                        "description": "Federal government of Canada",
                        "level_order": 1,
                        "created_at": "2025-08-20T20:00:00Z",
                        "updated_at": "2025-08-20T20:00:00Z"
                    },
                    "created_at": "2025-08-20T20:00:00Z",
                    "updated_at": "2025-08-20T20:00:00Z"
                },
                "created_at": "2025-08-20T20:00:00Z",
                "updated_at": "2025-08-20T20:00:00Z"
            }
        }


class BillResponse(BillBase):
    """Bill response model"""
    id: str = Field(..., description="Bill ID")
    jurisdiction: JurisdictionResponse = Field(..., description="Jurisdiction details")
    sponsor: Optional[RepresentativeResponse] = Field(None, description="Sponsor details")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440004",
                "title": "An Act to amend the Criminal Code",
                "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440001",
                "bill_number": "C-123",
                "summary": "A bill to amend the Criminal Code...",
                "status": "introduced",
                "introduced_date": "2025-08-20T20:00:00Z",
                "sponsor_id": "550e8400-e29b-41d4-a716-446655440002",
                "extras": {},
                "jurisdiction": {
                    "id": "550e8400-e29b-41d4-a716-446655440001",
                    "name": "House of Commons",
                    "code": "federal_house_of_commons",
                    "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
                    "province": None,
                    "jurisdiction_type": "parliament",
                    "website": "https://www.ourcommons.ca",
                    "extras": {},
                    "government_level": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "Federal",
                        "description": "Federal government of Canada",
                        "level_order": 1,
                        "created_at": "2025-08-20T20:00:00Z",
                        "updated_at": "2025-08-20T20:00:00Z"
                    },
                    "created_at": "2025-08-20T20:00:00Z",
                    "updated_at": "2025-08-20T20:00:00Z"
                },
                "sponsor": {
                    "id": "550e8400-e29b-41d4-a716-446655440002",
                    "name": "Justin Trudeau",
                    "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440001",
                    "party": "Liberal Party of Canada",
                    "position": "mp",
                    "riding": "Papineau",
                    "email": "justin.trudeau@parl.gc.ca",
                    "phone": "+1-613-992-4211",
                    "website": "https://www.justintrudeau.ca",
                    "extras": {},
                    "metadata_json": {},
                    "jurisdiction": {
                        "id": "550e8400-e29b-41d4-a716-446655440001",
                        "name": "House of Commons",
                        "code": "federal_house_of_commons",
                        "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
                        "province": None,
                        "jurisdiction_type": "parliament",
                        "website": "https://www.ourcommons.ca",
                        "extras": {},
                        "government_level": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "name": "Federal",
                            "description": "Federal government of Canada",
                            "level_order": 1,
                            "created_at": "2025-08-20T20:00:00Z",
                            "updated_at": "2025-08-20T20:00:00Z"
                        },
                        "created_at": "2025-08-20T20:00:00Z",
                        "updated_at": "2025-08-20T20:00:00Z"
                    },
                    "created_at": "2025-08-20T20:00:00Z",
                    "updated_at": "2025-08-20T20:00:00Z"
                },
                "created_at": "2025-08-20T20:00:00Z",
                "updated_at": "2025-08-20T20:00:00Z"
            }
        }


class VoteResponse(VoteBase):
    """Vote response model"""
    id: str = Field(..., description="Vote ID")
    bill: BillResponse = Field(..., description="Bill details")
    representative: RepresentativeResponse = Field(..., description="Representative details")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440005",
                "bill_id": "550e8400-e29b-41d4-a716-446655440004",
                "representative_id": "550e8400-e29b-41d4-a716-446655440002",
                "vote_position": "yes",
                "vote_date": "2025-08-20T20:00:00Z",
                "session": "44-1",
                "extras": {},
                "bill": {
                    "id": "550e8400-e29b-41d4-a716-446655440004",
                    "title": "An Act to amend the Criminal Code",
                    "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440001",
                    "bill_number": "C-123",
                    "summary": "A bill to amend the Criminal Code...",
                    "status": "introduced",
                    "introduced_date": "2025-08-20T20:00:00Z",
                    "sponsor_id": "550e8400-e29b-41d4-a716-446655440002",
                    "extras": {},
                    "jurisdiction": {
                        "id": "550e8400-e29b-41d4-a716-446655440001",
                        "name": "House of Commons",
                        "code": "federal_house_of_commons",
                        "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
                        "province": None,
                        "jurisdiction_type": "parliament",
                        "website": "https://www.ourcommons.ca",
                        "extras": {},
                        "government_level": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "name": "Federal",
                            "description": "Federal government of Canada",
                            "level_order": 1,
                            "created_at": "2025-08-20T20:00:00Z",
                            "updated_at": "2025-08-20T20:00:00Z"
                        },
                        "created_at": "2025-08-20T20:00:00Z",
                        "updated_at": "2025-08-20T20:00:00Z"
                    },
                    "sponsor": {
                        "id": "550e8400-e29b-41d4-a716-446655440002",
                        "name": "Justin Trudeau",
                        "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440001",
                        "party": "Liberal Party of Canada",
                        "position": "mp",
                        "riding": "Papineau",
                        "email": "justin.trudeau@parl.gc.ca",
                        "phone": "+1-613-992-4211",
                        "website": "https://www.justintrudeau.ca",
                        "extras": {},
                        "metadata_json": {},
                        "jurisdiction": {
                            "id": "550e8400-e29b-41d4-a716-446655440001",
                            "name": "House of Commons",
                            "code": "federal_house_of_commons",
                            "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
                            "province": None,
                            "jurisdiction_type": "parliament",
                            "website": "https://www.ourcommons.ca",
                            "extras": {},
                            "government_level": {
                                "id": "550e8400-e29b-41d4-a716-446655440000",
                                "name": "Federal",
                                "description": "Federal government of Canada",
                                "level_order": 1,
                                "created_at": "2025-08-20T20:00:00Z",
                                "updated_at": "2025-08-20T20:00:00Z"
                            },
                            "created_at": "2025-08-20T20:00:00Z",
                            "updated_at": "2025-08-20T20:00:00Z"
                        },
                        "created_at": "2025-08-20T20:00:00Z",
                        "updated_at": "2025-08-20T20:00:00Z"
                    },
                    "created_at": "2025-08-20T20:00:00Z",
                    "updated_at": "2025-08-20T20:00:00Z"
                },
                "representative": {
                    "id": "550e8400-e29b-41d4-a716-446655440002",
                    "name": "Justin Trudeau",
                    "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440001",
                    "party": "Liberal Party of Canada",
                    "position": "mp",
                    "riding": "Papineau",
                    "email": "justin.trudeau@parl.gc.ca",
                    "phone": "+1-613-992-4211",
                    "website": "https://www.justintrudeau.ca",
                    "extras": {},
                    "metadata_json": {},
                    "jurisdiction": {
                        "id": "550e8400-e29b-41d4-a716-446655440001",
                        "name": "House of Commons",
                        "code": "federal_house_of_commons",
                        "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
                        "province": None,
                        "jurisdiction_type": "parliament",
                        "website": "https://www.ourcommons.ca",
                        "extras": {},
                        "government_level": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "name": "Federal",
                            "description": "Federal government of Canada",
                            "level_order": 1,
                            "created_at": "2025-08-20T20:00:00Z",
                            "updated_at": "2025-08-20T20:00:00Z"
                        },
                        "created_at": "2025-08-20T20:00:00Z",
                        "updated_at": "2025-08-20T20:00:00Z"
                    },
                    "created_at": "2025-08-20T20:00:00Z",
                    "updated_at": "2025-08-20T20:00:00Z"
                },
                "created_at": "2025-08-20T20:00:00Z",
                "updated_at": "2025-08-20T20:00:00Z"
            }
        }


class DataSourceResponse(DataSourceBase):
    """Data source response model"""
    id: str = Field(..., description="Data source ID")
    jurisdiction: JurisdictionResponse = Field(..., description="Jurisdiction details")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440006",
                "name": "OpenParliament Federal Bills",
                "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440001",
                "source_type": "api",
                "url": "https://openparliament.ca/api/v1/bills/",
                "legacy_module": "openparliament",
                "legacy_class": "BillsScraper",
                "last_updated": "2025-08-20T20:00:00Z",
                "extras": {},
                "jurisdiction": {
                    "id": "550e8400-e29b-41d4-a716-446655440001",
                    "name": "House of Commons",
                    "code": "federal_house_of_commons",
                    "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
                    "province": None,
                    "jurisdiction_type": "parliament",
                    "website": "https://www.ourcommons.ca",
                    "extras": {},
                    "government_level": {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "Federal",
                        "description": "Federal government of Canada",
                        "level_order": 1,
                        "created_at": "2025-08-20T20:00:00Z",
                        "updated_at": "2025-08-20T20:00:00Z"
                    },
                    "created_at": "2025-08-20T20:00:00Z",
                    "updated_at": "2025-08-20T20:00:00Z"
                },
                "created_at": "2025-08-20T20:00:00Z",
                "updated_at": "2025-08-20T20:00:00Z"
            }
        }


# List Response Models
class PaginationInfo(BaseModel):
    """Pagination information"""
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total: int = Field(..., description="Total number of items")
    total_pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")


class GovernmentLevelListResponse(BaseModel):
    """Government levels list response"""
    items: List[GovernmentLevelResponse] = Field(..., description="List of government levels")
    pagination: PaginationInfo = Field(..., description="Pagination information")


class JurisdictionListResponse(BaseModel):
    """Jurisdictions list response"""
    items: List[JurisdictionResponse] = Field(..., description="List of jurisdictions")
    pagination: PaginationInfo = Field(..., description="Pagination information")


class RepresentativeListResponse(BaseModel):
    """Representatives list response"""
    items: List[RepresentativeResponse] = Field(..., description="List of representatives")
    pagination: PaginationInfo = Field(..., description="Pagination information")


class OfficeListResponse(BaseModel):
    """Offices list response"""
    items: List[OfficeResponse] = Field(..., description="List of offices")
    pagination: PaginationInfo = Field(..., description="Pagination information")


class BillListResponse(BaseModel):
    """Bills list response"""
    items: List[BillResponse] = Field(..., description="List of bills")
    pagination: PaginationInfo = Field(..., description="Pagination information")


class VoteListResponse(BaseModel):
    """Votes list response"""
    items: List[VoteResponse] = Field(..., description="List of votes")
    pagination: PaginationInfo = Field(..., description="Pagination information")


class DataSourceListResponse(BaseModel):
    """Data sources list response"""
    items: List[DataSourceResponse] = Field(..., description="List of data sources")
    pagination: PaginationInfo = Field(..., description="Pagination information")


# Search and Filter Models
class RepresentativeSearchParams(BaseModel):
    """Representative search parameters"""
    q: Optional[str] = Field(None, description="Search query for name")
    jurisdiction_id: Optional[str] = Field(None, description="Filter by jurisdiction")
    government_level: Optional[GovernmentLevelEnum] = Field(None, description="Filter by government level")
    province: Optional[str] = Field(None, description="Filter by province")
    party: Optional[str] = Field(None, description="Filter by political party")
    position: Optional[RepresentativePositionEnum] = Field(None, description="Filter by position")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


class BillSearchParams(BaseModel):
    """Bill search parameters"""
    q: Optional[str] = Field(None, description="Search query for title")
    jurisdiction_id: Optional[str] = Field(None, description="Filter by jurisdiction")
    government_level: Optional[GovernmentLevelEnum] = Field(None, description="Filter by government level")
    status: Optional[BillStatusEnum] = Field(None, description="Filter by status")
    sponsor_id: Optional[str] = Field(None, description="Filter by sponsor")
    introduced_after: Optional[datetime] = Field(None, description="Filter by introduction date (after)")
    introduced_before: Optional[datetime] = Field(None, description="Filter by introduction date (before)")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


class VoteSearchParams(BaseModel):
    """Vote search parameters"""
    bill_id: Optional[str] = Field(None, description="Filter by bill")
    representative_id: Optional[str] = Field(None, description="Filter by representative")
    vote_position: Optional[VotePositionEnum] = Field(None, description="Filter by vote position")
    vote_after: Optional[datetime] = Field(None, description="Filter by vote date (after)")
    vote_before: Optional[datetime] = Field(None, description="Filter by vote date (before)")
    session: Optional[str] = Field(None, description="Filter by session")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")


# Statistics Models
class JurisdictionStats(BaseModel):
    """Jurisdiction statistics"""
    jurisdiction_id: str = Field(..., description="Jurisdiction ID")
    jurisdiction_name: str = Field(..., description="Jurisdiction name")
    total_representatives: int = Field(..., description="Total number of representatives")
    total_bills: int = Field(..., description="Total number of bills")
    total_votes: int = Field(..., description="Total number of votes")
    total_offices: int = Field(..., description="Total number of offices")
    last_updated: datetime = Field(..., description="Last update timestamp")


class GovernmentLevelStats(BaseModel):
    """Government level statistics"""
    level_id: str = Field(..., description="Government level ID")
    level_name: str = Field(..., description="Government level name")
    total_jurisdictions: int = Field(..., description="Total number of jurisdictions")
    total_representatives: int = Field(..., description="Total number of representatives")
    total_bills: int = Field(..., description="Total number of bills")
    total_votes: int = Field(..., description="Total number of votes")
    total_offices: int = Field(..., description="Total number of offices")
    last_updated: datetime = Field(..., description="Last update timestamp")


class SystemStats(BaseModel):
    """System-wide statistics"""
    total_government_levels: int = Field(..., description="Total number of government levels")
    total_jurisdictions: int = Field(..., description="Total number of jurisdictions")
    total_representatives: int = Field(..., description="Total number of representatives")
    total_bills: int = Field(..., description="Total number of bills")
    total_votes: int = Field(..., description="Total number of votes")
    total_offices: int = Field(..., description="Total number of offices")
    total_data_sources: int = Field(..., description="Total number of data sources")
    last_updated: datetime = Field(..., description="Last update timestamp")
