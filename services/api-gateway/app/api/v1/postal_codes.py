"""
Postal Code API endpoints for OpenParliament.

Provides RESTful endpoints for postal code lookups and member associations.
Implements FEAT-001: Global Search with Postal Code MP Lookup
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import text, and_, desc, or_
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.database import get_db
from app.models.openparliament import Member, Party, Jurisdiction
from app.schemas.search import PostcodeResponse
import re
import httpx

router = APIRouter()


@router.get("/{code}/members", response_model=PostcodeResponse)
async def get_members_by_postal_code(
    code: str,
    db: DBSession = Depends(get_db)
):
    """
    Get all members (MPs) representing a postal code area.
    
    This is the RESTful implementation of postal code lookup.
    Follows REST principles: /resource/{id}/sub-resource
    
    Parameters:
    - code: Canadian postal code (with or without space)
    
    Returns:
    - List of representatives for the postal code
    """
    
    # Clean up postcode format
    clean_postcode = code.upper().replace(" ", "")
    
    # Validate postal code format (Canadian format: K1A0A6)
    if len(clean_postcode) != 6:
        raise HTTPException(
            status_code=400, 
            detail="Invalid postal code format. Must be 6 characters (e.g., K1A0A6)"
        )
    
    # Check if it matches Canadian postal code pattern
    if not re.match(r'^[A-Z]\d[A-Z]\d[A-Z]\d$', clean_postcode):
        raise HTTPException(
            status_code=400, 
            detail="Invalid postal code format. Must follow Canadian format (e.g., K1A0A6)"
        )
    
    try:
        # Call Represent Canada API
        represent_api_url = f"https://represent.opennorth.ca/postcodes/{clean_postcode}/"
        
        # Make request to Represent API
        with httpx.Client(timeout=10.0) as client:
            response = client.get(represent_api_url)
        
        if response.status_code == 404:
            raise HTTPException(
                status_code=404, 
                detail=f"No representatives found for postal code {clean_postcode}"
            )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"Error calling Represent API: {response.status_code}"
            )
        
        # Parse the response
        data = response.json()
        
        # Extract representative information
        representatives = []
        
        if 'representatives_centroid' in data:
            for rep in data['representatives_centroid']:
                # Only include federal MPs (House of Commons members)
                if rep.get('elected_office') == 'MP' or 'house of commons' in rep.get('related', {}).get('boundary_set_name', '').lower():
                    representative_info = {
                        'name': rep.get('name', 'Unknown'),
                        'party': rep.get('party_name', 'Unknown'),
                        'riding': rep.get('district_name', 'Unknown'),
                        'level': 'Federal',
                        'url': rep.get('url', ''),
                        'photo_url': rep.get('photo_url', ''),
                        'email': rep.get('email', ''),
                        'phone': rep.get('offices', [{}])[0].get('tel', '') if rep.get('offices') else ''
                    }
                    representatives.append(representative_info)
        
        # Create response following RESTful principles
        return PostcodeResponse(
            postcode=clean_postcode,
            representatives=representatives,
            total_count=len(representatives),
            source="Represent Canada API",
            timestamp=datetime.now().isoformat()
        )
        
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="External API request timed out"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calling external API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )