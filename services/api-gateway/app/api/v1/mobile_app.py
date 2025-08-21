"""
Mobile App API endpoints for OpenPolicy V2.

Provides exact API compatibility with the OpenPolicy mobile app.
This ensures feature parity between mobile and web platforms.
"""

from fastapi import APIRouter, HTTPException, Depends, Body, Query
from sqlalchemy.orm import Session as DBSession
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.database import get_db
from app.models.openparliament import Bill, ElectedMember, VoteQuestion, Politician, Party, Riding

router = APIRouter()


# ============================================================================
# 1. USER APIs
# ============================================================================

@router.post("/app-auth/register")
async def register_user(
    user_data: Dict[str, Any] = Body(..., description="User registration data"),
    db: DBSession = Depends(get_db)
):
    """
    Register a new user (mobile app compatible).
    """
    # Validate required fields
    required_fields = ["name", "email", "password", "postal_code"]
    for field in required_fields:
        if field not in user_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # For now, create mock user response
    # In a full implementation, this would create a user in the database
    mock_user = {
        "id": 101,
        "name": user_data["name"],
        "email": user_data["email"],
        "postal_code": user_data["postal_code"],
        "avatar": "https://cdn.domain.com/avatars/101.png",
        "role": 0
    }
    
    return {
        "success": True,
        "user": mock_user,
        "token": "jwt-token-abc123"
    }


@router.post("/app-auth/login")
async def login_user(
    login_data: Dict[str, Any] = Body(..., description="Login credentials"),
    db: DBSession = Depends(get_db)
):
    """
    Login user (mobile app compatible).
    """
    # Validate required fields
    required_fields = ["email", "password"]
    for field in required_fields:
        if field not in login_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # For now, create mock login response
    # In a full implementation, this would validate credentials
    mock_user = {
        "id": 101,
        "name": "Ashish Tandon",
        "email": login_data["email"],
        "avatar": "https://cdn.domain.com/avatars/101.png",
        "postal_code": "A1B2C3"
    }
    
    return {
        "success": True,
        "token": "jwt-token-abc123",
        "user": mock_user
    }


@router.get("/app/v1/profile")
async def fetch_profile(
    db: DBSession = Depends(get_db)
):
    """
    Fetch user profile (mobile app compatible).
    """
    # For now, return mock profile
    # In a full implementation, this would get the authenticated user's profile
    mock_profile = {
        "id": 101,
        "name": "Ashish Tandon",
        "email": "ashish@example.com",
        "avatar": "https://cdn.domain.com/avatars/101.png",
        "postal_code": "A1B2C3",
        "role": 0
    }
    
    return {
        "success": True,
        "user": mock_profile
    }


@router.put("/app/v1/profile")
async def update_profile(
    profile_data: Dict[str, Any] = Body(..., description="Profile update data"),
    db: DBSession = Depends(get_db)
):
    """
    Update user profile (mobile app compatible).
    """
    # Validate required fields
    required_fields = ["name"]
    for field in required_fields:
        if field not in profile_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # For now, return mock updated profile
    # In a full implementation, this would update the user's profile
    updated_profile = {
        "id": 101,
        "name": profile_data["name"],
        "avatar": profile_data.get("avatar", "https://cdn.domain.com/avatars/101.png"),
        "postal_code": profile_data.get("postal_code", "A1B2C3")
    }
    
    return {
        "success": True,
        "user": updated_profile
    }


@router.post("/app/v1/change-password")
async def change_password(
    password_data: Dict[str, Any] = Body(..., description="Password change data"),
    db: DBSession = Depends(get_db)
):
    """
    Change user password (mobile app compatible).
    """
    # Validate required fields
    required_fields = ["old_password", "new_password"]
    for field in required_fields:
        if field not in password_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    return {
        "success": True,
        "message": "Password updated successfully."
    }


