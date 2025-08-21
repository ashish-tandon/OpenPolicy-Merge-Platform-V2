"""
Bill Vote Casting API endpoints for OpenPolicy V2.

Provides endpoints for users to cast votes on bills and track voting history.
This is a critical feature that was missing from the current implementation.
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Body
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import text
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from app.database import get_db
from app.models.openparliament import Bill, ElectedMember, VoteQuestion, Politician, Party, Riding

router = APIRouter()


@router.post("/bills/{bill_id}/cast-vote")
async def cast_bill_vote(
    bill_id: int,
    vote_data: Dict[str, Any] = Body(..., description="Vote data"),
    db: DBSession = Depends(get_db)
):
    """
    Cast a vote on a specific bill.
    Users can vote Yes, No, or Abstain on bills.
    """
    # Validate required fields
    required_fields = ["user_id", "vote_choice", "reason"]
    for field in required_fields:
        if field not in vote_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # Validate vote choice
    valid_choices = ["yes", "no", "abstain"]
    if vote_data["vote_choice"].lower() not in valid_choices:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid vote choice. Must be one of: {', '.join(valid_choices)}"
        )
    
    # Verify bill exists
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # Check if bill is currently open for voting
    # For now, we'll assume all bills are open for voting
    # In a real implementation, this would check bill status and voting windows
    
    # Check if user has already voted on this bill
    # For now, we'll allow multiple votes (in real implementation, this would be restricted)
    
    # For now, create mock vote response
    # In a full implementation, this would save to the database
    vote_record = {
        "id": "vote-123",
        "bill_id": str(bill_id),
        "bill_title": bill.name_en,
        "bill_number": bill.number,
        "user_id": vote_data["user_id"],
        "vote_choice": vote_data["vote_choice"].lower(),
        "reason": vote_data["reason"],
        "confidence_level": vote_data.get("confidence_level", "medium"),
        "vote_date": datetime.utcnow().isoformat(),
        "constituency": vote_data.get("constituency"),
        "party_preference": vote_data.get("party_preference"),
        "influence_factors": vote_data.get("influence_factors", []),
        "related_issues": vote_data.get("related_issues", []),
        "public_visibility": vote_data.get("public_visibility", "public"),
        "vote_weight": vote_data.get("vote_weight", 1.0),
        "metadata": {
            "device": vote_data.get("device", "web"),
            "location": vote_data.get("location"),
            "session_id": vote_data.get("session_id")
        }
    }
    
    return {
        "success": True,
        "message": "Vote cast successfully",
        "vote_record": vote_record,
        "bill_info": {
            "id": str(bill.id),
            "title": bill.name_en,
            "number": bill.number,
            "status": bill.status_code
        }
    }


@router.get("/bills/{bill_id}/user-votes")
async def get_bill_user_votes(
    bill_id: int,
    user_id: Optional[str] = Query(None, description="Filter by specific user"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    Get all user votes for a specific bill.
    Shows how the public is voting on the bill.
    """
    # Verify bill exists
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # For now, create mock user votes data
    # In a full implementation, this would come from the database
    mock_user_votes = [
        {
            "id": "1",
            "bill_id": str(bill_id),
            "bill_title": bill.name_en,
            "user_id": "user-123",
            "username": "john_doe",
            "display_name": "John Doe",
            "vote_choice": "yes",
            "reason": "Strongly support environmental protection measures",
            "confidence_level": "high",
            "vote_date": "2025-01-15T10:30:00Z",
            "constituency": "Toronto Centre",
            "party_preference": "Liberal",
            "influence_factors": ["environmental_concerns", "constituent_feedback"],
            "related_issues": ["climate_change", "pollution_control"],
            "public_visibility": "public",
            "vote_weight": 1.0,
            "user_verified": True,
            "constituency_match": True
        },
        {
            "id": "2",
            "bill_id": str(bill_id),
            "bill_title": bill.name_en,
            "user_id": "user-456",
            "username": "jane_smith",
            "display_name": "Jane Smith",
            "vote_choice": "no",
            "reason": "Concerned about economic impact on small businesses",
            "confidence_level": "medium",
            "vote_date": "2025-01-15T09:15:00Z",
            "constituency": "Calgary Centre",
            "party_preference": "Conservative",
            "influence_factors": ["economic_concerns", "business_interests"],
            "related_issues": ["economic_impact", "business_regulation"],
            "public_visibility": "public",
            "vote_weight": 1.0,
            "user_verified": True,
            "constituency_match": True
        },
        {
            "id": "3",
            "bill_id": str(bill_id),
            "bill_title": bill.name_en,
            "user_id": "user-789",
            "username": "bob_wilson",
            "display_name": "Bob Wilson",
            "vote_choice": "abstain",
            "reason": "Need more information about implementation details",
            "confidence_level": "low",
            "vote_date": "2025-01-15T08:45:00Z",
            "constituency": "Vancouver Centre",
            "party_preference": "Independent",
            "influence_factors": ["information_gaps", "uncertainty"],
            "related_issues": ["implementation", "transparency"],
            "public_visibility": "public",
            "vote_weight": 1.0,
            "user_verified": False,
            "constituency_match": False
        }
    ]
    
    # Apply user filter if specified
    if user_id:
        mock_user_votes = [
            vote for vote in mock_user_votes
            if vote["user_id"] == user_id
        ]
    
    # Apply pagination
    total = len(mock_user_votes)
    offset = (page - 1) * page_size
    paginated_votes = mock_user_votes[offset:offset + page_size]
    
    # Calculate vote statistics
    vote_stats = {
        "total_votes": total,
        "yes_votes": len([v for v in mock_user_votes if v["vote_choice"] == "yes"]),
        "no_votes": len([v for v in mock_user_votes if v["vote_choice"] == "no"]),
        "abstentions": len([v for v in mock_user_votes if v["vote_choice"] == "abstain"]),
        "confidence_breakdown": {
            "high": len([v for v in mock_user_votes if v["confidence_level"] == "high"]),
            "medium": len([v for v in mock_user_votes if v["confidence_level"] == "medium"]),
            "low": len([v for v in mock_user_votes if v["confidence_level"] == "low"])
        },
        "constituency_coverage": len(set(v["constituency"] for v in mock_user_votes if v["constituency"])),
        "party_diversity": len(set(v["party_preference"] for v in mock_user_votes if v["party_preference"]))
    }
    
    return {
        "success": True,
        "results": paginated_votes,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page * page_size < total,
            "has_prev": page > 1
        },
        "vote_statistics": vote_stats,
        "bill_info": {
            "id": str(bill.id),
            "title": bill.name_en,
            "number": bill.number,
            "status": bill.status_code
        }
    }


