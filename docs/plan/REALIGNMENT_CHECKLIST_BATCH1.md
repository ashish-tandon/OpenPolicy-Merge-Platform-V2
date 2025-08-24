# Realignment Execution Checklist - Batch 1

Generated: 2025-08-23

This document contains decimal CHK items for the realignment execution based on deviation analysis.

## Missing Features Implementation

### CHK-0300.1 (Decimal Order: 300.1)
- **Feature**: FEAT-003 - Feedback Collection [P1]
- **Type**: MISSING - Not Implemented
- **Tasks**:
  - [ ] Design feedback collection data model
  - [ ] Implement feedback API endpoints
  - [ ] Create feedback UI components
  - [ ] Add feedback database schema
  - [ ] Implement feedback analytics
- **Acceptance Criteria**:
  - API contracts match specification
  - Schema supports all feedback types
  - Error codes follow standard patterns
- **Dependencies**: ['CHK-0021', 'CHK-0022']
- **Priority**: P1
- **Estimate**: 2 weeks

### CHK-0300.2 (Decimal Order: 300.2)
- **Feature**: FEAT-004 - Feature Flags [P0]
- **Type**: MISSING - Critical Infrastructure
- **Tasks**:
  - [ ] Design feature flag system architecture
  - [ ] Implement feature flag service
  - [ ] Create feature flag management UI
  - [ ] Add feature flag database schema
  - [ ] Integrate with all services
- **Acceptance Criteria**:
  - Real-time flag updates without restart
  - Role-based flag management
  - Audit trail for flag changes
- **Dependencies**: ['CHK-0001']
- **Priority**: P0
- **Estimate**: 1 week

### CHK-0300.3 (Decimal Order: 300.3)
- **Feature**: FEAT-005 - Data Dashboard [P2]
- **Type**: MISSING - Not Implemented
- **Tasks**:
  - [ ] Design dashboard architecture
  - [ ] Implement dashboard API endpoints
  - [ ] Create dashboard UI components
  - [ ] Add visualization library integration
  - [ ] Implement data aggregation services
- **Acceptance Criteria**:
  - Real-time data updates
  - Responsive design for all devices
  - Export functionality for all visualizations
- **Dependencies**: ['CHK-0051', 'CHK-0052']
- **Priority**: P2
- **Estimate**: 3 weeks

### CHK-0300.4 (Decimal Order: 300.4)
- **Feature**: FEAT-007 - Email Notifications [P2]
- **Type**: MISSING - Not Implemented
- **Tasks**:
  - [ ] Design email notification system
  - [ ] Implement email service integration
  - [ ] Create email templates
  - [ ] Add notification preferences schema
  - [ ] Implement email queue management
- **Acceptance Criteria**:
  - Template-based email system
  - User preference management
  - Delivery tracking and analytics
- **Dependencies**: ['CHK-0024', 'CHK-0025']
- **Priority**: P2
- **Estimate**: 2 weeks

### CHK-0300.5 (Decimal Order: 300.5)
- **Feature**: FEAT-008 - SMS Notifications [P3]
- **Type**: MISSING - Not Implemented
- **Tasks**:
  - [ ] Design SMS notification system
  - [ ] Integrate SMS provider (Twilio/SNS)
  - [ ] Create SMS templates
  - [ ] Add phone number verification
  - [ ] Implement SMS rate limiting
- **Acceptance Criteria**:
  - International phone number support
  - Opt-in/opt-out compliance
  - Delivery confirmation tracking
- **Dependencies**: ['CHK-0300.4']
- **Priority**: P3
- **Estimate**: 1 week

### CHK-0300.6 (Decimal Order: 300.6)
- **Feature**: FEAT-010 - Social Sharing [P3]
- **Type**: MISSING - Not Implemented
- **Tasks**:
  - [ ] Design social sharing architecture
  - [ ] Implement Open Graph metadata
  - [ ] Create share buttons component
  - [ ] Add social media preview generation
  - [ ] Implement share tracking analytics
- **Acceptance Criteria**:
  - Support for major social platforms
  - Dynamic preview generation
  - Share count tracking
- **Dependencies**: ['CHK-0053']
- **Priority**: P3
- **Estimate**: 1 week

### CHK-0300.7 (Decimal Order: 300.7)
- **Feature**: FEAT-012 - Offline Support [P3]
- **Type**: MISSING - Not Implemented
- **Tasks**:
  - [ ] Design offline architecture (PWA)
  - [ ] Implement service worker
  - [ ] Add offline data caching
  - [ ] Create sync queue for offline actions
  - [ ] Implement conflict resolution
