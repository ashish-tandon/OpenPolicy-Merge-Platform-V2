# Comprehensive TODO List: OpenParliament Migration

**Date**: January 2025  
**Project**: OpenPolicy Merge Platform V2  
**Status**: Core APIs Working, UI and Advanced Features Pending

## 🎯 **CRITICAL PRIORITY: User Interface (Week 1-2)**

### **1. Create Next.js Web Application** 
- [ ] **Setup Next.js Project** in `services/web-ui/`
  - [ ] Initialize with TypeScript and Tailwind CSS
  - [ ] Configure API client for our working FastAPI backend
  - [ ] Setup routing structure for parliamentary data
  - **Legacy Reference**: `legacy/openparliament/` - Django templates for UI patterns
  - **Current State**: APIs working, no UI exists

### **2. Core Parliamentary Data Pages**
- [ ] **Bills Page** (`/bills`)
  - [ ] Display bill list with pagination
  - [ ] Connect to working `/api/v1/bills/` API
  - [ ] Implement search and filtering
  - [ ] Show bill details and status
  - **Legacy Reference**: `legacy/openparliament/` - Bill display patterns
  - **API Status**: ✅ Working with real data

- [ ] **MPs Page** (`/mps`)
  - [ ] Display MP list with photos and party info
  - [ ] Connect to working `/api/v1/members/` API
  - [ ] Implement province and party filtering
  - [ ] Show individual MP profiles
  - **Legacy Reference**: `legacy/openparliament/` - MP display patterns
  - **API Status**: ✅ Working with real data

- [ ] **Debates Page** (`/debates`)
  - [ ] Display debate list by date
  - [ ] Connect to working `/api/v1/debates/` API
  - [ ] Show debate summaries and statement counts
  - [ ] Implement date-based navigation
  - **Legacy Reference**: `legacy/openparliament/` - Debate display patterns
  - **API Status**: ✅ Working with real data

- [ ] **Search Page** (`/search`)
  - [ ] Implement search interface
  - [ ] Connect to working `/api/v1/search/` API
  - [ ] Show results with snippets and filtering
  - [ ] Support content type filtering
  - **Legacy Reference**: `legacy/openparliament/` - Search interface patterns
  - **API Status**: ✅ Working with real data

## 🔄 **HIGH PRIORITY: Data Pipeline Integration (Week 2-4)**

### **3. Analyze Legacy Scraping Capabilities**
- [ ] **Review `legacy/civic-scraper/`**
  - [ ] Document existing scraping utilities
  - [ ] Identify parliamentary data sources
  - [ ] Map data flow and output formats
  - [ ] Assess integration requirements
  - **Current State**: Not analyzed, needs integration

- [ ] **Review `legacy/scrapers-ca/`**
  - [ ] Document Canadian data scrapers
  - [ ] Identify Parliament of Canada sources
  - [ ] Map scraping patterns and schedules
  - [ ] Assess data quality and reliability
  - **Current State**: Not analyzed, needs integration

### **4. Design ETL Pipeline**
- [ ] **Map Data Sources to Database**
  - [ ] Parliament of Canada (bills, votes, debates)
  - [ ] Elections Canada (MP data, constituency info)
  - [ ] Committee information sources
  - [ ] Real-time parliamentary status
  - **Current State**: Static 6GB database, no updates

- [ ] **Design Data Flow Architecture**
  - [ ] Source → Scraper → Transformer → Database
  - [ ] Real-time vs. batch processing
  - [ ] Data validation and quality checks
  - [ ] Error handling and retry logic
  - **Current State**: ETL service exists but not connected

### **5. Integrate First Scraper**
- [ ] **Start with Basic Parliamentary Updates**
  - [ ] Bill status updates
  - [ ] New vote results
  - [ ] Recent debate transcripts
  - [ ] MP information updates
  - **Current State**: No real-time updates

## 🔧 **MEDIUM PRIORITY: Advanced Features (Week 4-8)**

### **6. Fix Votes API and Enable Advanced Features**
- [ ] **Resolve Recursion Issues**
  - [ ] Fix circular relationships in SQLAlchemy models
  - [ ] Update `services/api-gateway/app/models/openparliament.py`
  - [ ] Test votes API endpoints
  - [ ] Enable in main.py router
  - **Current State**: Disabled due to recursion errors

### **7. Implement User Authentication**
- [ ] **Create Auth Service**
  - [ ] User registration and login
  - [ ] OAuth integration (Google, GitHub)
  - [ ] JWT token management
  - [ ] User profile management
  - **Legacy Reference**: `legacy/openparliament/` - User system patterns
  - **Current State**: No authentication system

### **8. Email Alert System**
- [ ] **Notification Service**
  - [ ] Email templates for parliamentary updates
  - [ ] User preference management
  - [ ] Alert scheduling and delivery
  - [ ] Rate limiting and spam prevention
  - **Legacy Reference**: `legacy/openparliament/` - Email system patterns
  - **Current State**: No notification system

## 🚀 **LONG-TERM: Advanced OpenParliament.ca Features (Week 8-16)**

### **9. AI Processing and Analysis**
- [ ] **Debate Summaries**
  - [ ] Natural language processing pipeline
  - [ ] Computer-generated debate summaries
  - [ ] Topic extraction and categorization
  - [ ] Word frequency analysis
  - **Legacy Reference**: `legacy/openparliament/` - AI processing patterns
  - **Current State**: No AI capabilities

### **10. Real-time Updates**
- [ ] **Live Parliamentary Status**
  - [ ] WebSocket connections for real-time data
  - [ ] Live vote results and debate updates
  - [ ] Parliamentary session status
  - [ ] Push notifications for users
  - **Legacy Reference**: `legacy/openparliament/` - Real-time patterns
  - **Current State**: No real-time capabilities

