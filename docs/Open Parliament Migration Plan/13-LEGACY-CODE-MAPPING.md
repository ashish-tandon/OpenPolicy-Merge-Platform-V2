# Legacy Code Mapping: OpenParliament Migration

**Date**: January 2025  
**Project**: OpenPolicy Merge Platform V2  
**Status**: Phase 1 Completed - Legacy Code Organized and Mapped

## 🎯 **Overview: Complete Legacy Code Migration**

Following **FUNDAMENTAL RULE #1: NEVER REINVENT THE WHEEL**, we have copied ALL OpenParliament.ca code to organized locations where it can be systematically adapted to our modern architecture.

## 📁 **Legacy Code Organization Structure**

### **1. Web UI Legacy Migration** (`services/web-ui/src/legacy-migration/`)

#### **Templates** (`templates/`)
**Source**: `legacy/openparliament/parliament/templates/`
**Purpose**: Django HTML templates for all UI components
**Contents**:
- `base.html` - Main layout template with navigation
- `home.html` - Homepage with search and parliamentary updates
- `bills/` - Bill listing and detail templates
- `politicians/` - MP profile and list templates
- `hansards/` - Debate and transcript templates
- `committees/` - Committee pages and meeting templates
- `search/` - Search interface and result templates
- `accounts/` - User authentication templates
- `alerts/` - Email alert and notification templates
- `labs/` - Experimental features (Haiku generator)
- `activity/` - User activity and dashboard templates

#### **Static Assets** (`static/`)
**Source**: `legacy/openparliament/parliament/static/`
**Purpose**: CSS, JavaScript, images, and other static files
**Contents**:
- `scss/` - Styling and layout
- `js/` - JavaScript functionality
- `images/` - Logos, icons, and graphics
- `fonts/` - Typography assets

#### **Core Models** (`core/`)
**Source**: `legacy/openparliament/parliament/core/`
**Purpose**: Django models for parliamentary data
**Contents**:
- `models.py` - Database models for MPs, parties, constituencies
- `admin.py` - Django admin interface configuration
- `views.py` - Core view logic
- `urls.py` - URL routing for core functionality

#### **Bills System** (`bills/`)
**Source**: `legacy/openparliament/parliament/bills/`
**Purpose**: Bill tracking and legislation management
**Contents**:
- `models.py` - Bill, vote, and sponsorship models
- `views.py` - Bill listing, detail, and search views
- `urls.py` - Bill-related URL routing
- `admin.py` - Bill admin interface

#### **Politicians System** (`politicians/`)
**Source**: `legacy/openparliament/parliament/politicians/`
**Purpose**: MP management and profiles
**Contents**:
- `models.py` - Politician, elected member, and party models
- `views.py` - MP profile and list views
- `urls.py` - MP-related URL routing
- `admin.py` - Politician admin interface

#### **Debates System** (`debates/`)
**Source**: `legacy/openparliament/parliament/hansards/`
**Purpose**: Parliamentary debate transcripts and analysis
**Contents**:
- `models.py` - Statement, debate, and speaker models
- `views.py` - Debate listing and detail views
- `urls.py` - Debate-related URL routing
- `admin.py` - Debate admin interface

#### **Committees System** (`committees/`)
**Source**: `legacy/openparliament/parliament/committees/`
**Purpose**: Parliamentary committee management
**Contents**:
- `models.py` - Committee, meeting, and study models
- `views.py` - Committee listing and detail views
- `urls.py` - Committee-related URL routing
- `admin.py` - Committee admin interface

#### **Search System** (`search/`)
**Source**: `legacy/openparliament/parliament/search/`
**Purpose**: Full-text search across parliamentary data
**Contents**:
- `views.py` - Search functionality and result display
- `urls.py` - Search URL routing
- Search indexing and query optimization

#### **User Accounts** (`accounts/`)
**Source**: `legacy/openparliament/parliament/accounts/`
**Purpose**: User authentication and management
**Contents**:
- `models.py` - User profile and preference models
- `views.py` - Login, registration, and profile views
- `urls.py` - Authentication URL routing
- `forms.py` - User input forms

#### **Alert System** (`alerts/`)
**Source**: `legacy/openparliament/parliament/alerts/`
**Purpose**: Email notifications and user alerts
**Contents**:
- `models.py` - Alert subscription and preference models
- `views.py` - Alert management and delivery views
- `urls.py` - Alert-related URL routing
- Email templates and delivery logic

