"""
Feature Flags Helper Module

Simple helper functions for using feature flags in application code.
"""

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.feature_flags import get_feature_flag_service
from app.schemas.feature_flags import EvaluationContext
from app.database import SessionLocal
import asyncio


class FeatureFlags:
    """Simple interface for feature flag evaluation."""
    
    @staticmethod
    async def is_enabled(
        feature_name: str,
        context: Optional[Dict[str, Any]] = None,
        db: Optional[Session] = None
    ) -> bool:
        """
        Check if a feature flag is enabled.
        
        Args:
            feature_name: Name of the feature flag
            context: Optional context dictionary
            db: Optional database session
            
        Returns:
            Boolean indicating if feature is enabled
        """
        # Get or create database session
        if db is None:
            db = SessionLocal()
            try:
                return await FeatureFlags._evaluate(feature_name, context, db)
            finally:
                db.close()
        else:
            return await FeatureFlags._evaluate(feature_name, context, db)
    
    @staticmethod
    async def _evaluate(
        feature_name: str,
        context: Optional[Dict[str, Any]],
        db: Session
    ) -> bool:
        """Internal evaluation method."""
        service = get_feature_flag_service(db)
        
        # Convert dict context to EvaluationContext if needed
        eval_context = None
        if context:
            eval_context = EvaluationContext(**context)
        
        return await service.evaluate(feature_name, eval_context)
    
    @staticmethod
    def is_enabled_sync(
        feature_name: str,
        context: Optional[Dict[str, Any]] = None,
        db: Optional[Session] = None
    ) -> bool:
        """
        Synchronous version of is_enabled for non-async code.
        
        Note: This creates a new event loop, so use sparingly.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                FeatureFlags.is_enabled(feature_name, context, db)
            )
        finally:
            loop.close()
    
    @staticmethod
    async def get_all_flags(
        context: Optional[Dict[str, Any]] = None,
        db: Optional[Session] = None
    ) -> Dict[str, bool]:
        """
        Get all feature flags for a given context.
        
        Returns:
            Dictionary mapping feature names to enabled status
        """
        if db is None:
            db = SessionLocal()
            try:
                service = get_feature_flag_service(db)
                eval_context = EvaluationContext(**context) if context else None
                return await service.evaluate_all(eval_context)
            finally:
                db.close()
        else:
            service = get_feature_flag_service(db)
            eval_context = EvaluationContext(**context) if context else None
            return await service.evaluate_all(eval_context)


# Convenience instance
feature_flags = FeatureFlags()


# Decorator for feature flags
def feature_flag(flag_name: str, default: bool = False):
    """
    Decorator to conditionally execute functions based on feature flags.
    
    Usage:
        @feature_flag("new_algorithm")
        async def new_implementation():
            return "new result"
    """
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            # Extract context from kwargs if present
            context = kwargs.get('feature_context', None)
            db = kwargs.get('db', None)
            
            if await feature_flags.is_enabled(flag_name, context, db):
                return await func(*args, **kwargs)
            else:
                return None
        
        def sync_wrapper(*args, **kwargs):
            # Extract context from kwargs if present
            context = kwargs.get('feature_context', None)
            db = kwargs.get('db', None)
            
            if feature_flags.is_enabled_sync(flag_name, context, db):
                return func(*args, **kwargs)
            else:
                return None
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator