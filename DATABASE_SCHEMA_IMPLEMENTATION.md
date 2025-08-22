# 🗄️ DATABASE SCHEMA IMPLEMENTATION
## Merge V2: Unified Data Model Implementation

**Date:** August 21, 2025  
**Version:** 1.0  
**Status:** 🔴 IMPLEMENTATION READY  
**Scope:** Complete database schema for unified parliamentary data platform  

---

## 🎯 SCHEMA DESIGN PRINCIPLES

### **1. Unified Data Model**
- Single source of truth for all parliamentary entities
- Consistent schema across all legacy systems
- Flexible JSONB storage for entity-specific data
- Full audit trail and versioning

### **2. Performance Optimization**
- Proper indexing for common query patterns
- Partitioning for large datasets
- Connection pooling and query optimization
- Full-text search capabilities

### **3. Data Integrity**
- Referential integrity with foreign keys
- Check constraints for data validation
- Triggers for automated updates
- Comprehensive error handling

---

## 🏗️ CORE SCHEMA STRUCTURE

### **Main Tables Overview**
```sql
-- Core parliamentary entities table
parliamentary_entities          -- All parliamentary data entities
entity_relationships            -- Relationships between entities
entity_audit_log              -- Complete audit trail
users                         -- User management
user_sessions                 -- User authentication sessions
data_sources                  -- Legacy system sources
sync_status                   -- ETL synchronization status
```

---

## 📊 DETAILED TABLE DEFINITIONS

### **1. Parliamentary Entities Table**
```sql
-- Main table for all parliamentary entities
CREATE TABLE parliamentary_entities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(50) NOT NULL CHECK (type IN ('mp', 'bill', 'vote', 'debate', 'committee', 'session', 'jurisdiction')),
    data JSONB NOT NULL,
    metadata JSONB DEFAULT '{}',
    relationships TEXT[] DEFAULT '{}',
    source VARCHAR(100) NOT NULL,
    source_id VARCHAR(255), -- Original ID from legacy system
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'deleted')),
    last_synced_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Comments for documentation
COMMENT ON TABLE parliamentary_entities IS 'Main table for all parliamentary entities with unified schema';
COMMENT ON COLUMN parliamentary_entities.type IS 'Entity type: mp, bill, vote, debate, committee, session, jurisdiction';
COMMENT ON COLUMN parliamentary_entities.data IS 'Entity-specific data in JSONB format';
COMMENT ON COLUMN parliamentary_entities.metadata IS 'Additional metadata and system information';
COMMENT ON COLUMN parliamentary_entities.relationships IS 'Array of related entity IDs';
COMMENT ON COLUMN parliamentary_entities.source IS 'Legacy system source identifier';
COMMENT ON COLUMN parliamentary_entities.source_id IS 'Original ID from legacy system';
COMMENT ON COLUMN parliamentary_entities.status IS 'Entity status: active, inactive, deleted';
```

### **2. Entity Relationships Table**
```sql
-- Relationships between parliamentary entities
CREATE TABLE entity_relationships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_entity_id UUID NOT NULL REFERENCES parliamentary_entities(id) ON DELETE CASCADE,
    target_entity_id UUID NOT NULL REFERENCES parliamentary_entities(id) ON DELETE CASCADE,
    relationship_type VARCHAR(100) NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(source_entity_id, target_entity_id, relationship_type)
);

-- Comments for documentation
COMMENT ON TABLE entity_relationships IS 'Relationships between parliamentary entities';
COMMENT ON COLUMN entity_relationships.relationship_type IS 'Type of relationship: sponsors, votes_for, member_of, etc.';
COMMENT ON COLUMN entity_relationships.metadata IS 'Additional relationship metadata';
```

### **3. Entity Audit Log Table**
```sql
-- Complete audit trail for all entities
CREATE TABLE entity_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id UUID NOT NULL REFERENCES parliamentary_entities(id) ON DELETE CASCADE,
    action VARCHAR(50) NOT NULL CHECK (action IN ('create', 'update', 'delete', 'restore')),
    changes JSONB, -- What changed
    previous_state JSONB, -- Previous state before change
    user_id VARCHAR(100), -- User who made the change
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET, -- IP address of the change
    user_agent TEXT -- User agent information
);

-- Comments for documentation
COMMENT ON TABLE entity_audit_log IS 'Complete audit trail for all entity changes';
COMMENT ON COLUMN entity_audit_log.changes IS 'JSON object describing what changed';
COMMENT ON COLUMN entity_audit_log.previous_state IS 'Previous state before the change';
```

