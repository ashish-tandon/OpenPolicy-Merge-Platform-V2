# Realignment Execution Plan


## Deviation Realignment Plan - 2025-08-23

### Executive Summary
- Missing Features: 12
- Partial Implementations: 4
- Drifted Implementations: 59
- Extra Implementations: 12310

### Realignment by Gate

#### Gate 1: Structure & Index (Foundation)
**Missing P0 Features** - Critical for platform operation

- [ ] Implement FEAT-004: Feature Flags
  - Owner: TBD
  - Due: Sprint 1
  - Dependencies: Data model, API design

- [ ] Implement FEAT-014: Authentication System
  - Owner: TBD
  - Due: Sprint 1
  - Dependencies: Data model, API design

- [ ] Implement FEAT-015: Member Management
  - Owner: TBD
  - Due: Sprint 1
  - Dependencies: Data model, API design

#### Gate 2: Feature Parity
**Partial Implementations** - Complete missing components

- [ ] Complete FEAT-002: Session Tracking for Beta Users (33% done)
  - Missing: API endpoint, Database schema, UI component
  - Owner: TBD
  - Due: Sprint 2

- [ ] Complete FEAT-016: Bill Tracking (40% done)
  - Missing: Business logic, Database schema, UI component
  - Owner: TBD
  - Due: Sprint 2

- [ ] Complete FEAT-017: Vote Recording (20% done)
  - Missing: Business logic, Database schema, UI component
  - Owner: TBD
  - Due: Sprint 2

- [ ] Complete FEAT-019: Committee Management (67% done)
  - Missing: Business logic, Database schema, UI component
  - Owner: TBD
  - Due: Sprint 2

#### Gate 3: Architecture Harmony
**Drifted Implementations** - Align with specifications

- [ ] Refactor FEAT-001: general_drift
  - Current: GET /api/v1/search
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-001: general_drift
  - Current: findMPByPostalCode() in services/web-ui/src/app/search/postal/[code]/page.tsx
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-001: general_drift
  - Current: PostalSearchPage() in services/web-ui/src/app/search/postal/[code]/page.tsx
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-001: general_drift
  - Current: getPartyColor() in services/web-ui/src/app/search/postal/[code]/page.tsx
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-001: non_restful_api
  - Current: GET /api/v1/search/postcode/{postcode}
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-002: general_drift
  - Current: User() in services/user-service/app/api/v1/users.py
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-006: general_drift
  - Current: GET /api/v1/bills
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-006: general_drift
  - Current: GET /api/v1/members
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-006: general_drift
  - Current: GET /api/v1/votes
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-006: general_drift
  - Current: GET /api/v1/debates
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-006: general_drift
  - Current: GET /api/v1/committees
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-006: general_drift
  - Current: GET /api/v1/jurisdictions
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-006: general_drift
  - Current: GET /api/v1/representatives
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-006: general_drift
  - Current: GET /api/v1/offices
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-006: general_drift
  - Current: GET /api/v1/search
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-006: general_drift
  - Current: GET /api/v1/bills/{bill_id}
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-006: general_drift
  - Current: GET /api/v1/members/{member_id}
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-006: general_drift
  - Current: GET /api/v1/committees/{committee_slug}
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-006: non_restful_api
  - Current: GET /api/v1/search/postcode/{postcode}
  - Target: Align with feature spec
  - Owner: TBD

- [ ] Refactor FEAT-009: general_drift
  - Current: for() in services/web-ui/src/components/ui/Theme.tsx
  - Target: Align with feature spec
  - Owner: TBD

#### Gate 4: Scope Management
**Extra Implementations** - Evaluate and classify

##### Evaluate Data Model (2 items)
- [ ] Table: 
- [ ] Table: 

##### Evaluate For Feature Mapping (9651 items)
- [ ] test_mcp_server() in test-mcp-simple.py
- [ ] print() in test-mcp-simple.py
- [ ] OpenMetadataMCPServer() in test-mcp-simple.py
- [ ] len() in test-mcp-simple.py
- [ ] __init__() in mcp-openmetadata-server.py
- ... and 9646 more

##### Evaluate For New Feature (5 items)
- [ ] POST /api/v1/bills/{bill_id}/cast-vote
- [ ] GET /api/v1/members/{member_id}/votes
- [ ] GET /api/v1/votes/{session_id}/{vote_number}
- [ ] GET /api/v1/debates/{year}/{month}/{day}
- [ ] GET /api/v1/debates/speeches/{speech_id}

