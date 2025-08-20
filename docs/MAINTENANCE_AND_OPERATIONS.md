# OpenParliament.ca V2 Maintenance & Operations Guide

## 🎯 **Purpose**

This document provides comprehensive step-by-step procedures for running, maintaining, and troubleshooting the OpenParliament.ca V2 data pipeline. All procedures follow the **FUNDAMENTAL RULE: NEVER REINVENT THE WHEEL**.

## 🚀 **Quick Start Commands**

### **Essential Commands**
```bash
# Navigate to ETL service
cd services/etl

# Activate virtual environment
source venv/bin/activate

# Check available commands
make help

# Run complete pipeline (collection + ingestion)
make full-pipeline

# Check status
make status
```

## 📋 **Daily Operations**

### **1. Morning Health Check**

```bash
# 1. Check system status
cd services/etl
source venv/bin/activate

# 2. Verify data sources are accessible
curl -I https://represent.opennorth.ca/api/
curl -I https://www.ourcommons.ca/
curl -I https://www.parl.ca/legisinfo/

# 3. Check last data collection
ls -lh data/legacy_adapted/
# Should see files with recent timestamps

# 4. Verify database connectivity
psql $DATABASE_URL -c "SELECT version();"

# 5. Check record counts
psql $DATABASE_URL -c "SELECT COUNT(*) FROM members;"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM bills;"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM votes;"
```

**Expected Results**:
- ✅ All APIs responding (HTTP 200)
- ✅ Data files present and recent (< 24 hours old)
- ✅ Database connection successful
- ✅ Record counts: ~686 MPs, ~412 bills, ~34 votes

### **2. Data Collection (if needed)**

```bash
# Run data collection
make collect-data

# Expected output:
# 🚀 Starting OpenParliament.ca V2 data collection...
# 📋 Following FUNDAMENTAL RULE: Using legacy OpenParliament importers
# ✅ Data collection completed successfully!
# 📊 Collected: 686 MPs, 412 bills, 34 votes
```

**Runtime**: 7-11 seconds
**Output**: `data/legacy_adapted/legacy_collected_YYYYMMDD_HHMMSS.json`

### **3. Data Ingestion (if needed)**

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

**Runtime**: 10-20 seconds
**Database Impact**: ~25,828 records inserted/updated

## 📅 **Weekly Operations**

### **1. Data Quality Assessment**

```bash
# 1. Check data source distribution
psql $DATABASE_URL -c "
SELECT 
    legacy_source, 
    COUNT(*) as record_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM members 
GROUP BY legacy_source;
"

# 2. Verify relationship integrity
psql $DATABASE_URL -c "
SELECT 
    'MPs with Offices' as relationship,
    COUNT(DISTINCT m.id) as mp_count,
    COUNT(mo.id) as office_count
FROM members m
LEFT JOIN mp_offices mo ON m.id = mo.mp_id
GROUP BY m.id
HAVING COUNT(mo.id) > 0;
"

# 3. Check for data anomalies
psql $DATABASE_URL -c "
SELECT 
    'MPs without email' as issue,
    COUNT(*) as count
FROM members 
WHERE email IS NULL OR email = '';
"
```

**Expected Results**:
- ✅ Data source distribution: ~50% represent_api, ~50% ourcommons
- ✅ All MPs have at least 2 offices (legislature + constituency)
- ✅ < 5% MPs missing email addresses

### **2. Performance Monitoring**

```bash
# 1. Check collection run statistics
psql $DATABASE_URL -c "
SELECT 
    run_type,
    COUNT(*) as total_runs,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as successful_runs,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_runs,
    ROUND(AVG(EXTRACT(EPOCH FROM (completed_at - started_at))), 2) as avg_runtime_seconds
FROM data_collection_runs 
WHERE started_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY run_type;
"

# 2. Monitor database performance
psql $DATABASE_URL -c "
SELECT 
    schemaname,
    tablename,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    n_live_tup as live_tuples
FROM pg_stat_user_tables 
WHERE schemaname = 'public'
ORDER BY n_live_tup DESC;
"
```

### **3. Error Analysis**

```bash
# Check for failed runs
psql $DATABASE_URL -c "
SELECT 
    id,
    run_type,
    started_at,
    error_message,
    mps_collected,
    bills_collected,
    votes_collected
FROM data_collection_runs 
WHERE status = 'failed'
ORDER BY started_at DESC
LIMIT 10;
"

# Check for data inconsistencies
psql $DATABASE_URL -c "
SELECT 
    'Orphaned offices' as issue,
    COUNT(*) as count
FROM mp_offices mo
LEFT JOIN members m ON mo.mp_id = m.id
WHERE m.id IS NULL;
"
```

## 📊 **Monthly Operations**

