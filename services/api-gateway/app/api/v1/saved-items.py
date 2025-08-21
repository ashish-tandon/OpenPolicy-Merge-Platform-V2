from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.models.saved_items import SavedItem
from app.schemas.saved_items import SavedItemCreate, SavedItemUpdate, SavedItemResponse, SavedItemListResponse

router = APIRouter(prefix="/saved-items", tags=["Saved Items"])

@router.post("/", response_model=SavedItemResponse)
async def add_saved_item(
    item_data: SavedItemCreate,
    db: Session = Depends(get_db)
):
    """Add a new item to user's saved list"""
    try:
        # Check if item already exists
        existing_item = db.query(SavedItem).filter(
            SavedItem.user_id == item_data.user_id,
            SavedItem.item_id == item_data.item_id,
            SavedItem.item_type == item_data.item_type
        ).first()
        
        if existing_item:
            raise HTTPException(status_code=400, detail="Item already saved")
        
        # Create new saved item
        saved_item = SavedItem(
            user_id=item_data.user_id,
            item_id=item_data.item_id,
            item_type=item_data.item_type,
            item_title=item_data.item_title,
            item_url=item_data.item_url,
            saved_at=datetime.utcnow(),
            notes=item_data.notes or "",
            tags=item_data.tags or []
        )
        
        db.add(saved_item)
        db.commit()
        db.refresh(saved_item)
        
        return SavedItemResponse.from_orm(saved_item)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save item: {str(e)}")

@router.get("/user/{user_id}", response_model=SavedItemListResponse)
async def get_user_saved_items(
    user_id: str,
    item_type: Optional[str] = Query(None, description="Filter by item type"),
    search: Optional[str] = Query(None, description="Search in titles, notes, and tags"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get user's saved items with optional filtering"""
    try:
        query = db.query(SavedItem).filter(SavedItem.user_id == user_id)
        
        # Apply filters
        if item_type:
            query = query.filter(SavedItem.item_type == item_type)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (SavedItem.item_title.ilike(search_term)) |
                (SavedItem.notes.ilike(search_term)) |
                (SavedItem.tags.any(lambda tag: search_term in tag))
            )
        
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",")]
            for tag in tag_list:
                query = query.filter(SavedItem.tags.contains([tag]))
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination
        offset = (page - 1) * page_size
        items = query.offset(offset).limit(page_size).all()
        
        # Convert to response models
        results = [SavedItemResponse.from_orm(item) for item in items]
        
        return SavedItemListResponse(
            results=results,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=(total_count + page_size - 1) // page_size
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve saved items: {str(e)}")

@router.get("/{item_id}", response_model=SavedItemResponse)
async def get_saved_item(
    item_id: str,
    user_id: str = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Get a specific saved item"""
    try:
        item = db.query(SavedItem).filter(
            SavedItem.id == item_id,
            SavedItem.user_id == user_id
        ).first()
        
        if not item:
            raise HTTPException(status_code=404, detail="Saved item not found")
        
        return SavedItemResponse.from_orm(item)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve saved item: {str(e)}")

@router.put("/{item_id}", response_model=SavedItemResponse)
async def update_saved_item(
    item_id: str,
    update_data: SavedItemUpdate,
    user_id: str = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Update a saved item (notes, tags)"""
    try:
        item = db.query(SavedItem).filter(
            SavedItem.id == item_id,
            SavedItem.user_id == user_id
        ).first()
        
        if not item:
            raise HTTPException(status_code=404, detail="Saved item not found")
        
        # Update fields
        if update_data.notes is not None:
            item.notes = update_data.notes
        if update_data.tags is not None:
            item.tags = update_data.tags
        
        db.commit()
        db.refresh(item)
        
        return SavedItemResponse.from_orm(item)
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update saved item: {str(e)}")

@router.delete("/{item_id}")
async def remove_saved_item(
    item_id: str,
    user_id: str = Query(..., description="User ID"),
    item_type: str = Query(..., description="Item type for identification"),
    db: Session = Depends(get_db)
):
    """Remove an item from user's saved list"""
    try:
        # Find item by user_id, item_id, and item_type
        item = db.query(SavedItem).filter(
            SavedItem.user_id == user_id,
            SavedItem.item_id == item_id,
            SavedItem.item_type == item_type
        ).first()
        
        if not item:
            raise HTTPException(status_code=404, detail="Saved item not found")
        
        db.delete(item)
        db.commit()
        
        return {"message": "Item removed from saved list successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to remove saved item: {str(e)}")

@router.get("/user/{user_id}/stats")
async def get_user_saved_stats(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get statistics about user's saved items"""
    try:
        # Get total count
        total_count = db.query(SavedItem).filter(SavedItem.user_id == user_id).count()
        
        # Get count by type
        type_counts = {}
        for item_type in ['bill', 'mp', 'debate', 'committee', 'vote']:
            count = db.query(SavedItem).filter(
                SavedItem.user_id == user_id,
                SavedItem.item_type == item_type
            ).count()
            type_counts[item_type] = count
        
        # Get recent activity
        recent_items = db.query(SavedItem).filter(
            SavedItem.user_id == user_id
        ).order_by(SavedItem.saved_at.desc()).limit(5).all()
        
        # Get tag statistics
        all_tags = []
        for item in db.query(SavedItem).filter(SavedItem.user_id == user_id).all():
            all_tags.extend(item.tags or [])
        
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Sort tags by frequency
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_saved_items": total_count,
            "items_by_type": type_counts,
            "recent_items": [
                {
                    "id": item.id,
                    "item_title": item.item_title,
                    "item_type": item.item_type,
                    "saved_at": item.saved_at.isoformat()
                }
                for item in recent_items
            ],
            "top_tags": [{"tag": tag, "count": count} for tag, count in top_tags]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve saved stats: {str(e)}")

@router.post("/user/{user_id}/bulk-actions")
async def bulk_actions(
    user_id: str,
    action: str = Query(..., description="Action to perform: 'add_tags', 'remove_tags', 'update_notes'"),
    item_ids: List[str] = Query(..., description="List of item IDs to update"),
    data: dict = None,
    db: Session = Depends(get_db)
):
    """Perform bulk actions on saved items"""
    try:
        items = db.query(SavedItem).filter(
            SavedItem.id.in_(item_ids),
            SavedItem.user_id == user_id
        ).all()
        
        if not items:
            raise HTTPException(status_code=404, detail="No items found")
        
        updated_count = 0
        
        for item in items:
            if action == "add_tags" and data and "tags" in data:
                new_tags = data["tags"]
                existing_tags = item.tags or []
                item.tags = list(set(existing_tags + new_tags))
                updated_count += 1
                
            elif action == "remove_tags" and data and "tags" in data:
                tags_to_remove = data["tags"]
                existing_tags = item.tags or []
                item.tags = [tag for tag in existing_tags if tag not in tags_to_remove]
                updated_count += 1
                
            elif action == "update_notes" and data and "notes" in data:
                item.notes = data["notes"]
                updated_count += 1
        
        db.commit()
        
        return {
            "message": f"Bulk action '{action}' completed successfully",
            "items_updated": updated_count
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to perform bulk action: {str(e)}")
