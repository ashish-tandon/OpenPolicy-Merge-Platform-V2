# Data Flow Mapping: OpenParliament.ca Architecture

**Date**: January 2025  
**Project**: OpenPolicy Merge Platform V2  
**Purpose**: Map data flow from sources to user interface

## 🏗️ **Complete System Architecture Overview**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DATA SOURCES                                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Parliament of Canada    │ Elections Canada    │ Committee Sources    │ Other    │
│ • Bills & Legislation   │ • MP Information    │ • Meeting Schedules  │ • News   │
│ • Vote Results          │ • Constituency Data │ • Study Reports      │ • Media  │
│ • Debate Transcripts    │ • Party Changes     │ • Witness Lists      │ • Social │
│ • Session Status        │ • Election Results  │ • Chair Elections    │ • RSS    │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        SCRAPING & ETL LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│ legacy/civic-scraper/  │ legacy/scrapers-ca/  │ services/etl/        │         │
│ • Web scraping utils   │ • Canadian sources   │ • Data pipeline      │         │
│ • Rate limiting        │ • Parliament tools   │ • Transformers       │         │
│ • Error handling       │ • Committee tools    │ • Validators         │         │
│ • Data extraction      │ • MP data tools      │ • Loaders            │         │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        DATA PROCESSING LAYER                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│ AI Processor           │ Real-time Processor  │ Data Enrichment      │         │
│ • Debate summaries     │ • Live updates       │ • Geocoding          │         │
│ • Topic extraction     │ • WebSocket events  │ • Party affiliation  │         │
│ • Word analysis        │ • Status changes     │ • Relationship maps  │         │
│ • Sentiment analysis   │ • Notifications      │ • Data validation    │         │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        DATABASE LAYER                                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│ PostgreSQL Database (6GB OpenParliament Data)                                 │
│ • bills_bill           │ • core_politician    │ • hansards_statement │         │
│ • bills_votequestion   │ • core_electedmember │ • core_party         │         │
│ • bills_membervote     │ • core_riding        │ • core_committee     │         │
│ • bills_partyvote      │ • core_politicianinfo│ • core_meeting       │         │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        API LAYER (✅ WORKING)                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│ services/api-gateway/ (FastAPI)                                               │
│ • /api/v1/bills/       │ • /api/v1/members/   │ • /api/v1/debates/   │         │
│ • /api/v1/search/      │ • /api/v1/committees/│ • /api/v1/votes/     │         │
│ • /api/v1/represent/   │ • /api/v1/alerts/    │ • /api/v1/export/    │         │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER (❌ MISSING)                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│ services/web-ui/ (Next.js)                                                    │
│ • Homepage            │ • Bills Browser       │ • MP Profiles        │         │
│ • Search Interface    │ • Debates Archive     │ • Committee Pages    │         │
│ • User Dashboard      │ • Vote Results        │ • Advanced Search    │         │
│ • Mobile App          │ • Data Export         │ • Admin Interface    │         │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        USER ENGAGEMENT LAYER (❌ MISSING)                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Notification Service  │ Authentication        │ Personalization      │         │
│ • Email alerts        │ • OAuth login         │ • Saved searches     │         │
│ • RSS feeds          │ • User accounts        │ • Custom dashboards  │         │
│ • Push notifications  │ • Profile management  │ • Alert preferences  │         │
│ • SMS alerts          │ • Role-based access   │ • Data export        │         │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 📊 **Current Implementation Status**

### **✅ COMPLETED LAYERS**

#### **Database Layer**
- **Status**: ✅ **FULLY OPERATIONAL**
- **Data**: 6GB OpenParliament production database
- **Schema**: All tables properly mapped and connected
- **Performance**: Optimized with proper indexes and relationships

#### **API Layer**
- **Status**: ✅ **FULLY OPERATIONAL**
- **Endpoints**: 5/6 core APIs working with real data
- **Data Flow**: Database → SQLAlchemy → Pydantic → FastAPI → JSON
- **Performance**: Fast response times with proper pagination

### **🔄 PARTIALLY IMPLEMENTED LAYERS**

