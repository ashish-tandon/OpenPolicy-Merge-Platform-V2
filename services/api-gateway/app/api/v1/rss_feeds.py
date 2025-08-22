"""
RSS Feeds API for OpenPolicy V2

Comprehensive RSS feed system for content distribution.
Implements P2 priority feature for enhanced content distribution and user engagement.
"""

from fastapi import APIRouter, HTTPException, Query, Depends, Path, Body, Response
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import and_, or_, desc, func
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import math
import xml.etree.ElementTree as ET
import hashlib
import json

from app.database import get_db
from app.models.rss_feeds import RSSFeed, RSSFeedItem, RSSSubscription, RSSAnalytics, RSSCache
from app.models.parliamentary_entities import ParliamentaryEntity
from app.schemas.rss_feeds import (
    RSSFeedResponse, RSSFeedItemResponse, RSSSubscriptionResponse, RSSAnalyticsResponse,
    RSSFeedListResponse, RSSFeedItemListResponse, RSSSubscriptionListResponse,
    RSSAnalyticsListResponse, RSSFeedCreateRequest, RSSFeedUpdateRequest,
    RSSFeedItemCreateRequest, RSSFeedItemUpdateRequest, RSSSubscriptionCreateRequest,
    RSSFeedGenerateRequest, RSSFeedStatistics, RSSSystemStatistics,
    RSSValidationResult, RSSCacheStatus, RSSFeedPreview, FeedTypeEnum, ContentTypeEnum
)
from app.api.v1.auth import get_current_user
from app.models.users import User
import structlog

logger = structlog.get_logger(__name__)
router = APIRouter()


# ============================================================================
# RSS FEED MANAGEMENT
# ============================================================================

