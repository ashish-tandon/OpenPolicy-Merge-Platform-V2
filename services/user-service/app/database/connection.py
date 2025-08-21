"""
Database connection and session management for User Service.

Uses async SQLAlchemy with PostgreSQL.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Create async engine
engine = create_async_engine(
    settings.USER_DATABASE_URL,
    echo=settings.DEBUG,
    poolclass=NullPool,  # Use NullPool for development
    future=True
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session() -> AsyncSession:
    """Get async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables."""
    try:
        from app.models.user import Base as UserBase
        from app.models.user_engagement import Base as EngagementBase
        
        # Import all models to ensure they're registered
        import app.models.user
        import app.models.user_engagement
        
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(UserBase.metadata.create_all)
            await conn.run_sync(EngagementBase.metadata.create_all)
        
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def close_db():
    """Close database connections."""
    await engine.dispose()
    logger.info("Database connections closed")

