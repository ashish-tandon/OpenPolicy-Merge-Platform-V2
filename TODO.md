# OpenParliament Migration - Cursor Todo List

**Date**: January 2025  
**Project**: OpenPolicy Merge Platform V2  
**Current Phase**: Phase 1 ✅ COMPLETED - Moving to Phase 2  
**Status**: Core APIs Working, ALL Legacy Code Copied and Organized

## 🎯 **PHASE 2: Systematic UI Migration (Week 1-2)**

### **✅ COMPLETED: Legacy Code Organization**

Following **FUNDAMENTAL RULE #1: NEVER REINVENT THE WHEEL**, we have successfully copied ALL OpenParliament.ca code to organized locations:

#### **1. Web UI Legacy Migration** ✅ COMPLETED
- [x] **ALL Django Templates**: `legacy/openparliament/parliament/templates/` → `services/web-ui/src/legacy-migration/templates/`
- [x] **ALL Static Assets**: `legacy/openparliament/parliament/static/` → `services/web-ui/src/legacy-migration/static/`
- [x] **ALL Core Models**: `legacy/openparliament/parliament/core/` → `services/web-ui/src/legacy-migration/core/`
- [x] **ALL Bills System**: `legacy/openparliament/parliament/bills/` → `services/web-ui/src/legacy-migration/bills/`
- [x] **ALL MPs System**: `legacy/openparliament/parliament/politicians/` → `services/web-ui/src/legacy-migration/politicians/`
- [x] **ALL Debates System**: `legacy/openparliament/parliament/hansards/` → `services/web-ui/src/legacy-migration/debates/`
- [x] **ALL Committees System**: `legacy/openparliament/parliament/committees/` → `services/web-ui/src/legacy-migration/committees/`
- [x] **ALL Search System**: `legacy/openparliament/parliament/search/` → `services/web-ui/src/legacy-migration/search/`
- [x] **ALL User Accounts**: `legacy/openparliament/parliament/accounts/` → `services/web-ui/src/legacy-migration/accounts/`
- [x] **ALL Alert System**: `legacy/openparliament/parliament/alerts/` → `services/web-ui/src/legacy-migration/alerts/`
- [x] **ALL Text Analysis**: `legacy/openparliament/parliament/text_analysis/` → `services/web-ui/src/legacy-migration/text-analysis/`
- [x] **ALL Summaries**: `legacy/openparliament/parliament/summaries/` → `services/web-ui/src/legacy-migration/summaries/`
- [x] **ALL Haiku System**: `legacy/openparliament/parliament/haiku/` → `services/web-ui/src/legacy-migration/haiku/`
- [x] **ALL Elections System**: `legacy/openparliament/parliament/elections/` → `services/web-ui/src/legacy-migration/elections/`
- [x] **ALL Data Imports**: `legacy/openparliament/parliament/imports/` → `services/web-ui/src/legacy-migration/imports/`
- [x] **ALL Activity Tracking**: `legacy/openparliament/parliament/activity/` → `services/web-ui/src/legacy-migration/activity/`
- [x] **ALL Utilities**: `legacy/openparliament/parliament/utils/` → `services/web-ui/src/legacy-migration/utils/`
- [x] **ALL API System**: `legacy/openparliament/parliament/api/` → `services/web-ui/src/legacy-migration/api/`
- [x] **ALL Localization**: `legacy/openparliament/parliament/locale/` → `services/web-ui/src/legacy-migration/locale/`
- [x] **ALL Configuration**: `legacy/openparliament/parliament/config/` → `services/web-ui/src/legacy-migration/config/`

#### **2. ETL Legacy Migration** ✅ COMPLETED
- [x] **ALL Civic Scrapers**: `legacy/civic-scraper/` → `services/etl/legacy-civic-scraper/`
- [x] **ALL Canadian Scrapers**: `legacy/scrapers-ca/` → `services/etl/legacy-scrapers-ca/`

