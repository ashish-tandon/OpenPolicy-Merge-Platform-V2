# Bugs Reconciliation

## Sources
- All legacy bug files and notes
- Validation gaps (CHECKLIST_VERIFICATION_REVIEWS.md)
- TEST_REPORT_pass1.md
- 10-pass merge validation findings

## Schema
- BUG-ID, Title, Source, Priority (P0–P4), Owner, Status, Repro Steps, Links (feature IDs, checklist IDs)

## Process
- Deduplicate exact/near duplicates
- Tie every bug to feature + data route and checklist task

## Active Bugs

### Authentication & Security

#### BUG-001: Missing Authentication Implementation
- **Title**: User authentication system not implemented
- **Source**: UI Validation Report
- **Priority**: P0
- **Owner**: Backend Team
- **Status**: Open
- **Repro Steps**: Try to login - no login flow exists
- **Links**: Feature F008, Checklist 5.7, 10.1

#### BUG-002: OAuth Integration Incomplete
- **Title**: Google OAuth integration UI exists but backend not connected
- **Source**: API Validation Report
- **Priority**: P1
- **Owner**: Backend Team
- **Status**: In Progress
- **Repro Steps**: Click Google login button - returns 404
- **Links**: Feature F038, Checklist 10.1

#### BUG-003: Missing Rate Limiting
- **Title**: API endpoints lack rate limiting implementation
- **Source**: API Validation Report
- **Priority**: P1
- **Owner**: API Team
- **Status**: Open
- **Repro Steps**: Send 1000+ requests/second - no throttling
- **Links**: All API features, Checklist 10.5

### Data & Scrapers

#### BUG-004: Provincial Scrapers Partial Integration
- **Title**: Some provincial scrapers not fully integrated with ETL pipeline
- **Source**: Scraper Validation Report
- **Priority**: P1
- **Owner**: ETL Team
- **Status**: In Progress
- **Repro Steps**: Check ingestion logs - missing provinces
- **Links**: Feature F007, Checklist 4.2

#### BUG-005: Scraper Website Change Failures
- **Title**: Multiple scrapers failing due to website structure changes
- **Source**: Scraper Validation Report
- **Priority**: P1
- **Owner**: ETL Team
- **Status**: Open
- **Repro Steps**: Run scrapers - see failure logs
- **Links**: Feature F012, Checklist 4.3

#### BUG-006: Missing Historical Data
- **Title**: Historical data not available for many jurisdictions
- **Source**: Scraper Validation Report
- **Priority**: P2
- **Owner**: Data Team
- **Status**: Open
- **Repro Steps**: Query pre-2020 data - returns empty
- **Links**: Feature F014, Checklist 4.1

### UI/UX Issues

#### BUG-007: Missing Loading States
- **Title**: No loading skeletons for async content
- **Source**: UI Validation Report
- **Priority**: P2
- **Owner**: Frontend Team
- **Status**: Open
- **Repro Steps**: Navigate between pages - see blank states
- **Links**: All UI features, Checklist 5.1-5.6

#### BUG-008: Mobile Navigation Issues
- **Title**: Mobile menu doesn't close after navigation
- **Source**: Manual Testing
- **Priority**: P2
- **Owner**: Frontend Team
- **Status**: Open
- **Repro Steps**: On mobile, open menu, click link - menu stays open
- **Links**: Feature F041, Checklist 5.1

#### BUG-009: Search Autocomplete Performance
- **Title**: Search suggestions slow with large datasets
- **Source**: Performance Testing
- **Priority**: P2
- **Owner**: Frontend Team
- **Status**: Open
- **Repro Steps**: Type in search - 2-3 second delay
- **Links**: Feature F001, Checklist 3.6

### API Issues

#### BUG-010: Missing API Versioning Headers
- **Title**: API responses lack version headers
- **Source**: API Validation Report
- **Priority**: P2
- **Owner**: API Team
- **Status**: Open
- **Repro Steps**: Check response headers - no API-Version
- **Links**: All API features, Checklist 3.1-3.8

