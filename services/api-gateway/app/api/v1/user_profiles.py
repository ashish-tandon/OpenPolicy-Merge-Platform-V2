"""
User Profiles API endpoints for OpenPolicy V2.

Provides endpoints for user profiles, analytics, and preferences.
This is adapted from the legacy OpenPolicy Infrastructure profile functionality.
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Body
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import text
from typing import Optional, List, Dict, Any
from app.database import get_db
from app.models.openparliament import Bill, ElectedMember, VoteQuestion, Politician, Party, Riding

router = APIRouter()


@router.get("/analytics")
async def get_user_analytics(
    user_id: str = Query(..., description="User ID for analytics"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: DBSession = Depends(get_db)
):
    """
    Get comprehensive user analytics and statistics.
    Provides insights into user engagement with parliamentary content.
    """
    # For now, create mock user analytics data
    # In a full implementation, this would come from user activity tracking
    mock_analytics = {
        "user_id": user_id,
        "period": f"{date_from} to {date_to}" if date_from and date_to else "All time",
        "engagement_summary": {
            "total_visits": 156,
            "active_days": 45,
            "last_activity": "2025-01-15",
            "engagement_score": 8.7
        },
        "content_interaction": {
            "bills_viewed": 89,
            "bills_supported": 23,
            "bills_bookmarked": 15,
            "mps_researched": 34,
            "votes_analyzed": 67,
            "debates_read": 45
        },
        "activity_breakdown": {
            "by_month": {
                "2024-11": 12,
                "2024-12": 18,
                "2025-01": 25
            },
            "by_content_type": {
                "bills": 45,
                "mps": 23,
                "votes": 34,
                "debates": 28,
                "committees": 26
            },
            "by_time_of_day": {
                "morning": 23,
                "afternoon": 45,
                "evening": 67,
                "night": 21
            }
        },
        "preferences": {
            "favorite_topics": ["Environment", "Health", "Economy", "Justice"],
            "favorite_mps": ["Hon. Member Smith", "Hon. Member Johnson"],
            "favorite_parties": ["Liberal", "Green"],
            "notification_preferences": {
                "email": True,
                "push": False,
                "sms": False
            }
        },
        "geographic_interest": {
            "primary_constituency": "Toronto Centre",
            "secondary_constituencies": ["Vancouver Centre", "Montreal Centre"],
            "province_breakdown": {
                "Ontario": 45,
                "British Columbia": 23,
                "Quebec": 18,
                "Alberta": 12,
                "Other": 2
            }
        },
        "social_engagement": {
            "shares": 23,
            "comments": 45,
            "followers": 12,
            "following": 8
        },
        "learning_progress": {
            "parliamentary_education_modules": 3,
            "voting_guides_read": 5,
            "committee_work_understood": "Intermediate",
            "bill_process_knowledge": "Advanced"
        }
    }
    
    return {
        "success": True,
        "analytics": mock_analytics,
        "generated_at": "2025-01-15T10:30:00Z"
    }


@router.post("/postal-code")
async def update_postal_code(
    user_id: str = Body(..., description="User ID"),
    postal_code: str = Body(..., description="New postal code"),
    db: DBSession = Depends(get_db)
):
    """
    Update user's postal code and find their MP.
    """
    # Validate postal code format (Canadian format)
    if not postal_code or len(postal_code) < 6:
        raise HTTPException(status_code=400, detail="Invalid postal code format")
    
    # For now, create mock MP data based on postal code
    # In a full implementation, this would query the database for the MP
    mock_mp_data = {
        "user_id": user_id,
        "postal_code": postal_code,
        "mp_found": True,
        "mp_details": {
            "id": "123",
            "name": "Hon. Member Smith",
            "party": "Liberal",
            "constituency": "Toronto Centre",
            "constituency_id": "35061",
            "province": "Ontario",
            "riding_name": "Toronto Centre",
            "contact_info": {
                "parliament_office": "613-992-1234",
                "constituency_office": "416-555-1234",
                "email": "member.smith@parl.gc.ca",
                "website": "https://membersmith.liberal.ca"
            },
            "social_media": {
                "twitter": "@MemberSmith",
                "facebook": "MemberSmithMP",
                "instagram": "membersmithmp"
            }
        },
        "constituency_info": {
            "population": 125000,
            "area_km2": 12.5,
            "demographics": {
                "median_age": 35,
                "median_income": 75000,
                "education_level": "High"
            },
            "key_issues": ["Housing", "Transit", "Environment", "Healthcare"]
        },
        "updated_at": "2025-01-15T10:30:00Z"
    }
    
    return {
        "success": True,
        "message": "Postal code updated successfully",
        "data": mock_mp_data
    }


@router.get("/constituency/{postal_code}")
async def get_constituency_by_postal_code(
    postal_code: str,
    db: DBSession = Depends(get_db)
):
    """
    Get constituency information by postal code.
    """
    # Validate postal code format
    if not postal_code or len(postal_code) < 6:
        raise HTTPException(status_code=400, detail="Invalid postal code format")
    
    # For now, create mock constituency data
    # In a full implementation, this would query the database
    mock_constituency_data = {
        "postal_code": postal_code,
        "constituency": {
            "id": "35061",
            "name": "Toronto Centre",
            "province": "Ontario",
            "federal_riding": "35061",
            "provincial_riding": "35061",
            "municipal_ward": "Ward 13"
        },
        "current_mp": {
            "id": "123",
            "name": "Hon. Member Smith",
            "party": "Liberal",
            "party_color": "#FF9999",
            "elected_date": "2021-09-20",
            "term_start": "2021-11-22",
            "experience": "2nd term",
            "committee_memberships": [
                "Standing Committee on Finance",
                "Standing Committee on Health"
            ]
        },
        "previous_mps": [
            {
                "name": "Hon. Member Brown",
                "party": "Conservative",
                "term": "2019-2021",
                "current_status": "Former MP"
            },
            {
                "name": "Hon. Member Davis",
                "party": "Liberal",
                "term": "2015-2019",
                "current_status": "Former MP"
            }
        ],
        "demographics": {
            "population": 125000,
            "area_km2": 12.5,
            "density_per_km2": 10000,
            "median_age": 35,
            "median_income": 75000,
            "education_level": "High",
            "languages": ["English", "French", "Mandarin", "Spanish"]
        },
        "key_issues": [
            "Housing affordability",
            "Public transit",
            "Environmental protection",
            "Healthcare access",
            "Economic development"
        ],
        "notable_places": [
            "University of Toronto",
            "Royal Ontario Museum",
            "Eaton Centre",
            "Yonge-Dundas Square",
            "St. Lawrence Market"
        ],
        "election_history": {
            "2021": {"winner": "Liberal", "margin": "15.2%", "turnout": "68.5%"},
            "2019": {"winner": "Conservative", "margin": "2.1%", "turnout": "65.2%"},
            "2015": {"winner": "Liberal", "margin": "18.7%", "turnout": "70.1%"}
        }
    }
    
    return {
        "success": True,
        "data": mock_constituency_data
    }


@router.get("/user/{user_id}/activity")
async def get_user_activity(
    user_id: str,
    activity_type: Optional[str] = Query(None, description="Type of activity to filter"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    Get detailed user activity timeline.
    """
    # For now, create mock user activity data
    # In a full implementation, this would come from user activity tracking
    mock_activities = [
        {
            "id": "1",
            "user_id": user_id,
            "activity_type": "bill_view",
            "activity_date": "2025-01-15T14:30:00Z",
            "content_id": "123",
            "content_type": "bill",
            "content_title": "Environmental Protection Act",
            "content_summary": "Viewed Bill C-123 on environmental protection",
            "interaction_details": {
                "time_spent": "5 minutes",
                "pages_viewed": 3,
                "actions_taken": ["read", "bookmarked"]
            },
            "related_content": {
                "bills": ["C-123"],
                "mps": ["Hon. Member Smith"],
                "committees": ["Standing Committee on Environment"]
            },
            "metadata": {
                "device": "Desktop",
                "browser": "Chrome",
                "location": "Toronto, ON"
            }
        },
        {
            "id": "2",
            "user_id": user_id,
            "activity_type": "mp_research",
            "activity_date": "2025-01-15T10:15:00Z",
            "content_id": "456",
            "content_type": "mp",
            "content_title": "Hon. Member Johnson",
            "content_summary": "Researched MP profile and voting record",
            "interaction_details": {
                "time_spent": "8 minutes",
                "pages_viewed": 5,
                "actions_taken": ["read", "searched", "compared"]
            },
            "related_content": {
                "bills": ["C-123", "C-124"],
                "votes": ["V-123", "V-124"],
                "committees": ["Standing Committee on Finance"]
            },
            "metadata": {
                "device": "Mobile",
                "browser": "Safari",
                "location": "Toronto, ON"
            }
        },
        {
            "id": "3",
            "user_id": user_id,
            "activity_type": "vote_analysis",
            "activity_date": "2025-01-14T16:45:00Z",
            "content_id": "789",
            "content_type": "vote",
            "content_title": "Vote on Bill C-123",
            "content_summary": "Analyzed voting patterns and party positions",
            "interaction_details": {
                "time_spent": "12 minutes",
                "pages_viewed": 4,
                "actions_taken": ["analyzed", "shared", "commented"]
            },
            "related_content": {
                "bills": ["C-123"],
                "mps": ["Hon. Member Smith", "Hon. Member Johnson"],
                "parties": ["Liberal", "Conservative", "NDP"]
            },
            "metadata": {
                "device": "Desktop",
                "browser": "Firefox",
                "location": "Toronto, ON"
            }
        }
    ]
    
    # Apply filters
    filtered_activities = mock_activities
    
    if activity_type:
        filtered_activities = [
            activity for activity in filtered_activities
            if activity["activity_type"] == activity_type
        ]
    
    # Apply pagination
    total = len(filtered_activities)
    offset = (page - 1) * page_size
    paginated_activities = filtered_activities[offset:offset + page_size]
    
    return {
        "success": True,
        "results": paginated_activities,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page * page_size < total,
            "has_prev": page > 1
        },
        "filters_applied": {
            "activity_type": activity_type,
            "date_range": f"{date_from} to {date_to}" if date_from and date_to else None
        }
    }


