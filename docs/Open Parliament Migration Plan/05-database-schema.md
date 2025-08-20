# Database Schema: OpenParliament.ca

**Database Engine**: PostgreSQL 13+  
**Total Size**: ~1.2GB compressed, multiple GB uncompressed  
**Historical Coverage**: 30+ years (1994-2025)  
**Key Features**: Full-text search, complex relationships, performance indexing

## Schema Overview

The database implements a sophisticated relational structure supporting:
- **338+ current MPs** with complete historical membership records
- **Thousands of bills** across multiple parliamentary sessions
- **Complete voting records** with individual MP positions  
- **30+ years of debates** with full-text searchable speeches
- **Committee system** with meeting and study tracking

## Core Models Architecture

### 1. Politicians and Membership System

#### Politicians Table
```sql
CREATE TABLE politicians_politician (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    name_family VARCHAR(50) NOT NULL,
    name_given VARCHAR(50) NOT NULL, 
    slug VARCHAR(50) UNIQUE NOT NULL,
    gender VARCHAR(10),
    
    -- Contact Information
    email VARCHAR(254),
    phone VARCHAR(20),
    fax VARCHAR(20),
    
    -- Current Position (denormalized for performance)
    current_party_id INTEGER REFERENCES politicians_party(id),
    current_riding_id INTEGER REFERENCES politicians_riding(id),
    
    -- Media
    photo VARCHAR(100),
    
    -- Full-text Search
    search_vector tsvector,
    
    -- Metadata  
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT politicians_politician_slug_unique UNIQUE (slug)
);

-- Indexes
CREATE INDEX politicians_politician_slug_idx ON politicians_politician(slug);
CREATE INDEX politicians_politician_current_party_idx ON politicians_politician(current_party_id);
CREATE INDEX politicians_politician_current_riding_idx ON politicians_politician(current_riding_id);
CREATE INDEX politicians_politician_search_idx ON politicians_politician USING gin(search_vector);
CREATE INDEX politicians_politician_name_idx ON politicians_politician(name_family, name_given);
```

#### Parties Table
```sql
CREATE TABLE politicians_party (
    id SERIAL PRIMARY KEY,
    name_en VARCHAR(100) NOT NULL,
    name_fr VARCHAR(100),
    short_name VARCHAR(20) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    color VARCHAR(7), -- Hex color code
    
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX politicians_party_slug_idx ON politicians_party(slug);
```

#### Ridings Table  
```sql
CREATE TABLE politicians_riding (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    province VARCHAR(2) NOT NULL, -- Two-letter province code
    electoral_district_number INTEGER,
    
    -- Geographic Data
    population INTEGER,
    area_km2 DECIMAL(10,2),
    
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX politicians_riding_province_idx ON politicians_riding(province);
CREATE INDEX politicians_riding_district_idx ON politicians_riding(electoral_district_number);
```

#### Memberships Table (Historical Party/Riding Associations)
```sql
CREATE TABLE politicians_membership (
    id SERIAL PRIMARY KEY,
    politician_id INTEGER NOT NULL REFERENCES politicians_politician(id),
    party_id INTEGER NOT NULL REFERENCES politicians_party(id), 
    riding_id INTEGER REFERENCES politicians_riding(id),
    
    start_date DATE NOT NULL,
    end_date DATE, -- NULL for current membership
    
    -- Parliamentary context
    session VARCHAR(10), -- e.g., "45-1"
    
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX politicians_membership_politician_idx ON politicians_membership(politician_id);
CREATE INDEX politicians_membership_party_idx ON politicians_membership(party_id); 
CREATE INDEX politicians_membership_dates_idx ON politicians_membership(start_date, end_date);
CREATE INDEX politicians_membership_current_idx ON politicians_membership(politician_id) WHERE end_date IS NULL;
```

### 2. Bills and Legislative Tracking

