# OpenMetadata Service for OpenPolicy Platform

## 🎯 **Purpose**

This service provides comprehensive **data lineage tracking** for the entire OpenPolicy platform, mapping every data point, nomenclature, and transformation from source databases through APIs to the final user interface.

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Source DBs    │───▶│  OpenMetadata    │───▶│  Data Lineage   │
│                 │    │     Server       │    │     UI          │
│ • bills_bill    │    │                  │    │                 │
│ • core_politician│   │ • Data Discovery │    │ • Lineage Maps  │
│ • core_member   │    │ • Schema Mapping │    │ • Data Quality  │
│ • core_party    │    │ • Flow Tracking  │    │ • Impact Analysis│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Gateway   │    │   Airflow        │    │   Monitoring    │
│                 │    │   Ingestion      │    │                 │
│ • /api/v1/bills│    │ • ETL Workflows  │    │ • Data Freshness│
│ • /api/v1/members│   │ • Data Quality   │    │ • Completeness  │
│ • Transformations│   │ • Lineage Updates│    │ • Performance   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 **Quick Start**

### 1. **Prerequisites**
- Docker and Docker Compose running
- Main OpenPolicy platform started (`mergev2_default` network exists)
- PostgreSQL database accessible

### 2. **Start the Service**
```bash
cd services/openmetadata
./start-openmetadata.sh
```

### 3. **Access the Interfaces**
- **OpenMetadata UI**: http://localhost:8585
  - Username: `admin@open-metadata.org`
  - Password: `admin`
- **Airflow UI**: http://localhost:8080
  - Username: `admin`
  - Password: `admin`

## 📊 **Data Lineage Coverage**

### **Complete Data Flow Mapping**

#### **Bills Data Lineage**
```
public.bills_bill (5,603 records)
         │
         ▼
   API Gateway Transformation
         │
         ▼
   /api/v1/bills/ endpoint
         │
         ▼
   Web UI Display
```

**Field Mappings:**
- `bills_bill.number` → `bill_number`
- `bills_bill.name_en` → `title`
- `bills_bill.status_code` → `status`
- `bills_bill.session_id` → `session_name`
- `bills_bill.privatemember` → `privatemember` (boolean)
- `bills_bill.law` → `law` (boolean)

#### **Members Data Lineage**
```
core_politician + core_electedmember + core_party
                    │
                    ▼
              API Gateway Joins
                    │
                    ▼
            /api/v1/members/ endpoint
                    │
                    ▼
              Web UI Member Lists
```

**Field Mappings:**
- `core_politician.name_given + name_family` → `full_name`
- `core_party.name_en` → `party_name`
- `core_electedmember.riding.name_en` → `constituency`

#### **Sessions Data Lineage**
```
core_session (Parliamentary sessions)
         │
         ▼
   Session Management
         │
         ▼
   Bill and Member Context
```

### **API Endpoint Tracking**
- `/api/v1/bills/` - Bills listing with pagination
- `/api/v1/bills/{id}/` - Single bill details
- `/api/v1/members/` - Members listing
- `/api/v1/committees/` - Committee information
- `/api/v1/votes/` - Voting records

## 🔧 **Configuration**

### **Database Connections**
- **Main DB**: `mergev2-db-1:5432/openpolicy`
- **OpenMetadata DB**: `mergev2-db-1:5432/openmetadata`
- **Airflow DB**: `mergev2-db-1:5432/airflow`

### **Data Quality Rules**
- All bills must have bill numbers and titles
- All members must have complete names
- Session IDs follow XX-X pattern
- Data freshness within 24 hours
- 95% data completeness threshold

### **Monitoring Metrics**
- **Data Freshness**: Parliamentary data recency
- **Data Completeness**: Required field population
- **API Performance**: Response time tracking
- **Transformation Success**: ETL workflow status

## 📁 **File Structure**

```
services/openmetadata/
├── docker-compose-custom.yml      # Custom Docker setup
├── data-lineage-config.yml        # Complete lineage configuration
├── start-openmetadata.sh          # Startup script
├── README.md                      # This file
├── docker-compose.yml             # PostgreSQL version (original)
└── docker-compose-mysql.yml       # MySQL version (original)
```

## 🎛️ **Management Commands**

### **Start Services**
```bash
docker-compose -f docker-compose-custom.yml up -d
```

### **Stop Services**
```bash
docker-compose -f docker-compose-custom.yml down
```

### **View Logs**
```bash
docker-compose -f docker-compose-custom.yml logs -f
```

### **Restart Services**
```bash
docker-compose -f docker-compose-custom.yml restart
```

## 🔍 **Data Discovery Features**

### **Automatic Discovery**
- Database schema detection
- Table relationship mapping
- Column type identification
- Foreign key discovery

### **Manual Configuration**
- Custom data source definitions
- Transformation rule specification
- Quality metric configuration
- Alert threshold setting

## 📈 **Benefits**

1. **Complete Visibility**: See every data point's journey
2. **Impact Analysis**: Understand data dependencies
3. **Quality Monitoring**: Track data health metrics
4. **Compliance**: Document data lineage for regulations
5. **Debugging**: Quickly identify data flow issues
6. **Documentation**: Auto-generated data dictionaries

## 🔗 **Integration Points**

- **ETL Service**: Data extraction workflows
- **API Gateway**: Endpoint monitoring
- **Web UI**: Frontend data consumption
- **Admin Dashboard**: Administrative oversight
- **Database**: Direct schema access

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Network Error**: Ensure `mergev2_default` network exists
2. **Port Conflicts**: Check if ports 8585 or 8080 are in use
3. **Database Connection**: Verify PostgreSQL is accessible
4. **Service Startup**: Wait 30 seconds for full initialization

### **Logs Location**
```bash
# OpenMetadata Server
docker logs mergev2-openmetadata-server

# Airflow Ingestion
docker logs mergev2-openmetadata-ingestion
```

## 📚 **Next Steps**

1. **Configure Data Sources**: Use the lineage config to set up sources
2. **Set Up Ingestion**: Create Airflow DAGs for data monitoring
3. **Define Quality Rules**: Configure validation and alerting
4. **Monitor Performance**: Track data flow metrics
5. **Generate Reports**: Create lineage documentation

## 🌟 **Advanced Features**

- **Real-time Lineage**: Live data flow tracking
- **Impact Analysis**: Change impact assessment
- **Data Governance**: Policy enforcement
- **Collaboration**: Team-based data management
- **API Integration**: REST API for automation

---

**🎯 Goal**: Complete visibility into every data point, transformation, and flow in the OpenPolicy platform for comprehensive data governance and lineage tracking.
