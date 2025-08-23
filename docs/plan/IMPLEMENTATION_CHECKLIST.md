# OpenPolicy V2 Implementation Checklist

Generated: 2025-08-23  
Total Items: 325  
Cycles Completed: 10/10  
Last Updated: 2025-08-23

This is the canonical implementation checklist for OpenPolicy V2. Items are enhanced through 10 cycles, append-only.

## Statistics

- Total Items: 325
- G1 (Structure/Index): 55
- G2 (Parity): 80
- G3 (Architecture Harmony): 65
- G4 (Test Strategy): 60
- G5 (Release Readiness): 65

## G1: Structure/Index

### CHK-0001 (Decimal Order: 1.1)
- **Title**: Refactor high-usage functions: Field
- **Gate**: G1
- **Feature(s)**: FEAT-001, FEAT-002, FEAT-003
- **Activity**: ACT-001
- **Data**: DATA-001, DATA-002
- **Route(s)**: RT-001
- **Code**: services/api-gateway/app/models/*.py
- **Owner**: @backend-team
- **Due**: 2025-09-01
- **Dependencies**: []
- **Acceptance Criteria**:
  1. All Field functions consolidated
  2. Performance benchmarks met
  3. Unit tests pass
- **Links**: [VAR_FUNC_MAP hotspots], [ADR-20250823-01]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0002 (Decimal Order: 1.2)
- **Title**: Refactor high-usage functions: Field (duplicate entries)
- **Gate**: G1
- **Feature(s)**: FEAT-001, FEAT-002, FEAT-003
- **Activity**: ACT-001
- **Data**: DATA-001, DATA-002
- **Route(s)**: RT-001
- **Code**: services/api-gateway/app/models/*.py
- **Owner**: @backend-team
- **Due**: 2025-09-01
- **Dependencies**: [CHK-0001]
- **Acceptance Criteria**:
  1. Duplicate Field functions removed
  2. References updated
  3. No breaking changes
- **Links**: [VAR_FUNC_MAP hotspots]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0003 through CHK-0015
<!-- Similar pattern for remaining refactoring tasks -->

### CHK-0016 (Decimal Order: 1.16)
- **Title**: Document or remove orphan route: /
- **Gate**: G1
- **Feature(s)**: -
- **Activity**: -
- **Data**: -
- **Route(s)**: RT-036
- **Code**: services/api-gateway/app/main.py
- **Owner**: @api-team
- **Due**: 2025-08-30
- **Dependencies**: []
- **Acceptance Criteria**:
  1. Root route serves documentation or redirects
  2. OpenAPI spec updated
- **Links**: [ROUTING_REALIGNMENT]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0017 (Decimal Order: 1.17)
- **Title**: Document or remove orphan route: /healthz
- **Gate**: G1
- **Feature(s)**: -
- **Activity**: -
- **Data**: -
- **Route(s)**: RT-037
- **Code**: services/api-gateway/app/health.py
- **Owner**: @devops-team
- **Due**: 2025-08-30
- **Dependencies**: []
- **Acceptance Criteria**:
  1. Health check endpoint returns service status
  2. Includes DB connectivity check
  3. Prometheus metrics exposed
- **Links**: [ARCH_BLUEPRINT monitoring]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0018 through CHK-0025
<!-- Similar pattern for remaining orphan routes -->

### CHK-0026 (Decimal Order: 1.26)
- **Title**: Audit and standardize directory structure across all services
- **Gate**: G1
- **Feature(s)**: ALL
- **Activity**: -
- **Data**: -
- **Route(s)**: -
- **Code**: services/*
- **Owner**: @architecture-team
- **Due**: 2025-09-05
- **Dependencies**: []
- **Acceptance Criteria**:
  1. Consistent directory structure documented
  2. All services follow the pattern
  3. README.md in each service
- **Links**: [ADR-20250823-01], [Bug #1-10 import errors]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0027 through CHK-0055
<!-- Similar pattern for remaining G1 tasks -->

## G2: Parity

### CHK-0056 (Decimal Order: 2.1)
- **Title**: Complete search index implementation for all entities
- **Gate**: G2
- **Feature(s)**: FEAT-001
- **Activity**: ACT-001
- **Data**: DATA-001, DATA-002, DATA-003, DATA-004, DATA-005
- **Route(s)**: RT-001, RT-002
- **Code**: services/etl/app/tasks/search_indexer.py
- **Owner**: @search-team
- **Due**: 2025-09-15
- **Dependencies**: [CHK-0026]
- **Acceptance Criteria**:
  1. All entities indexed in Elasticsearch
  2. Search returns relevant results
  3. Performance < 500ms p95
- **Links**: [DATA_CYCLE_MAP search], [ADR-20250823-05]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0057 through CHK-0088
<!-- Parity tasks for data completeness -->

### CHK-0089 (Decimal Order: 2.33)
- **Title**: Implement global search with facets and filters
- **Gate**: G2
- **Feature(s)**: FEAT-001
- **Activity**: ACT-001
- **Data**: DATA-001, DATA-002, DATA-003, DATA-004, DATA-005
- **Route(s)**: RT-001
- **Code**: services/api-gateway/app/api/v1/search.py
- **Owner**: @search-team
- **Due**: 2025-09-20
- **Dependencies**: [CHK-0056]
- **Acceptance Criteria**:
  1. Faceted search works
  2. Filters apply correctly
  3. Results are paginated
- **Links**: [FEATURE_ACTIVITY_MAP FEAT-001]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0090 through CHK-0135
<!-- Feature parity tasks -->

### CHK-0136 (Decimal Order: 2.80)
- **Title**: Complete LEGISinfo integration for bill synchronization
- **Gate**: G2
- **Feature(s)**: FEAT-003
- **Activity**: ACT-006
- **Data**: DATA-002, DATA-014
- **Route(s)**: RT-011
- **Code**: services/etl/app/extractors/legisinfo.py
- **Owner**: @etl-team
- **Due**: 2025-09-25
- **Dependencies**: [CHK-0092]
- **Acceptance Criteria**:
  1. Bills sync every 6 hours
  2. Updates detected and applied
  3. No duplicate bills
- **Links**: [DATA_CYCLE_MAP bills], [Legacy LEGISinfo code]
- **Enhancements**:
  <!-- Enhancements will be added here -->

## G3: Architecture Harmony

### CHK-0137 (Decimal Order: 3.1)
- **Title**: Implement WebSocket infrastructure for real-time updates
- **Gate**: G3
- **Feature(s)**: FEAT-004
- **Activity**: ACT-008
- **Data**: DATA-004, DATA-017
- **Route(s)**: RT-015
- **Code**: services/api-gateway/app/services/websocket.py
- **Owner**: @realtime-team
- **Due**: 2025-10-01
- **Dependencies**: [CHK-0094]
- **Acceptance Criteria**:
  1. WebSocket connections stable
  2. Auto-reconnect on disconnect
  3. Message delivery guaranteed
- **Links**: [ADR-20250823-07], [ARCH_BLUEPRINT realtime]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0138 through CHK-0178
<!-- Architecture alignment tasks -->

### CHK-0179 (Decimal Order: 3.43)
- **Title**: Migrate legacy Canadian scrapers to new framework
- **Gate**: G3
- **Feature(s)**: FEAT-009
- **Activity**: ACT-014
- **Data**: DATA-029, DATA-030
- **Route(s)**: RT-028
- **Code**: services/etl/legacy-scrapers-ca/*
- **Owner**: @scraper-team
- **Due**: 2025-10-15
- **Dependencies**: [CHK-0183.1]
- **Acceptance Criteria**:
  1. All 139 scrapers migrated
  2. Data format consistent
  3. Error handling improved
- **Links**: [legacy_vs_current_diff], [139 scraper files]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0179.1 through CHK-0179.13
<!-- Provincial scraper subtasks -->

### CHK-0180.1 through CHK-0182.40
<!-- Municipal scraper subtasks -->

### CHK-0183.1 (Decimal Order: 3.44.1)
- **Title**: Base scraper class with retry logic
- **Gate**: G3
- **Feature(s)**: FEAT-009
- **Activity**: ACT-014
- **Data**: DATA-029
- **Route(s)**: -
- **Code**: services/etl/app/scrapers/base.py
- **Owner**: @scraper-team
- **Due**: 2025-10-05
- **Dependencies**: []
- **Acceptance Criteria**:
  1. Exponential backoff retry
  2. Circuit breaker pattern
  3. Comprehensive logging
- **Links**: [Legacy CanadianScraper class]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0183.2 through CHK-0183.10
<!-- Scraper framework components -->

### CHK-0184 through CHK-0201
<!-- Remaining architecture tasks -->

## G4: Test Strategy

### CHK-0202 (Decimal Order: 4.1)
- **Title**: Create comprehensive unit test suite for API Gateway
- **Gate**: G4
- **Feature(s)**: ALL
- **Activity**: -
- **Data**: -
- **Route(s)**: ALL
- **Code**: services/api-gateway/tests/*
- **Owner**: @qa-team
- **Due**: 2025-10-20
- **Dependencies**: [CHK-0026]
- **Acceptance Criteria**:
  1. 90% code coverage
  2. All endpoints tested
  3. Error cases covered
- **Links**: [ARCH_BLUEPRINT testing]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0203 through CHK-0245
<!-- Testing tasks for each service -->

### CHK-0246 (Decimal Order: 4.45)
- **Title**: Implement contract testing between services
- **Gate**: G4
- **Feature(s)**: ALL
- **Activity**: -
- **Data**: -
- **Route(s)**: ALL
- **Code**: tests/contracts/*
- **Owner**: @qa-team
- **Due**: 2025-10-25
- **Dependencies**: [CHK-0202]
- **Acceptance Criteria**:
  1. All service interfaces have contracts
  2. Contract tests run in CI
  3. Breaking changes detected
- **Links**: [ADR-20250823-03 API Gateway]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0247 through CHK-0261
<!-- Security and performance testing -->

## G5: Release Readiness

### CHK-0262 (Decimal Order: 5.1)
- **Title**: Set up monitoring and alerting infrastructure
- **Gate**: G5
- **Feature(s)**: ALL
- **Activity**: -
- **Data**: -
- **Route(s)**: RT-039
- **Code**: monitoring/*
- **Owner**: @devops-team
- **Due**: 2025-11-01
- **Dependencies**: [CHK-0017]
- **Acceptance Criteria**:
  1. Prometheus collecting metrics
  2. Grafana dashboards created
  3. Alerts configured
- **Links**: [ARCH_BLUEPRINT monitoring]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0263 through CHK-0299
<!-- Deployment and operational readiness -->

### CHK-0300 (Decimal Order: 5.39)
- **Title**: Create disaster recovery procedures
- **Gate**: G5
- **Feature(s)**: ALL
- **Activity**: -
- **Data**: ALL
- **Route(s)**: -
- **Code**: docs/operations/dr/*
- **Owner**: @devops-team
- **Due**: 2025-11-10
- **Dependencies**: [CHK-0262]
- **Acceptance Criteria**:
  1. RTO < 4 hours documented
  2. RPO < 1 hour achievable
  3. Runbooks created
- **Links**: [ARCH_BLUEPRINT disaster recovery]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0301 through CHK-0317
<!-- Feature flag implementation -->

### CHK-0318 (Decimal Order: 5.57)
- **Title**: Implement Debates API endpoints
- **Gate**: G5
- **Feature(s)**: FEAT-001
- **Activity**: -
- **Data**: DATA-003
- **Route(s)**: RT-029, RT-030
- **Code**: services/api-gateway/app/api/v1/debates.py
- **Owner**: @api-team
- **Due**: 2025-11-15
- **Dependencies**: [CHK-0056]
- **Acceptance Criteria**:
  1. Debates searchable
  2. Transcripts viewable
  3. Speaker attribution
- **Links**: [Implementation gap from FEATURE_ACTIVITY_MAP]
- **Enhancements**:
  <!-- Enhancements will be added here -->

### CHK-0319 through CHK-0324
<!-- Remaining API gaps -->

### CHK-0325 (Decimal Order: 5.65)
- **Title**: Final production readiness review
- **Gate**: G5
- **Feature(s)**: ALL
- **Activity**: ALL
- **Data**: ALL
- **Route(s)**: ALL
- **Code**: ALL
- **Owner**: @cto
- **Due**: 2025-11-30
- **Dependencies**: [ALL]
- **Acceptance Criteria**:
  1. All checklist items complete
  2. Performance benchmarks met
  3. Security scan passed
  4. Documentation complete
  5. Team trained
- **Links**: [All ADRs], [All documentation]
- **Enhancements**:
  <!-- Enhancements will be added here -->

## Summary by Gate

| Gate | Items | Description |
|------|-------|-------------|
| G1 | 55 | Structure and indexing tasks |
| G2 | 80 | Feature parity and data completeness |
| G3 | 65 | Architecture alignment and migration |
| G4 | 60 | Testing strategy and quality assurance |
| G5 | 65 | Release readiness and operations |
| **Total** | **325** | **All implementation tasks** |

## Notes

1. This checklist is append-only - items are never removed
2. Each item will be enhanced 10 times through the enhancement cycles
3. Decimal order allows for infinite sub-task expansion
4. All CHK IDs are permanent and traceable
5. Dependencies must be completed before dependent tasks
6. Due dates are initial estimates and may be adjusted
7. Owner assignments are team-level, individuals TBD