### **4. Users Table**
```sql
-- User management and authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('admin', 'moderator', 'user', 'api')),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login_at TIMESTAMP WITH TIME ZONE,
    email_verified_at TIMESTAMP WITH TIME ZONE,
    password_changed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Comments for documentation
COMMENT ON TABLE users IS 'User management and authentication';
COMMENT ON COLUMN users.role IS 'User role: admin, moderator, user, api';
COMMENT ON COLUMN users.status IS 'User status: active, inactive, suspended';
```

### **5. User Sessions Table**
```sql
-- User authentication sessions
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_used_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- Comments for documentation
COMMENT ON TABLE user_sessions IS 'User authentication sessions and tokens';
COMMENT ON COLUMN user_sessions.session_token IS 'JWT or session token';
COMMENT ON COLUMN user_sessions.expires_at IS 'When the session expires';
```

### **6. Data Sources Table**
```sql
-- Legacy system sources and configuration
CREATE TABLE data_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    type VARCHAR(50) NOT NULL CHECK (type IN ('parliamentary', 'municipal', 'external')),
    config JSONB NOT NULL, -- Connection and configuration details
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'error')),
    last_sync_at TIMESTAMP WITH TIME ZONE,
    last_sync_status VARCHAR(50),
    sync_frequency_minutes INTEGER DEFAULT 60,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Comments for documentation
COMMENT ON TABLE data_sources IS 'Legacy system sources and ETL configuration';
COMMENT ON COLUMN data_sources.config IS 'Connection details, credentials, and ETL settings';
COMMENT ON COLUMN data_sources.sync_frequency_minutes IS 'How often to sync from this source';
```

### **7. Sync Status Table**
```sql
-- ETL synchronization status and history
CREATE TABLE sync_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id UUID NOT NULL REFERENCES data_sources(id) ON DELETE CASCADE,
    sync_type VARCHAR(50) NOT NULL CHECK (sync_type IN ('full', 'incremental', 'manual')),
    status VARCHAR(50) NOT NULL CHECK (status IN ('running', 'completed', 'failed', 'cancelled')),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    entities_processed INTEGER DEFAULT 0,
    entities_created INTEGER DEFAULT 0,
    entities_updated INTEGER DEFAULT 0,
    entities_deleted INTEGER DEFAULT 0,
    error_message TEXT,
    metadata JSONB DEFAULT '{}'
);

-- Comments for documentation
COMMENT ON TABLE sync_status IS 'ETL synchronization status and history';
COMMENT ON COLUMN entity_relationships.sync_type IS 'Type of sync: full, incremental, manual';
COMMENT ON COLUMN entity_relationships.status IS 'Current sync status';
```

---

## 🔍 PERFORMANCE INDEXES

### **Primary Performance Indexes**
```sql
-- Core entity indexes
CREATE INDEX idx_parliamentary_entities_type ON parliamentary_entities(type);
CREATE INDEX idx_parliamentary_entities_source ON parliamentary_entities(source);
CREATE INDEX idx_parliamentary_entities_status ON parliamentary_entities(status);
CREATE INDEX idx_parliamentary_entities_created_at ON parliamentary_entities(created_at);
CREATE INDEX idx_parliamentary_entities_updated_at ON parliamentary_entities(updated_at);
CREATE INDEX idx_parliamentary_entities_last_synced_at ON parliamentary_entities(last_synced_at);

-- Composite indexes for common queries
CREATE INDEX idx_parliamentary_entities_type_status ON parliamentary_entities(type, status);
CREATE INDEX idx_parliamentary_entities_source_type ON parliamentary_entities(source, type);
CREATE INDEX idx_parliamentary_entities_created_status ON parliamentary_entities(created_at, status);

-- JSONB indexes for data queries
CREATE INDEX idx_parliamentary_entities_data_gin ON parliamentary_entities USING GIN (data);
CREATE INDEX idx_parliamentary_entities_metadata_gin ON parliamentary_entities USING GIN (metadata);

-- Full-text search index
CREATE INDEX idx_parliamentary_entities_search ON parliamentary_entities 
USING GIN (to_tsvector('english', data::text));

-- Relationship indexes
CREATE INDEX idx_entity_relationships_source ON entity_relationships(source_entity_id);
CREATE INDEX idx_entity_relationships_target ON entity_relationships(target_entity_id);
CREATE INDEX idx_entity_relationships_type ON entity_relationships(relationship_type);
CREATE INDEX idx_entity_relationships_source_type ON entity_relationships(source_entity_id, relationship_type);

-- Audit log indexes
CREATE INDEX idx_entity_audit_log_entity ON entity_audit_log(entity_id);
CREATE INDEX idx_entity_audit_log_action ON entity_audit_log(action);
CREATE INDEX idx_entity_audit_log_timestamp ON entity_audit_log(timestamp);
CREATE INDEX idx_entity_audit_log_user ON entity_audit_log(user_id);

-- User indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_status ON users(status);

-- Session indexes
CREATE INDEX idx_user_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_token ON user_sessions(session_token);
CREATE INDEX idx_user_sessions_expires ON user_sessions(expires_at);
CREATE INDEX idx_user_sessions_active ON user_sessions(is_active);

-- Sync status indexes
CREATE INDEX idx_sync_status_source ON sync_status(source_id);
CREATE INDEX idx_sync_status_status ON sync_status(status);
CREATE INDEX idx_sync_status_started ON sync_status(started_at);
CREATE INDEX idx_sync_status_completed ON sync_status(completed_at);
```

