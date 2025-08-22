"""
PWA System API for OpenPolicy V2

Comprehensive Progressive Web App (PWA) system for enhanced mobile accessibility.
Implements P2 priority feature for enhanced mobile accessibility and user experience.
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Path, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_, or_, func
from typing import Optional
from datetime import datetime
import math

from app.database import get_db
from app.models.pwa_system import (
    PWAManifest, ServiceWorker, OfflineResource,
    PWAInstallation, PWAAnalytics
)
from app.models.users import User
from app.schemas.pwa_system import (
    PWAManifestResponse, ServiceWorkerResponse, OfflineResourceResponse,
    PWAManifestListResponse, ServiceWorkerListResponse, OfflineResourceListResponse,
    PWAManifestCreateRequest,
    ServiceWorkerCreateRequest,
    OfflineResourceCreateRequest,
    PWAInstallationTrackingRequest, PWAStatistics,
    DisplayModeEnum, CacheStrategyEnum, ResourceTypeEnum, ResourceCategoryEnum
)
from app.api.v1.auth import get_current_user
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter()


# ============================================================================
# PWA MANIFEST MANAGEMENT
# ============================================================================

@router.post("/manifests", response_model=PWAManifestResponse)
async def create_pwa_manifest(
    manifest_data: PWAManifestCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new PWA manifest.
    
    This creates a new PWA manifest configuration for the system.
    """
    # Check if manifest name already exists
    existing_manifest = db.query(PWAManifest).filter(
        PWAManifest.manifest_name == manifest_data.manifest_name
    ).first()
    
    if existing_manifest:
        raise HTTPException(
            status_code=400,
            detail=f"PWA manifest with name '{manifest_data.manifest_name}' already exists"
        )
    
    # If this is set as default, unset other defaults
    if manifest_data.is_default:
        db.query(PWAManifest).filter(PWAManifest.is_default).update({"is_default": False})
    
    # Create new manifest
    manifest = PWAManifest(**manifest_data.dict())
    manifest.created_by = current_user.username
    db.add(manifest)
    db.commit()
    db.refresh(manifest)
    
    logger.info(f"PWA manifest created: {current_user.username} - {manifest_data.manifest_name}")
    
    return PWAManifestResponse(
        id=str(manifest.id),
        manifest_name=manifest.manifest_name,
        app_name=manifest.app_name,
        short_name=manifest.short_name,
        description=manifest.description,
        start_url=manifest.start_url,
        display_mode=manifest.display_mode,
        orientation=manifest.orientation,
        theme_color=manifest.theme_color,
        background_color=manifest.background_color,
        scope=manifest.scope,
        lang=manifest.lang,
        dir=manifest.dir,
        categories=manifest.categories,
        icons=manifest.icons,
        screenshots=manifest.screenshots,
        shortcuts=manifest.shortcuts,
        related_applications=manifest.related_applications,
        prefer_related_applications=manifest.prefer_related_applications,
        is_active=manifest.is_active,
        is_default=manifest.is_default,
        created_by=manifest.created_by,
        created_at=manifest.created_at,
        updated_at=manifest.updated_at
    )


