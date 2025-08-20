# OpenPolicy – Instructions for Cursor

## 🎯 **Current Focus: OpenParliament Integration First**

**Strategy**: Get OpenParliament fully working before adding other repositories. This gives us a solid foundation to build upon.

## Objectives
- Merge repos into a coherent monorepo.
- Provide a stable, versioned API for web, mobile, and admin.
- Build a robust ETL to ingest federal (OpenParliament), provincial/municipal (scrapers-ca), and external (Represent API) data.
- Maintain a crisp separation between legacy code and new services.

## Constraints
- PostgreSQL 15+ only.
- No breaking API changes without semver bump and migration notes.
- Keep /legacy read-only except for patches required to export data.
- **Focus on OpenParliament first** - other repos will be added incrementally.

## Definition of Done (per feature)
1. OpenAPI spec updated.
2. Endpoint implemented in FastAPI.
3. Unit + integration tests passing.
4. Database migration applied and reversible.
5. Docs updated (README, ADR if needed).

## 🚀 **Work Phases (OpenParliament-First)**

### **Phase 1: Foundation & OpenParliament (Week 1-2) ✅**
- [x] Project structure and configuration
- [x] Legacy code setup (reference only)
- [x] Database schema for OpenParliament
- [ ] OpenParliament data models and API endpoints
- [ ] Full testing and validation

### **Phase 2: OpenParliament ETL (Week 3)**
- [ ] Extract data from OpenParliament Django app
- [ ] Transform to canonical schema
- [ ] Load into PostgreSQL with full-text search
- [ ] Test with real OpenParliament data

### **Phase 3: API Development (Week 4)**
- [ ] Bills endpoints (list, detail, search)
- [ ] Members endpoints (list, detail)
- [ ] Votes endpoints (list, detail)
- [ ] Sessions endpoints (list, detail)

### **Phase 4: Gradual Expansion (Week 5-8)**
- [ ] Add provincial scrapers one by one
- [ ] Integrate Represent API
- [ ] Add remaining UI components
- [ ] End-to-end testing

## 🎯 **Immediate Tasks (OpenParliament Focus)**

### **Task 1: Legacy Code Setup** ✅
```bash
make legacy-setup    # Clone all repos to /legacy (reference only)
make openparliament-focus  # See current focus and next steps
```

### **Task 2: OpenParliament Database Integration**
- [ ] Review `legacy/openparliament/` structure
- [ ] Extract Django models and understand data relationships
- [ ] Implement SQLAlchemy models matching our schema
- [ ] Create Alembic migrations

### **Task 3: OpenParliament ETL Pipeline**
- [ ] Build extractor for OpenParliament data
- [ ] Create normalizer for bills, members, votes
- [ ] Implement loader with upsert semantics
- [ ] Test with sample OpenParliament data

### **Task 4: OpenParliament API Endpoints**
- [ ] Implement `/bills` endpoints with search
- [ ] Implement `/members` endpoints
- [ ] Implement `/votes` endpoints
- [ ] Add full-text search capabilities

## Coding Standards
- TS: strict; no `any`; use Zod for runtime validation.
- Python: type hints everywhere; pydantic for models; ruff/black pre-commit.
- SQL: all schema changes via Alembic migrations.

## Data Contracts
- External sources: Version and snapshot source datasets; keep hashes for provenance.
- ETL must log row counts, durations, and error summaries.

## 🎯 **Cursor Tasks (OpenParliament Focus)**

### **Current Priority: OpenParliament Integration**
1. **Review Legacy Code**: Analyze `legacy/openparliament/` structure
2. **Database Models**: Create SQLAlchemy models for bills, members, votes
3. **ETL Pipeline**: Build OpenParliament data extractor and normalizer
4. **API Endpoints**: Implement bills, members, votes endpoints
5. **Testing**: Full test coverage for OpenParliament functionality

### **Next Phase (After OpenParliament is Working)**
- Add provincial scrapers one by one
- Integrate Represent API for district data
- Expand to other repositories

> **Keep PRs under 400 lines; always include tests.**
> **Focus on OpenParliament first - get it fully working before expanding.**
