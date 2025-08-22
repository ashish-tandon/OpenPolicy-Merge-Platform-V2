"""
Data Visualizations API for OpenPolicy V2

Comprehensive data visualization and dashboard system for enhanced user insights.
Implements P2 priority feature for enhanced user engagement and data understanding.
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Path, Body
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_, or_, desc, func
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import math
import hashlib
import json

from app.database import get_db
from app.models.data_visualizations import (
    VisualizationType, DataVisualization, Dashboard, DashboardVisualization,
    VisualizationCache, VisualizationAnalytics
)
from app.models.users import User
from app.schemas.data_visualizations import (
    VisualizationTypeResponse, DataVisualizationResponse, DashboardResponse,
    DashboardVisualizationResponse,
    VisualizationTypeListResponse, DataVisualizationListResponse, DashboardListResponse,
    VisualizationTypeCreateRequest, VisualizationTypeUpdateRequest,
    DataVisualizationCreateRequest, DataVisualizationUpdateRequest,
    DashboardCreateRequest, DashboardUpdateRequest,
    DashboardVisualizationCreateRequest, DashboardVisualizationUpdateRequest,
    VisualizationDataRequest, VisualizationStatistics,
    DataSourceEnum, ThemeEnum
)
from app.api.v1.auth import get_current_user
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter()


# ============================================================================
# VISUALIZATION TYPE MANAGEMENT
# ============================================================================

@router.post("/types", response_model=VisualizationTypeResponse)
async def create_visualization_type(
    type_data: VisualizationTypeCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new visualization type.
    
    This creates a new visualization type configuration for the system.
    """
    # Check if type name already exists
    existing_type = db.query(VisualizationType).filter(
        VisualizationType.type_name == type_data.type_name
    ).first()
    
    if existing_type:
        raise HTTPException(
            status_code=400,
            detail=f"Visualization type with name '{type_data.type_name}' already exists"
        )
    
    # Create new visualization type
    viz_type = VisualizationType(**type_data.dict())
    db.add(viz_type)
    db.commit()
    db.refresh(viz_type)
    
    logger.info(f"Visualization type created: {current_user.username} - {type_data.type_name}")
    
    return VisualizationTypeResponse(
        id=str(viz_type.id),
        type_name=viz_type.type_name,
        display_name=viz_type.display_name,
        description=viz_type.description,
        category=viz_type.category,
        is_active=viz_type.is_active,
        supported_data_types=viz_type.supported_data_types,
        configuration_schema=viz_type.configuration_schema,
        default_options=viz_type.default_options,
        created_at=viz_type.created_at,
        updated_at=viz_type.updated_at
    )


