# OpenParliament.ca V2 Data Pipeline Documentation

## 🎯 **Overview**

This document provides comprehensive documentation of the OpenParliament.ca V2 data pipeline, following the **FUNDAMENTAL RULE: NEVER REINVENT THE WHEEL**. All data collection uses existing, proven legacy OpenParliament importers and adapters.

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Legacy Data   │    │   Legacy Data    │    │   Database      │    │   Frontend      │
│   Sources       │───▶│   Adapters       │───▶│   Schema        │───▶│   Display       │
└─────────────────┘    └──────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 **Data Sources & Scrapers Mapping**

### 1. **Represent API Scraper** (`services/etl/app/extractors/legacy_adapters.py`)

**Source**: `https://represent.opennorth.ca/api/`
**Data Type**: Member of Parliament (MP) information
**Collection Method**: REST API calls
**Frequency**: On-demand via `make collect-data`

**Data Collected**:
- MP names, parties, contact information
- Electoral district information
- Office locations and contact details
- Photo URLs and personal websites

**Runtime**: ~2-3 seconds for 343 MPs
**Output**: JSON data with MP records

### 2. **OurCommons.ca XML Scraper** (`services/etl/app/extractors/legacy_adapters.py`)

**Source**: `https://www.ourcommons.ca/Content/Parliamentarians/`
**Data Type**: MP profiles, bills, votes
**Collection Method**: XML parsing via `lxml`
**Frequency**: On-demand via `make collect-data`

**Data Collected**:
- MP profiles and contact information
- Bill details and legislative status
- Voting records and individual MP ballots
- Parliamentary session information

**Runtime**: ~3-5 seconds for 343 MPs + bills + votes
**Output**: XML parsed to JSON format

### 3. **LEGISinfo API Scraper** (`services/etl/app/extractors/legacy_adapters.py`)

**Source**: `https://www.parl.ca/legisinfo/`
**Data Type**: Bill information and legislative details
**Collection Method**: REST API calls
**Frequency**: On-demand via `make collect-data`

**Data Collected**:
- Bill numbers and titles
- Legislative status and progress
- Sponsor information
- Session and parliament details

**Runtime**: ~2-3 seconds for 412 bills
**Output**: JSON data with bill records

## 🔄 **Data Flow & Processing Pipeline**

### **Phase 1: Data Collection** (`make collect-data`)

```bash
# Run data collection
cd services/etl
make collect-data
```

**Process**:
1. **LegacyDataCollectionTask** orchestrates collection
2. **Represent API** → 343 MPs collected
3. **OurCommons.ca** → 343 MPs + bills + votes collected
4. **LEGISinfo API** → 412 bills collected
5. **Data deduplication** and merging
6. **Output**: `data/legacy_adapted/legacy_collected_YYYYMMDD_HHMMSS.json`

**Runtime**: **Total: ~7-11 seconds**
- Represent API: 2-3 seconds
- OurCommons.ca: 3-5 seconds  
- LEGISinfo: 2-3 seconds

### **Phase 2: Data Ingestion** (`make ingest-data`)

```bash
# Run data ingestion
cd services/etl
make ingest-data
```

**Process**:
1. **LegacyDataIngester** loads JSON data
2. **Database connection** to PostgreSQL
3. **Schema validation** against database
4. **Data insertion/update** with conflict resolution
5. **Relationship creation** (MPs → Offices, Votes → Ballots)

**Runtime**: **Total: ~10-20 seconds**
- Database connection: 1-2 seconds
- MP ingestion: 5-8 seconds
- Bill ingestion: 3-5 seconds
- Vote ingestion: 2-5 seconds

### **Phase 3: Full Pipeline** (`make full-pipeline`)

```bash
# Run complete pipeline
cd services/etl
make full-pipeline
```

**Process**: Combines Phase 1 + Phase 2
**Runtime**: **Total: ~17-31 seconds**

