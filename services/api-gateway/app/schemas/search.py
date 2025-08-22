"""
Pydantic schemas for search API.

Defines the data models for API requests and responses.
Adapted from legacy OpenParliament search functionality.
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class SearchResult(BaseModel):
    """A single search result item."""
    
    id: str = Field(..., description="Unique identifier for the result")
    title: str = Field(..., description="Title/heading for the result")
    content_type: str = Field(..., description="Type of content (debate, bill, politician, etc.)")
    snippet: str = Field(..., description="Text snippet with search context")
    url: str = Field(..., description="URL to the full content")
    date: Optional[str] = Field(None, description="Date associated with the content (YYYY-MM-DD)")
    politician_name: Optional[str] = Field(None, description="Associated politician name")
    bill_number: Optional[str] = Field(None, description="Associated bill number")
    relevance_score: float = Field(..., description="Relevance score for ranking")
    
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


class SearchResponse(BaseModel):
    """Response model for search endpoint."""
    
    query: str = Field(..., description="The search query that was executed")
    total_results: int = Field(..., description="Total number of results found")
    results: List[SearchResult] = Field(..., description="List of search results")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")


class SearchSuggestion(BaseModel):
    """A search suggestion for autocomplete."""
    
    text: str = Field(..., description="Suggested search text")
    type: str = Field(..., description="Type of suggestion (politician, bill, etc.)")
    url: Optional[str] = Field(None, description="URL if suggestion links to specific content")
    
    model_config = {"from_attributes": True}


class SearchSuggestionsResponse(BaseModel):
    """Response model for search suggestions endpoint."""
    
    suggestions: List[SearchSuggestion] = Field(..., description="List of search suggestions")


class PostcodeResult(BaseModel):
    """Result of a postal code lookup."""
    
    name: str = Field(..., description="Representative name")
    party: str = Field(..., description="Political party")
    riding: str = Field(..., description="Electoral district name")
    level: str = Field(..., description="Government level (federal, provincial, municipal)")
    url: str = Field(..., description="URL to representative's profile")
    photo_url: Optional[str] = Field(None, description="URL to representative's photo")
    email: Optional[str] = Field(None, description="Representative's email address")
    phone: Optional[str] = Field(None, description="Representative's phone number")
    
    model_config = {"from_attributes": True}


class PostcodeResponse(BaseModel):
    """Response model for postcode lookup endpoint."""
    
    postcode: str = Field(..., description="The queried postal code")
    representatives: List[PostcodeResult] = Field(..., description="List of representatives for this postal code")
    total_count: int = Field(..., description="Total number of representatives found")
    source: str = Field(..., description="Data source (e.g., Represent Canada API)")
    timestamp: str = Field(..., description="When the lookup was performed")
