# Implementation Instructions for Agent

## 🎯 Mission Statement
You are tasked with implementing the OpenPolicy V2 platform based on the comprehensive documentation created. Your mission is to follow the established plans exactly without deviation, working systematically through the todo lists and implementing features according to specifications.

## 📋 Primary Documents to Follow

### 1. Master Execution Checklist
**Location**: `/workspace/docs/validation/UPDATED_MASTER_EXECUTION_CHECKLIST.md`
- This is your primary guide
- Work through tasks in order: 1.x → 2.x → 3.x etc.
- Mark tasks as complete as you finish them
- Each task has a unique ID (e.g., [3.1], [4.2]) - reference these in commits

### 2. Bug Tracking Document
**Location**: `/workspace/docs/bugs/BUGS_RECONCILIATION.md`
- Contains 20 prioritized bugs (P0-P2)
- Fix P0 (Critical) bugs first: BUG-001, BUG-018
- Each bug has reproduction steps and links to features
- Update status as you fix each bug

### 3. Feature Mapping
**Location**: `/workspace/docs/plan/features/FEATURE_MAPPING_UNIFIED.md`
- 50 features documented with complete specifications
- Each feature has:
  - Unique ID (F001-F050)
  - Data entities required
  - API endpoints to implement
  - UI components needed
  - Test requirements
  - Execution checklist IDs

### 4. Data Lineage Map
**Location**: `/workspace/docs/plan/lineage/DATA_LINEAGE_MAP.md`
- Shows end-to-end data flow for each feature
- Follow the exact flow: Ingestion → Transform → Storage → API → UI
- Includes error handling requirements

## 🛠️ Implementation Order

### Phase 1: Critical Bug Fixes (Week 1)
```bash
# Start with P0 bugs
1. BUG-001: Implement authentication system
   - Follow Security docs: /workspace/docs/SECURITY_AND_COMPLIANCE.md
   - Section: "Authentication & Authorization"
   - Use JWT implementation provided

2. BUG-018: Setup database backups
   - Follow Runbooks: /workspace/docs/OPERATIONAL_RUNBOOKS.md
   - Section: "Database Operations → Backup Procedures"
   - Implement the backup script exactly as specified
```

### Phase 2: Complete Authentication (Week 1-2)
```bash
# Implement Feature F008 & F038
1. Review feature specifications in FEATURE_MAPPING_UNIFIED.md
2. Implement database models from: /workspace/services/api-gateway/app/models/users.py
3. Create API endpoints from: /workspace/services/api-gateway/app/api/v1/auth.py
4. Follow OAuth2 integration in SECURITY_AND_COMPLIANCE.md
5. Write tests as specified in COMPREHENSIVE_TESTING_STRATEGIES.md
```

### Phase 3: Complete Core Features (Week 2-4)
Follow execution checklist items in order:
- [3.1] Bills endpoints
- [3.2] Members endpoints
- [3.3] Votes endpoints
- [3.4] Debates endpoints
- [3.5] Committees endpoints

## 📝 Strict Rules to Follow

### 1. NO DEVIATIONS
- Do NOT create new features not in the documentation
- Do NOT change API contracts defined in `/workspace/docs/validation/API_DESIGN_SPECIFICATION.md`
- Do NOT modify database schemas without updating migrations
- Do NOT skip tests - follow `/workspace/docs/validation/COMPREHENSIVE_TESTING_STRATEGIES.md`

### 2. Use Existing Code
- **ALWAYS** check `/workspace/legacy/` for existing implementations
- Copy and adapt legacy code rather than writing from scratch
- Document any adaptations in code comments

### 3. Follow Established Patterns
```python
# Example: Always use this pattern for API endpoints
@router.get("/items/{item_id}")
async def get_item(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ItemResponse:
    """Get item by ID.
    
    Reference: Feature F003, Checklist [3.1]
    """
    # Implementation here
```

### 4. Testing Requirements
For EVERY implementation:
1. Write unit tests (minimum 80% coverage)
2. Write integration tests for API endpoints
3. Update E2E tests for user journeys
4. Run: `make test` before committing