## 🗄️ **Database Schema Mapping**

### **Core Tables & Data Sources**

| Table | Data Source | Records | Key Fields | Legacy Source |
|-------|-------------|---------|------------|---------------|
| `members` | Represent API + OurCommons | 686 MPs | name, party, email | represent_api, ourcommons |
| `mp_offices` | Represent API + OurCommons | ~1372 offices | mp_id, type, tel, fax | represent_api, ourcommons |
| `bills` | LEGISinfo + OurCommons | 412 bills | number, session, title | legisinfo, ourcommons |
| `votes` | OurCommons XML | 34 votes | parliament, session, number | ourcommons |
| `vote_ballots` | OurCommons XML | ~23,324 ballots | vote_id, member_id, ballot | ourcommons |

### **Extended Schema Fields**

#### **Members Table Extensions**
```sql
-- New columns for legacy data
legacy_source VARCHAR(50),        -- 'represent_api' or 'ourcommons'
extracted_at TIMESTAMP,           -- When data was collected
preferred_languages TEXT[],       -- Array of language preferences
photo_url VARCHAR(500),          -- MP photo URL
personal_url VARCHAR(500),        -- Personal website URL
```

#### **Bills Table Extensions**
```sql
-- New columns for legacy data
legisinfo_id VARCHAR(50),         -- LEGISinfo identifier
parliament_number INTEGER,        -- Parliament number
session_number INTEGER,           -- Session number
bill_type VARCHAR(20),            -- Government/Private bill
chamber VARCHAR(20),              -- House/Senate
sponsor_title VARCHAR(200),       -- Sponsor information
```

#### **Votes Table Extensions**
```sql
-- New columns for legacy data
parliament_number INTEGER,        -- Parliament number
session_number INTEGER,           -- Session number
vote_number INTEGER,              -- Vote sequence number
vote_type VARCHAR(50),            -- Type of vote
result VARCHAR(20),               -- Vote result
yea_count INTEGER,                -- Yes votes
nay_count INTEGER,                -- No votes
paired_count INTEGER,             -- Paired votes
```

## 🚀 **Running & Maintenance Procedures**

### **Daily Operations**

#### **1. Data Collection**
```bash
cd services/etl
source venv/bin/activate

# Collect fresh data
make collect-data

# Expected output:
# ✅ Data collection completed successfully!
# 📁 Check the 'data/legacy_adapted/' directory for collected data
# 📊 Collected: 686 MPs, 412 bills, 34 votes
```

#### **2. Data Ingestion**
```bash
# Ingest collected data into database
make ingest-data

# Expected output:
# 🎉 Legacy Data Ingestion Complete!
# 📊 Final Results:
#    👥 MPs: 686 inserted, 0 updated
#    📄 Bills: 412 inserted, 0 updated
#    🗳️ Votes: 34 inserted, 0 updated
#    🏢 Offices: 1372 inserted
#    ☑️ Ballots: 23324 inserted
```

#### **3. Full Pipeline**
```bash
# Run complete ETL pipeline
make full-pipeline

# This runs both collection and ingestion
# Total runtime: ~17-31 seconds
```

### **Weekly Maintenance**

#### **1. Data Quality Checks**
```bash
# Check data collection statistics
ls -lh data/legacy_adapted/
# Should see files ~536KB with recent timestamps

# Verify database record counts
psql $DATABASE_URL -c "SELECT COUNT(*) FROM members;"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM bills;"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM votes;"
```

#### **2. Error Monitoring**
```bash
# Check for ingestion errors
psql $DATABASE_URL -c "SELECT * FROM data_collection_runs ORDER BY started_at DESC LIMIT 5;"

# Check for failed runs
psql $DATABASE_URL -c "SELECT * FROM data_collection_runs WHERE status = 'failed';"
```

### **Monthly Maintenance**