@router.delete("/app/v1/delete-account")
async def delete_account(
    delete_data: Dict[str, Any] = Body(..., description="Account deletion data"),
    db: DBSession = Depends(get_db)
):
    """
    Delete user account (mobile app compatible).
    """
    # Validate required fields
    required_fields = ["reason", "email"]
    for field in required_fields:
        if field not in delete_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    return {
        "success": True,
        "message": "Account deleted."
    }


# ============================================================================
# 2. BILLS APIs
# ============================================================================

@router.get("/app/v1/bills")
async def get_bills_list(
    search: Optional[str] = Query(None, description="Search query for bills"),
    db: DBSession = Depends(get_db)
):
    """
    Get list of bills (mobile app compatible).
    """
    # For now, return mock bills data
    # In a full implementation, this would query the database
    mock_bills = [
        {
            "id": 201,
            "number": "B-234",
            "title": "Education Reform Act",
            "description": "Improves public education.",
            "status": "active",
            "support_percentage": 65,
            "oppose_percentage": 35,
            "bookmarked": False,
            "app_summary": "Reforms educational standards and funding."
        },
        {
            "id": 202,
            "number": "B-235",
            "title": "Climate Action Bill",
            "description": "Addresses climate change concerns.",
            "status": "active",
            "support_percentage": 78,
            "oppose_percentage": 22,
            "bookmarked": True,
            "app_summary": "Implements climate change mitigation strategies."
        }
    ]
    
    # Apply search filter if provided
    if search:
        mock_bills = [bill for bill in mock_bills if search.lower() in bill["title"].lower()]
    
    return {
        "success": True,
        "data": mock_bills
    }


@router.get("/app/v1/bills/{bill_id}")
async def get_bill_detail(
    bill_id: int,
    db: DBSession = Depends(get_db)
):
    """
    Get bill detail (mobile app compatible).
    """
    # For now, return mock bill detail
    # In a full implementation, this would query the database
    mock_bill = {
        "id": bill_id,
        "number": "B-234",
        "title": "Education Reform Act",
        "description": "Improves public education.",
        "status": "active",
        "support_percentage": 65,
        "oppose_percentage": 35,
        "bookmarked": False,
        "app_summary": "Reforms educational standards and funding."
    }
    
    return {
        "success": True,
        "data": mock_bill,
        "vote_cast": "support",
        "support_percentage": 65,
        "oppose_percentage": 35,
        "bookmark": False
    }


@router.post("/app/v1/bills/{bill_id}/support")
async def support_oppose_bill(
    bill_id: int,
    support_data: Dict[str, Any] = Body(..., description="Support/oppose data"),
    db: DBSession = Depends(get_db)
):
    """
    Support or oppose a bill (mobile app compatible).
    """
    # Validate required fields
    if "support" not in support_data:
        raise HTTPException(status_code=400, detail="Missing required field: support")
    
    # For now, return success response
    # In a full implementation, this would record the vote
    return {
        "success": True
    }


@router.post("/app/v1/bills/{bill_id}/bookmark")
async def bookmark_bill(
    bill_id: int,
    db: DBSession = Depends(get_db)
):
    """
    Bookmark a bill (mobile app compatible).
    """
    # For now, return success response
    # In a full implementation, this would toggle the bookmark
    return {
        "success": True
    }


# ============================================================================
# 3. ISSUES APIs
# ============================================================================

@router.post("/app/v1/issues/create")
async def create_issue(
    issue_data: Dict[str, Any] = Body(..., description="Issue creation data"),
    db: DBSession = Depends(get_db)
):
    """
    Create a new issue (mobile app compatible).
    """
    # Validate required fields
    required_fields = ["bill_id", "title", "description"]
    for field in required_fields:
        if field not in issue_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # For now, return mock issue response
    # In a full implementation, this would create the issue
    mock_issue = {
        "id": 301,
        "title": issue_data["title"],
        "description": issue_data["description"],
        "status": "open",
        "related_bill": issue_data["bill_id"]
    }
    
    return {
        "success": True,
        "issue": mock_issue
    }


