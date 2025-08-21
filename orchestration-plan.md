# OpenPolicy Platform - Comprehensive Orchestration Plan

## 🎯 **Overview**
This document outlines the orchestration strategy for deploying and managing the OpenPolicy platform with OpenMetadata integration.

## 🏗️ **Architecture Components**

### **Core Services (Phase 1 - Foundation)**
1. **PostgreSQL Database** (`mergev2-db-1`)
   - Port: 5432
   - Purpose: Primary data storage
   - Dependencies: None
   - Health Check: Database connectivity

2. **Redis Cache** (`mergev2-redis-1`)
   - Port: 6379
   - Purpose: Session and cache storage
   - Dependencies: None
   - Health Check: Redis ping

3. **API Gateway** (`mergev2-api-gateway-1`)
   - Port: 8080
   - Purpose: Data API and business logic
   - Dependencies: PostgreSQL, Redis
   - Health Check: `/health` endpoint

4. **User Service** (`mergev2-user-service-1`)
   - Port: 8082
   - Purpose: User authentication and management
   - Dependencies: PostgreSQL, Redis
   - Health Check: `/health` endpoint

### **Data Services (Phase 2 - Data Layer)**
5. **ETL Service** (`mergev2-etl-1`)
   - Port: 8083
   - Purpose: Data extraction and transformation
   - Dependencies: PostgreSQL, Redis
   - Health Check: `/health` endpoint

6. **Legacy Scrapers**
   - Purpose: Municipal data extraction
   - Dependencies: ETL Service
   - Health Check: Scraper status endpoints

### **Metadata & Governance (Phase 3 - Intelligence)**
7. **OpenMetadata Server** (`mergev2-openmetadata-server`)
   - Port: 8585
   - Purpose: Data lineage and governance
   - Dependencies: PostgreSQL (openmetadata schema)
   - Health Check: `/health` endpoint

8. **Elasticsearch** (`mergev2-elasticsearch`)
   - Ports: 9200, 9300
   - Purpose: Metadata indexing and search
   - Dependencies: None
   - Health Check: `/cluster/health` endpoint

9. **OpenMetadata Ingestion** (`mergev2-openmetadata-ingestion`)
   - Port: 8083 (Airflow)
   - Purpose: Metadata ingestion workflows
   - Dependencies: PostgreSQL (airflow schema), OpenMetadata Server
   - Health Check: Airflow webserver status

### **User Interfaces (Phase 4 - Presentation)**
10. **Admin UI** (`mergev2-admin-ui-1`)
    - Port: 3000
    - Purpose: Administrative interface
    - Dependencies: API Gateway, OpenMetadata Server
    - Health Check: Page load status

11. **Web UI** (`mergev2-web-ui-1`)
    - Port: 3001
    - Purpose: Public user interface
    - Dependencies: API Gateway
    - Health Check: Page load status

## 🔄 **Deployment Phases**

### **Phase 1: Foundation (5 minutes)**
```bash
# Start core infrastructure
docker-compose up -d db redis
# Wait for health checks
docker-compose up -d api-gateway user-service
```

### **Phase 2: Data Layer (10 minutes)**
```bash
# Start ETL and scrapers
docker-compose up -d etl
# Initialize data schemas
docker-compose exec db psql -U openpolicy -d openpolicy -f /docker-entrypoint-initdb.d/init.sql
```

### **Phase 3: Metadata Layer (15 minutes)**
```bash
# Start OpenMetadata services
docker-compose --profile openmetadata up -d
# Wait for OpenMetadata to be ready
# Initialize metadata schemas
docker-compose exec db psql -U openpolicy -d openmetadata -f /docker-entrypoint-initdb.d/openmetadata-init.sql
```

### **Phase 4: User Interfaces (5 minutes)**
```bash
# Start UI services
docker-compose up -d admin-ui web-ui
# Verify all services are healthy
```