### **🔄 NEXT: Systematic Migration from Organized Legacy Code**

#### **Week 1: Foundation Analysis**
- [ ] **Study Legacy Structure**: Analyze copied code organization in `services/web-ui/src/legacy-migration/`
- [ ] **Map Dependencies**: Understand how components interact across the copied codebase
- [ ] **Create Migration Plan**: Plan component-by-component migration strategy
- [ ] **Set Up Development Environment**: Configure Next.js with proper TypeScript and Tailwind

#### **Week 2: Core Components Migration**
- [ ] **Layout Component**: Convert `legacy-migration/templates/base.html` to `Layout.tsx`
  - [ ] Copy navigation structure (MPs, Bills, Debates, Committees, About, Labs)
  - [ ] Copy search functionality from navbar
  - [ ] Copy language toggle (English/French)
  - [ ] Copy responsive design patterns

- [ ] **Homepage Component**: Convert `legacy-migration/templates/home.html` to `page.tsx`
  - [ ] Copy search box with postal code, name, phrase functionality
  - [ ] Copy "What we're doing" section
  - [ ] Copy "What they're talking about" section with latest Hansard
  - [ ] Copy recently debated bills section
  - [ ] Copy recent votes section
  - [ ] Copy site news section

#### **Week 3: Feature Components Migration**
- [ ] **Bills System**: Migrate from `legacy-migration/bills/`
  - [ ] Convert Django models to TypeScript interfaces
  - [ ] Convert Django views to React components
  - [ ] Implement bill listing and detail pages
  - [ ] Connect to working `/api/v1/bills/` API

- [ ] **MPs System**: Migrate from `legacy-migration/politicians/`
  - [ ] Convert Django models to TypeScript interfaces
  - [ ] Convert Django views to React components
  - [ ] Implement MP listing and profile pages
  - [ ] Connect to working `/api/v1/members/` API

#### **Week 4: Advanced Components Migration**
- [ ] **Debates System**: Migrate from `legacy-migration/debates/`
  - [ ] Convert Django models to TypeScript interfaces
  - [ ] Convert Django views to React components
  - [ ] Implement debate listing and detail pages
  - [ ] Connect to working `/api/v1/debates/` API

- [ ] **Search System**: Migrate from `legacy-migration/search/`
  - [ ] Convert Django search views to React components
  - [ ] Implement search interface and result display
  - [ ] Connect to working `/api/v1/search/` API

## 🔄 **PHASE 3: Data Pipeline Integration (Week 5-6)**

### **Integrate Organized Legacy Scrapers with ETL**

#### **1. Analyze Organized Legacy Scraping Capabilities**
- [ ] **Review `services/etl/legacy-civic-scraper/`**
  - [ ] Document existing scraping utilities
  - [ ] Identify parliamentary data sources
  - [ ] Map data flow and output formats
  - [ ] Assess integration requirements

- [ ] **Review `services/etl/legacy-scrapers-ca/`**
  - [ ] Document Canadian data scrapers
  - [ ] Identify Parliament of Canada sources
  - [ ] Map scraping patterns and schedules
  - [ ] Assess data quality and reliability

#### **2. Design ETL Pipeline**
- [ ] **Map Data Sources to Database**
  - [ ] Parliament of Canada (bills, votes, debates)
  - [ ] Elections Canada (MP data, constituency info)
  - [ ] Committee information sources
  - [ ] Real-time parliamentary status

- [ ] **Design Data Flow Architecture**
  - [ ] Source → Scraper → Transformer → Database
  - [ ] Real-time vs. batch processing
  - [ ] Data validation and quality checks
  - [ ] Error handling and retry logic

#### **3. Integrate First Scraper**
- [ ] **Start with Basic Parliamentary Updates**
  - [ ] Bill status updates
  - [ ] New vote results
  - [ ] Recent debate transcripts
  - [ ] MP information updates