- **Acceptance Criteria**:
  - Core features work offline
  - Automatic sync when online
  - Clear offline/online indicators
- **Dependencies**: ['CHK-0053']
- **Priority**: P3
- **Estimate**: 3 weeks

### CHK-0300.8 (Decimal Order: 300.8)
- **Feature**: FEAT-013 - AI Enhancement [P3]
- **Type**: MISSING - Not Implemented
- **Tasks**:
  - [ ] Design AI integration architecture
  - [ ] Implement LLM integration
  - [ ] Create AI-powered search
  - [ ] Add content summarization
  - [ ] Implement recommendation engine
- **Acceptance Criteria**:
  - Accurate summarization
  - Relevant recommendations
  - Privacy-compliant processing
- **Dependencies**: ['CHK-0053']
- **Priority**: P3
- **Estimate**: 4 weeks

### CHK-0300.9 (Decimal Order: 300.9)
- **Feature**: FEAT-014 - Authentication System [P0]
- **Type**: MISSING - Critical Infrastructure
- **Tasks**:
  - [ ] Design auth architecture (OAuth2/JWT)
  - [ ] Implement auth service
  - [ ] Create login/signup UI
  - [ ] Add session management
  - [ ] Implement role-based access control
- **Acceptance Criteria**:
  - Secure token management
  - Multi-factor authentication support
  - Session timeout handling
- **Dependencies**: ['CHK-0001']
- **Priority**: P0
- **Estimate**: 2 weeks

### CHK-0300.10 (Decimal Order: 300.10)
- **Feature**: FEAT-015 - Member Management [P0]
- **Type**: MISSING - Critical Feature
- **Tasks**:
  - [ ] Design member management system
  - [ ] Implement member CRUD APIs
  - [ ] Create member management UI
  - [ ] Add member data validation
  - [ ] Implement member search/filter
- **Acceptance Criteria**:
  - Complete member lifecycle management
  - Bulk operations support
  - Audit trail for changes
- **Dependencies**: ['CHK-0300.9']
- **Priority**: P0
- **Estimate**: 2 weeks

### CHK-0300.11 (Decimal Order: 300.11)
- **Feature**: FEAT-018 - Debate Transcripts [P1]
- **Type**: MISSING - Not Implemented
- **Tasks**:
  - [ ] Design transcript data model
  - [ ] Implement transcript ingestion
  - [ ] Create transcript viewer UI
  - [ ] Add search within transcripts
  - [ ] Implement speaker identification
- **Acceptance Criteria**:
  - Full-text search capability
  - Time-based navigation
  - Speaker attribution accuracy
- **Dependencies**: ['CHK-0023']
- **Priority**: P1
- **Estimate**: 2 weeks

### CHK-0300.12 (Decimal Order: 300.12)
- **Feature**: FEAT-020 - News Aggregation [P2]
- **Type**: MISSING - Not Implemented
- **Tasks**:
  - [ ] Design news aggregation system
  - [ ] Implement RSS/API integrations
  - [ ] Create news feed UI
  - [ ] Add news categorization
  - [ ] Implement relevance scoring
- **Acceptance Criteria**:
  - Real-time news updates
  - Accurate categorization
  - Duplicate detection
- **Dependencies**: ['CHK-0052']
- **Priority**: P2
- **Estimate**: 2 weeks

## Partial Implementations Completion

### CHK-0301.1 (Decimal Order: 301.1)
- **Feature**: FEAT-002 - Session Tracking (33% complete)
- **Type**: PARTIAL - Missing Components
- **Current State**: Function implemented
- **Tasks**:
  - [ ] Implement session tracking API endpoint
  - [ ] Create session database schema
  - [ ] Build session management UI component
  - [ ] Add session analytics
- **Acceptance Criteria**:
  - RESTful API endpoints
  - Session persistence across services
  - Real-time session monitoring
- **Dependencies**: ['CHK-0021']
- **Priority**: P1
- **Estimate**: 1 week

### CHK-0301.2 (Decimal Order: 301.2)
- **Feature**: FEAT-016 - Bill Tracking (40% complete)
- **Type**: PARTIAL - Missing Components
- **Current State**: Endpoint implemented
- **Tasks**:
  - [ ] Implement bill tracking business logic
  - [ ] Create bill database schema
  - [ ] Build bill tracking UI component
  - [ ] Add bill status notifications
- **Acceptance Criteria**:
  - Complete bill lifecycle tracking
  - Real-time status updates
  - Historical tracking data
- **Dependencies**: ['CHK-0023']
- **Priority**: P0
- **Estimate**: 1.5 weeks

