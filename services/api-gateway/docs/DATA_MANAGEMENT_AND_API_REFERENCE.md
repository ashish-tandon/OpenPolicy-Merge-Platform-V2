# OpenParliament.ca V2 - Data Management & API Reference
**Following FUNDAMENTAL RULE: NEVER REINVENT THE WHEEL**

Generated: 2025-08-20T20:00:00.000000

## Executive Summary

This document provides comprehensive documentation for the OpenParliament.ca V2 data management system and API endpoints. It covers all data sources, schemas, and API routes for the unified multi-level government platform.

## 1. Data Management Overview

### 1.1 Database Architecture
The OpenParliament.ca V2 platform uses a **3-schema architecture**:

1. **OpenParliament Schema** - Federal bills, votes, debates
2. **Represent Canada Schema** - Federal representatives, contact info
3. **Multi-Level Government Schema** - Unified schema for all government levels

### 1.2 Data Flow Architecture
```
Legacy Sources → ETL Service → Database → API Gateway → Frontend/Users
     ↓              ↓           ↓          ↓
OpenParliament   Transform   Store     Serve
Represent Canada  Validate   Index     Cache
Civic Scrapers   Enrich     Query     Rate Limit
Scrapers-CA      Log        Monitor   Document
```

### 1.3 Data Provenance Tracking
Every piece of data is tracked with:
- **Source ID**: Unique identifier for the data source
- **Jurisdiction ID**: Which government level/jurisdiction
- **Ingestion Timestamp**: When the data was collected
- **Source URL**: Original source of the data
- **Legacy Module/Class**: If from legacy scrapers

## 2. API Endpoints Reference

### 2.1 Base URL
```
https://api.openparliament.ca/v1
```

### 2.2 Authentication
Currently, the API is open for read access. Write operations require authentication (to be implemented).

### 2.3 Rate Limiting
- **Standard Rate Limit**: 1000 requests per hour per IP
- **Burst Rate Limit**: 100 requests per minute per IP
- **Search Rate Limit**: 100 requests per hour per IP

## 3. Multi-Level Government API Endpoints

### 3.1 Government Levels

#### List Government Levels
```http
GET /api/v1/multi-level-government/government-levels
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20, max: 100)

**Response:**
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Federal",
      "description": "Federal government of Canada",
      "level_order": 1,
      "created_at": "2025-08-20T20:00:00Z",
      "updated_at": "2025-08-20T20:00:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "name": "Provincial",
      "description": "Provincial and territorial governments",
      "level_order": 2,
      "created_at": "2025-08-20T20:00:00Z",
      "updated_at": "2025-08-20T20:00:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "name": "Municipal",
      "description": "Municipal governments and city councils",
      "level_order": 3,
      "created_at": "2025-08-20T20:00:00Z",
      "updated_at": "2025-08-20T20:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 3,
    "total_pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

#### Get Government Level by ID
```http
GET /api/v1/multi-level-government/government-levels/{level_id}
```

**Response:** Single government level object

### 3.2 Jurisdictions

#### List Jurisdictions
```http
GET /api/v1/multi-level-government/jurisdictions
```

**Query Parameters:**
- `government_level` (optional): Filter by government level ID
- `province` (optional): Filter by province/territory
- `jurisdiction_type` (optional): Filter by jurisdiction type
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20, max: 100)

**Jurisdiction Types:**
- `legislature` - Provincial legislatures
- `parliament` - Federal parliament
- `city_council` - Municipal city councils
- `town_council` - Municipal town councils
- `regional_council` - Regional councils
- `first_nations` - First Nations governments

**Response:**
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440003",
      "name": "House of Commons",
      "code": "federal_house_of_commons",
      "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
      "province": null,
      "jurisdiction_type": "parliament",
      "website": "https://www.ourcommons.ca",
      "extras": {},
      "government_level": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Federal",
        "description": "Federal government of Canada",
        "level_order": 1,
        "created_at": "2025-08-20T20:00:00Z",
        "updated_at": "2025-08-20T20:00:00Z"
      },
      "created_at": "2025-08-20T20:00:00Z",
      "updated_at": "2025-08-20T20:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 135,
    "total_pages": 7,
    "has_next": true,
    "has_prev": false
  }
}
```

