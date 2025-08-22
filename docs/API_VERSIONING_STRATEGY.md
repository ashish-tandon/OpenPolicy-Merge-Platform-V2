# API Versioning Strategy

## Executive Summary
This document outlines the API versioning strategy for the OpenPolicy platform, ensuring backward compatibility, smooth migrations, and clear deprecation policies while maintaining API stability for all consumers.

## Versioning Philosophy

### Core Principles
1. **Stability First**: Breaking changes are avoided whenever possible
2. **Clear Communication**: Version changes are well-documented and communicated
3. **Graceful Deprecation**: Old versions supported with clear migration paths
4. **Semantic Versioning**: Predictable version numbering
5. **Consumer-Friendly**: Multiple versioning mechanisms for flexibility

## Versioning Scheme

### Semantic Versioning (SemVer)
We follow Semantic Versioning 2.0.0: `MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality additions
- **PATCH**: Backward-compatible bug fixes

Examples:
- `1.0.0` → `1.0.1`: Bug fix (PATCH)
- `1.0.1` → `1.1.0`: New endpoint added (MINOR)
- `1.1.0` → `2.0.0`: Breaking change (MAJOR)

### API Version Format
```
/api/v{MAJOR}/resource
```

Examples:
- `/api/v1/bills`
- `/api/v2/members`

## Versioning Implementation

### URL Path Versioning (Primary)
```python
# FastAPI implementation
from fastapi import APIRouter

# Version 1 routes
v1_router = APIRouter(prefix="/api/v1")

@v1_router.get("/bills")
async def get_bills_v1():
    return {"version": "1.0", "data": await fetch_bills_v1()}

# Version 2 routes
v2_router = APIRouter(prefix="/api/v2")

@v2_router.get("/bills")
async def get_bills_v2():
    return {"version": "2.0", "data": await fetch_bills_v2()}

# Main app
app.include_router(v1_router)
app.include_router(v2_router)
```

### Header Versioning (Secondary)
```python
# Accept header versioning
from fastapi import Header, HTTPException

@app.get("/api/bills")
async def get_bills(accept: str = Header(None)):
    if accept and "version=2" in accept:
        return await get_bills_v2()
    elif accept and "version=1" in accept:
        return await get_bills_v1()
    else:
        # Default to latest stable
        return await get_bills_v2()
```

### Query Parameter Versioning (Fallback)
```python
# Query parameter for testing/debugging
@app.get("/api/bills")
async def get_bills(api_version: str = None):
    if api_version == "2":
        return await get_bills_v2()
    elif api_version == "1":
        return await get_bills_v1()
    else:
        return await get_bills_v2()  # Default
```

## Version Lifecycle

### Version States
1. **Alpha**: Internal testing only (`v2-alpha`)
2. **Beta**: Limited external testing (`v2-beta`)
3. **Release Candidate**: Pre-production (`v2-rc`)
4. **Stable**: Production ready (`v2`)
5. **Deprecated**: Scheduled for removal (`v1-deprecated`)
6. **Sunset**: No longer available

### Version Timeline
```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   Alpha     │    Beta     │     RC      │   Stable    │ Deprecated  │
│  (1 month)  │  (2 months) │  (1 month)  │ (18 months) │ (6 months)  │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
                                           │                            │
                                           └── New version released ───┘
```

## Breaking Changes

### What Constitutes a Breaking Change
1. **Removing endpoints or fields**
2. **Changing field types** (e.g., string → number)
3. **Changing required fields**
4. **Modifying authentication methods**
5. **Altering response structure**
6. **Changing error codes/formats**

### What is NOT a Breaking Change
1. **Adding new endpoints**
2. **Adding optional fields**
3. **Adding new optional parameters**
4. **Adding new response headers**
5. **Improving performance**
6. **Fixing bugs that don't change contracts**

## Backward Compatibility

### Response Evolution
```python
# Version 1 response
class BillV1(BaseModel):
    id: str
    title: str
    status: str

# Version 2 response (backward compatible)
class BillV2(BaseModel):
    id: str
    title: str
    status: str
    # New optional fields
    summary: Optional[str] = None
    sponsor: Optional[str] = None
    tags: List[str] = []

# Response adapter for compatibility
def adapt_bill_response(bill: Bill, version: int) -> dict:
    if version == 1:
        return BillV1(
            id=bill.id,
            title=bill.title,
            status=bill.status
        ).dict()
    else:
        return BillV2(
            id=bill.id,
            title=bill.title,
            status=bill.status,
            summary=bill.summary,
            sponsor=bill.sponsor,
            tags=bill.tags
        ).dict()
