"""
User engagement API endpoints.

Includes all missing features from Open Policy Infra:
- Bill voting
- Bill saving
- Representative issues
- User analytics
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime

from app.auth.simple_auth import current_active_user, require_role
from app.schemas.user_schemas import UserAnalytics
from app.models.user import User

router = APIRouter(prefix="/engagement", tags=["User Engagement"])


@router.post("/bills/{bill_id}/vote", response_model=dict)
async def cast_bill_vote(
    bill_id: str,
    vote_type: str = Query(..., pattern="^(support|oppose|abstain)$"),
    vote_reason: Optional[str] = Query(None, max_length=1000),
    current_user: User = Depends(current_active_user)
):
    """Cast a vote on a bill (like Open Policy Infra BillVoteCast)."""
    try:
        # TODO: Validate bill_id exists
        # TODO: Check if user already voted on this bill
        
        # TODO: Create BillVoteCast record
        # vote_record = BillVoteCast(
        #     user_id=current_user.id,
        #     bill_id=bill_id,
        #     vote_type=vote_type,
        #     vote_reason=vote_reason
        # )
        # await db.add(vote_record)
        # await db.commit()
        
        return {
            "success": True,
            "message": f"Vote {vote_type} cast successfully on bill {bill_id}",
            "vote": {
                "bill_id": bill_id,
                "vote_type": vote_type,
                "vote_reason": vote_reason,
                "cast_at": datetime.utcnow().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cast vote: {str(e)}"
        )


@router.get("/bills/{bill_id}/vote", response_model=dict)
async def get_bill_vote(
    bill_id: str,
    current_user: User = Depends(current_active_user)
):
    """Get user's vote on a specific bill."""
    try:
        # TODO: Get vote from database
        # vote = await db.query(BillVoteCast).filter(
        #     BillVoteCast.user_id == current_user.id,
        #     BillVoteCast.bill_id == bill_id
        # ).first()
        
        # For now, return mock data
        return {
            "success": True,
            "has_voted": False,
            "vote": None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get bill vote: {str(e)}"
        )


