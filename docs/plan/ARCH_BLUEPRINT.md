# OpenPolicy V2 Architecture Blueprint

Generated: 2025-08-23

This document describes the architecture of OpenPolicy V2 using the C4 model (Context, Container, Component, Code).

## System Context (Level 1)

```mermaid
graph TB
    subgraph "OpenPolicy V2 System"
        OP[OpenPolicy Platform]
    end
    
    subgraph "Users"
        CIT[Citizens]
        MP[MPs/Staff]
        RES[Researchers]
        ADM[Administrators]
    end
    
    subgraph "External Systems"
        PARL[Parliament APIs]
        LEG[LEGISinfo]
        SOC[Social Media APIs]
        EMAIL[Email Service]
    end
    
    CIT --> OP
    MP --> OP
    RES --> OP
    ADM --> OP
    
    OP --> PARL
    OP --> LEG
    OP --> SOC
    OP --> EMAIL
```

### Context Description

**OpenPolicy V2** is a platform that provides transparent access to Canadian parliamentary data including:
- MP profiles and contact information
- Bill tracking and status
- Voting records and analysis
- Committee activities
- Debate transcripts

**Users**:
- **Citizens**: View parliamentary data, track bills, see how MPs vote
- **MPs/Staff**: Monitor legislation, track constituent feedback
- **Researchers**: Access historical data, analyze voting patterns
- **Administrators**: Manage system, monitor data quality

**External Systems**:
- **Parliament APIs**: Official parliamentary data sources
- **LEGISinfo**: Legislative information system
- **Social Media APIs**: Twitter/Facebook for MP social activity
- **Email Service**: SendGrid/AWS SES for notifications

## Container Diagram (Level 2)

```mermaid
graph TB
    subgraph "Web Browser"
        WEB[Web Application<br/>React/Next.js]
    end
    
    subgraph "Mobile Device"
        MOB[Mobile App<br/>React Native]
    end
    
    subgraph "API Gateway"
        GW[API Gateway<br/>FastAPI]
    end
    
    subgraph "Application Services"
        ETL[ETL Service<br/>Python]
        USER[User Service<br/>FastAPI]
        ADMIN[Admin Service<br/>FastAPI]
    end
    
    subgraph "Data Storage"
        PG[(PostgreSQL<br/>Primary DB)]
        REDIS[(Redis<br/>Cache/Queue)]
        ES[(Elasticsearch<br/>Search)]
    end
    
    subgraph "External"
        EXT[External APIs]
    end
    
    WEB --> GW
    MOB --> GW
    
    GW --> USER
    GW --> ADMIN
    GW --> PG
    GW --> REDIS
    GW --> ES
    
    ETL --> PG
    ETL --> REDIS
    ETL --> ES
    ETL --> EXT
    
    USER --> PG
    USER --> REDIS
    ADMIN --> PG
```

### Container Descriptions

**Frontend Containers**:
- **Web Application**: Next.js SSR application for desktop/mobile web
- **Mobile App**: React Native application for iOS/Android (future)

**API Layer**:
- **API Gateway**: Central entry point, handles auth, routing, rate limiting

**Application Services**:
- **ETL Service**: Ingests data from external sources, transforms, loads
- **User Service**: Handles user auth, preferences, subscriptions
- **Admin Service**: System management, monitoring, manual overrides

**Data Storage**:
- **PostgreSQL**: Primary database for all transactional data
- **Redis**: Caching layer and task queue
- **Elasticsearch**: Full-text search across all content

## Component Diagram - API Gateway (Level 3)

```mermaid
graph TB
    subgraph "API Gateway Components"
        AUTH[Auth Middleware]
        RATE[Rate Limiter]
        ROUTE[Router]
        CACHE[Cache Manager]
        VALID[Request Validator]
        
        subgraph "API Endpoints"
            MEMB[Members API]
            BILL[Bills API]
            VOTE[Votes API]
            SRCH[Search API]
        end
    end
    
    subgraph "External"
        CLIENT[Client Request]
        BACKEND[Backend Services]
    end
    
    CLIENT --> AUTH
    AUTH --> RATE
    RATE --> VALID
    VALID --> ROUTE
    ROUTE --> CACHE
    
    CACHE --> MEMB
    CACHE --> BILL
    CACHE --> VOTE
    CACHE --> SRCH
    
    MEMB --> BACKEND
    BILL --> BACKEND
    VOTE --> BACKEND
    SRCH --> BACKEND
```

### Component Descriptions

**Auth Middleware**: JWT validation, user context extraction
**Rate Limiter**: Redis-backed rate limiting per user/IP
**Request Validator**: Pydantic-based input validation
**Router**: FastAPI router, handles versioning
**Cache Manager**: Redis cache with TTL policies
**API Endpoints**: Domain-specific API handlers