### 5. Documentation Updates
When implementing each feature:
1. Update status in ALIGNMENT_GATES_LOG.md
2. Mark checklist items complete
3. Update bug status in BUGS_RECONCILIATION.md
4. Add implementation notes to feature in FEATURE_MAPPING_UNIFIED.md

## 🔄 Daily Workflow

### Morning
1. Check `/workspace/docs/plan/OPENPOLICY_V2_SOURCE_OF_TRUTH.md`
2. Review your current checklist item
3. Read the feature specification
4. Check for existing legacy code

### Implementation
1. Create feature branch: `git checkout -b impl/[checklist-id]-description`
2. Implement following the exact specifications
3. Write tests as you go (TDD approach)
4. Commit with reference: `feat: implement [3.1] bills API endpoints per spec`

### Evening
1. Run full test suite: `make test`
2. Update documentation with progress
3. Push changes: `git push origin impl/[checklist-id]-description`
4. Create PR with checklist item reference

## 🚫 What NOT to Do

### DON'T:
- ❌ Refactor working code "to make it better"
- ❌ Add features because "users might want it"
- ❌ Change API responses from specifications
- ❌ Skip writing tests to "save time"
- ❌ Implement your own authentication
- ❌ Create new database tables not in schema
- ❌ Modify the monitoring setup
- ❌ Change deployment configurations

### DO:
- ✅ Follow specifications exactly
- ✅ Copy from legacy code when available
- ✅ Write tests for everything
- ✅ Update documentation as you go
- ✅ Ask for clarification if specs unclear
- ✅ Commit frequently with clear messages
- ✅ Keep PRs small and focused

## 📊 Progress Tracking

### Use the Makefile commands:
```bash
# Check documentation compliance
make docs-audit

# Verify all features have checklist IDs
make verify-features

# Run 10-pass validation
make ten-pass-merge

# Run all tests
make test
```

### Update todos:
```python
# When starting a task
todo_write(merge=True, todos=[{
    "id": "impl-3.1", 
    "content": "Implement bills API endpoints",
    "status": "in_progress"
}])

# When completing a task
todo_write(merge=True, todos=[{
    "id": "impl-3.1",
    "content": "Implement bills API endpoints", 
    "status": "completed"
}])
```

## 🎯 Success Criteria

You are successful when:
1. All P0 and P1 bugs are fixed
2. All checklist items [3.1] through [5.6] are complete
3. Test coverage is ≥80% overall, ≥95% for critical paths
4. All features match their specifications exactly
5. No deviations from documented architecture
6. All tests passing in CI/CD

## 🚀 Getting Started

1. First, read these documents in order:
   - DOCUMENTATION_CONSOLIDATION_FINAL_REPORT.md
   - docs/plan/OPENPOLICY_V2_SOURCE_OF_TRUTH.md
   - docs/validation/UPDATED_MASTER_EXECUTION_CHECKLIST.md

2. Set up your environment:
   ```bash
   ./setup_dev_environment.sh
   docker-compose up -d
   make test  # Verify everything works
   ```

3. Start with BUG-001 (Authentication):
   - Read the bug description
   - Find Feature F008 in FEATURE_MAPPING_UNIFIED.md
   - Follow the implementation in SECURITY_AND_COMPLIANCE.md
   - Use existing code from services/api-gateway/app/api/v1/auth.py

## 📞 When to Seek Clarification

Only ask for help if:
- A specification conflicts with another specification
- Required legacy code is missing
- Tests are failing due to infrastructure issues
- You find a security vulnerability not documented

Do NOT ask for help on:
- How to implement a feature (it's documented)
- What order to do things (follow the checklist)
- Whether to add a feature (if not documented, don't add)
- How to test something (see COMPREHENSIVE_TESTING_STRATEGIES.md)

---

**Remember**: Your job is to implement exactly what's documented. No more, no less. The documentation is complete and correct. Trust it and follow it precisely.