---

## 🔧 DATABASE FUNCTIONS & TRIGGERS

### **1. Updated At Trigger Function**
```sql
-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to all tables with updated_at
CREATE TRIGGER update_parliamentary_entities_updated_at 
    BEFORE UPDATE ON parliamentary_entities 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_entity_relationships_updated_at 
    BEFORE UPDATE ON entity_relationships 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_data_sources_updated_at 
    BEFORE UPDATE ON data_sources 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### **2. Entity Versioning Function**
```sql
-- Function to automatically increment version number
CREATE OR REPLACE FUNCTION increment_entity_version()
RETURNS TRIGGER AS $$
BEGIN
    NEW.version = OLD.version + 1;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply version trigger to parliamentary_entities
CREATE TRIGGER increment_parliamentary_entities_version 
    BEFORE UPDATE ON parliamentary_entities 
    FOR EACH ROW EXECUTE FUNCTION increment_entity_version();
```

### **3. Audit Log Trigger Function**
```sql
-- Function to automatically log changes to audit table
CREATE OR REPLACE FUNCTION log_entity_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO entity_audit_log (entity_id, action, changes, user_id)
        VALUES (NEW.id, 'create', NEW.data, current_setting('app.current_user_id', true));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO entity_audit_log (entity_id, action, changes, previous_state, user_id)
        VALUES (NEW.id, 'update', 
                jsonb_build_object('data', NEW.data, 'metadata', NEW.metadata),
                jsonb_build_object('data', OLD.data, 'metadata', OLD.metadata),
                current_setting('app.current_user_id', true));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO entity_audit_log (entity_id, action, previous_state, user_id)
        VALUES (OLD.id, 'delete', 
                jsonb_build_object('data', OLD.data, 'metadata', OLD.metadata),
                current_setting('app.current_user_id', true));
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';

-- Apply audit trigger to parliamentary_entities
CREATE TRIGGER audit_parliamentary_entities_changes 
    AFTER INSERT OR UPDATE OR DELETE ON parliamentary_entities 
    FOR EACH ROW EXECUTE FUNCTION log_entity_changes();
```

---

## 📊 DATA VALIDATION & CONSTRAINTS

### **1. Check Constraints**
```sql
-- Add check constraints for data validation
ALTER TABLE parliamentary_entities 
ADD CONSTRAINT check_entity_type_valid 
CHECK (type IN ('mp', 'bill', 'vote', 'debate', 'committee', 'session', 'jurisdiction'));

ALTER TABLE parliamentary_entities 
ADD CONSTRAINT check_status_valid 
CHECK (status IN ('active', 'inactive', 'deleted'));

ALTER TABLE users 
ADD CONSTRAINT check_role_valid 
CHECK (role IN ('admin', 'moderator', 'user', 'api'));

ALTER TABLE users 
ADD CONSTRAINT check_status_valid 
CHECK (status IN ('active', 'inactive', 'suspended'));

ALTER TABLE entity_relationships 
ADD CONSTRAINT check_relationship_type_valid 
CHECK (relationship_type IN ('sponsors', 'votes_for', 'votes_against', 'member_of', 'chairs', 'participates_in'));