#### Get Jurisdiction by ID
```http
GET /api/v1/multi-level-government/jurisdictions/{jurisdiction_id}
```

**Response:** Single jurisdiction object with government level details

### 3.3 Representatives

#### List Representatives
```http
GET /api/v1/multi-level-government/representatives
```

**Query Parameters:**
- `q` (optional): Search query for representative name
- `jurisdiction_id` (optional): Filter by jurisdiction ID
- `government_level` (optional): Filter by government level ID
- `province` (optional): Filter by province/territory
- `party` (optional): Filter by political party
- `position` (optional): Filter by position
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20, max: 100)

**Representative Positions:**
- `mp` - Member of Parliament (Federal)
- `mla` - Member of Legislative Assembly (Provincial)
- `mpp` - Member of Provincial Parliament (Ontario)
- `mayor` - Municipal mayor
- `councillor` - Municipal councillor
- `deputy_mayor` - Deputy mayor
- `chair` - Council chair
- `deputy_chair` - Deputy chair

**Response:**
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440004",
      "name": "Justin Trudeau",
      "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440003",
      "party": "Liberal Party of Canada",
      "position": "mp",
      "riding": "Papineau",
      "email": "justin.trudeau@parl.gc.ca",
      "phone": "+1-613-992-4211",
      "website": "https://www.justintrudeau.ca",
      "extras": {},
      "metadata_json": {},
      "jurisdiction": {
        "id": "550e8400-e29b-41d4-a716-446655440003",
        "name": "House of Commons",
        "code": "federal_house_of_commons",
        "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
        "province": null,
        "jurisdiction_type": "parliament",
        "website": "https://www.ourcommons.ca",
        "extras": {},
        "government_level": {
          "id": "550e8400-e29b-41d4-a716-446655440000",
          "name": "Federal",
          "description": "Federal government of Canada",
          "level_order": 1,
          "created_at": "2025-08-20T20:00:00Z",
          "updated_at": "2025-08-20T20:00:00Z"
        },
        "created_at": "2025-08-20T20:00:00Z",
        "updated_at": "2025-08-20T20:00:00Z"
      },
      "created_at": "2025-08-20T20:00:00Z",
      "updated_at": "2025-08-20T20:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 1200,
    "total_pages": 60,
    "has_next": true,
    "has_prev": false
  }
}
```

#### Get Representative by ID
```http
GET /api/v1/multi-level-government/representatives/{representative_id}
```

**Response:** Single representative object with jurisdiction and government level details

### 3.4 Offices

#### List Offices
```http
GET /api/v1/multi-level-government/offices
```

**Query Parameters:**
- `jurisdiction_id` (optional): Filter by jurisdiction ID
- `government_level` (optional): Filter by government level ID
- `office_type` (optional): Filter by office type
- `province` (optional): Filter by province/territory
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20, max: 100)

**Office Types:**
- `constituency` - Constituency offices
- `parliamentary` - Parliamentary offices
- `city_hall` - City hall offices
- `town_hall` - Town hall offices
- `regional_office` - Regional government offices
- `legislative` - Legislative building offices

**Response:**
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440005",
      "name": "Papineau Constituency Office",
      "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440003",
      "office_type": "constituency",
      "location": "123 Main Street, Montreal, QC",
      "phone": "+1-514-555-0123",
      "email": "papineau@liberal.ca",
      "extras": {},
      "jurisdiction": {
        "id": "550e8400-e29b-41d4-a716-446655440003",
        "name": "House of Commons",
        "code": "federal_house_of_commons",
        "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
        "province": null,
        "jurisdiction_type": "parliament",
        "website": "https://www.ourcommons.ca",
        "extras": {},
        "government_level": {
          "id": "550e8400-e29b-41d4-a716-446655440000",
          "name": "Federal",
          "description": "Federal government of Canada",
          "level_order": 1,
          "created_at": "2025-08-20T20:00:00Z",
          "updated_at": "2025-08-20T20:00:00Z"
        },
        "created_at": "2025-08-20T20:00:00Z",
        "updated_at": "2025-08-20T20:00:00Z"
      },
      "created_at": "2025-08-20T20:00:00Z",
      "updated_at": "2025-08-20T20:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 500,
    "total_pages": 25,
    "has_next": true,
    "has_prev": false
  }
}
```

