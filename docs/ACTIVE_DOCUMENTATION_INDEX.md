# Active Documentation Index
**Updated**: 2025-01-10  
**Purpose**: Central index for all active documentation  
**Status**: Current

## 📚 Documentation Structure

### 🎯 Master Planning Documents
- [MASTER_PLANNING_FRAMEWORK.md](MASTER_PLANNING_FRAMEWORK.md) - Overall planning framework and iteration tracking

### 📋 Current Audits & Analyses
- [CODE_DEVIATION_AUDIT.md](CODE_DEVIATION_AUDIT.md) - Code quality and deviation analysis
- [COMPREHENSIVE_TESTING_VERIFICATION_STRATEGY.md](COMPREHENSIVE_TESTING_VERIFICATION_STRATEGY.md) - Testing strategies
- [FEATURE_PRIORITY_ANALYSIS.md](FEATURE_PRIORITY_ANALYSIS.md) - Feature prioritization matrix

### 🏗️ Architecture & Design
- [SYSTEM_ARCHITECTURE_DESIGN.md](SYSTEM_ARCHITECTURE_DESIGN.md) - Target system architecture
- [architecture.md](architecture.md) - Quick architecture overview
- [ADR/0001-use-fastapi-and-postgres.md](ADR/0001-use-fastapi-and-postgres.md) - Architecture decisions

### 📊 Data Management
- [DATA_MAP.md](DATA_MAP.md) - Comprehensive data mapping and lineage
- [DATA_LINEAGE_TECHNICAL_IMPLEMENTATION.md](DATA_LINEAGE_TECHNICAL_IMPLEMENTATION.md) - Technical implementation guide
- [DATA_LINEAGE_DOCUMENTATION_SUMMARY.md](DATA_LINEAGE_DOCUMENTATION_SUMMARY.md) - Documentation summary
- [DATA_GOVERNANCE_FRAMEWORK.md](DATA_GOVERNANCE_FRAMEWORK.md) - Data governance policies
- [validation/DATA_DIFF_REPORT.md](validation/DATA_DIFF_REPORT.md) - Schema differences report
- [validation/DATA_LINEAGE_VALIDATION_SUMMARY.md](validation/DATA_LINEAGE_VALIDATION_SUMMARY.md) - Validation results

### 🚀 Implementation Guides
- [PERFORMANCE_OPTIMIZATION_GUIDE.md](PERFORMANCE_OPTIMIZATION_GUIDE.md) - Performance optimization strategies
- [DEPLOYMENT_AND_OPERATIONS_GUIDE.md](DEPLOYMENT_AND_OPERATIONS_GUIDE.md) - Deployment procedures
- [PROJECT_SETUP_AND_DEPLOYMENT_GUIDE.md](PROJECT_SETUP_AND_DEPLOYMENT_GUIDE.md) - Project setup instructions

### 🔒 Security & Compliance
- [SECURITY_AUDIT_AND_COMPLIANCE.md](SECURITY_AUDIT_AND_COMPLIANCE.md) - Security audit findings

### 📝 Project Management
- [instructions.md](instructions.md) - Task instructions
- [README.md](README.md) - Documentation overview
- [QUICK_START_SUMMARY.md](QUICK_START_SUMMARY.md) - Quick start guide

### 🔍 Reference Documentation
- [REFERENCE/omitted.md](REFERENCE/omitted.md) - Deprecated code tracking
- [SCRAPER_MAPPING.md](SCRAPER_MAPPING.md) - Scraper inventory
- [COMPLETE_SCRAPER_INVENTORY.md](COMPLETE_SCRAPER_INVENTORY.md) - Detailed scraper listing

### 📂 Legacy Documentation
- [legacy/LEGACY_DOCUMENTATION_INVENTORY.md](legacy/LEGACY_DOCUMENTATION_INVENTORY.md) - Index of moved legacy docs
- All historical implementation summaries, migration plans, and superseded documentation have been moved to `/docs/legacy/`

## 🗂️ Documentation Categories

### Active Development
Documents actively used for ongoing development:
- Planning frameworks
- Current audits
- Implementation guides
- Architecture designs

### Reference
Stable documentation for reference:
- Data mappings
- API documentation
- Scraper inventories

### Validation
Completed validation reports:
- Data lineage validation
- Schema difference reports

### Legacy
Historical documentation moved to `/docs/legacy/`:
- Implementation summaries
- Migration plans
- Superseded tracking documents

## 📋 Documentation Guidelines

### Naming Conventions
- **Active**: Use descriptive names without version numbers
- **Reference**: Prefix with `REF_` when stable
- **Legacy**: Move to legacy folder when superseded

### Update Frequency
- **Daily**: Task tracking, TODO lists
- **Weekly**: Progress summaries, audit updates
- **As Needed**: Architecture, guides, references

### Documentation Lifecycle
1. **Draft** → Active development
2. **Active** → In use for current work
3. **Reference** → Stable, occasional updates
4. **Legacy** → Historical record only