# Environment, Bug, and Data Audit Report

Generated: 2025-08-23T18:27:42.347156

## Environment Scan

### Services Status

| Service | Status | Type | Ports |
|---------|--------|------|-------|

**Total Services**: 0
**Running**: 0
**Stopped**: 0

### Listening Ports


## Bug Inventory (Deduplicated)

**Total Unique Bugs**: 57

### Bugs by Type

#### security (57 bugs)

- **Bug #?**: Possible binding to all interfaces....
  - File: `./services/api-gateway/app/config.py`
  - Checklist: CHK-0061
- **Bug #?**: Using xml.etree.ElementTree to parse untrusted XML data is known to be vulnerabl...
  - File: `./services/api-gateway/src/api/v1/export.py`
  - Checklist: CHK-0061
- **Bug #?**: Using xml.dom.minidom.parseString to parse untrusted XML data is known to be vul...
  - File: `./services/api-gateway/src/api/v1/export.py`
  - Checklist: CHK-0061
- **Bug #?**: Use of assert detected. The enclosed code will be removed when compiling to opti...
  - File: `./services/api-gateway/tests/test_bills.py`
  - Checklist: CHK-0061
- **Bug #?**: Use of possibly insecure function - consider using safer ast.literal_eval....
  - File: `./services/api-gateway/venv/lib/python3.12/site-packages/_pytest/_code/code.py`
  - Checklist: CHK-0061
- ...and 52 more

## Data Points Traced

**Total Data Points**: 45

### Data Points by Type

#### Data_Entity (45 points)

| Entity | ID | Ingestion | API | UI |
|--------|----|-----------|----|----|
| members | DATA-001 | - | - | - |
| bills | DATA-002 | - | - | - |
| debates | DATA-003 | - | - | - |
| votes | DATA-004 | - | - | - |
| jurisdictions | DATA-005 | - | - | - |
| jurisdictions | DATA-005 | - | - | - |
| postal_codes | DATA-006 | - | - | - |
| elected_members | DATA-007 | - | - | - |
| representatives | DATA-008 | - | - | - |
| offices | DATA-009 | - | - | - |

*...and 35 more*

## Health Check Summary

| Metric | Value | Status |
|--------|-------|--------|
| Service Health | 0% | 🔴 Poor |
| Bug Severity | 100% | 🔴 High |
| Data Coverage | 90% | 🟢 Good |
| **Overall Health** | **30%** | **🔴 Critical** |

## Recommendations

1. **Service Health**: Several services are not running. Check Docker/systemd configurations.
2. **Critical Bugs**: Address syntax errors and import issues first (see checklist items).

## Bug to Checklist Mapping

All bugs have been mapped to implementation checklist items:

| Checklist ID | Bug Count | Description |
|--------------|-----------|-------------|
| CHK-0061 | 57 | Implement security best practices |