##### Keep As Utility (95 items)
- [ ] define_transformation_phases() in scripts/arch_synthesis.py
- [ ] trace_transformations() in scripts/data_journey.py
- [ ] TestUtilities() in services/api-gateway/tests/test_config.py
- [ ] test_get_email_analytics_invalid_date_format() in services/api-gateway/tests/test_email_alerts.py
- [ ] TestDataHelpers() in services/api-gateway/tests/fixtures/test_utilities.py
- ... and 90 more

##### Requires Review (2557 items)
- [ ] Class: OpenMetadataMCPServer
- [ ] Class: CodeMapper
- [ ] Class: PythonVisitor
- [ ] Class: ArchitectureSynthesizer
- [ ] Class: DataJourneyMapper
- ... and 2552 more

### Risk Mitigation

#### High Risks
1. **Data Model Changes**: Some realignments may require schema migration
   - Mitigation: Create backwards-compatible migrations
2. **API Breaking Changes**: Drift corrections might break existing clients
   - Mitigation: Version APIs and maintain legacy endpoints
3. **Feature Scope Creep**: Extra implementations might indicate scope expansion
   - Mitigation: Document and get approval for new features

#### Dependencies
- Database migration framework must be operational
- API versioning strategy must be implemented
- Feature flag system for gradual rollout

## Plan Append (2025-08-23 20:36:28)
| FEAT | Name | Type | Method | Endpoint/Symbol | Class | Action |
|---|---|---|---|---|---|---|