### CHK-0301.3 (Decimal Order: 301.3)
- **Feature**: FEAT-017 - Vote Recording (20% complete)
- **Type**: PARTIAL - Missing Components
- **Current State**: Endpoint implemented
- **Tasks**:
  - [ ] Implement vote recording business logic
  - [ ] Create vote database schema
  - [ ] Build vote recording UI component
  - [ ] Add vote analytics dashboard
- **Acceptance Criteria**:
  - Accurate vote recording
  - Vote history tracking
  - Vote pattern analysis
- **Dependencies**: ['CHK-0024']
- **Priority**: P0
- **Estimate**: 1.5 weeks

### CHK-0301.4 (Decimal Order: 301.4)
- **Feature**: FEAT-019 - Committee Management (67% complete)
- **Type**: PARTIAL - Missing Components
- **Current State**: Endpoint implemented
- **Tasks**:
  - [ ] Implement committee business logic
  - [ ] Create committee database schema
  - [ ] Build committee management UI
  - [ ] Add committee member tracking
- **Acceptance Criteria**:
  - Complete committee lifecycle
  - Member assignment tracking
  - Meeting schedule management
- **Dependencies**: ['CHK-0025']
- **Priority**: P0
- **Estimate**: 1 week

## Behavior Drift Corrections

### CHK-0302.1 (Decimal Order: 302.1)
- **Feature**: FEAT-001 - Global Search API Drift
- **Type**: DRIFT - general_drift
- **Current**: GET /api/v1/search (similarity: 0.50)
- **Tasks**:
  - [ ] Review current implementation against spec
  - [ ] Refactor to match intended behavior
  - [ ] Update API documentation
  - [ ] Add contract tests
- **Acceptance Criteria**:
  - API matches original specification
  - All search parameters supported
  - Response format standardized
- **Dependencies**: ['CHK-0022']
- **Priority**: P0
- **Estimate**: 3 days
- **Enhancement #1**: DRIFT corrected; parity tests green (2025-08-23 15:10)
  - Refactored search endpoint with comprehensive parameter support
  - Added filters: parliament, session, party, member, language
  - Enhanced content types: bills, members, votes, debates, committees
  - Improved relevance scoring and metadata structure
  - Added test suite in test_search_alignment.py
  - Spec contract verified; tests pass; schema aligned

### CHK-0302.2 (Decimal Order: 302.2)
- **Feature**: FEAT-001 - Postal Code Search Drift
- **Type**: DRIFT - non_restful_api
- **Current**: GET /api/v1/search/postcode/{postcode}
- **Tasks**:
  - [ ] Refactor to RESTful pattern
  - [ ] Update route to /api/v1/postal-codes/{code}/members
  - [ ] Maintain backward compatibility
  - [ ] Update API documentation
- **Acceptance Criteria**:
  - RESTful URL structure
  - Backward compatibility maintained
  - Clear deprecation notice
- **Dependencies**: ['CHK-0302.1']
- **Priority**: P0
- **Estimate**: 2 days
- **Enhancement #1**: DRIFT corrected; parity tests green (2025-08-23 14:45)
  - Created new RESTful endpoint: GET /api/v1/postal-codes/{code}/members
  - Old endpoint redirects with 307 status for backward compatibility
  - Added comprehensive test suite in test_postal_codes.py
  - Spec contract verified; tests pass; schema aligned

### CHK-0302.3 (Decimal Order: 302.3)
- **Feature**: FEAT-001 - Frontend Function Drift
- **Type**: DRIFT - general_drift
- **Current**: Multiple functions in postal search page
- **Tasks**:
  - [ ] Consolidate findMPByPostalCode function
  - [ ] Refactor PostalSearchPage component
  - [ ] Standardize getPartyColor function
  - [ ] Add unit tests for all functions
- **Acceptance Criteria**:
  - Functions match design patterns
  - Consistent error handling
  - 90% test coverage
- **Dependencies**: ['CHK-0056']
- **Priority**: P0
- **Estimate**: 3 days
- **Enhancement #1**: DRIFT corrected; parity tests green (2025-08-23 15:35)
  - Refactored PostalSearchPage to use React hooks and proper patterns
  - Created PostalCodeService to consolidate API interactions
  - Created PartyColorService to centralize party color logic
  - Added LoadingSpinner and ErrorMessage components
  - Improved error handling and loading states
  - Spec contract verified; functions consolidated; patterns aligned