#### BUG-011: Inconsistent Error Responses
- **Title**: Error responses not following standard format
- **Source**: API Testing
- **Priority**: P2
- **Owner**: API Team
- **Status**: Open
- **Repro Steps**: Trigger various errors - different formats
- **Links**: All API features, Checklist 3.1-3.8

#### BUG-012: Missing Pagination on Some Endpoints
- **Title**: Large data endpoints missing pagination
- **Source**: API Validation Report
- **Priority**: P1
- **Owner**: API Team
- **Status**: Open
- **Repro Steps**: GET /api/v1/debates - returns all records
- **Links**: Feature F005, Checklist 3.4

### Testing & Documentation

#### BUG-013: Missing E2E Test Suite
- **Title**: End-to-end tests not implemented
- **Source**: Test Strategy Review
- **Priority**: P1
- **Owner**: QA Team
- **Status**: Open
- **Repro Steps**: Check test coverage - E2E at 0%
- **Links**: All features, Checklist 7.4

#### BUG-014: Incomplete API Documentation
- **Title**: Several endpoints missing from OpenAPI spec
- **Source**: API Validation Report
- **Priority**: P2
- **Owner**: API Team
- **Status**: In Progress
- **Repro Steps**: Compare actual endpoints to docs
- **Links**: All API features, Checklist 8.1

#### BUG-015: Missing User Documentation
- **Title**: No end-user documentation available
- **Source**: Documentation Review
- **Priority**: P2
- **Owner**: Documentation Team
- **Status**: Open
- **Repro Steps**: Look for user guides - none exist
- **Links**: All features, Checklist 8.4

### Infrastructure & Deployment

#### BUG-016: Kubernetes Configs Not Ready
- **Title**: Production Kubernetes deployment configs missing
- **Source**: DevOps Review
- **Priority**: P1
- **Owner**: DevOps Team
- **Status**: Open
- **Repro Steps**: Check k8s/ directory - incomplete
- **Links**: All features, Checklist 9.2

#### BUG-017: Missing Monitoring Setup
- **Title**: Production monitoring not configured
- **Source**: Infrastructure Review
- **Priority**: P1
- **Owner**: DevOps Team
- **Status**: Open
- **Repro Steps**: Check monitoring dashboards - not set up
- **Links**: Feature F012, Checklist 9.4

#### BUG-018: No Backup Strategy
- **Title**: Database backup procedures not implemented
- **Source**: Infrastructure Review
- **Priority**: P0
- **Owner**: DevOps Team
- **Status**: Open
- **Repro Steps**: Check backup jobs - none configured
- **Links**: All features, Checklist 9.5

### Accessibility

#### BUG-019: Missing Alt Text on Images
- **Title**: MP photos lack alt text attributes
- **Source**: Accessibility Audit
- **Priority**: P1
- **Owner**: Frontend Team
- **Status**: Open
- **Repro Steps**: Screen reader on MP profiles - no descriptions
- **Links**: Feature F046, Checklist 5.2

#### BUG-020: Keyboard Navigation Gaps
- **Title**: Some interactive elements not keyboard accessible
- **Source**: Accessibility Audit
- **Priority**: P1
- **Owner**: Frontend Team
- **Status**: Open
- **Repro Steps**: Tab through UI - skip some buttons
- **Links**: All UI features, Checklist 5.1-5.6

## Summary Statistics
- **Total Bugs**: 20
- **P0 (Critical)**: 2
- **P1 (High)**: 10
- **P2 (Medium)**: 8
- **P3 (Low)**: 0
- **P4 (Trivial)**: 0

## Bug Status
- **Open**: 16
- **In Progress**: 4
- **Resolved**: 0
- **Closed**: 0

## Team Distribution
- **API Team**: 4 bugs
- **Backend Team**: 2 bugs
- **Frontend Team**: 5 bugs
- **ETL Team**: 2 bugs
- **Data Team**: 1 bug
- **QA Team**: 1 bug
- **Documentation Team**: 1 bug
- **DevOps Team**: 4 bugs