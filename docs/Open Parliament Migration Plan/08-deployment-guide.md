# Deployment Guide: OpenParliament Migration

**Date**: January 2025  
**Project**: OpenPolicy Merge Platform V2  
**Phase**: Phase 1 - Core Infrastructure & APIs

## 🚀 **Current Deployment Status**

### **✅ DEPLOYED & WORKING**
- **Database**: PostgreSQL 15+ with 6GB OpenParliament data
- **API Gateway**: FastAPI running on port 8080
- **Redis**: Cache and session storage
- **Docker Infrastructure**: All services containerized and running

### **❌ NOT YET DEPLOYED**
- **Web UI**: Next.js application (needs to be built from legacy)
- **ETL Pipeline**: Data ingestion from Parliament sources
- **Authentication Service**: User management and OAuth
- **AI Processing**: Debate analysis and summaries

## 🏗️ **Deployment Architecture**

### **Current Stack (Phase 1)**
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           PRODUCTION ENVIRONMENT                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Docker Compose Stack                                                          │
│ • PostgreSQL 15+ (Database)                                                   │
│ • Redis 7 (Cache & Sessions)                                                  │
│ • FastAPI Gateway (Port 8080)                                                 │
│ • Nginx (Reverse Proxy - Optional)                                            │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### **Target Stack (Phase 2-3)**
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        COMPLETE PRODUCTION STACK                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Frontend Layer                                                                 │
│ • Next.js Web Application (Port 3000)                                         │
│ • React Native Mobile App                                                     │
│ • Admin Dashboard                                                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Backend Layer                                                                  │
│ • FastAPI Gateway (Port 8080)                                                 │
│ • Authentication Service (Port 8081)                                          │
│ • ETL Pipeline Service (Port 8082)                                            │
│ • AI Processing Service (Port 8083)                                           │
│ • Notification Service (Port 8084)                                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Data Layer                                                                    │
│ • PostgreSQL 15+ (Primary Database)                                           │
│ • Redis 7 (Cache & Sessions)                                                  │
│ • Elasticsearch (Search & Analytics)                                          │
│ • MinIO (Document Storage)                                                    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📋 **Deployment Checklist**

### **Phase 1: Core Infrastructure (✅ COMPLETED)**
- [x] **Database Setup**
  - [x] PostgreSQL 15+ installation
  - [x] OpenParliament database restore (6GB)
  - [x] Schema validation and optimization
  - [x] Connection testing

- [x] **API Gateway Setup**
  - [x] FastAPI application deployment
  - [x] Database connection configuration
  - [x] API endpoint testing
  - [x] CORS and security configuration

- [x] **Infrastructure Setup**
  - [x] Docker and Docker Compose
  - [x] Redis cache service
  - [x] Health monitoring
  - [x] Logging configuration

### **Phase 2: User Interface (🔄 IN PROGRESS)**
- [ ] **Web Application Deployment**
  - [ ] Copy legacy UI patterns from `legacy/openparliament/`
  - [ ] Adapt Django templates to Next.js components
  - [ ] Build and deploy Next.js application
  - [ ] Connect to working APIs
  - [ ] Test with real parliamentary data

- [ ] **UI Infrastructure**
  - [ ] Nginx reverse proxy configuration
  - [ ] Static asset serving
  - [ ] SSL/TLS certificate setup
  - [ ] CDN configuration (optional)

### **Phase 3: Data Pipeline (❌ NOT STARTED)**
- [ ] **ETL Service Deployment**
  - [ ] Copy legacy scrapers from `legacy/civic-scraper/`
  - [ ] Copy legacy scrapers from `legacy/scrapers-ca/`
  - [ ] Adapt to our ETL architecture
  - [ ] Deploy data ingestion pipeline
  - [ ] Test real-time updates

- [ ] **Data Processing**
  - [ ] AI processing service deployment
  - [ ] Real-time update system
  - [ ] Data validation and quality checks
  - [ ] Performance monitoring

### **Phase 4: User Services (❌ NOT STARTED)**
- [ ] **Authentication Service**
  - [ ] Copy user system from `legacy/openparliament/`
  - [ ] Adapt to modern auth patterns
  - [ ] OAuth integration (Google, GitHub)
  - [ ] JWT token management

- [ ] **Notification Service**
  - [ ] Copy email system from legacy
  - [ ] Email template adaptation
  - [ ] Alert scheduling system
  - [ ] Rate limiting and spam prevention

## 🔧 **Deployment Commands**

### **Current Stack (Phase 1)**
```bash
# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f api-gateway

# Test API
curl http://localhost:8080/healthz
```

### **Web UI Deployment (Phase 2)**
```bash
# Navigate to web-ui directory
cd services/web-ui

# Install dependencies (after copying from legacy)
npm install

# Build for production
npm run build

# Start development server
npm run dev

# Start production server
npm start
```