#### Bills Table
```sql
CREATE TABLE bills_bill (
    id SERIAL PRIMARY KEY,
    session VARCHAR(10) NOT NULL, -- e.g., "45-1", "44-1" 
    number VARCHAR(10) NOT NULL, -- e.g., "C-1", "C-2", "S-1"
    
    -- Bill Classification
    bill_type VARCHAR(3) NOT NULL, -- 'C', 'S', 'PMB'
    private_member_bill BOOLEAN DEFAULT FALSE,
    home_chamber VARCHAR(10) DEFAULT 'House', -- 'House' or 'Senate'
    
    -- Content (Bilingual)
    name_en TEXT NOT NULL,
    name_fr TEXT,
    short_title_en VARCHAR(200),
    short_title_fr VARCHAR(200), 
    summary_en TEXT,
    summary_fr TEXT,
    
    -- Status Tracking
    status_code VARCHAR(50), -- Internal status code
    status_en VARCHAR(100),  -- Human-readable status
    
    -- Legislative Process
    sponsor_politician_id INTEGER REFERENCES politicians_politician(id),
    sponsor_membership_id INTEGER REFERENCES politicians_membership(id),
    
    -- Key Dates
    introduced_date DATE,
    last_action_date DATE,
    law_date DATE, -- NULL if not law, date if royal assent
    
    -- External Integration
    legisinfo_id INTEGER UNIQUE, -- Parliament LEGISinfo ID
    legisinfo_url TEXT,
    text_url TEXT, -- Link to full bill text
    
    -- Search
    search_vector tsvector,
    
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT bills_bill_session_number UNIQUE (session, number)
);

-- Indexes
CREATE INDEX bills_bill_session_number_idx ON bills_bill(session, number);
CREATE INDEX bills_bill_status_idx ON bills_bill(status_code);
CREATE INDEX bills_bill_sponsor_idx ON bills_bill(sponsor_politician_id);
CREATE INDEX bills_bill_dates_idx ON bills_bill(introduced_date DESC);
CREATE INDEX bills_bill_law_idx ON bills_bill(law_date) WHERE law_date IS NOT NULL;
CREATE INDEX bills_bill_search_idx ON bills_bill USING gin(search_vector);
CREATE INDEX bills_bill_legisinfo_idx ON bills_bill(legisinfo_id);
```

### 3. Voting System

#### Votes Table
```sql
CREATE TABLE votes_vote (
    id SERIAL PRIMARY KEY,
    session VARCHAR(10) NOT NULL,
    number INTEGER NOT NULL, -- Sequential vote number per session
    
    date DATE NOT NULL,
    
    -- Vote Description (Bilingual)
    description_en TEXT NOT NULL,
    description_fr TEXT,
    
    -- Related Bill (optional - some votes not bill-related)
    bill_id INTEGER REFERENCES bills_bill(id),
    
    -- Vote Outcome
    result VARCHAR(10) NOT NULL, -- 'Passed', 'Failed', 'Tie'
    yea_total INTEGER DEFAULT 0,
    nay_total INTEGER DEFAULT 0,
    paired_total INTEGER DEFAULT 0, -- Legacy parliamentary procedure
    
    -- External Integration
    source_url TEXT,
    
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT votes_vote_session_number UNIQUE (session, number)
);

-- Indexes
CREATE INDEX votes_vote_session_number_idx ON votes_vote(session, number);
CREATE INDEX votes_vote_date_idx ON votes_vote(date DESC);
CREATE INDEX votes_vote_result_idx ON votes_vote(result);
CREATE INDEX votes_vote_bill_idx ON votes_vote(bill_id);
CREATE INDEX votes_vote_totals_idx ON votes_vote(yea_total, nay_total);
```

