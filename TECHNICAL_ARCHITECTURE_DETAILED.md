# 🏗️ DETAILED TECHNICAL ARCHITECTURE
## Merge V2: Unified Parliamentary Data Platform

**Date:** August 21, 2025  
**Version:** 1.0  
**Status:** 🔴 DESIGN PHASE  
**Scope:** Complete technical specification  

---

## 🎯 ARCHITECTURE PRINCIPLES

### **1. Unified Data Model**
- Single source of truth for all parliamentary entities
- Consistent schema across all legacy systems
- Versioned data with full audit trail

### **2. Microservices Architecture**
- Loosely coupled, independently deployable services
- Clear service boundaries and interfaces
- Event-driven communication where appropriate

### **3. API-First Design**
- All functionality exposed via REST/GraphQL APIs
- Consistent API patterns and error handling
- Comprehensive API documentation

### **4. Data Pipeline Architecture**
- Extract → Transform → Load (ETL) for all data sources
- Real-time and batch processing capabilities
- Data quality validation at every stage

---

## 🏛️ SYSTEM ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  Web App (React)  │  Mobile App  │  Admin UI   │  3rd Party   │
│                   │  (React Native)│  (React)    │  Integrations│
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│  Authentication  │  Rate Limiting │  Request Routing │  Caching │
│  & Authorization │                │                 │          │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SERVICE LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  Parliamentary  │  Municipal     │  Analytics   │  Admin      │
│  Service       │  Service       │  Service     │  Service    │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│  PostgreSQL    │  Redis Cache   │  Elasticsearch │  MinIO     │
│  (Primary DB)  │  (Session/API) │  (Search)      │  (Files)   │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ETL PIPELINE LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  Legacy System │  Data          │  Quality      │  Monitoring │
│  Connectors    │  Transformers  │  Validators   │  & Alerting │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔧 CORE COMPONENTS SPECIFICATION

### **1. API Gateway (FastAPI + Traefik)**

#### **Technology Stack**
- **Framework:** FastAPI 0.104+
- **Reverse Proxy:** Traefik 3.0+
- **Authentication:** JWT + OAuth2
- **Rate Limiting:** Redis-based
- **Documentation:** OpenAPI 3.0 + Swagger UI

#### **Key Features**
```python
# API Gateway Configuration
class APIGatewayConfig:
    # Rate limiting
    rate_limit_per_minute: int = 100
    rate_limit_per_hour: int = 1000
    
    # Authentication
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60
    
    # Caching
    cache_ttl_seconds: int = 300
    cache_max_size: int = 10000
```

#### **API Endpoints Structure**
```
/api/v1/
├── /auth/           # Authentication & authorization
├── /parliamentary/  # MPs, bills, votes, debates
├── /municipal/      # Municipal government data
├── /analytics/      # Data insights & reporting
├── /admin/          # Administrative functions
└── /health/         # System health checks
```

### **2. Parliamentary Service (Core Business Logic)**

#### **Data Models**
```python
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field

class EntityType(str, Enum):
    MP = "mp"
    BILL = "bill"
    VOTE = "vote"
    DEBATE = "debate"
    COMMITTEE = "committee"
    SESSION = "session"

class ParliamentaryEntity(BaseModel):
    id: str = Field(..., description="Unique identifier")
    type: EntityType = Field(..., description="Entity type")
    data: Dict[str, Any] = Field(..., description="Entity data")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    relationships: List[str] = Field(default_factory=list)
    source: str = Field(..., description="Legacy system source")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    version: int = Field(default=1, description="Data version")

class MP(ParliamentaryEntity):
    type: EntityType = EntityType.MP
    data: Dict[str, Any] = Field(..., description="MP-specific data")
    
    @property
    def name(self) -> str:
        return self.data.get("name", "")
    
    @property
    def party(self) -> str:
        return self.data.get("party", "")
    
    @property
    def riding(self) -> str:
        return self.data.get("riding", "")

class Bill(ParliamentaryEntity):
    type: EntityType = EntityType.BILL
    data: Dict[str, Any] = Field(..., description="Bill-specific data")
    
    @property
    def title(self) -> str:
        return self.data.get("title", "")
    
    @property
    def status(self) -> str:
        return self.data.get("status", "")
    
    @property
    def sponsor(self) -> str:
        return self.data.get("sponsor", "")
```

#### **Service Implementation**
```python
from typing import List, Optional
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

class ParliamentaryService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_mp(self, mp_id: str) -> Optional[MP]:
        """Retrieve MP by ID"""
        # Implementation with caching and error handling
        pass
    
    async def get_mps_by_party(self, party: str) -> List[MP]:
        """Retrieve all MPs by party"""
        # Implementation with pagination
        pass
    
    async def get_bill(self, bill_id: str) -> Optional[Bill]:
        """Retrieve bill by ID"""
        # Implementation with relationship loading
        pass
    
    async def search_entities(
        self, 
        query: str, 
        entity_type: Optional[EntityType] = None,
        limit: int = 50
    ) -> List[ParliamentaryEntity]:
        """Search across all entity types"""
        # Implementation with full-text search
        pass
```

### **3. ETL Pipeline (Data Integration)**

#### **Legacy System Connectors**
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
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
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
        # Implementation with transaction handling
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

class MunicipalScrapersConnector(LegacyConnector):
    """Connector for municipal scrapers"""
    
    async def extract(self) -> List[Dict[str, Any]]:
        """Extract municipal data from various sources"""
        # Implementation using existing scraper infrastructure
        pass
    
    async def transform(self, raw_data: Dict[str, Any]) -> ParliamentaryEntity:
        """Transform municipal data to unified format"""
        # Implementation with data normalization
        pass
