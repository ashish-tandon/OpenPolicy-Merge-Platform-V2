# Quick Reference Action Guide - OpenPolicy V2
Generated: 2025-01-19 | Final Loop: 2/3

## 🚨 CRITICAL FIXES (48 HOURS)

### 1. Fix Votes API ⏱️ 8 hours
```bash
cd /workspace/services/api-gateway
# Fix: app/schemas/votes.py - Pydantic v2 migration
# Uncomment: app/main.py line with votes import
# Test: pytest tests/test_votes.py
```

### 2. Complete Debates ⏱️ 16 hours
```bash
cd /workspace/services/api-gateway/app/api/v1
# Create: debates.py with all endpoints
# Models: app/models/debates.py
# Test: curl localhost:8080/api/v1/debates
```

### 3. Load Committees ⏱️ 4 hours
```sql
-- Run: Load all 26+ committees
INSERT INTO committees SELECT * FROM legacy.committees;
```

### 4. Postal Code Search ⏱️ 8 hours
```python
# Add to: app/api/v1/members.py
@router.get("/by-postal/{postal_code}")
async def find_mp_by_postal(postal_code: str):
    # Integrate Represent API
```

## 📊 QUICK STATUS

| System | Health | Coverage | Action |
|--------|--------|----------|--------|
| Bills API | 🟢 90% | Working | Polish |
| Members API | 🟢 85% | Working | Add postal |
| Votes API | 🔴 0% | BROKEN | Fix NOW |
| Debates | 🔴 20% | Partial | Complete |
| Committees | 🟡 8% | 2/26 | Load all |
| Search | 🟡 60% | No postal | Enhance |
| Tests | 🔴 15% | Critical | Add tests |
| Bilingual | 🔴 0% | Missing | Implement |

## 🎯 PRIORITY MATRIX

### P0 - Platform Broken (This Week)
- [ ] Votes API - Pydantic v2
- [ ] Debates - Complete implementation  
- [ ] Committees - Load missing 24
- [ ] Postal Search - MP lookup

### P1 - Core Features (Week 2-3)
- [ ] Email Alerts - User engagement
- [ ] Bilingual - Legal requirement
- [ ] Test Framework - Quality gates
- [ ] Error Handling - Consistency

### P2 - Enhancements (Month 2)
- [ ] WebSockets - Real-time
- [ ] RSS Feeds - Syndication
- [ ] Visualizations - Insights
- [ ] PWA - Mobile web

### P3 - Nice to Have (Month 3+)
- [ ] AI Summaries - Innovation
- [ ] Native Apps - Consider defer
- [ ] Haiku Generator - Fun feature
- [ ] Voice Interface - Accessibility

## 🛠️ TECH STACK CONFIRMED

```yaml
Backend:
  - Python 3.11 + FastAPI
  - PostgreSQL 16 + Redis 7
  - Elasticsearch 8
  - Docker → Kubernetes

Frontend:
  - Next.js 14 + React 18  
  - Tailwind CSS
  - TypeScript 5
  - PWA ready

Tools:
  - GitHub Actions CI/CD
  - Prometheus + Grafana
  - pytest + Playwright
  - Sentry error tracking
```

## 📁 KEY LOCATIONS

```bash
# API Gateway (Main API)
/workspace/services/api-gateway/

# User Service (Auth)
/workspace/services/user-service/

# Web UI (Next.js)
/workspace/services/web-ui/

# Admin UI (React)  
/workspace/services/admin-ui/

# ETL (Scrapers)
/workspace/services/etl/

# Legacy Code
/workspace/services/web-ui/src/legacy-migration/
```

## 🔧 COMMON COMMANDS

```bash
# Start everything
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api-gateway

# Run tests
pytest services/api-gateway/tests/

# Database access
docker-compose exec postgres psql -U postgres openparliament

# Redis CLI
docker-compose exec redis redis-cli
```

## 📈 SUCCESS METRICS

| Metric | Current | Week 1 | Month 1 | Target |
|--------|---------|--------|---------|--------|
| Features | 71% | 80% | 90% | 100% |
| Tests | 15% | 30% | 50% | 85% |
| API Coverage | 70% | 85% | 95% | 100% |
| Bilingual | 0% | 10% | 30% | 100% |
| Performance | ? | Baseline | <300ms | <200ms |

## 👥 TEAM ALLOCATION

```
Backend (2): Fix Votes + Debates
Frontend (2): Bilingual + PWA  
DevOps (1): CI/CD + Monitoring
QA (1): Test Framework

Week 1 Focus: P0 fixes only
Week 2: P1 features
Week 3+: Enhancement
```

## 🚦 GO/NO-GO CRITERIA

### Week 1 Checkpoint ✓
- [ ] Votes API working
- [ ] Debates complete
- [ ] All committees loaded
- [ ] Postal search working
- [ ] 30% test coverage

### Month 1 Launch Gate ✓
- [ ] All APIs functional
- [ ] 50% test coverage
- [ ] Performance <500ms
- [ ] Monitoring active
- [ ] Bilingual started

### Production Ready ✓
- [ ] 100% features
- [ ] 85% tests
- [ ] <200ms response
- [ ] Full bilingual
- [ ] Security audit

## 💡 QUICK WINS

1. **Fix Votes** - Unblocks major feature
2. **Load Committees** - Quick data fix
3. **Add Postal** - High user value
4. **Setup Monitoring** - Visibility
5. **Add Health Checks** - Reliability

## ⚠️ AVOID THESE

1. **Feature Creep** - Stick to roadmap
2. **Test Skipping** - Quality first
3. **Over-Engineering** - Simple solutions
4. **Scope Changes** - Stay focused
5. **Tech Debt** - Fix as you go

## 📞 ESCALATION

**Technical**: Team Lead → Architect → CTO
**Resource**: PM → Director → Sponsor
**Blockers**: Daily standup → Emergency meet

## 🔗 REFERENCE DOCS

1. `/docs/validation/EXECUTIVE_IMPLEMENTATION_GUIDE.md` - Full plan
2. `/docs/validation/CODE_DEVIATIONS_ANALYSIS.md` - Tech gaps
3. `/docs/validation/PRIORITY_ANALYSIS_AND_RECOMMENDATIONS.md` - Priorities
4. `/docs/validation/API_DESIGN_SPECIFICATION.md` - API specs
5. `/docs/validation/COMPREHENSIVE_TESTING_STRATEGIES.md` - Test plan

---
**ONE PAGE TO RULE THEM ALL** - Print and pin this guide!

End of Loop 2/3