@router.get("/types", response_model=VisualizationTypeListResponse)
async def list_visualization_types(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search in type names and descriptions"),
    db: DBSession = Depends(get_db)
):
    """
    List visualization types with filtering and pagination.
    """
    # Build base query
    query = db.query(VisualizationType)
    
    # Apply filters
    if category:
        query = query.filter(VisualizationType.category == category)
    
    if is_active is not None:
        query = query.filter(VisualizationType.is_active == is_active)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                VisualizationType.type_name.ilike(search_term),
                VisualizationType.display_name.ilike(search_term),
                VisualizationType.description.ilike(search_term)
            )
        )
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get types
    types = query.order_by(VisualizationType.type_name).offset(offset).limit(page_size).all()
    
    # Convert to response format
    type_responses = []
    for viz_type in types:
        type_responses.append(VisualizationTypeResponse(
            id=str(viz_type.id),
            type_name=viz_type.type_name,
            display_name=viz_type.display_name,
            description=viz_type.description,
            category=viz_type.category,
            is_active=viz_type.is_active,
            supported_data_types=viz_type.supported_data_types,
            configuration_schema=viz_type.configuration_schema,
            default_options=viz_type.default_options,
            created_at=viz_type.created_at,
            updated_at=viz_type.updated_at
        ))
    
    return VisualizationTypeListResponse(
        types=type_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


@router.get("/types/{type_id}", response_model=VisualizationTypeResponse)
async def get_visualization_type(
    type_id: str = Path(..., description="Visualization type ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific visualization type by ID.
    """
    viz_type = db.query(VisualizationType).filter(VisualizationType.id == type_id).first()
    
    if not viz_type:
        raise HTTPException(status_code=404, detail="Visualization type not found")
    
    return VisualizationTypeResponse(
        id=str(viz_type.id),
        type_name=viz_type.type_name,
        display_name=viz_type.display_name,
        description=viz_type.description,
        category=viz_type.category,
        is_active=viz_type.is_active,
        supported_data_types=viz_type.supported_data_types,
        configuration_schema=viz_type.configuration_schema,
        default_options=viz_type.default_options,
        created_at=viz_type.created_at,
        updated_at=viz_type.updated_at
    )


# ============================================================================
# DATA VISUALIZATION MANAGEMENT
# ============================================================================

@router.post("/visualizations", response_model=DataVisualizationResponse)
async def create_data_visualization(
    viz_data: DataVisualizationCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new data visualization.
    """
    # Verify visualization type exists
    viz_type = db.query(VisualizationType).filter(
        VisualizationType.id == viz_data.visualization_type_id
    ).first()
    
    if not viz_type:
        raise HTTPException(status_code=404, detail="Visualization type not found")
    
    # Create new visualization
    visualization = DataVisualization(**viz_data.dict())
    visualization.created_by = current_user.username
    db.add(visualization)
    db.commit()
    db.refresh(visualization)
    
    logger.info(f"Data visualization created: {current_user.username} - {viz_data.title}")
    
    return DataVisualizationResponse(
        id=str(visualization.id),
        title=visualization.title,
        description=visualization.description,
        visualization_type_id=str(visualization.visualization_type_id),
        data_source=visualization.data_source,
        data_query=visualization.data_query,
        configuration=visualization.configuration,
        is_public=visualization.is_public,
        is_featured=visualization.is_featured,
        created_by=visualization.created_by,
        tags=visualization.tags,
        view_count=visualization.view_count,
        last_generated=visualization.last_generated,
        generation_time_ms=visualization.generation_time_ms,
        cache_key=visualization.cache_key,
        cache_expires=visualization.cache_expires,
        created_at=visualization.created_at,
        updated_at=visualization.updated_at
    )


@router.get("/visualizations", response_model=DataVisualizationListResponse)
async def list_data_visualizations(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    visualization_type_id: Optional[str] = Query(None, description="Filter by visualization type ID"),
    data_source: Optional[DataSourceEnum] = Query(None, description="Filter by data source"),
    is_public: Optional[bool] = Query(None, description="Filter by public status"),
    is_featured: Optional[bool] = Query(None, description="Filter by featured status"),
    created_by: Optional[str] = Query(None, description="Filter by creator"),
    search: Optional[str] = Query(None, description="Search in titles and descriptions"),
    db: DBSession = Depends(get_db)
):
    """
    List data visualizations with filtering and pagination.
    """
    # Build base query
    query = db.query(DataVisualization)
    
    # Apply filters
    if visualization_type_id:
        query = query.filter(DataVisualization.visualization_type_id == visualization_type_id)
    
    if data_source:
        query = query.filter(DataVisualization.data_source == data_source)
    
    if is_public is not None:
        query = query.filter(DataVisualization.is_public == is_public)
    
    if is_featured is not None:
        query = query.filter(DataVisualization.is_featured == is_featured)
    
    if created_by:
        query = query.filter(DataVisualization.created_by == created_by)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                DataVisualization.title.ilike(search_term),
                DataVisualization.description.ilike(search_term)
            )
        )
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get visualizations
    visualizations = query.order_by(desc(DataVisualization.created_at)).offset(offset).limit(page_size).all()
    
    # Convert to response format
    viz_responses = []
    for visualization in visualizations:
        viz_responses.append(DataVisualizationResponse(
            id=str(visualization.id),
            title=visualization.title,
            description=visualization.description,
            visualization_type_id=str(visualization.visualization_type_id),
            data_source=visualization.data_source,
            data_query=visualization.data_query,
            configuration=visualization.configuration,
            is_public=visualization.is_public,
            is_featured=visualization.is_featured,
            created_by=visualization.created_by,
            tags=visualization.tags,
            view_count=visualization.view_count,
            last_generated=visualization.last_generated,
            generation_time_ms=visualization.generation_time_ms,
            cache_key=visualization.cache_key,
            cache_expires=visualization.cache_expires,
            created_at=visualization.created_at,
            updated_at=visualization.updated_at
        ))
    
    return DataVisualizationListResponse(
        visualizations=viz_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


@router.get("/visualizations/{visualization_id}", response_model=DataVisualizationResponse)
async def get_data_visualization(
    visualization_id: str = Path(..., description="Visualization ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific data visualization by ID.
    """
    visualization = db.query(DataVisualization).filter(
        DataVisualization.id == visualization_id
    ).first()
    
    if not visualization:
        raise HTTPException(status_code=404, detail="Data visualization not found")
    
    # Increment view count
    visualization.view_count += 1
    db.commit()
    
    return DataVisualizationResponse(
        id=str(visualization.id),
        title=visualization.title,
        description=visualization.description,
        visualization_type_id=str(visualization.visualization_type_id),
        data_source=visualization.data_source,
        data_query=visualization.data_query,
        configuration=visualization.configuration,
        is_public=visualization.is_public,
        is_featured=visualization.is_featured,
        created_by=visualization.created_by,
        tags=visualization.tags,
        view_count=visualization.view_count,
        last_generated=visualization.last_generated,
        generation_time_ms=visualization.generation_time_ms,
        cache_key=visualization.cache_key,
        cache_expires=visualization.cache_expires,
        created_at=visualization.created_at,
        updated_at=visualization.updated_at
    )


# ============================================================================
# DASHBOARD MANAGEMENT
# ============================================================================

@router.post("/dashboards", response_model=DashboardResponse)
async def create_dashboard(
    dashboard_data: DashboardCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new dashboard.
    """
    # Create new dashboard
    dashboard = Dashboard(**dashboard_data.dict())
    dashboard.created_by = current_user.username
    db.add(dashboard)
    db.commit()
    db.refresh(dashboard)
    
    logger.info(f"Dashboard created: {current_user.username} - {dashboard_data.title}")
    
    return DashboardResponse(
        id=str(dashboard.id),
        title=dashboard.title,
        description=dashboard.description,
        layout_config=dashboard.layout_config,
        theme=dashboard.theme,
        is_public=dashboard.is_public,
        is_featured=dashboard.is_featured,
        created_by=dashboard.created_by,
        tags=dashboard.tags,
        refresh_interval=dashboard.refresh_interval,
        view_count=dashboard.view_count,
        last_accessed=dashboard.last_accessed,
        created_at=dashboard.created_at,
        updated_at=dashboard.updated_at
    )


@router.get("/dashboards", response_model=DashboardListResponse)
async def list_dashboards(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    theme: Optional[ThemeEnum] = Query(None, description="Filter by theme"),
    is_public: Optional[bool] = Query(None, description="Filter by public status"),
    is_featured: Optional[bool] = Query(None, description="Filter by featured status"),
    created_by: Optional[str] = Query(None, description="Filter by creator"),
    search: Optional[str] = Query(None, description="Search in titles and descriptions"),
    db: DBSession = Depends(get_db)
):
    """
    List dashboards with filtering and pagination.
    """
    # Build base query
    query = db.query(Dashboard)
    
    # Apply filters
    if theme:
        query = query.filter(Dashboard.theme == theme)
    
    if is_public is not None:
        query = query.filter(Dashboard.is_public == is_public)
    
    if is_featured is not None:
        query = query.filter(Dashboard.is_featured == is_featured)
    
    if created_by:
        query = query.filter(Dashboard.created_by == created_by)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Dashboard.title.ilike(search_term),
                Dashboard.description.ilike(search_term)
            )
        )
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get dashboards
    dashboards = query.order_by(desc(Dashboard.created_at)).offset(offset).limit(page_size).all()
    
    # Convert to response format
    dashboard_responses = []
    for dashboard in dashboards:
        dashboard_responses.append(DashboardResponse(
            id=str(dashboard.id),
            title=dashboard.title,
            description=dashboard.description,
            layout_config=dashboard.layout_config,
            theme=dashboard.theme,
            is_public=dashboard.is_public,
            is_featured=dashboard.is_featured,
            created_by=dashboard.created_by,
            tags=dashboard.tags,
            refresh_interval=dashboard.refresh_interval,
            view_count=dashboard.view_count,
            last_accessed=dashboard.last_accessed,
            created_at=dashboard.created_at,
            updated_at=dashboard.updated_at
        ))
    
    return DashboardListResponse(
        dashboards=dashboard_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


@router.get("/dashboards/{dashboard_id}", response_model=DashboardResponse)
async def get_dashboard(
    dashboard_id: str = Path(..., description="Dashboard ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific dashboard by ID.
    """
    dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
    
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    
    # Update last accessed and view count
    dashboard.last_accessed = datetime.utcnow()
    dashboard.view_count += 1
    db.commit()
    
    return DashboardResponse(
        id=str(dashboard.id),
        title=dashboard.title,
        description=dashboard.description,
        layout_config=dashboard.layout_config,
        theme=dashboard.theme,
        is_public=dashboard.is_public,
        is_featured=dashboard.is_featured,
        created_by=dashboard.created_by,
        tags=dashboard.tags,
        refresh_interval=dashboard.refresh_interval,
        view_count=dashboard.view_count,
        last_accessed=dashboard.last_accessed,
        created_at=dashboard.created_at,
        updated_at=dashboard.updated_at
    )


# ============================================================================
# VISUALIZATION DATA GENERATION
# ============================================================================

@router.post("/visualizations/{visualization_id}/generate")
async def generate_visualization_data(
    visualization_id: str = Path(..., description="Visualization ID"),
    request_data: VisualizationDataRequest = Body(...),
    db: DBSession = Depends(get_db)
):
    """
    Generate data for a specific visualization.
    """
    # Get visualization
    visualization = db.query(DataVisualization).filter(
        DataVisualization.id == visualization_id
    ).first()
    
    if not visualization:
        raise HTTPException(status_code=404, detail="Visualization not found")
    
    # Check cache first
    if not request_data.force_regenerate:
        cached_data = db.query(VisualizationCache).filter(
            and_(
                VisualizationCache.visualization_id == visualization_id,
                VisualizationCache.expires_at > datetime.utcnow()
            )
        ).first()
        
        if cached_data:
            # Update cache hits
            cached_data.hits += 1
            cached_data.last_hit = datetime.utcnow()
            db.commit()
            
            # Track analytics
            _track_visualization_access(db, visualization_id)
            
            return {
                "visualization_id": visualization_id,
                "data": cached_data.generated_data,
                "is_cached": True,
                "cache_key": cached_data.cache_key,
                "expires_at": cached_data.expires_at,
                "generation_time_ms": cached_data.generation_time_ms
            }
    
    # Generate new data
    start_time = datetime.utcnow()
    
    try:
        # Generate visualization data based on type and source
        generated_data = await _generate_visualization_data(
            db, visualization, request_data.custom_filters
        )
        
        generation_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        # Cache the generated data
        data_hash = hashlib.md5(json.dumps(generated_data, sort_keys=True).encode(), usedforsecurity=False).hexdigest()
        config_hash = hashlib.md5(json.dumps(visualization.configuration, sort_keys=True).encode(), usedforsecurity=False).hexdigest()
        cache_key = f"viz_{visualization_id}_{data_hash}_{config_hash}"
        expires_at = datetime.utcnow() + timedelta(hours=1)  # Cache for 1 hour
        
        # Remove old cache entries
        db.query(VisualizationCache).filter(
            VisualizationCache.visualization_id == visualization_id
        ).delete()
        
        # Create new cache entry
        cache_entry = VisualizationCache(
            visualization_id=visualization_id,
            cache_key=cache_key,
            data_hash=data_hash,
            config_hash=config_hash,
            generated_data=generated_data,
            data_size=len(json.dumps(generated_data)),
            generation_time_ms=int(generation_time),
            expires_at=expires_at,
            hits=1,
            last_hit=datetime.utcnow()
        )
        db.add(cache_entry)
        
        # Update visualization metadata
        visualization.last_generated = datetime.utcnow()
        visualization.generation_time_ms = int(generation_time)
        visualization.cache_key = cache_key
        visualization.cache_expires = expires_at
        
        db.commit()
        
        # Track analytics
        _track_visualization_access(db, visualization_id)
        
        logger.info(f"Visualization data generated: {visualization.title} - {generation_time:.2f}ms")
        
        return {
            "visualization_id": visualization_id,
            "data": generated_data,
            "is_cached": False,
            "cache_key": cache_key,
            "expires_at": expires_at,
            "generation_time_ms": int(generation_time)
        }
        
    except Exception as e:
        # Log error
        error_message = str(e)
        logger.error(f"Visualization generation failed: {visualization.title} - {error_message}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate visualization data: {error_message}"
        )


# ============================================================================
# DASHBOARD VISUALIZATION MANAGEMENT
# ============================================================================

@router.post("/dashboards/{dashboard_id}/visualizations", response_model=DashboardVisualizationResponse)
async def add_visualization_to_dashboard(
    dashboard_id: str = Path(..., description="Dashboard ID"),
    viz_data: DashboardVisualizationCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a visualization to a dashboard.
    """
    # Verify dashboard exists
    dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
    if not dashboard:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    
    # Verify visualization exists
    visualization = db.query(DataVisualization).filter(
        DataVisualization.id == viz_data.visualization_id
    ).first()
    
    if not visualization:
        raise HTTPException(status_code=404, detail="Visualization not found")
    
    # Check if visualization is already in dashboard
    existing_viz = db.query(DashboardVisualization).filter(
        and_(
            DashboardVisualization.dashboard_id == dashboard_id,
            DashboardVisualization.visualization_id == viz_data.visualization_id
        )
    ).first()
    
    if existing_viz:
        raise HTTPException(
            status_code=400,
            detail="Visualization is already in this dashboard"
        )
    
    # Create dashboard visualization
    dashboard_viz = DashboardVisualization(**viz_data.dict())
    dashboard_viz.dashboard_id = dashboard_id
    db.add(dashboard_viz)
    db.commit()
    db.refresh(dashboard_viz)
    
    logger.info(f"Visualization added to dashboard: {current_user.username} - {visualization.title}")
    
    return DashboardVisualizationResponse(
        id=str(dashboard_viz.id),
        dashboard_id=str(dashboard_viz.dashboard_id),
        visualization_id=str(dashboard_viz.visualization_id),
        position_x=dashboard_viz.position_x,
        position_y=dashboard_viz.position_y,
        width=dashboard_viz.width,
        height=dashboard_viz.height,
        title_override=dashboard_viz.title_override,
        is_visible=dashboard_viz.is_visible,
        refresh_interval=dashboard_viz.refresh_interval,
        custom_config=dashboard_viz.custom_config,
        created_at=dashboard_viz.created_at,
        updated_at=dashboard_viz.updated_at
    )


# ============================================================================
# STATISTICS AND ANALYTICS
# ============================================================================

@router.get("/statistics")
async def get_visualization_statistics(
    db: DBSession = Depends(get_db)
):
    """
    Get comprehensive visualization statistics.
    """
    # Get all visualizations
    visualizations = db.query(DataVisualization).all()
    
    statistics = []
    for visualization in visualizations:
        # Get analytics data
        analytics = db.query(VisualizationAnalytics).filter(
            VisualizationAnalytics.visualization_id == visualization.id
        ).all()
        
        # Calculate statistics
        total_views = sum([a.daily_views for a in analytics])
        total_generations = sum([a.daily_generations for a in analytics])
        
        # Calculate averages
        avg_generation_time = 0
        if analytics:
            avg_generation_time = sum([a.avg_generation_time for a in analytics]) / len(analytics)
        
        # Time-based views
        last_24h_analytics = [a for a in analytics if a.analytics_date >= datetime.utcnow() - timedelta(hours=24)]
        last_7d_analytics = [a for a in analytics if a.analytics_date >= datetime.utcnow() - timedelta(days=7)]
        
        last_24h_views = sum([a.daily_views for a in last_24h_analytics])
        last_7d_views = sum([a.daily_views for a in last_7d_analytics])
        
        # Cache hit rate (mock for now)
        cache_hit_rate = 75.5
        
        # User engagement (mock for now)
        user_engagement_score = 82.3
        
        statistics.append(VisualizationStatistics(
            visualization_id=str(visualization.id),
            title=visualization.title,
            total_views=total_views,
            total_generations=total_generations,
            avg_generation_time=avg_generation_time,
            cache_hit_rate=cache_hit_rate,
            last_24h_views=last_24h_views,
            last_7d_views=last_7d_views,
            user_engagement_score=user_engagement_score,
            generated_at=datetime.utcnow()
        ))
    
    return {
        "visualizations": statistics,
        "total_visualizations": len(visualizations),
        "generated_at": datetime.utcnow()
    }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

async def _generate_visualization_data(
    db: DBSession, visualization: DataVisualization, custom_filters: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """Generate visualization data based on type and source."""
    
    # This is a simplified implementation - in production, you would have
    # more sophisticated data generation logic based on the visualization type
    # and data source
    
    data_source = visualization.data_source
    viz_type = visualization.visualization_type_id
    
    # Mock data generation based on source
    if data_source == "bills":
        return {
            "labels": ["Introduced", "First Reading", "Second Reading", "Committee", "Third Reading", "Royal Assent"],
            "data": [45, 38, 32, 28, 25, 22],
            "chart_type": "bar",
            "title": "Bill Progress Through Parliament",
            "description": "Number of bills at each legislative stage"
        }
    
    elif data_source == "votes":
        return {
            "labels": ["Government", "Opposition", "Independent"],
            "data": [156, 142, 23],
            "chart_type": "pie",
            "title": "Vote Distribution by Party",
            "description": "Distribution of votes across political parties"
        }
    
    elif data_source == "members":
        return {
            "labels": ["Liberal", "Conservative", "NDP", "Bloc", "Green", "Independent"],
            "data": [158, 119, 25, 32, 2, 1],
            "chart_type": "bar",
            "title": "MP Distribution by Party",
            "description": "Number of Members of Parliament by political party"
        }
    
    else:
        # Generic data structure
        return {
            "labels": ["Category 1", "Category 2", "Category 3", "Category 4", "Category 5"],
            "data": [25, 30, 20, 35, 15],
            "chart_type": "bar",
            "title": "Generic Data Visualization",
            "description": "Sample data for demonstration purposes"
        }


def _track_visualization_access(db: DBSession, visualization_id: str) -> None:
    """Track visualization access for analytics."""
    today = datetime.utcnow().date()
    
    # Get or create analytics record for today
    analytics = db.query(VisualizationAnalytics).filter(
        and_(
            VisualizationAnalytics.visualization_id == visualization_id,
            func.date(VisualizationAnalytics.analytics_date) == today
        )
    ).first()
    
    if not analytics:
        analytics = VisualizationAnalytics(
            visualization_id=visualization_id,
            analytics_date=datetime.utcnow(),
            daily_views=1,
            daily_generations=1
        )
        db.add(analytics)
    else:
        analytics.daily_views += 1
        analytics.daily_generations += 1
    
    db.commit()