## 🚦 **Health Check Strategy**

### **Service Health Checks**
```yaml
health_checks:
  database:
    endpoint: "postgresql://openpolicy:openpolicy@db:5432/openpolicy"
    timeout: 30s
    retries: 3
    
  redis:
    endpoint: "redis://redis:6379"
    timeout: 10s
    retries: 3
    
  api_gateway:
    endpoint: "http://api-gateway:8080/health"
    timeout: 15s
    retries: 3
    
  openmetadata:
    endpoint: "http://openmetadata-server:8585/health"
    timeout: 30s
    retries: 5
```

### **Dependency Chain**
```
db → redis → api-gateway → user-service
db → etl → scrapers
db → openmetadata-server → elasticsearch → ingestion
api-gateway → admin-ui
api-gateway → web-ui
openmetadata-server → admin-ui
```

## 🔧 **MCP Integration Strategy**

### **Container-Based MCP Server**
1. **Install MCP inside OpenMetadata container**
2. **Expose MCP endpoints via container network**
3. **Configure Cursor to connect to container MCP**

### **MCP Configuration Files**
1. **`~/.cursor/mcp.json`** - Global Cursor MCP config
2. **`project/.cursor/mcp.json`** - Project-specific MCP config
3. **`mcp-proxy.servers.json`** - MCP proxy configuration

### **MCP Server Implementation**
```python
# Inside OpenMetadata container
class OpenMetadataMCPServer:
    def __init__(self):
        self.openmetadata_url = "http://localhost:8585"
        self.auth_token = "admin"
    
    def get_data_lineage(self, entity_id):
        # Query OpenMetadata API
        pass
    
    def search_entities(self, query):
        # Search OpenMetadata
        pass
```

## 📊 **Monitoring & Alerting**

### **Key Metrics**
- Service uptime and response times
- Database connection pool status
- API endpoint performance
- Data ingestion success rates
- Metadata freshness

### **Alerting Rules**
- Service down for >5 minutes
- Database response time >2 seconds
- API response time >1 second
- Data ingestion failure rate >5%

## 🚨 **Troubleshooting Guide**

### **Common Issues**
1. **Ingestion Service Restarting**
   - Check database connectivity
   - Verify Airflow database initialization
   - Check environment variables

2. **MCP Connection Issues**
   - Verify container network connectivity
   - Check MCP server logs
   - Validate Cursor configuration

3. **Service Dependencies**
   - Ensure proper startup order
   - Check health check endpoints
   - Verify network connectivity

## 🎯 **Next Steps**

### **Immediate Actions**
1. ✅ Fix OpenMetadata ingestion service
2. ✅ Install MCP server inside container
3. ✅ Configure Cursor MCP integration
4. ✅ Test complete data lineage flow

### **Short Term (Next 24 hours)**
1. 🚧 Implement health check automation
2. 🚧 Create deployment scripts
3. 🚧 Set up monitoring dashboards
4. 🚧 Test end-to-end workflows

### **Medium Term (Next week)**
1. 📋 Production deployment preparation
2. 📋 Performance optimization
3. 📋 Security hardening
4. 📋 Documentation completion

## 🔗 **Useful Commands**

### **Service Management**
```bash
# Start all services
docker-compose up -d

# Start with OpenMetadata profile
docker-compose --profile openmetadata up -d

# Check service status
docker-compose ps

# View service logs
docker-compose logs -f [service-name]
```

### **Health Checks**
```bash
# Database health
docker-compose exec db pg_isready -U openpolicy

# API Gateway health
curl http://localhost:8080/health

# OpenMetadata health
curl http://localhost:8585/health

# Elasticsearch health
curl http://localhost:9200/_cluster/health
```

### **MCP Testing**
```bash
# Test MCP server connection
python mcp-openmetadata-server.py

# Test data lineage query
curl -H "Authorization: Bearer admin" \
     http://localhost:8585/api/v1/tables
```