#### **Text Analysis** (`text-analysis/`)
**Source**: `legacy/openparliament/parliament/text_analysis/`
**Purpose**: AI-powered debate analysis and processing
**Contents**:
- Natural language processing for debates
- Topic extraction and categorization
- Word frequency analysis
- Sentiment analysis

#### **Summaries** (`summaries/`)
**Source**: `legacy/openparliament/parliament/summaries/`
**Purpose**: Computer-generated debate summaries
**Contents**:
- AI summary generation
- Summary storage and retrieval
- Summary quality assessment

#### **Haiku System** (`haiku/`)
**Source**: `legacy/openparliament/parliament/haiku/`
**Purpose**: Experimental AI poetry generation
**Contents**:
- Haiku generation from parliamentary text
- Creative text processing
- Experimental features

#### **Elections System** (`elections/`)
**Source**: `legacy/openparliament/parliament/elections/`
**Purpose**: Electoral data and results
**Contents**:
- Election result models
- Historical electoral data
- Riding and constituency information

#### **Data Imports** (`imports/`)
**Source**: `legacy/openparliament/parliament/imports/`
**Purpose**: Data ingestion and synchronization
**Contents**:
- Parliamentary data import scripts
- Data validation and cleaning
- Import scheduling and monitoring

#### **Activity Tracking** (`activity/`)
**Source**: `legacy/openparliament/parliament/activity/`
**Purpose**: User activity and engagement tracking
**Contents**:
- User activity models
- Engagement metrics
- Activity feeds and notifications

#### **Utilities** (`utils/`)
**Source**: `legacy/openparliament/parliament/utils/`
**Purpose**: Helper functions and utilities
**Contents**:
- Common utility functions
- Data processing helpers
- Formatting and validation utilities

#### **API System** (`api/`)
**Source**: `legacy/openparliament/parliament/api/`
**Purpose**: REST API endpoints
**Contents**:
- API views and serializers
- API authentication and permissions
- API documentation and versioning

#### **Localization** (`locale/`)
**Source**: `legacy/openparliament/parliament/locale/`
**Purpose**: English/French language support
**Contents**:
- Translation files
- Language-specific content
- Internationalization support

#### **Configuration** (`config/`)
**Source**: `legacy/openparliament/parliament/`
**Purpose**: System configuration and settings
**Contents**:
- `default_settings.py` - Django configuration
- `urls.py` - Main URL routing
- `jobs.py` - Background job definitions

### **2. ETL Legacy Migration** (`services/etl/`)

#### **Civic Scraper** (`legacy-civic-scraper/`)
**Source**: `legacy/civic-scraper/`
**Purpose**: General web scraping utilities
**Contents**:
- Web scraping tools and utilities
- Rate limiting and error handling
- Data extraction patterns

#### **Canadian Scrapers** (`legacy-scrapers-ca/`)
**Source**: `legacy/scrapers-ca/`
**Purpose**: Canada-specific data scraping
**Contents**:
- Parliament of Canada scrapers
- Elections Canada data tools
- Provincial and municipal scrapers

## 🔄 **Migration Strategy by Component**

### **Phase 2: UI Migration (Week 1-2)**

#### **1. Template to Component Mapping**
- **Django Templates** → **React Components**
  - `base.html` → `Layout.tsx`
  - `home.html` → `page.tsx`
  - `bills/` → `app/bills/`
  - `politicians/` → `app/mps/`
  - `hansards/` → `app/debates/`
  - `committees/` → `app/committees/`
  - `search/` → `app/search/`

#### **2. Static Asset Migration**
- **Django Static** → **Next.js Public**
  - CSS/SCSS → Tailwind CSS + custom styles
  - JavaScript → React hooks and components
  - Images → Optimized Next.js image components

#### **3. Model to Interface Mapping**
- **Django Models** → **TypeScript Interfaces**
  - `core.models` → `types/core.ts`
  - `bills.models` → `types/bills.ts`
  - `politicians.models` → `types/politicians.ts`
  - `hansards.models` → `types/debates.ts`

### **Phase 3: Data Pipeline Migration (Week 2-4)**

