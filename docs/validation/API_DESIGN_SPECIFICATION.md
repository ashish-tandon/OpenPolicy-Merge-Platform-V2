# API Design Specification
Generated: 2025-01-19 | Iteration: 5/10

## 🎯 API Design Principles

### Core Principles
1. **RESTful**: Follow REST conventions strictly
2. **Versioned**: API v1, v2 with clear deprecation
3. **Consistent**: Uniform response formats
4. **Bilingual**: All responses in EN/FR
5. **Performant**: <200ms response time
6. **Secure**: OAuth2, rate limiting, audit logs

## 📊 API Structure

### Base URLs
```yaml
production:
  - https://api.openparliament.ca/v1
  - https://api.parlement-ouvert.ca/v1
  
staging:
  - https://staging-api.openparliament.ca/v1
  
development:
  - http://localhost:8080/api/v1
```

### Authentication
```http
# OAuth2 Bearer Token
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# API Key (deprecated in v2)
X-API-Key: op_live_1234567890abcdef

# Language Selection
Accept-Language: fr-CA, en-CA;q=0.9
```

## 🔧 Complete API Endpoints

### Bills API
```yaml
/api/v1/bills:
  GET:
    summary: List all bills
    parameters:
      - page: integer (default: 1)
      - per_page: integer (default: 20, max: 100)
      - session: string (e.g., "44-1")
      - status: enum [first_reading, second_reading, third_reading, committee, senate, royal_assent]
      - sponsor: string (member name or ID)
      - keyword: string (search in title/summary)
      - introduced_after: date
      - introduced_before: date
      - sort: enum [introduced, -introduced, number, -number, last_updated]
      - lang: enum [en, fr]
    response:
      200:
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    $ref: '#/components/schemas/Bill'
                meta:
                  $ref: '#/components/schemas/Pagination'
                links:
                  $ref: '#/components/schemas/Links'

  POST:
    summary: Track a bill (authenticated)
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              bill_id: integer
              notification_types: array
    response:
      201:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BillTracking'

/api/v1/bills/{id}:
  GET:
    summary: Get bill details
    parameters:
      - id: integer (required)
      - include: array [votes, amendments, speeches, committees]
      - lang: enum [en, fr]
    response:
      200:
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  $ref: '#/components/schemas/BillDetail'
                included:
                  type: array
                  description: Related resources if requested

/api/v1/bills/{id}/votes:
  GET:
    summary: Get votes on a bill
    response:
      200:
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    $ref: '#/components/schemas/Vote'

/api/v1/bills/{id}/amendments:
  GET:
    summary: Get bill amendments
    response:
      200:
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    $ref: '#/components/schemas/Amendment'

/api/v1/bills/{id}/timeline:
  GET:
    summary: Get bill progress timeline
    response:
      200:
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    $ref: '#/components/schemas/TimelineEvent'
```

### Members API
```yaml
/api/v1/members:
  GET:
    summary: List all members
    parameters:
      - page: integer
      - per_page: integer
      - parliament: integer (e.g., 44)
      - party: string (party code or name)
      - province: string (2-letter code)
      - name: string (search)
      - current: boolean (default: true)
      - include: array [votes, bills, speeches, committees]
    response:
      200:
        schema:
          $ref: '#/components/schemas/MemberList'

/api/v1/members/{id}:
  GET:
    summary: Get member details
    parameters:
      - id: integer or string (ID or slug)
      - include: array [votes, bills, speeches, committees, contact]
    response:
      200:
        schema:
          $ref: '#/components/schemas/MemberDetail'

/api/v1/members/{id}/votes:
  GET:
    summary: Get member's voting record
    parameters:
      - session: string
      - bill: integer
      - result: enum [yea, nay, paired, absent]
      - page: integer
      - per_page: integer
    response:
      200:
        schema:
          $ref: '#/components/schemas/MemberVotes'

/api/v1/members/by-postal-code/{postal_code}:
  GET:
    summary: Find MP by postal code
    parameters:
      - postal_code: string (required, format: "K1A0A6")
    response:
      200:
        schema:
          $ref: '#/components/schemas/Member'
      404:
        description: No MP found for postal code
```

