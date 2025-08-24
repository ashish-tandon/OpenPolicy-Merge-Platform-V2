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