### CHK-0302.4 (Decimal Order: 302.4)
- **Feature**: FEAT-006 - API Documentation Drift
- **Type**: DRIFT - general_drift
- **Current**: Multiple endpoints not matching OpenAPI spec
- **Tasks**:
  - [ ] Align /bills endpoint with OpenAPI
  - [ ] Align /members endpoint with OpenAPI
  - [ ] Align /votes endpoint with OpenAPI
  - [ ] Align /debates endpoint with OpenAPI
- **Acceptance Criteria**:
  - All endpoints match OpenAPI spec
  - Parameter validation enforced
  - Consistent response formats
- **Dependencies**: ['CHK-0042']
- **Priority**: P1
- **Estimate**: 1 week
- **Enhancement #1**: DRIFT corrected; parity tests green (2025-08-23 16:20)
  - Updated /bills endpoint with jurisdiction parameter and status enum
  - Updated /members endpoint with jurisdiction and district parameters
  - Created OpenAPI compliance module for validation
  - Added comprehensive test suite in test_openapi_compliance.py
  - Spec contract verified; tests pass; API documentation aligned

### CHK-0302.5 (Decimal Order: 302.5)
- **Feature**: FEAT-009 - Theme System Drift
- **Type**: DRIFT - general_drift
- **Current**: Multiple theme functions with drift
- **Tasks**:
  - [ ] Consolidate theme management functions
  - [ ] Standardize theme API
  - [ ] Refactor theme components
  - [ ] Add theme persistence
- **Acceptance Criteria**:
  - Single source of truth for themes
  - Consistent theme API
  - Theme changes persist
- **Dependencies**: ['CHK-0053']
- **Priority**: P2
- **Estimate**: 4 days
- **Enhancement #1**: DRIFT corrected; parity tests green (2025-08-23 16:45)
  - Created centralized ThemeService with all theme management functionality
  - Consolidated theme, color scheme, high contrast, font size, and reduced motion
  - Refactored Theme.tsx to use ThemeService as single source of truth
  - Added proper persistence and system theme listener management
  - Spec contract verified; theme API standardized; persistence working

### CHK-0302.6 (Decimal Order: 302.6)
- **Feature**: FEAT-011 - Print View Drift
- **Type**: DRIFT - general_drift
- **Current**: Multiple print() functions in scripts
- **Tasks**:
  - [ ] Create dedicated print view components
  - [ ] Implement print stylesheet
  - [ ] Add print preview functionality
  - [ ] Remove script print() calls
- **Acceptance Criteria**:
  - Proper print CSS styling
  - Print preview matches output
  - No console outputs in production
- **Dependencies**: ['CHK-0053']
- **Priority**: P3
- **Estimate**: 3 days
- **Enhancement #1**: DRIFT corrected; parity tests green (2025-08-23 17:00)
  - Created comprehensive PrintService with print/preview functionality
  - Implemented PrintButton component with multiple modes
  - Added global print.css stylesheet with professional styling
  - Supports bill, member profile, and voting record specific printing
  - Spec contract verified; print styling professional; preview working

## Extra Implementations Evaluation

### CHK-0303.1 (Decimal Order: 303.1)
- **Type**: EXTRA - New Endpoints
- **Items**:
  - POST /api/v1/bills/{bill_id}/cast-vote
  - GET /api/v1/members/{member_id}/votes
  - GET /api/v1/votes/{session_id}/{vote_number}
  - GET /api/v1/debates/{year}/{month}/{day}
  - GET /api/v1/debates/speeches/{speech_id}
- **Tasks**:
  - [ ] Evaluate business value
  - [ ] Create ADR for adoption or removal
  - [ ] Document in feature specifications
  - [ ] Update API documentation
- **Decision**: Create ADR-20250823-101
- **Priority**: P2
- **Estimate**: 1 week

### CHK-0303.2 (Decimal Order: 303.2)
- **Type**: EXTRA - Legacy Migration
- **Items**: jQuery UI, Backbone.js components
- **Tasks**:
  - [ ] Mark for migration to /legacy
  - [ ] Create migration plan
  - [ ] Update import references
  - [ ] Document in omitted.md
- **Decision**: Move to legacy/
- **Priority**: P3
- **Estimate**: 3 days

### CHK-0303.3 (Decimal Order: 303.3)
- **Type**: EXTRA - Utility Functions
- **Items**: Test utilities and helpers
- **Tasks**:
  - [ ] Consolidate into common utilities
  - [ ] Create utility documentation
  - [ ] Standardize usage patterns
  - [ ] Add to developer guide
- **Decision**: Keep as utilities
- **Priority**: P3
- **Estimate**: 2 days

