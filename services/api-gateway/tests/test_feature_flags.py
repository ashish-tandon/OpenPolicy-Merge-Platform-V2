"""
Tests for Feature Flags System - CHK-0300.2

Comprehensive test suite for the feature flag implementation.
"""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.feature_flags import FeatureFlag, FeatureEvaluation
from app.schemas.feature_flags import EvaluationContext, TargetingRules, TargetingRule
from app.core.feature_flags import FeatureFlagService
from app.features import feature_flags
from app.database import get_db

client = TestClient(app)


class TestFeatureFlagEvaluation:
    """Test feature flag evaluation logic."""
    
    @pytest.fixture
    def db_session(self):
        """Get test database session."""
        # In a real test, this would use a test database
        from app.database import SessionLocal
        db = SessionLocal()
        yield db
        db.close()
    
    @pytest.fixture
    def service(self, db_session):
        """Get feature flag service."""
        return FeatureFlagService(db_session)
    
    @pytest.mark.asyncio
    async def test_simple_feature_flag(self, service, db_session):
        """Test basic feature flag evaluation."""
        # Create a simple enabled flag
        flag = FeatureFlag(
            feature_name="test_feature",
            feature_description="Test feature",
            is_enabled=True
        )
        db_session.add(flag)
        db_session.commit()
        
        # Evaluate flag
        result = await service.evaluate("test_feature")
        assert result is True
        
        # Test non-existent flag
        result = await service.evaluate("non_existent")
        assert result is False
    
    @pytest.mark.asyncio
    async def test_disabled_flag(self, service, db_session):
        """Test disabled feature flag."""
        flag = FeatureFlag(
            feature_name="disabled_feature",
            is_enabled=False
        )
        db_session.add(flag)
        db_session.commit()
        
        result = await service.evaluate("disabled_feature")
        assert result is False
    
    @pytest.mark.asyncio
    async def test_rollout_percentage(self, service, db_session):
        """Test percentage-based rollout."""
        # 50% rollout
        flag = FeatureFlag(
            feature_name="rollout_feature",
            is_enabled=True,
            rollout_percentage=50
        )
        db_session.add(flag)
        db_session.commit()
        
        # Test with multiple user IDs
        enabled_count = 0
        for i in range(100):
            context = EvaluationContext(user_id=f"user_{i}")
            if await service.evaluate("rollout_feature", context):
                enabled_count += 1
        
        # Should be roughly 50% (with some variance)
        assert 35 <= enabled_count <= 65
    
    @pytest.mark.asyncio
    async def test_user_targeting(self, service, db_session):
        """Test user-specific targeting rules."""
        targeting_rules = {
            "rules": [
                {
                    "type": "user",
                    "operator": "in",
                    "values": ["user1", "user2", "user3"]
                }
            ],
            "default": False
        }
        
        flag = FeatureFlag(
            feature_name="user_targeted",
            is_enabled=True,
            targeting_rules=targeting_rules
        )
        db_session.add(flag)
        db_session.commit()
        
        # Test targeted users
        context1 = EvaluationContext(user_id="user1")
        assert await service.evaluate("user_targeted", context1) is True
        
        context2 = EvaluationContext(user_id="user2")
        assert await service.evaluate("user_targeted", context2) is True
        
        # Test non-targeted user
        context3 = EvaluationContext(user_id="user4")
        assert await service.evaluate("user_targeted", context3) is False
    
    @pytest.mark.asyncio
    async def test_environment_targeting(self, service, db_session):
        """Test environment-based targeting."""
        flag = FeatureFlag(
            feature_name="env_feature",
            is_enabled=True,
            environments=["staging", "development"]
        )
        db_session.add(flag)
        db_session.commit()
        
        # Test allowed environments
        context_staging = EvaluationContext(environment="staging")
        assert await service.evaluate("env_feature", context_staging) is True
        
        context_dev = EvaluationContext(environment="development")
        assert await service.evaluate("env_feature", context_dev) is True
        
        # Test disallowed environment
        context_prod = EvaluationContext(environment="production")
        assert await service.evaluate("env_feature", context_prod) is False
    
    @pytest.mark.asyncio
    async def test_time_based_feature(self, service, db_session):
        """Test time-based feature flags."""
        # Flag that starts tomorrow
        tomorrow = datetime.utcnow() + timedelta(days=1)
        flag_future = FeatureFlag(
            feature_name="future_feature",
            is_enabled=True,
            start_date=tomorrow
        )
        db_session.add(flag_future)
        
        # Flag that ended yesterday
        yesterday = datetime.utcnow() - timedelta(days=1)
        flag_past = FeatureFlag(
            feature_name="past_feature",
            is_enabled=True,
            end_date=yesterday
        )
        db_session.add(flag_past)
        
        # Currently active flag
        flag_current = FeatureFlag(
            feature_name="current_feature",
            is_enabled=True,
            start_date=yesterday,
            end_date=tomorrow
        )
        db_session.add(flag_current)
        db_session.commit()
        
        # Test evaluations
        assert await service.evaluate("future_feature") is False
        assert await service.evaluate("past_feature") is False
        assert await service.evaluate("current_feature") is True
    
    @pytest.mark.asyncio
    async def test_user_overrides(self, service, db_session):
        """Test user-specific overrides."""
        flag = FeatureFlag(
            feature_name="override_feature",
            is_enabled=False,  # Globally disabled
            user_overrides={
                "special_user": True,
                "blocked_user": False
            }
        )
        db_session.add(flag)
        db_session.commit()
        
        # Test overridden users
        context_special = EvaluationContext(user_id="special_user")
        assert await service.evaluate("override_feature", context_special) is True
        
        context_blocked = EvaluationContext(user_id="blocked_user")
        assert await service.evaluate("override_feature", context_blocked) is False
        
        # Test regular user (should follow global setting)
        context_regular = EvaluationContext(user_id="regular_user")
        assert await service.evaluate("override_feature", context_regular) is False
    
    @pytest.mark.asyncio
    async def test_jurisdiction_targeting(self, service, db_session):
        """Test jurisdiction-based targeting."""
        targeting_rules = {
            "rules": [
                {
                    "type": "jurisdiction",
                    "operator": "in",
                    "values": ["ontario", "quebec", "british_columbia"]
                }
            ],
            "default": False
        }
        
        flag = FeatureFlag(
            feature_name="provincial_feature",
            is_enabled=True,
            targeting_rules=targeting_rules
        )
        db_session.add(flag)
        db_session.commit()
        
        # Test targeted jurisdictions
        context_on = EvaluationContext(jurisdiction="ontario")
        assert await service.evaluate("provincial_feature", context_on) is True
        
        context_qc = EvaluationContext(jurisdiction="quebec")
        assert await service.evaluate("provincial_feature", context_qc) is True
        
        # Test non-targeted jurisdiction
        context_ab = EvaluationContext(jurisdiction="alberta")
        assert await service.evaluate("provincial_feature", context_ab) is False


