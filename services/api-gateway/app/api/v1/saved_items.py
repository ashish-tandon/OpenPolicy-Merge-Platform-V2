"""
Saved Items API endpoints for OpenPolicy V2.

Provides endpoints for user bookmarks, saved items, and content preferences.
This is adapted from the legacy OpenPolicy Infrastructure bookmark functionality.
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Body
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import text
from typing import Optional, List, Dict, Any
from app.database import get_db
from app.models.openparliament import Bill, ElectedMember, VoteQuestion, Politician, Party, Riding

router = APIRouter()


@router.get("/user/{user_id}/saved-items")
async def get_user_saved_items(
    user_id: str,
    content_type: Optional[str] = Query(None, description="Type of content to filter"),
    tags: Optional[str] = Query(None, description="Comma-separated tags to filter by"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    Get user's saved items and bookmarks.
    """
    # For now, create mock saved items data
    # In a full implementation, this would come from user bookmarks database
    mock_saved_items = [
        {
            "id": "1",
            "user_id": user_id,
            "content_type": "bill",
            "content_id": "123",
            "content_title": "Environmental Protection Act",
            "content_summary": "Bill C-123 on environmental protection and climate action",
            "content_url": "/bills/123",
            "saved_date": "2025-01-15T10:30:00Z",
            "tags": ["environment", "climate", "legislation", "important"],
            "notes": "Key bill to track for environmental policy",
            "priority": "high",
            "reminder_date": "2025-02-01T00:00:00Z",
            "content_metadata": {
                "bill_number": "C-123",
                "sponsor": "Hon. Member Smith",
                "status": "Second Reading",
                "introduced_date": "2025-01-10"
            },
            "last_updated": "2025-01-15T10:30:00Z"
        },
        {
            "id": "2",
            "user_id": user_id,
            "content_type": "mp",
            "content_id": "456",
            "content_title": "Hon. Member Johnson",
            "content_summary": "MP profile and voting record for Hon. Member Johnson",
            "content_url": "/mps/456",
            "saved_date": "2025-01-14T14:20:00Z",
            "tags": ["mp", "voting", "constituency", "research"],
            "notes": "Interesting voting patterns on environmental bills",
            "priority": "medium",
            "reminder_date": None,
            "content_metadata": {
                "constituency": "Vancouver Centre",
                "party": "Green",
                "experience": "2nd term",
                "committee_memberships": ["Environment", "Health"]
            },
            "last_updated": "2025-01-14T14:20:00Z"
        },
        {
            "id": "3",
            "user_id": user_id,
            "content_type": "vote",
            "content_id": "789",
            "content_title": "Vote on Bill C-123",
            "content_summary": "Second reading vote on Environmental Protection Act",
            "content_url": "/votes/789",
            "saved_date": "2025-01-13T16:45:00Z",
            "tags": ["vote", "environment", "analysis", "party_positions"],
            "notes": "Important vote showing party divisions on environment",
            "priority": "high",
            "reminder_date": "2025-01-20T00:00:00Z",
            "content_metadata": {
                "vote_date": "2025-01-13",
                "result": "Passed",
                "total_votes": 338,
                "yes_votes": 245,
                "no_votes": 93
            },
            "last_updated": "2025-01-13T16:45:00Z"
        },
        {
            "id": "4",
            "user_id": user_id,
            "content_type": "committee",
            "content_id": "101",
            "content_title": "Standing Committee on Environment",
            "content_summary": "Committee studying environmental legislation and policy",
            "content_url": "/committees/101",
            "saved_date": "2025-01-12T09:15:00Z",
            "tags": ["committee", "environment", "policy", "study"],
            "notes": "Key committee for environmental policy development",
            "priority": "medium",
            "reminder_date": None,
            "content_metadata": {
                "committee_type": "Standing",
                "chair": "Hon. Member Davis",
                "focus_areas": ["Climate Change", "Biodiversity", "Pollution Control"]
            },
            "last_updated": "2025-01-12T09:15:00Z"
        },
        {
            "id": "5",
            "user_id": user_id,
            "content_type": "debate",
            "content_id": "202",
            "content_title": "Debate on Environmental Policy",
            "content_summary": "Parliamentary debate on government environmental initiatives",
            "content_url": "/debates/202",
            "saved_date": "2025-01-11T11:30:00Z",
            "tags": ["debate", "environment", "government", "policy"],
            "notes": "Good overview of government environmental priorities",
            "priority": "low",
            "reminder_date": None,
            "content_metadata": {
                "debate_date": "2025-01-11",
                "debate_type": "Government Orders",
                "duration": "2 hours 15 minutes",
                "participants": 15
            },
            "last_updated": "2025-01-11T11:30:00Z"
        }
    ]
    
    # Apply filters
    filtered_items = mock_saved_items
    
    if content_type:
        filtered_items = [
            item for item in filtered_items
            if item["content_type"] == content_type
        ]
    
    if tags:
        tag_list = [tag.strip().lower() for tag in tags.split(",")]
        filtered_items = [
            item for item in filtered_items
            if any(tag in [t.lower() for t in item["tags"]] for tag in tag_list)
        ]
    
    # Apply pagination
    total = len(filtered_items)
    offset = (page - 1) * page_size
    paginated_items = filtered_items[offset:offset + page_size]
    
    return {
        "success": True,
        "results": paginated_items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page * page_size < total,
            "has_prev": page > 1
        },
        "filters_applied": {
            "content_type": content_type,
            "tags": tags,
            "date_range": f"{date_from} to {date_to}" if date_from and date_to else None
        },
        "summary": {
            "total_saved_items": total,
            "by_content_type": {
                "bills": len([item for item in filtered_items if item["content_type"] == "bill"]),
                "mps": len([item for item in filtered_items if item["content_type"] == "mp"]),
                "votes": len([item for item in filtered_items if item["content_type"] == "vote"]),
                "committees": len([item for item in filtered_items if item["content_type"] == "committee"]),
                "debates": len([item for item in filtered_items if item["content_type"] == "debate"])
            },
            "by_priority": {
                "high": len([item for item in filtered_items if item["priority"] == "high"]),
                "medium": len([item for item in filtered_items if item["priority"] == "medium"]),
                "low": len([item for item in filtered_items if item["priority"] == "low"])
            }
        }
    }


