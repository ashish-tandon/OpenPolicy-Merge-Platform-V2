"""
Core News Aggregation Service

Business logic for news aggregation functionality.
Implements FEAT-020 News Aggregation (P2 priority).
"""

from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import hashlib
import feedparser
import requests
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_, and_, desc, asc
from sqlalchemy.dialects.postgresql import TSVECTOR
from fastapi import HTTPException, status
from app.models.news_aggregation import (
    NewsSource, NewsArticle, RelatedArticle, ArticleMention,
    ArticleInteraction, NewsTopic, NewsDigest, NewsAlert,
    NewsSourceMetrics, NewsSourceType, NewsCategory, NewsSentiment
)
from app.models.users import User
from app.schemas.news_aggregation import (
    NewsSourceCreate, NewsSourceUpdate,
    NewsArticleCreate, NewsArticleUpdate,
    NewsTopicCreate, NewsTopicUpdate,
    NewsDigestCreate, NewsAlertCreate, NewsAlertUpdate,
    NewsSearchRequest, ArticleInteractionCreate
)
from app.core.cache import cache_service
import logging
import re
from collections import defaultdict
from urllib.parse import urlparse
import asyncio

logger = logging.getLogger(__name__)


class NewsAggregationService:
    """Service for managing news aggregation."""
    
    def __init__(self, db: Session):
        self.db = db
        self.processors = {
            NewsSourceType.RSS: self._process_rss_source,
            NewsSourceType.API: self._process_api_source,
            NewsSourceType.PRESS_RELEASE: self._process_press_release_source
        }
    
    # Source management
    def create_source(self, source_data: NewsSourceCreate) -> NewsSource:
        """Create news source."""
        # Generate slug
        slug = self._generate_slug(source_data.name)
        
        # Check for duplicate
        existing = self.db.query(NewsSource).filter(
            or_(
                NewsSource.slug == slug,
                NewsSource.feed_url == source_data.feed_url
            )
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Source with this name or feed URL already exists"
            )
        
        source = NewsSource(
            **source_data.dict(),
            slug=slug
        )
        
        self.db.add(source)
        self.db.commit()
        
        logger.info(f"Created news source: {source.name}")
        return source
    
    def update_source(
        self,
        source_id: UUID,
        source_data: NewsSourceUpdate
    ) -> NewsSource:
        """Update news source."""
        source = self.db.query(NewsSource).filter(
            NewsSource.id == source_id
        ).first()
        
        if not source:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="News source not found"
            )
        
        for field, value in source_data.dict(exclude_unset=True).items():
            setattr(source, field, value)
        
        self.db.commit()
        return source
    
    def get_sources(
        self,
        source_type: Optional[NewsSourceType] = None,
        is_active: bool = True,
        is_trusted: Optional[bool] = None
    ) -> List[NewsSource]:
        """Get news sources."""
        query = self.db.query(NewsSource).filter(
            NewsSource.is_active == is_active
        )
        
        if source_type:
            query = query.filter(NewsSource.source_type == source_type)
        
        if is_trusted is not None:
            query = query.filter(NewsSource.is_trusted == is_trusted)
        
        return query.order_by(NewsSource.name).all()
    
    # Article fetching and processing
    async def fetch_articles(self, source_id: Optional[UUID] = None) -> Dict[str, Any]:
        """Fetch articles from sources."""
        results = {
            "sources_processed": 0,
            "articles_fetched": 0,
            "articles_new": 0,
            "articles_updated": 0,
            "errors": []
        }
        
        # Get sources to process
        query = self.db.query(NewsSource).filter(
            NewsSource.is_active == True
        )
        
        if source_id:
            query = query.filter(NewsSource.id == source_id)
        else:
            # Only fetch sources that are due
            cutoff_time = datetime.utcnow() - timedelta(minutes=1)
            query = query.filter(
                or_(
                    NewsSource.last_fetched.is_(None),
                    NewsSource.last_fetched < cutoff_time
                )
            )
        
        sources = query.all()
        
        for source in sources:
            # Check if it's time to fetch
            if source.last_fetched:
                next_fetch = source.last_fetched + timedelta(minutes=source.fetch_frequency_minutes)
                if next_fetch > datetime.utcnow() and not source_id:
                    continue
            
            try:
                # Process based on source type
                processor = self.processors.get(source.source_type)
                if processor:
                    source_results = await processor(source)
                    results["articles_fetched"] += source_results["fetched"]
                    results["articles_new"] += source_results["new"]
                    results["articles_updated"] += source_results["updated"]
                else:
                    logger.warning(f"No processor for source type: {source.source_type}")
                    results["errors"].append(f"{source.name}: Unsupported source type")
                
                # Update source
                source.last_fetched = datetime.utcnow()
                source.last_error = None
                results["sources_processed"] += 1
                
            except Exception as e:
                logger.error(f"Error fetching from {source.name}: {str(e)}")
                source.last_error = str(e)
                source.error_count += 1
                results["errors"].append(f"{source.name}: {str(e)}")
            
            self.db.commit()
        
        # Post-process articles
        if results["articles_new"] > 0:
            await self._post_process_articles()
        
        return results
    
    async def _process_rss_source(self, source: NewsSource) -> Dict[str, int]:
        """Process RSS feed source."""
        results = {"fetched": 0, "new": 0, "updated": 0}
        
        # Parse RSS feed
        feed = feedparser.parse(source.feed_url)
        
        if feed.bozo:
            raise Exception(f"RSS feed error: {feed.bozo_exception}")
        
        # Process entries
        for entry in feed.entries[:source.max_items_per_fetch]:
            try:
                # Extract article data
                article_data = {
                    "source_id": source.id,
                    "title": entry.get("title", "").strip(),
                    "url": entry.get("link", "").strip(),
                    "published_at": self._parse_date(entry.get("published_parsed")),
                    "summary": self._clean_html(entry.get("summary", "")),
                    "author": entry.get("author", ""),
                }
                
                # Skip if no URL
                if not article_data["url"]:
                    continue
                
                results["fetched"] += 1
                
                # Check if article exists
                existing = self.db.query(NewsArticle).filter(
                    NewsArticle.url == article_data["url"]
                ).first()
                
                if existing:
                    # Update if changed
                    if existing.title != article_data["title"] or \
                       existing.summary != article_data["summary"]:
                        existing.title = article_data["title"]
                        existing.summary = article_data["summary"]
                        existing.updated_at = datetime.utcnow()
                        results["updated"] += 1
                else:
                    # Create new article
                    article = NewsArticle(**article_data)
                    
                    # Generate content hash
                    content = f"{article.title}{article.summary}"
                    article.content_hash = hashlib.sha256(content.encode()).hexdigest()
                    
                    # Basic categorization
                    article.categories = self._categorize_article(article)
                    
                    # Extract entities
                    article.entities = self._extract_entities(article)
                    
                    # Calculate relevance
                    article.relevance_score = self._calculate_relevance(article)
                    
                    # Update search vector
                    article.search_vector = func.to_tsvector('english', f"{article.title} {article.summary}")
                    
                    self.db.add(article)
                    results["new"] += 1
                    
                    # Update source stats
                    source.total_articles += 1
                
            except Exception as e:
                logger.error(f"Error processing RSS entry: {str(e)}")
        
        self.db.flush()
        return results
    
    async def _process_api_source(self, source: NewsSource) -> Dict[str, int]:
        """Process API source."""
        results = {"fetched": 0, "new": 0, "updated": 0}
        
        # Make API request
        headers = source.api_config.get("headers", {}) if source.api_config else {}
        params = source.api_config.get("params", {}) if source.api_config else {}
        
        response = requests.get(
            source.api_endpoint,
            headers=headers,
            params=params,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        
        # Extract articles based on API structure
        articles_data = data
        if source.api_config and "articles_path" in source.api_config:
            # Navigate to articles in response
            path = source.api_config["articles_path"].split(".")
            for key in path:
                articles_data = articles_data.get(key, [])
        
        # Process articles
        for item in articles_data[:source.max_items_per_fetch]:
            # Implementation would depend on specific API structure
            # This is a placeholder
            results["fetched"] += 1
        
        return results
    
    async def _process_press_release_source(self, source: NewsSource) -> Dict[str, int]:
        """Process press release source."""
        # Similar to RSS but might have different structure
        return await self._process_rss_source(source)
    
    # Article search and retrieval
    def search_articles(
        self,
        search_request: NewsSearchRequest
    ) -> Tuple[List[NewsArticle], int, Dict[str, Dict[str, int]]]:
        """Search news articles."""
        query = self.db.query(NewsArticle).join(
            NewsSource
        ).options(
            joinedload(NewsArticle.source),
            joinedload(NewsArticle.mentions),
            joinedload(NewsArticle.related_articles)
        )
        
        # Full-text search
        if search_request.query:
            search_query = func.plainto_tsquery('english', search_request.query)
            query = query.filter(
                NewsArticle.search_vector.match(search_query)
            )
        
        # Filter by sources
        if search_request.sources:
            query = query.filter(NewsArticle.source_id.in_(search_request.sources))
        
        # Filter by categories
        if search_request.categories:
            query = query.filter(
                NewsArticle.categories.contains(
                    [c.value for c in search_request.categories]
                )
            )
        
        # Filter by tags
        if search_request.tags:
            for tag in search_request.tags:
                query = query.filter(NewsArticle.tags.contains([tag]))
        
        # Filter by sentiment
        if search_request.sentiment:
            query = query.filter(NewsArticle.sentiment == search_request.sentiment)
        
        # Date range
        if search_request.start_date:
            query = query.filter(NewsArticle.published_at >= search_request.start_date)
        if search_request.end_date:
            query = query.filter(NewsArticle.published_at <= search_request.end_date)
        
        # Boolean filters
        if search_request.is_featured is not None:
            query = query.filter(NewsArticle.is_featured == search_request.is_featured)
        if search_request.is_breaking is not None:
            query = query.filter(NewsArticle.is_breaking == search_request.is_breaking)
        if search_request.is_verified is not None:
            query = query.filter(NewsArticle.is_verified == search_request.is_verified)
        
        # Relevance filter
        if search_request.min_relevance:
            query = query.filter(NewsArticle.relevance_score >= search_request.min_relevance)
        
        # Filter duplicates
        query = query.filter(NewsArticle.is_duplicate == False)
        
        # Get total count
        total_count = query.count()
        
        # Calculate facets
        facets = self._calculate_facets(query)
        
        # Apply sorting
        if search_request.sort_by == "relevance" and search_request.query:
            # Sort by search relevance
            query = query.order_by(
                desc(func.ts_rank(NewsArticle.search_vector, search_query))
            )
        elif search_request.sort_by == "views":
            query = query.order_by(desc(NewsArticle.view_count))
        elif search_request.sort_by == "shares":
            query = query.order_by(desc(NewsArticle.share_count))
        else:  # published_at
            if search_request.sort_order == "desc":
                query = query.order_by(desc(NewsArticle.published_at))
            else:
                query = query.order_by(asc(NewsArticle.published_at))
        
        # Apply pagination
        offset = (search_request.page - 1) * search_request.page_size
        articles = query.offset(offset).limit(search_request.page_size).all()
        
        return articles, total_count, facets
    
    def get_article(self, article_id: UUID) -> NewsArticle:
        """Get article by ID."""
        article = self.db.query(NewsArticle).options(
            joinedload(NewsArticle.source),
            joinedload(NewsArticle.mentions),
            joinedload(NewsArticle.related_articles).joinedload(RelatedArticle.related)
        ).filter(NewsArticle.id == article_id).first()
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found"
            )
        
        return article
    
    # User interactions
    def track_interaction(
        self,
        article_id: UUID,
        user: User,
        interaction_data: ArticleInteractionCreate
    ) -> None:
        """Track user interaction with article."""
        # Create interaction record
        interaction = ArticleInteraction(
            article_id=article_id,
            user_id=user.id,
            interaction_type=interaction_data.interaction_type,
            interaction_data=interaction_data.interaction_data
        )
        
        self.db.add(interaction)
        
        # Update article stats
        article = self.db.query(NewsArticle).filter(
            NewsArticle.id == article_id
        ).first()
        
        if article:
            if interaction_data.interaction_type == "view":
                article.view_count += 1
            elif interaction_data.interaction_type == "share":
                article.share_count += 1
            elif interaction_data.interaction_type == "save":
                article.save_count += 1
        
        self.db.commit()
    
    def get_saved_articles(
        self,
        user: User,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[NewsArticle], int]:
        """Get user's saved articles."""
        query = self.db.query(NewsArticle).join(
            ArticleInteraction
        ).filter(
            ArticleInteraction.user_id == user.id,
            ArticleInteraction.interaction_type == "save"
        ).options(
            joinedload(NewsArticle.source)
        )
        
        total_count = query.count()
        
        # Order by save date
        query = query.order_by(desc(ArticleInteraction.created_at))
        
        # Pagination
        offset = (page - 1) * page_size
        articles = query.offset(offset).limit(page_size).all()
        
        return articles, total_count
    
    # Topics and trends
    def get_trending_topics(self, hours: int = 24) -> List[NewsTopic]:
        """Get trending topics."""
        # Get topics with high activity
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        topics = self.db.query(NewsTopic).filter(
            NewsTopic.is_trending == True
        ).order_by(
            desc(NewsTopic.trend_score)
        ).limit(10).all()
        
        return topics
    
    def update_trending_topics(self) -> None:
        """Update trending topics based on recent articles."""
        # Calculate topic trends from last 24 hours
        cutoff_24h = datetime.utcnow() - timedelta(hours=24)
        cutoff_7d = datetime.utcnow() - timedelta(days=7)
        
        # Get article counts by category
        category_counts_24h = self.db.query(
            NewsArticle.categories,
            func.count(NewsArticle.id)
        ).filter(
            NewsArticle.published_at >= cutoff_24h
        ).group_by(NewsArticle.categories).all()
        
        # Update topics
        topics = self.db.query(NewsTopic).all()
        
        for topic in topics:
            # Count articles for this topic
            article_count_24h = self.db.query(func.count(NewsArticle.id)).filter(
                NewsArticle.published_at >= cutoff_24h,
                NewsArticle.categories.contains([topic.category.value])
            ).scalar()
            
            article_count_7d = self.db.query(func.count(NewsArticle.id)).filter(
                NewsArticle.published_at >= cutoff_7d,
                NewsArticle.categories.contains([topic.category.value])
            ).scalar()
            
            topic.article_count_24h = article_count_24h
            topic.article_count_7d = article_count_7d
            
            # Calculate trend score (simple algorithm)
            if article_count_7d > 0:
                trend_score = (article_count_24h * 7) / article_count_7d
            else:
                trend_score = float(article_count_24h)
            
            topic.trend_score = trend_score
            topic.is_trending = trend_score > 2.0  # Threshold for trending
            
            if topic.is_trending and not topic.trending_since:
                topic.trending_since = datetime.utcnow()
            elif not topic.is_trending:
                topic.trending_since = None
        
        self.db.commit()
    
    # Alerts
    def create_alert(
        self,
        alert_data: NewsAlertCreate,
        user: User
    ) -> NewsAlert:
        """Create news alert."""
        alert = NewsAlert(
            **alert_data.dict(),
            user_id=user.id
        )
        
        self.db.add(alert)
        self.db.commit()
        
        logger.info(f"Created news alert: {alert.name} for user {user.id}")
        return alert
    
    def check_alerts(self) -> List[Tuple[NewsAlert, List[NewsArticle]]]:
        """Check all active alerts for new matching articles."""
        triggered_alerts = []
        
        # Get active alerts
        alerts = self.db.query(NewsAlert).filter(
            NewsAlert.is_active == True
        ).all()
        
        for alert in alerts:
            # Check based on alert type and frequency
            if not self._should_check_alert(alert):
                continue
            
            # Find matching articles
            matching_articles = self._find_matching_articles(alert)
            
            if matching_articles:
                alert.trigger_count += 1
                alert.last_triggered = datetime.utcnow()
                triggered_alerts.append((alert, matching_articles))
        
        self.db.commit()
        
        return triggered_alerts
    
    # Analytics
    def get_analytics(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Get news analytics."""
        # Total counts
        total_articles = self.db.query(func.count(NewsArticle.id)).filter(
            NewsArticle.published_at >= start_date,
            NewsArticle.published_at <= end_date
        ).scalar()
        
        total_sources = self.db.query(
            func.count(func.distinct(NewsArticle.source_id))
        ).filter(
            NewsArticle.published_at >= start_date,
            NewsArticle.published_at <= end_date
        ).scalar()
        
        # Engagement metrics
        engagement = self.db.query(
            func.sum(NewsArticle.view_count),
            func.sum(NewsArticle.share_count),
            func.sum(NewsArticle.save_count)
        ).filter(
            NewsArticle.published_at >= start_date,
            NewsArticle.published_at <= end_date
        ).first()
        
        # Articles by category
        category_counts = {}
        for category in NewsCategory:
            count = self.db.query(func.count(NewsArticle.id)).filter(
                NewsArticle.published_at >= start_date,
                NewsArticle.published_at <= end_date,
                NewsArticle.categories.contains([category.value])
            ).scalar()
            category_counts[category.value] = count
        
        # Articles by sentiment
        sentiment_counts = {}
        for sentiment in NewsSentiment:
            count = self.db.query(func.count(NewsArticle.id)).filter(
                NewsArticle.published_at >= start_date,
                NewsArticle.published_at <= end_date,
                NewsArticle.sentiment == sentiment
            ).scalar()
            sentiment_counts[sentiment.value] = count
        
        # Get trending topics
        trending_topics = self.get_trending_topics()
        
        return {
            "period": f"{start_date.date()} to {end_date.date()}",
            "total_articles": total_articles,
            "total_sources": total_sources,
            "total_views": engagement[0] or 0,
            "total_shares": engagement[1] or 0,
            "total_saves": engagement[2] or 0,
            "articles_by_category": category_counts,
            "articles_by_sentiment": sentiment_counts,
            "trending_topics": [
                {
                    "name": topic.name,
                    "score": topic.trend_score,
                    "articles_24h": topic.article_count_24h
                }
                for topic in trending_topics
            ]
        }
    
    # Helper methods
    def _generate_slug(self, text: str) -> str:
        """Generate URL-safe slug from text."""
        slug = text.lower().strip()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[\s_-]+', '-', slug)
        slug = re.sub(r'^-+|-+$', '', slug)
        return slug
    
    def _parse_date(self, date_tuple) -> datetime:
        """Parse date from feedparser tuple."""
        if date_tuple:
            try:
                import time
                return datetime.fromtimestamp(time.mktime(date_tuple))
            except:
                pass
        return datetime.utcnow()
    
    def _clean_html(self, text: str) -> str:
        """Clean HTML from text."""
        if not text:
            return ""
        
        # Simple HTML tag removal
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text).strip()
    
    def _categorize_article(self, article: NewsArticle) -> List[str]:
        """Categorize article based on content."""
        categories = []
        content = f"{article.title} {article.summary}".lower()
        
        # Simple keyword-based categorization
        category_keywords = {
            NewsCategory.LEGISLATION: ["bill", "law", "legislation", "act", "amendment"],
            NewsCategory.POLITICS: ["election", "campaign", "party", "leader", "poll"],
            NewsCategory.POLICY: ["policy", "regulation", "reform", "plan", "strategy"],
            NewsCategory.COMMITTEES: ["committee", "testimony", "hearing", "study"],
            NewsCategory.BUDGET: ["budget", "spending", "fiscal", "deficit", "tax"],
            NewsCategory.INTERNATIONAL: ["foreign", "international", "treaty", "trade"],
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in content for keyword in keywords):
                categories.append(category.value)
        
        if not categories:
            categories.append(NewsCategory.GENERAL.value)
        
        return categories
    
    def _extract_entities(self, article: NewsArticle) -> Dict[str, List[str]]:
        """Extract entities from article."""
        entities = {
            "members": [],
            "bills": [],
            "committees": [],
            "parties": []
        }
        
        # This would use NLP in production
        # For now, simple pattern matching
        content = f"{article.title} {article.summary}"
        
        # Extract bill numbers
        bill_pattern = r'\b[CS]-\d{1,4}\b'
        bills = re.findall(bill_pattern, content)
        entities["bills"] = list(set(bills))
        
        return entities
    
    def _calculate_relevance(self, article: NewsArticle) -> float:
        """Calculate article relevance score."""
        score = 0.5  # Base score
        
        # Boost for trusted sources
        if article.source.is_trusted:
            score += 0.2
        
        # Boost for verified articles
        if article.is_verified:
            score += 0.1
        
        # Boost for certain categories
        priority_categories = [NewsCategory.LEGISLATION, NewsCategory.POLICY]
        if any(cat in article.categories for cat in priority_categories):
            score += 0.1
        
        # Penalty for duplicates
        if article.is_duplicate:
            score -= 0.3
        
        return max(0.0, min(1.0, score))
    
    def _calculate_facets(self, query) -> Dict[str, Dict[str, int]]:
        """Calculate faceted search results."""
        facets = {
            "category": defaultdict(int),
            "source": defaultdict(int),
            "sentiment": defaultdict(int)
        }
        
        # This is simplified - in production would be more efficient
        articles = query.limit(1000).all()
        
        for article in articles:
            # Categories
            if article.categories:
                for category in article.categories:
                    facets["category"][category] += 1
            
            # Sources
            facets["source"][article.source.name] += 1
            
            # Sentiment
            facets["sentiment"][article.sentiment.value] += 1
        
        return {k: dict(v) for k, v in facets.items()}
    
    async def _post_process_articles(self) -> None:
        """Post-process new articles."""
        # Find duplicates
        await self._detect_duplicates()
        
        # Find related articles
        await self._find_related_articles()
        
        # Update trending topics
        self.update_trending_topics()
    
    async def _detect_duplicates(self) -> None:
        """Detect duplicate articles."""
        # Get recent articles
        cutoff = datetime.utcnow() - timedelta(hours=24)
        recent_articles = self.db.query(NewsArticle).filter(
            NewsArticle.published_at >= cutoff,
            NewsArticle.is_duplicate == False
        ).all()
        
        # Group by content hash
        hash_groups = defaultdict(list)
        for article in recent_articles:
            if article.content_hash:
                hash_groups[article.content_hash].append(article)
        
        # Mark duplicates
        for hash_value, articles in hash_groups.items():
            if len(articles) > 1:
                # Keep the oldest as original
                articles.sort(key=lambda x: x.published_at)
                original = articles[0]
                
                for duplicate in articles[1:]:
                    duplicate.is_duplicate = True
                    duplicate.duplicate_of_id = original.id
        
        self.db.commit()
    
    async def _find_related_articles(self) -> None:
        """Find related articles."""
        # This would use ML/NLP in production
        # For now, simple implementation based on shared categories
        pass
    
    def _should_check_alert(self, alert: NewsAlert) -> bool:
        """Check if alert should be evaluated."""
        if alert.frequency == "realtime":
            return True
        
        if not alert.last_triggered:
            return True
        
        if alert.frequency == "hourly":
            return alert.last_triggered < datetime.utcnow() - timedelta(hours=1)
        elif alert.frequency == "daily":
            return alert.last_triggered < datetime.utcnow() - timedelta(days=1)
        
        return False
    
    def _find_matching_articles(self, alert: NewsAlert) -> List[NewsArticle]:
        """Find articles matching alert criteria."""
        # Base query for recent articles
        since = alert.last_triggered or datetime.utcnow() - timedelta(days=1)
        query = self.db.query(NewsArticle).filter(
            NewsArticle.published_at > since
        )
        
        # Apply alert filters based on type
        if alert.alert_type == "keyword":
            keywords = alert.alert_config.get("keywords", [])
            if keywords:
                # Search in title and summary
                conditions = []
                for keyword in keywords:
                    conditions.append(
                        or_(
                            NewsArticle.title.ilike(f"%{keyword}%"),
                            NewsArticle.summary.ilike(f"%{keyword}%")
                        )
                    )
                query = query.filter(or_(*conditions))
        
        elif alert.alert_type == "category":
            categories = alert.alert_config.get("categories", [])
            if categories:
                query = query.filter(
                    NewsArticle.categories.overlap(categories)
                )
        
        elif alert.alert_type == "entity":
            entities = alert.alert_config.get("entities", {})
            # Would filter by entities
        
        return query.order_by(desc(NewsArticle.published_at)).limit(10).all()


# Dependency injection helper
def get_news_aggregation_service(db: Session) -> NewsAggregationService:
    """Get news aggregation service instance."""
    return NewsAggregationService(db)