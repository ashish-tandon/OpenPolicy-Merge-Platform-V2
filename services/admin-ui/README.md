# OpenPolicy Admin UI

A comprehensive administrative interface for the OpenPolicy platform that provides administrators with complete control over all aspects of the system.

## 🚀 **Features Delivered**

### ✅ **Core Admin Dashboard**
- **System Overview**: Real-time platform health and status
- **Key Metrics**: Representatives, bills, jurisdictions, votes counts
- **Data Source Status**: Live monitoring of all data sources
- **Recent Activity**: System events and user actions
- **Quick Actions**: Direct access to common administrative tasks

### ✅ **Data Management**
- **Government Levels**: Full CRUD operations for Federal, Provincial, Municipal levels
- **Jurisdictions**: Manage specific government jurisdictions (Coming Soon)
- **Data Sources**: Monitor data source health (Coming Soon)
- **Data Quality**: Validation rules and checks (Coming Soon)

### ✅ **ETL & Data Pipeline Management**
- **Pipeline Overview**: Real-time status of all data processing jobs
- **Job Management**: Start, pause, retry, and monitor ETL jobs
- **Data Source Monitoring**: Health checks and error tracking
- **Performance Metrics**: Processing times and record counts
- **Error Handling**: Detailed error logs and retry mechanisms

### ✅ **Advanced Navigation**
- **Responsive Sidebar**: Collapsible sections with submenus
- **Mobile Support**: Full responsive design with mobile sidebar
- **Active State Management**: Visual feedback for current page
- **Breadcrumb Navigation**: Clear path indication

## 🛠️ **Technology Stack**

- **Frontend Framework**: React 18 + TypeScript
- **Build Tool**: Vite 6.2
- **Styling**: Tailwind CSS 4.0
- **Routing**: React Router DOM 6.28
- **State Management**: Zustand 4.5
- **Data Fetching**: TanStack React Query 5.28
- **UI Components**: Headless UI + Heroicons
- **Charts & Visualization**: Recharts + Chart.js
- **Forms**: React Hook Form 7.51

## 📁 **Project Structure**

```
services/admin-ui/
├── src/
│   ├── pages/
│   │   ├── Dashboard.tsx (Main dashboard)
│   │   ├── data/
│   │   │   └── GovernmentLevels.tsx (Government levels management)
│   │   └── ETLManagement.tsx (ETL pipeline control)
│   ├── components/
│   │   └── navigation/
│   │       └── AdminNavigation.tsx (Sidebar navigation)
│   ├── App.tsx (Main app component)
│   └── main.tsx (Entry point)
├── router.tsx (Routing configuration)
├── package.json (Dependencies and scripts)
└── docs/
    └── ADMIN_UI_IMPLEMENTATION_SUMMARY.md (Complete implementation details)
```

## 🚀 **Quick Start**

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation
```bash
cd services/admin-ui
npm install
```

### Development
```bash
npm run dev
```

The admin UI will be available at `http://localhost:5173`

### Build
```bash
npm run build
```

### Linting
```bash
npm run lint
```

## 🔧 **Configuration**

### Environment Variables
Create a `.env` file in the root directory:

```env
VITE_API_BASE_URL=http://localhost:8080
VITE_ADMIN_API_KEY=your_admin_api_key
```

### API Integration
The Admin UI integrates with the OpenPolicy API Gateway:

- **Base URL**: `/api/v1/`
- **Multi-Level Government**: `/api/v1/multi-level-government/`
- **Admin Endpoints**: `/api/v1/admin/` (Coming Soon)

## 📊 **Admin Features Overview**

### 1. **Dashboard** (`/`)
- System health monitoring
- Key performance indicators
- Recent activity feed
- Quick action buttons

### 2. **Data Management** (`/data`)
- **Government Levels** (`/data/government-levels`):
  - Create, read, update, delete government levels
  - Level ordering and activation controls
  - Statistics and relationship counts

