# Represent Integration - OpenParliament.ca V2

## Overview

This document describes the integration of the **Represent Canada** platform into OpenParliament.ca V2. Represent provides comprehensive electoral district boundaries, representative data, and postal code concordances for all levels of government in Canada.

## What is Represent?

Represent is the open database of Canadian elected officials and electoral districts, providing:
- **Electoral Boundaries**: Geographic boundaries for federal, provincial, and municipal districts
- **Representatives**: Current and historical data for MPs, MLAs, and municipal officials
- **Postal Code Concordances**: Mapping between postal codes and electoral districts
- **Free API**: REST API with 60 requests/minute rate limit

## Integration Status

### ✅ **Completed**
1. **Legacy Codebase**: Copied `represent-canada` and `represent-canada-data` repositories to `legacy/` directory
2. **Backend API**: Existing Represent API integration in FastAPI gateway (`/api/v1/represent/`)
3. **Frontend Pages**: Complete Represent section with proper hierarchy
4. **Navigation**: Added Represent to main site navigation

### 🔄 **In Progress**
1. **Data Schema**: Integrating Represent data models with existing OpenParliament schema
2. **Enhanced API**: Expanding Represent endpoints for better integration
3. **Interactive Features**: Building map-based district exploration tools

### 📋 **Planned**
1. **Data Synchronization**: Regular updates from Represent data sources
2. **Advanced Mapping**: Interactive electoral district maps
3. **Mobile Optimization**: Responsive design for mobile devices

## Architecture

### Directory Structure
```
legacy/
├── represent-canada/          # Main Represent Django application
│   ├── finder/               # Core application views and templates
│   ├── represent/            # Django project settings
│   └── requirements.txt      # Python dependencies
└── represent-canada-data/    # Electoral data repository
    ├── boundaries/           # Shapefiles and geographic data
    ├── representatives/      # Elected official data
    └── postcodes/           # Postal code concordances

services/
├── api-gateway/              # FastAPI backend with Represent endpoints
│   └── app/api/v1/represent.py
└── web-ui/                   # Next.js frontend with Represent pages
    └── src/app/represent/
        ├── page.tsx          # Main Represent page
        ├── api/page.tsx      # API documentation
        ├── data/page.tsx     # Data downloads
        └── demo/page.tsx     # Interactive demo
```

### API Endpoints

#### Existing Represent API (FastAPI)
- `GET /api/v1/represent/boundary-sets` - Available electoral boundary sets
- `GET /api/v1/represent/boundaries/{slug}` - Boundaries for a specific set
- `GET /api/v1/represent/representatives/{slug}` - Representatives in a set
- `GET /api/v1/represent/postal-code/{code}` - Lookup by postal code
- `GET /api/v1/represent/geocode` - Lookup by coordinates
- `GET /api/v1/represent/health` - API health check

#### External Represent API (OpenNorth)
- Base URL: `https://represent.opennorth.ca`
- Rate Limit: 60 requests/minute
- Format: JSON with pagination support

## Frontend Pages

### 1. Main Represent Page (`/represent`)
- **Purpose**: Overview and introduction to Represent services
- **Features**: 
  - Hero section with call-to-action buttons
  - Benefits and use cases
  - User testimonials and examples
  - Quick action links

### 2. API Documentation (`/represent/api`)
- **Purpose**: Comprehensive API reference and examples
- **Features**:
  - Endpoint documentation with examples
  - Request/response schemas
  - Rate limiting information
  - Integration libraries and tools
  - Quick start guide

### 3. Data Downloads (`/represent/data`)
- **Purpose**: Information about available data sets and download options
- **Features**:
  - Data set descriptions
  - Format options (Shapefile, GeoJSON, CSV, JSON)
  - Data quality and update frequency
  - Usage examples and use cases
  - GitHub repository links

            ### 4. Interactive Demo (`/represent/demo`)
            - **Purpose**: Showcase interactive features and tools
            - **Features**:
              - Postal code lookup demo
              - Sample results and data
              - Interactive feature previews
              - Use case examples
              - Getting started guide

            ### 5. Government Data Contribution (`/represent/government`)
            - **Purpose**: Guide municipalities on contributing elected official data
            - **Features**:
              - CSV schema documentation
              - Required vs. optional field explanations
              - Step-by-step contribution process
              - Municipal adoption showcase
              - CSV template download
              - **Source**: Adapted from `legacy/represent-canada/finder/templates/government.html`

            ### 6. Privacy Policy (`/represent/privacy`)
            - **Purpose**: Privacy policy and data handling information
            - **Features**:
              - Information collection practices
              - Data security measures
              - Policy change notifications
              - Contact information
              - **Source**: Adapted from `legacy/represent-canada/finder/templates/privacy.html`

## Data Models

### Core Entities

#### Boundary
```typescript
interface Boundary {
  name: string;                    // District name
  boundary_set_name: string;       // Set name (e.g., "federal-electoral-districts")
  external_id: string;             // External identifier
  centroid_lat?: number;           // Centroid latitude
  centroid_lon?: number;           // Centroid longitude
  area?: number;                   // Area in square kilometers
}
```

