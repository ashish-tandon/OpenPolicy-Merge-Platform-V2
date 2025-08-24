"""
Feature Flags Core Service

Core service for evaluating feature flags with caching, targeting rules,
and audit logging. Implements the evaluation engine for the feature flag system.
"""

import hashlib
import json
import random
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Set
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.feature_flags import FeatureFlag, FeatureEvaluation, FeatureFlagChange
from app.schemas.feature_flags import EvaluationContext, TargetingRules
from app.core.cache import cache_service
import logging

logger = logging.getLogger(__name__)


class FeatureFlagService:
    """Service for managing and evaluating feature flags."""
    
    CACHE_PREFIX = "feature_flag:"
    CACHE_TTL = 300  # 5 minutes
    
    def __init__(self, db: Session):
        self.db = db
    
    async def evaluate(
        self, 
        feature_name: str, 
        context: Optional[EvaluationContext] = None
    ) -> bool:
        """
        Evaluate a feature flag with the given context.
        
        Args:
            feature_name: Name of the feature flag
            context: Evaluation context with user and environment info
            
        Returns:
            Boolean indicating if the feature is enabled
        """
        # Check cache first
        cache_key = self._get_cache_key(feature_name, context)
        cached_result = await cache_service.get(cache_key)
        if cached_result is not None:
            return cached_result
        
        # Get flag from database
        flag = self.db.query(FeatureFlag).filter(
            FeatureFlag.feature_name == feature_name
        ).first()
        
        if not flag:
            # Flag doesn't exist, default to disabled
            logger.warning(f"Feature flag '{feature_name}' not found")
            return False
        
        # Evaluate the flag
        result = await self._evaluate_flag(flag, context)
        
        # Cache the result
        await cache_service.set(cache_key, result, ttl=self.CACHE_TTL)
        
        # Log evaluation (async, don't wait)
        self._log_evaluation(flag.id, context, result)
        
        return result
    
    async def evaluate_all(
        self, 
        context: Optional[EvaluationContext] = None,
        feature_names: Optional[List[str]] = None
    ) -> Dict[str, bool]:
        """Evaluate multiple feature flags at once."""
        query = self.db.query(FeatureFlag)
        
        if feature_names:
            query = query.filter(FeatureFlag.feature_name.in_(feature_names))
        
        flags = query.all()
        results = {}
        
        for flag in flags:
            results[flag.feature_name] = await self._evaluate_flag(flag, context)
        
        return results
    
    async def _evaluate_flag(
        self, 
        flag: FeatureFlag, 
        context: Optional[EvaluationContext] = None
    ) -> bool:
        """Internal method to evaluate a single flag."""
        # Check if globally disabled
        if not flag.is_enabled:
            return False
        
        # Check time-based constraints
        now = datetime.now(timezone.utc)
        if flag.start_date and now < flag.start_date:
            return False
        if flag.end_date and now > flag.end_date:
            return False
        
        # Check environment
        if context and flag.environments != ["all"]:
            env = context.environment or "production"
            if env not in flag.environments:
                return False
        
        # Check dependencies
        if flag.dependencies:
            for dep_name in flag.dependencies:
                if not await self.evaluate(dep_name, context):
                    return False
        
        # Check user overrides
        if context and context.user_id and flag.user_overrides:
            if context.user_id in flag.user_overrides:
                return flag.user_overrides[context.user_id]
        
        # Check targeting rules
        if flag.targeting_rules:
            rules = TargetingRules(**flag.targeting_rules)
            if await self._evaluate_targeting_rules(rules, context):
                return True
            elif not rules.default:
                return False
        
        # Check rollout percentage
        if flag.rollout_percentage > 0:
            return self._check_rollout_percentage(
                flag.feature_name, 
                context.user_id if context else None,
                flag.rollout_percentage
            )
        
        # Default to the flag's enabled state
        return flag.is_enabled
    
    async def _evaluate_targeting_rules(
        self, 
        rules: TargetingRules, 
        context: Optional[EvaluationContext]
    ) -> bool:
        """Evaluate targeting rules."""
        if not context or not rules.rules:
            return rules.default
        
        results = []
        
        for rule in rules.rules:
            result = await self._evaluate_single_rule(rule, context)
            results.append(result)
        
        # Apply AND/OR logic
        if rules.require_all:
            return all(results)
        else:
            return any(results)
    
    async def _evaluate_single_rule(self, rule: Any, context: EvaluationContext) -> bool:
        """Evaluate a single targeting rule."""
        rule_type = rule.type
        
        if rule_type == "user":
            if not context.user_id:
                return False
            if rule.operator == "in":
                return context.user_id in (rule.values or [])
            elif rule.operator == "not_in":
                return context.user_id not in (rule.values or [])
        
        elif rule_type == "percentage":
            user_id = context.user_id or context.session_id or "anonymous"
            return self._check_rollout_percentage("", user_id, rule.value or 0)
        
        elif rule_type == "jurisdiction":
            if not context.jurisdiction:
                return False
            if rule.operator == "equals":
                return context.jurisdiction == rule.value
            elif rule.operator == "not_equals":
                return context.jurisdiction != rule.value
            elif rule.operator == "in":
                return context.jurisdiction in (rule.values or [])
        
        elif rule_type == "date_range":
            now = datetime.now(timezone.utc)
            if rule.start and now < rule.start:
                return False
            if rule.end and now > rule.end:
                return False
            return True
        
        elif rule_type == "environment":
            env = context.environment or "production"
            if rule.operator == "equals":
                return env == rule.value
            elif rule.operator == "in":
                return env in (rule.values or [])
        
        elif rule_type == "role":
            if not context.user_role:
                return False
            if rule.operator == "equals":
                return context.user_role == rule.value
            elif rule.operator == "in":
                return context.user_role in (rule.values or [])
        
        # Unknown rule type
        return False
    
    def _check_rollout_percentage(
        self, 
        feature_name: str, 
        user_id: Optional[str], 
        percentage: int
    ) -> bool:
        """Check if user falls within rollout percentage."""
        if percentage <= 0:
            return False
        if percentage >= 100:
            return True
        
        # Create stable hash for consistent bucketing
        bucket_key = f"{feature_name}:{user_id or 'anonymous'}"
        hash_value = int(hashlib.md5(bucket_key.encode()).hexdigest(), 16)
        bucket = hash_value % 100
        
        return bucket < percentage
    
    def _get_cache_key(self, feature_name: str, context: Optional[EvaluationContext]) -> str:
        """Generate cache key for feature flag evaluation."""
        if not context:
            return f"{self.CACHE_PREFIX}{feature_name}:global"
        
        # Include relevant context in cache key
        context_parts = [
            context.user_id or "",
            context.environment or "production",
            context.jurisdiction or "",
            context.user_role or ""
        ]
        context_hash = hashlib.md5(":".join(context_parts).encode()).hexdigest()[:8]
        
        return f"{self.CACHE_PREFIX}{feature_name}:{context_hash}"
    
    def _log_evaluation(
        self, 
        flag_id: UUID, 
        context: Optional[EvaluationContext], 
        result: bool
    ):
        """Log feature flag evaluation (fire and forget)."""
        try:
            evaluation = FeatureEvaluation(
                flag_id=flag_id,
                user_id=context.user_id if context else None,
                evaluation_result=result,
                evaluation_context=context.dict() if context else None
            )
            self.db.add(evaluation)
            self.db.commit()
        except Exception as e:
            logger.error(f"Failed to log feature evaluation: {e}")
            self.db.rollback()
    
    def create_flag(self, flag_data: Dict[str, Any], created_by: str) -> FeatureFlag:
        """Create a new feature flag."""
        flag = FeatureFlag(**flag_data)
        flag.created_by = created_by
        
        self.db.add(flag)
        self.db.flush()
        
        # Log change
        self._log_change(flag.id, created_by, "create", None, flag.to_dict())
        
        self.db.commit()
        
        # Clear cache
        self._clear_flag_cache(flag.feature_name)
        
        return flag
    
    def update_flag(
        self, 
        feature_name: str, 
        updates: Dict[str, Any], 
        updated_by: str
    ) -> Optional[FeatureFlag]:
        """Update an existing feature flag."""
        flag = self.db.query(FeatureFlag).filter(
            FeatureFlag.feature_name == feature_name
        ).first()
        
        if not flag:
            return None
        
        old_value = flag.to_dict()
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(flag, key):
                setattr(flag, key, value)
        
        # Log change
        self._log_change(flag.id, updated_by, "update", old_value, flag.to_dict())
        
        self.db.commit()
        
        # Clear cache
        self._clear_flag_cache(feature_name)
        
        return flag
    
    def delete_flag(self, feature_name: str, deleted_by: str) -> bool:
        """Delete a feature flag."""
        flag = self.db.query(FeatureFlag).filter(
            FeatureFlag.feature_name == feature_name
        ).first()
        
        if not flag:
            return False
        
        old_value = flag.to_dict()
        
        # Log change
        self._log_change(flag.id, deleted_by, "delete", old_value, None)
        
        # Delete flag
        self.db.delete(flag)
        self.db.commit()
        
        # Clear cache
        self._clear_flag_cache(feature_name)
        
        return True
    
    def _log_change(
        self, 
        flag_id: UUID, 
        changed_by: str, 
        change_type: str,
        old_value: Optional[Dict[str, Any]],
        new_value: Optional[Dict[str, Any]]
    ):
        """Log a change to a feature flag."""
        change = FeatureFlagChange(
            flag_id=flag_id,
            changed_by=changed_by,
            change_type=change_type,
            old_value=old_value,
            new_value=new_value
        )
        self.db.add(change)
    
    def _clear_flag_cache(self, feature_name: str):
        """Clear cache for a specific flag."""
        # In a real implementation, this would clear all cache entries
        # for the given feature flag across all contexts
        cache_service.delete_pattern(f"{self.CACHE_PREFIX}{feature_name}:*")
    
    def get_flag_stats(self, feature_name: str) -> Dict[str, Any]:
        """Get evaluation statistics for a feature flag."""
        flag = self.db.query(FeatureFlag).filter(
            FeatureFlag.feature_name == feature_name
        ).first()
        
        if not flag:
            return {}
        
        # Get evaluation counts
        total_evals = self.db.query(FeatureEvaluation).filter(
            FeatureEvaluation.flag_id == flag.id
        ).count()
        
        true_evals = self.db.query(FeatureEvaluation).filter(
            and_(
                FeatureEvaluation.flag_id == flag.id,
                FeatureEvaluation.evaluation_result == True
            )
        ).count()
        
        # Get unique users
        unique_users = self.db.query(FeatureEvaluation.user_id).filter(
            and_(
                FeatureEvaluation.flag_id == flag.id,
                FeatureEvaluation.user_id.isnot(None)
            )
        ).distinct().count()
        
        return {
            "flag_id": flag.id,
            "feature_name": flag.feature_name,
            "total_evaluations": total_evals,
            "true_evaluations": true_evals,
            "false_evaluations": total_evals - true_evals,
            "unique_users": unique_users,
            "evaluation_rate": (true_evals / total_evals * 100) if total_evals > 0 else 0
        }


# Singleton instance
feature_flag_service = None

def get_feature_flag_service(db: Session) -> FeatureFlagService:
    """Get or create feature flag service instance."""
    global feature_flag_service
    if feature_flag_service is None:
        feature_flag_service = FeatureFlagService(db)
    return feature_flag_service