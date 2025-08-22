"""
Search API endpoints for OpenParliament data.

Provides endpoints for searching across all parliamentary content.
Copied and adapted from legacy OpenParliament search functionality.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import text, and_, desc, or_
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from app.database import get_db
from app.models.openparliament import Vote, Bill, Member, Party, Jurisdiction
from app.schemas.search import (
    SearchResult, SearchResponse, SearchSuggestion, SearchSuggestionsResponse,
    PostcodeResult, PostcodeResponse
)

router = APIRouter()


@router.get("/", response_model=SearchResponse)
async def search_content(
    q: str = Query(..., description="Search query"),
    content_type: Optional[str] = Query(None, description="Content type filter (bills, debates, politicians)"),
    politician: Optional[str] = Query(None, description="Politician name filter"),
    date__gte: Optional[str] = Query(None, description="Date greater than or equal (YYYY-MM-DD)"),
    date__lte: Optional[str] = Query(None, description="Date less than or equal (YYYY-MM-DD)"),
    sort: Optional[str] = Query("relevance", description="Sort order (relevance, date)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    Search across all parliamentary content.
    
    Based on legacy search functionality with full-text search capabilities.
    """
    
    if not q or len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Search query must be at least 2 characters")
    
    search_query = q.strip()
    results = []
    total = 0
    
    # Search in different content types based on filter
    if not content_type or content_type == "debates":
        # Search votes/debates
        stmt_query = db.query(Vote).join(Bill, Vote.bill_id == Bill.id, isouter=True)
        
        # Add text search
        stmt_query = stmt_query.filter(Vote.vote_type.ilike(f"%{search_query}%"))
        
        # Apply additional filters
        if politician:
            stmt_query = stmt_query.join(Bill).join(Member, Bill.jurisdiction_id == Member.jurisdiction_id, isouter=True).filter(Member.full_name.ilike(f"%{politician}%"))
        
        if date__gte:
            try:
                date_gte = datetime.strptime(date__gte, "%Y-%m-%d")
                stmt_query = stmt_query.filter(Vote.vote_date >= date_gte)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        if date__lte:
            try:
                date_lte = datetime.strptime(date__lte, "%Y-%m-%d")
                stmt_query = stmt_query.filter(Vote.vote_date <= date_lte)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Apply sorting
        if sort == "date":
            stmt_query = stmt_query.order_by(desc(Vote.vote_date))
        else:
            # For relevance, we could implement a scoring system
            # For now, just order by date
            stmt_query = stmt_query.order_by(desc(Vote.vote_date))
        
        # Get total count
        stmt_total = stmt_query.count()
        total += stmt_total
        
        # Apply pagination
        offset = (page - 1) * page_size
        statements = stmt_query.offset(offset).limit(page_size).all()
    
        # Convert to search results
        for stmt in statements:
            # Create snippet with highlighted search terms
            text = stmt.vote_type or ""
            if text:
                snippet_start = max(0, text.lower().find(search_query.lower()) - 50)
                snippet_end = min(len(text), snippet_start + 200)
                snippet = text[snippet_start:snippet_end]
                if snippet_start > 0:
                    snippet = "..." + snippet
                if snippet_end < len(text):
                    snippet = snippet + "..."
            else:
                snippet = "No description available"
            
            results.append(SearchResult(
                id=str(stmt.id),
                title=f"Vote on {stmt.bill.title if stmt.bill else 'Unknown Bill'}",
                content_type="debate",
                snippet=snippet,
                url=f"/api/v1/votes/{stmt.id}/",
                date=stmt.vote_date.date().isoformat() if stmt.vote_date else None,
                politician_name=None,  # Not directly available in this schema
                relevance_score=1.0  # Could implement actual scoring
            ))
    
    if not content_type or content_type == "bills":
        # Search bills
        bill_query = db.query(Bill)
        
        # Add text search on title and summary
        bill_query = bill_query.filter(
            or_(
                Bill.title.ilike(f"%{search_query}%"),
                Bill.summary.ilike(f"%{search_query}%") if Bill.summary else False
            )
        )
        
        # Apply additional filters
        if date__gte:
            try:
                date_gte = datetime.strptime(date__gte, "%Y-%m-%d")
                bill_query = bill_query.filter(Bill.introduced_date >= date_gte)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        if date__lte:
            try:
                date_lte = datetime.strptime(date__lte, "%Y-%m-%d")
                bill_query = bill_query.filter(Bill.introduced_date <= date_lte)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Apply sorting
        if sort == "date":
            bill_query = bill_query.order_by(desc(Bill.introduced_date))
        else:
            # For relevance, order by title similarity
            bill_query = bill_query.order_by(Bill.title.ilike(f"%{search_query}%").desc())
        
        # Get total count
        bill_total = bill_query.count()
        total += bill_total
        
        # Apply pagination
        offset = (page - 1) * page_size
        bills = bill_query.offset(offset).limit(page_size).all()
        
        # Convert to search results
        for bill in bills:
            # Create snippet with highlighted search terms
            text = bill.title or ""
            if bill.summary:
                text += " " + bill.summary
            
            if text:
                snippet_start = max(0, text.lower().find(search_query.lower()) - 50)
                snippet_end = min(len(text), snippet_start + 200)
                snippet = text[snippet_start:snippet_end]
                if snippet_start > 0:
                    snippet = "..." + snippet
                if snippet_end < len(text):
                    snippet = snippet + "..."
            else:
                snippet = "No description available"
            
            results.append(SearchResult(
                id=str(bill.id),
                title=f"Bill {bill.bill_number}: {bill.title}",
                content_type="bill",
                snippet=snippet,
                url=f"/api/v1/bills/{bill.id}/",
                date=bill.introduced_date.isoformat() if bill.introduced_date else None,
                politician_name=None,  # Not directly available in this schema
                relevance_score=1.0  # Could implement actual scoring
            ))
    
    if not content_type or content_type == "politicians":
        # Search politicians
        pol_query = db.query(Member)
        
        # Add name search
        pol_query = pol_query.filter(Member.full_name.ilike(f"%{search_query}%"))
        
        politicians = pol_query.limit(page_size // 3).all()  # Limit politician results
        
        # Convert to search results
        for politician in politicians:
            results.append(SearchResult(
                id=str(politician.id),
                title=f"Member: {politician.full_name}",
                content_type="politician",
                snippet=f"Member of Parliament representing {politician.district or 'Unknown District'}",
                url=f"/api/v1/members/{politician.id}/",
                date=politician.start_date.isoformat() if politician.start_date else None,
                politician_name=politician.full_name,
                relevance_score=1.0  # Could implement actual scoring
            ))
    
    # Sort all results by relevance/date
    if sort == "date":
        results.sort(key=lambda x: x.date or date.min, reverse=True)
    
    return SearchResponse(
        query=search_query,
        total_results=total,
        results=results,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size if total > 0 else 0
    )


@router.get("/suggestions", response_model=SearchSuggestionsResponse)
async def get_search_suggestions(
    q: str = Query(..., description="Partial search query"),
    limit: int = Query(10, ge=1, le=20, description="Maximum number of suggestions"),
    db: DBSession = Depends(get_db)
):
    """
    Get search suggestions for autocomplete functionality.
    
    Based on legacy politician autocomplete and search suggestion features.
    """
    
    if len(q.strip()) < 2:
        return SearchSuggestionsResponse(suggestions=[])
    
    search_query = q.strip()
    
    # Get politician name suggestions
    politicians = db.query(Member).filter(
        Member.full_name.ilike(f"{search_query}%")
    ).limit(limit // 2).all()
    
    # Get bill title suggestions
    bills = db.query(Bill).filter(
        Bill.title.ilike(f"{search_query}%")
    ).limit(limit // 2).all()
    
    suggestions = []
    
    # Add politician suggestions
    for politician in politicians:
        suggestions.append(SearchSuggestion(
            text=politician.full_name,
            type="politician",
            url=f"/api/v1/members/{politician.id}/"
        ))
    
    # Add bill suggestions
    for bill in bills:
        suggestions.append(SearchSuggestion(
            text=f"Bill {bill.bill_number}: {bill.title}",
            type="bill",
            url=f"/api/v1/bills/{bill.id}/"
        ))
    
    return SearchSuggestionsResponse(suggestions=suggestions[:limit])


@router.get("/postcode/{postcode}", response_model=PostcodeResponse)
async def lookup_postcode(
    postcode: str,
    db: DBSession = Depends(get_db)
):
    """
    Look up MP by postal code.
    
    Based on legacy postcode lookup functionality.
    Implements Feature F001: Global Search with Postal Code MP Lookup
    """
    
    # Clean up postcode format
    clean_postcode = postcode.upper().replace(" ", "")
    
    # Validate postal code format (Canadian format: K1A0A6)
    if len(clean_postcode) != 6:
        raise HTTPException(status_code=400, detail="Invalid postal code format. Must be 6 characters (e.g., K1A0A6)")
    
    # Check if it matches Canadian postal code pattern
    import re
    if not re.match(r'^[A-Z]\d[A-Z]\d[A-Z]\d$', clean_postcode):
        raise HTTPException(status_code=400, detail="Invalid postal code format. Must follow Canadian format (e.g., K1A0A6)")
    
    try:
        # Import httpx for external API calls
        import httpx
        
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
                representative_info = {
                    'name': rep.get('name', 'Unknown'),
                    'party': rep.get('party_name', 'Unknown'),
                    'riding': rep.get('district_name', 'Unknown'),
                    'level': rep.get('elected_office', 'Unknown'),
                    'url': rep.get('url', ''),
                    'photo_url': rep.get('photo_url', ''),
                    'email': rep.get('email', ''),
                    'phone': rep.get('offices', [{}])[0].get('tel', '') if rep.get('offices') else ''
                }
                representatives.append(representative_info)
        
        # Create response
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
            detail="Represent API request timed out"
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