## Component Diagram - ETL Service (Level 3)

```mermaid
graph LR
    subgraph "ETL Components"
        SCHED[Scheduler<br/>APScheduler]
        
        subgraph "Extractors"
            PARL_EX[Parliament Extractor]
            LEG_EX[LEGISinfo Extractor]
            CSV_EX[CSV Extractor]
        end
        
        subgraph "Transformers"
            NORM[Normalizer]
            VALID[Validator]
            ENRICH[Enricher]
        end
        
        subgraph "Loaders"
            PG_LOAD[PostgreSQL Loader]
            ES_LOAD[Elasticsearch Indexer]
        end
        
        QUEUE[Task Queue<br/>Redis Queue]
    end
    
    SCHED --> QUEUE
    QUEUE --> PARL_EX
    QUEUE --> LEG_EX
    QUEUE --> CSV_EX
    
    PARL_EX --> NORM
    LEG_EX --> NORM
    CSV_EX --> NORM
    
    NORM --> VALID
    VALID --> ENRICH
    ENRICH --> PG_LOAD
    ENRICH --> ES_LOAD
```

## Data Architecture

### Database Schema (Core Tables)

```sql
-- Members
CREATE TABLE members (
    id UUID PRIMARY KEY,
    parliament_id VARCHAR UNIQUE,
    name VARCHAR NOT NULL,
    party VARCHAR,
    constituency VARCHAR,
    province VARCHAR,
    email VARCHAR,
    photo_url VARCHAR,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Bills
CREATE TABLE bills (
    id UUID PRIMARY KEY,
    number VARCHAR UNIQUE,
    title TEXT NOT NULL,
    summary TEXT,
    status VARCHAR,
    sponsor_id UUID REFERENCES members(id),
    introduced_date DATE,
    last_updated TIMESTAMP
);

-- Votes
CREATE TABLE votes (
    id UUID PRIMARY KEY,
    bill_id UUID REFERENCES bills(id),
    vote_date TIMESTAMP,
    result VARCHAR,
    yeas INTEGER,
    nays INTEGER,
    abstentions INTEGER
);

-- Ballots (Individual MP votes)
CREATE TABLE ballots (
    id UUID PRIMARY KEY,
    vote_id UUID REFERENCES votes(id),
    member_id UUID REFERENCES members(id),
    position VARCHAR, -- 'yea', 'nay', 'abstain', 'absent'
    UNIQUE(vote_id, member_id)
);
```

### Caching Strategy

| Data Type | Cache TTL | Invalidation |
|-----------|-----------|--------------|
| Member profiles | 1 hour | On update |
| Bill list | 5 minutes | On new bill |
| Vote results | 5 minutes | On new vote |
| Search results | 15 minutes | Time-based |
| Static content | 24 hours | Manual |

### Search Index Structure

```json
{
  "bills": {
    "mappings": {
      "properties": {
        "number": { "type": "keyword" },
        "title": { "type": "text", "analyzer": "english" },
        "summary": { "type": "text", "analyzer": "english" },
        "status": { "type": "keyword" },
        "sponsor_name": { "type": "text" },
        "introduced_date": { "type": "date" }
      }
    }
  }
}
```

## Deployment Architecture

### Production Environment

```mermaid
graph TB
    subgraph "Internet"
        USERS[Users]
        CF[Cloudflare CDN]
    end
    
    subgraph "Load Balancer"
        LB[Application LB]
    end
    
    subgraph "Kubernetes Cluster"
        subgraph "Web Tier"
            WEB1[Web Pod 1]
            WEB2[Web Pod 2]
            WEB3[Web Pod 3]
        end
        
        subgraph "API Tier"
            API1[API Pod 1]
            API2[API Pod 2]
            API3[API Pod 3]
        end
        
        subgraph "Worker Tier"
            ETL1[ETL Worker 1]
            ETL2[ETL Worker 2]
        end
    end
    
    subgraph "Data Tier"
        subgraph "PostgreSQL"
            PG_PRIMARY[(Primary)]
            PG_REPLICA[(Replica)]
        end
        
        subgraph "Redis Cluster"
            REDIS1[(Redis 1)]
            REDIS2[(Redis 2)]
        end
        
        subgraph "Elasticsearch"
            ES1[(ES Node 1)]
            ES2[(ES Node 2)]
            ES3[(ES Node 3)]
        end
    end
    
    USERS --> CF
    CF --> LB
    LB --> WEB1
    LB --> WEB2
    LB --> WEB3
    
    WEB1 --> API1
    WEB2 --> API2
    WEB3 --> API3
    
    API1 --> PG_PRIMARY
    API2 --> PG_PRIMARY
    API3 --> PG_REPLICA
    
    ETL1 --> PG_PRIMARY
    ETL2 --> PG_PRIMARY
```