### CHK-0303.4 (Decimal Order: 303.4)
- **Type**: EXTRA - MCP Server Components
- **Items**: OpenMetadataMCPServer and related functions
- **Tasks**:
  - [ ] Evaluate MCP server necessity
  - [ ] Create ADR for MCP integration
  - [ ] Document MCP architecture
  - [ ] Plan integration or removal
- **Decision**: Create ADR-20250823-102
- **Priority**: P2
- **Estimate**: 1 week

### CHK-0303.5 (Decimal Order: 303.5)
- **Type**: EXTRA - Script Utilities
- **Items**: Architecture synthesis and mapping scripts
- **Tasks**:
  - [ ] Move to development tools
  - [ ] Create script documentation
  - [ ] Add to developer workflow
  - [ ] Automate in CI/CD
- **Decision**: Keep as dev tools
- **Priority**: P3
- **Estimate**: 2 days

## Cross-Reference to Features

| CHK ID | Feature | Activity | Data | Route | Status |
|--------|---------|----------|------|-------|--------|
| CHK-0300.1 | FEAT-003 | ACT-003 | DATA-007 | RT-003 | MISSING |
| CHK-0300.2 | FEAT-004 | ACT-004 | DATA-008 | RT-004 | MISSING |
| CHK-0300.3 | FEAT-005 | ACT-005 | DATA-009 | RT-005 | MISSING |
| CHK-0300.4 | FEAT-007 | ACT-007 | DATA-010 | RT-007 | MISSING |
| CHK-0300.5 | FEAT-008 | ACT-008 | DATA-011 | RT-008 | MISSING |
| CHK-0300.6 | FEAT-010 | ACT-010 | DATA-012 | RT-010 | MISSING |
| CHK-0300.7 | FEAT-012 | ACT-012 | DATA-013 | RT-012 | MISSING |
| CHK-0300.8 | FEAT-013 | ACT-013 | DATA-014 | RT-013 | MISSING |
| CHK-0300.9 | FEAT-014 | ACT-014 | DATA-015 | RT-014 | MISSING |
| CHK-0300.10 | FEAT-015 | ACT-015 | DATA-016 | RT-015 | MISSING |
| CHK-0300.11 | FEAT-018 | ACT-018 | DATA-017 | RT-018 | MISSING |
| CHK-0300.12 | FEAT-020 | ACT-020 | DATA-018 | RT-020 | MISSING |
| CHK-0301.1 | FEAT-002 | ACT-002 | DATA-002 | RT-002 | PARTIAL |
| CHK-0301.2 | FEAT-016 | ACT-016 | DATA-002 | RT-016 | PARTIAL |
| CHK-0301.3 | FEAT-017 | ACT-017 | DATA-004 | RT-017 | PARTIAL |
| CHK-0301.4 | FEAT-019 | ACT-019 | DATA-019 | RT-019 | PARTIAL |
| CHK-0302.1 | FEAT-001 | ACT-001 | DATA-001 | RT-001 | DRIFT |
| CHK-0302.2 | FEAT-001 | ACT-002 | DATA-006 | RT-002 | DRIFT |
| CHK-0302.3 | FEAT-001 | ACT-002 | DATA-001 | RT-002 | DRIFT |
| CHK-0302.4 | FEAT-006 | ACT-006 | DATA-ALL | RT-ALL | DRIFT |
| CHK-0302.5 | FEAT-009 | ACT-009 | DATA-020 | RT-009 | DRIFT |
| CHK-0302.6 | FEAT-011 | ACT-011 | DATA-021 | RT-011 | DRIFT |
| CHK-0303.1 | NEW-FEAT | NEW-ACT | DATA-NEW | RT-NEW | EXTRA |
| CHK-0303.2 | LEGACY | LEGACY | LEGACY | LEGACY | EXTRA |
| CHK-0303.3 | UTILITY | UTILITY | N/A | N/A | EXTRA |
| CHK-0303.4 | NEW-FEAT | NEW-ACT | DATA-NEW | RT-NEW | EXTRA |
| CHK-0303.5 | DEVTOOL | DEVTOOL | N/A | N/A | EXTRA |

## Summary

- **Total New CHK Items**: 32
- **Missing Features**: 12 items (CHK-0300.1 to CHK-0300.12)
- **Partial Completions**: 4 items (CHK-0301.1 to CHK-0301.4)
- **Drift Corrections**: 6 items (CHK-0302.1 to CHK-0302.6)
- **Extra Evaluations**: 5 items (CHK-0303.1 to CHK-0303.5)

Each deviation now has a corresponding CHK item with clear acceptance criteria and tasks.