```

### Database Migration Strategy
```python
# Alembic migration with API versioning consideration
"""add_bill_summary_field

Revision ID: abc123
Revises: def456
Create Date: 2024-01-20 10:00:00

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add new column as nullable for backward compatibility
    op.add_column('bills', sa.Column('summary', sa.Text(), nullable=True))
    
    # Populate with default values
    op.execute("UPDATE bills SET summary = 'No summary available' WHERE summary IS NULL")

def downgrade():
    op.drop_column('bills', 'summary')
```

## Deprecation Policy

### Deprecation Timeline
1. **Announcement**: 6 months before deprecation
2. **Deprecation Warning**: Added to responses
3. **Feature Freeze**: No new features added
4. **End of Life**: Version removed

### Deprecation Headers
```python
# Deprecation middleware
@app.middleware("http")
async def add_deprecation_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Check if using deprecated version
    if "/api/v1/" in str(request.url):
        response.headers["Sunset"] = "Sun, 01 Jul 2024 00:00:00 GMT"
        response.headers["Deprecation"] = "version=\"1.0\""
        response.headers["Link"] = '</api/v2/docs>; rel="successor-version"'
    
    return response
```

### Deprecation Response
```json
{
  "data": {
    // Normal response data
  },
  "warnings": [
    {
      "code": "DEPRECATION_WARNING",
      "message": "API v1 is deprecated and will be removed on 2024-07-01. Please migrate to v2.",
      "migration_guide": "https://docs.openpolicy.ca/api/migration/v1-to-v2"
    }
  ]
}
```

## Client Migration

### Migration Guide Template
```markdown
# Migrating from API v1 to v2

## Overview
API v2 introduces several improvements while maintaining backward compatibility where possible.

## Breaking Changes

### 1. Authentication
- **v1**: API key in query parameter
- **v2**: Bearer token in Authorization header

```bash
# v1
curl https://api.openpolicy.ca/v1/bills?api_key=YOUR_KEY

# v2
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.openpolicy.ca/v2/bills
```

### 2. Response Format
- **v1**: Flat response structure
- **v2**: Nested response with metadata

```json
// v1 Response
{
  "bills": [...],
  "total": 100
}

// v2 Response
{
  "data": {
    "bills": [...]
  },
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20
  }
}
```

## New Features in v2
- Pagination improvements
- Filtering enhancements
- GraphQL endpoint
- WebSocket support

## Migration Checklist
- [ ] Update authentication method
- [ ] Update response parsing
- [ ] Test error handling
- [ ] Update API base URL
- [ ] Review new features
```

### Client Libraries
```python
# Python client with version support
class OpenPolicyClient:
    def __init__(self, api_key: str, version: str = "v2"):
        self.api_key = api_key
        self.version = version
        self.base_url = f"https://api.openpolicy.ca/{version}"
    
    def get_bills(self, **params):
        if self.version == "v1":
            # v1 compatibility
            params["api_key"] = self.api_key
            response = requests.get(f"{self.base_url}/bills", params=params)
        else:
            # v2 implementation
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(f"{self.base_url}/bills", 
                                  headers=headers, params=params)
        
        return self._parse_response(response)
    
    def _parse_response(self, response):
        if self.version == "v1":
            return response.json()
        else:
            # v2 returns data wrapped
            return response.json().get("data", {})
```

## Version Discovery

### Version Endpoint
```python
@app.get("/api/versions")
async def get_api_versions():
    return {
        "versions": [
            {
                "version": "1.0",
                "status": "deprecated",
                "deprecation_date": "2024-07-01",
                "endpoints": "https://api.openpolicy.ca/v1/docs"
            },
            {
                "version": "2.0",
                "status": "stable",
                "released": "2024-01-01",
                "endpoints": "https://api.openpolicy.ca/v2/docs"
            },
            {
                "version": "3.0",
                "status": "beta",
                "released": "2024-06-01",
                "endpoints": "https://api.openpolicy.ca/v3-beta/docs"
            }
        ],
        "recommended": "2.0",
        "minimum_supported": "1.0"
    }
```

### OpenAPI Documentation
```python
# Separate OpenAPI specs per version
@app.get("/api/v1/openapi.json")
async def openapi_v1():
    return get_openapi(
        title="OpenPolicy API",
        version="1.0",
        routes=app.routes,
        tags=v1_tags
    )

@app.get("/api/v2/openapi.json")
async def openapi_v2():
    return get_openapi(
        title="OpenPolicy API",
        version="2.0",
        routes=app.routes,
        tags=v2_tags
    )
```

## Feature Flags

### Version-Specific Features
```python
# Feature flags for gradual rollout
class FeatureFlags:
    def __init__(self):
        self.flags = {
            "v2_pagination": True,
            "v2_graphql": True,
            "v2_websocket": False,  # Still in development
            "v3_ai_summaries": False  # v3 feature
        }
    
    def is_enabled(self, feature: str, version: str) -> bool:
        if version == "v1":
            return False  # No new features in v1
        
        return self.flags.get(feature, False)

# Usage in endpoints
@v2_router.get("/bills")
async def get_bills_v2(
    page: int = 1,
    per_page: int = 20,
    feature_flags: FeatureFlags = Depends()
):
    if feature_flags.is_enabled("v2_pagination", "v2"):
        # Use new pagination
        return await get_paginated_bills(page, per_page)
    else:
        # Fall back to v1 style
        return await get_all_bills()
```

## API Gateway Configuration

### Nginx Routing
```nginx
# API version routing
server {
    listen 443 ssl http2;
    server_name api.openpolicy.ca;
    
    # Version 1 (deprecated)
    location /v1/ {
        add_header Sunset "Sun, 01 Jul 2024 00:00:00 GMT" always;
        add_header Deprecation "version=\"1.0\"" always;
        proxy_pass http://api-v1:8080/;
    }
    
    # Version 2 (stable)
    location /v2/ {
        proxy_pass http://api-v2:8080/;
    }
    
    # Version 3 (beta)
    location /v3-beta/ {
        add_header Warning "199 - \"Beta version, subject to change\"" always;
        proxy_pass http://api-v3:8080/;
    }
    
    # Default to latest stable
    location / {
        return 302 /v2$request_uri;
    }
}
```

### Rate Limiting by Version
```python
# Different rate limits per version
from slowapi import Limiter

def get_rate_limit_key(request: Request) -> str:
    # Include version in rate limit key
    version = "v1" if "/v1/" in str(request.url) else "v2"
    return f"{get_remote_address(request)}:{version}"

limiter = Limiter(key_func=get_rate_limit_key)

# Stricter limits for deprecated versions
@app.get("/api/v1/bills")
@limiter.limit("50 per minute")  # Reduced limit
async def get_bills_v1():
    pass

@app.get("/api/v2/bills")
@limiter.limit("200 per minute")  # Normal limit
async def get_bills_v2():
    pass
```

## Monitoring and Analytics

### Version Usage Metrics
```python
# Prometheus metrics for version tracking
from prometheus_client import Counter, Histogram

api_requests = Counter(
    'api_requests_total',
    'Total API requests',
    ['version', 'endpoint', 'method', 'status']
)

api_latency = Histogram(
    'api_request_duration_seconds',
    'API request latency',
    ['version', 'endpoint']
)

# Middleware to track metrics
@app.middleware("http")
async def track_metrics(request: Request, call_next):
    start_time = time.time()
    
    # Extract version
    version = "unknown"
    if "/v1/" in str(request.url):
        version = "v1"
    elif "/v2/" in str(request.url):
        version = "v2"
    elif "/v3-beta/" in str(request.url):
        version = "v3-beta"
    
    response = await call_next(request)
    
    # Record metrics
    duration = time.time() - start_time
    api_requests.labels(
        version=version,
        endpoint=request.url.path,
        method=request.method,
        status=response.status_code
    ).inc()
    
    api_latency.labels(
        version=version,
        endpoint=request.url.path
    ).observe(duration)
    
    return response
```

### Version Adoption Dashboard
```sql
-- Version usage analytics
SELECT 
    version,
    COUNT(*) as request_count,
    COUNT(DISTINCT client_id) as unique_clients,
    AVG(response_time) as avg_response_time,
    DATE_TRUNC('day', timestamp) as date
FROM api_logs
WHERE timestamp > NOW() - INTERVAL '30 days'
GROUP BY version, date
ORDER BY date DESC, version;

-- Client migration status
SELECT 
    client_id,
    MAX(CASE WHEN version = 'v1' THEN timestamp END) as last_v1_usage,
    MAX(CASE WHEN version = 'v2' THEN timestamp END) as last_v2_usage,
    CASE 
        WHEN MAX(CASE WHEN version = 'v2' THEN 1 ELSE 0 END) = 1 THEN 'Migrated'
        ELSE 'Not Migrated'
    END as migration_status
FROM api_logs
GROUP BY client_id;
```

## Communication Strategy

### Deprecation Announcement Template
```markdown
# Important: API v1 Deprecation Notice

Dear OpenPolicy API Users,

We are writing to inform you that API v1 will be deprecated on July 1, 2024.

## What This Means
- API v1 will continue to function until July 1, 2024
- After this date, v1 endpoints will return 410 Gone responses
- All users must migrate to API v2 before the deprecation date

## Why We're Deprecating v1
- Enhanced performance in v2
- Better security features
- Improved developer experience
- Cost optimization

## Migration Resources
- [Migration Guide](https://docs.openpolicy.ca/api/migration/v1-to-v2)
- [API v2 Documentation](https://api.openpolicy.ca/v2/docs)
- [Client Libraries](https://github.com/openpolicy/client-libraries)

## Support
- Email: api-support@openpolicy.ca
- Slack: #api-migration
- Office Hours: Every Tuesday 2-3 PM EST

## Timeline
- March 1, 2024: Deprecation announced
- April 1, 2024: Deprecation warnings added to responses
- June 1, 2024: Final reminder sent
- July 1, 2024: API v1 sunset

Thank you for your continued support.

The OpenPolicy Team
```

### In-App Notifications
```python
# SDK notification system
class OpenPolicySDK:
    def __init__(self):
        self.version_check_interval = 86400  # Daily
        self.last_check = 0
    
    async def check_version_status(self):
        if time.time() - self.last_check < self.version_check_interval:
            return
        
        self.last_check = time.time()
        
        try:
            response = await self.client.get("/api/versions")
            versions = response.json()
            
            current_version = self.get_current_version()
            version_info = next(
                (v for v in versions["versions"] if v["version"] == current_version),
                None
            )
            
            if version_info and version_info["status"] == "deprecated":
                warnings.warn(
                    f"API {current_version} is deprecated and will be removed on "
                    f"{version_info['deprecation_date']}. Please upgrade to "
                    f"{versions['recommended']}",
                    DeprecationWarning
                )
        except Exception:
            pass  # Silently fail version check
```

## Testing Strategy

### Version Compatibility Tests
```python
# Pytest fixtures for multi-version testing
import pytest

@pytest.fixture(params=["v1", "v2"])
def api_version(request):
    return request.param

@pytest.fixture
def api_client(api_version):
    return TestClient(app, base_url=f"/api/{api_version}")

# Test both versions
def test_get_bills(api_client, api_version):
    response = api_client.get("/bills")
    assert response.status_code == 200
    
    if api_version == "v1":
        assert "bills" in response.json()
    else:  # v2
        assert "data" in response.json()
        assert "bills" in response.json()["data"]
```

### Contract Tests
```python
# Ensure backward compatibility
class TestBackwardCompatibility:
    def test_v1_response_fields_exist_in_v2(self):
        v1_response = self.get_v1_bill()
        v2_response = self.get_v2_bill()
        
        # All v1 fields must exist in v2
        for field in v1_response.keys():
            assert field in v2_response["data"]
    
    def test_v1_endpoints_exist_in_v2(self):
        v1_endpoints = self.get_v1_endpoints()
        v2_endpoints = self.get_v2_endpoints()
        
        for endpoint in v1_endpoints:
            # Remove version prefix and compare
            path = endpoint.replace("/v1", "")
            assert f"/v2{path}" in v2_endpoints
```

## Implementation Checklist

### New Version Release Checklist
- [ ] Create version branch
- [ ] Update OpenAPI specification
- [ ] Implement version router
- [ ] Add version to gateway configuration
- [ ] Create migration guide
- [ ] Update client libraries
- [ ] Set up version-specific monitoring
- [ ] Configure rate limiting
- [ ] Add to version discovery endpoint
- [ ] Update documentation
- [ ] Create deprecation timeline (if applicable)
- [ ] Set up feature flags
- [ ] Test backward compatibility
- [ ] Performance testing
- [ ] Security review
- [ ] Beta testing period
- [ ] GA announcement

### Version Deprecation Checklist
- [ ] Send initial deprecation notice (6 months)
- [ ] Add deprecation headers
- [ ] Update version discovery endpoint
- [ ] Add in-app warnings
- [ ] Send reminder (3 months)
- [ ] Final notice (1 month)
- [ ] Monitor adoption metrics
- [ ] Support migration issues
- [ ] Sunset date implementation
- [ ] Post-sunset monitoring
- [ ] Remove deprecated code
- [ ] Archive documentation

## Best Practices

### Do's
- ✅ Version from day one
- ✅ Use semantic versioning
- ✅ Maintain backward compatibility when possible
- ✅ Provide clear migration paths
- ✅ Give ample deprecation notice
- ✅ Support multiple versions simultaneously
- ✅ Document all changes thoroughly
- ✅ Monitor version usage
- ✅ Provide client libraries
- ✅ Use feature flags for gradual rollout

### Don'ts
- ❌ Break APIs without version change
- ❌ Remove versions without notice
- ❌ Change response formats in patch versions
- ❌ Use date-based versioning
- ❌ Version too frequently
- ❌ Support too many versions
- ❌ Ignore client feedback
- ❌ Make migration difficult
- ❌ Hide version information
- ❌ Force immediate migrations