### **1. Schema Updates**

```bash
# 1. Check migration status
cd services/api-gateway
alembic current
alembic history

# 2. Apply any pending migrations
alembic upgrade head

# 3. Verify schema integrity
psql $DATABASE_URL -c "\dt"
psql $DATABASE_URL -c "\d members"
psql $DATABASE_URL -c "\d bills"
psql $DATABASE_URL -c "\d votes"
```

### **2. Database Maintenance**

```bash
# 1. Analyze table statistics
psql $DATABASE_URL -c "ANALYZE;"

# 2. Check index usage
psql $DATABASE_URL -c "
SELECT 
    schemaname,
    tablename,
    indexrelname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes 
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
"

# 3. Monitor database growth
psql $DATABASE_URL -c "
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) as index_size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"
```

### **3. Performance Optimization**

```bash
# 1. Check slow queries
psql $DATABASE_URL -c "
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements 
WHERE mean_time > 100
ORDER BY mean_time DESC
LIMIT 10;
"

# 2. Identify unused indexes
psql $DATABASE_URL -c "
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as scans
FROM pg_stat_user_indexes 
WHERE idx_scan = 0
ORDER BY schemaname, tablename;
"
```

## 🔧 **Troubleshooting Procedures**

### **1. Data Collection Failures**

#### **Represent API Issues**
```bash
# Check API status
curl -v https://represent.opennorth.ca/api/

# Check rate limiting
# Represent API: 60 requests/minute
# Wait 1 minute if rate limited

# Verify endpoint accessibility
curl "https://represent.opennorth.ca/api/representatives/house-of-commons/"
```

#### **OurCommons.ca Issues**
```bash
# Check website accessibility
curl -v https://www.ourcommons.ca/

# Verify XML parsing
curl "https://www.ourcommons.ca/Content/Parliamentarians/Images/OfficialMPPhotos/45/" | head -20

# Check for site maintenance
curl -I https://www.ourcommons.ca/
```

#### **LEGISinfo Issues**
```bash
# Check API status
curl -v https://www.parl.ca/legisinfo/

# Verify endpoint accessibility
curl "https://www.parl.ca/legisinfo/api/bills?session=44-1"
```

### **2. Database Connection Issues**

```bash
# 1. Test basic connectivity
pg_isready -h localhost -p 5432

# 2. Check connection string
echo $DATABASE_URL

# 3. Test with psql
psql $DATABASE_URL -c "SELECT 1;"

# 4. Check PostgreSQL service status
brew services list | grep postgresql
# or
sudo systemctl status postgresql
```

### **3. Schema Mismatch Issues**

```bash
# 1. Check if all tables exist
psql $DATABASE_URL -c "\dt"

# 2. Verify table schemas
psql $DATABASE_URL -c "\d members"
psql $DATABASE_URL -c "\d bills"
psql $DATABASE_URL -c "\d votes"

# 3. Check for missing columns
psql $DATABASE_URL -c "
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'members'
ORDER BY ordinal_position;
"
```

### **4. Data Quality Issues**

```bash
# 1. Check for duplicate MPs
psql $DATABASE_URL -c "
SELECT 
    name,
    party,
    COUNT(*) as duplicate_count
FROM members 
GROUP BY name, party
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;
"

# 2. Verify MP-office relationships
psql $DATABASE_URL -c "
SELECT 
    m.name,
    COUNT(mo.id) as office_count
FROM members m
LEFT JOIN mp_offices mo ON m.id = mo.mp_id
GROUP BY m.id, m.name
HAVING COUNT(mo.id) = 0
ORDER BY m.name;
"

# 3. Check for orphaned records
psql $DATABASE_URL -c "
SELECT 
    'Orphaned offices' as issue,
    COUNT(*) as count
FROM mp_offices mo
LEFT JOIN members m ON mo.mp_id = m.id
WHERE m.id IS NULL;
"
```

## 📈 **Monitoring & Alerting**

### **1. Health Check Scripts**

