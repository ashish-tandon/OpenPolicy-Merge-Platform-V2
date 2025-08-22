# AGENT IMPLEMENTATION PROMPT - OpenPolicy V2

## 🚨 CRITICAL: READ THIS FIRST
You are tasked with implementing the OpenPolicy V2 platform. 

**DO NOT DEVIATE FROM THESE INSTRUCTIONS.**
**DO NOT ADD NEW FEATURES.**
**DO NOT CHANGE API SPECIFICATIONS.**

## 📋 YOUR MISSION
Implement OpenPolicy V2 exactly as specified in the documentation, following the established architecture and feature specifications.

## 🎯 IMPLEMENTATION PRIORITIES

### PHASE 1: CRITICAL BUG FIXES (P0)
1. **BUG-001: Authentication System** - Implement user authentication (P0)
2. **BUG-018: Database Backups** - Implement automated backup system (P0)
3. **BUG-002: OAuth Integration** - Complete Google OAuth backend connection (P1)
4. **BUG-003: Rate Limiting** - Implement API rate limiting (P1)

### PHASE 2: CORE FEATURES (P0-P1)
Follow the exact order in `docs/plan/features/FEATURE_MAPPING_UNIFIED.md`:
- F001: Global Search with Postal Code MP Lookup (P0)
- F002: Complete MP Database with Individual Profiles (P0)
- F003: Complete Bills Database with Status Tracking (P0)
- F004: Complete Voting Records with MP Positions (P0)
- F007: Multi-Level Government Database (P0)
- F008: User Authentication and Profile Management (P0)

### PHASE 3: SUPPORTING FEATURES (P1-P2)
Continue with remaining features in priority order.

## 📚 REQUIRED DOCUMENTS TO READ

### 1. Implementation Guide
- `docs/validation/MASTER_EXECUTION_CHECKLIST.md` - 93+ checklist items with IDs
- `docs/validation/EXECUTIVE_IMPLEMENTATION_GUIDE.md` - Step-by-step implementation

### 2. Feature Specifications
- `docs/plan/features/FEATURE_MAPPING_UNIFIED.md` - 50+ feature specifications
- `docs/validation/API_DESIGN_SPECIFICATION.md` - API contract definitions

### 3. Bug Status
- `docs/bugs/BUGS_RECONCILIATION.md` - 20+ prioritized bugs with repro steps

### 4. Architecture & Testing
- `docs/validation/COMPREHENSIVE_TESTING_STRATEGIES.md` - Testing requirements
- `docs/OPENPOLICY_V2_ARCHITECTURE_OVERVIEW.md` - System architecture

## 🚫 STRICT RULES - NO DEVIATIONS

### What You MUST Do:
1. **Follow checklist items exactly** - Use the sequential numbering system
2. **Implement features as specified** - No modifications to requirements
3. **Write tests for everything** - 80%+ code coverage required
4. **Reuse legacy code** - Check `/legacy` directory first before implementing new
5. **Follow established patterns** - Use existing code structure and conventions

### What You MUST NOT Do:
1. **Add new features** - Only implement what's documented
2. **Change API contracts** - Follow existing OpenAPI specifications
3. **Skip testing** - Every feature needs unit, integration, and e2e tests
4. **Ignore legacy code** - Always check `/legacy` first for existing implementations
5. **Modify database schemas** - Use existing models and migrations

## 🧪 TESTING REQUIREMENTS

### Coverage Targets:
- **Statement Coverage**: 85%+ for API gateway and ETL services
- **Branch Coverage**: 95%+ for critical modules (parsers, normalizers)
- **Test Types**: Unit, Integration, E2E, Contract tests

### Test Commands:
```bash
# Run all tests
make test

# Run specific service tests
cd services/api-gateway && pytest
cd services/etl && pytest

# Check coverage
make coverage
```

## 📊 PROGRESS TRACKING

### Daily Workflow:
1. **Morning**: Read relevant documentation sections
2. **Implementation**: Follow checklist items sequentially
3. **Testing**: Write and run tests for each feature
4. **Documentation**: Update progress in implementation notes
5. **Validation**: Run `make docs-audit` to check compliance

### Success Metrics:
- ✅ All P0 bugs fixed
- ✅ All P0 features implemented
- ✅ 80%+ test coverage achieved
- ✅ All checklist items completed
- ✅ Platform passes health checks

## 🔧 IMPLEMENTATION TOOLS

### Available Commands:
```bash
# Documentation audit
make docs-audit

# Run all tests
make test

# Feature verification
make verify-features

# Health check
make health-check
```

### Development Environment:
- **API Gateway**: FastAPI + PostgreSQL
- **ETL Pipeline**: Python + Celery
- **Frontend**: React + TypeScript
- **Database**: PostgreSQL with Alembic migrations

## 📝 IMPLEMENTATION PROCESS

### For Each Feature:
1. **Read specification** from `FEATURE_MAPPING_UNIFIED.md`
2. **Check legacy code** in `/legacy` directory first
3. **Follow checklist items** from `MASTER_EXECUTION_CHECKLIST.md`
4. **Implement API endpoints** following existing patterns
5. **Write comprehensive tests** (unit, integration, e2e)
6. **Update documentation** with implementation notes
7. **Run validation** with `make docs-audit`

### For Each Bug Fix:
1. **Read bug details** from `BUGS_RECONCILIATION.md`
2. **Identify root cause** and affected components
3. **Implement fix** following established patterns
4. **Write regression tests** to prevent recurrence
5. **Verify fix** with original repro steps
6. **Update bug status** in documentation

## 🎯 SUCCESS CRITERIA

### Phase 1 Complete:
- ✅ All P0 bugs resolved
- ✅ Authentication system working
- ✅ Database backups automated

### Phase 2 Complete:
- ✅ All P0 features implemented
- ✅ Core API endpoints functional
- ✅ Basic UI components working

### Final Success:
- ✅ Platform fully functional
- ✅ All tests passing
- ✅ Documentation complete
- ✅ Ready for production deployment

## 🚨 EMERGENCY PROCEDURES

### If You Encounter Issues:
1. **Check documentation first** - Solutions are documented
2. **Review legacy code** - Similar implementations may exist
3. **Follow established patterns** - Don't reinvent solutions
4. **Document problems** - Update implementation notes
5. **Continue with next item** - Don't get blocked

### If You Need Help:
1. **Review relevant documentation** sections
2. **Check existing implementations** in similar features
3. **Follow the checklist** - Each item has detailed steps
4. **Use validation tools** - `make docs-audit`, `make test`

## 📋 START HERE

1. **Read this document completely** - Understand your mission
2. **Read the implementation guide** - `docs/validation/EXECUTIVE_IMPLEMENTATION_GUIDE.md`
3. **Review the checklist** - `docs/validation/MASTER_EXECUTION_CHECKLIST.md`
4. **Start with P0 bugs** - Begin with BUG-001 (Authentication)
5. **Follow the process** - Implement features sequentially
6. **Track progress** - Update documentation as you go

## 🎯 REMEMBER

- **NO DEVIATIONS** from documented specifications
- **ALWAYS CHECK LEGACY CODE** before implementing new
- **WRITE TESTS FOR EVERYTHING** - 80%+ coverage required
- **FOLLOW THE CHECKLIST** - Each item is numbered and documented
- **SUCCESS = COMPLETE IMPLEMENTATION** of documented requirements

**You have everything needed to succeed. Follow the documentation exactly.**