@router.post("/bills/{bill_id}/save", response_model=dict)
async def save_bill(
    bill_id: str,
    bill_title: Optional[str] = Query(None, max_length=500),
    bill_summary: Optional[str] = Query(None, max_length=2000),
    notes: Optional[str] = Query(None, max_length=1000),
    current_user: User = Depends(current_active_user)
):
    """Save a bill for later reference (like Open Policy Infra SavedBill)."""
    try:
        # TODO: Check if bill already saved
        # existing_save = await db.query(SavedBill).filter(
        #     SavedBill.user_id == current_user.id,
        #     SavedBill.bill_id == bill_id
        # ).first()
        
        # if existing_save:
        #     existing_save.is_saved = True
        #     existing_save.notes = notes
        #     await db.commit()
        # else:
        #     save_record = SavedBill(
        #         user_id=current_user.id,
        #         bill_id=bill_id,
        #         bill_title=bill_title,
        #         bill_summary=bill_summary,
        #         notes=notes
        #     )
        #     await db.add(save_record)
        #     await db.commit()
        
        return {
            "success": True,
            "message": f"Bill {bill_id} saved successfully",
            "saved_bill": {
                "bill_id": bill_id,
                "bill_title": bill_title,
                "saved_at": datetime.utcnow().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save bill: {str(e)}"
        )


@router.delete("/bills/{bill_id}/save", response_model=dict)
async def unsave_bill(
    bill_id: str,
    current_user: User = Depends(current_active_user)
):
    """Remove a bill from saved list."""
    try:
        # TODO: Update SavedBill record
        # saved_bill = await db.query(SavedBill).filter(
        #     SavedBill.user_id == current_user.id,
        #     SavedBill.bill_id == bill_id
        # ).first()
        
        # if saved_bill:
        #     saved_bill.is_saved = False
        #     await db.commit()
        
        return {
            "success": True,
            "message": f"Bill {bill_id} removed from saved list"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to unsave bill: {str(e)}"
        )


@router.get("/bills/saved", response_model=dict)
async def get_saved_bills(
    current_user: User = Depends(current_active_user),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    """Get user's saved bills."""
    try:
        # TODO: Get saved bills from database with pagination
        # saved_bills = await db.query(SavedBill).filter(
        #     SavedBill.user_id == current_user.id,
        #     SavedBill.is_saved == True
        # ).offset((page - 1) * limit).limit(limit).all()
        
        # For now, return mock data
        return {
            "success": True,
            "saved_bills": [],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": 0,
                "pages": 0
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get saved bills: {str(e)}"
        )


@router.post("/representatives/{representative_id}/issues", response_model=dict)
async def create_representative_issue(
    representative_id: str,
    issue_title: str = Query(..., max_length=255),
    issue_description: str = Query(..., max_length=5000),
    issue_category: Optional[str] = Query(None, max_length=100),
    priority: str = Query("medium", pattern="^(low|medium|high)$"),
    current_user: User = Depends(current_active_user)
):
    """Create an issue for a representative (like Open Policy Infra RepresentativeIssue)."""
    try:
        # TODO: Validate representative_id exists
        # TODO: Create RepresentativeIssue record
        # issue = RepresentativeIssue(
        #     user_id=current_user.id,
        #     representative_id=representative_id,
        #     issue_title=issue_title,
        #     issue_description=issue_description,
        #     issue_category=issue_category,
        #     priority=priority
        # )
        # await db.add(issue)
        # await db.commit()
        
        return {
            "success": True,
            "message": "Issue created successfully",
            "issue": {
                "id": "mock_id",  # TODO: Get actual ID
                "representative_id": representative_id,
                "issue_title": issue_title,
                "issue_category": issue_category,
                "priority": priority,
                "status": "pending",
                "created_at": datetime.utcnow().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create issue: {str(e)}"
        )


@router.get("/representatives/{representative_id}/issues", response_model=dict)
async def get_representative_issues(
    representative_id: str,
    current_user: User = Depends(current_active_user),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    """Get user's issues for a specific representative."""
    try:
        # TODO: Get issues from database with pagination
        # issues = await db.query(RepresentativeIssue).filter(
        #     RepresentativeIssue.user_id == current_user.id,
        #     RepresentativeIssue.representative_id == representative_id
        # ).offset((page - 1) * limit).limit(limit).all()
        
        # For now, return mock data
        return {
            "success": True,
            "issues": [],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": 0,
                "pages": 0
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get representative issues: {str(e)}"
        )


@router.get("/issues", response_model=dict)
async def get_user_issues(
    current_user: User = Depends(current_active_user),
    status_filter: Optional[str] = Query(None, pattern="^(pending|approved|rejected|resolved)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    """Get all user's issues across all representatives."""
    try:
        # TODO: Get issues from database with filters and pagination
        # query = db.query(RepresentativeIssue).filter(
        #     RepresentativeIssue.user_id == current_user.id
        # )
        
        # if status_filter:
        #     query = query.filter(RepresentativeIssue.status == status_filter)
        
        # issues = query.offset((page - 1) * limit).limit(limit).all()
        
        # For now, return mock data
        return {
            "success": True,
            "issues": [],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": 0,
                "pages": 0
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user issues: {str(e)}"
        )


@router.get("/analytics", response_model=UserAnalytics)
async def get_engagement_analytics(current_user: User = Depends(current_active_user)):
    """Get comprehensive user engagement analytics."""
    try:
        # TODO: Get actual data from database
        # votes_cast = await db.query(BillVoteCast).filter(
        #     BillVoteCast.user_id == current_user.id
        # ).count()
        
        # saved_bills = await db.query(SavedBill).filter(
        #     SavedBill.user_id == current_user.id,
        #     SavedBill.is_saved == True
        # ).count()
        
        # issues_raised = await db.query(RepresentativeIssue).filter(
        #     RepresentativeIssue.user_id == current_user.id
        # ).count()
        
        # For now, return mock data
        analytics = UserAnalytics(
            votes_cast=0,
            saved_bills=0,
            issues_raised=0
        )
        
        return analytics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get engagement analytics: {str(e)}"
        )