#### Ballots Table (Individual MP Votes)
```sql
CREATE TABLE votes_ballot (
    id SERIAL PRIMARY KEY,
    vote_id INTEGER NOT NULL REFERENCES votes_vote(id) ON DELETE CASCADE,
    politician_id INTEGER NOT NULL REFERENCES politicians_politician(id),
    politician_membership_id INTEGER REFERENCES politicians_membership(id),
    
    ballot VARCHAR(15) NOT NULL, -- 'Yes', 'No', 'Paired', "Didn't vote"
    
    -- Party Line Analysis
    dissent BOOLEAN DEFAULT FALSE, -- Automated party line analysis
    
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT votes_ballot_vote_politician UNIQUE (vote_id, politician_id)
);

-- Indexes
CREATE INDEX votes_ballot_vote_idx ON votes_ballot(vote_id);
CREATE INDEX votes_ballot_politician_idx ON votes_ballot(politician_id);  
CREATE INDEX votes_ballot_ballot_idx ON votes_ballot(ballot);
CREATE INDEX votes_ballot_dissent_idx ON votes_ballot(dissent) WHERE dissent = TRUE;
```

### 4. Debates and Speeches System

#### Debates Table
```sql
CREATE TABLE debates_debate (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    session VARCHAR(10) NOT NULL,
    
    -- Sequential numbering within session
    number VARCHAR(10), -- e.g., "20" for 20th sitting day
    
    -- Hierarchical Subject Structure
    h1_en VARCHAR(500), -- Main topic (e.g., "Government Orders")
    h2_en VARCHAR(500), -- Sub-topic (e.g., "Budget Implementation Act")
    h3_en VARCHAR(500), -- Specific item
    
    h1_fr VARCHAR(500), -- French equivalents
    h2_fr VARCHAR(500),
    h3_fr VARCHAR(500),
    
    -- Content Analysis
    most_frequent_word_en VARCHAR(100), -- "Word of the day"
    most_frequent_word_fr VARCHAR(100),
    
    -- AI-Generated Content
    summary TEXT,
    summary_generated BOOLEAN DEFAULT FALSE,
    summary_accuracy_disclaimer BOOLEAN DEFAULT TRUE,
    
    -- External Integration
    source_id INTEGER, -- Parliament source ID
    source_url TEXT,  -- Link to official Hansard
    document_type VARCHAR(20) DEFAULT 'Debate',
    
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT debates_debate_date_session UNIQUE (date, session)
);

-- Indexes
CREATE INDEX debates_debate_date_idx ON debates_debate(date DESC);
CREATE INDEX debates_debate_session_idx ON debates_debate(session);
CREATE INDEX debates_debate_subjects_idx ON debates_debate(h1_en, h2_en, h3_en);
CREATE INDEX debates_debate_word_idx ON debates_debate(most_frequent_word_en);
```

#### Speeches Table
```sql
CREATE TABLE speeches_speech (
    id SERIAL PRIMARY KEY,
    debate_id INTEGER NOT NULL REFERENCES debates_debate(id) ON DELETE CASCADE,
    politician_id INTEGER NOT NULL REFERENCES politicians_politician(id),
    politician_membership_id INTEGER REFERENCES politicians_membership(id),
    
    -- Timing and Sequence
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    sequence INTEGER NOT NULL, -- Order within debate
    
    -- Content (Bilingual)
    content_en TEXT NOT NULL,
    content_fr TEXT,
    
    -- Speech Classification
    procedural BOOLEAN DEFAULT FALSE, -- Procedural vs substantive speech
    
    -- Cross-references
    bill_debated_id INTEGER REFERENCES bills_bill(id),
    mentioned_politicians INTEGER[], -- Array of politician IDs mentioned
    mentioned_bills INTEGER[], -- Array of bill IDs mentioned
    
    -- Text Analysis
    word_count INTEGER DEFAULT 0,
    language_primary VARCHAR(2) DEFAULT 'en', -- Primary language
    
    -- Full-text Search
    search_vector tsvector,
    
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT speeches_speech_debate_sequence UNIQUE (debate_id, sequence)
);

-- Indexes  
CREATE INDEX speeches_speech_debate_idx ON speeches_speech(debate_id, sequence);
CREATE INDEX speeches_speech_politician_idx ON speeches_speech(politician_id);
CREATE INDEX speeches_speech_time_idx ON speeches_speech(time DESC);
CREATE INDEX speeches_speech_bill_idx ON speeches_speech(bill_debated_id);
CREATE INDEX speeches_speech_search_idx ON speeches_speech USING gin(search_vector);
CREATE INDEX speeches_speech_word_count_idx ON speeches_speech(word_count);
CREATE INDEX speeches_speech_mentions_politicians_idx ON speeches_speech USING gin(mentioned_politicians);
CREATE INDEX speeches_speech_mentions_bills_idx ON speeches_speech USING gin(mentioned_bills);
```

