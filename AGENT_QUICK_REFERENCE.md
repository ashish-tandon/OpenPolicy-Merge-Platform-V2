# AGENT QUICK REFERENCE - OpenPolicy V2

## 🚨 DAILY STARTUP CHECKLIST

### 1. Fresh Shell Setup
```bash
cd /workspace
source services/api-gateway/venv/bin/activate
source services/etl/venv/bin/activate
```

### 2. Check Current Status
```bash
make health-check
make docs-audit
```

### 3. Review Today's Goals
- Check `IMPLEMENTATION_PROGRESS.md`
- Review next checklist item from `MASTER_EXECUTION_CHECKLIST.md`
- Read relevant feature spec from `FEATURE_MAPPING_UNIFIED.md`

## 📋 IMPLEMENTATION PRIORITIES

### P0 CRITICAL (Fix First)
- [ ] BUG-001: Authentication system
- [ ] BUG-018: Database backups
- [ ] Feature F001: Global Search
- [ ] Feature F002: MP Database
- [ ] Feature F003: Bills Tracking
- [ ] Feature F004: Voting Records

### P1 HIGH (Implement Next)
- [ ] Feature F007: Multi-Level Government
- [ ] Feature F008: User Management
- [ ] Feature F009: Mobile API Support

## 🔧 ESSENTIAL COMMANDS

### Testing
```bash
# Run all tests
make test

# Run specific service
cd services/api-gateway && pytest
cd services/etl && pytest

# Check coverage
make coverage
```

### Validation
```bash
# Documentation audit
make docs-audit

# Feature verification
make verify-features

# Health check
make health-check
```

### Development
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

## 📚 REQUIRED DOCUMENTS

### Implementation Guide
- `AGENT_IMPLEMENTATION_PROMPT.md` - Your mission briefing
- `IMPLEMENTATION_INSTRUCTIONS_FOR_AGENT.md` - Detailed guide
- `docs/validation/MASTER_EXECUTION_CHECKLIST.md` - 93+ checklist items

### Feature Specifications
- `docs/plan/features/FEATURE_MAPPING_UNIFIED.md` - 50+ features
- `docs/validation/API_DESIGN_SPECIFICATION.md` - API contracts

### Bug Status
- `docs/bugs/BUGS_RECONCILIATION.md` - 20+ prioritized bugs

## 🚫 CRITICAL RULES - NEVER BREAK

### NO DEVIATIONS
- ❌ Don't add new features
- ❌ Don't change API specs
- ❌ Don't modify database schemas
- ❌ Don't ignore legacy code

### ALWAYS DO
- ✅ Check `/legacy` directory first
- ✅ Follow existing patterns
- ✅ Write tests for everything
- ✅ Follow checklist exactly

## 📊 PROGRESS TRACKING

### Daily Log Template
```markdown
## Date: [Current Date]

### Completed:
- [ ] [Feature/Bug] - Status: [Complete/In Progress]

### Blockers:
- [Description of any blockers]

### Next Steps:
1. [Next task]
2. [Following task]

### Notes:
- [Any important notes]
```

### Weekly Report Template
```markdown
## Week [X] Status Report

### Completed This Week:
- [List of completed features/bugs]

### Test Coverage:
- Current: [X]%
- Target: 80%+

### Blockers:
- [List any blockers]

### Next Week Plan:
- [List of planned work]
```

## 🚨 EMERGENCY PROCEDURES

### If Stuck:
1. Check documentation first
2. Review legacy code
3. Follow checklist exactly
4. Use validation tools
5. Continue with next item

### If Errors:
1. Read error messages carefully
2. Check existing implementations
3. Review test files
4. Check database state
5. Document the problem

## 🎯 SUCCESS METRICS

### Phase 1 (Week 1):
- ✅ All P0 bugs resolved
- ✅ Authentication working
- ✅ Database backups automated

### Phase 2 (Weeks 2-4):
- ✅ All P0 features implemented
- ✅ Core APIs functional
- ✅ Basic UI working

### Final (Week 8):
- ✅ Platform fully functional
- ✅ All tests passing
- ✅ Ready for production

## 📋 IMPLEMENTATION WORKFLOW

### For Each Feature:
1. Read spec from `FEATURE_MAPPING_UNIFIED.md`
2. Check legacy code in `/legacy`
3. Follow checklist from `MASTER_EXECUTION_CHECKLIST.md`
4. Implement following existing patterns
5. Write comprehensive tests
6. Update progress log
7. Run validation tools

### For Each Bug:
1. Read details from `BUGS_RECONCILIATION.md`
2. Identify root cause
3. Implement fix following patterns
4. Write regression tests
5. Verify fix works
6. Update bug status

## 🔍 LEGACY CODE CHECK

### Before Implementing ANYTHING:
```bash
cd /workspace/legacy
find . -name "*feature_name*" -type f
find . -name "*similar_function*" -type f
ls -la services/etl/legacy-scrapers-ca/
ls -la services/etl/legacy-civic-scraper/
```

### Common Legacy Locations:
- `/legacy/services/etl/legacy-scrapers-ca/` - Canadian scrapers
- `/legacy/services/etl/legacy-civic-scraper/` - Civic data
- `/legacy/services/api-gateway/` - API implementations
- `/legacy/services/web-ui/` - UI components

## 🎯 REMEMBER

- **NO DEVIATIONS** from documented specifications
- **ALWAYS CHECK LEGACY CODE** before implementing new
- **WRITE TESTS FOR EVERYTHING** - 80%+ coverage required
- **FOLLOW THE CHECKLIST** - Each item is numbered and documented
- **SUCCESS = COMPLETE IMPLEMENTATION** of documented requirements

**You have everything needed to succeed. Follow the documentation exactly.**
