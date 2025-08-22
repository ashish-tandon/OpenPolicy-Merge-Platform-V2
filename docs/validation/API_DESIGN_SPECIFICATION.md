# API Design Specification

## Overview
OpenPolicy V2 API Gateway provides unified access to Canadian parliamentary and civic data.

## API Endpoints

### Bills
GET /api/v1/bills - List all bills
GET /api/v1/bills/{bill_id} - Get bill details
POST /api/v1/bills/{bill_id}/cast-vote - Cast user vote

### Members
GET /api/v1/members - List all members
GET /api/v1/members/{member_id} - Get member details
GET /api/v1/members/{member_id}/votes - Member voting history

### Votes
GET /api/v1/votes - List all votes
GET /api/v1/votes/{session_id}/{vote_number} - Get vote details

### Debates
GET /api/v1/debates - List all debates
GET /api/v1/debates/{year}/{month}/{day} - Get debate by date
GET /api/v1/debates/speeches/{speech_id} - Get speech details

### Committees
GET /api/v1/committees - List all committees
GET /api/v1/committees/{committee_slug} - Get committee details

### Multi-Level Government
GET /api/v1/jurisdictions - List all jurisdictions
GET /api/v1/representatives - List all representatives
GET /api/v1/offices - List all offices

### Search
GET /api/v1/search - Unified search across all data
GET /api/v1/search/postcode/{postcode} - Search by postal code