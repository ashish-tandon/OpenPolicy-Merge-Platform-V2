"""
News Aggregation System

Revision ID: 013_news_aggregation_system
Revises: 012_email_notification_system
Create Date: 2025-08-24 01:00:00

Implements FEAT-020 News Aggregation (P2 priority).
Creates tables for comprehensive news aggregation and management.
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '013_news_aggregation_system'
down_revision = '012_email_notification_system'
branch_labels = None
depends_on = None


def upgrade():
    """Create news aggregation tables."""
    
    # Create news_sources table
    op.create_table(
        'news_sources',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('slug', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('website_url', sa.String(500), nullable=False),
        sa.Column('logo_url', sa.String(500), nullable=True),
        sa.Column('source_type', sa.Enum('rss', 'api', 'scraper', 'twitter', 'press_release', 'manual', name='newssourcetype'), nullable=False),
        sa.Column('feed_url', sa.String(500), nullable=True),
        sa.Column('api_endpoint', sa.String(500), nullable=True),
        sa.Column('api_config', postgresql.JSONB(), nullable=True),
        sa.Column('language', sa.String(10), server_default='en', nullable=False),
        sa.Column('country', sa.String(2), server_default='CA', nullable=False),
        sa.Column('province', sa.String(2), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('is_trusted', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_partisan', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('political_leaning', sa.String(20), nullable=True),
        sa.Column('fetch_frequency_minutes', sa.Integer(), server_default='60', nullable=False),
        sa.Column('max_items_per_fetch', sa.Integer(), server_default='50', nullable=False),
        sa.Column('reliability_score', sa.Float(), server_default='0.5', nullable=False),
        sa.Column('accuracy_score', sa.Float(), server_default='0.5', nullable=False),
        sa.Column('total_articles', sa.Integer(), server_default='0', nullable=False),
        sa.Column('last_fetched', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_error', sa.Text(), nullable=True),
        sa.Column('error_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )
    
    # Create indexes for news_sources
    op.create_index('idx_source_slug', 'news_sources', ['slug'])
    op.create_index('idx_source_type', 'news_sources', ['source_type'])
    op.create_index('idx_source_active', 'news_sources', ['is_active'])
    op.create_index('idx_source_trusted', 'news_sources', ['is_trusted'])
    
    # Create news_articles table
    op.create_table(
        'news_articles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('url', sa.String(1000), nullable=False),
        sa.Column('author', sa.String(200), nullable=True),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('content_hash', sa.String(64), nullable=True),
        sa.Column('image_url', sa.String(1000), nullable=True),
        sa.Column('video_url', sa.String(1000), nullable=True),
        sa.Column('categories', postgresql.JSONB(), nullable=True),
        sa.Column('tags', postgresql.JSONB(), nullable=True),
        sa.Column('entities', postgresql.JSONB(), nullable=True),
        sa.Column('relevance_score', sa.Float(), server_default='0.5', nullable=False),
        sa.Column('sentiment', sa.Enum('positive', 'negative', 'neutral', 'mixed', name='newssentiment'), server_default='neutral', nullable=False),
        sa.Column('sentiment_score', sa.Float(), nullable=True),
        sa.Column('view_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('share_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('save_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('search_vector', postgresql.TSVECTOR(), nullable=True),
        sa.Column('is_featured', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_breaking', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_verified', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_duplicate', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('duplicate_of_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['source_id'], ['news_sources.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('url')
    )
    
    # Create indexes for news_articles
    op.create_index('idx_article_source', 'news_articles', ['source_id'])
    op.create_index('idx_article_published', 'news_articles', ['published_at'])
    op.create_index('idx_article_relevance', 'news_articles', ['relevance_score'])
    op.create_index('idx_article_featured', 'news_articles', ['is_featured'])
    op.create_index('idx_article_breaking', 'news_articles', ['is_breaking'])
    op.create_index('idx_article_search', 'news_articles', ['search_vector'], postgresql_using='gin')
    op.create_index('idx_article_url_hash', 'news_articles', ['content_hash'])
    
    # Create related_articles table
    op.create_table(
        'related_articles',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('article_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('related_article_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('similarity_score', sa.Float(), nullable=False),
        sa.Column('relationship_type', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['article_id'], ['news_articles.id'], ),
        sa.ForeignKeyConstraint(['related_article_id'], ['news_articles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for related_articles
    op.create_index('idx_related_article', 'related_articles', ['article_id'])
    op.create_index('idx_related_related', 'related_articles', ['related_article_id'])
    op.create_index('idx_related_similarity', 'related_articles', ['similarity_score'])
    
    # Create article_mentions table
    op.create_table(
        'article_mentions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('article_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('entity_type', sa.String(50), nullable=False),
        sa.Column('entity_id', sa.String(100), nullable=False),
        sa.Column('entity_name', sa.String(200), nullable=False),
        sa.Column('mention_count', sa.Integer(), server_default='1', nullable=False),
        sa.Column('sentiment', sa.Enum('positive', 'negative', 'neutral', 'mixed', name='newssentiment'), nullable=True),
        sa.Column('context', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['article_id'], ['news_articles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for article_mentions
    op.create_index('idx_mention_article', 'article_mentions', ['article_id'])
    op.create_index('idx_mention_entity', 'article_mentions', ['entity_type', 'entity_id'])
    
    # Create article_interactions table
    op.create_table(
        'article_interactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('article_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('interaction_type', sa.String(20), nullable=False),
        sa.Column('interaction_data', postgresql.JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['article_id'], ['news_articles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for article_interactions
    op.create_index('idx_interaction_article', 'article_interactions', ['article_id'])
    op.create_index('idx_interaction_user', 'article_interactions', ['user_id'])
    op.create_index('idx_interaction_type', 'article_interactions', ['interaction_type'])
    op.create_index('idx_interaction_created', 'article_interactions', ['created_at'])
    
    # Create news_topics table
    op.create_table(
        'news_topics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('slug', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.Enum('legislation', 'politics', 'policy', 'committees', 'elections', 'budget', 'international', 'provincial', 'municipal', 'opinion', 'analysis', 'general', name='newscategory'), nullable=False),
        sa.Column('keywords', postgresql.JSONB(), nullable=True),
        sa.Column('is_trending', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('trend_score', sa.Float(), server_default='0.0', nullable=False),
        sa.Column('article_count_24h', sa.Integer(), server_default='0', nullable=False),
        sa.Column('article_count_7d', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.Column('trending_since', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug')
    )
    
    # Create indexes for news_topics
    op.create_index('idx_topic_slug', 'news_topics', ['slug'])
    op.create_index('idx_topic_trending', 'news_topics', ['is_trending', 'trend_score'])
    op.create_index('idx_topic_category', 'news_topics', ['category'])
    
    # Create news_digests table
    op.create_table(
        'news_digests',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('digest_type', sa.String(20), nullable=False),
        sa.Column('digest_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('featured_articles', postgresql.JSONB(), nullable=False),
        sa.Column('topic_summaries', postgresql.JSONB(), nullable=True),
        sa.Column('trending_topics', postgresql.JSONB(), nullable=True),
        sa.Column('total_articles', sa.Integer(), server_default='0', nullable=False),
        sa.Column('sources_included', sa.Integer(), server_default='0', nullable=False),
        sa.Column('email_sent', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('email_sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('email_recipients', sa.Integer(), server_default='0', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for news_digests
    op.create_index('idx_digest_type', 'news_digests', ['digest_type'])
    op.create_index('idx_digest_date', 'news_digests', ['digest_date'])
    op.create_index('idx_digest_published', 'news_digests', ['published_at'])
    
    # Create news_alerts table
    op.create_table(
        'news_alerts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('alert_type', sa.String(50), nullable=False),
        sa.Column('alert_config', postgresql.JSONB(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('notification_channels', postgresql.JSONB(), nullable=False),
        sa.Column('frequency', sa.String(20), server_default='realtime', nullable=False),
        sa.Column('trigger_count', sa.Integer(), server_default='0', nullable=False),
        sa.Column('last_triggered', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for news_alerts
    op.create_index('idx_alert_user', 'news_alerts', ['user_id'])
    op.create_index('idx_alert_active', 'news_alerts', ['is_active'])
    op.create_index('idx_alert_type', 'news_alerts', ['alert_type'])
    
    # Create news_source_metrics table
    op.create_table(
        'news_source_metrics',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('metric_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('metric_type', sa.String(20), nullable=False),
        sa.Column('articles_published', sa.Integer(), server_default='0', nullable=False),
        sa.Column('articles_featured', sa.Integer(), server_default='0', nullable=False),
        sa.Column('total_views', sa.Integer(), server_default='0', nullable=False),
        sa.Column('total_shares', sa.Integer(), server_default='0', nullable=False),
        sa.Column('avg_relevance_score', sa.Float(), nullable=True),
        sa.Column('avg_sentiment_score', sa.Float(), nullable=True),
        sa.Column('duplicate_rate', sa.Float(), nullable=True),
        sa.Column('error_rate', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['source_id'], ['news_sources.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for news_source_metrics
    op.create_index('idx_metric_source', 'news_source_metrics', ['source_id'])
    op.create_index('idx_metric_date', 'news_source_metrics', ['metric_date'])
    op.create_index('idx_metric_type', 'news_source_metrics', ['metric_type'])
    
    # Insert default news sources
    from sqlalchemy.sql import table, column
    import uuid
    
    sources_table = table(
        'news_sources',
        column('id', postgresql.UUID),
        column('name', sa.String),
        column('slug', sa.String),
        column('description', sa.Text),
        column('website_url', sa.String),
        column('source_type', sa.String),
        column('feed_url', sa.String),
        column('is_trusted', sa.Boolean),
        column('is_partisan', sa.Boolean),
        column('political_leaning', sa.String)
    )
    
    default_sources = [
        {
            'id': uuid.uuid4(),
            'name': 'CBC News - Politics',
            'slug': 'cbc-news-politics',
            'description': 'Canadian Broadcasting Corporation political news',
            'website_url': 'https://www.cbc.ca/news/politics',
            'source_type': 'rss',
            'feed_url': 'https://www.cbc.ca/cmlink/rss-politics',
            'is_trusted': True,
            'is_partisan': False,
            'political_leaning': None
        },
        {
            'id': uuid.uuid4(),
            'name': 'Global News - Politics',
            'slug': 'global-news-politics',
            'description': 'Global News Canadian politics coverage',
            'website_url': 'https://globalnews.ca/politics/',
            'source_type': 'rss',
            'feed_url': 'https://globalnews.ca/politics/feed/',
            'is_trusted': True,
            'is_partisan': False,
            'political_leaning': None
        },
        {
            'id': uuid.uuid4(),
            'name': 'CTV News - Politics',
            'slug': 'ctv-news-politics',
            'description': 'CTV News political coverage',
            'website_url': 'https://www.ctvnews.ca/politics',
            'source_type': 'rss',
            'feed_url': 'https://www.ctvnews.ca/rss/Politics',
            'is_trusted': True,
            'is_partisan': False,
            'political_leaning': None
        },
        {
            'id': uuid.uuid4(),
            'name': 'The Globe and Mail - Politics',
            'slug': 'globe-mail-politics',
            'description': 'The Globe and Mail political news',
            'website_url': 'https://www.theglobeandmail.com/politics/',
            'source_type': 'rss',
            'feed_url': 'https://www.theglobeandmail.com/arc/outboundfeeds/rss/category/politics/',
            'is_trusted': True,
            'is_partisan': False,
            'political_leaning': 'center'
        },
        {
            'id': uuid.uuid4(),
            'name': 'National Post - Politics',
            'slug': 'national-post-politics',
            'description': 'National Post political coverage',
            'website_url': 'https://nationalpost.com/category/news/politics/',
            'source_type': 'rss',
            'feed_url': 'https://nationalpost.com/category/news/politics/feed',
            'is_trusted': True,
            'is_partisan': False,
            'political_leaning': 'center-right'
        },
        {
            'id': uuid.uuid4(),
            'name': 'Parliament of Canada - Press Releases',
            'slug': 'parliament-press-releases',
            'description': 'Official press releases from Parliament',
            'website_url': 'https://www.parl.ca/',
            'source_type': 'press_release',
            'feed_url': 'https://www.parl.ca/rss/press-releases.xml',
            'is_trusted': True,
            'is_partisan': False,
            'political_leaning': None
        }
    ]
    
    op.bulk_insert(sources_table, default_sources)
    
    # Insert default topics
    topics_table = table(
        'news_topics',
        column('id', postgresql.UUID),
        column('name', sa.String),
        column('slug', sa.String),
        column('description', sa.Text),
        column('category', sa.String),
        column('keywords', postgresql.JSONB)
    )
    
    default_topics = [
        {
            'id': uuid.uuid4(),
            'name': 'Federal Legislation',
            'slug': 'federal-legislation',
            'description': 'News about federal bills and laws',
            'category': 'legislation',
            'keywords': ['bill', 'act', 'legislation', 'law', 'amendment']
        },
        {
            'id': uuid.uuid4(),
            'name': 'Elections & Campaigns',
            'slug': 'elections-campaigns',
            'description': 'Electoral news and campaign coverage',
            'category': 'elections',
            'keywords': ['election', 'campaign', 'candidate', 'poll', 'vote']
        },
        {
            'id': uuid.uuid4(),
            'name': 'Budget & Finance',
            'slug': 'budget-finance',
            'description': 'Federal budget and fiscal policy news',
            'category': 'budget',
            'keywords': ['budget', 'fiscal', 'spending', 'tax', 'deficit', 'economy']
        },
        {
            'id': uuid.uuid4(),
            'name': 'Climate Policy',
            'slug': 'climate-policy',
            'description': 'Climate change and environmental policy',
            'category': 'policy',
            'keywords': ['climate', 'environment', 'carbon', 'emissions', 'green']
        },
        {
            'id': uuid.uuid4(),
            'name': 'Healthcare Policy',
            'slug': 'healthcare-policy',
            'description': 'Healthcare system and policy news',
            'category': 'policy',
            'keywords': ['healthcare', 'health', 'medical', 'hospital', 'doctor']
        }
    ]
    
    op.bulk_insert(topics_table, default_topics)


def downgrade():
    """Drop news aggregation tables."""
    
    # Drop tables in reverse order due to foreign key constraints
    op.drop_index('idx_metric_type', table_name='news_source_metrics')
    op.drop_index('idx_metric_date', table_name='news_source_metrics')
    op.drop_index('idx_metric_source', table_name='news_source_metrics')
    op.drop_table('news_source_metrics')
    
    op.drop_index('idx_alert_type', table_name='news_alerts')
    op.drop_index('idx_alert_active', table_name='news_alerts')
    op.drop_index('idx_alert_user', table_name='news_alerts')
    op.drop_table('news_alerts')
    
    op.drop_index('idx_digest_published', table_name='news_digests')
    op.drop_index('idx_digest_date', table_name='news_digests')
    op.drop_index('idx_digest_type', table_name='news_digests')
    op.drop_table('news_digests')
    
    op.drop_index('idx_topic_category', table_name='news_topics')
    op.drop_index('idx_topic_trending', table_name='news_topics')
    op.drop_index('idx_topic_slug', table_name='news_topics')
    op.drop_table('news_topics')
    
    op.drop_index('idx_interaction_created', table_name='article_interactions')
    op.drop_index('idx_interaction_type', table_name='article_interactions')
    op.drop_index('idx_interaction_user', table_name='article_interactions')
    op.drop_index('idx_interaction_article', table_name='article_interactions')
    op.drop_table('article_interactions')
    
    op.drop_index('idx_mention_entity', table_name='article_mentions')
    op.drop_index('idx_mention_article', table_name='article_mentions')
    op.drop_table('article_mentions')
    
    op.drop_index('idx_related_similarity', table_name='related_articles')
    op.drop_index('idx_related_related', table_name='related_articles')
    op.drop_index('idx_related_article', table_name='related_articles')
    op.drop_table('related_articles')
    
    op.drop_index('idx_article_url_hash', table_name='news_articles')
    op.drop_index('idx_article_search', table_name='news_articles')
    op.drop_index('idx_article_breaking', table_name='news_articles')
    op.drop_index('idx_article_featured', table_name='news_articles')
    op.drop_index('idx_article_relevance', table_name='news_articles')
    op.drop_index('idx_article_published', table_name='news_articles')
    op.drop_index('idx_article_source', table_name='news_articles')
    op.drop_table('news_articles')
    
    op.drop_index('idx_source_trusted', table_name='news_sources')
    op.drop_index('idx_source_active', table_name='news_sources')
    op.drop_index('idx_source_type', table_name='news_sources')
    op.drop_index('idx_source_slug', table_name='news_sources')
    op.drop_table('news_sources')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS newssourcetype')
    op.execute('DROP TYPE IF EXISTS newscategory')
    op.execute('DROP TYPE IF EXISTS newssentiment')