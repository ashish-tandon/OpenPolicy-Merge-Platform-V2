"""
Amendment API schemas for Pydantic v2 compatibility.

Schemas for bill amendment operations including listing, creation, and detailed views.
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class AmendmentBase(BaseModel):
    """Base amendment information."""
    
    number: str = Field(..., description="Amendment number/identifier")
    title_en: Optional[str] = Field(None, description="Amendment title in English")
    title_fr: Optional[str] = Field(None, description="Amendment title in French")
    description_en: Optional[str] = Field(None, description="Amendment description in English")
    description_fr: Optional[str] = Field(None, description="Amendment description in French")
    institution: str = Field(..., description="Institution where amendment was proposed (House/Senate)")
    stage: Optional[str] = Field(None, description="Legislative stage (report, committee, consideration)")
    amendment_type: Optional[str] = Field(None, description="Type of amendment (substantive, technical, consequential)")
    clause_reference: Optional[str] = Field(None, description="Reference to specific clause being amended")
    line_number: Optional[int] = Field(None, description="Line number in bill text")


class AmendmentCreate(AmendmentBase):
    """Schema for creating a new amendment."""
    
    bill_id: int = Field(..., description="ID of the bill being amended")
    mover_politician_id: Optional[int] = Field(None, description="ID of politician proposing the amendment")
    mover_member_id: Optional[int] = Field(None, description="ID of member proposing the amendment")
    proposed_date: Optional[date] = Field(None, description="Date amendment was proposed")
    text_en: Optional[str] = Field(None, description="Full amendment text in English")
    text_fr: Optional[str] = Field(None, description="Full amendment text in French")


class AmendmentSummary(AmendmentBase):
    """Summary information for amendment listings."""
    
    id: int = Field(..., description="Unique amendment identifier")
    bill_id: int = Field(..., description="ID of the bill being amended")
    status: str = Field(..., description="Amendment status (proposed, adopted, withdrawn, defeated)")
    proposed_date: Optional[date] = Field(None, description="Date amendment was proposed")
    mover_name: Optional[str] = Field(None, description="Name of member who proposed the amendment")
    mover_party: Optional[str] = Field(None, description="Party of member who proposed the amendment")
    
    model_config = ConfigDict(from_attributes=True)


class AmendmentDetail(AmendmentSummary):
    """Detailed amendment information."""
    
    text_en: Optional[str] = Field(None, description="Full amendment text in English")
    text_fr: Optional[str] = Field(None, description="Full amendment text in French")
    bill_number: Optional[str] = Field(None, description="Number of the bill being amended")
    bill_title: Optional[str] = Field(None, description="Title of the bill being amended")
    created_at: Optional[datetime] = Field(None, description="Amendment creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Amendment last update timestamp")


class AmendmentListResponse(BaseModel):
    """Response schema for amendment listings."""
    
    amendments: List[AmendmentSummary] = Field(..., description="List of amendments")
    pagination: dict = Field(..., description="Pagination information")
    
    model_config = ConfigDict(from_attributes=True)


class AmendmentDetailResponse(BaseModel):
    """Response schema for amendment detail."""
    
    amendment: AmendmentDetail = Field(..., description="Detailed amendment information")
    
    model_config = ConfigDict(from_attributes=True)


class AmendmentStatsResponse(BaseModel):
    """Response schema for amendment statistics."""
    
    total_amendments: int = Field(..., description="Total number of amendments")
    by_status: dict = Field(..., description="Amendments grouped by status")
    by_institution: dict = Field(..., description="Amendments grouped by institution")
    by_type: dict = Field(..., description="Amendments grouped by type")
    by_stage: dict = Field(..., description="Amendments grouped by stage")
    recent_amendments: int = Field(..., description="Number of amendments in last 30 days")
    
    model_config = ConfigDict(from_attributes=True)
