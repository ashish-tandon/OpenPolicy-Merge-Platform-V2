# Unified Feature Mapping

## Master Inventory
- Based on 84/120+ features implemented (70% complete)

## Feature: Global Search
- ID: F001
- Name: Global Search with Postal Code MP Lookup  
- Priority (P0–P4): P0
- Data Entities (tables/indices): members, bills, debates, votes, jurisdictions
- API Endpoints (with methods): GET /api/v1/search, GET /api/v1/search/postcode/{postcode}
- UI Views/Components: GlobalSearch, SearchAutocomplete
- Tests Required (unit/int/e2e/contract): unit, integration, e2e
- Dependencies & Flags: Elasticsearch for full-text search
- Execution Checklist IDs: 3.6, 5.1

## Feature: MP Profile System
- ID: F002
- Name: Complete MP Database with Individual Profiles
- Priority (P0–P4): P0
- Data Entities (tables/indices): elected_members, representatives, offices, contact_details
- API Endpoints (with methods): GET /api/v1/members, GET /api/v1/members/{member_id}
- UI Views/Components: MPListView, MPDetailView, MPProfileCard
- Tests Required (unit/int/e2e/contract): unit, integration, e2e
- Dependencies & Flags: Photo storage, social media APIs
- Execution Checklist IDs: 3.2, 5.2

## Feature: Bills Tracking
- ID: F003
- Name: Complete Bills Database with Status Tracking
- Priority (P0–P4): P0
- Data Entities (tables/indices): bills, votes, bill_history
- API Endpoints (with methods): GET /api/v1/bills, GET /api/v1/bills/{bill_id}
- UI Views/Components: BillListView, BillDetailView, BillStatusTracker
- Tests Required (unit/int/e2e/contract): unit, integration, e2e
- Dependencies & Flags: LEGISinfo integration
- Execution Checklist IDs: 3.1, 5.3

## Feature: Voting Records
- ID: F004
- Name: Complete Voting Records with MP Positions
- Priority (P0–P4): P0
- Data Entities (tables/indices): votes, ballots, user_votes
- API Endpoints (with methods): GET /api/v1/votes, POST /api/v1/bills/{bill_id}/cast-vote
- UI Views/Components: VoteListView, VoteDetailView, VotingPositions
- Tests Required (unit/int/e2e/contract): unit, integration, e2e
- Dependencies & Flags: Real-time vote updates
- Execution Checklist IDs: 3.3, 5.4

## Feature: Debates Archive
- ID: F005
- Name: Complete Hansard Archive with AI Summaries
- Priority (P0–P4): P1
- Data Entities (tables/indices): debates, speeches, debate_summaries
- API Endpoints (with methods): GET /api/v1/debates, GET /api/v1/debates/{year}/{month}/{day}
- UI Views/Components: DebateListView, DebateDetailView, AISummaryDisplay
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: AI summarization service
- Execution Checklist IDs: 3.4, 5.5

## Feature: Committee Tracking
- ID: F006
- Name: Complete Committee Database with Meetings
- Priority (P0–P4): P1
- Data Entities (tables/indices): committees, committee_members, meetings
- API Endpoints (with methods): GET /api/v1/committees, GET /api/v1/committees/{committee_slug}
- UI Views/Components: CommitteeListView, CommitteeDetailView, MeetingSchedule
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Meeting calendar integration
- Execution Checklist IDs: 3.5, 5.6

## Feature: Multi-Level Government
- ID: F007
- Name: Federal/Provincial/Municipal Representative Database
- Priority (P0–P4): P0
- Data Entities (tables/indices): jurisdictions, representatives, offices, government_levels
- API Endpoints (with methods): GET /api/v1/jurisdictions, GET /api/v1/representatives
- UI Views/Components: JurisdictionSelector, RepresentativeList, GovernmentLevelFilter
- Tests Required (unit/int/e2e/contract): unit, integration, e2e
- Dependencies & Flags: Scraper scheduling system
- Execution Checklist IDs: 3.7, 4.1, 4.2, 4.3

## Feature: User Management
- ID: F008
- Name: User Authentication and Profile Management
- Priority (P0–P4): P0
- Data Entities (tables/indices): users, user_profiles, user_preferences
- API Endpoints (with methods): POST /api/v1/users, GET /api/v1/users/{user_id}
- UI Views/Components: LoginForm, UserProfile, PreferencesPanel
- Tests Required (unit/int/e2e/contract): unit, integration, e2e, security
- Dependencies & Flags: OAuth integration, JWT tokens
- Execution Checklist IDs: 3.8, 5.7, 10.1

## Feature: Mobile API Support
- ID: F009
- Name: Mobile-Optimized API Endpoints
- Priority (P0–P4): P1
- Data Entities (tables/indices): All core entities with mobile optimization
- API Endpoints (with methods): GET /api/v1/app/*, POST /api/v1/app-auth/*
- UI Views/Components: Mobile-specific components
- Tests Required (unit/int/e2e/contract): unit, integration, contract
- Dependencies & Flags: Push notification service
- Execution Checklist IDs: 6.1, 6.2

## Feature: Data Export
- ID: F010
- Name: Bulk Data Export Functionality
- Priority (P0–P4): P2
- Data Entities (tables/indices): All public entities
- API Endpoints (with methods): GET /api/v1/export/*, GET /api/v1/bulk/{dataset}
- UI Views/Components: ExportPanel, DatasetSelector
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Background job processing
- Execution Checklist IDs: 3.6

## Feature: Real-time House Status
- ID: F011
- Name: Dynamic House of Commons Status Banner
- Priority (P0–P4): P1
- Data Entities (tables/indices): house_status, session_calendar
- API Endpoints (with methods): GET /api/v1/house/status
- UI Views/Components: HouseStatusBanner, SessionIndicator
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: WebSocket for real-time updates
- Execution Checklist IDs: 5.1

## Feature: Scraper Monitoring
- ID: F012
- Name: ETL Pipeline Health Dashboard
- Priority (P0–P4): P2
- Data Entities (tables/indices): data_sources, ingestion_logs
- API Endpoints (with methods): GET /api/v1/data-sources, GET /api/v1/stats/system
- UI Views/Components: ScraperDashboard, IngestionStatus
- Tests Required (unit/int/e2e/contract): unit, integration
- Dependencies & Flags: Monitoring alerts
- Execution Checklist IDs: 4.4, 4.5

<!-- MERGE_NOTE: Additional features to be added from validation docs and legacy notes -->