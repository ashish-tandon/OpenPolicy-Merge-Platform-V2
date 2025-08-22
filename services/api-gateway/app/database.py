"""
Database connection and session management for the OpenPolicy API Gateway.

Uses SQLAlchemy with async support and Alembic for migrations.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Create database engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db() -> Session:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables."""
    try:
        # Import models to ensure they're registered
        from app.models import parliamentary_entities, users, user_sessions, entity_audit_log, data_sources, sync_status
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Insert initial data sources if they don't exist
        db = SessionLocal()
        try:
            from app.models.data_sources import DataSource
            from app.models.sync_status import SyncStatus
            
            # Check if data sources exist
            if db.query(DataSource).count() == 0:
                initial_sources = [
                    DataSource(
                        name="OpenParliament",
                        type="parliamentary",
                        config={"base_url": "https://openparliament.ca", "api_version": "v1"},
                        is_active=True
                    ),
                    DataSource(
                        name="Municipal Scrapers",
                        type="municipal",
                        config={"scrapers": ["ca_on_toronto", "ca_on_ottawa", "ca_bc_vancouver"]},
                        is_active=True
                    ),
                    DataSource(
                        name="Civic Scraper",
                        type="civic",
                        config={"base_url": "https://civicdata.io", "api_version": "v2"},
                        is_active=True
                    )
                ]
                db.add_all(initial_sources)
                db.commit()
                logger.info("Initial data sources created")
            
            # Check if sync status exists
            if db.query(SyncStatus).count() == 0:
                initial_sync = SyncStatus(
                    source_name="OpenParliament",
                    last_sync="2024-01-01T00:00:00Z",
                    status="pending",
                    records_processed=0
                )
                db.add(initial_sync)
                db.commit()
                logger.info("Initial sync status created")
                
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

def check_db_connection() -> bool:
    """Check if database connection is working."""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False