#### **1. Schema Updates**
```bash
# Apply any new database migrations
cd services/api-gateway
alembic upgrade head

# Check migration status
alembic current
alembic history
```

#### **2. Performance Monitoring**
```bash
# Check database performance
psql $DATABASE_URL -c "SELECT schemaname, tablename, n_tup_ins, n_tup_upd FROM pg_stat_user_tables;"

# Check index usage
psql $DATABASE_URL -c "SELECT schemaname, tablename, indexrelname, idx_scan FROM pg_stat_user_indexes;"
```

## 🔧 **Troubleshooting & Debugging**

### **Common Issues**

#### **1. Data Collection Failures**
```bash
# Check network connectivity
curl -I https://represent.opennorth.ca/api/
curl -I https://www.ourcommons.ca/
curl -I https://www.parl.ca/legisinfo/

# Check API rate limits
# Represent API: 60 requests/minute
# OurCommons: No known limits
# LEGISinfo: No known limits
```

#### **2. Database Connection Issues**
```bash
# Test database connectivity
psql $DATABASE_URL -c "SELECT version();"

# Check database status
pg_isready -h localhost -p 5432
```

#### **3. Schema Mismatch Issues**
```bash
# Check if all tables exist
psql $DATABASE_URL -c "\dt"

# Check table schemas
psql $DATABASE_URL -c "\d members"
psql $DATABASE_URL -c "\d bills"
psql $DATABASE_URL -c "\d votes"
```

### **Debug Mode**

```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG

# Run with detailed output
python collect_data.py --verbose
python ingest_legacy_data.py --verbose
```

## 📈 **Performance Metrics & Monitoring**

### **Expected Performance**

| Operation | Expected Time | Success Rate | Data Volume |
|-----------|---------------|--------------|-------------|
| Data Collection | 7-11 seconds | 99%+ | 536KB JSON |
| Data Ingestion | 10-20 seconds | 99%+ | 686 MPs + 412 bills + 34 votes |
| Full Pipeline | 17-31 seconds | 99%+ | Complete dataset |

### **Monitoring Commands**

```bash
# Monitor data collection runs
watch -n 5 'psql $DATABASE_URL -c "SELECT run_type, status, started_at, mps_collected, bills_collected, votes_collected FROM data_collection_runs ORDER BY started_at DESC LIMIT 3;"'

# Monitor database growth
watch -n 30 'psql $DATABASE_URL -c "SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||\".\"||tablename)) as size FROM pg_tables WHERE schemaname = \'public\';"'
```

## 🔒 **Security & Access Control**

### **API Access**
- **Represent API**: Public, no authentication required
- **OurCommons.ca**: Public, no authentication required  
- **LEGISinfo**: Public, no authentication required

### **Database Access**
- **Connection**: PostgreSQL with connection pooling
- **Authentication**: Environment variable `DATABASE_URL`
- **Permissions**: Read/write access to public schema

## 📚 **Additional Resources**

### **Code Locations**
- **Data Collection**: `services/etl/app/extractors/legacy_adapters.py`
- **Data Ingestion**: `services/etl/app/ingestion/legacy_data_ingester.py`
- **Database Schema**: `services/api-gateway/alembic/versions/002_represent_integration_schema.py`
- **Configuration**: `services/etl/requirements.txt`, `services/etl/Makefile`

### **Legacy Sources**
- **Represent Canada**: `legacy/represent-canada/`
- **Represent Data**: `legacy/represent-canada-data/`
- **Original OpenParliament**: Referenced in legacy adapters

### **Documentation**
- **API Documentation**: `/represent/api`
- **Data Downloads**: `/represent/data`
- **Government Guide**: `/represent/government`

---

**Last Updated**: 2025-08-20
**Version**: 1.0
**Maintainer**: OpenParliament.ca V2 Team
**FUNDAMENTAL RULE**: ✅ **NEVER REINVENT THE WHEEL** - All functionality based on existing, proven legacy code