### **ETL Pipeline Deployment (Phase 3)**
```bash
# Navigate to ETL directory
cd services/etl

# Copy legacy scrapers
cp -r ../../legacy/civic-scraper/* .
cp -r ../../legacy/scrapers-ca/* .

# Adapt and deploy
# (Implementation details to be determined)
```

## 🌐 **Environment Configuration**

### **Required Environment Variables**
```bash
# Database
POSTGRES_DB=openpolicy
POSTGRES_USER=openpolicy
POSTGRES_PASSWORD=<secure_password>

# API Gateway
API_HOST=0.0.0.0
API_PORT=8080
DEBUG=false
CORS_ORIGINS=https://yourdomain.com

# Web UI
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXT_PUBLIC_SITE_URL=https://yourdomain.com

# Authentication
GOOGLE_OAUTH_CLIENT_ID=<client_id>
GOOGLE_OAUTH_CLIENT_SECRET=<client_secret>
JWT_SECRET=<secure_jwt_secret>

# Email Service
SMTP_HOST=<smtp_host>
SMTP_PORT=587
SMTP_USER=<email_user>
SMTP_PASSWORD=<email_password>
```

### **Production Environment Setup**
```bash
# Create production environment file
cp .env.example .env.production

# Edit with production values
nano .env.production

# Load production environment
export $(cat .env.production | xargs)
```

## 📊 **Monitoring & Health Checks**

### **Current Health Endpoints**
- **API Gateway**: `http://localhost:8080/healthz`
- **Database**: Connection test via API health check
- **Redis**: Connection test via API health check

### **Target Health Endpoints (Phase 2-3)**
- **Web UI**: `http://localhost:3000/health`
- **ETL Service**: `http://localhost:8082/health`
- **Auth Service**: `http://localhost:8081/health`
- **AI Service**: `http://localhost:8083/health`

### **Monitoring Tools**
- **Application Logs**: Docker Compose logging
- **Database Monitoring**: PostgreSQL performance metrics
- **API Performance**: FastAPI built-in monitoring
- **System Resources**: Docker stats and system monitoring

## 🚨 **Security Considerations**

### **Current Security (Phase 1)**
- ✅ **Database**: Secure password, no external access
- ✅ **API Gateway**: CORS configuration, input validation
- ✅ **Network**: Local development environment

### **Production Security (Phase 2-3)**
- [ ] **SSL/TLS**: HTTPS encryption for all traffic
- [ ] **Authentication**: Secure user authentication system
- [ ] **Authorization**: Role-based access control
- [ ] **Input Validation**: Comprehensive input sanitization
- [ ] **Rate Limiting**: API usage throttling
- [ ] **Monitoring**: Security event logging and alerting

## 📈 **Scaling Considerations**

### **Current Scale (Phase 1)**
- **Database**: 6GB OpenParliament data
- **API Load**: Development/testing load
- **Users**: No user interface yet

### **Target Scale (Phase 2-3)**
- **Database**: Real-time updates + historical data
- **API Load**: Production parliamentary monitoring traffic
- **Users**: Public parliamentary data access
- **Real-time**: Live parliamentary session updates

### **Scaling Strategies**
- **Database**: Read replicas, connection pooling
- **API**: Load balancing, horizontal scaling
- **Cache**: Redis clustering, CDN for static assets
- **Storage**: Object storage for documents and media

## 🎯 **Deployment Timeline**

### **Week 1-2: Web UI (Phase 2)**
- [ ] Copy legacy UI patterns
- [ ] Build Next.js application
- [ ] Deploy and test with real data
- [ ] Basic user interface functionality

### **Week 3-4: Data Pipeline (Phase 3)**
- [ ] Copy legacy scrapers
- [ ] Adapt to ETL architecture
- [ ] Deploy data ingestion
- [ ] Test real-time updates

### **Week 5-8: User Services (Phase 4)**
- [ ] Authentication system
- [ ] Email notifications
- [ ] User management
- [ ] Advanced features

## 🔗 **Legacy Integration Notes**

Following our **FUNDAMENTAL RULE #1: NEVER REINVENT THE WHEEL**:

1. **UI Patterns**: Copy from `legacy/openparliament/parliament/templates/`
2. **Scraping Logic**: Copy from `legacy/civic-scraper/` and `legacy/scrapers-ca/`
3. **User System**: Copy from `legacy/openparliament/parliament/accounts/`
4. **Email System**: Copy from `legacy/openparliament/parliament/alerts/`

**Key Principle**: Adapt existing working code to our modern architecture rather than rebuilding from scratch.

## 📋 **Next Steps**

1. **Immediate**: Copy legacy UI templates and adapt to Next.js
2. **Short-term**: Deploy web application with working APIs
3. **Medium-term**: Integrate legacy scrapers for real-time data
4. **Long-term**: Full OpenParliament.ca feature parity

This deployment guide provides the roadmap from our current working state to a complete parliamentary monitoring platform, following our established development approach and architecture.