ALTER TABLE sync_status 
ADD CONSTRAINT check_sync_type_valid 
CHECK (sync_type IN ('full', 'incremental', 'manual'));

ALTER TABLE sync_status 
ADD CONSTRAINT check_sync_status_valid 
CHECK (status IN ('running', 'completed', 'failed', 'cancelled'));
```

### **2. JSONB Schema Validation**
```sql
-- Function to validate MP data structure
CREATE OR REPLACE FUNCTION validate_mp_data(data JSONB)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN (
        data ? 'name' AND
        data ? 'party' AND
        data ? 'riding' AND
        jsonb_typeof(data->'name') = 'string' AND
        jsonb_typeof(data->'party') = 'string' AND
        jsonb_typeof(data->'riding') = 'string'
    );
END;
$$ language 'plpgsql';

-- Function to validate Bill data structure
CREATE OR REPLACE FUNCTION validate_bill_data(data JSONB)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN (
        data ? 'title' AND
        data ? 'status' AND
        data ? 'sponsor' AND
        jsonb_typeof(data->'title') = 'string' AND
        jsonb_typeof(data->'status') = 'string' AND
        jsonb_typeof(data->'sponsor') = 'string'
    );
END;
$$ language 'plpgsql';

-- Apply validation triggers
CREATE TRIGGER validate_mp_data_trigger
    BEFORE INSERT OR UPDATE ON parliamentary_entities
    FOR EACH ROW
    WHEN (NEW.type = 'mp')
    EXECUTE FUNCTION validate_mp_data(NEW.data);

CREATE TRIGGER validate_bill_data_trigger
    BEFORE INSERT OR UPDATE ON parliamentary_entities
    FOR EACH ROW
    WHEN (NEW.type = 'bill')
    EXECUTE FUNCTION validate_bill_data(NEW.data);
```

---

## 🚀 MIGRATION SCRIPTS

### **1. Initial Schema Creation**
```sql
-- Migration script: 001_initial_schema.sql
-- Create initial database schema

BEGIN;

-- Create tables
-- (All CREATE TABLE statements from above)

-- Create indexes
-- (All CREATE INDEX statements from above)

-- Create functions
-- (All CREATE FUNCTION statements from above)

-- Create triggers
-- (All CREATE TRIGGER statements from above)

-- Insert initial data
INSERT INTO data_sources (name, description, type, config) VALUES
('openparliament', 'OpenParliament legacy system', 'parliamentary', '{"url": "https://openparliament.ca", "api_version": "v1"}'),
('municipal_scrapers', 'Municipal government scrapers', 'municipal', '{"scrapers": 100, "jurisdictions": "all"}'),
('represent_canada', 'Represent Canada MP data', 'parliamentary', '{"url": "https://represent.opennorth.ca", "api_version": "v1"}');

-- Create admin user
INSERT INTO users (username, email, password_hash, role, status) VALUES
('admin', 'admin@mergev2.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5u.6G', 'admin', 'active');

COMMIT;
```

### **2. Sample Data Insertion**
```sql
-- Migration script: 002_sample_data.sql
-- Insert sample data for testing

BEGIN;

-- Sample MP data
INSERT INTO parliamentary_entities (type, data, source, source_id) VALUES
('mp', '{"name": "Justin Trudeau", "party": "Liberal", "riding": "Papineau", "province": "QC"}', 'openparliament', 'mp_001'),
('mp', '{"name": "Jagmeet Singh", "party": "NDP", "riding": "Burnaby South", "province": "BC"}', 'openparliament', 'mp_002'),
('mp', '{"name": "Pierre Poilievre", "party": "Conservative", "riding": "Carleton", "province": "ON"}', 'openparliament', 'mp_003');

-- Sample Bill data
INSERT INTO parliamentary_entities (type, data, source, source_id) VALUES
('bill', '{"title": "C-18 Online News Act", "status": "passed", "sponsor": "mp_001", "session": "44-1"}', 'openparliament', 'bill_001'),
('bill', '{"title": "C-11 Online Streaming Act", "status": "passed", "sponsor": "mp_001", "session": "44-1"}', 'openparliament', 'bill_002');

-- Sample relationships
INSERT INTO entity_relationships (source_entity_id, target_entity_id, relationship_type) VALUES
((SELECT id FROM parliamentary_entities WHERE source_id = 'mp_001'), (SELECT id FROM parliamentary_entities WHERE source_id = 'bill_001'), 'sponsors'),
((SELECT id FROM parliamentary_entities WHERE source_id = 'mp_001'), (SELECT id FROM parliamentary_entities WHERE source_id = 'bill_002'), 'sponsors');

