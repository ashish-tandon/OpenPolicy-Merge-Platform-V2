# IMPLEMENTATION INSTRUCTIONS FOR AGENT - OpenPolicy V2

## 🚨 CRITICAL: FOLLOW THESE INSTRUCTIONS EXACTLY

This document provides the detailed implementation guide for the OpenPolicy V2 platform. 
**DO NOT DEVIATE from these specifications. DO NOT ADD new features.**

## 📋 IMPLEMENTATION PHASES

### PHASE 1: CRITICAL BUG FIXES (Week 1)

#### BUG-001: Authentication System Implementation
**Priority**: P0 (Critical)
**Location**: `services/api-gateway/app/api/v1/auth.py`

**Steps**:
1. Navigate to `services/api-gateway/app/api/v1/`
2. Create `auth.py` file if it doesn't exist
3. Implement JWT-based authentication:
   ```python
   from fastapi import APIRouter, Depends, HTTPException, status
   from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
   from jose import JWTError, jwt
   from passlib.context import CryptContext
   from datetime import datetime, timedelta
   
   router = APIRouter()
   pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
   
   # JWT Configuration
   SECRET_KEY = "your-secret-key"  # Move to environment variables
   ALGORITHM = "HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   
   @router.post("/token")
   async def login(form_data: OAuth2PasswordRequestForm = Depends()):
       # Implement user authentication logic
       pass
   
   @router.get("/users/me")
   async def read_users_me(current_user = Depends(get_current_user)):
       return current_user
   ```

4. **DO NOT**: Add new authentication methods not in the spec
5. **DO**: Follow existing FastAPI patterns in the codebase
6. **Test**: Write unit tests for all endpoints

#### BUG-018: Database Backup System
**Priority**: P0 (Critical)
**Location**: `services/api-gateway/scripts/backup.py`

**Steps**:
1. Navigate to `services/api-gateway/scripts/`
2. Create `backup.py` script:
   ```python
   import subprocess
   import os
   from datetime import datetime
   
   def create_backup():
       timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
       backup_dir = f"/backups/{timestamp}"
       os.makedirs(backup_dir, exist_ok=True)
       
       # PostgreSQL backup
       subprocess.run([
           "pg_dump", 
           "-h", "localhost",
           "-U", "postgres",
           "-d", "openpolicy_v2",
           "-f", f"{backup_dir}/database.sql"
       ])
       
       # File backup
       subprocess.run(["tar", "-czf", f"{backup_dir}/files.tar.gz", "/data"])
   
   if __name__ == "__main__":
       create_backup()
   ```

3. **DO NOT**: Change database connection parameters
4. **DO**: Use existing database configuration
5. **Test**: Verify backup files are created successfully

### PHASE 2: CORE FEATURES IMPLEMENTATION (Weeks 2-4)

#### Feature F001: Global Search with Postal Code MP Lookup
**Priority**: P0
**Location**: `services/api-gateway/app/api/v1/search.py`

**Implementation Steps**:
1. **Check legacy code first**:
   ```bash
   cd /workspace/legacy
   find . -name "*search*" -type f
   find . -name "*postal*" -type f
   ```

2. **Create search endpoint**:
   ```python
   from fastapi import APIRouter, Query, HTTPException
   import requests
   
   router = APIRouter()
   
   @router.get("/search")
   async def global_search(q: str = Query(..., min_length=2)):
       # Implement search logic
       # Check legacy code for existing search implementations
       pass
   
   @router.get("/search/postcode/{postal_code}")
   async def search_by_postal_code(postal_code: str):
       # Validate postal code format (K1A0A6)
       if not re.match(r'^[A-Z]\d[A-Z]\d[A-Z]\d$', postal_code.upper()):
           raise HTTPException(status_code=400, detail="Invalid postal code format")
       
       # Call Represent Canada API
       response = requests.get(f"https://represent.opennorth.ca/postcodes/{postal_code}/")
       # Process response and map to internal models
       pass
   ```

