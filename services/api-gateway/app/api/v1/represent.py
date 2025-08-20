"""
Represent API Integration

Integrates with OpenNorth Represent API to provide electoral district
and representative information for Canadian jurisdictions.
"""

import httpx
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

router = APIRouter()

# Represent API base URL
REPRESENT_API_BASE = "https://represent.opennorth.ca"

# Rate limiting: 60 requests per minute
RATE_LIMIT_PER_MINUTE = 60


class BoundarySet(BaseModel):
    """Electoral boundary set (e.g., federal ridings, provincial districts)."""
    name: str = Field(..., description="Name of the boundary set")
    domain: str = Field(..., description="Domain (e.g., 'ca')")
    authority: str = Field(..., description="Authority (e.g., 'Elections Canada')")
    slug: str = Field(..., description="URL slug for the boundary set")
    last_updated: Optional[str] = Field(None, description="Last update timestamp")


class Boundary(BaseModel):
    """Electoral boundary (e.g., specific riding or district)."""
    name: str = Field(..., description="Name of the boundary")
    boundary_set_name: str = Field(..., description="Name of the boundary set")
    external_id: str = Field(..., description="External identifier")
    centroid_lat: Optional[float] = Field(None, description="Centroid latitude")
    centroid_lon: Optional[float] = Field(None, description="Centroid longitude")
    area: Optional[float] = Field(None, description="Area in square kilometers")


class Representative(BaseModel):
    """Elected representative information."""
    name: str = Field(..., description="Full name of the representative")
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    party_name: Optional[str] = Field(None, description="Political party name")
    email: Optional[str] = Field(None, description="Email address")
    photo_url: Optional[str] = Field(None, description="Photo URL")
    elected_office: str = Field(..., description="Elected office (e.g., 'MP', 'MLA')")
    district_name: str = Field(..., description="District/riding name")
    url: Optional[str] = Field(None, description="Personal website URL")


class PostalCodeLookup(BaseModel):
    """Postal code lookup result."""
    postal_code: str = Field(..., description="The postal code")
    boundaries_centroid: List[Boundary] = Field(..., description="Boundaries containing the centroid")
    boundaries_concordance: List[Boundary] = Field(..., description="Boundaries linked by postal code")
    representatives_centroid: List[Representative] = Field(..., description="Representatives for centroid boundaries")
    representatives_concordance: List[Representative] = Field(..., description="Representatives for concordance boundaries")


@router.get("/boundary-sets", response_model=List[BoundarySet])
async def get_boundary_sets():
    """
    Get available electoral boundary sets.
    
    Returns:
        List of available boundary sets (federal, provincial, municipal)
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{REPRESENT_API_BASE}/boundary-sets/")
            response.raise_for_status()
            data = response.json()
            return data.get("objects", [])
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Represent API error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch boundary sets: {str(e)}")


@router.get("/boundaries/{boundary_set_slug}", response_model=List[Boundary])
async def get_boundaries(
    boundary_set_slug: str,
    limit: int = Query(20, ge=1, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip")
):
    """
    Get boundaries for a specific boundary set.
    
    Args:
        boundary_set_slug: Slug of the boundary set (e.g., 'federal-electoral-districts')
        limit: Number of results per page
        offset: Number of results to skip
    
    Returns:
        List of boundaries in the specified set
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{REPRESENT_API_BASE}/boundaries/{boundary_set_slug}/",
                params={"limit": limit, "offset": offset}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("objects", [])
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Represent API error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch boundaries: {str(e)}")


@router.get("/representatives/{representative_set_slug}", response_model=List[Representative])
async def get_representatives(
    representative_set_slug: str,
    limit: int = Query(20, ge=1, le=100, description="Number of results per page"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
    district_name: Optional[str] = Query(None, description="Filter by district name"),
    party_name: Optional[str] = Query(None, description="Filter by party name")
):
    """
    Get representatives for a specific representative set.
    
    Args:
        representative_set_slug: Slug of the representative set (e.g., 'house-of-commons')
        limit: Number of results per page
        offset: Number of results to skip
        district_name: Filter by district name
        party_name: Filter by party name
    
    Returns:
        List of representatives in the specified set
    """
    try:
        params = {"limit": limit, "offset": offset}
        if district_name:
            params["district_name__icontains"] = district_name
        if party_name:
            params["party_name__icontains"] = party_name
            
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{REPRESENT_API_BASE}/representatives/{representative_set_slug}/",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            return data.get("objects", [])
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Represent API error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch representatives: {str(e)}")


@router.get("/postal-code/{postal_code}", response_model=PostalCodeLookup)
async def lookup_by_postal_code(postal_code: str):
    """
    Look up electoral boundaries and representatives by postal code.
    
    Args:
        postal_code: Canadian postal code (e.g., 'K1A0A6')
    
    Returns:
        Boundaries and representatives for the postal code
    """
    # Clean postal code (remove spaces, uppercase)
    postal_code = postal_code.replace(" ", "").upper()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{REPRESENT_API_BASE}/postcodes/{postal_code}/")
            response.raise_for_status()
            data = response.json()
            
            # Transform the response to match our schema
            return PostalCodeLookup(
                postal_code=postal_code,
                boundaries_centroid=data.get("boundaries_centroid", []),
                boundaries_concordance=data.get("boundaries_concordance", []),
                representatives_centroid=data.get("representatives_centroid", []),
                representatives_concordance=data.get("representatives_concordance", [])
            )
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Postal code {postal_code} not found")
        raise HTTPException(status_code=e.response.status_code, detail="Represent API error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to lookup postal code: {str(e)}")


@router.get("/geocode", response_model=List[Boundary])
async def lookup_by_coordinates(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    boundary_set: Optional[str] = Query(None, description="Boundary set to search in")
):
    """
    Look up electoral boundaries by geographic coordinates.
    
    Args:
        lat: Latitude
        lon: Longitude
        boundary_set: Optional boundary set to limit search
    
    Returns:
        List of boundaries containing the coordinates
    """
    try:
        params = {"lat": lat, "lon": lon}
        if boundary_set:
            params["sets"] = boundary_set
            
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{REPRESENT_API_BASE}/boundaries/",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            return data.get("objects", [])
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Represent API error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to lookup coordinates: {str(e)}")


@router.get("/health")
async def represent_api_health():
    """
    Check Represent API health and rate limit status.
    
    Returns:
        API health information
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{REPRESENT_API_BASE}/boundary-sets/")
            response.raise_for_status()
            
            # Check rate limit headers if available
            rate_limit_remaining = response.headers.get("X-RateLimit-Remaining", "unknown")
            
            return {
                "status": "healthy",
                "represent_api": "operational",
                "rate_limit_remaining": rate_limit_remaining,
                "rate_limit_per_minute": RATE_LIMIT_PER_MINUTE
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "represent_api": "error",
            "error": str(e),
            "rate_limit_per_minute": RATE_LIMIT_PER_MINUTE
        }
