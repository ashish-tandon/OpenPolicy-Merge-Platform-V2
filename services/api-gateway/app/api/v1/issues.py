"""
Issues API endpoints for OpenPolicy V2.

Provides user-driven issue creation and management functionality.
This is a critical feature that was missing from the current implementation.
"""

from fastapi import APIRouter, HTTPException, Depends, Body, Query
from sqlalchemy.orm import Session as DBSession
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.database import get_db
from app.models.openparliament import Bill, ElectedMember, VoteQuestion, Politician, Party, Riding

router = APIRouter()


@router.post("/create")
async def create_issue(
    issue_data: Dict[str, Any] = Body(..., description="Issue data"),
    db: DBSession = Depends(get_db)
):
    """
    Create a new user issue.
    Users can report issues that need government attention.
    """
    # Validate required fields
    required_fields = ["name", "summary", "description"]
    for field in required_fields:
        if field not in issue_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # Validate field lengths
    if len(issue_data["name"]) < 3:
        raise HTTPException(status_code=400, detail="Issue name must be at least 3 characters")
    
    if len(issue_data["summary"]) < 10:
        raise HTTPException(status_code=400, detail="Issue summary must be at least 10 characters")
    
    if len(issue_data["description"]) < 20:
        raise HTTPException(status_code=400, detail="Issue description must be at least 20 characters")
    
    # For now, create mock issue response
    # In a full implementation, this would save to the database
    issue_record = {
        "id": f"issue-{datetime.utcnow().timestamp()}",
        "name": issue_data["name"],
        "summary": issue_data["summary"],
        "description": issue_data["description"],
        "category": issue_data.get("category", "general"),
        "priority": issue_data.get("priority", "medium"),
        "status": "pending_approval",
        "user_id": issue_data.get("user_id", "demo-user"),
        "constituency": issue_data.get("constituency"),
        "postal_code": issue_data.get("postal_code"),
        "contact_email": issue_data.get("contact_email"),
        "tags": issue_data.get("tags", []),
        "attachments": issue_data.get("attachments", []),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "metadata": {
            "source": "web",
            "user_agent": issue_data.get("user_agent", "unknown"),
            "ip_address": issue_data.get("ip_address"),
            "location": issue_data.get("location")
        }
    }
    
    return {
        "success": True,
        "message": "Issue created successfully and is pending admin approval",
        "issue": issue_record,
        "next_steps": [
            "Your issue has been submitted for review",
            "An admin will review and approve your issue",
            "You will receive updates on the approval status",
            "Approved issues will be visible to the community"
        ]
    }