@router.post("/user/{user_id}/save-item")
async def save_item(
    user_id: str,
    content_data: Dict[str, Any] = Body(..., description="Content to save"),
    db: DBSession = Depends(get_db)
):
    """
    Save a new item to user's bookmarks.
    """
    # Validate required fields
    required_fields = ["content_type", "content_id", "content_title"]
    for field in required_fields:
        if field not in content_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # For now, return success response
    # In a full implementation, this would save to the database
    saved_item = {
        "id": "new-item-id",
        "user_id": user_id,
        "content_type": content_data["content_type"],
        "content_id": content_data["content_id"],
        "content_title": content_data["content_title"],
        "content_summary": content_data.get("content_summary", ""),
        "content_url": content_data.get("content_url", ""),
        "saved_date": "2025-01-15T10:30:00Z",
        "tags": content_data.get("tags", []),
        "notes": content_data.get("notes", ""),
        "priority": content_data.get("priority", "medium"),
        "reminder_date": content_data.get("reminder_date"),
        "content_metadata": content_data.get("content_metadata", {}),
        "last_updated": "2025-01-15T10:30:00Z"
    }
    
    return {
        "success": True,
        "message": "Item saved successfully",
        "saved_item": saved_item
    }


@router.put("/user/{user_id}/saved-items/{item_id}")
async def update_saved_item(
    user_id: str,
    item_id: str,
    update_data: Dict[str, Any] = Body(..., description="Updated item data"),
    db: DBSession = Depends(get_db)
):
    """
    Update a saved item (tags, notes, priority, etc.).
    """
    # Validate update data
    allowed_fields = ["tags", "notes", "priority", "reminder_date"]
    invalid_fields = [field for field in update_data.keys() if field not in allowed_fields]
    
    if invalid_fields:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid fields for update: {', '.join(invalid_fields)}"
        )
    
    # For now, return success response
    # In a full implementation, this would update the database
    return {
        "success": True,
        "message": "Item updated successfully",
        "item_id": item_id,
        "updated_fields": list(update_data.keys()),
        "updated_at": "2025-01-15T10:30:00Z"
    }


@router.delete("/user/{user_id}/saved-items/{item_id}")
async def delete_saved_item(
    user_id: str,
    item_id: str,
    db: DBSession = Depends(get_db)
):
    """
    Remove an item from user's saved items.
    """
    # For now, return success response
    # In a full implementation, this would delete from the database
    return {
        "success": True,
        "message": "Item removed successfully",
        "item_id": item_id,
        "deleted_at": "2025-01-15T10:30:00Z"
    }


