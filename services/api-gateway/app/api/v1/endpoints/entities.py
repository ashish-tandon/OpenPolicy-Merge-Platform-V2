"""
Entities endpoints for parliamentary data
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
import time

router = APIRouter()

# Pydantic models
class EntityBase(BaseModel):
    type: str
    data: dict
    metadata: dict = {}
    source: str
    source_id: str
    relationships: List[dict] = []

class EntityCreate(EntityBase):
    pass

class EntityResponse(EntityBase):
    id: str
    created_at: str
    updated_at: str
    version: int

class EntityListResponse(BaseModel):
    entities: List[EntityResponse]
    total: int
    page: int
    size: int

@router.get("/", response_model=EntityListResponse)
async def list_entities(
    type: Optional[str] = Query(None, description="Filter by entity type"),
    source: Optional[str] = Query(None, description="Filter by data source"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size")
):
    """List parliamentary entities with pagination and filtering"""
    # TODO: Implement actual database query
    # For now, return mock data
    mock_entities = [
        {
            "id": "mock-id-1",
            "type": "mp",
            "data": {"name": "John Doe", "party": "Liberal"},
            "metadata": {"source_url": "https://example.com"},
            "source": "openparliament",
            "source_id": "123",
            "relationships": [],
            "created_at": "2025-08-21T00:00:00Z",
            "updated_at": "2025-08-21T00:00:00Z",
            "version": 1
        }
    ]
    
    return EntityListResponse(
        entities=mock_entities,
        total=1,
        page=page,
        size=size
    )

@router.get("/{entity_id}", response_model=EntityResponse)
async def get_entity(entity_id: str):
    """Get a specific entity by ID"""
    # TODO: Implement actual database query
    # For now, return mock data
    if entity_id == "mock-id-1":
        return {
            "id": entity_id,
            "type": "mp",
            "data": {"name": "John Doe", "party": "Liberal"},
            "metadata": {"source_url": "https://example.com"},
            "source": "openparliament",
            "source_id": "123",
            "relationships": [],
            "created_at": "2025-08-21T00:00:00Z",
            "updated_at": "2025-08-21T00:00:00Z",
            "version": 1
        }
    
    raise HTTPException(status_code=404, detail="Entity not found")

@router.post("/", response_model=EntityResponse)
async def create_entity(entity: EntityCreate):
    """Create a new entity"""
    # TODO: Implement actual database creation
    # For now, return mock response
    return {
        "id": "new-entity-id",
        "type": entity.type,
        "data": entity.data,
        "metadata": entity.metadata,
        "source": entity.source,
        "source_id": entity.source_id,
        "relationships": entity.relationships,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": 1
    }

@router.get("/types", response_model=List[str])
async def list_entity_types():
    """List all available entity types"""
    return ["mp", "bill", "vote", "debate", "committee", "session", "jurisdiction"]