@router.post("/feeds", response_model=RSSFeedResponse)
async def create_rss_feed(
    feed_data: RSSFeedCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new RSS feed.
    
    This creates a new RSS feed configuration for content distribution.
    """
    # Check if feed name already exists
    existing_feed = db.query(RSSFeed).filter(RSSFeed.feed_name == feed_data.feed_name).first()
    if existing_feed:
        raise HTTPException(
            status_code=400,
            detail=f"Feed with name '{feed_data.feed_name}' already exists"
        )
    
    # Check if feed URL already exists
    existing_url = db.query(RSSFeed).filter(RSSFeed.feed_url == feed_data.feed_url).first()
    if existing_url:
        raise HTTPException(
            status_code=400,
            detail=f"Feed with URL '{feed_data.feed_url}' already exists"
        )
    
    # Create new feed
    feed = RSSFeed(**feed_data.dict())
    db.add(feed)
    db.commit()
    db.refresh(feed)
    
    logger.info(f"RSS feed created: {current_user.username} - {feed_data.feed_name}")
    
    return RSSFeedResponse(
        id=str(feed.id),
        feed_name=feed.feed_name,
        feed_title=feed.feed_title,
        feed_description=feed.feed_description,
        feed_type=feed.feed_type,
        feed_url=feed.feed_url,
        feed_language=feed.feed_language,
        is_active=feed.is_active,
        is_public=feed.is_public,
        max_items=feed.max_items,
        update_frequency_minutes=feed.update_frequency_minutes,
        last_generated=feed.last_generated,
        last_error=feed.last_error,
        generation_count=feed.generation_count,
        subscriber_count=feed.subscriber_count,
        filter_criteria=feed.filter_criteria,
        custom_styling=feed.custom_styling,
        created_at=feed.created_at,
        updated_at=feed.updated_at
    )


@router.get("/feeds", response_model=RSSFeedListResponse)
async def list_rss_feeds(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    feed_type: Optional[FeedTypeEnum] = Query(None, description="Filter by feed type"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_public: Optional[bool] = Query(None, description="Filter by public status"),
    language: Optional[str] = Query(None, description="Filter by language"),
    search: Optional[str] = Query(None, description="Search in feed name or title"),
    db: DBSession = Depends(get_db)
):
    """
    List RSS feeds with filtering and pagination.
    """
    # Build base query
    query = db.query(RSSFeed)
    
    # Apply filters
    if feed_type:
        query = query.filter(RSSFeed.feed_type == feed_type)
    
    if is_active is not None:
        query = query.filter(RSSFeed.is_active == is_active)
    
    if is_public is not None:
        query = query.filter(RSSFeed.is_public == is_public)
    
    if language:
        query = query.filter(RSSFeed.feed_language == language)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                RSSFeed.feed_name.ilike(search_term),
                RSSFeed.feed_title.ilike(search_term),
                RSSFeed.feed_description.ilike(search_term)
            )
        )
    
    # Get total count
    total = query.count()
    
    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    
    # Get feeds
    feeds = query.order_by(desc(RSSFeed.created_at)).offset(offset).limit(page_size).all()
    
    # Convert to response format
    feed_responses = []
    for feed in feeds:
        feed_responses.append(RSSFeedResponse(
            id=str(feed.id),
            feed_name=feed.feed_name,
            feed_title=feed.feed_title,
            feed_description=feed.feed_description,
            feed_type=feed.feed_type,
            feed_url=feed.feed_url,
            feed_language=feed.feed_language,
            is_active=feed.is_active,
            is_public=feed.is_public,
            max_items=feed.max_items,
            update_frequency_minutes=feed.update_frequency_minutes,
            last_generated=feed.last_generated,
            last_error=feed.last_error,
            generation_count=feed.generation_count,
            subscriber_count=feed.subscriber_count,
            filter_criteria=feed.filter_criteria,
            custom_styling=feed.custom_styling,
            created_at=feed.created_at,
            updated_at=feed.updated_at
        ))
    
    return RSSFeedListResponse(
        feeds=feed_responses,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    )


@router.get("/feeds/{feed_id}", response_model=RSSFeedResponse)
async def get_rss_feed(
    feed_id: str = Path(..., description="Feed ID"),
    db: DBSession = Depends(get_db)
):
    """
    Get a specific RSS feed by ID.
    """
    feed = db.query(RSSFeed).filter(RSSFeed.id == feed_id).first()
    
    if not feed:
        raise HTTPException(status_code=404, detail="RSS feed not found")
    
    return RSSFeedResponse(
        id=str(feed.id),
        feed_name=feed.feed_name,
        feed_title=feed.feed_title,
        feed_description=feed.feed_description,
        feed_type=feed.feed_type,
        feed_url=feed.feed_url,
        feed_language=feed.feed_language,
        is_active=feed.is_active,
        is_public=feed.is_public,
        max_items=feed.max_items,
        update_frequency_minutes=feed.update_frequency_minutes,
        last_generated=feed.last_generated,
        last_error=feed.last_error,
        generation_count=feed.generation_count,
        subscriber_count=feed.subscriber_count,
        filter_criteria=feed.filter_criteria,
        custom_styling=feed.custom_styling,
        created_at=feed.created_at,
        updated_at=feed.updated_at
    )


@router.put("/feeds/{feed_id}", response_model=RSSFeedResponse)
async def update_rss_feed(
    feed_id: str = Path(..., description="Feed ID"),
    feed_data: RSSFeedUpdateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an RSS feed.
    """
    feed = db.query(RSSFeed).filter(RSSFeed.id == feed_id).first()
    
    if not feed:
        raise HTTPException(status_code=404, detail="RSS feed not found")
    
    # Update feed fields
    update_data = feed_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(feed, field):
            setattr(feed, field, value)
    
    feed.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(feed)
    
    logger.info(f"RSS feed updated: {current_user.username} - {feed.feed_name}")
    
    return RSSFeedResponse(
        id=str(feed.id),
        feed_name=feed.feed_name,
        feed_title=feed.feed_title,
        feed_description=feed.feed_description,
        feed_type=feed.feed_type,
        feed_url=feed.feed_url,
        feed_language=feed.feed_language,
        is_active=feed.is_active,
        is_public=feed.is_public,
        max_items=feed.max_items,
        update_frequency_minutes=feed.update_frequency_minutes,
        last_generated=feed.last_generated,
        last_error=feed.last_error,
        generation_count=feed.generation_count,
        subscriber_count=feed.subscriber_count,
        filter_criteria=feed.filter_criteria,
        custom_styling=feed.custom_styling,
        created_at=feed.created_at,
        updated_at=feed.updated_at
    )


@router.delete("/feeds/{feed_id}")
async def delete_rss_feed(
    feed_id: str = Path(..., description="Feed ID"),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an RSS feed.
    """
    feed = db.query(RSSFeed).filter(RSSFeed.id == feed_id).first()
    
    if not feed:
        raise HTTPException(status_code=404, detail="RSS feed not found")
    
    feed_name = feed.feed_name
    db.delete(feed)
    db.commit()
    
    logger.info(f"RSS feed deleted: {current_user.username} - {feed_name}")
    
    return {"message": f"RSS feed '{feed_name}' deleted successfully"}


# ============================================================================
# RSS FEED GENERATION AND XML OUTPUT
# ============================================================================

@router.get("/feeds/{feed_id}/generate", response_class=PlainTextResponse)
async def generate_rss_feed(
    feed_id: str = Path(..., description="Feed ID"),
    force: bool = Query(False, description="Force regeneration"),
    db: DBSession = Depends(get_db)
):
    """
    Generate RSS XML for a specific feed.
    """
    feed = db.query(RSSFeed).filter(RSSFeed.id == feed_id).first()
    
    if not feed:
        raise HTTPException(status_code=404, detail="RSS feed not found")
    
    if not feed.is_active:
        raise HTTPException(status_code=400, detail="RSS feed is not active")
    
    # Check cache first
    cache_key = f"rss_feed_{feed_id}"
    cached_content = None
    
    if not force:
        cached_content = db.query(RSSCache).filter(
            and_(
                RSSCache.feed_id == feed_id,
                RSSCache.cache_key == cache_key,
                RSSCache.expires_at > datetime.utcnow()
            )
        ).first()
    
    if cached_content:
        # Update cache hits
        cached_content.hits += 1
        cached_content.last_hit = datetime.utcnow()
        db.commit()
        
        # Track analytics
        _track_feed_access(db, feed_id)
        
        return PlainTextResponse(
            content=cached_content.rss_content,
            media_type="application/rss+xml"
        )
    
    # Generate new RSS content
    start_time = datetime.utcnow()
    
    try:
        rss_xml = await _generate_rss_xml(db, feed)
        generation_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        # Cache the generated content
        content_hash = hashlib.md5(rss_xml.encode()).hexdigest()
        expires_at = datetime.utcnow() + timedelta(minutes=feed.update_frequency_minutes)
        
        # Remove old cache entries
        db.query(RSSCache).filter(RSSCache.feed_id == feed_id).delete()
        
        # Create new cache entry
        cache_entry = RSSCache(
            feed_id=feed_id,
            cache_key=cache_key,
            rss_content=rss_xml,
            content_hash=content_hash,
            item_count=len(rss_xml.split('<item>')),
            generation_time_ms=int(generation_time),
            expires_at=expires_at,
            hits=1,
            last_hit=datetime.utcnow()
        )
        db.add(cache_entry)
        
        # Update feed metadata
        feed.last_generated = datetime.utcnow()
        feed.generation_count += 1
        feed.last_error = None
        
        db.commit()
        
        # Track analytics
        _track_feed_access(db, feed_id)
        
        logger.info(f"RSS feed generated: {feed.feed_name} - {generation_time:.2f}ms")
        
        return PlainTextResponse(
            content=rss_xml,
            media_type="application/rss+xml"
        )
        
    except Exception as e:
        # Log error
        error_message = str(e)
        feed.last_error = error_message
        db.commit()
        
        logger.error(f"RSS feed generation failed: {feed.feed_name} - {error_message}")
        
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate RSS feed: {error_message}"
        )


@router.get("/feeds/by-name/{feed_name}", response_class=PlainTextResponse)
async def get_rss_feed_by_name(
    feed_name: str = Path(..., description="Feed name"),
    db: DBSession = Depends(get_db)
):
    """
    Get RSS XML by feed name (for direct RSS client access).
    """
    feed = db.query(RSSFeed).filter(
        and_(
            RSSFeed.feed_name == feed_name,
            RSSFeed.is_active == True,
            RSSFeed.is_public == True
        )
    ).first()
    
    if not feed:
        raise HTTPException(status_code=404, detail="RSS feed not found")
    
    return await generate_rss_feed(str(feed.id), False, db)


# ============================================================================
# RSS FEED ITEMS MANAGEMENT
# ============================================================================

@router.post("/feeds/{feed_id}/items", response_model=RSSFeedItemResponse)
async def create_rss_feed_item(
    feed_id: str = Path(..., description="Feed ID"),
    item_data: RSSFeedItemCreateRequest = Body(...),
    db: DBSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new RSS feed item.
    """
    # Verify feed exists
    feed = db.query(RSSFeed).filter(RSSFeed.id == feed_id).first()
    if not feed:
        raise HTTPException(status_code=404, detail="RSS feed not found")
    
    # Check if item GUID already exists
    existing_item = db.query(RSSFeedItem).filter(
        RSSFeedItem.item_guid == item_data.item_guid
    ).first()
    
    if existing_item:
        raise HTTPException(
            status_code=400,
            detail=f"Feed item with GUID '{item_data.item_guid}' already exists"
        )
    
    # Create new item
    item = RSSFeedItem(**item_data.dict())
    item.feed_id = feed_id
    db.add(item)
    db.commit()
    db.refresh(item)
    
    # Invalidate cache for this feed
    _invalidate_feed_cache(db, feed_id)
    
    logger.info(f"RSS feed item created: {current_user.username} - {item_data.item_title}")
    
    return RSSFeedItemResponse(
        id=str(item.id),
        feed_id=str(item.feed_id),
        item_title=item.item_title,
        item_description=item.item_description,
        item_link=item.item_link,
        item_guid=item.item_guid,
        item_pub_date=item.item_pub_date,
        item_category=item.item_category,
        item_author=item.item_author,
        content_type=item.content_type,
        content_id=item.content_id,
        item_content=item.item_content,
        item_summary=item.item_summary,
        is_featured=item.is_featured,
        view_count=item.view_count,
        item_metadata=item.item_metadata,
        created_at=item.created_at,
        updated_at=item.updated_at
    )


# ============================================================================
# RSS ANALYTICS AND STATISTICS
# ============================================================================

@router.get("/feeds/{feed_id}/statistics", response_model=RSSFeedStatistics)
async def get_rss_feed_statistics(
    feed_id: str = Path(..., description="Feed ID"),
    days: int = Query(30, ge=1, le=365, description="Number of days for statistics"),
    db: DBSession = Depends(get_db)
):
    """
    Get comprehensive statistics for an RSS feed.
    """
    feed = db.query(RSSFeed).filter(RSSFeed.id == feed_id).first()
    
    if not feed:
        raise HTTPException(status_code=404, detail="RSS feed not found")
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Get analytics data
    analytics = db.query(RSSAnalytics).filter(
        and_(
            RSSAnalytics.feed_id == feed_id,
            RSSAnalytics.analytics_date >= start_date
        )
    ).all()
    
    # Calculate statistics
    total_items = db.query(RSSFeedItem).filter(RSSFeedItem.feed_id == feed_id).count()
    total_views = sum([a.daily_views for a in analytics])
    total_subscribers = feed.subscriber_count
    
    # Calculate averages
    avg_generation_time = 0
    if analytics:
        avg_generation_time = sum([a.generation_time_ms for a in analytics]) / len(analytics)
    
    # Time-based views
    last_24h_analytics = [a for a in analytics if a.analytics_date >= end_date - timedelta(hours=24)]
    last_7d_analytics = [a for a in analytics if a.analytics_date >= end_date - timedelta(days=7)]
    last_30d_analytics = [a for a in analytics if a.analytics_date >= end_date - timedelta(days=30)]
    
    last_24h_views = sum([a.daily_views for a in last_24h_analytics])
    last_7d_views = sum([a.daily_views for a in last_7d_analytics])
    last_30d_views = sum([a.daily_views for a in last_30d_analytics])
    
    # Top categories (mock data for now)
    top_categories = [
        {"category": "Bills", "count": 45},
        {"category": "Votes", "count": 32},
        {"category": "Debates", "count": 28}
    ]
    
    # Subscriber growth (mock data for now)
    subscriber_growth = [
        {"date": "2024-01-15", "subscribers": 120},
        {"date": "2024-01-16", "subscribers": 125},
        {"date": "2024-01-17", "subscribers": 128}
    ]
    
    # Error rate
    error_count = sum([a.error_count for a in analytics])
    total_generations = len(analytics)
    error_rate = (error_count / total_generations * 100) if total_generations > 0 else 0
    
    # Cache hit rate (mock for now)
    cache_hit_rate = 85.5
    
    return RSSFeedStatistics(
        feed_id=feed_id,
        feed_name=feed.feed_name,
        total_items=total_items,
        total_subscribers=total_subscribers,
        total_views=total_views,
        avg_generation_time=avg_generation_time,
        last_24h_views=last_24h_views,
        last_7d_views=last_7d_views,
        last_30d_views=last_30d_views,
        top_categories=top_categories,
        subscriber_growth=subscriber_growth,
        error_rate=round(error_rate, 2),
        cache_hit_rate=cache_hit_rate,
        generated_at=datetime.utcnow()
    )


@router.get("/statistics", response_model=RSSSystemStatistics)
async def get_rss_system_statistics(
    db: DBSession = Depends(get_db)
):
    """
    Get system-wide RSS statistics.
    """
    # Count feeds
    total_feeds = db.query(RSSFeed).count()
    active_feeds = db.query(RSSFeed).filter(RSSFeed.is_active == True).count()
    
    # Count items
    total_items = db.query(RSSFeedItem).count()
    
    # Count subscribers
    total_subscribers = db.query(func.sum(RSSFeed.subscriber_count)).scalar() or 0
    
    # Views in last 24 hours
    yesterday = datetime.utcnow() - timedelta(hours=24)
    total_views_24h = db.query(func.sum(RSSAnalytics.daily_views)).filter(
        RSSAnalytics.analytics_date >= yesterday
    ).scalar() or 0
    
    # Averages
    avg_items_per_feed = total_items / total_feeds if total_feeds > 0 else 0
    avg_subscribers_per_feed = total_subscribers / total_feeds if total_feeds > 0 else 0
    
    # Top performing feeds
    top_feeds = db.query(RSSFeed).order_by(desc(RSSFeed.subscriber_count)).limit(5).all()
    top_performing_feeds = [
        {"feed_name": feed.feed_name, "subscribers": feed.subscriber_count}
        for feed in top_feeds
    ]
    
    # Feed type distribution
    feed_types = db.query(RSSFeed.feed_type, func.count(RSSFeed.id)).group_by(RSSFeed.feed_type).all()
    feed_type_distribution = {feed_type: count for feed_type, count in feed_types}
    
    # Language distribution
    languages = db.query(RSSFeed.feed_language, func.count(RSSFeed.id)).group_by(RSSFeed.feed_language).all()
    language_distribution = {lang: count for lang, count in languages}
    
    # Error summary (mock for now)
    error_summary = {
        "generation_errors": 2,
        "cache_errors": 0,
        "validation_errors": 1
    }
    
    # Cache performance (mock for now)
    cache_performance = {
        "hit_rate": 87.3,
        "average_response_time": 23.5,
        "cache_size_mb": 45.2
    }
    
    return RSSSystemStatistics(
        total_feeds=total_feeds,
        active_feeds=active_feeds,
        total_items=total_items,
        total_subscribers=total_subscribers,
        total_views_24h=total_views_24h,
        avg_items_per_feed=round(avg_items_per_feed, 1),
        avg_subscribers_per_feed=round(avg_subscribers_per_feed, 1),
        top_performing_feeds=top_performing_feeds,
        feed_type_distribution=feed_type_distribution,
        language_distribution=language_distribution,
        error_summary=error_summary,
        cache_performance=cache_performance,
        generated_at=datetime.utcnow()
    )


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

async def _generate_rss_xml(db: DBSession, feed: RSSFeed) -> str:
    """Generate RSS XML content for a feed."""
    
    # Create RSS root element
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    
    # Add channel information
    ET.SubElement(channel, "title").text = feed.feed_title
    ET.SubElement(channel, "description").text = feed.feed_description
    ET.SubElement(channel, "link").text = f"https://openpolicy.ca{feed.feed_url}"
    ET.SubElement(channel, "language").text = feed.feed_language
    ET.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    ET.SubElement(channel, "generator").text = "OpenPolicy V2 RSS Generator"
    ET.SubElement(channel, "ttl").text = str(feed.update_frequency_minutes)
    
    # Get content based on feed type
    items = []
    
    if feed.feed_type == "bills":
        bills = db.query(ParliamentaryEntity).filter(
            ParliamentaryEntity.type == "bill"
        ).order_by(desc(ParliamentaryEntity.updated_at)).limit(feed.max_items).all()
        for bill in bills:
            items.append(_create_bill_item(bill))
    
    elif feed.feed_type == "votes":
        votes = db.query(ParliamentaryEntity).filter(
            ParliamentaryEntity.type == "vote"
        ).order_by(desc(ParliamentaryEntity.updated_at)).limit(feed.max_items).all()
        for vote in votes:
            items.append(_create_vote_item(vote))
    
    elif feed.feed_type == "committees":
        committees = db.query(ParliamentaryEntity).filter(
            ParliamentaryEntity.type == "committee"
        ).order_by(desc(ParliamentaryEntity.updated_at)).limit(feed.max_items).all()
        for committee in committees:
            items.append(_create_committee_item(committee))
    
    elif feed.feed_type == "members":
        members = db.query(ParliamentaryEntity).filter(
            ParliamentaryEntity.type == "member"
        ).order_by(desc(ParliamentaryEntity.updated_at)).limit(feed.max_items).all()
        for member in members:
            items.append(_create_member_item(member))
    
    elif feed.feed_type == "all":
        # Get mix of all content types
        entities = db.query(ParliamentaryEntity).order_by(desc(ParliamentaryEntity.updated_at)).limit(feed.max_items).all()
        for entity in entities:
            if entity.type == "bill":
                items.append(_create_bill_item(entity))
            elif entity.type == "vote":
                items.append(_create_vote_item(entity))
            elif entity.type == "committee":
                items.append(_create_committee_item(entity))
            elif entity.type == "member":
                items.append(_create_member_item(entity))
    
    # Add items to channel
    for item_data in items:
        item_elem = ET.SubElement(channel, "item")
        ET.SubElement(item_elem, "title").text = item_data["title"]
        ET.SubElement(item_elem, "description").text = item_data["description"]
        ET.SubElement(item_elem, "link").text = item_data["link"]
        ET.SubElement(item_elem, "guid", isPermaLink="false").text = item_data["guid"]
        ET.SubElement(item_elem, "pubDate").text = item_data["pubDate"]
        if item_data.get("category"):
            ET.SubElement(item_elem, "category").text = item_data["category"]
        if item_data.get("author"):
            ET.SubElement(item_elem, "author").text = item_data["author"]
    
    # Convert to string
    xml_str = ET.tostring(rss, encoding="unicode")
    
    # Add XML declaration
    return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'


def _create_bill_item(entity: ParliamentaryEntity) -> Dict[str, str]:
    """Create RSS item data for a bill entity."""
    bill_data = entity.data
    bill_number = bill_data.get("number", "Unknown")
    bill_name = bill_data.get("name_en", bill_data.get("title", "Unknown Bill"))
    
    return {
        "title": f"Bill {bill_number}: {bill_name}",
        "description": bill_data.get("summary_en", bill_data.get("description", bill_name)),
        "link": f"https://openpolicy.ca/bills/{bill_data.get('session_id', '44-1')}/{bill_number}",
        "guid": f"bill_{entity.source_id or entity.id}",
        "pubDate": entity.updated_at.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "category": "Bills",
        "author": "Parliament of Canada"
    }


def _create_vote_item(entity: ParliamentaryEntity) -> Dict[str, str]:
    """Create RSS item data for a vote entity."""
    vote_data = entity.data
    vote_number = vote_data.get("vote_number", "Unknown")
    bill_number = vote_data.get("bill_number", "")
    
    return {
        "title": f"Vote {vote_number}: {bill_number or 'Motion'}",
        "description": vote_data.get("description", f"Parliamentary vote on {bill_number or 'motion'}"),
        "link": f"https://openpolicy.ca/votes/{vote_number}",
        "guid": f"vote_{entity.source_id or entity.id}",
        "pubDate": entity.updated_at.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "category": "Votes",
        "author": "Parliament of Canada"
    }


def _create_committee_item(entity: ParliamentaryEntity) -> Dict[str, str]:
    """Create RSS item data for a committee entity."""
    committee_data = entity.data
    committee_name = committee_data.get("name_en", committee_data.get("name", "Unknown Committee"))
    committee_code = committee_data.get("committee_code", entity.source_id or str(entity.id))
    
    return {
        "title": f"Committee: {committee_name}",
        "description": committee_data.get("mandate_en", committee_data.get("description", f"Parliamentary committee: {committee_name}")),
        "link": f"https://openpolicy.ca/committees/{committee_code}",
        "guid": f"committee_{entity.source_id or entity.id}",
        "pubDate": entity.updated_at.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "category": "Committees",
        "author": "Parliament of Canada"
    }


def _create_member_item(entity: ParliamentaryEntity) -> Dict[str, str]:
    """Create RSS item data for a member entity."""
    member_data = entity.data
    member_name = member_data.get("name", "Unknown Member")
    party = member_data.get("party", "Unknown Party")
    riding = member_data.get("riding", "Unknown Riding")
    member_id = member_data.get("member_id", entity.source_id or str(entity.id))
    
    return {
        "title": f"MP: {member_name} ({party})",
        "description": f"{member_name}, {party} representative for {riding}",
        "link": f"https://openpolicy.ca/members/{member_id}",
        "guid": f"member_{entity.source_id or entity.id}",
        "pubDate": entity.updated_at.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "category": "Members",
        "author": "Parliament of Canada"
    }


def _track_feed_access(db: DBSession, feed_id: str) -> None:
    """Track RSS feed access for analytics."""
    today = datetime.utcnow().date()
    
    # Get or create analytics record for today
    analytics = db.query(RSSAnalytics).filter(
        and_(
            RSSAnalytics.feed_id == feed_id,
            func.date(RSSAnalytics.analytics_date) == today
        )
    ).first()
    
    if not analytics:
        analytics = RSSAnalytics(
            feed_id=feed_id,
            analytics_date=datetime.utcnow(),
            daily_views=1
        )
        db.add(analytics)
    else:
        analytics.daily_views += 1
    
    db.commit()


def _invalidate_feed_cache(db: DBSession, feed_id: str) -> None:
    """Invalidate cache for a specific feed."""
    db.query(RSSCache).filter(RSSCache.feed_id == feed_id).delete()
    db.commit()