### Votes API (Fixed)
```yaml
/api/v1/votes:
  GET:
    summary: List all votes
    parameters:
      - page: integer
      - per_page: integer
      - session: string
      - date_from: date
      - date_to: date
      - result: enum [agreed, negatived, tied]
      - type: enum [recorded, voice, unanimous]
    response:
      200:
        schema:
          $ref: '#/components/schemas/VoteList'

/api/v1/votes/{id}:
  GET:
    summary: Get vote details
    parameters:
      - id: integer
      - include: array [member_votes, party_summary]
    response:
      200:
        schema:
          $ref: '#/components/schemas/VoteDetail'

/api/v1/votes/{id}/members:
  GET:
    summary: Get individual member votes
    parameters:
      - party: string
      - vote: enum [yea, nay, paired, absent]
    response:
      200:
        schema:
          $ref: '#/components/schemas/MemberVoteList'
```

### Committees API
```yaml
/api/v1/committees:
  GET:
    summary: List all committees
    parameters:
      - type: enum [standing, special, joint, subcommittee]
      - session: string
      - active: boolean
    response:
      200:
        schema:
          $ref: '#/components/schemas/CommitteeList'

/api/v1/committees/{id}:
  GET:
    summary: Get committee details
    parameters:
      - id: string (slug)
      - include: array [members, meetings, reports, bills]
    response:
      200:
        schema:
          $ref: '#/components/schemas/CommitteeDetail'

/api/v1/committees/{id}/meetings:
  GET:
    summary: Get committee meetings
    parameters:
      - date_from: date
      - date_to: date
      - page: integer
    response:
      200:
        schema:
          $ref: '#/components/schemas/MeetingList'
```

### Debates API
```yaml
/api/v1/debates:
  GET:
    summary: List debate days
    parameters:
      - date_from: date
      - date_to: date
      - type: enum [house, committee, senate]
      - page: integer
    response:
      200:
        schema:
          $ref: '#/components/schemas/DebateList'

/api/v1/debates/{date}:
  GET:
    summary: Get debate for specific date
    parameters:
      - date: date (YYYY-MM-DD)
      - type: enum [house, committee, senate]
      - include: array [statements, topics, speakers]
    response:
      200:
        schema:
          $ref: '#/components/schemas/DebateDetail'

/api/v1/debates/{date}/statements:
  GET:
    summary: Get debate statements
    parameters:
      - speaker: string (member name or ID)
      - topic: string
      - keyword: string
      - time_from: time
      - time_to: time
      - page: integer
    response:
      200:
        schema:
          $ref: '#/components/schemas/StatementList'

/api/v1/debates/search:
  GET:
    summary: Search debate transcripts
    parameters:
      - q: string (required)
      - date_from: date
      - date_to: date
      - speaker: string
      - type: enum [house, committee, senate]
      - page: integer
    response:
      200:
        schema:
          $ref: '#/components/schemas/DebateSearchResults'
```

### Search API
```yaml
/api/v1/search:
  GET:
    summary: Global search
    parameters:
      - q: string (required)
      - type: array [bills, members, debates, committees, votes]
      - date_from: date
      - date_to: date
      - page: integer
      - lang: enum [en, fr]
    response:
      200:
        schema:
          $ref: '#/components/schemas/SearchResults'

/api/v1/search/suggest:
  GET:
    summary: Search suggestions
    parameters:
      - q: string (required, min: 2 chars)
      - type: array [bills, members, topics]
      - limit: integer (default: 5, max: 10)
    response:
      200:
        schema:
          type: object
          properties:
            suggestions:
              type: array
              items:
                type: object
                properties:
                  text: string
                  type: string
                  id: string
```

## 📦 Data Schemas

