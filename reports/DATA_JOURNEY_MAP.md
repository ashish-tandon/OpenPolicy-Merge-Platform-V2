# Data Journey Map

Generated: 2025-08-23T16:44:22.670877

## Summary

- **Total Data Points**: 6
- **Complete Journeys**: 0
- **Average Completeness**: 80.6%

### Missing Stages

- analytics: 6 data points missing this stage
- ui_usage: 1 data points missing this stage

## Data Point Journeys

### Parliamentary Bills (bills)

**Type**: legislative | **Completeness**: 83%

**Key Fields**: bill_id, title, sponsor, status, text

#### Journey Stages

##### 1. Ingestion
- **etl_script**: `services/etl/legacy-scrapers-ca/tasks.py`
  - Sources: https://www12.statcan.gc.ca/census-recensement/2016/ref/dict/tab/t1_4-eng.cfm, https://www12.statcan.gc.ca/census-recensement/2016/ref/dict/tab/t1_5-eng.cfm
- **etl_script**: `services/etl/legacy-civic-scraper/setup.py`
  - Sources: https://github.com/biglocalnews/civic-scraper
- **etl_script**: `services/etl/app/data_mapping_library.py`
  - Sources: https://www.parl.ca/, https://www.parl.ca/

##### 2. Transformation
- **data_model**: `services/web-ui/src/legacy-migration/accounts/models.py`
  - Fields: email, email_bouncing, email_bounce_reason, name, created
- **data_model**: `services/web-ui/src/legacy-migration/bills/models.py`
  - Fields: name_en, name_fr, short_title_en, short_title_fr, number
- **data_model**: `services/web-ui/src/legacy-migration/alerts/models.py`
  - Fields: query, created, last_checked, last_found, topic

##### 3. Storage
- **database_table**: `bills_bill`
- **database_table**: `bills_billtext`
- **migration**: `services/web-ui/src/legacy-migration/bills/migrations/0003_add_billstage_json.py`

##### 4. API Exposure
- **configured_endpoint**: `/api/v1/bills/`
- **configured_endpoint**: `/api/v1/bills/{id}`
- **route_definition**: `/recent-bills` (`services/api-gateway/src/api/v1/feeds.py`)

##### 5. UI Usage
- **component_definition**: BillsList (`services/web-ui/src/components/Bills/BillsList.tsx`)
- **component_definition**: BillDetail (`services/web-ui/src/components/Bills/BillDetail.tsx`)
- **component_definition**: BillStatusTracker (`services/web-ui/src/components/Bills/BillStatusTracker.tsx`)

##### 6. Analytics
- ❌ No analytics found

---

### Members of Parliament (members)

**Type**: person | **Completeness**: 83%

**Key Fields**: member_id, name, party, constituency, email

#### Journey Stages

##### 1. Ingestion
- **etl_script**: `services/etl/legacy-scrapers-ca/tasks.py`
  - Sources: https://www12.statcan.gc.ca/census-recensement/2016/ref/dict/tab/t1_4-eng.cfm, https://www12.statcan.gc.ca/census-recensement/2016/ref/dict/tab/t1_5-eng.cfm
- **etl_script**: `services/etl/legacy-civic-scraper/setup.py`
  - Sources: https://github.com/biglocalnews/civic-scraper
- **etl_script**: `services/etl/app/data_mapping_library.py`
  - Sources: https://www.parl.ca/, https://www.parl.ca/

##### 2. Transformation
- **data_model**: `services/web-ui/src/legacy-migration/accounts/models.py`
  - Fields: email, email_bouncing, email_bounce_reason, name, created
- **data_model**: `services/web-ui/src/legacy-migration/bills/models.py`
  - Fields: name_en, name_fr, short_title_en, short_title_fr, number
- **data_model**: `services/web-ui/src/legacy-migration/alerts/models.py`
  - Fields: query, created, last_checked, last_found, topic

##### 3. Storage
- **database_table**: `core_electedmember`
- **database_table**: `core_membership`

##### 4. API Exposure
- **configured_endpoint**: `/api/v1/members/`
- **configured_endpoint**: `/api/v1/members/{id}`
- **route_definition**: `/members` (`services/api-gateway/src/api/v1/export.py`)

##### 5. UI Usage
- **component_definition**: MPList (`services/web-ui/src/components/MPs/MPList.tsx`)
- **component_definition**: MPProfile (`services/web-ui/src/components/MPs/MPProfile.tsx`)
- **component_definition**: MPVotingRecord (`services/web-ui/src/components/MPs/MPVotingRecord.tsx`)