## 🔧 **PHASE 4: Advanced Features Migration (Week 7-8)**

### **Migrate Advanced Features from Organized Legacy Code**

#### **1. Fix Votes API and Enable Advanced Features**
- [ ] **Resolve Recursion Issues**
  - [ ] Update `services/api-gateway/app/models/openparliament.py`
  - [ ] Resolve `MemberVote` and `Politician` circular dependencies
  - [ ] Test votes API endpoints
  - [ ] Enable in main.py router

#### **2. Implement User Authentication**
- [ ] **Migrate Legacy User System** from `legacy-migration/accounts/`
  - [ ] Convert Django user models to modern auth patterns
  - [ ] Implement OAuth integration (Google, GitHub)
  - [ ] JWT token management

#### **3. Email Alert System**
- [ ] **Migrate Legacy Notification System** from `legacy-migration/alerts/`
  - [ ] Convert email templates for parliamentary updates
  - [ ] User preference management
  - [ ] Alert scheduling and delivery

## 🚀 **PHASE 5: Advanced OpenParliament.ca Features (Week 9-12)**

### **AI Processing and Real-time Updates**

#### **1. AI Processing Pipeline**
- [ ] **Migrate Legacy AI Capabilities** from `legacy-migration/text-analysis/` and `legacy-migration/summaries/`
  - [ ] Natural language processing for debates
  - [ ] Topic extraction and categorization
  - [ ] Word frequency analysis
  - [ ] Sentiment analysis

#### **2. Real-time Updates**
- [ ] **Migrate Legacy Real-time Patterns** from `legacy-migration/` real-time features
  - [ ] WebSocket connections for live data
  - [ ] Live vote results and debate updates
  - [ ] Parliamentary session status

#### **3. Advanced UI Features**
- [ ] **Migrate Legacy Visualization Patterns** from `legacy-migration/` visualization code
  - [ ] Word clouds from debates
  - [ ] Voting patterns charts
  - [ ] Parliamentary activity timelines

## 📋 **Documentation and Testing Tasks**

### **1. Update Project Documentation**
- [ ] **Update README.md**
  - [ ] Current status and achievements
  - [ ] API documentation links
  - [ ] Development setup instructions
  - [ ] Feature roadmap

- [ ] **Create Development Guides**
  - [ ] API development guide
  - [ ] UI development guide (copying from organized legacy)
  - [ ] Database schema documentation
  - [ ] Deployment instructions

### **2. Testing and Quality Assurance**
- [ ] **API Testing**
  - [ ] Unit tests for all endpoints
  - [ ] Integration tests with database
  - [ ] Performance testing for large datasets
  - [ ] Error handling validation

- [ ] **UI Testing**
  - [ ] Component testing with React Testing Library
  - [ ] End-to-end testing with Playwright
  - [ ] Accessibility testing
  - [ ] Cross-browser compatibility

## 🔗 **Legacy Integration Tasks**

### **1. Legacy Code Analysis and Migration**
- [ ] **Review Organized Legacy Code** in `services/web-ui/src/legacy-migration/`
  - [ ] Document Django implementation patterns
  - [ ] Extract reusable business logic
  - [ ] Map Django models to our SQLAlchemy models
  - [ ] Identify migration strategies

- [ ] **Review Other Legacy Repositories**
  - [ ] `legacy/open-policy-web/` - Web UI patterns
  - [ ] `legacy/open-policy-app/` - Mobile app patterns
  - [ ] `legacy/admin-open-policy/` - Admin interface patterns
  - [ ] `legacy/open-policy-infra/` - Infrastructure patterns

### **2. Data Migration and Synchronization**
- [ ] **Database Schema Alignment**
  - [ ] Compare legacy Django models with current SQLAlchemy
  - [ ] Identify missing fields and relationships
  - [ ] Plan schema updates and migrations
  - [ ] Test data integrity