Create `scripts/health_check.sh`:
```bash
#!/bin/bash
# Daily health check script

echo "🔍 OpenParliament.ca V2 Health Check - $(date)"

# Check data sources
echo "📡 Checking data sources..."
curl -s -o /dev/null -w "%{http_code}" https://represent.opennorth.ca/api/ | grep -q "200" && echo "✅ Represent API: OK" || echo "❌ Represent API: FAILED"
curl -s -o /dev/null -w "%{http_code}" https://www.ourcommons.ca/ | grep -q "200" && echo "✅ OurCommons.ca: OK" || echo "❌ OurCommons.ca: FAILED"
curl -s -o /dev/null -w "%{http_code}" https://www.parl.ca/legisinfo/ | grep -q "200" && echo "✅ LEGISinfo: OK" || echo "❌ LEGISinfo: FAILED"

# Check database
echo "🗄️ Checking database..."
psql $DATABASE_URL -c "SELECT COUNT(*) FROM members;" > /dev/null 2>&1 && echo "✅ Database: OK" || echo "❌ Database: FAILED"

# Check recent data
echo "📊 Checking recent data..."
RECENT_FILE=$(ls -t data/legacy_adapted/legacy_collected_*.json 2>/dev/null | head -1)
if [ -n "$RECENT_FILE" ]; then
    FILE_AGE=$(( $(date +%s) - $(stat -f %m "$RECENT_FILE") ))
    if [ $FILE_AGE -lt 86400 ]; then
        echo "✅ Recent data: OK (< 24 hours old)"
    else
        echo "⚠️ Recent data: OLD ($((FILE_AGE/3600)) hours old)"
    fi
else
    echo "❌ Recent data: NO FILES FOUND"
fi
```

### **2. Automated Monitoring**

Create `scripts/monitor_pipeline.sh`:
```bash
#!/bin/bash
# Continuous pipeline monitoring

while true; do
    echo "🔄 Pipeline Monitor - $(date)"
    
    # Check last collection run
    LAST_RUN=$(psql $DATABASE_URL -t -c "SELECT started_at FROM data_collection_runs ORDER BY started_at DESC LIMIT 1;" 2>/dev/null)
    
    if [ -n "$LAST_RUN" ]; then
        RUN_AGE=$(( $(date +%s) - $(date -d "$LAST_RUN" +%s) ))
        if [ $RUN_AGE -gt 86400 ]; then
            echo "⚠️ WARNING: No data collection in $((RUN_AGE/3600)) hours"
            # Send alert (email, Slack, etc.)
        fi
    fi
    
    # Check database record counts
    MP_COUNT=$(psql $DATABASE_URL -t -c "SELECT COUNT(*) FROM members;" 2>/dev/null)
    BILL_COUNT=$(psql $DATABASE_URL -t -c "SELECT COUNT(*) FROM bills;" 2>/dev/null)
    
    echo "📊 Current counts: $MP_COUNT MPs, $BILL_COUNT bills"
    
    # Wait 1 hour
    sleep 3600
done
```

## 🚨 **Emergency Procedures**

### **1. Complete Pipeline Failure**

```bash
# 1. Stop all processes
pkill -f "python.*collect_data"
pkill -f "python.*ingest_legacy_data"

# 2. Check system resources
top
df -h
free -h

# 3. Restart database if needed
brew services restart postgresql
# or
sudo systemctl restart postgresql

# 4. Verify database integrity
psql $DATABASE_URL -c "SELECT pg_check_visible('public');"

# 5. Restart pipeline
make full-pipeline
```

### **2. Data Corruption**

```bash
# 1. Identify corrupted data
psql $DATABASE_URL -c "
SELECT 
    'Corrupted records' as issue,
    COUNT(*) as count
FROM members 
WHERE name IS NULL OR name = '';
"

# 2. Restore from backup (if available)
# psql $DATABASE_URL < backup_$(date -d '1 day ago' +%Y%m%d).sql

# 3. Re-run data collection
make collect-data
make ingest-data
```

### **3. API Rate Limiting**

```bash
# 1. Check current rate limits
# Represent API: 60 requests/minute
# Wait for rate limit reset

# 2. Implement exponential backoff
python collect_data.py --backoff

# 3. Monitor API responses
curl -I https://represent.opennorth.ca/api/
# Look for 429 (Too Many Requests) or 503 (Service Unavailable)
```

## 📚 **Reference Information**

### **Environment Variables**
```bash
# Required
export DATABASE_URL="postgresql://username:password@localhost:5432/openparliament"

# Optional
export LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR
export COLLECTION_TIMEOUT="300"  # 5 minutes
export INGESTION_TIMEOUT="600"   # 10 minutes
```

### **File Locations**
- **Data Collection**: `services/etl/data/legacy_adapted/`
- **Logs**: Console output (redirect to file if needed)
- **Configuration**: `services/etl/requirements.txt`, `services/etl/Makefile`
- **Database**: PostgreSQL (local or remote)

### **Contact Information**
- **Team**: OpenParliament.ca V2 Team
- **Documentation**: `/docs/` directory
- **Issues**: GitHub repository issues
- **Emergency**: Team Slack/email

---

**Last Updated**: 2025-08-20
**Version**: 1.0
**Maintainer**: OpenParliament.ca V2 Team
**FUNDAMENTAL RULE**: ✅ **NEVER REINVENT THE WHEEL** - All procedures based on existing, proven legacy OpenParliament operations