## Plan Append (2025-08-23 20:36:59)
| FEAT | Name | Evidence | Endpoint/Module | Drift Type | Action |
|---|---|---|---|---|---|
| FEAT-003 | Feedback Collection | Not found in codebase | N/A | MISSING | Implement according to spec |
| FEAT-004 | Feature Flags | Not found in codebase | N/A | MISSING | Implement according to spec |
| FEAT-005 | Data Dashboard | Not found in codebase | N/A | MISSING | Implement according to spec |
| FEAT-007 | Email Notifications | Not found in codebase | N/A | MISSING | Implement according to spec |
| FEAT-008 | SMS Notifications | Not found in codebase | N/A | MISSING | Implement according to spec |
| FEAT-010 | Social Sharing | Not found in codebase | N/A | MISSING | Implement according to spec |
| FEAT-012 | Offline Support | Not found in codebase | N/A | MISSING | Implement according to spec |
| FEAT-013 | AI Enhancement | Not found in codebase | N/A | MISSING | Implement according to spec |
| FEAT-014 | Authentication System | Not found in codebase | N/A | MISSING | Implement according to spec |
| FEAT-015 | Member Management | Not found in codebase | N/A | MISSING | Implement according to spec |
| FEAT-018 | Debate Transcripts | Not found in codebase | N/A | MISSING | Implement according to spec |
| FEAT-020 | News Aggregation | Not found in codebase | N/A | MISSING | Implement according to spec |
| FEAT-002 | Session Tracking for Beta Users | 33% coverage | User() in services/user-service/app/api/v1/users.py | PARTIAL | Complete implementation |
| FEAT-016 | Bill Tracking | 40% coverage | GET /api/v1/bills, GET /api/v1/bills/{bill_id} | PARTIAL | Complete implementation |
| FEAT-017 | Vote Recording | 20% coverage | GET /api/v1/votes | PARTIAL | Complete implementation |
| FEAT-019 | Committee Management | 67% coverage | GET /api/v1/committees, GET /api/v1/committees/{committee_slug} | PARTIAL | Complete implementation |
| FEAT-001 | Global Search with Postal Code MP Lookup | Score: 0.50 | GET /api/v1/search | DRIFT (general_drift) | Review |
| FEAT-001 | Global Search with Postal Code MP Lookup | Score: 0.43 | findMPByPostalCode() in services/web-ui/src/app/search/postal/[code]/page.tsx | DRIFT (general_drift) | Review |
| FEAT-001 | Global Search with Postal Code MP Lookup | Score: 0.43 | PostalSearchPage() in services/web-ui/src/app/search/postal/[code]/page.tsx | DRIFT (general_drift) | Review |
| FEAT-001 | Global Search with Postal Code MP Lookup | Score: 0.43 | getPartyColor() in services/web-ui/src/app/search/postal/[code]/page.tsx | DRIFT (general_drift) | Review |
| FEAT-001 | Global Search with Postal Code MP Lookup | Score: 0.33 | GET /api/v1/search/postcode/{postcode} | DRIFT (non_restful_api) | Review |
| FEAT-002 | Session Tracking for Beta Users | Score: 0.33 | User() in services/user-service/app/api/v1/users.py | DRIFT (general_drift) | Review |
| FEAT-006 | Basic API Documentation | Score: 0.50 | GET /api/v1/bills | DRIFT (general_drift) | Review |
| FEAT-006 | Basic API Documentation | Score: 0.50 | GET /api/v1/members | DRIFT (general_drift) | Review |
| FEAT-006 | Basic API Documentation | Score: 0.50 | GET /api/v1/votes | DRIFT (general_drift) | Review |
| FEAT-006 | Basic API Documentation | Score: 0.50 | GET /api/v1/debates | DRIFT (general_drift) | Review |
| FEAT-006 | Basic API Documentation | Score: 0.50 | GET /api/v1/committees | DRIFT (general_drift) | Review |
| FEAT-006 | Basic API Documentation | Score: 0.50 | GET /api/v1/jurisdictions | DRIFT (general_drift) | Review |
| FEAT-006 | Basic API Documentation | Score: 0.50 | GET /api/v1/representatives | DRIFT (general_drift) | Review |
| FEAT-006 | Basic API Documentation | Score: 0.50 | GET /api/v1/offices | DRIFT (general_drift) | Review |
| FEAT-006 | Basic API Documentation | Score: 0.50 | GET /api/v1/search | DRIFT (general_drift) | Review |
| FEAT-006 | Basic API Documentation | Score: 0.33 | GET /api/v1/bills/{bill_id} | DRIFT (general_drift) | Review |
| FEAT-006 | Basic API Documentation | Score: 0.33 | GET /api/v1/members/{member_id} | DRIFT (general_drift) | Review |
| FEAT-006 | Basic API Documentation | Score: 0.33 | GET /api/v1/committees/{committee_slug} | DRIFT (general_drift) | Review |
| FEAT-006 | Basic API Documentation | Score: 0.33 | GET /api/v1/search/postcode/{postcode} | DRIFT (non_restful_api) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | for() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | ThemeProvider() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | useTheme() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | ThemeToggle() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | ColorSchemePicker() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | ThemeSwitcher() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | ThemeAware() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | HighContrastToggle() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | FontSizeToggle() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | ReducedMotionToggle() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | ThemeSettingsPanel() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | handleChange() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | setTheme() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | setColorScheme() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | toggleTheme() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | getThemeIcon() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | getThemeLabel() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | toggleHighContrast() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | changeFontSize() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-009 | Theme Customization | Score: 0.50 | toggleReducedMotion() in services/web-ui/src/components/ui/Theme.tsx | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/ensure_feature_stubs.py | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/var_func_map.py | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/verify_feature_checklist_ids.py | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/arch_synthesis.py | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/data_journey.py | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/multi_loop_runner.py | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/env_audit.py | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/ten_pass_merge.py | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/complete_all_passes.py | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/generate_lineage.py | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/source_of_truth.py | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/routing_realignment.py | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/exec_plan.py | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/bug_audit.py | DRIFT (general_drift) | Review |
| FEAT-011 | Print View | Score: 0.33 | print() in scripts/flow_design.py | DRIFT (general_drift) | Review |
| FEAT-016 | Bill Tracking | Score: 0.50 | GET /api/v1/bills | DRIFT (general_drift) | Review |
| FEAT-016 | Bill Tracking | Score: 0.33 | GET /api/v1/bills/{bill_id} | DRIFT (general_drift) | Review |
| FEAT-017 | Vote Recording | Score: 0.50 | GET /api/v1/votes | DRIFT (general_drift) | Review |
| FEAT-019 | Committee Management | Score: 0.50 | GET /api/v1/committees | DRIFT (general_drift) | Review |
| FEAT-019 | Committee Management | Score: 0.33 | GET /api/v1/committees/{committee_slug} | DRIFT (general_drift) | Review |
| NEW-FEAT | Unplanned Implementation | Found in codebase | POST /api/v1/bills/{bill_id}/cast-vote | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | GET /api/v1/members/{member_id}/votes | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | GET /api/v1/votes/{session_id}/{vote_number} | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | GET /api/v1/debates/{year}/{month}/{day} | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | GET /api/v1/debates/speeches/{speech_id} | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | Table:  | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | Table:  | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | test_mcp_server() in test-mcp-simple.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | print() in test-mcp-simple.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | OpenMetadataMCPServer() in test-mcp-simple.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | len() in test-mcp-simple.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | Class: OpenMetadataMCPServer | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | __init__() in mcp-openmetadata-server.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | get_platform_overview() in mcp-openmetadata-server.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | len() in mcp-openmetadata-server.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | str() in mcp-openmetadata-server.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | get_data_flow_mapping() in mcp-openmetadata-server.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | main() in mcp-openmetadata-server.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | print() in mcp-openmetadata-server.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | OpenMetadataMCPServer() in mcp-openmetadata-server.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | input() in mcp-openmetadata-server.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | open() in scripts/ensure_feature_stubs.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | len() in scripts/ensure_feature_stubs.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | Class: CodeMapper | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | __init__() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | Path() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | defaultdict() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | get_or_create_node() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | str() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | add_edge() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | analyze_python_file() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | open() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | Class: PythonVisitor | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | visit_FunctionDef() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | hasattr() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | visit_ClassDef() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | visit_Assign() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | isinstance() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | visit_Call() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | visit_Import() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | visit_ImportFrom() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | PythonVisitor() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | analyze_javascript_file() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | analyze_sql_file() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | analyze_codebase() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | any() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | generate_hotspots() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | sorted() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | export_json() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |
| NEW-FEAT | Unplanned Implementation | Found in codebase | list() in scripts/var_func_map.py | EXTRA | Evaluate scope → map/legacy/ADR |