### **11. Advanced UI Features**
- [ ] **Data Visualizations**
  - [ ] Word clouds from debates
  - [ ] Voting patterns charts
  - [ ] Parliamentary activity timelines
  - [ ] Interactive maps for constituencies
  - **Legacy Reference**: `legacy/openparliament/` - Visualization patterns
  - **Current State**: Basic UI only

### **12. External API Integrations**
- [ ] **Represent API Integration**
  - [ ] Electoral boundary data
  - [ ] Postal code MP lookup
  - [ ] Geographic data integration
  - [ ] Rate limiting and caching
  - **Current State**: Basic integration exists but needs fixing

- [ ] **LEGISinfo Integration**
  - [ ] Official government bill data
  - [ ] Legislative text access
  - [ ] Status synchronization
  - [ ] Document management
  - **Current State**: No integration

## 📋 **Documentation and Testing Tasks**

### **13. Update Project Documentation**
- [ ] **Update README.md**
  - [ ] Current status and achievements
  - [ ] API documentation links
  - [ ] Development setup instructions
  - [ ] Feature roadmap
  - **Current State**: Basic README exists

- [ ] **Create Development Guides**
  - [ ] API development guide
  - [ ] UI development guide
  - [ ] Database schema documentation
  - [ ] Deployment instructions
  - **Current State**: Limited documentation

### **14. Testing and Quality Assurance**
- [ ] **API Testing**
  - [ ] Unit tests for all endpoints
  - [ ] Integration tests with database
  - [ ] Performance testing for large datasets
  - [ ] Error handling validation
  - **Current State**: Basic functionality, limited testing

- [ ] **UI Testing**
  - [ ] Component testing with React Testing Library
  - [ ] End-to-end testing with Playwright
  - [ ] Accessibility testing
  - [ ] Cross-browser compatibility
  - **Current State**: No UI exists

## 🔗 **Legacy Integration Tasks**

### **15. Legacy Code Analysis and Migration**
- [ ] **Review `legacy/openparliament/`**
  - [ ] Document Django implementation patterns
  - [ ] Extract reusable business logic
  - [ ] Map Django models to our SQLAlchemy models
  - [ ] Identify migration strategies
  - **Current State**: Basic analysis done, needs deeper review

- [ ] **Review Other Legacy Repositories**
  - [ ] `legacy/open-policy-web/` - Web UI patterns
  - [ ] `legacy/open-policy-app/` - Mobile app patterns
  - [ ] `legacy/admin-open-policy/` - Admin interface patterns
  - [ ] `legacy/open-policy-infra/` - Infrastructure patterns
  - **Current State**: Not analyzed

### **16. Data Migration and Synchronization**
- [ ] **Database Schema Alignment**
  - [ ] Compare legacy Django models with current SQLAlchemy
  - [ ] Identify missing fields and relationships
  - [ ] Plan schema updates and migrations
  - [ ] Test data integrity
  - **Current State**: Basic alignment done, needs verification

## 📊 **Progress Tracking**

### **Week 1-2: Foundation (Current)**
- [x] Database integration and API development
- [x] Schema alignment and Pydantic compatibility
- [ ] Next.js web application setup
- [ ] Core parliamentary data pages

### **Week 3-4: Data Pipeline**
- [ ] Legacy scraper analysis
- [ ] ETL pipeline design
- [ ] First scraper integration
- [ ] Real-time data updates

### **Week 5-8: User Experience**
- [ ] User authentication system
- [ ] Email alert system
- [ ] Advanced search features
- [ ] Votes API fixes

### **Week 9-16: Advanced Features**
- [ ] AI processing pipeline
- [ ] Real-time updates
- [ ] Advanced visualizations
- [ ] External API integrations

## 🎯 **Success Criteria**

### **Phase 1: Basic Functionality (Week 1-2)**
- [ ] Web application accessible at localhost:3000
- [ ] All parliamentary data pages functional
- [ ] Search interface working
- [ ] Basic navigation and layout

### **Phase 2: Data Pipeline (Week 3-4)**
- [ ] Real-time parliamentary updates
- [ ] Automated data synchronization
- [ ] Error handling and monitoring
- [ ] Performance optimization

### **Phase 3: User Experience (Week 5-8)**
- [ ] User accounts and authentication
- [ ] Personalized email alerts
- [ ] Advanced search and filtering
- [ ] Mobile-responsive design

### **Phase 4: Feature Parity (Week 9-16)**
- [ ] AI-powered debate analysis
- [ ] Real-time parliamentary monitoring
- [ ] Advanced data visualizations
- [ ] External API integrations

## 🔗 **Resource Links**

- **Current Implementation**: `services/api-gateway/` - Working FastAPI backend
- **Legacy Reference**: `legacy/openparliament/` - Original Django implementation
- **Database Schema**: `db/openparliament.public.sql` - 6GB production database
- **API Documentation**: `openapi.yaml` - Current API specification
- **Migration Plan**: This document and related analysis files
- **OpenParliament.ca Analysis**: Complete feature inventory and technical documentation

## 🎯 **Next Immediate Action**

**START WITH: User Interface Development**
1. Create Next.js project in `services/web-ui/`
2. Implement basic parliamentary data pages
3. Connect to working APIs
4. Test with real data

**Following the fundamental rule**: Copy UI patterns from `legacy/openparliament/` and adapt to our Next.js architecture.

This comprehensive todo list provides a clear roadmap from our current working state to full OpenParliament.ca feature parity, following our established development approach and architecture.
