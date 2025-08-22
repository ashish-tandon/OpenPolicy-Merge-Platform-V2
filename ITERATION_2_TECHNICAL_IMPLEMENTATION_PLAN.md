# 🔧 ITERATION 2: TECHNICAL IMPLEMENTATION PLANNING
## Merge V2: Detailed Architecture & Implementation Specifications

**Date:** August 21, 2025  
**Iteration:** 2 of 10  
**Status:** 🔄 IN PROGRESS  
**Duration:** 1-2 weeks  
**Scope:** Detailed technical architecture and implementation planning  

---

## 🎯 ITERATION 2 OBJECTIVES

### **Primary Goals**
1. **API Design Specification** - Complete API endpoint definitions
2. **Database Schema Design** - Unified data model implementation
3. **ETL Pipeline Design** - Legacy system integration architecture
4. **Development Environment Setup** - Docker, CI/CD, testing infrastructure

### **Success Criteria**
- Complete API specification with OpenAPI documentation
- Database schema with migrations and indexes
- ETL pipeline architecture with connector specifications
- Working development environment with automated testing

---

## 🏗️ API DESIGN SPECIFICATION

### **Core API Structure**
```
/api/v1/
├── /auth/           # Authentication & authorization
├── /parliamentary/  # MPs, bills, votes, debates
├── /municipal/      # Municipal government data
├── /analytics/      # Data insights & reporting
├── /admin/          # Administrative functions
└── /health/         # System health checks
```

### **Key Endpoints Design**
```python
# Parliamentary Endpoints
GET    /api/v1/parliamentary/mp/{mp_id}
GET    /api/v1/parliamentary/mp/search?q={query}
POST   /api/v1/parliamentary/mp
PUT    /api/v1/parliamentary/mp/{mp_id}
DELETE /api/v1/parliamentary/mp/{mp_id}

GET    /api/v1/parliamentary/bill/{bill_id}
GET    /api/v1/parliamentary/bill/search?q={query}
GET    /api/v1/parliamentary/bill/{bill_id}/votes

GET    /api/v1/parliamentary/vote/{vote_id}
GET    /api/v1/parliamentary/vote/search?bill_id={bill_id}

# Municipal Endpoints
GET    /api/v1/municipal/jurisdiction/{jurisdiction_id}
GET    /api/v1/municipal/jurisdiction/search?q={query}
GET    /api/v1/municipal/data/{data_type}?jurisdiction_id={id}
```

---

## 🗄️ DATABASE SCHEMA DESIGN

### **Core Tables Structure**
```sql
-- Parliamentary entities table
CREATE TABLE parliamentary_entities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(50) NOT NULL,
    data JSONB NOT NULL,
    metadata JSONB DEFAULT '{}',
    relationships TEXT[] DEFAULT '{}',
    source VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Relationships table
CREATE TABLE entity_relationships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_entity_id UUID REFERENCES parliamentary_entities(id),
    target_entity_id UUID REFERENCES parliamentary_entities(id),
    relationship_type VARCHAR(100) NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Audit trail table
CREATE TABLE entity_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id UUID REFERENCES parliamentary_entities(id),
    action VARCHAR(50) NOT NULL,
    changes JSONB,
    user_id VARCHAR(100),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### **Indexes for Performance**
```sql
-- Performance indexes
CREATE INDEX idx_parliamentary_entities_type ON parliamentary_entities(type);
CREATE INDEX idx_parliamentary_entities_source ON parliamentary_entities(source);
CREATE INDEX idx_parliamentary_entities_created_at ON parliamentary_entities(created_at);
CREATE INDEX idx_parliamentary_entities_data_gin ON parliamentary_entities USING GIN (data);

-- Full-text search index
CREATE INDEX idx_parliamentary_entities_search ON parliamentary_entities 
USING GIN (to_tsvector('english', data::text));
```

---

## 🔄 ETL PIPELINE ARCHITECTURE

### **Legacy System Connectors**
```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import asyncio
import aiohttp

class LegacyConnector(ABC):
    """Abstract base class for legacy system connectors"""
    
    def __init__(self, source_name: str, config: Dict[str, Any]):
        self.source_name = source_name
        self.config = config
        self.session = None
    
    @abstractmethod
    async def extract(self) -> List[Dict[str, Any]]:
        """Extract data from legacy system"""
        pass
    
    @abstractmethod
    async def transform(self, raw_data: Dict[str, Any]) -> ParliamentaryEntity:
        """Transform raw data to unified format"""
        pass
    
    async def load(self, entity: ParliamentaryEntity) -> bool:
        """Load entity to unified system"""
        pass

class OpenParliamentConnector(LegacyConnector):
    """Connector for OpenParliament legacy system"""
    
    async def extract(self) -> List[Dict[str, Any]]:
        """Extract MPs, bills, votes from OpenParliament"""
        # Implementation using Django ORM or direct DB access
        pass
    
    async def transform(self, raw_data: Dict[str, Any]) -> ParliamentaryEntity:
        """Transform OpenParliament data to unified format"""
        # Implementation with data mapping and validation
        pass
