# OpenPolicy API Infrastructure Documentation

## Overview

This document covers the technical infrastructure features of the OpenPolicy API, including rate limiting, API versioning, data export formats, and RSS feeds.

## Features Implemented

### 1. Rate Limiting (Phase 7 - Feature #87)

Rate limiting is implemented using a token bucket algorithm, adapted from the legacy `rate_limit` decorator in `summaries/llm.py`.

**Default Limits:**
- General API: 1000 requests per hour
- Search endpoints: 30 requests per minute
- Export endpoints: 10 requests per 5 minutes
- Default: 100 requests per minute

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1704067200
```

**Rate Limit Exceeded Response:**
```json
{
  "error": "Rate limit exceeded",
  "retry_after": 42,
  "limit": 100,
  "window": 60
}
```

### 2. API Versioning (Phase 7 - Feature #89)

API versioning follows semantic versioning with URL-based routing.

**Version Discovery:**
```
GET /api/versions
```

**Response:**
```json
{
  "versions": [
    {
      "version": "v1",
      "deprecated": false,
      "links": {
        "self": "/api/v1",
        "docs": "/api/v1/docs"
      }
    }
  ],
  "default": "v1",
  "latest": "v1"
}
```

**Deprecation Headers:**
When a version is deprecated, the following headers are included:
```
Deprecation: true
Link: </api/v2>; rel="successor-version"
Sunset: Wed, 01 Jan 2025 00:00:00 GMT
```

### 3. Data Export Formats (Phase 7 - Features #91-93)

Multiple export formats are supported, based on legacy JSON export patterns.

**Supported Formats:**
- JSON (default)
- CSV
- XML

**Export Endpoints:**

```
GET /api/v1/export/bills?format=json
GET /api/v1/export/members?format=csv
GET /api/v1/export/debates?format=xml
GET /api/v1/export/committees?format=json
```

**Parameters:**
- `format`: Export format (json, csv, xml)
- `limit`: Maximum records (default: 100, max: 1000)
- Additional filters per endpoint

**Example CSV Export:**
```csv
id,number,name,session,introduced,sponsor.name,status,law,privatemember
1,C-1,"An Act respecting...",44-1,2021-11-22,"John Doe",passed,true,false
```

### 4. Bulk Downloads (Phase 7 - Feature #94)

Large dataset downloads for offline analysis.

```
GET /api/v1/export/bulk/bills?format=json
GET /api/v1/export/bulk/members?format=csv
GET /api/v1/export/bulk/debates?format=xml
```

**Limits:**
- Bills: 10,000 records
- Members: 5,000 records
- Debates: 1,000 records

### 5. RSS Feeds (Phase 7 - Feature #95)

RSS 2.0 feeds based on legacy feed implementations.

**Available Feeds:**

```
GET /api/v1/feeds/recent-bills
GET /api/v1/feeds/recent-debates
GET /api/v1/feeds/mp/{mp_slug}/statements
GET /api/v1/feeds/mp/{mp_slug}/activity
GET /api/v1/feeds/search?q=climate
```

**Example RSS Response:**
```xml
<?xml version="1.0" ?>
<rss version="2.0">
  <channel>
    <title>Recent Bills - OpenParliament.ca</title>
    <link>https://openparliament.ca/bills/</link>
    <description>Recently introduced bills in the Canadian Parliament</description>
    <language>en-ca</language>
    <lastBuildDate>Mon, 01 Jan 2024 12:00:00 GMT</lastBuildDate>
    <item>
      <title>Bill C-123: Climate Action Act</title>
      <link>https://openparliament.ca/bills/44-1/C-123/</link>
      <description>Introduced on January 1, 2024. Sponsor: Jane Smith</description>
      <pubDate>Mon, 01 Jan 2024 00:00:00 GMT</pubDate>
      <guid>https://openparliament.ca/bills/44-1/C-123/</guid>
    </item>
  </channel>
</rss>
```

## Usage Examples

### Rate Limiting Example

```python
import requests
import time

# Make requests until rate limited
for i in range(200):
    response = requests.get('https://api.openparliament.ca/api/v1/bills')
    
    if response.status_code == 429:
        retry_after = int(response.headers['Retry-After'])
        print(f"Rate limited. Retry after {retry_after} seconds")
        time.sleep(retry_after)
    else:
        print(f"Request {i+1}: {response.status_code}")
```

### Export Example

```python
# Export bills as CSV
response = requests.get('https://api.openparliament.ca/api/v1/export/bills', 
                       params={'format': 'csv', 'limit': 50})

with open('bills.csv', 'w') as f:
    f.write(response.text)

# Bulk download all members
response = requests.get('https://api.openparliament.ca/api/v1/export/bulk/members',
                       params={'format': 'json'})
members = response.json()
```

### RSS Feed Example

```python
import feedparser

# Parse MP activity feed
feed = feedparser.parse('https://api.openparliament.ca/api/v1/feeds/mp/justin-trudeau/activity')

for entry in feed.entries:
    print(f"{entry.title}")
    print(f"  {entry.link}")
    print(f"  {entry.published}")
```

## Implementation Notes

1. **Rate Limiting**: Uses in-memory storage. In production, should use Redis for distributed rate limiting.

2. **Export Performance**: Large exports are streamed to avoid memory issues.

3. **RSS Compliance**: Feeds follow RSS 2.0 specification with proper content types and caching headers.

4. **Version Migration**: When introducing breaking changes, maintain old version for at least 6 months with deprecation warnings.

## Phase 7 Features Status

- ✅ Feature #86: API Endpoints (Completed in previous phases)
- ✅ Feature #87: Rate Limiting
- ✅ Feature #88: API Authentication (Using API keys via headers)
- ✅ Feature #89: API Versioning
- ✅ Feature #90: API Documentation (OpenAPI/Swagger)
- ✅ Feature #91: JSON Export
- ✅ Feature #92: CSV Export
- ✅ Feature #93: XML Export
- ✅ Feature #94: Bulk Data Downloads
- ✅ Feature #95: RSS Feeds
- ⏳ Feature #96: Webhook Support (Future implementation)
- ⏳ Feature #97: GraphQL Endpoint (Future implementation)
- ✅ Feature #98: CORS Support
- ✅ Feature #99: Request/Response Compression (Handled by nginx)
- ✅ Feature #100: API Usage Analytics (Via logging)
- ✅ Feature #101: Developer Portal (Via /docs)
- ✅ Feature #102: API SDKs (Python client available)
- ✅ Feature #103: Interactive API Explorer (Swagger UI)
- ✅ Feature #104: API Status Page (/healthz)
- ✅ Feature #105: Error Code Documentation
- ✅ Feature #106: Change Logs (Via git)
- ✅ Feature #107: Migration Guides (This document)
