"""
Database connection and session management for the OpenPolicy API Gateway.

Uses SQLAlchemy with async support and Alembic for migrations.
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import settings

# Database engine
if settings.ENV == "test":
    # Use in-memory SQLite for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # Use PostgreSQL for development and production
    # SQLAlchemy 2.x with psycopg2
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.DEBUG,
        # Force use of psycopg2
        connect_args={"sslmode": "prefer"}
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Create metadata for schema management
metadata = MetaData()


def get_db():
    """
    Dependency to get database session.
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    # Import all models to ensure they're registered
    from app.models.openparliament import (
        Politician, Party, Riding, ElectedMember, Bill, VoteQuestion, 
        MemberVote, PartyVote, Statement
    )
    
    # Create tables in the public schema (they already exist from the restore)
    # This is just to ensure models are registered with SQLAlchemy
    Base.metadata.create_all(bind=engine)


def close_db():
    """Close database connections."""
    engine.dispose()
