"""
Unified Feature Flag Service

This service consolidates the PWA feature flags and API version flags
into a single, powerful feature flag system with targeting, rollouts,
and A/B testing capabilities.
"""

import json
import logging
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from redis import Redis

from app.models.pwa_system import PWAFeature
from app.core.cache import cache_manager

logger = logging.getLogger(__name__)

class FeatureFlagType(Enum):
    RELEASE = "release"  # Standard feature toggle
    EXPERIMENT = "experiment"  # A/B test
    OPERATIONAL = "operational"  # Kill switch
    PERMISSION = "permission"  # User permission based

class TargetingRuleType(Enum):
    USER = "user"
    PERCENTAGE = "percentage"
    JURISDICTION = "jurisdiction"
    ROLE = "role"
    DATE_RANGE = "date_range"
    CUSTOM = "custom"

class UnifiedFeatureFlagService:
    """
    Unified service that combines:
    1. PWA database-backed feature flags
    2. API version code-based flags
    3. New targeting and rollout capabilities
    """
    
    def __init__(self, db: Session, redis: Optional[Redis] = None):
        self.db = db
        self.redis = redis or cache_manager.get_redis()
        self._cache_ttl = 300  # 5 minutes
        
        # Migrate hardcoded API version flags
        self._legacy_flags = {
            "v2_pagination": True,
            "v2_graphql": True,
            "v2_websocket": False,
            "v3_ai_summaries": False
        }
        
    async def evaluate(
        self, 
        flag_name: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Evaluate a feature flag with optional context
        
        Args:
            flag_name: Name of the feature flag
            context: Evaluation context (user_id, jurisdiction, etc.)
            
        Returns:
            Boolean indicating if feature is enabled
        """
        context = context or {}
        
        # Check cache first
        cache_key = self._get_cache_key(flag_name, context)
        cached = await self._get_cached_evaluation(cache_key)
        if cached is not None:
            return cached
            
        # Check legacy hardcoded flags
        if flag_name in self._legacy_flags:
            result = self._legacy_flags[flag_name]
            await self._cache_evaluation(cache_key, result)
            return result
            
        # Load flag from database
        flag = self._get_flag(flag_name)
        if not flag:
            logger.warning(f"Feature flag not found: {flag_name}")
            return False
            
        # Evaluate flag
        result = self._evaluate_flag(flag, context)
        
        # Cache result
        await self._cache_evaluation(cache_key, result)
        
        # Track evaluation for analytics
        await self._track_evaluation(flag_name, context, result)
        
        return result
        
    def _get_flag(self, flag_name: str) -> Optional[PWAFeature]:
        """Get feature flag from database"""
        return self.db.query(PWAFeature).filter(
            PWAFeature.feature_name == flag_name
        ).first()
        
    def _evaluate_flag(
        self, 
        flag: PWAFeature, 
        context: Dict[str, Any]
    ) -> bool:
        """
        Evaluate flag based on targeting rules
        
        This is where the magic happens - complex targeting logic
        """
        # Global kill switch
        if not flag.is_enabled:
            return False
            
        # Parse targeting rules
        rules = flag.feature_config.get("targeting_rules", {}) if flag.feature_config else {}
        
        # No rules means flag is on for everyone
        if not rules.get("rules"):
            return True
            
        # Evaluate each rule
        for rule in rules.get("rules", []):
            if self._evaluate_rule(rule, context, flag):
                return True
                
        # Fall back to default
        return rules.get("default", False)
        
    def _evaluate_rule(
        self, 
        rule: Dict[str, Any], 
        context: Dict[str, Any],
        flag: PWAFeature
    ) -> bool:
        """Evaluate a single targeting rule"""
        rule_type = rule.get("type")
        
        if rule_type == "user":
            return self._evaluate_user_rule(rule, context)
        elif rule_type == "percentage":
            return self._evaluate_percentage_rule(rule, context, flag)
        elif rule_type == "jurisdiction":
            return self._evaluate_jurisdiction_rule(rule, context)
        elif rule_type == "role":
            return self._evaluate_role_rule(rule, context)
        elif rule_type == "date_range":
            return self._evaluate_date_range_rule(rule)
        elif rule_type == "custom":
            return self._evaluate_custom_rule(rule, context)
        else:
            logger.warning(f"Unknown rule type: {rule_type}")
            return False
            
    def _evaluate_user_rule(
        self, 
        rule: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> bool:
        """Evaluate user-based targeting"""
        user_id = context.get("user_id")
        if not user_id:
            return False
            
        operator = rule.get("operator", "in")
        values = rule.get("values", [])
        
        if operator == "in":
            return str(user_id) in values
        elif operator == "not_in":
            return str(user_id) not in values
        else:
            return False
            
    def _evaluate_percentage_rule(
        self, 
        rule: Dict[str, Any], 
        context: Dict[str, Any],
        flag: PWAFeature
    ) -> bool:
        """
        Evaluate percentage-based rollout
        
        Uses consistent hashing to ensure same user always gets same result
        """
        percentage = rule.get("value", 0)
        if percentage <= 0:
            return False
        if percentage >= 100:
            return True
            
        # Get stable identifier
        user_id = context.get("user_id", context.get("session_id", "anonymous"))
        
        # Create stable hash
        hash_input = f"{flag.feature_name}:{user_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        
        # Check if user is in percentage
        return (hash_value % 100) < percentage
        
    def _evaluate_jurisdiction_rule(
        self, 
        rule: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> bool:
        """
        Evaluate jurisdiction-based targeting
        
        This is specific to parliamentary systems
        """
        user_jurisdiction = context.get("jurisdiction")
        if not user_jurisdiction:
            return False
            
        operator = rule.get("operator", "equals")
        value = rule.get("value")
        
        if operator == "equals":
            return user_jurisdiction == value
        elif operator == "in":
            return user_jurisdiction in rule.get("values", [])
        elif operator == "not_equals":
            return user_jurisdiction != value
        else:
            return False
            
    def _evaluate_role_rule(
        self, 
        rule: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> bool:
        """Evaluate role-based targeting"""
        user_roles = context.get("roles", [])
        if not user_roles:
            return False
            
        required_roles = rule.get("values", [])
        operator = rule.get("operator", "any")
        
        if operator == "any":
            return any(role in required_roles for role in user_roles)
        elif operator == "all":
            return all(role in user_roles for role in required_roles)
        elif operator == "none":
            return not any(role in required_roles for role in user_roles)
        else:
            return False
            
    def _evaluate_date_range_rule(self, rule: Dict[str, Any]) -> bool:
        """Evaluate date range rule for time-based features"""
        now = datetime.utcnow()
        
        start_str = rule.get("start")
        end_str = rule.get("end")
        
        if start_str:
            start = datetime.fromisoformat(start_str)
            if now < start:
                return False
                
        if end_str:
            end = datetime.fromisoformat(end_str)
            if now > end:
                return False
                
        return True
        
    def _evaluate_custom_rule(
        self, 
        rule: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> bool:
        """
        Evaluate custom rule
        
        This allows for complex business logic
        """
        rule_name = rule.get("name")
        
        # Parliamentary-specific rules
        if rule_name == "active_session":
            # Check if parliament is in session
            return context.get("parliament_in_session", False)
        elif rule_name == "beta_tester":
            return context.get("beta_tester", False)
        elif rule_name == "high_engagement":
            # Users with high platform engagement
            return context.get("engagement_score", 0) > 80
        else:
            logger.warning(f"Unknown custom rule: {rule_name}")
            return False
            
    async def get_all_flags(
        self, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get all feature flags for a given context
        
        Useful for initializing client SDKs
        """
        context = context or {}
        result = {}
        
        # Include legacy flags
        for name, value in self._legacy_flags.items():
            result[name] = value
            
        # Get all database flags
        flags = self.db.query(PWAFeature).filter(
            PWAFeature.is_enabled == True
        ).all()
        
        for flag in flags:
            try:
                result[flag.feature_name] = await self.evaluate(
                    flag.feature_name, 
                    context
                )
            except Exception as e:
                logger.error(f"Error evaluating flag {flag.feature_name}: {e}")
                result[flag.feature_name] = False
                
        return result
        
    async def create_flag(
        self, 
        name: str,
        description: str,
        flag_type: FeatureFlagType = FeatureFlagType.RELEASE,
        enabled: bool = False,
        targeting_rules: Optional[Dict[str, Any]] = None
    ) -> PWAFeature:
        """Create a new feature flag"""
        flag = PWAFeature(
            feature_name=name,
            feature_description=description,
            is_enabled=enabled,
            feature_config={
                "type": flag_type.value,
                "targeting_rules": targeting_rules or {"rules": [], "default": False}
            }
        )
        
        self.db.add(flag)
        self.db.commit()
        self.db.refresh(flag)
        
        # Clear cache
        await self._clear_flag_cache(name)
        
        logger.info(f"Created feature flag: {name}")
        return flag
        
    async def update_flag(
        self,
        name: str,
        **updates
    ) -> Optional[PWAFeature]:
        """Update an existing feature flag"""
        flag = self._get_flag(name)
        if not flag:
            return None
            
        # Update fields
        for key, value in updates.items():
            if hasattr(flag, key):
                setattr(flag, key, value)
                
        self.db.commit()
        self.db.refresh(flag)
        
        # Clear cache
        await self._clear_flag_cache(name)
        
        logger.info(f"Updated feature flag: {name}")
        return flag
        
    def _get_cache_key(
        self, 
        flag_name: str, 
        context: Dict[str, Any]
    ) -> str:
        """Generate cache key for evaluation result"""
        # Sort context keys for consistent hashing
        context_str = json.dumps(context, sort_keys=True)
        context_hash = hashlib.md5(context_str.encode()).hexdigest()[:8]
        return f"feature_flag:{flag_name}:{context_hash}"
        
    async def _get_cached_evaluation(self, cache_key: str) -> Optional[bool]:
        """Get cached evaluation result"""
        if not self.redis:
            return None
            
        try:
            result = await self.redis.get(cache_key)
            if result is not None:
                return result == b"1"
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            
        return None
        
    async def _cache_evaluation(self, cache_key: str, result: bool):
        """Cache evaluation result"""
        if not self.redis:
            return
            
        try:
            await self.redis.setex(
                cache_key,
                self._cache_ttl,
                "1" if result else "0"
            )
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            
    async def _clear_flag_cache(self, flag_name: str):
        """Clear all cache entries for a flag"""
        if not self.redis:
            return
            
        try:
            # Find all keys for this flag
            pattern = f"feature_flag:{flag_name}:*"
            cursor = 0
            
            while True:
                cursor, keys = await self.redis.scan(
                    cursor, 
                    match=pattern,
                    count=100
                )
                
                if keys:
                    await self.redis.delete(*keys)
                    
                if cursor == 0:
                    break
                    
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            
    async def _track_evaluation(
        self,
        flag_name: str,
        context: Dict[str, Any],
        result: bool
    ):
        """Track feature flag evaluation for analytics"""
        # TODO: Implement analytics tracking
        # This would send to analytics service or write to database
        pass