### 5. Committee System

#### Committees Table
```sql
CREATE TABLE committees_committee (
    id SERIAL PRIMARY KEY,
    
    -- Names (Bilingual)
    name_en VARCHAR(200) NOT NULL,
    name_fr VARCHAR(200),
    short_name_en VARCHAR(100) NOT NULL,
    short_name_fr VARCHAR(100),
    
    slug VARCHAR(50) UNIQUE NOT NULL,
    
    -- Committee Hierarchy
    parent_committee_id INTEGER REFERENCES committees_committee(id),
    
    -- Status
    active BOOLEAN DEFAULT TRUE,
    
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX committees_committee_slug_idx ON committees_committee(slug);
CREATE INDEX committees_committee_parent_idx ON committees_committee(parent_committee_id);
CREATE INDEX committees_committee_active_idx ON committees_committee(active) WHERE active = TRUE;
```

#### Committee Sessions (Historical Participation)
```sql
CREATE TABLE committees_committeesession (
    id SERIAL PRIMARY KEY,
    committee_id INTEGER NOT NULL REFERENCES committees_committee(id),
    session VARCHAR(10) NOT NULL, -- Parliamentary session
    
    acronym VARCHAR(10), -- e.g., "ETHI", "FINA"
    source_url TEXT, -- Link to official committee page
    
    active BOOLEAN DEFAULT TRUE,
    
    CONSTRAINT committees_committeesession_committee_session UNIQUE (committee_id, session)
);

CREATE INDEX committees_committeesession_committee_idx ON committees_committeesession(committee_id);
CREATE INDEX committees_committeesession_session_idx ON committees_committeesession(session);
```

#### Committee Meetings
```sql
CREATE TABLE committees_meeting (
    id SERIAL PRIMARY KEY,
    committee_id INTEGER NOT NULL REFERENCES committees_committee(id),
    session VARCHAR(10) NOT NULL,
    
    date DATE NOT NULL,
    number INTEGER NOT NULL, -- Sequential meeting number per session
    
    -- Meeting Details
    in_camera BOOLEAN DEFAULT FALSE, -- Public vs private meeting
    has_evidence BOOLEAN DEFAULT FALSE, -- Transcript availability
    
    -- Meeting Content
    agenda TEXT,
    minutes TEXT,
    
    -- External Integration
    source_url TEXT,
    
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT committees_meeting_committee_session_number UNIQUE (committee_id, session, number)
);

-- Indexes
CREATE INDEX committees_meeting_committee_idx ON committees_meeting(committee_id);
CREATE INDEX committees_meeting_date_idx ON committees_meeting(date DESC);
CREATE INDEX committees_meeting_session_idx ON committees_meeting(session);
CREATE INDEX committees_meeting_evidence_idx ON committees_meeting(has_evidence) WHERE has_evidence = TRUE;
```

### 6. User System and Alerts

