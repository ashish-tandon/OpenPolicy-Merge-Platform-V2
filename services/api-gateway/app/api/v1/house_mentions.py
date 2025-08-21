"""
House Mentions API endpoints for OpenParliament data.

Provides endpoints for tracking parliamentary activity, debate mentions, and committee activity.
This is adapted from the legacy OpenPolicy Infrastructure house mention functionality.
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import text
from typing import Optional, List
from app.database import get_db
from app.models.openparliament import Bill, ElectedMember, VoteQuestion, Politician, Party, Riding

router = APIRouter()


@router.get("/bills/{bill_id}/mentions")
async def get_bill_house_mentions(
    bill_id: int,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    Get house mentions for a specific bill.
    Tracks when and how bills are mentioned in parliamentary debates.
    """
    # Verify bill exists
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # For now, create mock house mention data
    # In a full implementation, this would come from debate transcripts and committee records
    mock_mentions = [
        {
            "id": "1",
            "bill_id": str(bill_id),
            "bill_title": bill.name_en,
            "mention_date": "2025-01-15",
            "mention_type": "debate",
            "context": "Second reading debate on the bill",
            "speaker_name": "Hon. Member Smith",
            "speaker_party": "Liberal",
            "speaker_constituency": "Toronto Centre",
            "debate_url": f"/debates/2025-01-15/bill-{bill.number}",
            "transcript_excerpt": f"The honourable member has introduced {bill.name_en} which addresses important concerns...",
            "committee_reference": None,
            "vote_reference": None,
            "media_coverage": [],
            "public_response": None,
            "source": "House of Commons Hansard"
        },
        {
            "id": "2",
            "bill_id": str(bill_id),
            "bill_title": bill.name_en,
            "mention_date": "2025-01-10",
            "mention_type": "committee",
            "context": "Committee study of the bill",
            "speaker_name": "Committee Chair",
            "speaker_party": "Conservative",
            "speaker_constituency": "Calgary Centre",
            "debate_url": None,
            "transcript_excerpt": f"The committee will now study {bill.name_en} in detail...",
            "committee_reference": "Standing Committee on Justice",
            "vote_reference": None,
            "media_coverage": [],
            "public_response": None,
            "source": "Committee Minutes"
        },
        {
            "id": "3",
            "bill_id": str(bill_id),
            "bill_title": bill.name_en,
            "mention_date": "2025-01-05",
            "mention_type": "vote",
            "context": "Vote on second reading",
            "speaker_name": "Speaker of the House",
            "speaker_party": "Independent",
            "speaker_constituency": "N/A",
            "debate_url": None,
            "transcript_excerpt": f"The question is on the motion for second reading of {bill.name_en}...",
            "committee_reference": None,
            "vote_reference": f"Vote {bill.number}-2025-01-05",
            "media_coverage": [],
            "public_response": None,
            "source": "House of Commons Votes"
        }
    ]
    
    # Apply pagination
    total = len(mock_mentions)
    offset = (page - 1) * page_size
    paginated_mentions = mock_mentions[offset:offset + page_size]
    
    return {
        "results": paginated_mentions,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page * page_size < total,
            "has_prev": page > 1
        },
        "bill_info": {
            "id": str(bill.id),
            "bill_number": bill.number,
            "title": bill.name_en,
            "short_title": bill.short_title_en,
            "status": bill.status_code,
            "introduced_date": bill.introduced
        }
    }