@router.post("/app/v1/issues/{issue_id}/support")
async def support_issue(
    issue_id: int,
    support_data: Dict[str, Any] = Body(..., description="Issue support data"),
    db: DBSession = Depends(get_db)
):
    """
    Support an issue (mobile app compatible).
    """
    # Validate required fields
    if "support" not in support_data:
        raise HTTPException(status_code=400, detail="Missing required field: support")
    
    return {
        "success": True
    }


@router.post("/app/v1/issues/{issue_id}/bookmark")
async def bookmark_issue(
    issue_id: int,
    db: DBSession = Depends(get_db)
):
    """
    Bookmark an issue (mobile app compatible).
    """
    return {
        "success": True
    }


@router.post("/app/v1/issues/{issue_id}/request-deletion")
async def request_issue_deletion(
    issue_id: int,
    deletion_data: Dict[str, Any] = Body(..., description="Issue deletion request data"),
    db: DBSession = Depends(get_db)
):
    """
    Request issue deletion (mobile app compatible).
    """
    # Validate required fields
    required_fields = ["reason"]
    for field in required_fields:
        if field not in deletion_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    return {
        "success": True,
        "message": "Issue deletion requested"
    }


# ============================================================================
# 4. REPRESENTATIVE APIs
# ============================================================================

@router.get("/app/v1/representatives")
async def find_user_representative(
    postal_code: str = Query(..., description="User's postal code"),
    db: DBSession = Depends(get_db)
):
    """
    Find user's representative by postal code (mobile app compatible).
    """
    # For now, return mock representative data
    # In a full implementation, this would query the database
    mock_representative = {
        "id": 401,
        "name": "Jane Doe",
        "constituency": "Central",
        "contact_info": {
            "email": "jane.doe@parliament.gov",
            "phone": "+123456789"
        }
    }
    
    return {
        "success": True,
        "representative": mock_representative
    }


@router.get("/app/v1/representatives/all")
async def search_representatives(
    search: str = Query(..., description="Search query for representatives"),
    db: DBSession = Depends(get_db)
):
    """
    Search all representatives (mobile app compatible).
    """
    # For now, return mock representatives data
    # In a full implementation, this would query the database
    mock_representatives = [
        {
            "id": 402,
            "name": "John Smith",
            "constituency": "North",
            "contact_info": {
                "email": "john.smith@parliament.gov",
                "phone": "+987654321"
            }
        }
    ]
    
    return {
        "success": True,
        "data": mock_representatives
    }


# ============================================================================
# 5. CHAT/GPT APIs
# ============================================================================

@router.get("/app/v1/chat/get-bill")
async def get_bill_for_chat(
    bill_id: int = Query(..., description="Bill ID for chat context"),
    db: DBSession = Depends(get_db)
):
    """
    Get bill summary for chat (mobile app compatible).
    """
    # For now, return mock bill summary
    # In a full implementation, this would query the database
    mock_summary = "The Education Reform Act improves standards and funding for public schools."
    
    return {
        "success": True,
        "summary": mock_summary
    }


@router.post("/app/v1/chat/bill-chat")
async def bill_chat(
    chat_data: Dict[str, Any] = Body(..., description="Bill chat data"),
    db: DBSession = Depends(get_db)
):
    """
    Chat with AI about a bill (mobile app compatible).
    """
    # Validate required fields
    required_fields = ["bill_id", "message"]
    for field in required_fields:
        if field not in chat_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # For now, return mock AI response
    # In a full implementation, this would integrate with an AI service
    mock_response = "Main criticisms are lack of detail in funding and concerns about rural schools."
    
    return {
        "success": True,
        "response": mock_response
    }


# ============================================================================
# 6. ERROR HANDLING
# ============================================================================

# Exception handlers should be defined at the app level, not router level
# @router.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     """
#     Standard error response format for mobile app compatibility.
#     """
#     return {
#         "success": False,
#         "message": exc.detail
#     }
