# OpenPolicy V2 — Source of Truth (SoT)

## Purpose
Authoritative plan aligning features, data flows, architecture, checklists, tests, and bugs.

## Golden Index

### Core Documentation
- **Execution Checklist**: /workspace/docs/validation/UPDATED_MASTER_EXECUTION_CHECKLIST.md
- **API Specification**: /workspace/docs/validation/API_DESIGN_SPECIFICATION.md

### Validation Reports
- **Database Validation**: /workspace/artifacts/db/pass1/database_validation_report.md
- **API Validation**: /workspace/artifacts/api/pass1/api_validation_report.md
- **UI Validation**: /workspace/artifacts/ui/pass1/ui_validation_report.md
- **Scraper Validation**: /workspace/artifacts/db/pass1/scraper_validation_report.md

### Plan Documents
- **Feature Mapping**: /workspace/docs/plan/features/FEATURE_MAPPING_UNIFIED.md
- **Data Lineage Map**: /workspace/docs/plan/lineage/DATA_LINEAGE_MAP.md
- **Data Lineage Auto**: /workspace/docs/plan/lineage/DATA_LINEAGE_AUTO.md
- **Architecture Alignment**: /workspace/docs/plan/architecture/ARCHITECTURE_ALIGNMENT.md
- **Bug Reconciliation**: /workspace/docs/bugs/BUGS_RECONCILIATION.md
- **Review Gates**: /workspace/docs/reviews/ALIGNMENT_GATES_LOG.md

### Implementation Documentation
- **API Gateway README**: /workspace/services/api-gateway/README.md
- **ETL Data Mapping**: /workspace/services/etl/docs/COMPREHENSIVE_DATA_MAPPING_AND_SCHEMA_REPORT.md
- **Web UI Status**: /workspace/services/web-ui/FINAL_IMPLEMENTATION_STATUS.md
- **Admin UI Summary**: /workspace/services/admin-ui/docs/ADMIN_UI_IMPLEMENTATION_SUMMARY.md
- **Project Setup Guide**: /workspace/docs/PROJECT_SETUP_AND_DEPLOYMENT_GUIDE.md

### Migration & Legacy
- **Migration Plan**: /workspace/docs/Open Parliament Migration Plan/README.md
- **Legacy Code Mapping**: /workspace/docs/Open Parliament Migration Plan/13-LEGACY-CODE-MAPPING.md
- **Data Flow Mapping**: /workspace/docs/Open Parliament Migration Plan/12-DATA-FLOW-MAPPING.md

## Alignment Model
- Feature → Data Entities → APIs → UI Flows → Tests → Rollout → Ops
- Every item must link to an Execution Checklist task ID.

## Gate Criteria (G1..G5)
- G1 Structure & Index: Index completeness ≥ 95%
- G2 Feature/Data/Route Parity: Legacy parity = 100%, gaps documented
- G3 Architecture Harmony: All deltas resolved or accepted with rationale
- G4 Test Strategy: Coverage plan ≥ 80%, CI jobs defined
- G5 Release Readiness: PRD-ready docs, runbooks, rollback plans

## Implementation Status
- **Features Implemented**: 84/120+ (70%)
- **API Endpoints**: 137 validated
- **Database Schemas**: 3 schemas, 12+ tables
- **Scrapers**: 100+ jurisdictions covered
- **UI Components**: 84 features across 6 phases

## Change Log
- 2025-01-20: Initial SoT creation with validation artifacts
- 2025-01-20: Added implementation documentation references
- 2025-01-20: Linked feature mapping with execution checklist IDs