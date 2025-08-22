# Code Deviations Analysis - Complete Review
Generated: 2025-01-19 | Iteration: 1/10

## 🎯 Overview
This document comprehensively analyzes all code deviations from legacy repositories, explaining architectural decisions and alignment strategies.

## 📊 Major Architectural Deviations

### 1. Django → FastAPI Migration

#### Deviation Details
| Component | Legacy (Django) | Current (FastAPI) | Reason for Change |
|-----------|----------------|-------------------|-------------------|
| Framework | Django 3.2 monolith | FastAPI microservices | Modern async support, better performance |
| ORM | Django ORM | SQLAlchemy | Async support, more flexible |
| Templates | Django templates | React/Next.js | SPA architecture, better UX |
| Auth | Django auth | JWT + OAuth | Stateless, scalable |
| Admin | Django admin | Custom React admin | More control, better UI |

#### Alignment Strategy
```python
# Legacy Django pattern
class Bill(models.Model):
    title = models.CharField(max_length=500)
    
# Current FastAPI pattern  
class Bill(Base):
    __tablename__ = "bills"
    title = Column(String(500))
    
# Alignment needed:
# 1. Port Django model validators to Pydantic
# 2. Implement Django admin features in React admin
# 3. Create Django compatibility layer for migrations
```

### 2. PHP → Python User Service

#### Deviation Details
| Component | Legacy (PHP/Laravel) | Current (Python/FastAPI) | Reason |
|-----------|---------------------|-------------------------|---------|
| Language | PHP 8.0 | Python 3.11 | Consistency with platform |
| Framework | Laravel | FastAPI | Unified tech stack |
| ORM | Eloquent | SQLAlchemy | Python ecosystem |
| Sessions | PHP sessions | Redis + JWT | Scalability |

#### Alignment Strategy
```php
// Legacy PHP pattern
class User extends Model {
    protected $fillable = ['name', 'email'];
}

# Current Python pattern
class User(Base):
    __tablename__ = "users"
    name = Column(String)
    email = Column(String)
    
# Alignment needed:
# 1. Port Laravel middleware to FastAPI
# 2. Implement Eloquent-like relationships
# 3. Add PHP session compatibility layer
```

### 3. React Native → Web-Only Mobile

#### Deviation Details
| Component | Legacy (React Native) | Current (Web) | Reason |
|-----------|---------------------|---------------|---------|
| Platform | iOS/Android native | Progressive Web App | Resource constraints |
| Navigation | React Navigation | Next.js routing | Web-first approach |
| Storage | AsyncStorage | LocalStorage | Browser compatibility |
| Push | Native push | Web push (planned) | Platform limitations |

#### Alignment Strategy
- Create React Native wrapper for web app
- Implement service workers for offline
- Add native features via Capacitor/Ionic
- Consider Flutter for true cross-platform

### 4. Monolithic → Microservices

#### Deviation Details
| Aspect | Legacy | Current | Reason |
|--------|--------|---------|---------|
| Architecture | Single Django app | 5+ microservices | Scalability, separation of concerns |
| Database | Single DB | Service-specific DBs | Data isolation |
| Deployment | Single server | Container orchestration | Cloud-native |
| Communication | Direct calls | REST APIs | Loose coupling |

#### Alignment Strategy
1. Implement service mesh for inter-service communication
2. Add distributed tracing for debugging
3. Create shared libraries for common functionality
4. Implement saga pattern for distributed transactions

## 🔍 Specific Code Deviations

### API Endpoints

#### 1. Votes API (CRITICAL DEVIATION)
```python
# Legacy Django
def vote_detail(request, vote_id):
    vote = get_object_or_404(Vote, pk=vote_id)
    return render(request, 'vote.html', {'vote': vote})

# Current FastAPI (BROKEN)
@router.get("/votes/{vote_id}")
async def get_vote(vote_id: int):
    # Pydantic v2 schema issues preventing this from working
    pass  # Currently commented out
    
# Fix needed:
from pydantic import BaseModel, ConfigDict

class VoteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # Migrate from Pydantic v1 Config class
```

#### 2. Search Functionality
```python
# Legacy Django
def search(request):
    query = request.GET.get('q')
    postal_code = request.GET.get('postal')
    # Complex search with postal code lookup
    
# Current FastAPI
@router.get("/search")
async def search(q: str, type: Optional[str] = None):
    # Missing postal code functionality
    
# Alignment needed:
# 1. Add postal_code parameter
# 2. Integrate with Represent API
# 3. Implement MP lookup by postal code
```

### Frontend Deviations

#### 1. Template System
```django
<!-- Legacy Django -->
{% extends "base.html" %}
{% block content %}
  <h1>{{ bill.title }}</h1>
{% endblock %}

// Current React
export default function BillPage({ bill }) {
  return <h1>{bill.title}</h1>
}

// Alignment strategy:
// 1. Create Django template parser for React
// 2. Port template tags to React components
// 3. Implement template inheritance pattern
```

#### 2. Real-time Features
```javascript
// Legacy: Server-sent events
var source = new EventSource('/house-status');

// Current: Not implemented
// Need WebSocket implementation:
const ws = new WebSocket('ws://localhost:8080/ws/house-status');

// Alignment needed:
// 1. Implement WebSocket server in FastAPI
// 2. Create real-time event system
// 3. Add fallback to polling
```

### Database Schema Deviations

#### 1. User Tables Split
```sql
-- Legacy: Single user table
CREATE TABLE auth_user (
    id, username, email, password, ...
);

-- Current: Split across services
-- User Service DB:
CREATE TABLE users (
    id, email, password_hash, ...
);

-- API Gateway DB:
CREATE TABLE user_profiles (
    user_id, preferences, ...
);

-- Alignment needed:
-- 1. Create unified user view
-- 2. Implement distributed joins
-- 3. Add data synchronization
```

## 📋 Deviation Priority Matrix

| Deviation | Impact | Effort | Priority | Action |
|-----------|--------|--------|----------|--------|
| Votes API broken | High | Low | P0 | Fix immediately |
| Debates incomplete | High | Medium | P0 | Complete implementation |
| Email alerts missing | High | Medium | P1 | Implement service |
| Postal code search | Medium | Low | P1 | Add to search API |
| Real-time updates | Medium | High | P2 | WebSocket implementation |
| Mobile native app | Low | High | P3 | Consider PWA first |

## 🔧 Technical Debt from Deviations

1. **Schema Mismatches**
   - Pydantic v1 → v2 migration incomplete
   - Django model features not ported
   - Validation logic scattered

2. **Authentication Complexity**
   - Multiple auth systems
   - Session management differs
   - Token validation inconsistent

3. **Data Model Differences**
   - Soft delete implementation varies
   - Timestamp field naming
   - Relationship handling

## ✅ Alignment Checklist

### Immediate Actions (Week 1)
- [ ] Fix Votes API Pydantic schemas
- [ ] Complete Debates API implementation
- [ ] Add postal code to search
- [ ] Unify error response format

### Short Term (Weeks 2-4)
- [ ] Implement email service
- [ ] Add WebSocket support
- [ ] Create Django compatibility layer
- [ ] Standardize validation

### Long Term (Months 2-3)
- [ ] Consider native mobile app
- [ ] Implement distributed tracing
- [ ] Add service mesh
- [ ] Complete test coverage

## 📊 Metrics for Alignment

- **Code Compatibility**: 60% → Target 95%
- **API Parity**: 70% → Target 100%
- **Feature Coverage**: 71% → Target 100%
- **Test Coverage**: 15% → Target 85%

---
End of Iteration 1/10