## 📊 **Progress Tracking**

### **Phase 1: Core Functionality (✅ COMPLETED)**
- [x] Database integration and API development
- [x] Schema alignment and Pydantic compatibility
- [x] Docker infrastructure setup
- [x] All core APIs working with real data
- [x] **ALL Legacy Code Copied and Organized**

### **Phase 2: UI Migration (🔄 IN PROGRESS)**
- [x] Copy ALL legacy UI templates and assets
- [x] Organize legacy code in proper folder structure
- [ ] Analyze organized legacy code structure
- [ ] Map dependencies and create migration plan
- [ ] Migrate core components systematically

### **Phase 3: Data Pipeline (❌ NOT STARTED)**
- [ ] Legacy scraper analysis (from organized locations)
- [ ] ETL pipeline design
- [ ] First scraper integration
- [ ] Real-time data updates

### **Phase 4: User Experience (❌ NOT STARTED)**
- [ ] User accounts and authentication (from organized legacy)
- [ ] Personalized email alerts (from organized legacy)
- [ ] Advanced search and filtering
- [ ] Votes API fixes

### **Phase 5: Advanced Features (❌ NOT STARTED)**
- [ ] AI processing pipeline (from organized legacy)
- [ ] Real-time updates (from organized legacy)
- [ ] Advanced visualizations (from organized legacy)
- [ ] External API integrations

## 🎯 **Success Criteria**

### **Phase 2: Basic Functionality (Week 1-4)**
- [ ] Web application accessible at localhost:3000
- [ ] All parliamentary data pages functional
- [ ] Search interface working
- [ ] Basic navigation and layout
- [ ] **All components migrated from organized legacy code**

### **Phase 3: Data Pipeline (Week 5-6)**
- [ ] Real-time parliamentary updates
- [ ] Automated data synchronization
- [ ] Error handling and monitoring
- [ ] Performance optimization

### **Phase 4: User Experience (Week 7-8)**
- [ ] User accounts and authentication (from organized legacy)
- [ ] Personalized email alerts (from organized legacy)
- [ ] Advanced search and filtering
- [ ] Mobile-responsive design

### **Phase 5: Feature Parity (Week 9-12)**
- [ ] AI-powered debate analysis (from organized legacy)
- [ ] Real-time parliamentary monitoring (from organized legacy)
- [ ] Advanced data visualizations (from organized legacy)
- [ ] External API integrations

## 🔗 **Resource Links**

- **Current Implementation**: `services/api-gateway/` - Working FastAPI backend
- **Legacy Reference**: `legacy/openparliament/` - Original Django implementation
- **Organized Legacy**: `services/web-ui/src/legacy-migration/` - **ALL OpenParliament code copied and organized**
- **ETL Legacy**: `services/etl/legacy-*/` - All legacy scrapers copied and organized
- **Database Schema**: `db/openparliament.public.sql` - 6GB production database
- **API Documentation**: `openapi.yaml` - Current API specification
- **Migration Plan**: `docs/Open Parliament Migration Plan/` - Complete documentation
- **Legacy Code Mapping**: `docs/Open Parliament Migration Plan/13-LEGACY-CODE-MAPPING.md` - Complete mapping

## 🎯 **Next Immediate Action**

**START WITH: Analyzing Organized Legacy Code Structure**

1. **Study copied Django templates** in `services/web-ui/src/legacy-migration/templates/`
2. **Analyze component organization** in the copied codebase
3. **Map dependencies** between different legacy components
4. **Create systematic migration plan** component by component

**Following the fundamental rule**: ALL legacy code is now copied and organized. We can systematically migrate each component from the organized legacy code to our modern Next.js architecture, ensuring we maintain all 109+ OpenParliament.ca features.

This comprehensive todo list provides a clear roadmap from our current working state to full OpenParliament.ca feature parity, following our established development approach and the fundamental rule of copying and adapting legacy code.