@router.get("/debates/mentions")
async def get_debate_mentions(
    q: Optional[str] = Query(None, description="Search query for debate content"),
    politician: Optional[str] = Query(None, description="Politician filter"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    mention_type: Optional[str] = Query(None, description="Type of mention (bill, motion, question)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    Get debate mentions with advanced filtering.
    Searches through parliamentary debate transcripts for specific content.
    """
    # For now, create mock debate mention data
    # In a full implementation, this would search through actual debate transcripts
    mock_debate_mentions = [
        {
            "id": "1",
            "debate_date": "2025-01-15",
            "debate_session": "44-1",
            "debate_type": "Question Period",
            "mention_type": "bill",
            "mention_content": "Bill C-123 on environmental protection",
            "speaker_name": "Hon. Member Johnson",
            "speaker_party": "Green",
            "speaker_constituency": "Vancouver Island",
            "transcript_excerpt": "The honourable member asks about the government's commitment to Bill C-123...",
            "related_bill": "C-123",
            "related_motion": None,
            "related_question": "Q-123",
            "debate_url": "/debates/2025-01-15/question-period",
            "media_coverage": ["CBC News", "Global News"],
            "public_response": "Positive social media engagement",
            "source": "House of Commons Hansard"
        },
        {
            "id": "2",
            "debate_date": "2025-01-14",
            "debate_session": "44-1",
            "debate_type": "Government Orders",
            "mention_type": "motion",
            "mention_content": "Motion to extend sitting hours",
            "speaker_name": "Hon. Member Davis",
            "speaker_party": "Liberal",
            "speaker_constituency": "Ottawa Centre",
            "transcript_excerpt": "I move that the House extend its sitting hours to complete consideration of...",
            "related_bill": None,
            "related_motion": "M-456",
            "related_question": None,
            "debate_url": "/debates/2025-01-14/government-orders",
            "media_coverage": ["CTV News"],
            "public_response": "Mixed parliamentary response",
            "source": "House of Commons Hansard"
        },
        {
            "id": "3",
            "debate_date": "2025-01-13",
            "debate_session": "44-1",
            "debate_type": "Statements by Members",
            "mention_type": "constituency",
            "mention_content": "Local infrastructure project",
            "speaker_name": "Hon. Member Wilson",
            "speaker_party": "Conservative",
            "speaker_constituency": "Calgary Southwest",
            "transcript_excerpt": "I rise today to highlight an important infrastructure project in my riding...",
            "related_bill": None,
            "related_motion": None,
            "related_question": None,
            "debate_url": "/debates/2025-01-13/statements",
            "media_coverage": ["Calgary Herald"],
            "public_response": "Local media coverage",
            "source": "House of Commons Hansard"
        }
    ]
    
    # Apply filters
    filtered_mentions = mock_debate_mentions
    
    if q:
        filtered_mentions = [
            mention for mention in filtered_mentions
            if q.lower() in mention["mention_content"].lower() or 
               q.lower() in mention["transcript_excerpt"].lower()
        ]
    
    if politician:
        filtered_mentions = [
            mention for mention in filtered_mentions
            if politician.lower() in mention["speaker_name"].lower()
        ]
    
    if mention_type:
        filtered_mentions = [
            mention for mention in filtered_mentions
            if mention["mention_type"] == mention_type
        ]
    
    # Apply pagination
    total = len(filtered_mentions)
    offset = (page - 1) * page_size
    paginated_mentions = filtered_mentions[offset:offset + page_size]
    
    return {
        "results": paginated_mentions,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page * page_size < total,
            "has_prev": page > 1
        },
        "filters_applied": {
            "search_query": q,
            "politician": politician,
            "mention_type": mention_type,
            "date_range": f"{date_from} to {date_to}" if date_from and date_to else None
        }
    }


@router.get("/committees/mentions")
async def get_committee_mentions(
    committee_id: Optional[str] = Query(None, description="Committee identifier"),
    committee_name: Optional[str] = Query(None, description="Committee name search"),
    topic: Optional[str] = Query(None, description="Topic or subject matter"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    Get committee mentions and activity.
    Tracks committee work, studies, and recommendations.
    """
    # For now, create mock committee mention data
    # In a full implementation, this would come from committee minutes and reports
    mock_committee_mentions = [
        {
            "id": "1",
            "committee_name": "Standing Committee on Finance",
            "committee_id": "FINA",
            "activity_date": "2025-01-15",
            "activity_type": "meeting",
            "topic": "Federal Budget 2025",
            "description": "Committee meeting to study the federal budget",
            "participants": [
                {"name": "Hon. Member Smith", "role": "Chair", "party": "Liberal"},
                {"name": "Hon. Member Johnson", "role": "Vice-Chair", "party": "Conservative"},
                {"name": "Hon. Member Davis", "role": "Member", "party": "NDP"}
            ],
            "witnesses": [
                {"name": "Dr. Jane Wilson", "title": "Chief Economist", "organization": "Bank of Canada"},
                {"name": "Mr. Robert Brown", "title": "Director", "organization": "Parliamentary Budget Office"}
            ],
            "recommendations": [
                "Increase funding for green infrastructure",
                "Review tax incentives for small businesses"
            ],
            "related_bills": ["C-123", "C-124"],
            "related_motions": ["M-456"],
            "report_url": "/committees/fina/reports/budget-2025",
            "minutes_url": "/committees/fina/minutes/2025-01-15",
            "media_coverage": ["CBC News", "Financial Post"],
            "public_response": "Positive stakeholder feedback",
            "source": "Committee Minutes"
        },
        {
            "id": "2",
            "committee_name": "Standing Committee on Health",
            "committee_id": "HESA",
            "activity_date": "2025-01-14",
            "activity_type": "study",
            "topic": "Mental Health Services",
            "description": "Study on mental health service delivery across Canada",
            "participants": [
                {"name": "Hon. Member Wilson", "role": "Chair", "party": "Conservative"},
                {"name": "Hon. Member Brown", "role": "Vice-Chair", "party": "Liberal"}
            ],
            "witnesses": [
                {"name": "Dr. Sarah Chen", "title": "Psychiatrist", "organization": "Canadian Psychiatric Association"},
                {"name": "Ms. Lisa Thompson", "title": "Executive Director", "organization": "Mental Health Commission of Canada"}
            ],
            "recommendations": [
                "Increase mental health funding",
                "Improve access to services in rural areas"
            ],
            "related_bills": ["C-125"],
            "related_motions": ["M-457"],
            "report_url": "/committees/hesa/reports/mental-health-2025",
            "minutes_url": "/committees/hesa/minutes/2025-01-14",
            "media_coverage": ["Global News", "Health News"],
            "public_response": "Strong public support",
            "source": "Committee Minutes"
        }
    ]
    
    # Apply filters
    filtered_mentions = mock_committee_mentions
    
    if committee_id:
        filtered_mentions = [
            mention for mention in filtered_mentions
            if mention["committee_id"] == committee_id
        ]
    
    if committee_name:
        filtered_mentions = [
            mention for mention in filtered_mentions
            if committee_name.lower() in mention["committee_name"].lower()
        ]
    
    if topic:
        filtered_mentions = [
            mention for mention in filtered_mentions
            if topic.lower() in mention["topic"].lower() or 
               topic.lower() in mention["description"].lower()
        ]
    
    # Apply pagination
    total = len(filtered_mentions)
    offset = (page - 1) * page_size
    paginated_mentions = filtered_mentions[offset:offset + page_size]
    
    return {
        "results": paginated_mentions,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page * page_size < total,
            "has_prev": page > 1
        },
        "filters_applied": {
            "committee_id": committee_id,
            "committee_name": committee_name,
            "topic": topic,
            "date_range": f"{date_from} to {date_to}" if date_from and date_to else None
        }
    }


@router.get("/votes/detailed")
async def get_detailed_votes(
    vote_id: Optional[str] = Query(None, description="Specific vote ID"),
    bill_id: Optional[str] = Query(None, description="Bill ID for vote analysis"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    result: Optional[str] = Query(None, description="Vote result filter"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    Get detailed voting information including individual MP votes.
    Provides comprehensive analysis of parliamentary votes.
    """
    # For now, create mock detailed vote data
    # In a full implementation, this would come from actual vote records
    mock_detailed_votes = [
        {
            "id": "1",
            "vote_date": "2025-01-15",
            "vote_number": "V-123",
            "bill_id": "123",
            "bill_title": "Environmental Protection Act",
            "vote_description": "Second reading vote on Bill C-123",
            "result": "Passed",
            "total_votes": 338,
            "yes_votes": 245,
            "no_votes": 93,
            "abstentions": 0,
            "absences": 0,
            "turnout_percentage": 100.0,
            "party_breakdown": {
                "Liberal": {"total": 120, "yes": 120, "no": 0, "abstain": 0},
                "Conservative": {"total": 95, "yes": 0, "no": 95, "abstain": 0},
                "NDP": {"total": 45, "yes": 45, "no": 0, "abstain": 0},
                "Bloc Québécois": {"total": 32, "yes": 32, "no": 0, "abstain": 0},
                "Green": {"total": 12, "yes": 12, "no": 0, "abstain": 0},
                "Independent": {"total": 4, "yes": 4, "no": 0, "abstain": 0}
            },
                         "constituency_breakdown": {
                 "Ontario": {"total": 121, "yes": 98, "no": 23},
                 "Quebec": {"total": 78, "yes": 65, "no": 13},
                 "British Columbia": {"total": 42, "yes": 35, "no": 7},
                 "Alberta": {"total": 34, "yes": 8, "no": 26},
                 "Other": {"total": 63, "yes": 39, "no": 24}
             },
            "whip_status": "whipped",
            "government_position": "for",
            "opposition_position": "against",
            "notable_votes": [
                {"mp_name": "Hon. Member Smith", "vote": "Yes", "party": "Liberal", "constituency": "Toronto Centre"},
                {"mp_name": "Hon. Member Johnson", "vote": "No", "party": "Conservative", "constituency": "Calgary Centre"}
            ],
            "vote_analysis": {
                "party_discipline": "High",
                "regional_patterns": "Strong urban-rural divide",
                "swing_votes": 5,
                "rebel_votes": 2,
                "confidence_measure": True
            },
            "related_debates": ["/debates/2025-01-14/bill-c-123"],
            "related_committees": ["Standing Committee on Environment"],
            "media_coverage": ["CBC News", "CTV News", "Global News"],
            "public_response": "Mixed public opinion",
            "source": "House of Commons Votes"
        }
    ]
    
    # Apply filters
    filtered_votes = mock_detailed_votes
    
    if vote_id:
        filtered_votes = [
            vote for vote in filtered_votes
            if vote["id"] == vote_id
        ]
    
    if bill_id:
        filtered_votes = [
            vote for vote in filtered_votes
            if vote["bill_id"] == bill_id
        ]
    
    if result:
        filtered_votes = [
            vote for vote in filtered_votes
            if vote["result"].lower() == result.lower()
        ]
    
    # Apply pagination
    total = len(filtered_votes)
    offset = (page - 1) * page_size
    paginated_votes = filtered_votes[offset:offset + page_size]
    
    return {
        "results": paginated_votes,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": page * page_size < total,
            "has_prev": page > 1
        },
        "filters_applied": {
            "vote_id": vote_id,
            "bill_id": bill_id,
            "result": result,
            "date_range": f"{date_from} to {date_to}" if date_from and date_to else None
        }
    }
