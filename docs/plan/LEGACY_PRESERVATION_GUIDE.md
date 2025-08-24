# Legacy Code Preservation Guide - OpenPolicy V2

Generated: 2025-08-23

This guide documents the valuable legacy code that must be preserved and migrated, not discarded. The legacy Django system contains years of parliamentary domain expertise encoded in models, managers, and business logic.

## Executive Summary

The legacy system contains:
- **Rich Domain Models**: Bill status tracking, debate parsing, election history
- **Complex Business Logic**: Parliamentary procedures, voting rules, member relationships
- **Historical Data**: Years of parliamentary records, user accounts, activity logs
- **Custom Features**: Word clouds, text analysis, summary polls

## Critical Legacy Components to Preserve

### 1. Bill Management System

**Location**: `services/web-ui/src/legacy-migration/bills/models.py`

**Key Features**:
- **47 Bill Status Codes**: Comprehensive tracking of parliamentary procedure
- **Bill Relationships**: Similar bills, sponsor tracking, committee stages
- **Smart Queries**: `recently_active()` method with complex parliamentary logic
- **Bilingual Support**: Language properties for names and titles

**Migration Strategy**:
```python
# Preserve status code mapping
LEGACY_STATUS_MAPPING = {
    'RoyalAssentGiven': 'LAW',
    'HouseInCommittee': 'COMMITTEE_HOUSE',
    'SenateInCommittee': 'COMMITTEE_SENATE',
    # ... preserve all 47 status codes
}

# Migrate business logic
class BillService:
    def get_recently_active(self, count=12):
        """Port of legacy recently_active() method"""
        return self.query_bills(
            status__in=['INTRODUCED'],
            private_member=True
        ).order_by('-status_date')[:count]
```

### 2. User Account System

**Location**: `services/web-ui/src/legacy-migration/accounts/models.py`

**Key Features**:
- **Email-based authentication**: Token login system
- **Bounce tracking**: Email deliverability management
- **Flexible data storage**: JSON field for user preferences
- **Login tracking**: Last login timestamps

**Migration Requirements**:
- Map email field to new user schema
- Preserve bounce tracking for notification system
- Migrate JSON data to structured preferences
- Generate secure passwords for token-based users

### 3. Parliamentary Debate System

**Location**: `services/web-ui/src/legacy-migration/debates/models.py`

**Key Features**:
- **Document Types**: Debates vs Committee Evidence
- **Word Cloud Generation**: Most frequent word analysis
- **XML Parsing State**: Download and parsing status tracking
- **Multilingual Support**: Content in both official languages

**Unique Value**:
- Word cloud generation logic should be preserved
- XML parsing state machine is battle-tested
- Document relationships encode parliamentary structure

### 4. Member Activity Tracking

**Location**: `services/web-ui/src/legacy-migration/activity/models.py`

**Key Features**:
- **Activity Types**: Various parliamentary activities
- **GUID System**: Unique activity identification
- **Payload Storage**: Flexible activity data
- **Active/Inactive States**: Soft delete pattern

**Business Logic**:
```python
class ActivityService:
    def track_member_activity(self, member, activity_type, data):
        """Preserve activity tracking pattern"""
        return Activity.create(
            politician=member,
            variety=activity_type,
            payload=self.format_payload(data),
            guid=self.generate_guid(member, activity_type, data)
        )
```

### 5. Riding and Postal Code System

**Location**: `services/web-ui/src/legacy-migration/core/models.py`

**Key Features**:
- **Riding Models**: Electoral district representation
- **Postal Code Cache**: Fast constituency lookup
- **Province Mapping**: Federal/provincial distinctions
- **Naming Patterns**: Bilingual riding names

**Critical Data**:
- Postal code to riding mappings (essential for FEAT-001)
- Historical riding boundaries
- Member-riding relationships over time

### 6. Election History

**Location**: `services/web-ui/src/legacy-migration/elections/models.py`

**Key Features**:
- **Election Records**: Historical election data
- **Candidacy Tracking**: Who ran where and when
- **Result Storage**: Vote counts and outcomes
- **Party Evolution**: Party changes over time

### 7. Text Analysis System

**Location**: `services/web-ui/src/legacy-migration/text-analysis/`

**Key Features**:
- **N-gram Analysis**: Speech pattern detection
- **Frequency Calculations**: Word usage statistics
- **Visualization Data**: Chart generation logic
- **Language Detection**: French/English classification

