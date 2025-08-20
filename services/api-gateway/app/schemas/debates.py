"""
Pydantic schemas for debates API.

Defines the data models for API requests and responses.
Adapted from legacy OpenParliament hansards functionality.
"""

from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class Pagination(BaseModel):
    """Pagination information for list responses."""
    
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total: int = Field(..., description="Total number of items")
    pages: int = Field(..., description="Total number of pages")


class DebateSummary(BaseModel):
    """Summary information about a House debate."""
    
    id: str = Field(..., description="Unique debate identifier")
    date: Optional[str] = Field(None, description="Date of the debate (YYYY-MM-DD)")
    number: int = Field(..., description="Hansard number/sitting ID")
    statement_count: int = Field(..., description="Number of statements in the debate")
    url: Optional[str] = Field(None, description="URL to debate detail")
    
    model_config = {"from_attributes": True}
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        if v is not None:
            try:
                return date.fromisoformat(v)
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD')
        return v


class DebateDetail(BaseModel):
    """Detailed information about a House debate."""
    
    id: str = Field(..., description="Unique debate identifier")
    date: str = Field(..., description="Date of the debate (YYYY-MM-DD)")
    number: int = Field(..., description="Hansard number/sitting ID")
    statement_count: int = Field(..., description="Number of statements in the debate")
    speaker_count: int = Field(..., description="Number of unique speakers")
    url: str = Field(..., description="URL to debate detail")
    
    model_config = {"from_attributes": True}
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        try:
            return date.fromisoformat(v)
        except ValueError:
            raise ValueError('Invalid date format. Use YYYY-MM-DD')


class SpeechSummary(BaseModel):
    """Summary information about a parliamentary speech/statement."""
    
    id: str = Field(..., description="Unique speech identifier")
    politician_name: str = Field(..., description="Name of the speaker")
    date: Optional[str] = Field(None, description="Date of the speech (YYYY-MM-DD)")
    time: Optional[str] = Field(None, description="Time of the speech (HH:MM:SS)")
    text_preview: str = Field(..., description="Preview of the speech text")
    bill_mentioned: Optional[str] = Field(None, description="Bill number if mentioned")
    url: str = Field(..., description="URL to speech detail")
    
    model_config = {"from_attributes": True}
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        if v is not None:
            try:
                return date.fromisoformat(v)
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD')
        return v
    
    @field_validator('time')
    @classmethod
    def validate_time(cls, v):
        if v is not None:
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                raise ValueError('Invalid time format. Use HH:MM:SS')
        return v


class SpeechDetail(BaseModel):
    """Detailed information about a parliamentary speech/statement."""
    
    id: str = Field(..., description="Unique speech identifier")
    politician_name: str = Field(..., description="Name of the speaker")
    party_name: Optional[str] = Field(None, description="Speaker's party name")
    constituency: Optional[str] = Field(None, description="Speaker's constituency")
    date: Optional[str] = Field(None, description="Date of the speech (YYYY-MM-DD)")
    time: Optional[str] = Field(None, description="Time of the speech (HH:MM:SS)")
    text: str = Field(..., description="Full text of the speech")
    bill_mentioned: Optional[str] = Field(None, description="Bill number if mentioned")
    sitting_id: int = Field(..., description="Sitting/debate identifier")
    sequence: int = Field(..., description="Sequence number in the debate")
    
    model_config = {"from_attributes": True}
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        if v is not None:
            try:
                return date.fromisoformat(v)
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD')
        return v
    
    @field_validator('time')
    @classmethod
    def validate_time(cls, v):
        if v is not None:
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                raise ValueError('Invalid time format. Use HH:MM:SS')
        return v


class DebateListResponse(BaseModel):
    """Response model for debate list endpoint."""
    
    debates: List[DebateSummary] = Field(..., description="List of debates")
    pagination: Pagination = Field(..., description="Pagination information")


class DebateDetailResponse(BaseModel):
    """Response model for debate detail endpoint."""
    
    debate: DebateDetail = Field(..., description="Detailed debate information")


class SpeechListResponse(BaseModel):
    """Response model for speech list endpoint."""
    
    speeches: List[SpeechSummary] = Field(..., description="List of speeches")
    pagination: Pagination = Field(..., description="Pagination information")


class SpeechDetailResponse(BaseModel):
    """Response model for speech detail endpoint."""
    
    speech: SpeechDetail = Field(..., description="Detailed speech information")


class DebateSummaryResponse(BaseModel):
    """Response model for debate summary statistics."""
    
    total_debates: int = Field(..., description="Total number of debates")
    total_speeches: int = Field(..., description="Total number of speeches")
    total_speakers: int = Field(..., description="Total number of unique speakers")
    latest_debate_date: Optional[date] = Field(None, description="Date of most recent debate")
