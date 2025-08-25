"""
News Aggregation API endpoints.

Implements FEAT-020 News Aggregation (P2 priority).
Provides comprehensive news aggregation and management.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.core.dependencies import get_current_user, require_permission
from app.core.news_aggregation import NewsAggregationService, get_news_aggregation_service
from app.models.users import User
from app.schemas.news_aggregation import (
    NewsSourceCreate, NewsSourceUpdate, NewsSourceResponse,
    NewsArticleCreate, NewsArticleUpdate, NewsArticleResponse, NewsArticleListResponse,
    RelatedArticleResponse, ArticleMentionResponse,
    NewsTopicCreate, NewsTopicUpdate, NewsTopicResponse,
    NewsDigestCreate, NewsDigestResponse,
    NewsAlertCreate, NewsAlertUpdate, NewsAlertResponse,
    NewsSearchRequest, ArticleInteractionCreate, SavedArticleResponse,
    NewsAnalytics, SourceMetrics, AggregationJobStatus,
    NewsSourceType, NewsCategory, NewsSentiment
)
import logging
import asyncio

logger = logging.getLogger(__name__)

router = APIRouter()


# Source management endpoints
@router.post("/sources", response_model=NewsSourceResponse, status_code=status.HTTP_201_CREATED)
async def create_news_source(
    source_data: NewsSourceCreate,
    current_user: User = Depends(require_permission("news", "write")),
    db: Session = Depends(get_db)
):
    """Create a new news source (admin only)."""
    service = get_news_aggregation_service(db)
    source = service.create_source(source_data)
    
    return NewsSourceResponse.from_orm(source)


@router.get("/sources", response_model=List[NewsSourceResponse])
async def list_news_sources(
    source_type: Optional[NewsSourceType] = Query(None),
    is_active: bool = Query(True),
    is_trusted: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """List news sources."""
    service = get_news_aggregation_service(db)
    sources = service.get_sources(source_type, is_active, is_trusted)
    
    return [NewsSourceResponse.from_orm(s) for s in sources]


@router.get("/sources/{source_id}", response_model=NewsSourceResponse)
async def get_news_source(
    source_id: UUID,
    db: Session = Depends(get_db)
):
    """Get news source details."""
    from app.models.news_aggregation import NewsSource
    
    source = db.query(NewsSource).filter(
        NewsSource.id == source_id
    ).first()
    
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News source not found"
        )
    
    return NewsSourceResponse.from_orm(source)


@router.put("/sources/{source_id}", response_model=NewsSourceResponse)
async def update_news_source(
    source_id: UUID,
    source_data: NewsSourceUpdate,
    current_user: User = Depends(require_permission("news", "write")),
    db: Session = Depends(get_db)
):
    """Update news source (admin only)."""
    service = get_news_aggregation_service(db)
    source = service.update_source(source_id, source_data)
    
    return NewsSourceResponse.from_orm(source)


@router.delete("/sources/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news_source(
    source_id: UUID,
    current_user: User = Depends(require_permission("news", "write")),
    db: Session = Depends(get_db)
):
    """Delete news source (admin only)."""
    from app.models.news_aggregation import NewsSource
    
    source = db.query(NewsSource).filter(
        NewsSource.id == source_id
    ).first()
    
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="News source not found"
        )
    
    db.delete(source)
    db.commit()


# Article fetching and management
@router.post("/fetch", response_model=Dict[str, Any])
async def fetch_articles(
    source_id: Optional[UUID] = Body(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: User = Depends(require_permission("news", "write")),
    db: Session = Depends(get_db)
):
    """Trigger article fetching (admin only)."""
    service = get_news_aggregation_service(db)
    
    # Run fetch in background
    async def fetch_task():
        return await service.fetch_articles(source_id)
    
    # For now, run synchronously (in production would use proper async)
    results = asyncio.run(fetch_task())
    
    return results


@router.post("/articles/search", response_model=NewsArticleListResponse)
async def search_articles(
    search_request: NewsSearchRequest,
    db: Session = Depends(get_db)
):
    """Search news articles."""
    service = get_news_aggregation_service(db)
    
    articles, total_count, facets = service.search_articles(search_request)
    
    # Build response
    results = []
    for article in articles:
        response = NewsArticleResponse.from_orm(article)
        response.source_name = article.source.name
        response.source_slug = article.source.slug
        results.append(response)
    
    return NewsArticleListResponse(
        results=results,
        pagination={
            "page": search_request.page,
            "page_size": search_request.page_size,
            "total": total_count,
            "total_pages": (total_count + search_request.page_size - 1) // search_request.page_size
        },
        facets=facets
    )


@router.get("/articles/latest", response_model=List[NewsArticleResponse])
async def get_latest_articles(
    limit: int = Query(20, ge=1, le=100),
    category: Optional[NewsCategory] = Query(None),
    source_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db)
):
    """Get latest news articles."""
    from app.models.news_aggregation import NewsArticle, NewsSource
    
    query = db.query(NewsArticle).join(NewsSource).filter(
        NewsArticle.is_duplicate == False
    )
    
    if category:
        query = query.filter(NewsArticle.categories.contains([category.value]))
    
    if source_id:
        query = query.filter(NewsArticle.source_id == source_id)
    
    articles = query.order_by(
        NewsArticle.published_at.desc()
    ).limit(limit).all()
    
    results = []
    for article in articles:
        response = NewsArticleResponse.from_orm(article)
        response.source_name = article.source.name
        response.source_slug = article.source.slug
        results.append(response)
    
    return results


@router.get("/articles/featured", response_model=List[NewsArticleResponse])
async def get_featured_articles(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get featured news articles."""
    from app.models.news_aggregation import NewsArticle, NewsSource
    
    articles = db.query(NewsArticle).join(NewsSource).filter(
        NewsArticle.is_featured == True,
        NewsArticle.is_duplicate == False
    ).order_by(
        NewsArticle.published_at.desc()
    ).limit(limit).all()
    
    results = []
    for article in articles:
        response = NewsArticleResponse.from_orm(article)
        response.source_name = article.source.name
        response.source_slug = article.source.slug
        results.append(response)
    
    return results