3. **DO NOT**: Add new search algorithms not in the spec
4. **DO**: Reuse existing search logic from legacy code
5. **Test**: Write tests for valid/invalid postal codes

#### Feature F002: Complete MP Database with Individual Profiles
**Priority**: P0
**Location**: `services/api-gateway/app/api/v1/members.py`

**Implementation Steps**:
1. **Check existing models**:
   ```bash
   cd /workspace/services/api-gateway/app/models
   cat members.py
   ```

2. **Extend existing models** (don't replace):
   ```python
   # Add to existing models/members.py
   class MemberProfile(Base):
       __tablename__ = "member_profiles"
       
       id = Column(Integer, primary_key=True, index=True)
       member_id = Column(Integer, ForeignKey("members.id"))
       bio = Column(Text)
       photo_url = Column(String)
       social_media = Column(JSON)
       
       member = relationship("Member", back_populates="profile")
   ```

3. **DO NOT**: Create new database tables without checking existing schema
4. **DO**: Extend existing models and relationships
5. **Test**: Verify profile data is properly linked to members

### PHASE 3: SUPPORTING FEATURES (Weeks 5-8)

#### Feature F012: Scraper Monitoring Dashboard
**Priority**: P2
**Location**: `services/etl/app/monitoring/`

**Implementation Steps**:
1. **Check legacy scraper code**:
   ```bash
   cd /workspace/legacy
   find . -name "*scraper*" -type d
   ls -la services/etl/legacy-scrapers-ca/
   ```

2. **Create monitoring endpoints**:
   ```python
   from fastapi import APIRouter
   from app.models.data_sources import DataSource
   from app.models.ingestion_logs import IngestionLog
   
   router = APIRouter()
   
   @router.get("/data-sources")
   async def get_data_sources():
       # Return scraper status and health
       pass
   
   @router.get("/stats/system")
   async def get_system_stats():
       # Return system performance metrics
       pass
   ```

3. **DO NOT**: Implement new monitoring systems
4. **DO**: Use existing ETL pipeline monitoring
5. **Test**: Verify scraper status is accurately reported

## 🚫 WHAT NOT TO DO - CRITICAL RULES

### 1. NO NEW FEATURES
- **DO NOT** add features not documented in `FEATURE_MAPPING_UNIFIED.md`
- **DO NOT** create new API endpoints outside the specification
- **DO NOT** implement user-requested features not in the plan

### 2. NO API CHANGES
- **DO NOT** modify existing API contracts
- **DO NOT** change request/response schemas
- **DO NOT** add new query parameters not in the spec
- **DO NOT** change HTTP status codes

### 3. NO DATABASE SCHEMA CHANGES
- **DO NOT** create new tables without checking existing schema
- **DO NOT** modify existing table structures
- **DO NOT** change column names or types
- **DO NOT** add new indexes without validation

### 4. NO LEGACY CODE IGNORANCE
- **DO NOT** implement new solutions without checking `/legacy`
- **DO NOT** rewrite existing functionality
- **DO NOT** ignore documented legacy implementations
- **DO NOT** create duplicate code

### 5. NO TESTING SHORTCUTS
- **DO NOT** skip unit tests
- **DO NOT** skip integration tests
- **DO NOT** skip E2E tests for critical features
- **DO NOT** accept less than 80% coverage

## ✅ WHAT YOU MUST DO - IMPLEMENTATION RULES

### 1. ALWAYS CHECK LEGACY FIRST
```bash
# Before implementing ANY feature:
cd /workspace/legacy
find . -name "*feature_name*" -type f
find . -name "*similar_function*" -type f
```

### 2. FOLLOW EXISTING PATTERNS
- Use the same import structure
- Follow the same naming conventions
- Use the same error handling patterns
- Follow the same testing structure

### 3. EXTEND, DON'T REPLACE
- Add to existing models, don't replace them
- Extend existing endpoints, don't recreate them
- Use existing database connections
- Follow existing authentication patterns

### 4. WRITE COMPREHENSIVE TESTS
```python
# Example test structure:
def test_feature_name_success():
    # Test successful case
    pass

def test_feature_name_validation():
    # Test input validation
    pass

def test_feature_name_error_handling():
    # Test error cases
    pass

def test_feature_name_integration():
    # Test with database
    pass
```

## 🔧 IMPLEMENTATION TOOLS AND COMMANDS

### Development Environment Setup
```bash
# Start fresh shell from workspace root
cd /workspace

# Activate virtual environments
source services/api-gateway/venv/bin/activate
source services/etl/venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Testing Commands
```bash
# Run all tests
make test

# Run specific service tests
cd services/api-gateway && pytest
cd services/etl && pytest

# Check coverage
make coverage

# Run linting
make lint
```

### Validation Commands
```bash
# Documentation audit
make docs-audit

# Feature verification
make verify-features

# Health check
make health-check

# Database validation
make db-validate
```

## 📊 PROGRESS TRACKING

### Daily Progress Log
Create `IMPLEMENTATION_PROGRESS.md` in the root directory:

```markdown
# Implementation Progress Log

## Date: [Current Date]

### Completed Today:
- [ ] BUG-001: Authentication system - Status: In Progress
- [ ] Feature F001: Global Search - Status: Not Started

### Blockers:
- None currently

### Next Steps:
1. Complete BUG-001 authentication
2. Start Feature F001 implementation

### Notes:
- Following checklist item #1 from MASTER_EXECUTION_CHECKLIST.md
```

### Weekly Status Report
Update every Friday with:
- Features completed
- Bugs resolved
- Test coverage achieved
- Blockers encountered
- Next week's plan

## 🚨 EMERGENCY PROCEDURES

### If You Get Stuck:
1. **Check documentation first** - Solutions are documented
2. **Review legacy code** - Similar implementations exist
3. **Follow the checklist** - Each item has detailed steps
4. **Use validation tools** - `make docs-audit`, `make test`
5. **Continue with next item** - Don't get blocked

### If You Encounter Errors:
1. **Read error messages carefully** - They often contain solutions
2. **Check existing implementations** - Similar code may have solutions
3. **Review test files** - Tests show expected behavior
4. **Check database state** - Verify data integrity
5. **Document the problem** - Update progress log

## 🎯 SUCCESS METRICS

### Phase 1 Success (Week 1):
- ✅ BUG-001: Authentication system working
- ✅ BUG-018: Database backups automated
- ✅ All P0 bugs resolved
- ✅ 80%+ test coverage maintained

### Phase 2 Success (Weeks 2-4):
- ✅ All P0 features implemented
- ✅ Core API endpoints functional
- ✅ Basic UI components working
- ✅ Database models complete

### Final Success (Week 8):
- ✅ Platform fully functional
- ✅ All tests passing
- ✅ Documentation complete
- ✅ Ready for production deployment

## 📋 IMPLEMENTATION CHECKLIST

### Before Starting Each Feature:
- [ ] Read feature specification from `FEATURE_MAPPING_UNIFIED.md`
- [ ] Check legacy code for existing implementations
- [ ] Review checklist items from `MASTER_EXECUTION_CHECKLIST.md`
- [ ] Understand API contract from `API_DESIGN_SPECIFICATION.md`
- [ ] Plan test coverage requirements

### During Implementation:
- [ ] Follow existing code patterns exactly
- [ ] Extend existing models, don't replace
- [ ] Write tests for every function
- [ ] Update progress log
- [ ] Run validation tools

### After Completing Each Feature:
- [ ] Verify all tests pass
- [ ] Check test coverage meets requirements
- [ ] Update documentation
- [ ] Run `make docs-audit`
- [ ] Update progress tracking

## 🎯 REMEMBER

- **NO DEVIATIONS** from documented specifications
- **ALWAYS CHECK LEGACY CODE** before implementing new
- **WRITE TESTS FOR EVERYTHING** - 80%+ coverage required
- **FOLLOW THE CHECKLIST** - Each item is numbered and documented
- **SUCCESS = COMPLETE IMPLEMENTATION** of documented requirements

**You have everything needed to succeed. Follow the documentation exactly.**