#### **Data Processing Layer**
- **Status**: 🔄 **BASIC STRUCTURE ONLY**
- **What Works**: Basic data validation and transformation
- **What's Missing**: AI processing, real-time updates, data enrichment
- **Current State**: Static data processing, no live updates

### **❌ MISSING LAYERS**

#### **Scraping & ETL Layer**
- **Status**: ❌ **NOT CONNECTED**
- **Legacy Code**: Available in `legacy/civic-scraper/` and `legacy/scrapers-ca/`
- **Current State**: ETL service exists but not integrated with scrapers
- **Data Flow**: No real-time data ingestion

#### **User Interface Layer**
- **Status**: ❌ **NOT IMPLEMENTED**
- **Legacy Reference**: Available in `legacy/openparliament/` (Django templates)
- **Current State**: APIs working but no way for users to interact
- **Impact**: System unusable for end users

#### **User Engagement Layer**
- **Status**: ❌ **NOT IMPLEMENTED**
- **Legacy Reference**: Available in `legacy/openparliament/` (user system)
- **Current State**: No authentication, alerts, or personalization
- **Impact**: No user accounts or engagement features

## 🔄 **Data Flow Mapping by Feature**

### **1. Bills & Legislation Flow**

```
Parliament of Canada
        │
        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Bill Status     │───▶│ ETL Pipeline    │───▶│ Database       │
│ Updates         │    │ (Not Connected) │    │ bills_bill     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                        ┌─────────────────┐    ┌─────────────────┐
                        │ Data Validation │    │ API Gateway    │
                        │ (Not Working)   │    │ /api/v1/bills/ │
                        └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │ Web UI          │
                                                │ (Not Built)     │
                                                └─────────────────┘
```

**Current Status**: ✅ Database → API working, ❌ Real-time updates missing

### **2. MP & Constituency Data Flow**

```
Elections Canada
        │
        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ MP Information  │───▶│ ETL Pipeline    │───▶│ Database       │
│ Updates         │    │ (Not Connected) │    │ core_politician│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                        ┌─────────────────┐    ┌─────────────────┐
                        │ Data Enrichment │    │ API Gateway    │
                        │ (Not Working)   │    │ /api/v1/members/│
                        └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │ Web UI          │
                                                │ (Not Built)     │
                                                └─────────────────┘
```

**Current Status**: ✅ Database → API working, ❌ Real-time updates missing

### **3. Debates & Hansard Flow**

```
Parliament of Canada
        │
        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Debate          │───▶│ ETL Pipeline    │───▶│ Database       │
│ Transcripts     │    │ (Not Connected) │    │ hansards_statement│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                        ┌─────────────────┐    ┌─────────────────┐
                        │ AI Processing   │    │ API Gateway    │
                        │ (Not Working)   │    │ /api/v1/debates/│
                        └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │ Web UI          │
                                                │ (Not Built)     │
                                                └─────────────────┘
```

**Current Status**: ✅ Database → API working, ❌ AI processing missing

### **4. Votes & Results Flow**

```
Parliament of Canada
        │
        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Vote Results    │───▶│ ETL Pipeline    │───▶│ Database       │
│ Updates         │    │ (Not Connected) │    │ bills_votequestion│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                        ┌─────────────────┐    ┌─────────────────┐
                        │ Real-time       │    │ API Gateway    │
                        │ Processing      │    │ /api/v1/votes/ │
                        │ (Not Working)   │    │ (Disabled)     │
                        └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │ Web UI          │
                                                │ (Not Built)     │
                                                └─────────────────┘
```

**Current Status**: ❌ API disabled due to recursion, ❌ Real-time updates missing

## 🔗 **Integration Points & Dependencies**

### **Critical Dependencies**

#### **1. ETL Pipeline Integration**
- **Dependency**: `services/etl/` ↔ `legacy/civic-scraper/` + `legacy/scrapers-ca/`
- **Status**: Not connected
- **Impact**: No real-time data updates
- **Priority**: HIGH (Week 2-4)

#### **2. Web UI Development**
- **Dependency**: `services/web-ui/` ↔ `services/api-gateway/`
- **Status**: Not implemented
- **Impact**: System unusable for users
- **Priority**: CRITICAL (Week 1-2)

