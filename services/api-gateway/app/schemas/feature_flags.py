"""
Feature Flags Schemas

Pydantic schemas for feature flag API requests and responses.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List, Literal
from datetime import datetime
from uuid import UUID


class TargetingRule(BaseModel):
    """Schema for targeting rules."""
    type: Literal["user", "percentage", "jurisdiction", "date_range", "environment", "role"]
    operator: Optional[Literal["in", "not_in", "equals", "not_equals", "greater_than", "less_than"]] = None
    values: Optional[List[str]] = None
    value: Optional[Any] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None


class TargetingRules(BaseModel):
    """Schema for complete targeting configuration."""
    rules: List[TargetingRule] = []
    default: bool = False
    require_all: bool = False  # AND vs OR for rules


class FeatureFlagBase(BaseModel):
    """Base schema for feature flags."""
    feature_name: str = Field(..., min_length=1, max_length=200, description="Unique feature identifier")
    feature_description: Optional[str] = Field(None, description="Feature description")
    flag_type: Literal["feature", "experiment", "operational", "permission"] = Field(
        "feature", 
        description="Type of feature flag"
    )
    is_enabled: bool = Field(False, description="Global on/off switch")
    rollout_percentage: int = Field(0, ge=0, le=100, description="Percentage rollout (0-100)")
    environments: List[str] = Field(["all"], description="Enabled environments")
    feature_config: Optional[Dict[str, Any]] = Field(None, description="Feature-specific configuration")
    dependencies: Optional[List[str]] = Field(None, description="Other flags this depends on")
    start_date: Optional[datetime] = Field(None, description="When to start showing feature")
    end_date: Optional[datetime] = Field(None, description="When to stop showing feature")
    
    @validator('feature_name')
    def validate_feature_name(cls, v):
        """Validate feature name format."""
        if not v.replace('_', '').replace('-', '').replace('.', '').isalnum():
            raise ValueError('Feature name must contain only alphanumeric characters, underscores, hyphens, and dots')
        return v
    
    @validator('end_date')
    def validate_dates(cls, v, values):
        """Ensure end date is after start date."""
        if v and 'start_date' in values and values['start_date']:
            if v <= values['start_date']:
                raise ValueError('End date must be after start date')
        return v


class FeatureFlagCreate(FeatureFlagBase):
    """Schema for creating a feature flag."""
    targeting_rules: Optional[TargetingRules] = None
    user_overrides: Optional[Dict[str, bool]] = Field(None, description="User-specific overrides")
    created_by: Optional[str] = Field(None, description="Who created the flag")


class FeatureFlagUpdate(BaseModel):
    """Schema for updating a feature flag."""
    feature_description: Optional[str] = None
    is_enabled: Optional[bool] = None
    rollout_percentage: Optional[int] = Field(None, ge=0, le=100)
    targeting_rules: Optional[TargetingRules] = None
    user_overrides: Optional[Dict[str, bool]] = None
    environments: Optional[List[str]] = None
    feature_config: Optional[Dict[str, Any]] = None
    dependencies: Optional[List[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class FeatureFlagResponse(FeatureFlagBase):
    """Schema for feature flag responses."""
    id: UUID
    targeting_rules: Optional[Dict[str, Any]] = None
    user_overrides: Optional[Dict[str, bool]] = None
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class EvaluationContext(BaseModel):
    """Context for feature flag evaluation."""
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_role: Optional[str] = None
    jurisdiction: Optional[str] = None
    environment: Optional[str] = "production"
    session_id: Optional[str] = None
    device_type: Optional[str] = None
    platform: Optional[str] = None
    browser: Optional[str] = None
    custom_attributes: Optional[Dict[str, Any]] = None


class FeatureFlagEvaluation(BaseModel):
    """Schema for feature flag evaluation result."""
    feature_name: str
    is_enabled: bool
    reason: Optional[str] = None
    variant: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BulkEvaluationRequest(BaseModel):
    """Request for evaluating multiple feature flags."""
    feature_names: Optional[List[str]] = Field(None, description="Specific flags to evaluate (None = all)")
    context: EvaluationContext


class BulkEvaluationResponse(BaseModel):
    """Response for bulk feature flag evaluation."""
    flags: Dict[str, bool]
    context: Dict[str, Any]
    evaluated_at: datetime


class FeatureFlagListResponse(BaseModel):
    """Response for listing feature flags."""
    flags: List[FeatureFlagResponse]
    total: int
    page: int
    page_size: int


class FeatureFlagChangeResponse(BaseModel):
    """Response for feature flag change audit."""
    id: UUID
    flag_id: UUID
    feature_name: str
    changed_by: str
    change_type: str
    old_value: Optional[Dict[str, Any]]
    new_value: Optional[Dict[str, Any]]
    changed_at: datetime
    
    class Config:
        from_attributes = True


class FeatureFlagStats(BaseModel):
    """Statistics for a feature flag."""
    flag_id: UUID
    feature_name: str
    total_evaluations: int
    true_evaluations: int
    false_evaluations: int
    unique_users: int
    evaluation_rate: float
    last_evaluated: Optional[datetime]
    environments: Dict[str, int]