@router.get("/user-issues")
async def get_user_issues(
    user_id: str,
    status: Optional[str] = Query(None, description="Filter by issue status"),
    category: Optional[str] = Query(None, description="Filter by issue category"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    Get issues created by a specific user.
    Provides paginated list of user's issues with filtering options.
    """
    # For now, create mock user issues
    # In a full implementation, this would query the database
    mock_issues = generate_mock_user_issues(user_id, status, category, page, page_size)
    
    return {
        "success": True,
        "user_issues": mock_issues["issues"],
        "pagination": mock_issues["pagination"],
        "user_id": user_id,
        "filters": {
            "status": status,
            "category": category
        },
        "summary": {
            "total_issues": mock_issues["pagination"]["total"],
            "pending_approval": 3,
            "approved": 5,
            "rejected": 1,
            "resolved": 2
        }
    }


@router.get("/{issue_id}")
async def get_issue_detail(
    issue_id: str,
    db: DBSession = Depends(get_db)
):
    """
    Get detailed information about a specific issue.
    Provides complete issue details and status information.
    """
    # For now, create mock issue detail
    # In a full implementation, this would query the database
    issue_detail = generate_mock_issue_detail(issue_id)
    
    if not issue_detail:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    return {
        "success": True,
        "issue": issue_detail
    }


@router.put("/{issue_id}/update")
async def update_issue(
    issue_id: str,
    update_data: Dict[str, Any] = Body(..., description="Update data"),
    db: DBSession = Depends(get_db)
):
    """
    Update an existing issue.
    Users can modify their issues before approval.
    """
    # Validate updateable fields
    allowed_fields = ["name", "summary", "description", "category", "priority", "tags"]
    invalid_fields = [field for field in update_data.keys() if field not in allowed_fields]
    
    if invalid_fields:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid fields for update: {', '.join(invalid_fields)}"
        )
    
    # For now, create mock update response
    # In a full implementation, this would update the database
    updated_issue = {
        "id": issue_id,
        "name": update_data.get("name", "Updated Issue Name"),
        "summary": update_data.get("summary", "Updated issue summary"),
        "description": update_data.get("description", "Updated issue description"),
        "category": update_data.get("category", "general"),
        "priority": update_data.get("priority", "medium"),
        "status": "pending_approval",
        "updated_at": datetime.utcnow().isoformat(),
        "update_history": [
            {
                "timestamp": datetime.utcnow().isoformat(),
                "action": "user_update",
                "changes": list(update_data.keys())
            }
        ]
    }
    
    return {
        "success": True,
        "message": "Issue updated successfully",
        "issue": updated_issue
    }


@router.delete("/{issue_id}")
async def delete_issue(
    issue_id: str,
    user_id: str = Query(..., description="User ID for verification"),
    db: DBSession = Depends(get_db)
):
    """
    Delete an issue.
    Users can delete their issues if they haven't been approved yet.
    """
    # For now, create mock delete response
    # In a full implementation, this would delete from the database
    return {
        "success": True,
        "message": "Issue deleted successfully",
        "deleted_issue_id": issue_id,
        "deleted_at": datetime.utcnow().isoformat()
    }


@router.get("/community/issues")
async def get_community_issues(
    status: Optional[str] = Query(None, description="Filter by issue status"),
    category: Optional[str] = Query(None, description="Filter by issue category"),
    constituency: Optional[str] = Query(None, description="Filter by constituency"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    Get community issues for public viewing.
    Provides approved issues that are visible to all users.
    """
    # For now, create mock community issues
    # In a full implementation, this would query the database
    community_issues = generate_mock_community_issues(status, category, constituency, priority, page, page_size)
    
    return {
        "success": True,
        "community_issues": community_issues["issues"],
        "pagination": community_issues["pagination"],
        "filters": {
            "status": status,
            "category": category,
            "constituency": constituency,
            "priority": priority
        },
        "summary": {
            "total_community_issues": community_issues["pagination"]["total"],
            "by_category": {
                "environmental": 15,
                "economic": 23,
                "social": 18,
                "infrastructure": 12,
                "healthcare": 20
            },
            "by_priority": {
                "high": 25,
                "medium": 45,
                "low": 18
            }
        }
    }


@router.post("/{issue_id}/support")
async def support_issue(
    issue_id: str,
    support_data: Dict[str, Any] = Body(..., description="Support data"),
    db: DBSession = Depends(get_db)
):
    """
    Support an issue.
    Users can show support for community issues.
    """
    # Validate required fields
    if "user_id" not in support_data:
        raise HTTPException(status_code=400, detail="Missing user_id")
    
    # For now, create mock support response
    # In a full implementation, this would save to the database
    support_record = {
        "id": f"support-{datetime.utcnow().timestamp()}",
        "issue_id": issue_id,
        "user_id": support_data["user_id"],
        "support_type": support_data.get("support_type", "general"),
        "comment": support_data.get("comment"),
        "constituency": support_data.get("constituency"),
        "created_at": datetime.utcnow().isoformat()
    }
    
    return {
        "success": True,
        "message": "Issue supported successfully",
        "support": support_record,
        "total_supporters": 42  # Mock total
    }


@router.get("/{issue_id}/supporters")
async def get_issue_supporters(
    issue_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: DBSession = Depends(get_db)
):
    """
    Get list of supporters for an issue.
    Shows who supports a particular community issue.
    """
    # For now, create mock supporters list
    # In a full implementation, this would query the database
    supporters = generate_mock_issue_supporters(issue_id, page, page_size)
    
    return {
        "success": True,
        "supporters": supporters["supporters"],
        "pagination": supporters["pagination"],
        "issue_id": issue_id,
        "total_supporters": supporters["pagination"]["total"]
    }


# Helper functions for generating mock data

def generate_mock_user_issues(user_id: str, status: Optional[str], category: Optional[str], page: int, page_size: int) -> Dict[str, Any]:
    """Generate mock user issues for demonstration."""
    issues = []
    
    for i in range(min(page_size, 5)):  # Mock 5 issues per page
        issue = {
            "id": f"issue-{page}-{i}",
            "name": f"Sample Issue {i+1}",
            "summary": f"This is a sample issue summary {i+1}",
            "description": f"This is a detailed description of sample issue {i+1}",
            "category": "environmental" if i % 3 == 0 else "economic" if i % 3 == 1 else "social",
            "priority": "high" if i % 4 == 0 else "medium" if i % 4 == 1 else "low",
            "status": "pending_approval" if i % 3 == 0 else "approved" if i % 3 == 1 else "resolved",
            "user_id": user_id,
            "constituency": "Sample Constituency",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        issues.append(issue)
    
    return {
        "issues": issues,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": 25,  # Mock total
            "total_pages": 5,
            "has_next": page < 5,
            "has_prev": page > 1
        }
    }


def generate_mock_issue_detail(issue_id: str) -> Optional[Dict[str, Any]]:
    """Generate mock issue detail for demonstration."""
    return {
        "id": issue_id,
        "name": "Sample Community Issue",
        "summary": "This is a sample community issue that demonstrates the issue management system.",
        "description": "This is a detailed description of the sample community issue. It includes information about the problem, its impact, and potential solutions.",
        "category": "environmental",
        "priority": "high",
        "status": "approved",
        "user_id": "demo-user-123",
        "constituency": "Sample Constituency",
        "postal_code": "M5V 3A8",
        "contact_email": "user@example.com",
        "tags": ["environment", "community", "policy"],
        "attachments": [],
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "supporters_count": 42,
        "comments_count": 8,
        "admin_notes": "This issue has been reviewed and approved for community visibility.",
        "resolution_status": "under_review",
        "government_response": None,
        "related_bills": [],
        "related_issues": []
    }


def generate_mock_community_issues(status: Optional[str], category: Optional[str], constituency: Optional[str], priority: Optional[str], page: int, page_size: int) -> Dict[str, Any]:
    """Generate mock community issues for demonstration."""
    issues = []
    
    for i in range(min(page_size, 5)):  # Mock 5 issues per page
        issue = {
            "id": f"community-issue-{page}-{i}",
            "name": f"Community Issue {i+1}",
            "summary": f"This is a community issue summary {i+1}",
            "description": f"This is a detailed description of community issue {i+1}",
            "category": "environmental" if i % 3 == 0 else "economic" if i % 3 == 1 else "social",
            "priority": "high" if i % 4 == 0 else "medium" if i % 4 == 1 else "low",
            "status": "approved",
            "user_id": f"user-{i+1}",
            "constituency": f"Constituency {i+1}",
            "created_at": datetime.utcnow().isoformat(),
            "supporters_count": 20 + i * 5,
            "comments_count": 3 + i * 2
        }
        issues.append(issue)
    
    return {
        "issues": issues,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": 88,  # Mock total
            "total_pages": 18,
            "has_next": page < 18,
            "has_prev": page > 1
        }
    }


def generate_mock_issue_supporters(issue_id: str, page: int, page_size: int) -> Dict[str, Any]:
    """Generate mock issue supporters for demonstration."""
    supporters = []
    
    for i in range(min(page_size, 5)):  # Mock 5 supporters per page
        supporter = {
            "id": f"supporter-{page}-{i}",
            "user_id": f"user-{i+1}",
            "username": f"User{i+1}",
            "constituency": f"Constituency {i+1}",
            "support_type": "general",
            "comment": f"Support comment {i+1}" if i % 2 == 0 else None,
            "created_at": datetime.utcnow().isoformat()
        }
        supporters.append(supporter)
    
    return {
        "supporters": supporters,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": 42,  # Mock total
            "total_pages": 9,
            "has_next": page < 9,
            "has_prev": page > 1
        }
    }