#### **3. Authentication System**
- **Dependency**: `services/auth-service/` ↔ `services/web-ui/`
- **Status**: Not implemented
- **Impact**: No user accounts or alerts
- **Priority**: HIGH (Week 5-8)

#### **4. AI Processing Pipeline**
- **Dependency**: `services/ai-processor/` ↔ `services/etl/`
- **Status**: Not implemented
- **Impact**: Missing debate summaries and analysis
- **Priority**: MEDIUM (Week 8-16)

### **Data Flow Dependencies**

#### **Real-time Updates**
```
Source → Scraper → ETL → Database → API → WebSocket → UI
  ❌      ❌       ❌      ✅       ✅     ❌        ❌
```

#### **User Authentication**
```
User → Auth Service → Database → API → UI
 ❌        ❌          ✅       ✅     ❌
```

#### **AI Processing**
```
Database → AI Processor → Enhanced Data → API → UI
   ✅         ❌            ❌           ✅     ❌
```

## 🎯 **Implementation Roadmap by Data Flow**

### **Phase 1: Basic Data Flow (Week 1-2)**
- [ ] **Database → API → UI Flow**
  - [ ] Create Next.js web application
  - [ ] Connect UI to working APIs
  - [ ] Display parliamentary data
  - [ ] Basic search functionality

### **Phase 2: Data Ingestion Flow (Week 2-4)**
- [ ] **Source → Scraper → ETL → Database Flow**
  - [ ] Analyze legacy scrapers
  - [ ] Design ETL pipeline
  - [ ] Integrate first scraper
  - [ ] Test real-time updates

### **Phase 3: User Engagement Flow (Week 5-8)**
- [ ] **User → Auth → Database → API → UI Flow**
  - [ ] Implement authentication
  - [ ] User account management
  - [ ] Personalized data display
  - [ ] Email alert system

### **Phase 4: Advanced Processing Flow (Week 8-16)**
- [ ] **Database → AI → Enhanced Data → API → UI Flow**
  - [ ] AI processing pipeline
  - [ ] Real-time updates
  - [ ] Advanced visualizations
  - [ ] External API integrations

## 🔍 **Data Quality & Validation Points**

### **Current Validation**
- ✅ **Database Schema**: Proper foreign keys and constraints
- ✅ **API Validation**: Pydantic schemas with proper validation
- ✅ **Data Integrity**: 6GB production data verified working

### **Missing Validation**
- ❌ **Source Data Validation**: No validation of scraped data
- ❌ **Real-time Validation**: No validation of live updates
- ❌ **User Input Validation**: No UI to test user inputs
- ❌ **Performance Validation**: No load testing of complete system

## 📊 **Performance Metrics & Monitoring**

### **Current Metrics**
- ✅ **API Response Time**: Fast with proper pagination
- ✅ **Database Query Performance**: Optimized with indexes
- ✅ **Data Volume**: 6GB successfully loaded and accessible

### **Missing Metrics**
- ❌ **Real-time Update Latency**: No live data to measure
- ❌ **User Experience Metrics**: No UI to measure
- ❌ **System Load Metrics**: No production usage to monitor
- ❌ **Data Freshness Metrics**: No update frequency tracking

## 🎯 **Conclusion & Next Steps**

### **Current State Assessment**
- **Strengths**: Solid database and API foundation
- **Weaknesses**: No user interface, no real-time updates
- **Opportunities**: Legacy scrapers available for integration
- **Threats**: System unusable without UI

### **Immediate Action Required**
1. **Week 1-2**: Build web UI to make system usable
2. **Week 2-4**: Integrate legacy scrapers for real-time data
3. **Week 5-8**: Add user authentication and engagement
4. **Week 8-16**: Implement advanced features and AI processing

### **Success Criteria**
- **Phase 1**: Users can browse parliamentary data via web interface
- **Phase 2**: System receives real-time parliamentary updates
- **Phase 3**: Users can create accounts and receive alerts
- **Phase 4**: Full OpenParliament.ca feature parity achieved

This data flow mapping provides a complete picture of our current architecture and the path to full implementation, following our fundamental rule of copying and adapting legacy code while building a modern, scalable system.
