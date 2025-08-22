# Data Lineage Map

## Scope
Covers ingestion → normalization → storage → indexing → API → UI → analytics.
Links to concrete tables, schemas, and API contracts.

## Entities (reference)
- Source Systems: Federal/Provincial/Municipal feeds, scrapers
- Storage: Postgres schemas, Elasticsearch indices
- Movement: ETL/ELT jobs, schedulers
- Exposure: API_DESIGN_SPECIFICATION.md (endpoint → table/index mapping)
- Consumption: UI components, dashboards

## Required Tables/Indices

### OpenParliament Schema
- **bills**: id, title, description, status, introduction_date, jurisdiction_id
  - Indexes: PRIMARY KEY (id), INDEX (status), INDEX (introduction_date)
- **votes**: id, bill_id, member_id, vote_position, vote_date
  - Indexes: PRIMARY KEY (id), FOREIGN KEY (bill_id), FOREIGN KEY (member_id)
- **elected_members**: id, name, party, riding, email, phone, jurisdiction_id
  - Indexes: PRIMARY KEY (id), INDEX (party), INDEX (riding)
- **debates**: id, bill_id, member_id, speech_text, debate_date
  - Indexes: PRIMARY KEY (id), FOREIGN KEY (bill_id), FOREIGN KEY (member_id)

### Represent Canada Schema
- **representatives**: id, name, party, riding, email, phone, website, social_media
- **offices**: id, office_name, office_type, location, phone, email
- **contact_details**: id, representative_id, contact_type, contact_value, is_primary

### Multi-Level Government Schema
- **jurisdictions**: id, name, level (federal/provincial/municipal), parent_id
  - Indexes: PRIMARY KEY (id), INDEX (level)
- **government_levels**: id, name, description, level_order
- **data_sources**: id, name, jurisdiction_id, source_type, url, last_updated
- **ingestion_logs**: id, data_source_id, started_at, completed_at, records_processed

## Route Map (per feature)

### Feature F001: Global Search
- **Ingestion**: All scrapers feed into normalized tables
- **Transform**: Text extraction, tokenization, indexing
- **Tables**: bills, members, debates, votes, jurisdictions
- **Indexes**: Full-text search on title, description, speech_text
- **Endpoints**: GET /api/v1/search, GET /api/v1/search/postcode/{postcode}
- **UI Views**: GlobalSearch, SearchAutocomplete components
- **Error Handling**: Fallback to database search if Elasticsearch unavailable

### Feature F002: MP Profile System
- **Ingestion**: OpenParliament + Represent Canada scrapers
- **Transform**: Member data normalization, photo processing
- **Tables**: elected_members, representatives, offices, contact_details
- **Endpoints**: GET /api/v1/members, GET /api/v1/members/{member_id}
- **UI Views**: MPListView, MPDetailView, MPProfileCard
- **Error Handling**: Graceful degradation for missing contact info

### Feature F003: Bills Tracking
- **Ingestion**: OpenParliament bills scraper, LEGISinfo integration
- **Transform**: Status normalization, text parsing
- **Tables**: bills, votes, bill_history
- **Endpoints**: GET /api/v1/bills, GET /api/v1/bills/{bill_id}
- **UI Views**: BillListView, BillDetailView, BillStatusTracker
- **Error Handling**: Retry logic for external API failures

### Feature F004: Voting Records
- **Ingestion**: Vote scraper with ballot details
- **Transform**: Vote aggregation, party line analysis
- **Tables**: votes, ballots, user_votes
- **Endpoints**: GET /api/v1/votes, POST /api/v1/bills/{bill_id}/cast-vote
- **UI Views**: VoteListView, VoteDetailView, VotingPositions
- **Error Handling**: Transaction rollback for failed vote casting

### Feature F005: Debates Archive
- **Ingestion**: Hansard scraper with speech segmentation
- **Transform**: AI summarization, topic extraction
- **Tables**: debates, speeches, debate_summaries
- **Endpoints**: GET /api/v1/debates, GET /api/v1/debates/{year}/{month}/{day}
- **UI Views**: DebateListView, DebateDetailView, AISummaryDisplay
- **Error Handling**: Fallback to raw transcript if AI fails

### Feature F006: Committee Tracking
- **Ingestion**: Committee scraper with meeting details
- **Transform**: Membership tracking, report extraction
- **Tables**: committees, committee_members, meetings
- **Endpoints**: GET /api/v1/committees, GET /api/v1/committees/{committee_slug}
- **UI Views**: CommitteeListView, CommitteeDetailView, MeetingSchedule
- **Error Handling**: Handle missing meeting data gracefully

### Feature F007: Multi-Level Government
- **Ingestion**: 100+ municipal/provincial scrapers
- **Transform**: Jurisdiction normalization, deduplication
- **Tables**: jurisdictions, representatives, offices, government_levels
- **Endpoints**: GET /api/v1/jurisdictions, GET /api/v1/representatives
- **UI Views**: JurisdictionSelector, RepresentativeList, GovernmentLevelFilter
- **Error Handling**: Scraper failure isolation, partial data updates

### Feature F008: User Management
- **Ingestion**: User registration, OAuth providers
- **Transform**: Profile normalization, preference aggregation
- **Tables**: users, user_profiles, user_preferences
- **Endpoints**: POST /api/v1/users, GET /api/v1/users/{user_id}
- **UI Views**: LoginForm, UserProfile, PreferencesPanel
- **Error Handling**: Secure password reset, session management

### Feature F009: Mobile API Support
- **Ingestion**: Same as web with mobile optimizations
- **Transform**: Response size optimization, caching
- **Tables**: All core entities with mobile-specific views
- **Endpoints**: GET /api/v1/app/*, POST /api/v1/app-auth/*
- **UI Views**: Mobile-optimized components
- **Error Handling**: Offline queue for failed requests

### Feature F010: Data Export
- **Ingestion**: Read from all public tables
- **Transform**: Format conversion (JSON, CSV, XML)
- **Tables**: All public entities
- **Endpoints**: GET /api/v1/export/*, GET /api/v1/bulk/{dataset}
- **UI Views**: ExportPanel, DatasetSelector
- **Error Handling**: Chunked downloads, resume support

### Feature F011: Real-time House Status
- **Ingestion**: Parliamentary schedule API
- **Transform**: Status calculation, event detection
- **Tables**: house_status, session_calendar
- **Endpoints**: GET /api/v1/house/status (WebSocket)
- **UI Views**: HouseStatusBanner, SessionIndicator
- **Error Handling**: Graceful WebSocket reconnection

### Feature F012: Scraper Monitoring
- **Ingestion**: Scraper logs, health checks
- **Transform**: Success rate calculation, anomaly detection
- **Tables**: data_sources, ingestion_logs
- **Endpoints**: GET /api/v1/data-sources, GET /api/v1/stats/system
- **UI Views**: ScraperDashboard, IngestionStatus
- **Error Handling**: Alert escalation for critical failures

## Validation
- All routes cross-checked with FEATURE_MAPPING_UNIFIED.md
- Each route has corresponding test checkpoint in UPDATED_MASTER_EXECUTION_CHECKLIST.md
- Data flow validated through 10-pass merge process