#### Get Office by ID
```http
GET /api/v1/multi-level-government/offices/{office_id}
```

**Response:** Single office object with jurisdiction and government level details

### 3.5 Bills

#### List Bills
```http
GET /api/v1/multi-level-government/bills
```

**Query Parameters:**
- `q` (optional): Search query for bill title
- `jurisdiction_id` (optional): Filter by jurisdiction ID
- `government_level` (optional): Filter by government level ID
- `status` (optional): Filter by bill status
- `sponsor_id` (optional): Filter by sponsor representative ID
- `introduced_after` (optional): Filter by introduction date (after)
- `introduced_before` (optional): Filter by introduction date (before)
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20, max: 100)

**Bill Statuses:**
- `introduced` - Bill introduced
- `first_reading` - First reading completed
- `second_reading` - Second reading completed
- `third_reading` - Third reading completed
- `committee` - In committee
- `royal_assent` - Royal assent granted
- `enacted` - Bill enacted into law
- `defeated` - Bill defeated
- `withdrawn` - Bill withdrawn

**Response:**
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440006",
      "title": "An Act to amend the Criminal Code",
      "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440003",
      "bill_number": "C-123",
      "summary": "A bill to amend the Criminal Code...",
      "status": "introduced",
      "introduced_date": "2025-08-20T20:00:00Z",
      "sponsor_id": "550e8400-e29b-41d4-a716-446655440004",
      "extras": {},
      "jurisdiction": {
        "id": "550e8400-e29b-41d4-a716-446655440003",
        "name": "House of Commons",
        "code": "federal_house_of_commons",
        "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
        "province": null,
        "jurisdiction_type": "parliament",
        "website": "https://www.ourcommons.ca",
        "extras": {},
        "government_level": {
          "id": "550e8400-e29b-41d4-a716-446655440000",
          "name": "Federal",
          "description": "Federal government of Canada",
          "level_order": 1,
          "created_at": "2025-08-20T20:00:00Z",
          "updated_at": "2025-08-20T20:00:00Z"
        },
        "created_at": "2025-08-20T20:00:00Z",
        "updated_at": "2025-08-20T20:00:00Z"
      },
      "sponsor": {
        "id": "550e8400-e29b-41d4-a716-446655440004",
        "name": "Justin Trudeau",
        "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440003",
        "party": "Liberal Party of Canada",
        "position": "mp",
        "riding": "Papineau",
        "email": "justin.trudeau@parl.gc.ca",
        "phone": "+1-613-992-4211",
        "website": "https://www.justintrudeau.ca",
        "extras": {},
        "metadata_json": {},
        "jurisdiction": {
          "id": "550e8400-e29b-41d4-a716-446655440003",
          "name": "House of Commons",
          "code": "federal_house_of_commons",
          "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
          "province": null,
          "jurisdiction_type": "parliament",
          "website": "https://www.ourcommons.ca",
          "extras": {},
          "government_level": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Federal",
            "description": "Federal government of Canada",
            "level_order": 1,
            "created_at": "2025-08-20T20:00:00Z",
            "updated_at": "2025-08-20T20:00:00Z"
          },
          "created_at": "2025-08-20T20:00:00Z",
          "updated_at": "2025-08-20T20:00:00Z"
        },
        "created_at": "2025-08-20T20:00:00Z",
        "updated_at": "2025-08-20T20:00:00Z"
      },
      "created_at": "2025-08-20T20:00:00Z",
      "updated_at": "2025-08-20T20:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 10000,
    "total_pages": 500,
    "has_next": true,
    "has_prev": false
  }
}
```

#### Get Bill by ID
```http
GET /api/v1/multi-level-government/bills/{bill_id}
```

**Response:** Single bill object with jurisdiction, government level, and sponsor details

### 3.6 Votes

#### List Votes
```http
GET /api/v1/multi-level-government/votes
```

**Query Parameters:**
- `bill_id` (optional): Filter by bill ID
- `representative_id` (optional): Filter by representative ID
- `vote_position` (optional): Filter by vote position
- `vote_after` (optional): Filter by vote date (after)
- `vote_before` (optional): Filter by vote date (before)
- `session` (optional): Filter by session
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20, max: 100)

**Vote Positions:**
- `yes` - Voted in favor
- `no` - Voted against
- `abstain` - Abstained from voting
- `absent` - Absent from vote
- `paired` - Paired vote

**Response:**
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440007",
      "bill_id": "550e8400-e29b-41d4-a716-446655440006",
      "representative_id": "550e8400-e29b-41d4-a716-446655440004",
      "vote_position": "yes",
      "vote_date": "2025-08-20T20:00:00Z",
      "session": "44-1",
      "extras": {},
      "bill": {
        "id": "550e8400-e29b-41d4-a716-446655440006",
        "title": "An Act to amend the Criminal Code",
        "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440003",
        "bill_number": "C-123",
        "summary": "A bill to amend the Criminal Code...",
        "status": "introduced",
        "introduced_date": "2025-08-20T20:00:00Z",
        "sponsor_id": "550e8400-e29b-41d4-a716-446655440004",
        "extras": {},
        "jurisdiction": {
          "id": "550e8400-e29b-41d4-a716-446655440003",
          "name": "House of Commons",
          "code": "federal_house_of_commons",
          "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
          "province": null,
          "jurisdiction_type": "parliament",
          "website": "https://www.ourcommons.ca",
          "extras": {},
          "government_level": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Federal",
            "description": "Federal government of Canada",
            "level_order": 1,
            "created_at": "2025-08-20T20:00:00Z",
            "updated_at": "2025-08-20T20:00:00Z"
          },
          "created_at": "2025-08-20T20:00:00Z",
          "updated_at": "2025-08-20T20:00:00Z"
        },
        "sponsor": null,
        "created_at": "2025-08-20T20:00:00Z",
        "updated_at": "2025-08-20T20:00:00Z"
      },
      "representative": {
        "id": "550e8400-e29b-41d4-a716-446655440004",
        "name": "Justin Trudeau",
        "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440003",
        "party": "Liberal Party of Canada",
        "position": "mp",
        "riding": "Papineau",
        "email": "justin.trudeau@parl.gc.ca",
        "phone": "+1-613-992-4211",
        "website": "https://www.justintrudeau.ca",
        "extras": {},
        "metadata_json": {},
        "jurisdiction": {
          "id": "550e8400-e29b-41d4-a716-446655440003",
          "name": "House of Commons",
          "code": "federal_house_of_commons",
          "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
          "province": null,
          "jurisdiction_type": "parliament",
          "website": "https://www.ourcommons.ca",
          "extras": {},
          "government_level": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Federal",
            "description": "Federal government of Canada",
            "level_order": 1,
            "created_at": "2025-08-20T20:00:00Z",
            "updated_at": "2025-08-20T20:00:00Z"
          },
          "created_at": "2025-08-20T20:00:00Z",
          "updated_at": "2025-08-20T20:00:00Z"
        },
        "created_at": "2025-08-20T20:00:00Z",
        "updated_at": "2025-08-20T20:00:00Z"
      },
      "created_at": "2025-08-20T20:00:00Z",
      "updated_at": "2025-08-20T20:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 50000,
    "total_pages": 2500,
    "has_next": true,
    "has_prev": false
  }
}
```