### Infrastructure Specifications

**Kubernetes Cluster**:
- 3 master nodes (m5.large)
- 6 worker nodes (m5.xlarge)
- Auto-scaling enabled (min: 6, max: 20)

**Database Tier**:
- PostgreSQL: RDS db.r6g.xlarge (Multi-AZ)
- Redis: ElastiCache cache.r6g.large (Cluster mode)
- Elasticsearch: 3x i3.large instances

**Storage**:
- Application: EBS gp3 volumes
- Database: EBS io2 volumes
- Backups: S3 with lifecycle policies

## Security Architecture

### Network Security

```mermaid
graph TB
    subgraph "Public Subnet"
        ALB[Application Load Balancer]
        NAT[NAT Gateway]
    end
    
    subgraph "Private Subnet - Web"
        WEB[Web Servers]
    end
    
    subgraph "Private Subnet - App"
        APP[Application Servers]
    end
    
    subgraph "Private Subnet - Data"
        DB[(Databases)]
    end
    
    INTERNET[Internet] --> ALB
    ALB --> WEB
    WEB --> APP
    APP --> DB
    APP --> NAT
    NAT --> INTERNET
```

### Security Layers

1. **Network Layer**:
   - VPC with public/private subnets
   - Security groups per tier
   - NACLs for subnet protection
   - VPN for admin access

2. **Application Layer**:
   - JWT authentication
   - API key management
   - Rate limiting
   - Input validation

3. **Data Layer**:
   - Encryption at rest
   - TLS for data in transit
   - Database user permissions
   - Audit logging

## Performance Requirements

### SLAs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Uptime | 99.9% | Monthly |
| API Response Time (p95) | < 200ms | Per endpoint |
| Search Response Time (p95) | < 500ms | Full-text search |
| Data Freshness | < 6 hours | Source to display |
| Concurrent Users | 10,000 | Peak capacity |

### Scaling Triggers

| Resource | Scale Up | Scale Down |
|----------|----------|------------|
| Web Pods | CPU > 70% | CPU < 30% |
| API Pods | CPU > 70% | CPU < 30% |
| ETL Workers | Queue > 1000 | Queue < 100 |
| Database Connections | > 80% | < 40% |

## Monitoring Architecture

### Observability Stack

```mermaid
graph LR
    subgraph "Applications"
        APP[Application<br/>Metrics & Logs]
    end
    
    subgraph "Collection"
        PROM[Prometheus]
        LOKI[Loki]
        TEMPO[Tempo]
    end
    
    subgraph "Storage"
        CORTEX[Cortex]
        S3[(S3 Storage)]
    end
    
    subgraph "Visualization"
        GRAF[Grafana]
        ALERT[AlertManager]
    end
    
    APP --> PROM
    APP --> LOKI
    APP --> TEMPO
    
    PROM --> CORTEX
    LOKI --> S3
    TEMPO --> S3
    
    CORTEX --> GRAF
    S3 --> GRAF
    PROM --> ALERT
```

### Key Metrics

**Application Metrics**:
- Request rate, error rate, duration (RED)
- Active users, sessions
- Feature usage statistics

**Infrastructure Metrics**:
- CPU, memory, disk, network
- Container restarts
- Database connections
- Cache hit rates

**Business Metrics**:
- Daily active users
- Bills tracked per user
- Search queries per day
- API usage by endpoint

## Disaster Recovery

### Backup Strategy

| Component | Frequency | Retention | Location |
|-----------|-----------|-----------|----------|
| Database | Continuous | 30 days | S3 Cross-region |
| Application State | Daily | 7 days | S3 |
| Configuration | On change | Forever | Git + S3 |
| Elasticsearch | Daily | 7 days | Snapshots to S3 |

### Recovery Objectives

- **RTO** (Recovery Time Objective): 4 hours
- **RPO** (Recovery Point Objective): 1 hour

### DR Procedures

1. **Database Failure**: Promote read replica, restore from backup
2. **Region Failure**: Failover to DR region (us-west-2)
3. **Data Corruption**: Point-in-time recovery from backups
4. **Service Failure**: Auto-restart, then manual intervention

## Evolution Roadmap

### Phase 1 (Current)
- Core features operational
- Basic monitoring
- Manual deployments

### Phase 2 (Q2 2025)
- GraphQL API
- Advanced analytics
- CI/CD automation

### Phase 3 (Q3 2025)
- Mobile applications
- AI-powered insights
- Multi-language support

### Phase 4 (Q4 2025)
- Real-time collaboration
- Predictive analytics
- Blockchain audit trail