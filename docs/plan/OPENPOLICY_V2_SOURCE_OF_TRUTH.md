# OpenPolicy V2 — Source of Truth (SoT)

## Purpose
Authoritative plan aligning features, data flows, architecture, checklists, tests, and bugs.

## Golden Index
- Validation Suite (27+ docs): /workspace/docs/validation/
- Artifacts: /workspace/artifacts/{api,ui,db}/pass1/
- Execution Checklist (primary): UPDATED_MASTER_EXECUTION_CHECKLIST.md
- Architecture: FUTURE_STATE_ARCHITECTURE.md, API_DESIGN_SPECIFICATION.md
- Testing: COMPREHENSIVE_TESTING_STRATEGIES.md
- Repo Mapping: COMPREHENSIVE_REPO_ANALYSIS_pass1.md
- Technical Debt: CODE_DEVIATIONS_ANALYSIS.md
- Feature Inventory: FEATURE_COMPARISON_pass1.csv

## Alignment Model
- Feature → Data Entities → APIs → UI Flows → Tests → Rollout → Ops
- Every item must link to an Execution Checklist task ID.

## Gate Criteria (G1..G5)
- G1 Structure & Index: Index completeness ≥ 95%
- G2 Feature/Data/Route Parity: Legacy parity = 100%, gaps documented
- G3 Architecture Harmony: All deltas resolved or accepted with rationale
- G4 Test Strategy: Coverage plan ≥ 80%, CI jobs defined
- G5 Release Readiness: PRD-ready docs, runbooks, rollback plans

## Change Log
- Track all alignment decisions and deltas with YYYY-MM-DD entries.