#### **1. Scraper Integration**
- **Legacy Scrapers** → **ETL Pipeline**
  - `legacy-civic-scraper/` → `services/etl/scrapers/`
  - `legacy-scrapers-ca/` → `services/etl/scrapers/`

#### **2. Data Processing**
- **Legacy Utils** → **Modern ETL**
  - `utils/` → `services/etl/processors/`
  - `imports/` → `services/etl/importers/`

### **Phase 4: Advanced Features Migration (Week 4-8)**

#### **1. AI Processing**
- **Legacy Text Analysis** → **AI Service**
  - `text-analysis/` → `services/ai-processor/`
  - `summaries/` → `services/ai-processor/summaries/`

#### **2. User Management**
- **Legacy Accounts** → **Auth Service**
  - `accounts/` → `services/auth-service/`
  - `alerts/` → `services/notification-service/`

## 📊 **Feature Mapping to Legacy Code**

### **Core Parliamentary Data (109+ Features)**

#### **Bills & Legislation (17 features)**
- **Source**: `bills/` + `core/`
- **Legacy Models**: Bill, VoteQuestion, MemberVote, PartyVote
- **Target**: Connect to working `/api/v1/bills/` API

#### **MPs & Constituencies (17 features)**
- **Source**: `politicians/` + `core/`
- **Legacy Models**: Politician, ElectedMember, Party, Riding
- **Target**: Connect to working `/api/v1/members/` API

#### **Debates & Hansard (10 features)**
- **Source**: `debates/` + `text-analysis/`
- **Legacy Models**: Statement, Debate, Speaker
- **Target**: Connect to working `/api/v1/debates/` API

#### **Committees (8 features)**
- **Source**: `committees/`
- **Legacy Models**: Committee, Meeting, Study
- **Target**: Connect to working `/api/v1/committees/` API

#### **Search & Discovery (5 features)**
- **Source**: `search/`
- **Legacy Views**: Full-text search, filtering, suggestions
- **Target**: Connect to working `/api/v1/search/` API

#### **User Engagement (15 features)**
- **Source**: `accounts/` + `alerts/`
- **Legacy Models**: User, Alert, Preference
- **Target**: Modern authentication and notification services

#### **AI & Analysis (7 features)**
- **Source**: `text-analysis/` + `summaries/`
- **Legacy Models**: AI processing, topic extraction
- **Target**: Modern AI processing pipeline

#### **Experimental Features (7 features)**
- **Source**: `haiku/` + `labs/`
- **Legacy Models**: Creative text processing
- **Target**: Modern experimental features

## 🎯 **Next Steps: Systematic Migration**

### **Week 1: Foundation**
1. **Study Legacy Structure**: Analyze copied code organization
2. **Map Dependencies**: Understand how components interact
3. **Plan Migration**: Create component-by-component migration plan

### **Week 2: Core Components**
1. **Layout Component**: Convert `base.html` to `Layout.tsx`
2. **Homepage**: Convert `home.html` to `page.tsx`
3. **Navigation**: Implement navigation from legacy patterns
4. **Search**: Implement search from legacy functionality

### **Week 3-4: Feature Components**
1. **Bills System**: Migrate bill-related components
2. **MPs System**: Migrate politician-related components
3. **Debates System**: Migrate debate-related components
4. **Committees System**: Migrate committee-related components

## 🔗 **Resource Links**

- **Legacy Source**: `legacy/openparliament/` - Original Django implementation
- **Organized Legacy**: `services/web-ui/src/legacy-migration/` - All code copied and organized
- **ETL Legacy**: `services/etl/legacy-*/` - Scraping and data processing code
- **Current APIs**: `services/api-gateway/` - Working FastAPI endpoints
- **Database**: `db/openparliament.public.sql` - 6GB production data

## 🎯 **Success Criteria**

### **Phase 2: UI Migration**
- [ ] All legacy templates copied and organized
- [ ] Component mapping completed
- [ ] Basic UI components functional
- [ ] Connected to working APIs

### **Phase 3: Data Pipeline**
- [ ] Legacy scrapers integrated with ETL
- [ ] Real-time data updates working
- [ ] Data validation and quality checks

### **Phase 4: Advanced Features**
- [ ] User authentication system
- [ ] Email alert system
- [ ] AI processing pipeline

This comprehensive mapping provides the foundation for systematic migration of all OpenParliament.ca functionality, following our fundamental rule of copying and adapting rather than reinventing.