### Bill Schema
```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "integer",
      "example": 1234
    },
    "number": {
      "type": "string",
      "example": "C-123"
    },
    "title": {
      "type": "object",
      "properties": {
        "en": {
          "type": "string",
          "example": "An Act to amend the Criminal Code"
        },
        "fr": {
          "type": "string",
          "example": "Loi modifiant le Code criminel"
        }
      }
    },
    "summary": {
      "type": "object",
      "properties": {
        "en": {"type": "string"},
        "fr": {"type": "string"}
      }
    },
    "status": {
      "type": "string",
      "enum": ["first_reading", "second_reading", "committee", "third_reading", "senate", "royal_assent"]
    },
    "introduced": {
      "type": "string",
      "format": "date",
      "example": "2024-03-15"
    },
    "sponsor": {
      "$ref": "#/components/schemas/MemberSummary"
    },
    "urls": {
      "type": "object",
      "properties": {
        "legisinfo": {"type": "string"},
        "parl": {"type": "string"},
        "self": {"type": "string"}
      }
    }
  }
}
```

### Vote Schema
```json
{
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "date": {"type": "string", "format": "date-time"},
    "number": {"type": "integer"},
    "description": {
      "type": "object",
      "properties": {
        "en": {"type": "string"},
        "fr": {"type": "string"}
      }
    },
    "result": {
      "type": "string",
      "enum": ["agreed", "negatived", "tied"]
    },
    "totals": {
      "type": "object",
      "properties": {
        "yea": {"type": "integer"},
        "nay": {"type": "integer"},
        "paired": {"type": "integer"},
        "absent": {"type": "integer"}
      }
    },
    "bill": {
      "$ref": "#/components/schemas/BillSummary"
    }
  }
}
```

### Member Schema
```json
{
  "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "name": {"type": "string"},
    "party": {
      "type": "object",
      "properties": {
        "code": {"type": "string"},
        "name": {
          "type": "object",
          "properties": {
            "en": {"type": "string"},
            "fr": {"type": "string"}
          }
        }
      }
    },
    "constituency": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "province": {"type": "string"}
      }
    },
    "email": {"type": "string"},
    "photo": {"type": "string", "format": "uri"}
  }
}
```

## 🔄 Response Format

### Standard Response
```json
{
  "data": {...},
  "meta": {
    "timestamp": "2024-01-19T10:30:00Z",
    "version": "1.0",
    "language": "en"
  },
  "links": {
    "self": "https://api.openparliament.ca/v1/bills/123",
    "first": "...",
    "prev": "...",
    "next": "...",
    "last": "..."
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Bill not found",
    "details": {
      "bill_id": 999,
      "suggestion": "Use /api/v1/bills to list available bills"
    }
  },
  "meta": {
    "timestamp": "2024-01-19T10:30:00Z",
    "request_id": "req_1234567890"
  }
}
```

### Pagination
```json
{
  "meta": {
    "pagination": {
      "page": 2,
      "per_page": 20,
      "total_pages": 50,
      "total_items": 1000
    }
  }
}
```

## 🚦 Rate Limiting

### Limits
```yaml
anonymous:
  - 60 requests per minute
  - 1000 requests per hour
  
authenticated:
  - 600 requests per minute
  - 10000 requests per hour
  
premium:
  - 6000 requests per minute
  - 100000 requests per hour
```

### Headers
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1642598400
X-RateLimit-Retry-After: 58
```

## 🌐 Internationalization

### Language Selection Priority
1. `lang` query parameter
2. `Accept-Language` header
3. User preference (if authenticated)
4. Default to English

### Bilingual Response Example
```json
{
  "data": {
    "id": 123,
    "title": {
      "en": "Budget Implementation Act",
      "fr": "Loi d'exécution du budget"
    },
    "current_text": {
      "@lang": "en",
      "@value": "Budget Implementation Act"
    }
  }
}
```

## 🔐 Security

### Authentication Methods
1. **OAuth2**: Preferred for applications
2. **JWT**: For user sessions
3. **API Key**: Legacy support only

### Security Headers
```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

---
End of Iteration 5/10