#### User Alerts
```sql
CREATE TABLE alerts_alert (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    
    alert_type VARCHAR(20) NOT NULL, -- 'politician', 'bill', 'keyword', 'committee'
    
    -- Alert Criteria (flexible JSON structure)
    criteria JSONB NOT NULL,
    
    -- Specific targets (for performance)
    politician_id INTEGER REFERENCES politicians_politician(id),
    bill_id INTEGER REFERENCES bills_bill(id),
    committee_id INTEGER REFERENCES committees_committee(id),
    
    -- Settings
    email_frequency VARCHAR(20) DEFAULT 'daily', -- 'realtime', 'daily', 'weekly'
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Tracking
    last_sent TIMESTAMP WITH TIME ZONE,
    total_sent INTEGER DEFAULT 0,
    
    created TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX alerts_alert_user_idx ON alerts_alert(user_id);
CREATE INDEX alerts_alert_type_idx ON alerts_alert(alert_type);
CREATE INDEX alerts_alert_active_idx ON alerts_alert(is_active) WHERE is_active = TRUE;
CREATE INDEX alerts_alert_criteria_idx ON alerts_alert USING gin(criteria);
CREATE INDEX alerts_alert_frequency_idx ON alerts_alert(email_frequency);
```

## Advanced Database Features

### 1. Full-Text Search Configuration

#### Search Vector Updates
```sql
-- Trigger function for politician search vector
CREATE OR REPLACE FUNCTION update_politician_search_vector() RETURNS trigger AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('english', COALESCE(NEW.name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.email, '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for automatic search vector updates
CREATE TRIGGER politician_search_vector_trigger
    BEFORE INSERT OR UPDATE ON politicians_politician
    FOR EACH ROW EXECUTE FUNCTION update_politician_search_vector();
```

#### Speech Search Configuration  
```sql
-- Advanced search configuration for speeches
CREATE OR REPLACE FUNCTION update_speech_search_vector() RETURNS trigger AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('english', COALESCE(NEW.content_en, '')), 'A');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER speech_search_vector_trigger
    BEFORE INSERT OR UPDATE ON speeches_speech
    FOR EACH ROW EXECUTE FUNCTION update_speech_search_vector();
```

### 2. Performance Optimization

#### Composite Indexes for Common Queries
```sql
-- Composite indexes for frequent query patterns
CREATE INDEX votes_session_date_idx ON votes_vote(session, date DESC);
CREATE INDEX ballots_politician_vote_idx ON votes_ballot(politician_id, vote_id);
CREATE INDEX speeches_politician_time_idx ON speeches_speech(politician_id, time DESC);
CREATE INDEX memberships_politician_dates_idx ON politicians_membership(politician_id, start_date DESC, end_date DESC);

-- Partial indexes for active data
CREATE INDEX politicians_current_idx ON politicians_politician(id) 
WHERE current_party_id IS NOT NULL;

CREATE INDEX bills_current_session_idx ON bills_bill(introduced_date DESC)
WHERE session = '45-1';

CREATE INDEX alerts_pending_idx ON alerts_alert(user_id, alert_type)
WHERE is_active = TRUE AND last_sent < NOW() - INTERVAL '1 day';
```

#### Materialized Views for Analytics
```sql
-- MP voting statistics  
CREATE MATERIALIZED VIEW mp_voting_stats AS
SELECT 
    p.id,
    p.name,
    p.current_party_id,
    COUNT(b.id) as total_votes,
    COUNT(CASE WHEN b.ballot = 'Yes' THEN 1 END) as yes_votes,
    COUNT(CASE WHEN b.ballot = 'No' THEN 1 END) as no_votes,
    COUNT(CASE WHEN b.dissent = TRUE THEN 1 END) as dissenting_votes,
    ROUND(COUNT(CASE WHEN b.dissent = TRUE THEN 1 END)::numeric / COUNT(b.id) * 100, 2) as dissent_percentage
FROM politicians_politician p
LEFT JOIN votes_ballot b ON p.id = b.politician_id
GROUP BY p.id, p.name, p.current_party_id;

CREATE UNIQUE INDEX ON mp_voting_stats(id);

-- Refresh materialized views daily
CREATE OR REPLACE FUNCTION refresh_analytics_views() RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mp_voting_stats;
END;
$$ LANGUAGE plpgsql;
```