@router.get("/manifests", response_model=PWAManifestListResponse)
async def list_pwa_manifests(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_default: Optional[bool] = Query(None, description="Filter by default status"),
    display_mode: Optional[DisplayModeEnum] = Query(None, description="Filter by display mode"),
    search: Optional[str] = Query(None, description="Search in manifest names and descriptions"),
    db: DBSession = Depends(get_db)
):
    """
    List PWA manifests with filtering and pagination.
    """
    # Build base query
    query = db.query(PWAManifest)
    
    # Apply filters
    if is_active is not None:
        query = query.filter(PWAManifest.is_active == is_active)
    
    if is_default is not None:
        query = query.filter(PWAManifest.is_default == is_default)
    
    if display_mode:
        query = query.filter(PWAManifest.display_mode == display_mode)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                PWAManifest.manifest_name.ilike(search_term),
                PWAManifest.app_name.ilike(search_term),
                PWAManifest.short_name.ilike(search_term),
                PWAManifest.description.ilike(search_term)
            )
        )
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get manifests
    manifests = query.order_by(PWAManifest.manifest_name).offset(offset).limit(page_size).all()
    
    # Convert to response format
    manifest_responses = []
    for manifest in manifests:
        manifest_responses.append(PWAManifestResponse(
            id=str(manifest.id),
            manifest_name=manifest.manifest_name,
            app_name=manifest.app_name,
            short_name=manifest.short_name,
            description=manifest.description,
            start_url=manifest.start_url,
            display_mode=manifest.display_mode,
            orientation=manifest.orientation,
            theme_color=manifest.theme_color,
            background_color=manifest.background_color,
            scope=manifest.scope,
            lang=manifest.lang,
            dir=manifest.dir,
            categories=manifest.categories,
            icons=manifest.icons,
            screenshots=manifest.screenshots,
            shortcuts=manifest.shortcuts,
            related_applications=manifest.related_applications,
            prefer_related_applications=manifest.prefer_related_applications,
            is_active=manifest.is_active,
            is_default=manifest.is_default,
            created_by=manifest.created_by,
            created_at=manifest.created_at,
            updated_at=manifest.updated_at
        ))
    
    return PWAManifestListResponse(
        manifests=manifest_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


@router.get("/manifests/{manifest_id}", response_model=PWAManifestResponse)
async def get_pwa_manifest(
    manifest_id: str = Path(..., description="PWA manifest ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific PWA manifest by ID.
    """
    manifest = db.query(PWAManifest).filter(PWAManifest.id == manifest_id).first()
    
    if not manifest:
        raise HTTPException(status_code=404, detail="PWA manifest not found")
    
    return PWAManifestResponse(
        id=str(manifest.id),
        manifest_name=manifest.manifest_name,
        app_name=manifest.app_name,
        short_name=manifest.short_name,
        description=manifest.description,
        start_url=manifest.start_url,
        display_mode=manifest.display_mode,
        orientation=manifest.orientation,
        theme_color=manifest.theme_color,
        background_color=manifest.background_color,
        scope=manifest.scope,
        lang=manifest.lang,
        dir=manifest.dir,
        categories=manifest.categories,
        icons=manifest.icons,
        screenshots=manifest.screenshots,
        shortcuts=manifest.shortcuts,
        related_applications=manifest.related_applications,
        prefer_related_applications=manifest.prefer_related_applications,
        is_active=manifest.is_active,
        is_default=manifest.is_default,
        created_by=manifest.created_by,
        created_at=manifest.created_at,
        updated_at=manifest.updated_at
    )


@router.get("/manifests/{manifest_id}/manifest.json")
async def get_pwa_manifest_json(
    manifest_id: str = Path(..., description="PWA manifest ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get PWA manifest as JSON for browser consumption.
    """
    manifest = db.query(PWAManifest).filter(PWAManifest.id == manifest_id).first()
    
    if not manifest:
        raise HTTPException(status_code=404, detail="PWA manifest not found")
    
    # Convert to standard PWA manifest format
    manifest_json = {
        "name": manifest.app_name,
        "short_name": manifest.short_name,
        "description": manifest.description,
        "start_url": manifest.start_url,
        "display": manifest.display_mode,
        "orientation": manifest.orientation,
        "theme_color": manifest.theme_color,
        "background_color": manifest.background_color,
        "scope": manifest.scope,
        "lang": manifest.lang,
        "dir": manifest.dir,
        "categories": manifest.categories,
        "icons": manifest.icons,
        "screenshots": manifest.screenshots,
        "shortcuts": manifest.shortcuts,
        "related_applications": manifest.related_applications,
        "prefer_related_applications": manifest.prefer_related_applications
    }
    
    return JSONResponse(content=manifest_json, media_type="application/manifest+json")


# ============================================================================
# SERVICE WORKER MANAGEMENT
# ============================================================================

@router.post("/manifests/{manifest_id}/service-workers", response_model=ServiceWorkerResponse)
async def create_service_worker(
    manifest_id: str = Path(..., description="PWA manifest ID"),
    worker_data: ServiceWorkerCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new service worker for a PWA manifest.
    """
    # Verify manifest exists
    manifest = db.query(PWAManifest).filter(PWAManifest.id == manifest_id).first()
    if not manifest:
        raise HTTPException(status_code=404, detail="PWA manifest not found")
    
    # Check if worker name already exists for this manifest
    existing_worker = db.query(ServiceWorker).filter(
        and_(
            ServiceWorker.manifest_id == manifest_id,
            ServiceWorker.worker_name == worker_data.worker_name
        )
    ).first()
    
    if existing_worker:
        raise HTTPException(
            status_code=400,
            detail=f"Service worker with name '{worker_data.worker_name}' already exists for this manifest"
        )
    
    # If this is set as default, unset other defaults for this manifest
    if worker_data.is_default:
        db.query(ServiceWorker).filter(
            and_(
                ServiceWorker.manifest_id == manifest_id,
                ServiceWorker.is_default == True
            )
        ).update({"is_default": False})
    
    # Create new service worker
    worker = ServiceWorker(**worker_data.dict())
    worker.manifest_id = manifest_id
    worker.created_by = current_user.username
    db.add(worker)
    db.commit()
    db.refresh(worker)
    
    logger.info(f"Service worker created: {current_user.username} - {worker_data.worker_name}")
    
    return ServiceWorkerResponse(
        id=str(worker.id),
        manifest_id=str(worker.manifest_id),
        worker_name=worker.worker_name,
        worker_url=worker.worker_url,
        worker_scope=worker.worker_scope,
        worker_version=worker.worker_version,
        worker_script=worker.worker_script,
        is_active=worker.is_active,
        is_default=worker.is_default,
        cache_strategy=worker.cache_strategy,
        offline_fallback=worker.offline_fallback,
        push_enabled=worker.push_enabled,
        background_sync_enabled=worker.background_sync_enabled,
        created_by=worker.created_by,
        created_at=worker.created_at,
        updated_at=worker.updated_at
    )


@router.get("/manifests/{manifest_id}/service-workers", response_model=ServiceWorkerListResponse)
async def list_service_workers(
    manifest_id: str = Path(..., description="PWA manifest ID"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_default: Optional[bool] = Query(None, description="Filter by default status"),
    cache_strategy: Optional[CacheStrategyEnum] = Query(None, description="Filter by cache strategy"),
    db: DBSession = Depends(get_db)
):
    """
    List service workers for a specific PWA manifest.
    """
    # Verify manifest exists
    manifest = db.query(PWAManifest).filter(PWAManifest.id == manifest_id).first()
    if not manifest:
        raise HTTPException(status_code=404, detail="PWA manifest not found")
    
    # Build base query
    query = db.query(ServiceWorker).filter(ServiceWorker.manifest_id == manifest_id)
    
    # Apply filters
    if is_active is not None:
        query = query.filter(ServiceWorker.is_active == is_active)
    
    if is_default is not None:
        query = query.filter(ServiceWorker.is_default == is_default)
    
    if cache_strategy:
        query = query.filter(ServiceWorker.cache_strategy == cache_strategy)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get workers
    workers = query.order_by(ServiceWorker.worker_name).offset(offset).limit(page_size).all()
    
    # Convert to response format
    worker_responses = []
    for worker in workers:
        worker_responses.append(ServiceWorkerResponse(
            id=str(worker.id),
            manifest_id=str(worker.manifest_id),
            worker_name=worker.worker_name,
            worker_url=worker.worker_url,
            worker_scope=worker.worker_scope,
            worker_version=worker.worker_version,
            worker_script=worker.worker_script,
            is_active=worker.is_active,
            is_default=worker.is_default,
            cache_strategy=worker.cache_strategy,
            offline_fallback=worker.offline_fallback,
            push_enabled=worker.push_enabled,
            background_sync_enabled=worker.background_sync_enabled,
            created_by=worker.created_by,
            created_at=worker.created_at,
            updated_at=worker.updated_at
        ))
    
    return ServiceWorkerListResponse(
        workers=worker_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


# ============================================================================
# OFFLINE RESOURCE MANAGEMENT
# ============================================================================

@router.post("/manifests/{manifest_id}/offline-resources", response_model=OfflineResourceResponse)
async def create_offline_resource(
    manifest_id: str = Path(..., description="PWA manifest ID"),
    resource_data: OfflineResourceCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new offline resource for a PWA manifest.
    """
    # Verify manifest exists
    manifest = db.query(PWAManifest).filter(PWAManifest.id == manifest_id).first()
    if not manifest:
        raise HTTPException(status_code=404, detail="PWA manifest not found")
    
    # Check if resource URL already exists for this manifest
    existing_resource = db.query(OfflineResource).filter(
        and_(
            OfflineResource.manifest_id == manifest_id,
            OfflineResource.resource_url == resource_data.resource_url
        )
    ).first()
    
    if existing_resource:
        raise HTTPException(
            status_code=400,
            detail=f"Offline resource with URL '{resource_data.resource_url}' already exists for this manifest"
        )
    
    # Create new offline resource
    resource = OfflineResource(**resource_data.dict())
    resource.manifest_id = manifest_id
    db.add(resource)
    db.commit()
    db.refresh(resource)
    
    logger.info(f"Offline resource created: {current_user.username} - {resource_data.resource_url}")
    
    return OfflineResourceResponse(
        id=str(resource.id),
        manifest_id=str(resource.manifest_id),
        resource_url=resource.resource_url,
        resource_type=resource.resource_type,
        resource_category=resource.resource_category,
        cache_duration=resource.cache_duration,
        is_offline_available=resource.is_offline_available,
        compression_enabled=resource.compression_enabled,
        version_hash=resource.version_hash,
        file_size=resource.file_size,
        last_updated=resource.last_updated,
        created_at=resource.created_at,
        updated_at=resource.updated_at
    )


@router.get("/manifests/{manifest_id}/offline-resources", response_model=OfflineResourceListResponse)
async def list_offline_resources(
    manifest_id: str = Path(..., description="PWA manifest ID"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    resource_type: Optional[ResourceTypeEnum] = Query(None, description="Filter by resource type"),
    resource_category: Optional[ResourceCategoryEnum] = Query(None, description="Filter by resource category"),
    is_offline_available: Optional[bool] = Query(None, description="Filter by offline availability"),
    db: DBSession = Depends(get_db)
):
    """
    List offline resources for a specific PWA manifest.
    """
    # Verify manifest exists
    manifest = db.query(PWAManifest).filter(PWAManifest.id == manifest_id).first()
    if not manifest:
        raise HTTPException(status_code=404, detail="PWA manifest not found")
    
    # Build base query
    query = db.query(OfflineResource).filter(OfflineResource.manifest_id == manifest_id)
    
    # Apply filters
    if resource_type:
        query = query.filter(OfflineResource.resource_type == resource_type)
    
    if resource_category:
        query = query.filter(OfflineResource.resource_category == resource_category)
    
    if is_offline_available is not None:
        query = query.filter(OfflineResource.is_offline_available == is_offline_available)
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get resources
    resources = query.order_by(OfflineResource.resource_url).offset(offset).limit(page_size).all()
    
    # Convert to response format
    resource_responses = []
    for resource in resources:
        resource_responses.append(OfflineResourceResponse(
            id=str(resource.id),
            manifest_id=str(resource.manifest_id),
            resource_url=resource.resource_url,
            resource_type=resource.resource_type,
            resource_category=resource.resource_category,
            cache_duration=resource.cache_duration,
            is_offline_available=resource.is_offline_available,
            compression_enabled=resource.compression_enabled,
            version_hash=resource.version_hash,
            file_size=resource.file_size,
            last_updated=resource.last_updated,
            created_at=resource.created_at,
            updated_at=resource.updated_at
        ))
    
    return OfflineResourceListResponse(
        resources=resource_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


# ============================================================================
# PWA INSTALLATION TRACKING
# ============================================================================

@router.post("/installations/track")
async def track_pwa_installation(
    tracking_data: PWAInstallationTrackingRequest = Body(...),
    db: DBSession = Depends(get_db)
):
    """
    Track PWA installation for analytics.
    """
    # Verify manifest exists
    manifest = db.query(PWAManifest).filter(PWAManifest.id == tracking_data.manifest_id).first()
    if not manifest:
        raise HTTPException(status_code=404, detail="PWA manifest not found")
    
    # Create installation record
    installation = PWAInstallation(
        manifest_id=tracking_data.manifest_id,
        session_id=tracking_data.session_id,
        device_type=tracking_data.device_type,
        platform=tracking_data.platform,
        browser=tracking_data.browser,
        install_method=tracking_data.install_method,
        install_timestamp=datetime.utcnow(),
        is_active=True,
        usage_count=1,
        last_used=datetime.utcnow()
    )
    
    db.add(installation)
    db.commit()
    db.refresh(installation)
    
    # Update analytics
    _update_pwa_analytics(db, tracking_data.manifest_id, "installation")
    
    logger.info(f"PWA installation tracked: {tracking_data.manifest_id} - {tracking_data.platform}")
    
    return {
        "message": "PWA installation tracked successfully",
        "installation_id": str(installation.id),
        "tracked_at": datetime.utcnow()
    }


# ============================================================================
# STATISTICS AND ANALYTICS
# ============================================================================

@router.get("/statistics")
async def get_pwa_statistics(
    db: DBSession = Depends(get_db)
):
    """
    Get comprehensive PWA statistics.
    """
    # Get all manifests
    manifests = db.query(PWAManifest).filter(PWAManifest.is_active == True).all()
    
    statistics = []
    for manifest in manifests:
        # Get installation data
        installations = db.query(PWAInstallation).filter(
            PWAInstallation.manifest_id == manifest.id
        ).all()
        
        total_installations = len(installations)
        active_installations = len([i for i in installations if i.is_active])
        
        # Get analytics data
        analytics = db.query(PWAAnalytics).filter(
            PWAAnalytics.manifest_id == manifest.id
        ).all()
        
        # Calculate statistics
        total_users = len(set([i.user_id for i in installations if i.user_id]))
        daily_active_users = sum([a.daily_active_users for a in analytics])
        
        # Calculate averages
        avg_session_duration = 0
        offline_usage_percentage = 0
        cache_hit_rate = 0
        push_notification_rate = 0
        
        if analytics:
            avg_session_duration = sum([a.avg_session_duration for a in analytics]) / len(analytics)
            offline_usage_percentage = sum([a.offline_usage_percentage for a in analytics]) / len(analytics)
            cache_hit_rate = sum([a.cache_hit_rate for a in analytics]) / len(analytics)
            
            total_sent = sum([a.push_notification_sent for a in analytics])
            total_opened = sum([a.push_notification_opened for a in analytics])
            push_notification_rate = (total_opened / total_sent * 100) if total_sent > 0 else 0
        
        statistics.append(PWAStatistics(
            manifest_id=str(manifest.id),
            app_name=manifest.app_name,
            total_installations=total_installations,
            active_installations=active_installations,
            total_users=total_users,
            daily_active_users=daily_active_users,
            avg_session_duration=avg_session_duration,
            offline_usage_percentage=round(offline_usage_percentage, 2),
            cache_hit_rate=round(cache_hit_rate, 2),
            push_notification_rate=round(push_notification_rate, 2),
            generated_at=datetime.utcnow()
        ))
    
    return {
        "manifests": statistics,
        "total_manifests": len(manifests),
        "generated_at": datetime.utcnow()
    }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def _update_pwa_analytics(db: DBSession, manifest_id: str, event_type: str) -> None:
    """Update PWA analytics for a specific event."""
    today = datetime.utcnow().date()
    
    # Get or create analytics record for today
    analytics = db.query(PWAAnalytics).filter(
        and_(
            PWAAnalytics.manifest_id == manifest_id,
            func.date(PWAAnalytics.analytics_date) == today
        )
    ).first()
    
    if not analytics:
        analytics = PWAAnalytics(
            manifest_id=manifest_id,
            analytics_date=datetime.utcnow()
        )
        db.add(analytics)
    
    # Update based on event type
    if event_type == "installation":
        analytics.daily_installations += 1
    elif event_type == "uninstallation":
        analytics.daily_uninstallations += 1
    elif event_type == "session":
        analytics.daily_sessions += 1
    elif event_type == "page_view":
        analytics.daily_page_views += 1
    
    db.commit()