### 3.7 Data Sources

#### List Data Sources
```http
GET /api/v1/multi-level-government/data-sources
```

**Query Parameters:**
- `jurisdiction_id` (optional): Filter by jurisdiction ID
- `government_level` (optional): Filter by government level ID
- `source_type` (optional): Filter by source type
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20, max: 100)

**Response:**
```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440008",
      "name": "OpenParliament Federal Bills",
      "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440003",
      "source_type": "api",
      "url": "https://openparliament.ca/api/v1/bills/",
      "legacy_module": "openparliament",
      "legacy_class": "BillsScraper",
      "last_updated": "2025-08-20T20:00:00Z",
      "extras": {},
      "jurisdiction": {
        "id": "550e8400-e29b-41d4-a716-446655440003",
        "name": "House of Commons",
        "code": "federal_house_of_commons",
        "government_level_id": "550e8400-e29b-41d4-a716-446655440000",
        "province": null,
        "jurisdiction_type": "parliament",
        "website": "https://www.ourcommons.ca",
        "extras": {},
        "government_level": {
          "id": "550e8400-e29b-41d4-a716-446655440000",
          "name": "Federal",
          "description": "Federal government of Canada",
          "level_order": 1,
          "created_at": "2025-08-20T20:00:00Z",
          "updated_at": "2025-08-20T20:00:00Z"
        },
        "created_at": "2025-08-20T20:00:00Z",
        "updated_at": "2025-08-20T20:00:00Z"
      },
      "created_at": "2025-08-20T20:00:00Z",
      "updated_at": "2025-08-20T20:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 135,
    "total_pages": 7,
    "has_next": true,
    "has_prev": false
  }
}
```

