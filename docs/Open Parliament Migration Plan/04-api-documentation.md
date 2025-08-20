# API Documentation: OpenParliament.ca

**Base URL**: `https://api.openparliament.ca/`  
**API Version**: v1  
**Content Type**: `application/json`  
**Rate Limiting**: HTTP 429 on exceeded limits

## API Overview

The OpenParliament.ca API provides comprehensive access to Canadian parliamentary data through RESTful endpoints. The API follows hypermedia principles with linked resources and supports advanced filtering, pagination, and multiple output formats.

### Key Features
- **Hyperlinked Resources**: URLs as resource identifiers
- **Advanced Filtering**: Multi-field query capabilities  
- **Comprehensive Pagination**: Offset/limit with navigation
- **Bilingual Content**: English/French data throughout
- **Rate Limiting**: Usage protection and throttling
- **Versioning**: Backward compatibility via headers

## Authentication & Rate Limiting

### API Versioning
```http
# Header-based versioning (recommended)
API-Version: v1

# Query parameter alternative  
GET /politicians/?version=v1
```

### Rate Limits
```
Anonymous Users: 100 requests/hour
Authenticated Users: 1000 requests/hour
Bulk Operations: 10 requests/minute
```

### User-Agent Requirements
```http
User-Agent: YourApp/1.0 (your-email@example.com)
```

## Core Endpoints

### 1. Politicians API

#### List Politicians
```http
GET /politicians/
```

**Query Parameters:**
- `party` - Filter by party slug (e.g., `liberal`, `conservative`)
- `province` - Filter by province code (e.g., `ON`, `BC`, `AB`)
- `current` - Boolean for current MPs only (`true`/`false`)
- `search` - Full-text search across names and ridings
- `limit` - Results per page (default: 20, max: 100)
- `offset` - Pagination offset

**Example Request:**
```http
GET /politicians/?party=liberal&province=ON&current=true&limit=50
```

**Response:**
```json
{
  "objects": [
    {
      "name": "Chrystia Freeland",
      "slug": "chrystia-freeland",
      "current_party": {
        "name_en": "Liberal Party of Canada",
        "short_name_en": "Liberal",
        "slug": "liberal",
        "color": "#DC143C"
      },
      "current_riding": {
        "name_en": "University—Rosedale",
        "province": "ON",
        "id": 35118
      },
      "url": "/politicians/chrystia-freeland/"
    }
  ],
  "pagination": {
    "offset": 0,
    "limit": 20,
    "total_count": 158,
    "next_url": "/politicians/?party=liberal&province=ON&limit=20&offset=20",
    "previous_url": null
  }
}
```

#### Get Individual Politician
```http
GET /politicians/{politician-slug}/
```

**Response:**
```json
{
  "name": "Chrystia Freeland",
  "given_name": "Chrystia",
  "family_name": "Freeland",
  "slug": "chrystia-freeland",
  "gender": "female",
  "email": "chrystia.freeland@parl.gc.ca",
  "phone": "613-992-5234",
  "current_party": {
    "name_en": "Liberal Party of Canada",
    "short_name_en": "Liberal"
  },
  "current_riding": {
    "name_en": "University—Rosedale",
    "province": "ON"
  },
  "memberships": [
    {
      "url": "/politicians/memberships/1234/",
      "start_date": "2019-10-21",
      "end_date": null,
      "party": {
        "name_en": "Liberal Party of Canada",
        "short_name_en": "Liberal"
      },
      "riding": {
        "name_en": "University—Rosedale",
        "province": "ON"
      }
    }
  ],
  "other_info": {
    "favourite_word": ["economy"],
    "twitter": ["cafreeland"],
    "parl_mp_id": ["88317"]
  },
  "links": [
    {
      "url": "https://www.ourcommons.ca/members/en/chrystia-freeland(88317)",
      "note": "Page on ourcommons.ca"
    }
  ],
  "related": {
    "speeches_url": "/speeches/?politician=chrystia-freeland",
    "ballots_url": "/votes/ballots/?politician=chrystia-freeland",
    "sponsored_bills_url": "/bills/?sponsor_politician=chrystia-freeland",
    "activity_rss_url": "/politicians/88317/rss/activity/"
  }
}
```

