# API Design for Consolidated Features

Generated: 2025-08-23

This document provides the consolidated API design for the core features that have multiple implementations. It follows RESTful conventions and provides a unified interface.

## Authentication API (Consolidated)

Base Path: `/api/v1/auth`

### Endpoints

#### User Registration
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "postal_code": "K1A0B1" // Optional, for constituency mapping
}

Response: 201 Created
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "roles": ["citizen"],
    "created_at": "2025-08-23T10:00:00Z"
  },
  "tokens": {
    "access_token": "jwt_token",
    "refresh_token": "refresh_jwt",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

#### User Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "user@example.com", // Email or username
  "password": "SecurePass123!"
}

Response: 200 OK
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_jwt", 
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "roles": ["citizen"]
  }
}
```

#### Token Refresh
```http
POST /api/v1/auth/refresh
Authorization: Bearer {refresh_token}

Response: 200 OK
{
  "access_token": "new_jwt_token",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

#### Password Reset Request
```http
POST /api/v1/auth/password-reset
Content-Type: application/json

{
  "email": "user@example.com"
}

Response: 200 OK
{
  "message": "Password reset email sent if account exists"
}
```

#### Password Reset Confirm
```http
POST /api/v1/auth/password-reset/confirm
Content-Type: application/json

{
  "token": "reset_token_from_email",
  "new_password": "NewSecurePass123!"
}

Response: 200 OK
{
  "message": "Password successfully reset"
}
```

#### OAuth Provider Login
```http
GET /api/v1/auth/oauth/{provider}
// Providers: google, facebook, github

Response: 302 Redirect to OAuth provider

Callback:
GET /api/v1/auth/oauth/{provider}/callback?code={auth_code}

Response: 302 Redirect with tokens in URL params
```

#### Two-Factor Authentication Setup
```http
POST /api/v1/auth/2fa/setup
Authorization: Bearer {access_token}

Response: 200 OK
{
  "secret": "base32_secret",
  "qr_code": "data:image/png;base64,..."
}
```

#### Two-Factor Authentication Verify
```http
POST /api/v1/auth/2fa/verify
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "code": "123456"
}

Response: 200 OK
{
  "message": "2FA enabled successfully"
}
```

#### Current User Profile
```http
GET /api/v1/auth/me
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "roles": ["citizen"],
  "permissions": ["view_bills", "view_members"],
  "constituency": {
    "id": "uuid",
    "name": "Ottawa Centre",
    "mp": {
      "id": "uuid",
      "name": "Jane Smith"
    }
  },
  "preferences": {
    "email_notifications": true,
    "language": "en"
  }
}
```

#### Logout
```http
POST /api/v1/auth/logout
Authorization: Bearer {access_token}

Response: 200 OK
{
  "message": "Successfully logged out"
}
```

### JWT Token Structure
```json
{
  "sub": "user_uuid",
  "email": "user@example.com",
  "roles": ["citizen"],
  "permissions": ["view_bills", "view_members"],
  "iat": 1234567890,
  "exp": 1234571490,
  "jti": "unique_token_id"
}
```

## Feature Flags API

Base Path: `/api/v1/features`

### Endpoints

#### Evaluate Feature Flags for User
```http
POST /api/v1/features/evaluate
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "context": {
    "user_id": "uuid",
    "jurisdiction": "ontario",
    "beta_tester": true
  }
}

Response: 200 OK
{
  "flags": {
    "new_voting_ui": true,
    "ai_bill_summaries": false,
    "enhanced_search": true,
    "committee_livestream": {
      "enabled": true,
      "config": {
        "quality": "HD",
        "chat_enabled": false
      }
    }
  }
}
```

#### Get All Feature Flags (Admin)
```http
GET /api/v1/features
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "flags": [
    {
      "id": "uuid",
      "name": "new_voting_ui",
      "description": "New voting interface design",
      "enabled": true,
      "rollout_percentage": 25,
      "targeting_rules": {
        "rules": [
          {
            "type": "percentage",
            "value": 25
          }
        ]
      },
      "environments": ["production"],
      "created_at": "2025-08-23T10:00:00Z",
      "updated_at": "2025-08-23T10:00:00Z"
    }
  ]
}
```

#### Create Feature Flag (Admin)
```http
POST /api/v1/features
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "name": "new_feature",
  "description": "Description of the feature",
  "enabled": false,
  "rollout_percentage": 0,
  "targeting_rules": {
    "rules": [],
    "default": false
  },
  "environments": ["staging"]
}

Response: 201 Created
{
  "id": "uuid",
  "name": "new_feature",
  ...
}
```

#### Update Feature Flag (Admin)
```http
PATCH /api/v1/features/{flag_id}
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "enabled": true,
  "rollout_percentage": 50,
  "targeting_rules": {
    "rules": [
      {
        "type": "user",
        "operator": "in",
        "values": ["user1", "user2"]
      }
    ]
  }
}

Response: 200 OK
{
  "id": "uuid",
  "name": "new_feature",
  ...
}
```

#### Get Feature Flag History (Admin)
```http
GET /api/v1/features/{flag_id}/history
Authorization: Bearer {admin_token}

Response: 200 OK
{
  "changes": [
    {
      "id": "uuid",
      "changed_by": "admin@example.com",
      "change_type": "update",
      "old_value": {"enabled": false},
      "new_value": {"enabled": true},
      "changed_at": "2025-08-23T10:00:00Z"
    }
  ]
}
```

### Client SDKs

#### JavaScript/TypeScript
```typescript
import { FeatureFlags } from '@openpolicy/feature-flags';

const flags = new FeatureFlags({
  apiKey: 'client_key',
  user: {
    id: 'user_id',
    attributes: {
      jurisdiction: 'ontario',
      beta_tester: true
    }
  }
});

// Check flag
if (flags.isEnabled('new_voting_ui')) {
  // Show new UI
}

// Get flag with config
const livestreamConfig = flags.getFlag('committee_livestream');
if (livestreamConfig.enabled) {
  setupLivestream(livestreamConfig.config);
}
```

#### Python
```python
from openpolicy.features import FeatureFlags

flags = FeatureFlags(
    api_key='server_key',
    default_context={
        'environment': 'production'
    }
)

# Check flag with context
if flags.is_enabled('new_voting_ui', user_id=current_user.id):
    # Use new voting logic
    pass

# Bulk evaluation
user_flags = flags.evaluate_all(
    user_id=current_user.id,
    jurisdiction=current_user.jurisdiction
)
```

## Member Management API (Enhanced)

Base Path: `/api/v1/members`

### Endpoints

#### List Members with Advanced Filtering
```http
GET /api/v1/members?page=1&per_page=20&q=smith&province=ON&party=liberal&current_only=true&has_photo=true

Response: 200 OK
{
  "data": [
    {
      "id": "uuid",
      "full_name": "Jane Smith",
      "first_name": "Jane",
      "last_name": "Smith",
      "party": {
        "id": "uuid",
        "name": "Liberal Party",
        "short_name": "LIB",
        "color": "#D71920"
      },
      "constituency": "Ottawa Centre",
      "province": "Ontario",
      "photo_url": "https://cdn.openpolicy.ca/members/jane-smith.jpg",
      "is_current": true,
      "roles": ["MP", "Committee Chair"],
      "email": "jane.smith@parl.gc.ca",
      "social_media": {
        "twitter": "@janesmith",
        "facebook": "janesmith.mp"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 338,
    "pages": 17
  },
  "facets": {
    "provinces": {
      "ON": 121,
      "QC": 78,
      "BC": 42
    },
    "parties": {
      "liberal": 157,
      "conservative": 119,
      "ndp": 25
    }
  }
}
```

#### Get Member Detail with Full Activity
```http
GET /api/v1/members/{member_id}?include=bills,votes,speeches,committees

Response: 200 OK
{
  "id": "uuid",
  "full_name": "Jane Smith",
  "bio": "Jane Smith has served...",
  "education": ["BA Political Science, University of Ottawa", "JD, Osgoode Hall"],
  "profession": "Lawyer",
  "first_elected": "2015-10-19",
  "offices": [
    {
      "type": "constituency",
      "address": "123 Main St, Ottawa, ON K1A 0A6",
      "phone": "613-555-0123",
      "fax": "613-555-0124"
    },
    {
      "type": "parliament",
      "address": "House of Commons, Ottawa, ON K1A 0A6",
      "phone": "613-555-0125"
    }
  ],
  "activity": {
    "bills_sponsored": 12,
    "bills_seconded": 45,
    "votes_total": 1234,
    "votes_present": 1180,
    "attendance_rate": 0.956,
    "speeches_count": 89,
    "questions_asked": 34
  },
  "recent_bills": [...],
  "recent_votes": [...],
  "committee_memberships": [
    {
      "committee": {
        "id": "uuid",
        "name": "Finance Committee",
        "acronym": "FINA"
      },
      "role": "Chair",
      "start_date": "2021-11-23"
    }
  ]
}
```

#### Compare Members
```http
POST /api/v1/members/compare
Content-Type: application/json

{
  "member_ids": ["uuid1", "uuid2", "uuid3"],
  "metrics": ["voting_similarity", "bill_cooperation", "attendance", "activity"]
}

Response: 200 OK
{
  "comparison": {
    "voting_similarity": {
      "uuid1_uuid2": 0.78,
      "uuid1_uuid3": 0.23,
      "uuid2_uuid3": 0.31
    },
    "bill_cooperation": {
      "co_sponsored": [
        {
          "members": ["uuid1", "uuid2"],
          "bills": ["C-123", "C-456"]
        }
      ]
    },
    "attendance": {
      "uuid1": 0.956,
      "uuid2": 0.923,
      "uuid3": 0.978
    }
  }
}
```

#### Member Activity Timeline
```http
GET /api/v1/members/{member_id}/timeline?from=2024-01-01&to=2024-12-31&types=bills,votes,speeches

Response: 200 OK
{
  "timeline": [
    {
      "date": "2024-12-20",
      "type": "speech",
      "title": "Speech on Bill C-123",
      "description": "Spoke in favor of the climate action bill",
      "link": "/debates/2024-12-20#speech-123"
    },
    {
      "date": "2024-12-19",
      "type": "vote",
      "title": "Vote on Bill C-456",
      "vote": "Yes",
      "result": "Passed",
      "link": "/votes/2024-12-19/vote-456"
    }
  ]
}
```

## WebSocket API for Real-time Updates

Connection: `wss://api.openpolicy.ca/v1/ws`

### Authentication
```javascript
const ws = new WebSocket('wss://api.openpolicy.ca/v1/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'auth',
    token: 'jwt_access_token'
  }));
};
```

### Subscribe to Updates
```javascript
// Subscribe to member updates
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'members',
  filters: {
    member_ids: ['uuid1', 'uuid2']
  }
}));

// Subscribe to feature flag changes
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'features',
  filters: {
    flags: ['new_voting_ui', 'ai_summaries']
  }
}));

// Receive updates
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'member_update':
      // Handle member activity update
      updateMemberCard(data.member_id, data.update);
      break;
      
    case 'feature_update':
      // Handle feature flag change
      if (data.flag === 'new_voting_ui' && data.enabled) {
        location.reload(); // Reload to get new UI
      }
      break;
  }
};
```

## Error Responses

All APIs use consistent error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  },
  "request_id": "req_123456"
}
```

### Common Error Codes
- `UNAUTHORIZED` - Invalid or missing authentication
- `FORBIDDEN` - Insufficient permissions
- `NOT_FOUND` - Resource not found
- `VALIDATION_ERROR` - Request validation failed
- `RATE_LIMITED` - Too many requests
- `INTERNAL_ERROR` - Server error

## Rate Limiting

All APIs implement rate limiting:

- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour
- Admin: 10000 requests/hour

Headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## API Versioning

All APIs support version negotiation:

1. URL versioning: `/api/v1/...`, `/api/v2/...`
2. Header versioning: `Accept: application/vnd.openpolicy.v2+json`
3. Query parameter: `?version=2` (deprecated)