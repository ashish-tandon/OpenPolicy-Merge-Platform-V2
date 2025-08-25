"""
Pydantic schemas for search API.

Defines the data models for API requests and responses.
Adapted from legacy OpenParliament search functionality.
"""

from datetime import date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class SearchResult(BaseModel):
    """A single search result item."""
    
    id: str = Field(..., description="Unique identifier for the result")
    title: str = Field(..., description="Title/heading for the result")
    content_type: str = Field(..., description="Type of content (bill, member, vote, debate, committee)")
    snippet: str = Field(..., description="Text snippet with search context, may include highlighting")
    url: str = Field(..., description="URL to the full content")
    date: Optional[str] = Field(None, description="Date associated with the content (YYYY-MM-DD)")
    relevance_score: float = Field(..., description="Relevance score for ranking (0.0-1.0)")
    
    # Enhanced metadata field for additional structured data
    metadata: Optional[Dict[str, Any]] = Field(
        None, 
        description="Additional metadata specific to content type"
    )
    
    # Deprecated fields maintained for backward compatibility
    politician_name: Optional[str] = Field(None, description="DEPRECATED: Use metadata.name instead")
    bill_number: Optional[str] = Field(None, description="DEPRECATED: Use metadata.bill_number instead")
    
    model_config = {"from_attributes": True}
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        if v is not None:
            try:
                # Allow both date and datetime strings
                if 'T' in str(v):
                    return str(v)  # Keep datetime strings as-is
                return date.fromisoformat(str(v)).isoformat()
            except ValueError:
                raise ValueError('Invalid date format. Use YYYY-MM-DD or ISO datetime')
        return v


class SearchResponse(BaseModel):
    """Response model for search endpoint."""
    
    query: str = Field(..., description="The search query that was executed")
    total_results: int = Field(..., description="Total number of results found")
    results: List[SearchResult] = Field(..., description="List of search results")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")
    
    # New field to show applied filters
    filters_applied: Optional[Dict[str, Any]] = Field(
        None,
        description="Filters that were applied to this search"
    )


class SearchSuggestion(BaseModel):
    """A search suggestion for autocomplete."""
    
    text: str = Field(..., description="Suggested search text")
    type: str = Field(..., description="Type of suggestion (member, bill, etc.)")
    url: Optional[str] = Field(None, description="URL if suggestion links to specific content")
    
    model_config = {"from_attributes": True}


class SearchSuggestionsResponse(BaseModel):
    """Response model for search suggestions endpoint."""
    
    suggestions: List[SearchSuggestion] = Field(..., description="List of search suggestions")


# PostcodeResult is now a dictionary in the actual response
class PostcodeResponse(BaseModel):
    """Response model for postcode lookup endpoint."""
    
    postcode: str = Field(..., description="The queried postal code (normalized)")
    representatives: List[Dict[str, Any]] = Field(
        ..., 
        description="List of representatives with name, party, riding, level, etc."
    )
    total_count: int = Field(..., description="Total number of representatives found")
    source: str = Field(..., description="Data source (e.g., Represent Canada API)")
    timestamp: str = Field(..., description="When the lookup was performed (ISO format)")
    
    model_config = {"from_attributes": True}