### 3.8 Statistics

#### System Statistics
```http
GET /api/v1/multi-level-government/stats/system
```

**Response:**
```json
{
  "total_government_levels": 3,
  "total_jurisdictions": 135,
  "total_representatives": 1200,
  "total_bills": 10000,
  "total_votes": 50000,
  "total_offices": 500,
  "total_data_sources": 135,
  "last_updated": "2025-08-20T20:00:00Z"
}
```

#### Government Level Statistics
```http
GET /api/v1/multi-level-government/stats/government-levels/{level_id}
```

**Response:**
```json
{
  "level_id": "550e8400-e29b-41d4-a716-446655440000",
  "level_name": "Federal",
  "total_jurisdictions": 1,
  "total_representatives": 338,
  "total_bills": 10000,
  "total_votes": 50000,
  "total_offices": 50,
  "last_updated": "2025-08-20T20:00:00Z"
}
```

#### Jurisdiction Statistics
```http
GET /api/v1/multi-level-government/stats/jurisdictions/{jurisdiction_id}
```

**Response:**
```json
{
  "jurisdiction_id": "550e8400-e29b-41d4-a716-446655440003",
  "jurisdiction_name": "House of Commons",
  "total_representatives": 338,
  "total_bills": 10000,
  "total_votes": 50000,
  "total_offices": 50,
  "last_updated": "2025-08-20T20:00:00Z"
}
```

## 4. Legacy API Endpoints

### 4.1 OpenParliament Endpoints
- **Bills**: `/api/v1/bills/*`
- **Members**: `/api/v1/members/*`
- **Votes**: `/api/v1/votes/*`
- **Debates**: `/api/v1/debates/*`
- **Committees**: `/api/v1/committees/*`
- **Search**: `/api/v1/search/*`

### 4.2 Represent Canada Endpoints
- **Representatives**: `/api/v1/represent/*`

## 5. Data Management Operations