##### 6. Analytics
- ❌ No analytics found

---

### Parliamentary Votes (votes)

**Type**: voting | **Completeness**: 83%

**Key Fields**: vote_id, bill_id, member_id, vote_type, date

#### Journey Stages

##### 1. Ingestion
- **etl_script**: `services/etl/legacy-scrapers-ca/tasks.py`
  - Sources: https://www12.statcan.gc.ca/census-recensement/2016/ref/dict/tab/t1_4-eng.cfm, https://www12.statcan.gc.ca/census-recensement/2016/ref/dict/tab/t1_5-eng.cfm
- **etl_script**: `services/etl/legacy-civic-scraper/setup.py`
  - Sources: https://github.com/biglocalnews/civic-scraper
- **etl_script**: `services/etl/app/data_mapping_library.py`
  - Sources: https://www.parl.ca/, https://www.parl.ca/

##### 2. Transformation
- **data_model**: `services/web-ui/src/legacy-migration/accounts/models.py`
  - Fields: email, email_bouncing, email_bounce_reason, name, created
- **data_model**: `services/web-ui/src/legacy-migration/bills/models.py`
  - Fields: name_en, name_fr, short_title_en, short_title_fr, number
- **data_model**: `services/web-ui/src/legacy-migration/alerts/models.py`
  - Fields: query, created, last_checked, last_found, topic

##### 3. Storage
- **database_table**: `votes_vote`
- **database_table**: `votes_ballotentry`

##### 4. API Exposure
- **configured_endpoint**: `/api/v1/votes/`
- **configured_endpoint**: `/api/v1/voting-records/`
- **route_definition**: `/{bill_id}/votes` (`services/api-gateway/app/api/v1/bills.py`)

##### 5. UI Usage
- **component_definition**: VotingRecordsList (`services/web-ui/src/components/voting/VotingRecordsList.tsx`)
- **component_definition**: BillVotes (`services/web-ui/src/components/Bills/BillVotes.tsx`)
- **component_definition**: MPVotes (`services/web-ui/src/components/MPs/MPVotes.tsx`)

##### 6. Analytics
- ❌ No analytics found

---

### Parliamentary Committees (committees)

**Type**: organization | **Completeness**: 83%

**Key Fields**: committee_id, name, type, members

#### Journey Stages

##### 1. Ingestion
- **etl_script**: `services/etl/legacy-scrapers-ca/tasks.py`
  - Sources: https://www12.statcan.gc.ca/census-recensement/2016/ref/dict/tab/t1_4-eng.cfm, https://www12.statcan.gc.ca/census-recensement/2016/ref/dict/tab/t1_5-eng.cfm
- **etl_script**: `services/etl/legacy-civic-scraper/setup.py`
  - Sources: https://github.com/biglocalnews/civic-scraper
- **etl_script**: `services/etl/app/data_mapping_library.py`
  - Sources: https://www.parl.ca/, https://www.parl.ca/

##### 2. Transformation
- **data_model**: `services/web-ui/src/legacy-migration/accounts/models.py`
  - Fields: email, email_bouncing, email_bounce_reason, name, created
- **data_model**: `services/web-ui/src/legacy-migration/bills/models.py`
  - Fields: name_en, name_fr, short_title_en, short_title_fr, number
- **data_model**: `services/web-ui/src/legacy-migration/alerts/models.py`
  - Fields: query, created, last_checked, last_found, topic

##### 3. Storage
- **database_table**: `committees_committee`
- **database_table**: `committees_membership`

##### 4. API Exposure
- **configured_endpoint**: `/api/v1/committees/`
- **configured_endpoint**: `/api/v1/committees/{id}`
- **route_definition**: `/{member_id}/committees` (`services/api-gateway/app/api/v1/members.py`)

##### 5. UI Usage
- **component_definition**: CommitteesList (`services/web-ui/src/components/Committees/CommitteesList.tsx`)
- **component_definition**: CommitteeMembers (`services/web-ui/src/components/Committees/CommitteeMembers.tsx`)
- **component_definition**: CommitteeReports (`services/web-ui/src/components/Committees/CommitteeReports.tsx`)

##### 6. Analytics
- ❌ No analytics found

---

### Parliamentary Debates (debates)