### 2. Bills API

#### List Bills
```http
GET /bills/
```

**Query Parameters:**
- `session` - Parliamentary session (e.g., `45-1`, `44-1`)
- `status` - Bill status (`introduced`, `passed`, `failed`, `royal_assent`)
- `bill_type` - Type of bill (`government`, `private_member`)
- `sponsor_politician` - Sponsoring MP slug
- `introduced__gte` - Bills introduced after date (`YYYY-MM-DD`)
- `search` - Full-text search in titles and summaries

**Example Request:**
```http
GET /bills/?session=45-1&status=passed&bill_type=government
```

**Response:**
```json
{
  "objects": [
    {
      "session": "45-1",
      "number": "C-5",
      "name": {
        "en": "An Act to enact the Free Trade and Labour Mobility in Canada Act and the Building Canada Act",
        "fr": "Loi édictant la Loi sur le libre-échange et la mobilité de la main-d'œuvre au Canada et la Loi visant à bâtir le Canada"
      },
      "short_title": {
        "en": "One Canadian Economy Act",
        "fr": "Loi sur l'unité de l'économie canadienne"
      },
      "status": "royal_assent",
      "sponsor_politician_url": "/politicians/gary-anandasangaree/",
      "introduced": "2025-05-27",
      "legisinfo_url": "https://www.parl.ca/legisinfo/en/bill/45-1/C-5",
      "url": "/bills/45-1/C-5/"
    }
  ],
  "pagination": {
    "offset": 0,
    "limit": 20,
    "next_url": "/bills/?session=45-1&limit=20&offset=20",
    "previous_url": null
  }
}
```

#### Get Individual Bill
```http
GET /bills/{session}/{bill-number}/
```

**Response:**
```json
{
  "session": "45-1",
  "number": "C-5", 
  "name": {
    "en": "An Act to enact the Free Trade and Labour Mobility in Canada Act and the Building Canada Act",
    "fr": "Loi édictant la Loi sur le libre-échange et la mobilité de la main-d'œuvre au Canada et la Loi visant à bâtir le Canada"
  },
  "short_title": {
    "en": "One Canadian Economy Act",
    "fr": "Loi sur l'unité de l'économie canadienne"
  },
  "status": "royal_assent",
  "status_code": "RoyalAssent",
  "home_chamber": "House",
  "sponsor_politician_url": "/politicians/gary-anandasangaree/",
  "sponsor_politician_membership_url": "/politicians/memberships/4779/",
  "introduced": "2025-05-27",
  "law": "2025-06-20",
  "private_member_bill": false,
  "legisinfo_id": 13539342,
  "legisinfo_url": "https://www.parl.ca/legisinfo/en/bill/45-1/C-5",
  "text_url": "https://www.parl.ca/DocumentViewer/en/13545752",
  "vote_urls": [
    "/votes/45-1/34/",
    "/votes/45-1/33/",
    "/votes/45-1/32/"
  ],
  "related": {
    "bills_url": "/bills/"
  }
}
```

### 3. Votes API

#### List Votes
```http
GET /votes/
```

**Query Parameters:**
- `session` - Parliamentary session
- `bill` - Bill URL (e.g., `/bills/45-1/C-5/`)
- `date` - Vote date, supports `__gte`, `__lte` operators
- `result` - Vote outcome (`Passed`, `Failed`, `Tie`)
- `yea_total__gt` - Minimum yes votes
- `nay_total__gt` - Minimum no votes

**Example Request:**
```http
GET /votes/?session=45-1&date__gte=2025-06-01&result=Passed
```

**Response:**
```json
{
  "objects": [
    {
      "session": "45-1",
      "number": 34,
      "date": "2025-06-20",
      "description": {
        "en": "3rd reading and adoption of Bill C-5, An Act to enact the Free Trade and Labour Mobility in Canada Act and the Building Canada Act (Part 2)",
        "fr": "3e lecture et adoption du projet de loi C-5, Loi édictant la Loi sur le libre-échange et la mobilité de la main-d'œuvre au Canada et la Loi visant à bâtir le Canada (Partie 2)"
      },
      "result": "Passed",
      "yea_total": 306,
      "nay_total": 31,
      "paired_total": 2,
      "bill_url": "/bills/45-1/C-5/",
      "url": "/votes/45-1/34/"
    }
  ],
  "pagination": {
    "offset": 0,
    "limit": 20,
    "next_url": "/votes/?session=45-1&limit=20&offset=20",
    "previous_url": null
  }
}
```