### 5.1 Data Ingestion
The ETL service handles data ingestion from multiple sources:

1. **OpenParliament API**: Real-time federal data updates
2. **Represent Canada**: Daily representative updates
3. **Civic Scrapers**: Weekly municipal data refresh
4. **Scrapers-CA**: Bi-weekly provincial/municipal updates

### 5.2 Data Validation
All ingested data is validated for:
- **Data Type Consistency**: Ensures proper data types
- **Referential Integrity**: Validates foreign key relationships
- **Required Fields**: Checks for mandatory data
- **Data Quality**: Validates business rules

### 5.3 Data Archival
- **Bills**: 7-year retention policy
- **Votes**: 3-year retention policy
- **Representatives**: Current term + 2 years
- **Metadata**: Permanent retention

## 6. API Usage Examples

### 6.1 Get All Federal Representatives
```bash
curl "https://api.openparliament.ca/v1/multi-level-government/representatives?government_level=550e8400-e29b-41d4-a716-446655440000"
```

### 6.2 Search for Bills by Title
```bash
curl "https://api.openparliament.ca/v1/multi-level-government/bills?q=criminal+code"
```

### 6.3 Get Provincial Jurisdictions
```bash
curl "https://api.openparliament.ca/v1/multi-level-government/jurisdictions?government_level=550e8400-e29b-41d4-a716-446655440001"
```

### 6.4 Get Votes for a Specific Bill
```bash
curl "https://api.openparliament.ca/v1/multi-level-government/votes?bill_id=550e8400-e29b-41d4-a716-446655440006"
```

### 6.5 Get System Statistics
```bash
curl "https://api.openparliament.ca/v1/multi-level-government/stats/system"
```

## 7. Error Handling

### 7.1 HTTP Status Codes
- **200**: Success
- **400**: Bad Request (invalid parameters)
- **404**: Not Found (resource doesn't exist)
- **422**: Validation Error (invalid data)
- **429**: Too Many Requests (rate limit exceeded)
- **500**: Internal Server Error

### 7.2 Error Response Format
```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": "Additional error details"
}
```

## 8. Performance Considerations

### 8.1 Caching
- **API Responses**: 5-minute cache for list endpoints
- **Individual Resources**: 15-minute cache for detail endpoints
- **Statistics**: 1-hour cache for system stats

### 8.2 Pagination
- **Default Page Size**: 20 items
- **Maximum Page Size**: 100 items
- **Total Count**: Always included in pagination info

### 8.3 Search Optimization
- **Full-Text Search**: PostgreSQL full-text search on relevant fields
- **Indexing**: B-tree indexes on frequently queried fields
- **Query Optimization**: Automatic query plan optimization

## 9. Monitoring and Health

### 9.1 Health Check
```http
GET /healthz
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-08-20T20:00:00Z",
  "version": "0.1.0",
  "environment": "production",
  "database": "connected"
}
```

### 9.2 API Version
```http
GET /version
```

**Response:**
```json
{
  "version": "0.1.0",
  "build_date": "2025-08-20T20:00:00Z",
  "git_commit": "abc123def456",
  "environment": "production"
}
```

## 10. Conclusion

The OpenParliament.ca V2 platform provides a comprehensive, unified API for accessing Canadian government data at all levels. The multi-level government API endpoints offer:

- **Unified Access**: Single API for federal, provincial, and municipal data
- **Comprehensive Coverage**: Representatives, bills, votes, offices, and data sources
- **Rich Filtering**: Multiple filter options for all endpoints
- **Full Pagination**: Proper pagination for large datasets
- **Data Provenance**: Complete tracking of data sources
- **Performance Optimized**: Caching, indexing, and query optimization

This API serves as the foundation for building applications that need access to comprehensive Canadian government data, following the FUNDAMENTAL RULE: NEVER REINVENT THE WHEEL by building upon existing legacy systems and extending them with new capabilities.
