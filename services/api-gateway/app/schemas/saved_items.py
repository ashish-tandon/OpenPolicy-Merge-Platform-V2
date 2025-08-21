from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class SavedItemBase(BaseModel):
    user_id: str = Field(..., description="User ID who saved the item")
    item_id: str = Field(..., description="ID of the saved item")
    item_type: str = Field(..., description="Type of saved item (bill, mp, debate, committee, vote)")
    item_title: str = Field(..., description="Title of the saved item")
    item_url: str = Field(..., description="URL of the saved item")
    notes: Optional[str] = Field("", description="User notes about the saved item")
    tags: Optional[List[str]] = Field([], description="User tags for organizing the saved item")

class SavedItemCreate(SavedItemBase):
    """Schema for creating a new saved item"""
    pass

class SavedItemUpdate(BaseModel):
    """Schema for updating a saved item"""
    notes: Optional[str] = Field(None, description="Updated notes")
    tags: Optional[List[str]] = Field(None, description="Updated tags")

class SavedItemResponse(SavedItemBase):
    """Schema for saved item response"""
    id: UUID = Field(..., description="Unique identifier for the saved item")
    saved_at: datetime = Field(..., description="When the item was saved")
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }

class SavedItemListResponse(BaseModel):
    """Schema for paginated list of saved items"""
    results: List[SavedItemResponse] = Field(..., description="List of saved items")
    total_count: int = Field(..., description="Total number of saved items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")

class SavedItemStats(BaseModel):
    """Schema for saved items statistics"""
    total_saved_items: int = Field(..., description="Total number of saved items")
    items_by_type: dict = Field(..., description="Count of items by type")
    recent_items: List[dict] = Field(..., description="Recently saved items")
    top_tags: List[dict] = Field(..., description="Most used tags")

class BulkActionRequest(BaseModel):
    """Schema for bulk actions on saved items"""
    action: str = Field(..., description="Action to perform")
    item_ids: List[str] = Field(..., description="List of item IDs to update")
    data: Optional[dict] = Field(None, description="Data for the action")

class BulkActionResponse(BaseModel):
    """Schema for bulk action response"""
    message: str = Field(..., description="Result message")
    items_updated: int = Field(..., description="Number of items updated")