**Type**: transcript | **Completeness**: 83%

**Key Fields**: debate_id, date, topic, speakers, transcript

#### Journey Stages

##### 1. Ingestion
- **etl_script**: `services/etl/legacy-scrapers-ca/tasks.py`
  - Sources: https://www12.statcan.gc.ca/census-recensement/2016/ref/dict/tab/t1_4-eng.cfm, https://www12.statcan.gc.ca/census-recensement/2016/ref/dict/tab/t1_5-eng.cfm
- **etl_script**: `services/etl/legacy-civic-scraper/setup.py`
  - Sources: https://github.com/biglocalnews/civic-scraper
- **etl_script**: `services/etl/app/data_mapping_library.py`
  - Sources: https://www.parl.ca/, https://www.parl.ca/

##### 2. Transformation
- **data_model**: `services/web-ui/src/legacy-migration/accounts/models.py`
  - Fields: email, email_bouncing, email_bounce_reason, name, created
- **data_model**: `services/web-ui/src/legacy-migration/bills/models.py`
  - Fields: name_en, name_fr, short_title_en, short_title_fr, number
- **data_model**: `services/web-ui/src/legacy-migration/alerts/models.py`
  - Fields: query, created, last_checked, last_found, topic

##### 3. Storage
- **database_table**: `debates_debate`
- **database_table**: `debates_statement`

##### 4. API Exposure
- **configured_endpoint**: `/api/v1/debates/`
- **configured_endpoint**: `/api/v1/debates/{date}/{number}`
- **route_definition**: `/recent-debates` (`services/api-gateway/src/api/v1/feeds.py`)

##### 5. UI Usage
- **component_definition**: DebatesList (`services/web-ui/src/components/Debates/DebatesList.tsx`)
- **component_definition**: DebateTranscript (`services/web-ui/src/components/Debates/DebateTranscript.tsx`)
- **component_definition**: MPSpeeches (`services/web-ui/src/components/MPs/MPSpeeches.tsx`)

##### 6. Analytics
- ❌ No analytics found

---

### Electoral Constituencies (constituencies)

**Type**: geographic | **Completeness**: 67%

**Key Fields**: constituency_id, name, province, boundaries

#### Journey Stages

##### 1. Ingestion
- **etl_script**: `services/etl/legacy-scrapers-ca/tasks.py`
  - Sources: https://www12.statcan.gc.ca/census-recensement/2016/ref/dict/tab/t1_4-eng.cfm, https://www12.statcan.gc.ca/census-recensement/2016/ref/dict/tab/t1_5-eng.cfm
- **etl_script**: `services/etl/legacy-civic-scraper/setup.py`
  - Sources: https://github.com/biglocalnews/civic-scraper
- **etl_script**: `services/etl/app/data_mapping_library.py`
  - Sources: https://www.parl.ca/, https://www.parl.ca/

##### 2. Transformation
- **data_model**: `services/web-ui/src/legacy-migration/accounts/models.py`
  - Fields: email, email_bouncing, email_bounce_reason, name, created
- **data_model**: `services/web-ui/src/legacy-migration/bills/models.py`
  - Fields: name_en, name_fr, short_title_en, short_title_fr, number
- **data_model**: `services/web-ui/src/legacy-migration/alerts/models.py`
  - Fields: query, created, last_checked, last_found, topic

##### 3. Storage
- **database_table**: `core_constituency`
- **database_table**: `core_boundary`

##### 4. API Exposure
- **configured_endpoint**: `/api/v1/constituencies/`
- **configured_endpoint**: `/api/v1/represent/`

##### 5. UI Usage
- ❌ No UI usage found

##### 6. Analytics
- ❌ No analytics found

---

## Recommendations

Based on the data journey analysis:

### Incomplete Journeys

- **Parliamentary Bills**: Missing analytics
- **Members of Parliament**: Missing analytics
- **Parliamentary Votes**: Missing analytics
- **Parliamentary Committees**: Missing analytics
- **Parliamentary Debates**: Missing analytics
- **Electoral Constituencies**: Missing ui_usage, analytics

### Data Flow Improvements

1. **Standardize ingestion patterns** - Use consistent ETL framework
2. **Document transformations** - Add inline documentation for data processing
3. **Centralize API definitions** - Use OpenAPI specifications
4. **Component mapping** - Maintain data-to-component mapping
5. **Analytics integration** - Add analytics hooks to key data flows