## Realignment Execution Batch 1 - CHK Mapping (2025-08-23)

### CHK Item References

All deviations have been mapped to decimal CHK items in `REALIGNMENT_CHECKLIST_BATCH1.md`:

#### Missing Features → CHK Items
- FEAT-003 (Feedback Collection) → CHK-0300.1
- FEAT-004 (Feature Flags) → CHK-0300.2
- FEAT-005 (Data Dashboard) → CHK-0300.3
- FEAT-007 (Email Notifications) → CHK-0300.4
- FEAT-008 (SMS Notifications) → CHK-0300.5
- FEAT-010 (Social Sharing) → CHK-0300.6
- FEAT-012 (Offline Support) → CHK-0300.7
- FEAT-013 (AI Enhancement) → CHK-0300.8
- FEAT-014 (Authentication System) → CHK-0300.9
- FEAT-015 (Member Management) → CHK-0300.10
- FEAT-018 (Debate Transcripts) → CHK-0300.11
- FEAT-020 (News Aggregation) → CHK-0300.12

#### Partial Implementations → CHK Items
- FEAT-002 (Session Tracking 33%) → CHK-0301.1
- FEAT-016 (Bill Tracking 40%) → CHK-0301.2
- FEAT-017 (Vote Recording 20%) → CHK-0301.3
- FEAT-019 (Committee Management 67%) → CHK-0301.4

#### Drift Corrections → CHK Items
- FEAT-001 (Search API Drift) → CHK-0302.1
- FEAT-001 (Postal Code Non-REST) → CHK-0302.2
- FEAT-001 (Frontend Functions) → CHK-0302.3
- FEAT-006 (API Documentation) → CHK-0302.4
- FEAT-009 (Theme System) → CHK-0302.5
- FEAT-011 (Print View) → CHK-0302.6

#### Extra Implementations → CHK Items
- New API Endpoints → CHK-0303.1 (ADR-20250823-101)
- Legacy JS Libraries → CHK-0303.2 (Move to /legacy)
- Test Utilities → CHK-0303.3 (Keep as utilities)
- MCP Server Components → CHK-0303.4 (ADR-20250823-102)
- Script Utilities → CHK-0303.5 (Keep as dev tools)

### Execution Priority Order

1. **P0 Critical (Sprint 1)**
   - CHK-0300.2 (Feature Flags)
   - CHK-0300.9 (Authentication)
   - CHK-0300.10 (Member Management)
   - CHK-0301.2 (Bill Tracking)
   - CHK-0301.3 (Vote Recording)
   - CHK-0301.4 (Committee Management)
   - CHK-0302.1 (Search API)
   - CHK-0302.2 (Postal Code API)
   - CHK-0302.3 (Frontend Functions)

2. **P1 High (Sprint 2)**
   - CHK-0300.1 (Feedback Collection)
   - CHK-0300.11 (Debate Transcripts)
   - CHK-0301.1 (Session Tracking)
   - CHK-0302.4 (API Documentation)

3. **P2 Medium (Sprint 3)**
   - CHK-0300.3 (Data Dashboard)
   - CHK-0300.4 (Email Notifications)
   - CHK-0300.12 (News Aggregation)
   - CHK-0302.5 (Theme System)
   - CHK-0303.1 (New Endpoints ADR)
   - CHK-0303.4 (MCP Server ADR)

4. **P3 Low (Sprint 4)**
   - CHK-0300.5 (SMS Notifications)
   - CHK-0300.6 (Social Sharing)
   - CHK-0300.7 (Offline Support)
   - CHK-0300.8 (AI Enhancement)
   - CHK-0302.6 (Print View)
   - CHK-0303.2 (Legacy Migration)
   - CHK-0303.3 (Utilities)
   - CHK-0303.5 (Dev Tools)

### Verification Gates

After each sprint, verify:
1. All CHK items completed have passing tests
2. API contracts match specifications
3. Documentation is updated
4. No new drift introduced
5. SoT crosslinks updated
