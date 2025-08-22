# Legacy Documentation Migration Plan
Generated: 2025-01-19 | Iteration: 6/10

## 🎯 Migration Strategy

### Objectives
1. Create proper `/legacy` directory structure
2. Move legacy-specific documentation
3. Preserve reference materials
4. Maintain accessibility
5. Clean up main directories

## 📊 Current Documentation Analysis

### Documentation Categories

#### 1. Migration-Related Documents
These documents describe the migration process and should stay in main docs:
- `/docs/Open Parliament Migration Plan/*` - Active migration guides
- `/docs/validation/*` - Current validation reports
- `/docs/architecture.md` - Current architecture

#### 2. Legacy Reference Documents
These should move to legacy directory:
- Legacy API documentation
- Original system specifications
- Historical implementation notes
- Original repository READMEs

#### 3. Mixed Documents
These contain both legacy and current info - need splitting:
- Implementation summaries
- Integration reports
- Feature comparisons

## 📁 Proposed Legacy Directory Structure

```
/workspace/legacy/
├── README.md                          # Overview of legacy content
├── openparliament/
│   ├── docs/
│   │   ├── original-readme.md        # Original repo README
│   │   ├── django-architecture.md    # Django app structure
│   │   ├── api-v1-spec.md           # Original API spec
│   │   └── features.md              # Feature documentation
│   └── code/                        # Already exists in web-ui/src/legacy-migration
│
├── scrapers-ca/
│   ├── docs/
│   │   ├── scraper-guide.md         # How scrapers work
│   │   ├── municipality-list.md     # List of all municipalities
│   │   └── pupa-integration.md      # Pupa framework docs
│   └── code/                        # Already exists in etl/legacy-scrapers-ca
│
├── open-policy-infra/
│   ├── docs/
│   │   ├── deployment-legacy.md     # Original deployment
│   │   ├── infrastructure-v1.md     # Original infra design
│   │   └── docker-compose-v1.yml    # Original compose file
│   └── code/                        # Infrastructure files
│
├── admin-open-policy/
│   ├── docs/
│   │   ├── admin-features.md        # Original admin features
│   │   └── ui-components.md         # Component documentation
│   └── code/                        # React admin code
│
├── open-policy-app/
│   ├── docs/
│   │   ├── mobile-architecture.md   # React Native architecture
│   │   ├── features.md              # Mobile features
│   │   └── api-integration.md       # Mobile API usage
│   └── code/                        # React Native code (if preserved)
│
├── open-policy-web/
│   ├── docs/
│   │   ├── nextjs-setup.md          # Original Next.js setup
│   │   └── component-library.md     # UI components
│   └── code/                        # Next.js code
│
├── represent-canada/
│   ├── docs/
│   │   ├── api-documentation.md     # Represent API docs
│   │   ├── data-sources.md          # Data source info
│   │   └── boundary-system.md       # Boundary management
│   └── code/                        # Django Represent code
│
└── migration-artifacts/
    ├── feature-mappings/             # How features were migrated
    ├── code-comparisons/             # Before/after code examples
    └── decision-log/                 # Why certain choices were made
```

## 🔄 Migration Actions

### Step 1: Create Legacy Directory Structure
```bash
mkdir -p /workspace/legacy/{openparliament,scrapers-ca,open-policy-infra}/docs
mkdir -p /workspace/legacy/{admin-open-policy,open-policy-app,open-policy-web}/docs
mkdir -p /workspace/legacy/{represent-canada,migration-artifacts}/{docs,code}
mkdir -p /workspace/legacy/migration-artifacts/{feature-mappings,code-comparisons,decision-log}
```

### Step 2: Create Legacy README
```markdown
# Legacy Documentation and Code Reference

This directory contains historical documentation and code from the original repositories that were merged into the OpenPolicy Platform V2.

## Purpose
- Reference for understanding original implementations
- Historical context for decisions
- Code examples for migration
- Feature specifications from original systems

## Structure
Each subdirectory corresponds to an original repository with:
- `/docs` - Original documentation
- `/code` - Links or references to preserved code

## Usage
This is reference material only. Active development should use the main documentation.
```

### Step 3: Document Migration List

#### Documents to Create in Legacy
1. **Django Architecture Guide** 
   - Extract from legacy Django code
   - Document model relationships
   - Template system overview

2. **Original API Specifications**
   - REST endpoints from Django
   - Authentication methods
   - Response formats

3. **Feature Implementation Guides**
   - How each feature worked
   - Business logic documentation
   - User flows

4. **Infrastructure Documentation**
   - Original deployment process
   - Server configurations
   - Database schemas

5. **Scraper Documentation**
   - How each scraper works
   - Data extraction methods
   - Update schedules

### Step 4: Documents to Move

#### From Services to Legacy
1. Legacy integration reports → `/legacy/migration-artifacts/`
2. Original implementation notes → `/legacy/{repo}/docs/`
3. Deprecated configuration files → `/legacy/{repo}/docs/`

#### Documents to Keep in Place
1. Current architecture documents
2. Active migration plans
3. Validation reports
4. API specifications for current system
5. Deployment guides for current system

## 📋 Migration Checklist

### Immediate Actions
- [ ] Create `/workspace/legacy` directory structure
- [ ] Create main legacy README.md
- [ ] Create subdirectory README files
- [ ] Extract Django documentation from code
- [ ] Document original API endpoints

### Documentation Creation
- [ ] Write Django architecture guide
- [ ] Document original features
- [ ] Create scraper documentation
- [ ] Write infrastructure history
- [ ] Document migration decisions

### File Movement
- [ ] Move deprecated configs
- [ ] Archive old deployment scripts
- [ ] Move historical reports
- [ ] Organize reference materials

### Cleanup Actions
- [ ] Update references in main docs
- [ ] Remove duplicate information
- [ ] Update navigation/indexes
- [ ] Verify no broken links

## 🎯 Success Criteria

1. **Clear Separation**: Legacy vs current documentation clearly separated
2. **Accessibility**: Legacy docs easily findable when needed
3. **Completeness**: All historical context preserved
4. **Organization**: Logical structure matching original repos
5. **Maintenance**: Easy to add new legacy findings

## 📊 Impact Analysis

### Benefits
- Cleaner main documentation
- Preserved historical context
- Better organization
- Easier onboarding
- Clear migration path

### Risks
- Potential link breakage
- Temporary confusion during migration
- Need to update references

### Mitigation
- Create redirects for moved files
- Update all internal references
- Announce changes clearly
- Maintain migration log

---
End of Iteration 6/10