### 3. **ETL Management** (`/etl`)
- Real-time job monitoring
- Start/pause/retry job controls
- Data source health tracking
- Performance metrics

### 4. **Navigation Structure**
```
Dashboard
├── Data Management
│   ├── Government Levels
│   ├── Jurisdictions (Coming Soon)
│   ├── Data Sources (Coming Soon)
│   └── Data Quality (Coming Soon)
├── Multi-Level Government
├── Parliamentary Data
├── Representatives
├── Bills & Legislation
├── Voting Records
├── ETL & Data Pipeline
├── System Monitoring
├── User Management
└── Settings
```

## 🔐 **Authentication & Security**

- **Protected Routes**: All admin pages require authentication
- **Session Management**: Secure token-based authentication
- **Route Guards**: Automatic redirection for unauthorized access
- **Role-Based Access**: Different permission levels (Coming Soon)

## 📱 **Responsive Design**

- **Desktop**: Full sidebar navigation with expandable sections
- **Tablet**: Adaptive layout with collapsible navigation
- **Mobile**: Mobile-first design with hamburger menu

## 🎨 **Design System**

- **Color Palette**: Consistent with OpenPolicy brand
- **Typography**: Clear hierarchy and readability
- **Components**: Reusable UI components
- **Icons**: Heroicons for consistent iconography

## 🚧 **Coming Soon Features**

### **Immediate Priorities**
- Parliamentary Data Management (Debates, Committees, Sessions)
- Representatives Management (Profiles, Activity Tracking)
- Bills Management (Legislation, Status Tracking)
- Voting Records (Vote Analysis, Roll Calls)

### **Advanced Features**
- Data Visualization (Charts, Analytics)
- Workflow Automation (Automated Pipelines)
- Advanced Search (Full-text Search)
- API Management (Developer Portal)

## 🧪 **Testing**

### Unit Tests
```bash
npm test
```

### Integration Tests
```bash
npm run test:integration
```

### E2E Tests
```bash
npm run test:e2e
```

## 📈 **Performance**

- **Lazy Loading**: Components loaded on demand
- **Efficient Polling**: Smart update intervals
- **Caching**: Client-side data caching
- **Optimization**: Bundle splitting and tree shaking

## 🔍 **Monitoring & Analytics**

- **Real-Time Updates**: Live data and status monitoring
- **Performance Metrics**: Response times and throughput
- **Error Tracking**: Comprehensive error logging
- **User Analytics**: Admin action tracking

## 🤝 **Contributing**

1. Follow the existing code style and patterns
2. Add TypeScript types for all new features
3. Include unit tests for new components
4. Update documentation for new features
5. Follow the FUNDAMENTAL RULE: NEVER REINVENT THE WHEEL

## 📚 **Documentation**

- **Implementation Summary**: `docs/ADMIN_UI_IMPLEMENTATION_SUMMARY.md`
- **API Reference**: Integration with OpenPolicy APIs
- **Component Library**: Reusable UI components
- **Design Guidelines**: Visual and interaction patterns

## 🆘 **Support**

For issues and questions:
1. Check the documentation
2. Review the implementation summary
3. Check existing issues
4. Create a new issue with detailed information

## 🎯 **Success Metrics**

### **Functionality Delivered** ✅
- Complete Dashboard with system overview
- Government Levels Management with full CRUD
- ETL Pipeline Control with real-time monitoring
- Responsive Navigation with mobile support
- Authentication System with protected routes

### **Technical Excellence** ✅
- Modern React with TypeScript
- Comprehensive type safety
- Optimized performance
- Accessibility compliance
- Responsive design

### **User Experience** ✅
- Intuitive interface design
- Real-time data updates
- Graceful error handling
- Clear visual feedback
- Efficient task completion

---

**Built with ❤️ for the OpenPolicy platform**

*Following FUNDAMENTAL RULE: NEVER REINVENT THE WHEEL*
