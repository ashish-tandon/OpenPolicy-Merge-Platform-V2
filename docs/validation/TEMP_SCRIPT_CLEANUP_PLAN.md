# Temporary Script Cleanup Plan
Generated: 2025-01-19 | Iteration: 7/10

## 🎯 Cleanup Objectives

1. Identify all temporary scripts and files
2. Categorize: Keep, Move, or Delete
3. Archive useful scripts
4. Remove truly temporary files
5. Update documentation

## 📊 File Analysis

### Root Directory Temporary Files

#### Files to Move to `/legacy/migration-artifacts/`
```bash
# Test scripts from migration
/workspace/test_integration.py
/workspace/test_integration.sh
/workspace/test-mcp-connection.sh
```
**Reason**: Historical migration testing artifacts

#### Files to Review from Git Status
```bash
# Untracked files (need review)
/workspace/BUG_DETECTION_SUMMARY.md
/workspace/api_gateway_safety.json
/workspace/bandit_report.json
/workspace/comprehensive_bug_report.txt
/workspace/etl_safety.json
/workspace/flake8_report.txt
/workspace/requirements-mcp.txt
/workspace/run_bugbot.sh
/workspace/safety_report.json
/workspace/test-mcp-simple.py
```
**Action**: Move security reports to `/docs/security/`

### Service-Level Temporary Files

#### ETL Service Test Files
```bash
/workspace/services/etl/test_multi_level_government.py
/workspace/services/etl/test_comprehensive_integration.py
/workspace/services/etl/test_municipal_ingestion.py
/workspace/services/etl/test_csv_ingestion.py
```
**Action**: Move to proper test directory structure

#### Legacy Test Files (Keep)
```bash
/workspace/services/etl/legacy-civic-scraper/tests/*
```
**Reason**: Part of preserved legacy code

### Scripts Directory
```bash
/workspace/scripts/test_openparliament.sh
```
**Action**: Move to `/workspace/tests/scripts/`

## 🗂️ Categorization

### 1. DELETE - True Temporary Files
```bash
# Empty or placeholder files
find /workspace -size 0 -name "*.tmp" -o -name "*.bak"

# Old log files
find /workspace -name "*.log" -mtime +7

# Python cache
find /workspace -name "__pycache__" -type d
find /workspace -name "*.pyc"

# Editor temporary files
find /workspace -name ".*.swp" -o -name "*~"
```

### 2. MOVE - Migration Artifacts
```bash
# To /legacy/migration-artifacts/test-scripts/
- test_integration.py
- test_integration.sh  
- test-mcp-connection.sh

# To /legacy/migration-artifacts/security-reports/
- api_gateway_safety.json
- bandit_report.json
- comprehensive_bug_report.txt
- etl_safety.json
- flake8_report.txt
- safety_report.json
- BUG_DETECTION_SUMMARY.md
```

### 3. ORGANIZE - Misplaced Test Files
```bash
# Create proper test structure
mkdir -p /workspace/tests/{unit,integration,e2e,scripts}

# Move ETL tests
mv /workspace/services/etl/test_*.py /workspace/tests/integration/etl/

# Move script tests
mv /workspace/scripts/test_*.sh /workspace/tests/scripts/
```

### 4. KEEP - Required Files
```bash
# Configuration templates
*.example
*.template

# Documentation
*.md (in proper locations)

# Setup scripts
setup.sh
deploy-platform.sh

# Development scripts
scripts/clone_all.sh
scripts/subtree_import.sh
```

## 📋 Cleanup Commands

### Phase 1: Create Archive Directories
```bash
# Create archive structure
mkdir -p /workspace/legacy/migration-artifacts/{test-scripts,security-reports,temp-configs}
mkdir -p /workspace/tests/{unit,integration,e2e,scripts}
mkdir -p /workspace/docs/security
```

### Phase 2: Move Files
```bash
# Move test scripts to legacy
mv /workspace/test_integration.* /workspace/legacy/migration-artifacts/test-scripts/
mv /workspace/test-mcp-*.* /workspace/legacy/migration-artifacts/test-scripts/

# Move security reports
mv /workspace/*_report.json /workspace/legacy/migration-artifacts/security-reports/
mv /workspace/*_report.txt /workspace/legacy/migration-artifacts/security-reports/
mv /workspace/BUG_DETECTION_SUMMARY.md /workspace/legacy/migration-artifacts/security-reports/

# Move ETL tests to proper location
mkdir -p /workspace/tests/integration/etl
mv /workspace/services/etl/test_*.py /workspace/tests/integration/etl/

# Move script tests
mv /workspace/scripts/test_*.sh /workspace/tests/scripts/
```

### Phase 3: Clean Temporary Files
```bash
# Remove Python cache
find /workspace -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find /workspace -name "*.pyc" -delete

# Remove editor temp files
find /workspace -name ".*.swp" -delete
find /workspace -name "*~" -delete

# Remove empty temp files
find /workspace -name "*.tmp" -size 0 -delete
find /workspace -name "*.bak" -delete

# Clean node_modules (if needed)
# find /workspace -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null
```

### Phase 4: Update References
```bash
# Update any scripts that reference moved files
grep -r "test_integration" /workspace/scripts/
grep -r "test-mcp" /workspace/

# Update documentation
# Add notes about moved files in relevant docs
```

## 🔍 Special Cases

### MCP-Related Files
```bash
requirements-mcp.txt  # Keep if MCP is still used
test-mcp-simple.py    # Archive to legacy
run_bugbot.sh         # Archive if one-time use
```

### Modified But Untracked
```bash
.cursor/mcp.json      # Keep, active configuration
docker-compose.yml    # Keep, active configuration
nginx.conf files      # Keep, active configuration
```

## 📊 Impact Assessment

### Before Cleanup
- Temporary files scattered in root
- Test files in wrong locations
- Security reports mixed with code
- No clear organization

### After Cleanup
- Clean root directory
- Organized test structure
- Archived migration artifacts
- Clear separation of concerns

## ✅ Verification Checklist

### Pre-Cleanup
- [ ] Backup important files
- [ ] Document file locations
- [ ] Check for hardcoded paths
- [ ] Verify no active dependencies

### During Cleanup
- [ ] Move files in phases
- [ ] Test after each phase
- [ ] Update references
- [ ] Maintain audit trail

### Post-Cleanup
- [ ] Verify builds still work
- [ ] Check all scripts run
- [ ] Update documentation
- [ ] Commit changes

## 🚫 Do NOT Delete

1. **Any file in .gitignore** - Check first
2. **Config files** - Even if temporary-looking
3. **Legacy test files** - Part of preserved code
4. **Migration logs** - Historical record
5. **Security reports** - Archive instead

## 📝 Documentation Updates

### Files to Update
1. `/README.md` - Note cleaned structure
2. `/docs/PROJECT_STRUCTURE.md` - Update paths
3. `/legacy/README.md` - Document archives
4. `/.gitignore` - Add new patterns

### New Documentation
1. `/tests/README.md` - Test organization
2. `/legacy/migration-artifacts/README.md` - Archive guide

## 🎯 Success Metrics

1. **Root directory**: Only essential files
2. **Test organization**: Clear structure
3. **Legacy artifacts**: Properly archived
4. **No broken references**: All paths updated
5. **Clean git status**: Organized changes

---
End of Iteration 7/10