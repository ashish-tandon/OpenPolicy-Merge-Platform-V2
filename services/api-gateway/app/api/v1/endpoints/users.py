from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    is_active: bool
    created_at: str
    updated_at: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    size: int

router = APIRouter()

@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    is_active: Optional[bool] = Query(None, description="Filter by active status")
):
    """List users with pagination and filtering."""
    # Mock data for now
    mock_users = [
        UserResponse(
            id="1",
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
            is_active=True,
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z"
        ),
        UserResponse(
            id="2",
            username="jane_smith",
            email="jane@example.com",
            full_name="Jane Smith",
            is_active=True,
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z"
        )
    ]
    
    if is_active is not None:
        mock_users = [u for u in mock_users if u.is_active == is_active]
    
    return UserListResponse(
        users=mock_users,
        total=len(mock_users),
        page=page,
        size=size
    )

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get a specific user by ID."""
    # Mock data for now
    if user_id == "1":
        return UserResponse(
            id="1",
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
            is_active=True,
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z"
        )
    elif user_id == "2":
        return UserResponse(
            id="2",
            username="jane_smith",
            email="jane@example.com",
            full_name="Jane Smith",
            is_active=True,
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z"
        )
    
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Create a new user."""
    # Mock creation for now
    return UserResponse(
        id="3",
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=True,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z"
    )

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate):
    """Update an existing user."""
    # Mock update for now
    existing_user = UserResponse(
        id=user_id,
        username="existing_user",
        email="existing@example.com",
        full_name=user_update.full_name or "Existing User",
        is_active=user_update.is_active if user_update.is_active is not None else True,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z"
    )
    
    return existing_user

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """Delete a user."""
    # Mock deletion for now
    return {"message": f"User {user_id} deleted successfully"}