@router.get("/user/{user_id}/preferences")
async def get_user_preferences(
    user_id: str,
    db: DBSession = Depends(get_db)
):
    """
    Get user preferences and settings.
    """
    # For now, create mock user preferences
    # In a full implementation, this would come from user settings
    mock_preferences = {
        "user_id": user_id,
        "notification_settings": {
            "email": {
                "enabled": True,
                "frequency": "daily",
                "types": ["bill_updates", "mp_activity", "vote_results", "committee_reports"]
            },
            "push": {
                "enabled": False,
                "frequency": "realtime",
                "types": ["urgent_alerts", "breaking_news"]
            },
            "sms": {
                "enabled": False,
                "frequency": "never",
                "types": []
            }
        },
        "content_preferences": {
            "favorite_topics": ["Environment", "Health", "Economy", "Justice", "Education"],
            "favorite_mps": ["Hon. Member Smith", "Hon. Member Johnson", "Hon. Member Davis"],
            "favorite_parties": ["Liberal", "Green", "NDP"],
            "excluded_topics": ["Sports", "Entertainment"],
            "language_preference": "English",
            "content_difficulty": "Intermediate"
        },
        "display_preferences": {
            "theme": "light",
            "font_size": "medium",
            "show_advanced_features": True,
            "show_analytics": True,
            "show_social_features": False
        },
        "privacy_settings": {
            "profile_visibility": "public",
            "activity_sharing": "friends_only",
            "data_collection": True,
            "third_party_sharing": False
        },
        "accessibility": {
            "high_contrast": False,
            "screen_reader": False,
            "keyboard_navigation": True,
            "reduced_motion": False
        }
    }
    
    return {
        "success": True,
        "preferences": mock_preferences
    }


@router.put("/user/{user_id}/preferences")
async def update_user_preferences(
    user_id: str,
    preferences: Dict[str, Any] = Body(..., description="Updated preferences"),
    db: DBSession = Depends(get_db)
):
    """
    Update user preferences and settings.
    """
    # Validate preferences structure
    if not preferences:
        raise HTTPException(status_code=400, detail="Preferences data is required")
    
    # For now, return success response
    # In a full implementation, this would update the database
    return {
        "success": True,
        "message": "Preferences updated successfully",
        "user_id": user_id,
        "updated_at": "2025-01-15T10:30:00Z",
        "updated_preferences": preferences
    }