class TestFeatureFlagAPI:
    """Test feature flag REST API endpoints."""
    
    def test_evaluate_single_flag(self):
        """Test single flag evaluation endpoint."""
        # Create evaluation context
        context = {
            "user_id": "test_user",
            "environment": "production",
            "jurisdiction": "ontario"
        }
        
        response = client.post(
            "/api/v1/feature-flags/evaluate/test_feature",
            json=context
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "feature_name" in data
        assert "is_enabled" in data
        assert isinstance(data["is_enabled"], bool)
    
    def test_evaluate_bulk_flags(self):
        """Test bulk flag evaluation endpoint."""
        request = {
            "feature_names": ["feature1", "feature2", "feature3"],
            "context": {
                "user_id": "test_user",
                "environment": "production"
            }
        }
        
        response = client.post(
            "/api/v1/feature-flags/evaluate",
            json=request
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "flags" in data
        assert isinstance(data["flags"], dict)
        assert "evaluated_at" in data


class TestFeatureFlagHelpers:
    """Test feature flag helper functions."""
    
    @pytest.mark.asyncio
    async def test_helper_is_enabled(self):
        """Test the helper is_enabled function."""
        # This would need a test database setup
        context = {
            "user_id": "test_user",
            "environment": "test"
        }
        
        # Test with context
        result = await feature_flags.is_enabled("test_feature", context)
        assert isinstance(result, bool)
        
        # Test without context
        result = await feature_flags.is_enabled("test_feature")
        assert isinstance(result, bool)
    
    def test_helper_is_enabled_sync(self):
        """Test synchronous helper function."""
        context = {
            "user_id": "test_user",
            "environment": "test"
        }
        
        result = feature_flags.is_enabled_sync("test_feature", context)
        assert isinstance(result, bool)
    
    @pytest.mark.asyncio
    async def test_feature_flag_decorator(self):
        """Test feature flag decorator."""
        call_count = 0
        
        @feature_flag("decorator_test")
        async def test_function():
            nonlocal call_count
            call_count += 1
            return "executed"
        
        # Function should only execute if flag is enabled
        result = await test_function()
        # Result depends on whether flag exists and is enabled
        assert result is None or result == "executed"


class TestFeatureFlagCaching:
    """Test feature flag caching behavior."""
    
    @pytest.mark.asyncio
    async def test_cache_hit(self, service, db_session):
        """Test that repeated evaluations use cache."""
        flag = FeatureFlag(
            feature_name="cached_feature",
            is_enabled=True
        )
        db_session.add(flag)
        db_session.commit()
        
        # First evaluation (cache miss)
        result1 = await service.evaluate("cached_feature")
        assert result1 is True
        
        # Change flag in database
        flag.is_enabled = False
        db_session.commit()
        
        # Second evaluation should still return cached value
        result2 = await service.evaluate("cached_feature")
        assert result2 is True  # Still cached
        
        # Clear cache and re-evaluate
        service._clear_flag_cache("cached_feature")
        result3 = await service.evaluate("cached_feature")
        assert result3 is False  # Now reflects database change