**Unique Algorithms**:
```python
def calculate_top_ngrams(text, n=1, limit=20):
    """Preserve n-gram calculation logic"""
    # This contains parliamentary-specific stopwords
    # and domain knowledge about speech patterns
```

### 8. Search Infrastructure

**Location**: `services/web-ui/src/legacy-migration/search/index.py`

**Key Features**:
- **Model Registration**: Decorator pattern for searchable models
- **Content Type System**: Unified search across models
- **Search Serialization**: Consistent search result format

## Data Migration Plan

### Phase 1: Schema Mapping (Week 1)
1. Create mapping tables for all legacy models
2. Document field transformations
3. Identify data quality issues
4. Plan for orphaned records

### Phase 2: Migration Scripts (Week 2)
```python
# Example migration script structure
class LegacyBillMigrator:
    def __init__(self):
        self.status_map = self.load_status_mapping()
        self.member_map = self.load_member_mapping()
        
    def migrate_bill(self, legacy_bill):
        return Bill(
            # Direct mappings
            number=legacy_bill.number,
            title_en=legacy_bill.name_en,
            title_fr=legacy_bill.name_fr,
            
            # Transformed mappings
            status=self.status_map[legacy_bill.status_code],
            sponsor_id=self.member_map.get(legacy_bill.sponsor_member_id),
            
            # Preserved JSON for unmapped data
            legacy_data={
                'legisinfo_id': legacy_bill.legisinfo_id,
                'text_docid': legacy_bill.text_docid,
                'billstages_json': legacy_bill.billstages_json
            }
        )
```

### Phase 3: Data Validation (Week 3)
1. Row count verification
2. Relationship integrity checks
3. Business rule validation
4. Sample data comparison

### Phase 4: Incremental Migration (Week 4)
1. Migrate reference data (parties, ridings)
2. Migrate core entities (members, bills)
3. Migrate relationships (votes, speeches)
4. Migrate activity data (recent first)

## Legacy Feature Preservation

### Custom Widgets to Preserve

1. **Word Cloud Generator**
   - Algorithm for parliamentary term extraction
   - Weighting system for importance
   - Bilingual stopword lists

2. **Activity Timeline**
   - Chronological activity display
   - Activity type icons and formatting
   - Pagination with date ranges

3. **Bill Status Visualizer**
   - Parliamentary procedure flow
   - Chamber-specific stages
   - Visual progress indicators

4. **Riding Map Integration**
   - Postal code lookup widget
   - Riding boundary display
   - Member information popup

### Business Rules to Maintain

1. **Bill Numbering**
   - Chamber-specific sequences
   - Session resets
   - Private member bill prefixes

2. **Member Status**
   - Current vs historical members
   - Party switching rules
   - Role progression tracking

3. **Voting Rules**
   - Paired voting
   - Speaker voting rules
   - Free votes vs party votes

## jQuery Components Analysis

**Location**: `bower_components/`

**Valuable Components**:
1. **Autocomplete**: Multilingual member/riding search
2. **Date Pickers**: Parliament session-aware
3. **Accessibility**: WCAG compliance features
4. **Browser Polyfills**: IE11 support (government requirement)

**Migration Path**:
- Port autocomplete logic to React components
- Preserve accessibility patterns
- Maintain keyboard navigation
- Keep ARIA labels and roles

## Risk Mitigation

### Data Loss Prevention
1. **Full Backup**: Complete database dump before migration
2. **Audit Tables**: Track all migrations with source IDs
3. **Rollback Plan**: Reverse migration scripts
4. **Parallel Run**: Keep legacy system running during migration

### Feature Parity Validation
1. **Checklist**: Every legacy feature mapped
2. **User Testing**: Key users validate migrated features
3. **A/B Testing**: Compare legacy vs new results
4. **Regression Suite**: Automated comparison tests

### Performance Considerations
1. **Index Preservation**: Maintain query performance
2. **Cache Warming**: Pre-populate caches
3. **Query Optimization**: Profile and tune
4. **Load Testing**: Verify under production load

## Success Criteria

1. **Zero Data Loss**: All records migrated
2. **Feature Parity**: All legacy features available
3. **Performance Match**: Equal or better response times
4. **User Acceptance**: Positive feedback from key users
5. **Search Quality**: Equal or better search results

## Conclusion

The legacy system represents years of parliamentary domain knowledge encoded in working software. Rather than discarding this as "technical debt", we must:

1. **Preserve** the domain knowledge
2. **Extract** the business logic
3. **Modernize** the implementation
4. **Maintain** the functionality

This approach ensures continuity for users while modernizing the technical foundation.