@router.get("/user/{user_id}/saved-items/tags")
async def get_user_tags(
    user_id: str,
    db: DBSession = Depends(get_db)
):
    """
    Get all tags used by the user across their saved items.
    """
    # For now, create mock tags data
    # In a full implementation, this would aggregate from the database
    mock_tags = [
        {"tag": "environment", "count": 8, "last_used": "2025-01-15T10:30:00Z"},
        {"tag": "legislation", "count": 6, "last_used": "2025-01-14T14:20:00Z"},
        {"tag": "voting", "count": 5, "last_used": "2025-01-13T16:45:00Z"},
        {"tag": "mp", "count": 4, "last_used": "2025-01-14T14:20:00Z"},
        {"tag": "climate", "count": 3, "last_used": "2025-01-15T10:30:00Z"},
        {"tag": "committee", "count": 3, "last_used": "2025-01-12T09:15:00Z"},
        {"tag": "policy", "count": 3, "last_used": "2025-01-11T11:30:00Z"},
        {"tag": "important", "count": 2, "last_used": "2025-01-15T10:30:00Z"},
        {"tag": "analysis", "count": 2, "last_used": "2025-01-13T16:45:00Z"},
        {"tag": "research", "count": 2, "last_used": "2025-01-14T14:20:00Z"},
        {"tag": "constituency", "count": 1, "last_used": "2025-01-14T14:20:00Z"},
        {"tag": "party_positions", "count": 1, "last_used": "2025-01-13T16:45:00Z"},
        {"tag": "study", "count": 1, "last_used": "2025-01-12T09:15:00Z"},
        {"tag": "government", "count": 1, "last_used": "2025-01-11T11:30:00Z"}
    ]
    
    return {
        "success": True,
        "tags": mock_tags,
        "total_tags": len(mock_tags),
        "most_used_tags": [tag["tag"] for tag in sorted(mock_tags, key=lambda x: x["count"], reverse=True)[:5]]
    }


@router.get("/user/{user_id}/saved-items/search")
async def search_saved_items(
    user_id: str,
    q: str = Query(..., description="Search query"),
    content_type: Optional[str] = Query(None, description="Filter by content type"),
    tags: Optional[str] = Query(None, description="Filter by tags"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    Search through user's saved items.
    """
    # For now, create mock search results
    # In a full implementation, this would search the database
    mock_search_results = [
        {
            "id": "1",
            "user_id": user_id,
            "content_type": "bill",
            "content_id": "123",
            "content_title": "Environmental Protection Act",
            "content_summary": "Bill C-123 on environmental protection and climate action",
            "content_url": "/bills/123",
            "saved_date": "2025-01-15T10:30:00Z",
            "tags": ["environment", "climate", "legislation", "important"],
            "notes": "Key bill to track for environmental policy",
            "priority": "high",
            "search_relevance": 0.95,
            "matched_fields": ["title", "summary", "notes", "tags"]
        },
        {
            "id": "3",
            "user_id": user_id,
            "content_type": "vote",
            "content_id": "789",
            "content_title": "Vote on Bill C-123",
            "content_summary": "Second reading vote on Environmental Protection Act",
            "content_url": "/votes/789",
            "saved_date": "2025-01-13T16:45:00Z",
            "tags": ["vote", "environment", "analysis", "party_positions"],
            "notes": "Important vote showing party divisions on environment",
            "priority": "high",
            "search_relevance": 0.87,
            "matched_fields": ["title", "summary", "notes"]
        }
    ]
    
    # Apply filters
    filtered_results = mock_search_results
    
    if content_type:
        filtered_results = [
            result for result in filtered_results
            if result["content_type"] == content_type
        ]
    
    if tags:
        tag_list = [tag.strip().lower() for tag in tags.split(",")]
        filtered_results = [
            result for result in filtered_results
            if any(tag in [t.lower() for t in result["tags"]] for tag in tag_list)
        ]
    
    # Sort by relevance
    filtered_results.sort(key=lambda x: x["search_relevance"], reverse=True)
    
    # Apply pagination
    total = len(filtered_results)
    offset = (page - 1) * page_size
    paginated_results = filtered_results[offset:offset + page_size]
    
    return {
        "success": True,
        "query": q,
        "results": paginated_results,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page * page_size < total,
            "has_prev": page > 1
        },
        "filters_applied": {
            "content_type": content_type,
            "tags": tags
        },
        "search_stats": {
            "total_results": total,
            "search_time_ms": 45,
            "query_suggestions": ["environmental", "protection", "climate"]
        }
    }