@router.get("/articles/breaking", response_model=List[NewsArticleResponse])
async def get_breaking_news(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get breaking news articles."""
    from app.models.news_aggregation import NewsArticle, NewsSource
    
    articles = db.query(NewsArticle).join(NewsSource).filter(
        NewsArticle.is_breaking == True,
        NewsArticle.is_duplicate == False
    ).order_by(
        NewsArticle.published_at.desc()
    ).limit(limit).all()
    
    results = []
    for article in articles:
        response = NewsArticleResponse.from_orm(article)
        response.source_name = article.source.name
        response.source_slug = article.source.slug
        results.append(response)
    
    return results


@router.get("/articles/{article_id}", response_model=NewsArticleResponse)
async def get_article(
    article_id: UUID,
    db: Session = Depends(get_db)
):
    """Get article details."""
    service = get_news_aggregation_service(db)
    article = service.get_article(article_id)
    
    response = NewsArticleResponse.from_orm(article)
    response.source_name = article.source.name
    response.source_slug = article.source.slug
    
    return response


@router.put("/articles/{article_id}", response_model=NewsArticleResponse)
async def update_article(
    article_id: UUID,
    article_data: NewsArticleUpdate,
    current_user: User = Depends(require_permission("news", "write")),
    db: Session = Depends(get_db)
):
    """Update article (admin only)."""
    from app.models.news_aggregation import NewsArticle
    
    article = db.query(NewsArticle).filter(
        NewsArticle.id == article_id
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    for field, value in article_data.dict(exclude_unset=True).items():
        setattr(article, field, value)
    
    db.commit()
    
    response = NewsArticleResponse.from_orm(article)
    response.source_name = article.source.name
    response.source_slug = article.source.slug
    
    return response


@router.get("/articles/{article_id}/related", response_model=List[RelatedArticleResponse])
async def get_related_articles(
    article_id: UUID,
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get related articles."""
    from app.models.news_aggregation import RelatedArticle
    
    related = db.query(RelatedArticle).filter(
        RelatedArticle.article_id == article_id
    ).order_by(
        RelatedArticle.similarity_score.desc()
    ).limit(limit).all()
    
    results = []
    for rel in related:
        results.append(RelatedArticleResponse(
            article_id=rel.related_article_id,
            article_title=rel.related.title,
            article_url=rel.related.url,
            similarity_score=rel.similarity_score,
            relationship_type=rel.relationship_type
        ))
    
    return results


@router.get("/articles/{article_id}/mentions", response_model=List[ArticleMentionResponse])
async def get_article_mentions(
    article_id: UUID,
    db: Session = Depends(get_db)
):
    """Get entities mentioned in article."""
    from app.models.news_aggregation import ArticleMention
    
    mentions = db.query(ArticleMention).filter(
        ArticleMention.article_id == article_id
    ).all()
    
    return [ArticleMentionResponse.from_orm(m) for m in mentions]


# User interactions
@router.post("/articles/{article_id}/interact")
async def track_article_interaction(
    article_id: UUID,
    interaction_data: ArticleInteractionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Track user interaction with article."""
    service = get_news_aggregation_service(db)
    service.track_interaction(article_id, current_user, interaction_data)
    
    return {"status": "success"}


@router.get("/saved", response_model=List[SavedArticleResponse])
async def get_saved_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's saved articles."""
    service = get_news_aggregation_service(db)
    articles, total_count = service.get_saved_articles(
        current_user, page, page_size
    )
    
    # Get save dates
    from app.models.news_aggregation import ArticleInteraction
    
    results = []
    for article in articles:
        # Get save interaction
        interaction = db.query(ArticleInteraction).filter(
            ArticleInteraction.article_id == article.id,
            ArticleInteraction.user_id == current_user.id,
            ArticleInteraction.interaction_type == "save"
        ).first()
        
        article_response = NewsArticleResponse.from_orm(article)
        article_response.source_name = article.source.name
        article_response.source_slug = article.source.slug
        
        results.append(SavedArticleResponse(
            article=article_response,
            saved_at=interaction.created_at if interaction else article.created_at
        ))
    
    return results


# Topics and trends
@router.get("/topics", response_model=List[NewsTopicResponse])
async def list_topics(
    category: Optional[NewsCategory] = Query(None),
    is_trending: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """List news topics."""
    from app.models.news_aggregation import NewsTopic
    
    query = db.query(NewsTopic)
    
    if category:
        query = query.filter(NewsTopic.category == category)
    
    if is_trending is not None:
        query = query.filter(NewsTopic.is_trending == is_trending)
    
    if is_trending:
        query = query.order_by(NewsTopic.trend_score.desc())
    else:
        query = query.order_by(NewsTopic.name)
    
    topics = query.all()
    
    return [NewsTopicResponse.from_orm(t) for t in topics]


@router.post("/topics", response_model=NewsTopicResponse, status_code=status.HTTP_201_CREATED)
async def create_topic(
    topic_data: NewsTopicCreate,
    current_user: User = Depends(require_permission("news", "write")),
    db: Session = Depends(get_db)
):
    """Create news topic (admin only)."""
    from app.models.news_aggregation import NewsTopic
    
    # Generate slug
    service = get_news_aggregation_service(db)
    slug = service._generate_slug(topic_data.name)
    
    topic = NewsTopic(
        **topic_data.dict(),
        slug=slug
    )
    
    db.add(topic)
    db.commit()
    
    return NewsTopicResponse.from_orm(topic)


@router.get("/topics/trending", response_model=List[NewsTopicResponse])
async def get_trending_topics(
    hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """Get trending topics."""
    service = get_news_aggregation_service(db)
    topics = service.get_trending_topics(hours)
    
    return [NewsTopicResponse.from_orm(t) for t in topics]


# Alerts
@router.post("/alerts", response_model=NewsAlertResponse, status_code=status.HTTP_201_CREATED)
async def create_news_alert(
    alert_data: NewsAlertCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create news alert."""
    service = get_news_aggregation_service(db)
    alert = service.create_alert(alert_data, current_user)
    
    return NewsAlertResponse.from_orm(alert)


@router.get("/alerts", response_model=List[NewsAlertResponse])
async def list_news_alerts(
    is_active: bool = Query(True),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's news alerts."""
    from app.models.news_aggregation import NewsAlert
    
    alerts = db.query(NewsAlert).filter(
        NewsAlert.user_id == current_user.id,
        NewsAlert.is_active == is_active
    ).order_by(NewsAlert.created_at.desc()).all()
    
    return [NewsAlertResponse.from_orm(a) for a in alerts]


@router.put("/alerts/{alert_id}", response_model=NewsAlertResponse)
async def update_news_alert(
    alert_id: UUID,
    alert_data: NewsAlertUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update news alert."""
    from app.models.news_aggregation import NewsAlert
    
    alert = db.query(NewsAlert).filter(
        NewsAlert.id == alert_id,
        NewsAlert.user_id == current_user.id
    ).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    for field, value in alert_data.dict(exclude_unset=True).items():
        setattr(alert, field, value)
    
    db.commit()
    
    return NewsAlertResponse.from_orm(alert)


@router.delete("/alerts/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news_alert(
    alert_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete news alert."""
    from app.models.news_aggregation import NewsAlert
    
    alert = db.query(NewsAlert).filter(
        NewsAlert.id == alert_id,
        NewsAlert.user_id == current_user.id
    ).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    db.delete(alert)
    db.commit()


# Digests
@router.get("/digests", response_model=List[NewsDigestResponse])
async def list_news_digests(
    digest_type: Optional[str] = Query(None, regex="^(daily|weekly|special)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """List news digests."""
    from app.models.news_aggregation import NewsDigest, NewsArticle
    
    query = db.query(NewsDigest).filter(
        NewsDigest.published_at.isnot(None)
    )
    
    if digest_type:
        query = query.filter(NewsDigest.digest_type == digest_type)
    
    if start_date:
        query = query.filter(NewsDigest.digest_date >= start_date)
    
    if end_date:
        query = query.filter(NewsDigest.digest_date <= end_date)
    
    digests = query.order_by(NewsDigest.digest_date.desc()).all()
    
    # Expand featured articles
    results = []
    for digest in digests:
        digest_dict = digest.__dict__.copy()
        
        # Get article details
        if digest.featured_articles:
            articles = db.query(NewsArticle).filter(
                NewsArticle.id.in_(digest.featured_articles)
            ).all()
            
            digest_dict["featured_articles"] = [
                {
                    "id": str(article.id),
                    "title": article.title,
                    "url": article.url,
                    "summary": article.summary
                }
                for article in articles
            ]
        
        results.append(NewsDigestResponse(**digest_dict))
    
    return results


@router.get("/digests/latest", response_model=NewsDigestResponse)
async def get_latest_digest(
    digest_type: str = Query("daily", regex="^(daily|weekly)$"),
    db: Session = Depends(get_db)
):
    """Get latest news digest."""
    from app.models.news_aggregation import NewsDigest, NewsArticle
    
    digest = db.query(NewsDigest).filter(
        NewsDigest.digest_type == digest_type,
        NewsDigest.published_at.isnot(None)
    ).order_by(NewsDigest.digest_date.desc()).first()
    
    if not digest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No digest found"
        )
    
    # Expand featured articles
    digest_dict = digest.__dict__.copy()
    
    if digest.featured_articles:
        articles = db.query(NewsArticle).filter(
            NewsArticle.id.in_(digest.featured_articles)
        ).all()
        
        digest_dict["featured_articles"] = [
            {
                "id": str(article.id),
                "title": article.title,
                "url": article.url,
                "summary": article.summary
            }
            for article in articles
        ]
    
    return NewsDigestResponse(**digest_dict)


@router.post("/digests", response_model=NewsDigestResponse, status_code=status.HTTP_201_CREATED)
async def create_news_digest(
    digest_data: NewsDigestCreate,
    current_user: User = Depends(require_permission("news", "write")),
    db: Session = Depends(get_db)
):
    """Create news digest (admin only)."""
    from app.models.news_aggregation import NewsDigest
    
    digest = NewsDigest(
        **digest_data.dict(),
        total_articles=len(digest_data.featured_articles),
        sources_included=0  # Would calculate from articles
    )
    
    db.add(digest)
    db.commit()
    
    return NewsDigestResponse.from_orm(digest)


# Analytics
@router.get("/analytics", response_model=NewsAnalytics)
async def get_news_analytics(
    period: str = Query("week", regex="^(day|week|month)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: User = Depends(require_permission("news", "read")),
    db: Session = Depends(get_db)
):
    """Get news analytics (admin only)."""
    service = get_news_aggregation_service(db)
    
    # Calculate date range
    if not end_date:
        end_date = datetime.utcnow()
    
    if not start_date:
        if period == "day":
            start_date = end_date - timedelta(days=1)
        elif period == "week":
            start_date = end_date - timedelta(weeks=1)
        else:  # month
            start_date = end_date - timedelta(days=30)
    
    analytics = service.get_analytics(start_date, end_date)
    
    return NewsAnalytics(**analytics)


@router.get("/analytics/sources", response_model=List[SourceMetrics])
async def get_source_metrics(
    metric_type: str = Query("daily", regex="^(daily|weekly|monthly)$"),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(require_permission("news", "read")),
    db: Session = Depends(get_db)
):
    """Get source performance metrics (admin only)."""
    from app.models.news_aggregation import NewsSourceMetrics
    
    # Get latest metrics
    metrics = db.query(NewsSourceMetrics).filter(
        NewsSourceMetrics.metric_type == metric_type
    ).order_by(
        NewsSourceMetrics.metric_date.desc(),
        NewsSourceMetrics.articles_published.desc()
    ).limit(limit).all()
    
    results = []
    for metric in metrics:
        metric_dict = metric.__dict__.copy()
        metric_dict["source_name"] = metric.source.name
        results.append(SourceMetrics(**metric_dict))
    
    return results


# Aggregation status
@router.get("/status", response_model=List[AggregationJobStatus])
async def get_aggregation_status(
    current_user: User = Depends(require_permission("news", "read")),
    db: Session = Depends(get_db)
):
    """Get aggregation job status (admin only)."""
    from app.models.news_aggregation import NewsSource
    
    sources = db.query(NewsSource).filter(
        NewsSource.is_active == True
    ).all()
    
    results = []
    for source in sources:
        # Calculate next run
        if source.last_fetched:
            next_run = source.last_fetched + timedelta(minutes=source.fetch_frequency_minutes)
        else:
            next_run = datetime.utcnow()
        
        # Determine status
        if source.last_error:
            status = "failed"
        elif source.last_fetched and source.last_fetched > datetime.utcnow() - timedelta(minutes=5):
            status = "completed"
        elif next_run <= datetime.utcnow():
            status = "pending"
        else:
            status = "scheduled"
        
        results.append(AggregationJobStatus(
            source_id=source.id,
            source_name=source.name,
            status=status,
            started_at=source.last_fetched,
            completed_at=source.last_fetched,
            articles_fetched=0,  # Would track in real system
            articles_new=0,
            articles_updated=0,
            errors=[source.last_error] if source.last_error else [],
            next_run=next_run
        ))
    
    return results