### 3. Data Integrity Constraints

#### Custom Constraints
```sql
-- Ensure current membership consistency
ALTER TABLE politicians_politician 
ADD CONSTRAINT current_party_has_membership 
CHECK (
    current_party_id IS NULL OR 
    EXISTS (
        SELECT 1 FROM politicians_membership m 
        WHERE m.politician_id = id 
        AND m.party_id = current_party_id 
        AND m.end_date IS NULL
    )
);

-- Ensure vote totals match ballots
CREATE OR REPLACE FUNCTION validate_vote_totals() RETURNS trigger AS $$
BEGIN
    IF (SELECT COUNT(*) FROM votes_ballot WHERE vote_id = NEW.id AND ballot = 'Yes') != NEW.yea_total THEN
        RAISE EXCEPTION 'Vote totals do not match ballot counts';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER vote_totals_validation_trigger
    AFTER UPDATE ON votes_vote
    FOR EACH ROW EXECUTE FUNCTION validate_vote_totals();
```

### 4. Historical Data Management

#### Partitioning for Large Tables
```sql
-- Partition speeches by year for performance
CREATE TABLE speeches_speech_2024 PARTITION OF speeches_speech
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE speeches_speech_2025 PARTITION OF speeches_speech  
FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- Automatic partition creation function
CREATE OR REPLACE FUNCTION create_speech_partition(partition_year INTEGER) RETURNS void AS $$
DECLARE
    partition_name TEXT := 'speeches_speech_' || partition_year;
    start_date TEXT := partition_year || '-01-01';
    end_date TEXT := (partition_year + 1) || '-01-01';
BEGIN
    EXECUTE 'CREATE TABLE ' || partition_name || ' PARTITION OF speeches_speech
             FOR VALUES FROM (''' || start_date || ''') TO (''' || end_date || ''')';
    
    EXECUTE 'CREATE INDEX ' || partition_name || '_time_idx ON ' || partition_name || '(time DESC)';
    EXECUTE 'CREATE INDEX ' || partition_name || '_politician_idx ON ' || partition_name || '(politician_id)';
END;
$$ LANGUAGE plpgsql;
```

### 5. Backup and Maintenance

#### Regular Maintenance Tasks
```sql
-- Database maintenance function
CREATE OR REPLACE FUNCTION maintain_database() RETURNS void AS $$
BEGIN
    -- Update search vectors for new content
    UPDATE politicians_politician SET search_vector = NULL WHERE search_vector IS NULL;
    UPDATE speeches_speech SET search_vector = NULL WHERE search_vector IS NULL;
    
    -- Refresh materialized views
    REFRESH MATERIALIZED VIEW CONCURRENTLY mp_voting_stats;
    
    -- Analyze tables for query planning
    ANALYZE politicians_politician;
    ANALYZE votes_vote;
    ANALYZE speeches_speech;
    
    -- Vacuum for space reclamation
    VACUUM (ANALYZE) votes_ballot;
    VACUUM (ANALYZE) debates_debate;
END;
$$ LANGUAGE plpgsql;
```

## Database Statistics

### Current Data Volume (August 2025)
```sql
-- Table sizes and record counts
SELECT 
    schemaname,
    tablename, 
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes
FROM pg_stat_user_tables 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Expected results:
-- speeches_speech: ~500MB, 2M+ records (30+ years of speeches)
-- votes_ballot: ~200MB, 1M+ records (individual MP votes)  
-- politicians_politician: ~50MB, 2000+ records (current + historical MPs)
-- bills_bill: ~100MB, 10000+ records (all federal legislation)
-- votes_vote: ~50MB, 5000+ records (all parliamentary votes)
```

---

*This database schema supports the full OpenParliament.ca platform with 30+ years of parliamentary data, advanced search capabilities, and sophisticated relationship tracking across all parliamentary entities.*