```

### **Data Pipeline Orchestrator**
```python
class ETLOrchestrator:
    """Orchestrates the entire ETL pipeline"""
    
    def __init__(self, connectors: List[LegacyConnector]):
        self.connectors = connectors
        self.metrics = {}
    
    async def run_full_sync(self) -> Dict[str, Any]:
        """Run full synchronization from all legacy systems"""
        start_time = datetime.utcnow()
        results = {}
        
        for connector in self.connectors:
            try:
                async with connector:
                    raw_data = await connector.extract()
                    entities = []
                    for data in raw_data:
                        entity = await connector.transform(data)
                        success = await connector.load(entity)
                        if success:
                            entities.append(entity)
                    
                    results[connector.source_name] = {
                        "extracted": len(raw_data),
                        "loaded": len(entities),
                        "success": True
                    }
                    
            except Exception as e:
                results[connector.source_name] = {
                    "extracted": 0,
                    "loaded": 0,
                    "success": False,
                    "error": str(e)
                }
        
        return results
```

---

## 🐳 DEVELOPMENT ENVIRONMENT SETUP

### **Docker Configuration**
```dockerfile
# API Gateway Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Docker Compose Setup**
```yaml
version: '3.8'

services:
  api-gateway:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/mergev2
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    volumes:
      - ./logs:/app/logs

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=mergev2
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

---

## 🧪 TESTING INFRASTRUCTURE

### **Test Configuration**
```python
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --strict-markers
    --strict-config
    --cov=services
    --cov=models
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=90
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    e2e: marks tests as end-to-end tests
    performance: marks tests as performance tests
```

### **Test Data Factories**
```python
from factory import Factory, Faker
from models.parliamentary_entity import MP

class MPFactory(Factory):
    class Meta:
        model = MP
    
    name = Faker('name')
    party = Faker('random_element', elements=['Liberal', 'Conservative', 'NDP', 'Green'])
    riding = Faker('city')
    source = 'test'
```

---

## 🚀 CI/CD PIPELINE SETUP

### **GitHub Actions Workflow**
```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ --cov=services --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ --cov=services --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## 📊 MONITORING & OBSERVABILITY

### **Metrics Collection**
```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Metrics definitions
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Number of active connections')

# Middleware for metrics collection
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_DURATION.observe(duration)
    
    return response
```

### **Logging Configuration**
```python
import logging
import json
from datetime import datetime

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
        
        return json.dumps(log_entry)
```

---

## 🔐 SECURITY IMPLEMENTATION

### **Authentication & Authorization**
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class SecurityService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
```

---

## 📋 IMPLEMENTATION TASKS

### **Week 1: Core Architecture**
1. **API Design Finalization** - Complete endpoint specifications
2. **Database Schema Creation** - Implement unified data model
3. **ETL Pipeline Design** - Legacy system connector architecture
4. **Security Framework** - Authentication and authorization setup

### **Week 2: Infrastructure & Testing**
1. **Development Environment** - Docker setup and configuration
2. **Testing Framework** - pytest configuration and test data factories
3. **CI/CD Pipeline** - GitHub Actions workflow setup
4. **Monitoring Setup** - Metrics collection and logging

---

## 🎯 SUCCESS CRITERIA

### **Technical Deliverables**
- ✅ Complete API specification with OpenAPI documentation
- ✅ Database schema with migrations and performance indexes
- ✅ ETL pipeline architecture with connector specifications
- ✅ Working development environment with Docker
- ✅ Automated testing framework with 90%+ coverage
- ✅ CI/CD pipeline with automated testing
- ✅ Monitoring and observability infrastructure

### **Quality Standards**
- **Code Coverage:** >90% across all components
- **API Documentation:** 100% OpenAPI specification coverage
- **Test Automation:** 100% automated test execution
- **Security:** JWT authentication and role-based access control
- **Performance:** <500ms API response times for 95% of requests

---

## 🔄 NEXT STEPS

### **Immediate Actions**
1. **Begin API endpoint design** - Start with parliamentary entities
2. **Create database schema** - Implement unified data model
3. **Design ETL connectors** - Legacy system integration architecture
4. **Set up Docker environment** - Development infrastructure

### **Validation Checkpoints**
- **API Design Review** - Validate endpoint specifications
- **Database Schema Review** - Confirm data model design
- **ETL Architecture Review** - Validate integration approach
- **Infrastructure Testing** - Verify development environment

---

## 💡 KEY INSIGHTS

### **1. API-First Design**
- Design APIs before implementation
- Focus on user experience and developer experience
- Ensure consistent patterns across all endpoints

### **2. Data Model Unification**
- Single source of truth for all entities
- Consistent schema across legacy systems
- Full audit trail and versioning

### **3. Testing from Start**
- Implement testing framework early
- Maintain high code coverage throughout development
- Automate testing in CI/CD pipeline

### **4. Security by Design**
- Implement authentication and authorization early
- Use industry-standard security practices
- Regular security testing and validation

---

## 📞 CONCLUSION

**Iteration 2 focuses on detailed technical implementation planning** to establish the foundation for successful development. By completing this iteration, we will have:

- **Complete API specification** ready for implementation
- **Unified database schema** designed for performance and scalability
- **ETL pipeline architecture** for legacy system integration
- **Development environment** with automated testing and CI/CD

**Ready to proceed with Iteration 3: Development Environment Setup**

**Status: 🔄 ITERATION 2 IN PROGRESS - TECHNICAL PLANNING**