#### Individual Vote Ballots
```http
GET /votes/ballots/
```

**Query Parameters:**
- `vote` - Vote URL (e.g., `/votes/45-1/34/`)
- `politician` - Politician slug
- `ballot` - Ballot choice (`Yes`, `No`, `Paired`, `Didn't vote`)
- `politician_membership` - Membership URL for historical context

**Response:**
```json
{
  "objects": [
    {
      "vote_url": "/votes/45-1/34/",
      "politician_url": "/politicians/chrystia-freeland/",
      "politician_membership_url": "/politicians/memberships/1234/",
      "ballot": "Yes"
    }
  ],
  "pagination": {
    "offset": 0,
    "limit": 20,
    "next_url": "/votes/ballots/?vote=/votes/45-1/34/&limit=20&offset=20",
    "previous_url": null
  }
}
```

### 4. Debates API

#### List Debates
```http
GET /debates/
```

**Query Parameters:**
- `session` - Parliamentary session
- `date` - Debate date, supports ranges
- `date__range` - Date range (`2025-01-01,2025-06-30`)
- `number` - Sequential Hansard number within session

**Response:**
```json
{
  "objects": [
    {
      "date": "2025-06-20",
      "number": "20",
      "session": "45-1",
      "most_frequent_word": {
        "en": "c-5"
      },
      "source_id": 13108027,
      "source_url": "https://www.ourcommons.ca/DocumentViewer/en/45-1/house/sitting-20/hansard",
      "document_type": "Debate",
      "url": "/debates/2025/6/20/"
    }
  ],
  "pagination": {
    "offset": 0,
    "limit": 20,
    "next_url": "/debates/?limit=20&offset=20",
    "previous_url": null
  }
}
```

#### List Speeches  
```http
GET /speeches/
```

**Query Parameters:**
- `document` - Parent debate URL
- `politician` - Speaker politician slug
- `bill_debated` - Bill being discussed
- `mentioned_politician` - MPs mentioned in speech
- `time__range` - Time range for speech timestamps
- `search` - Full-text search across speech content

**Response:**
```json
{
  "objects": [
    {
      "time": "2025-06-20T10:00:00-04:00",
      "politician_url": "/politicians/jenny-kwan/",
      "politician_membership_url": "/politicians/memberships/4248/",
      "content_en": "Mr. Speaker, I rise today on a point of order regarding the government's Bill C-5...",
      "procedural": false,
      "document_url": "/debates/2025/6/20/",
      "h1": "Points of Order",
      "h2": "The Application of Standing Order 69.1 to Bill C-5",
      "bill_debated_url": "/bills/45-1/C-5/",
      "url": "/speeches/12345/"
    }
  ],
  "pagination": {
    "offset": 0,
    "limit": 20,
    "next_url": "/speeches/?document=/debates/2025/6/20/&limit=20&offset=20",
    "previous_url": null
  }
}
```

### 5. Committees API

#### List Committees
```http
GET /committees/
```

**Response:**
```json
{
  "objects": [
    {
      "name": {
        "en": "Access to Information, Privacy and Ethics",
        "fr": "Accès à l'information, protection des renseignements personnels et éthique"
      },
      "short_name": {
        "en": "Information & Ethics",
        "fr": "Information et éthique"
      },
      "slug": "ethics",
      "parent_url": null,
      "sessions": [
        {
          "session": "45-1",
          "acronym": "ETHI",
          "source_url": "https://www.ourcommons.ca/Committees/en/ETHI?parl=45&session=1"
        }
      ],
      "subcommittees": [
        "/committees/ethics-sap/"
      ],
      "url": "/committees/ethics/"
    }
  ]
}
```

#### Committee Meetings
```http
GET /committees/meetings/
```

**Query Parameters:**
- `committee` - Committee slug
- `date__gte` - Meetings after date
- `in_camera` - Public/private meetings (`true`/`false`)
- `session` - Parliamentary session