@router.get("/user/{user_id}/voting-history")
async def get_user_voting_history(
    user_id: str,
    bill_id: Optional[int] = Query(None, description="Filter by specific bill"),
    vote_choice: Optional[str] = Query(None, description="Filter by vote choice"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    Get a user's complete voting history.
    Shows all bills they've voted on and their voting patterns.
    """
    # For now, create mock voting history data
    # In a full implementation, this would come from the database
    mock_voting_history = [
        {
            "id": "1",
            "user_id": user_id,
            "bill_id": "123",
            "bill_title": "Environmental Protection Act",
            "bill_number": "C-123",
            "vote_choice": "yes",
            "reason": "Strongly support environmental protection measures",
            "confidence_level": "high",
            "vote_date": "2025-01-15T10:30:00Z",
            "bill_status": "Second Reading",
            "constituency": "Toronto Centre",
            "party_preference": "Liberal",
            "influence_factors": ["environmental_concerns", "constituent_feedback"],
            "related_issues": ["climate_change", "pollution_control"],
            "vote_weight": 1.0,
            "bill_outcome": "Passed",
            "mp_vote_match": True,
            "constituency_consensus": "high"
        },
        {
            "id": "2",
            "user_id": user_id,
            "bill_id": "124",
            "bill_title": "Economic Recovery Act",
            "bill_number": "C-124",
            "vote_choice": "no",
            "reason": "Concerned about increased government spending",
            "confidence_level": "medium",
            "vote_date": "2025-01-10T14:20:00Z",
            "bill_status": "Third Reading",
            "constituency": "Toronto Centre",
            "party_preference": "Liberal",
            "influence_factors": ["fiscal_concerns", "economic_philosophy"],
            "related_issues": ["government_spending", "economic_policy"],
            "vote_weight": 1.0,
            "bill_outcome": "Passed",
            "mp_vote_match": False,
            "constituency_consensus": "medium"
        },
        {
            "id": "3",
            "user_id": user_id,
            "bill_id": "125",
            "bill_title": "Healthcare Accessibility Act",
            "bill_number": "C-125",
            "vote_choice": "yes",
            "reason": "Universal healthcare is a fundamental right",
            "confidence_level": "high",
            "vote_date": "2025-01-05T11:15:00Z",
            "bill_status": "Royal Assent",
            "constituency": "Toronto Centre",
            "party_preference": "Liberal",
            "influence_factors": ["healthcare_values", "social_justice"],
            "related_issues": ["healthcare", "accessibility"],
            "vote_weight": 1.0,
            "bill_outcome": "Passed",
            "mp_vote_match": True,
            "constituency_consensus": "very_high"
        }
    ]
    
    # Apply filters
    filtered_history = mock_voting_history
    
    if bill_id:
        filtered_history = [
            vote for vote in filtered_history
            if vote["bill_id"] == str(bill_id)
        ]
    
    if vote_choice:
        filtered_history = [
            vote for vote in filtered_history
            if vote["vote_choice"] == vote_choice.lower()
        ]
    
    # Apply pagination
    total = len(filtered_history)
    offset = (page - 1) * page_size
    paginated_history = filtered_history[offset:offset + page_size]
    
    # Calculate user voting statistics
    user_stats = {
        "total_votes_cast": total,
        "voting_pattern": {
            "yes_votes": len([v for v in filtered_history if v["vote_choice"] == "yes"]),
            "no_votes": len([v for v in filtered_history if v["vote_choice"] == "no"]),
            "abstentions": len([v for v in filtered_history if v["vote_choice"] == "abstain"])
        },
        "confidence_breakdown": {
            "high": len([v for v in filtered_history if v["confidence_level"] == "high"]),
            "medium": len([v for v in filtered_history if v["confidence_level"] == "medium"]),
            "low": len([v for v in filtered_history if v["confidence_level"] == "low"])
        },
        "mp_vote_alignment": {
            "matches": len([v for v in filtered_history if v["mp_vote_match"]]),
            "mismatches": len([v for v in filtered_history if not v["mp_vote_match"]])
        },
        "constituency_alignment": {
            "high_consensus": len([v for v in filtered_history if v["constituency_consensus"] in ["high", "very_high"]]),
            "medium_consensus": len([v for v in filtered_history if v["constituency_consensus"] == "medium"]),
            "low_consensus": len([v for v in filtered_history if v["constituency_consensus"] == "low"])
        },
        "top_issues": ["environment", "healthcare", "economy"],
        "voting_frequency": "regular",
        "influence_score": 8.5
    }
    
    return {
        "success": True,
        "results": paginated_history,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page * page_size < total,
            "has_prev": page > 1
        },
        "user_voting_statistics": user_stats,
        "filters_applied": {
            "bill_id": bill_id,
            "vote_choice": vote_choice,
            "date_range": f"{date_from} to {date_to}" if date_from and date_to else None
        }
    }


@router.get("/bills/{bill_id}/voting-summary")
async def get_bill_voting_summary(
    bill_id: int,
    db: DBSession = Depends(get_db)
):
    """
    Get comprehensive voting summary for a specific bill.
    Shows public opinion, constituency breakdown, and voting trends.
    """
    # Verify bill exists
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # For now, create mock voting summary data
    # In a full implementation, this would aggregate from the database
    mock_voting_summary = {
        "bill_info": {
            "id": str(bill.id),
            "title": bill.name_en,
            "number": bill.number,
            "status": bill.status_code,
            "introduced_date": bill.introduced,
            "sponsor": "Hon. Member Smith",
            "sponsor_party": "Liberal"
        },
        "overall_statistics": {
            "total_votes_cast": 1250,
            "yes_votes": 789,
            "no_votes": 312,
            "abstentions": 149,
            "yes_percentage": 63.1,
            "no_percentage": 25.0,
            "abstain_percentage": 11.9
        },
        "constituency_breakdown": {
            "total_constituencies": 45,
            "constituencies_with_votes": 42,
            "constituency_coverage": 93.3,
            "top_supporting_constituencies": [
                {"name": "Vancouver Centre", "yes_percentage": 78.5, "total_votes": 45},
                {"name": "Toronto Centre", "yes_percentage": 76.2, "total_votes": 67},
                {"name": "Montreal Centre", "yes_percentage": 74.8, "total_votes": 52}
            ],
            "top_opposing_constituencies": [
                {"name": "Calgary Centre", "no_percentage": 68.3, "total_votes": 38},
                {"name": "Edmonton Centre", "no_percentage": 65.7, "total_votes": 41},
                {"name": "Winnipeg Centre", "no_percentage": 62.1, "total_votes": 29}
            ]
        },
        "demographic_breakdown": {
            "age_groups": {
                "18-25": {"yes": 85, "no": 12, "abstain": 8},
                "26-35": {"yes": 234, "no": 67, "abstain": 23},
                "36-45": {"yes": 198, "no": 89, "abstain": 34},
                "46-55": {"yes": 156, "no": 78, "abstain": 45},
                "55+": {"yes": 116, "no": 66, "abstain": 39}
            },
            "party_preferences": {
                "Liberal": {"yes": 89.2, "no": 8.1, "abstain": 2.7},
                "Conservative": {"yes": 23.4, "no": 71.8, "abstain": 4.8},
                "NDP": {"yes": 94.7, "no": 3.2, "abstain": 2.1},
                "Green": {"yes": 98.5, "no": 1.2, "abstain": 0.3},
                "Independent": {"yes": 67.3, "no": 25.4, "abstain": 7.3}
            }
        },
        "voting_trends": {
            "daily_voting": {
                "2025-01-10": 89,
                "2025-01-11": 156,
                "2025-01-12": 234,
                "2025-01-13": 198,
                "2025-01-14": 167,
                "2025-01-15": 406
            },
            "peak_voting_time": "7:00 PM - 9:00 PM",
            "voting_momentum": "increasing",
            "constituency_spread": "rapid"
        },
        "issue_analysis": {
            "top_reasons_for_yes": [
                "Environmental protection is crucial",
                "Climate action is needed now",
                "Future generations will benefit",
                "International leadership opportunity"
            ],
            "top_reasons_for_no": [
                "Economic impact concerns",
                "Too much government regulation",
                "Implementation costs too high",
                "Timeline is too aggressive"
            ],
            "key_issues": ["environment", "economy", "regulation", "climate_change"]
        },
        "confidence_analysis": {
            "high_confidence_votes": 789,
            "medium_confidence_votes": 312,
            "low_confidence_votes": 149,
            "average_confidence": 8.2
        },
        "influence_metrics": {
            "constituency_representativeness": 0.87,
            "demographic_balance": 0.82,
            "geographic_coverage": 0.93,
            "overall_quality_score": 8.7
        }
    }
    
    return {
        "success": True,
        "voting_summary": mock_voting_summary,
        "generated_at": datetime.utcnow().isoformat()
    }


@router.get("/user/{user_id}/voting-recommendations")
async def get_voting_recommendations(
    user_id: str,
    bill_id: Optional[int] = Query(None, description="Specific bill for recommendation"),
    db: DBSession = Depends(get_db)
):
    """
    Get personalized voting recommendations for a user.
    Based on their voting history, preferences, and constituency alignment.
    """
    # For now, create mock recommendation data
    # In a full implementation, this would use ML algorithms
    mock_recommendations = {
        "user_id": user_id,
        "recommendations": [
            {
                "bill_id": "126",
                "bill_title": "Digital Privacy Protection Act",
                "bill_number": "C-126",
                "recommended_vote": "yes",
                "confidence_score": 0.89,
                "reasoning": [
                    "Strong alignment with your privacy values",
                    "Consistent with your previous voting patterns",
                    "High support in your constituency",
                    "Matches your party preference"
                ],
                "constituency_alignment": 0.92,
                "party_alignment": 0.88,
                "issue_alignment": 0.91,
                "mp_vote_prediction": "yes",
                "constituency_consensus_prediction": "high"
            },
            {
                "bill_id": "127",
                "bill_title": "Infrastructure Investment Act",
                "bill_number": "C-127",
                "recommended_vote": "abstain",
                "confidence_score": 0.67,
                "reasoning": [
                    "Mixed signals from your voting history",
                    "Uncertain economic impact",
                    "Constituency is divided on this issue",
                    "Need more information to make informed decision"
                ],
                "constituency_alignment": 0.45,
                "party_alignment": 0.52,
                "issue_alignment": 0.38,
                "mp_vote_prediction": "yes",
                "constituency_consensus_prediction": "medium"
            }
        ],
        "recommendation_factors": {
            "voting_history_weight": 0.35,
            "constituency_alignment_weight": 0.25,
            "party_preference_weight": 0.20,
            "issue_alignment_weight": 0.15,
            "mp_alignment_weight": 0.05
        },
        "accuracy_metrics": {
            "historical_accuracy": 0.87,
            "constituency_prediction_accuracy": 0.82,
            "party_prediction_accuracy": 0.79,
            "overall_recommendation_accuracy": 0.84
        }
    }
    
    return {
        "success": True,
        "recommendations": mock_recommendations,
        "generated_at": datetime.utcnow().isoformat()
    }