#### Representative
```typescript
interface Representative {
  name: string;                    // Full name
  first_name?: string;             // First name
  last_name?: string;              // Last name
  party_name?: string;             // Political party
  email?: string;                  // Email address
  photo_url?: string;              // Photo URL
  elected_office: string;          // Office (e.g., "MP", "MLA")
  district_name: string;           // District/riding name
  url?: string;                    // Personal website
}
```

#### Postal Code Lookup
```typescript
interface PostalCodeLookup {
  postal_code: string;             // The postal code
  boundaries_centroid: Boundary[]; // Boundaries containing centroid
  boundaries_concordance: Boundary[]; // Boundaries linked by postal code
  representatives_centroid: Representative[]; // Representatives for centroid
  representatives_concordance: Representative[]; // Representatives for concordance
}
```

## Integration Points

### 1. **OpenParliament MPs Integration**
- Enhance existing MP profiles with electoral district boundaries
- Add postal code lookup functionality
- Integrate with existing voting records and debates

### 2. **Search Enhancement**
- Add electoral district search to main search functionality
- Include representative search across all levels of government
- Geographic search by coordinates or postal code

### 3. **Data Visualization**
- Interactive maps showing electoral districts
- Boundary visualization for bills and votes
- Geographic analysis of parliamentary activity

### 4. **API Unification**
- Single API gateway for all electoral data
- Consistent response formats
- Unified authentication and rate limiting

## Data Sources

### Federal Level
- **Elections Canada**: Federal electoral district boundaries
- **House of Commons**: Current MP information
- **Parliament of Canada**: Parliamentary session data

### Provincial Level
- **Provincial Elections Offices**: Provincial electoral boundaries
- **Legislative Assemblies**: MLA and MPP information
- **Provincial Governments**: Official government data

### Municipal Level
- **Municipal Governments**: City ward boundaries
- **Regional Districts**: Regional electoral areas
- **Local Elections**: Municipal representative data

## Development Guidelines

### 1. **Follow FUNDAMENTAL RULE**
- Always check legacy code first before implementing new features
- Adapt existing Represent functionality rather than recreating
- Preserve proven data collection and processing logic

### 2. **Data Consistency**
- Maintain consistent data models across the platform
- Use standardized geographic coordinate systems
- Implement proper error handling for external API calls

### 3. **Performance Considerations**
- Cache frequently accessed data (boundaries, representatives)
- Implement efficient geographic queries
- Use pagination for large data sets

### 4. **User Experience**
- Provide clear feedback for postal code lookups
- Include helpful error messages for invalid inputs
- Ensure responsive design for all devices

## Testing Strategy

### 1. **API Testing**
- Test all Represent endpoints with various inputs
- Verify rate limiting and error handling
- Test with real postal codes and coordinates

### 2. **Frontend Testing**
- Test all Represent pages for responsiveness
- Verify navigation and routing
- Test interactive features and forms

### 3. **Integration Testing**
- Test Represent data integration with existing features
- Verify data consistency across the platform
- Test search and filtering functionality

## Deployment Considerations

### 1. **Data Updates**
- Regular synchronization with Represent data sources
- Automated updates for electoral boundaries
- Version control for data changes

### 2. **API Management**
- Monitor Represent API usage and rate limits
- Implement fallback mechanisms for API failures
- Cache frequently requested data

### 3. **Performance Monitoring**
- Track API response times
- Monitor geographic query performance
- Optimize data loading and caching

## Future Enhancements

### 1. **Advanced Mapping**
- Interactive electoral district maps
- Geographic visualization of voting patterns
- Boundary change tracking over time

### 2. **Enhanced Search**
- Geographic search by drawing boundaries
- Multi-level government search
- Advanced filtering and sorting

### 3. **Data Analytics**
- Electoral district comparison tools
- Representative activity analysis
- Geographic voting pattern analysis

### 4. **Mobile Applications**
- Native mobile apps for electoral lookup
- Offline data access
- Push notifications for updates

## Resources

### Documentation
- [Represent API Documentation](https://represent.opennorth.ca/api/)
- [GitHub Repository](https://github.com/opennorth/represent-canada)
- [Data Repository](https://github.com/opennorth/represent-canada-data)

### Support
- **Email**: represent@opennorth.ca
- **GitHub Issues**: Report bugs and feature requests
- **Community**: OpenNorth community forums

### Integration Examples
- [The Tyee BC Election Guide](https://thetyee.ca/election-guide-2017/)
- [Dogwood Initiative Campaign Tools](https://dogwoodbc.ca/)
- [Various nonprofit and union applications](https://represent.opennorth.ca/)

## Conclusion

The Represent integration significantly enhances OpenParliament.ca V2 by providing comprehensive electoral data and tools. This integration follows the FUNDAMENTAL RULE by leveraging existing, proven systems while modernizing the user experience and API capabilities.

The platform now offers:
- Complete electoral district coverage across Canada
- Multi-level government representative information
- Geographic and postal code lookup capabilities
- Comprehensive API for developers
- Interactive tools for citizens and organizations

This integration positions OpenParliament.ca V2 as the premier platform for Canadian parliamentary and electoral information, serving the needs of citizens, researchers, journalists, and advocacy organizations across the country.