COMMIT;
```

---

## 📈 PERFORMANCE OPTIMIZATION

### **1. Partitioning Strategy**
```sql
-- Partition parliamentary_entities by type for large datasets
CREATE TABLE parliamentary_entities_mp PARTITION OF parliamentary_entities
    FOR VALUES IN ('mp');

CREATE TABLE parliamentary_entities_bill PARTITION OF parliamentary_entities
    FOR VALUES IN ('bill');

CREATE TABLE parliamentary_entities_vote PARTITION OF parliamentary_entities
    FOR VALUES IN ('vote');

-- Partition audit log by date for performance
CREATE TABLE entity_audit_log_2025 PARTITION OF entity_audit_log
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

CREATE TABLE entity_audit_log_2024 PARTITION OF entity_audit_log
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

### **2. Connection Pooling Configuration**
```sql
-- PostgreSQL connection pooling settings
-- Add to postgresql.conf
max_connections = 200
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
```

---

## 🔒 SECURITY & ACCESS CONTROL

### **1. Row Level Security (RLS)**
```sql
-- Enable RLS on sensitive tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE entity_audit_log ENABLE ROW LEVEL SECURITY;

-- RLS policies
CREATE POLICY users_own_data ON users
    FOR ALL USING (id = current_setting('app.current_user_id')::UUID);

CREATE POLICY sessions_own_data ON user_sessions
    FOR ALL USING (user_id = current_setting('app.current_user_id')::UUID);

CREATE POLICY audit_log_admin_only ON entity_audit_log
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = current_setting('app.current_user_id')::UUID 
            AND role = 'admin'
        )
    );
```

### **2. Database User Roles**
```sql
-- Create application user with limited permissions
CREATE ROLE mergev2_app WITH LOGIN PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE mergev2 TO mergev2_app;
GRANT USAGE ON SCHEMA public TO mergev2_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO mergev2_app;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO mergev2_app;

-- Create read-only user for analytics
CREATE ROLE mergev2_readonly WITH LOGIN PASSWORD 'readonly_password';
GRANT CONNECT ON DATABASE mergev2 TO mergev2_readonly;
GRANT USAGE ON SCHEMA public TO mergev2_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO mergev2_readonly;
```

---

## 📊 MONITORING & MAINTENANCE

### **1. Database Statistics**
```sql
-- Enable statistics collection
ALTER SYSTEM SET track_activities = on;
ALTER SYSTEM SET track_counts = on;
ALTER SYSTEM SET track_io_timing = on;
ALTER SYSTEM SET track_functions = all;

-- Create statistics view
CREATE VIEW database_stats AS
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats
WHERE schemaname = 'public'
ORDER BY tablename, attname;
```

### **2. Maintenance Tasks**
```sql
-- Vacuum and analyze tables
VACUUM ANALYZE parliamentary_entities;
VACUUM ANALYZE entity_relationships;
VACUUM ANALYZE entity_audit_log;

-- Update statistics
ANALYZE parliamentary_entities;
ANALYZE entity_relationships;
ANALYZE entity_audit_log;
```

---

## 🎯 IMPLEMENTATION CHECKLIST

### **Phase 1: Schema Creation**
- [ ] Create all tables with proper constraints
- [ ] Implement all indexes for performance
- [ ] Create database functions and triggers
- [ ] Set up initial data sources

### **Phase 2: Data Migration**
- [ ] Create ETL connectors for legacy systems
- [ ] Implement data validation and transformation
- [ ] Set up incremental sync processes
- [ ] Validate data integrity and relationships

### **Phase 3: Performance & Security**
- [ ] Implement partitioning for large tables
- [ ] Set up connection pooling
- [ ] Configure row-level security
- [ ] Create monitoring and maintenance procedures

---

## 📞 CONCLUSION

This database schema provides a robust, scalable foundation for the Merge V2 platform with:

- **Unified data model** for all parliamentary entities
- **High performance** with proper indexing and partitioning
- **Data integrity** with constraints and validation
- **Security** with row-level security and access control
- **Audit trail** for complete change tracking
- **Flexibility** with JSONB storage for entity-specific data

**Ready for implementation and data migration from legacy systems.**

**Status: ✅ SCHEMA DESIGN COMPLETE - READY FOR IMPLEMENTATION**