```

#### **Data Pipeline Orchestrator**
```python
import asyncio
from typing import List
from datetime import datetime

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
                    # Extract
                    raw_data = await connector.extract()
                    
                    # Transform and load
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
        
        self.metrics["last_sync"] = {
            "start_time": start_time,
            "end_time": datetime.utcnow(),
            "results": results
        }
        
        return results
    
    async def run_incremental_sync(self) -> Dict[str, Any]:
        """Run incremental synchronization"""
        # Implementation with change detection
        pass
```

### **4. Data Layer (PostgreSQL + Redis)**

#### **Database Schema Design**
```sql
-- Core entities table
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

-- Indexes for performance
CREATE INDEX idx_parliamentary_entities_type ON parliamentary_entities(type);
CREATE INDEX idx_parliamentary_entities_source ON parliamentary_entities(source);
CREATE INDEX idx_parliamentary_entities_created_at ON parliamentary_entities(created_at);
CREATE INDEX idx_parliamentary_entities_data_gin ON parliamentary_entities USING GIN (data);

-- Full-text search index
CREATE INDEX idx_parliamentary_entities_search ON parliamentary_entities 
USING GIN (to_tsvector('english', data::text));

-- Relationships table for complex queries
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

#### **Redis Configuration**
```python
# Redis configuration for caching and sessions
REDIS_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
    "password": None,
    "decode_responses": True,
    "max_connections": 20
}

# Cache key patterns
CACHE_KEYS = {
    "mp": "mp:{mp_id}",
    "bill": "bill:{bill_id}",
    "search": "search:{query_hash}",
    "session": "session:{session_id}"
}

# Cache TTL settings
CACHE_TTL = {
    "mp": 3600,        # 1 hour
    "bill": 1800,      # 30 minutes
    "search": 900,     # 15 minutes
    "session": 86400   # 24 hours
}
```

---

## 🔐 SECURITY ARCHITECTURE

### **1. Authentication & Authorization**
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

### **2. API Security**
```python
# Security middleware configuration
SECURITY_CONFIG = {
    "cors_origins": ["https://yourdomain.com"],
    "rate_limiting": {
        "requests_per_minute": 100,
        "requests_per_hour": 1000
    },
    "api_keys": {
        "required": True,
        "header_name": "X-API-Key"
    }
}
```

---

## 📊 MONITORING & OBSERVABILITY

### **1. Metrics Collection**
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

### **2. Logging Strategy**
```python
import logging
import json
from datetime import datetime

# Structured logging configuration
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

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "structured": {
            "()": StructuredFormatter
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "structured"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "structured"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    }
}
```

---

## 🚀 DEPLOYMENT & INFRASTRUCTURE

### **1. Docker Configuration**
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

### **2. Docker Compose**
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

  etl-pipeline:
    build: ./etl
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/mergev2
    depends_on:
      - postgres
    volumes:
      - ./data:/app/data

volumes:
  postgres_data:
  redis_data:
```

---

## 🧪 TESTING STRATEGY

### **1. Test Pyramid**
```
        /\
       /  \     E2E Tests (10%)
      /____\    
     /      \   Integration Tests (20%)
    /________\  
   /          \  Unit Tests (70%)
  /____________\
```

### **2. Test Coverage Requirements**
```python
# Test coverage configuration
COVERAGE_CONFIG = {
    "minimum_coverage": 90,
    "exclude_patterns": [
        "*/tests/*",
        "*/migrations/*",
        "*/venv/*"
    ],
    "fail_under": 90
}

# Component-specific coverage requirements
COMPONENT_COVERAGE = {
    "api_gateway": 95,
    "parliamentary_service": 90,
    "etl_pipeline": 85,
    "data_models": 100
}
```

---

## 📈 PERFORMANCE REQUIREMENTS

### **1. Response Time Targets**
```python
# Performance targets
PERFORMANCE_TARGETS = {
    "api_response_time": {
        "p50": "< 200ms",
        "p95": "< 500ms",
        "p99": "< 1000ms"
    },
    "database_query_time": {
        "simple_queries": "< 50ms",
        "complex_queries": "< 200ms"
    },
    "etl_processing_time": {
        "incremental_sync": "< 5 minutes",
        "full_sync": "< 2 hours"
    }
}
```

### **2. Scalability Targets**
```python
# Scalability requirements
SCALABILITY_TARGETS = {
    "concurrent_users": 10000,
    "requests_per_second": 1000,
    "data_volume": "100TB+",
    "entities_per_second": 10000
}
```

---

## 🔄 NEXT STEPS

### **Immediate (Next 2 Weeks)**
1. **Set up development environment** with Docker
2. **Create database schema** and migrations
3. **Implement core data models** and services
4. **Set up basic API endpoints** for testing

### **Short Term (Next Month)**
1. **Implement ETL pipeline** for one legacy system
2. **Create basic web interface** for data viewing
3. **Set up monitoring** and logging infrastructure
4. **Begin integration testing** with legacy systems

### **Medium Term (Next 3 Months)**
1. **Complete ETL pipeline** for all legacy systems
2. **Implement full API** with authentication
3. **Create comprehensive web interface**
4. **Begin user acceptance testing**

This technical architecture provides the foundation for a robust, scalable, and maintainable parliamentary data platform that will successfully integrate all legacy systems while providing a modern, unified user experience.
