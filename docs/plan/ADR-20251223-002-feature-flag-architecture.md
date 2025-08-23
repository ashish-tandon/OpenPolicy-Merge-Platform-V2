# ADR-20251223-002: Unified Feature Flag Architecture

## Status
Proposed

## Context
OpenPolicy V2 has two separate feature flag implementations that were discovered:

1. **PWA Feature Flags** (`services/api-gateway/app/models/pwa_system.py`)
   - Database-backed with PostgreSQL
   - Rich data model with browser/platform support
   - Configuration stored as JSONB
   - No management API or UI
   - Tied to PWA manifests

2. **API Version Feature Flags** (`docs/API_VERSIONING_STRATEGY.md`)
   - Code-based Python class
   - Version-aware toggles
   - Hardcoded boolean values
   - No runtime configuration
   - Used for API versioning

Additionally, we need feature flags for:
- Gradual feature rollout
- A/B testing capabilities  
- Emergency feature kill switches
- Beta feature access
- Per-user feature enablement
- Environment-specific features

## Decision
Create a unified feature flag service by extending the existing PWA feature flag system into a comprehensive solution that serves all feature flag needs across the platform.

### Rationale
1. **Database model already exists** - PWA system provides a solid foundation
2. **Avoid external dependencies** - No need for LaunchDarkly or similar
3. **Custom requirements** - Parliamentary-specific needs (jurisdiction-based flags)
4. **Data sovereignty** - Keep feature data in our control
5. **Cost effective** - No external service fees

## Consequences

### Positive
- Single system for all feature flags
- Database-backed for runtime changes
- Rich configuration options
- Audit trail of changes
- Performance (local evaluation)
- Custom business rules

### Negative  
- Need to build management UI
- More complex than external service
- Maintenance overhead
- Need caching layer
- SDK development needed

## Implementation Design

### Data Model Enhancement
```sql
-- Extend existing PWAFeature table
ALTER TABLE pwa_features RENAME TO feature_flags;
ALTER TABLE feature_flags 
  ADD COLUMN flag_type VARCHAR(50) DEFAULT 'feature',
  ADD COLUMN targeting_rules JSONB,
  ADD COLUMN rollout_percentage INTEGER DEFAULT 0,
  ADD COLUMN environments JSONB DEFAULT '["all"]',
  ADD COLUMN user_overrides JSONB,
  ADD COLUMN start_date TIMESTAMP,
  ADD COLUMN end_date TIMESTAMP,
  ADD COLUMN dependencies JSONB;

-- Add evaluation cache
CREATE TABLE feature_evaluations (
  id UUID PRIMARY KEY,
  flag_id UUID REFERENCES feature_flags(id),
  user_id VARCHAR(255),
  evaluation_result BOOLEAN,
  evaluation_context JSONB,
  evaluated_at TIMESTAMP DEFAULT NOW()
);

-- Audit log
CREATE TABLE feature_flag_changes (
  id UUID PRIMARY KEY,
  flag_id UUID REFERENCES feature_flags(id),
  changed_by VARCHAR(255),
  change_type VARCHAR(50),
  old_value JSONB,
  new_value JSONB,
  changed_at TIMESTAMP DEFAULT NOW()
);
```

### API Design
```python
# Feature Flag Service API
class FeatureFlagService:
    async def evaluate(
        self,
        flag_name: str,
        context: dict = None
    ) -> bool:
        """Evaluate a feature flag with context"""
        
    async def get_all_flags(
        self,
        user_context: dict = None
    ) -> dict:
        """Get all flags for a user context"""
        
    async def create_flag(
        self,
        flag: FeatureFlagCreate
    ) -> FeatureFlag:
        """Create a new feature flag"""
        
    async def update_flag(
        self,
        flag_name: str,
        updates: FeatureFlagUpdate
    ) -> FeatureFlag:
        """Update feature flag configuration"""
```

### Targeting Rules Schema
```json
{
  "rules": [
    {
      "type": "user",
      "operator": "in",
      "values": ["user123", "user456"]
    },
    {
      "type": "percentage",
      "value": 25
    },
    {
      "type": "jurisdiction",
      "operator": "equals",
      "value": "ontario"
    },
    {
      "type": "date_range",
      "start": "2024-01-01",
      "end": "2024-12-31"
    }
  ],
  "default": false
}
```

## Implementation Plan

### Phase 1: Core Service (Week 1)
1. Migrate PWA feature table schema
2. Implement evaluation engine
3. Create caching layer
4. Build REST API endpoints
5. Add metrics and logging

### Phase 2: Management UI (Week 2)
1. Admin dashboard for flag management
2. Targeting rule builder
3. Rollout percentage controls
4. Environment configuration
5. Audit log viewer

### Phase 3: SDK Development (Week 3)
1. Python SDK for backend services
2. JavaScript/TypeScript SDK for frontend
3. React hooks for feature flags
4. Documentation and examples

### Phase 4: Migration (Week 4)
1. Migrate API version flags to new system
2. Convert hardcoded flags to database
3. Update all flag references
4. Remove old implementations

### Phase 5: Advanced Features (Week 5-6)
1. A/B testing framework
2. Feature flag analytics
3. Dependency management
4. Scheduled rollouts
5. Integration with monitoring

## Usage Examples

### Backend Usage
```python
from app.features import feature_flags

# Simple evaluation
if await feature_flags.is_enabled("new_voting_system"):
    return new_voting_logic()
else:
    return legacy_voting_logic()

# With context
context = {
    "user_id": current_user.id,
    "jurisdiction": current_user.jurisdiction,
    "role": current_user.role
}
if await feature_flags.is_enabled("beta_analytics", context):
    show_beta_features()
```

### Frontend Usage
```typescript
// React component
import { useFeatureFlag } from '@openpolicy/features';

function MPProfile() {
  const showNewProfile = useFeatureFlag('new_mp_profile_design');
  
  return showNewProfile ? <NewProfile /> : <LegacyProfile />;
}
```

## Monitoring

Key metrics to track:
- Flag evaluation latency (target: <5ms)
- Cache hit rate (target: >95%)
- Flag update propagation time
- SDK initialization time
- API endpoint performance

## Security Considerations

1. **Access Control**: Only admins can modify flags
2. **Audit Trail**: All changes logged with user info
3. **Validation**: Strict schema validation for targeting rules
4. **Rate Limiting**: Prevent evaluation spam
5. **Encryption**: Sensitive targeting data encrypted

## Alternatives Considered

### 1. External Service (LaunchDarkly, Split.io)
- **Pros**: Full-featured, proven, good SDKs
- **Cons**: Cost, data sovereignty, vendor lock-in
- **Rejected because**: Expensive and less control

### 2. Simple Config Files
- **Pros**: Very simple, no database needed
- **Cons**: No runtime changes, deployment needed
- **Rejected because**: Too limiting for our needs

### 3. Build Minimal Toggle Service
- **Pros**: Simple, focused
- **Cons**: Lacks advanced features we'll eventually need
- **Rejected because**: Better to build full solution now

## References
- [Feature Toggle Patterns](https://martinfowler.com/articles/feature-toggles.html)
- [Progressive Delivery](https://launchdarkly.com/blog/what-is-progressive-delivery/)
- [Feature Flag Best Practices](https://featureflags.io/feature-flag-best-practices/)