**Response:**
```json
{
  "objects": [
    {
      "date": "2025-06-19",
      "number": 1,
      "in_camera": false,
      "has_evidence": true,
      "committee_url": "/committees/ethics/",
      "session": "45-1",
      "url": "/committees/ethics/45-1/1/"
    }
  ]
}
```

## Advanced Features

### Filtering and Search

#### Multi-field Filtering
```http
# Complex politician query
GET /politicians/?party=liberal&province=ON&search=finance&current=true

# Bill search with date range
GET /bills/?session=45-1&introduced__gte=2025-01-01&status=passed&search=economy

# Vote filtering by totals
GET /votes/?yea_total__gt=200&nay_total__lt=50&date__gte=2025-06-01
```

#### Full-Text Search
```http
# Search across speech content
GET /speeches/?search=climate+change&politician=elizabeth-may

# Search bills by content
GET /bills/?search=artificial+intelligence&session=45-1
```

### Hypermedia Navigation
```json
{
  "politician": {
    "name": "John Doe",
    "url": "/politicians/john-doe/",
    "current_party": "/parties/liberal/",
    "related": {
      "speeches_url": "/speeches/?politician=john-doe",
      "ballots_url": "/votes/ballots/?politician=john-doe", 
      "sponsored_bills_url": "/bills/?sponsor_politician=john-doe"
    }
  }
}
```

### Data Export Formats

#### JSON (Default)
```http
GET /politicians/
Accept: application/json
```

#### XML Alternative
```http  
GET /politicians/
Accept: application/xml
```

#### CSV Export (where supported)
```http
GET /politicians/?format=csv
```

## Error Handling

### Standard HTTP Status Codes
- `200 OK` - Successful request
- `400 Bad Request` - Invalid parameters
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

### Error Response Format
```json
{
  "error": "Invalid parameter",
  "detail": "The 'date' parameter must be in YYYY-MM-DD format",
  "code": 400
}
```

### Rate Limiting Headers
```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0  
X-RateLimit-Reset: 1629123456
Retry-After: 3600

{
  "error": "Rate limit exceeded",
  "detail": "API rate limit of 100 requests per hour exceeded",
  "code": 429
}
```

## Bulk Data Access

### Database Downloads
```http
GET /data-download/
```

**Available Downloads:**
- Complete PostgreSQL database dump (~1.2GB compressed)
- CSV exports of major tables
- JSON bulk exports by table
- Historical data archives

### RSS Feeds
```http
# MP activity feeds
GET /politicians/{politician-id}/rss/activity/

# Recent votes feed
GET /votes/rss/

# Committee activity
GET /committees/{committee-slug}/rss/
```

## Best Practices

### Efficient API Usage
1. **Use Pagination**: Don't request large datasets at once
2. **Filter Early**: Use query parameters to limit results
3. **Cache Responses**: Implement client-side caching
4. **Follow Links**: Use hypermedia navigation for relationships
5. **Set User-Agent**: Include contact information in requests

### Example Client Implementation
```python
import requests
from time import sleep

class OpenParliamentClient:
    BASE_URL = 'https://api.openparliament.ca'
    
    def __init__(self, user_agent):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent,
            'API-Version': 'v1'
        })
    
    def get_politicians(self, **params):
        """Get politician list with filtering"""
        response = self.session.get(
            f'{self.BASE_URL}/politicians/',
            params=params
        )
        
        if response.status_code == 429:
            sleep(60)  # Wait for rate limit reset
            return self.get_politicians(**params)
            
        response.raise_for_status()
        return response.json()
    
    def get_all_pages(self, url, **params):
        """Get all pages of paginated results"""
        results = []
        
        while url:
            data = self.session.get(url, params=params).json()
            results.extend(data['objects'])
            url = data['pagination']['next_url']
            
        return results

# Usage example
client = OpenParliamentClient('MyApp/1.0 (developer@example.com)')
liberal_mps = client.get_politicians(party='liberal', current=True)
```

---

*This API documentation covers the comprehensive REST API available at api.openparliament.ca, providing programmatic access to 30+ years of Canadian parliamentary data.*