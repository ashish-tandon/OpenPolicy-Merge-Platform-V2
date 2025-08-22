# Data Lineage Map

## Scope
Covers ingestion → normalization → storage → indexing → API → UI → analytics.
Links to concrete tables, schemas, and API contracts.

## Entities (reference)
- Source Systems: Federal/Provincial/Municipal feeds, scrapers
- Storage: Postgres schemas, Elasticsearch indices
- Movement: ETL/ELT jobs, schedulers
- Exposure: API_DESIGN_SPECIFICATION.md (endpoint → table/index mapping)
- Consumption: UI components, dashboards

## Required Tables/Indices
- [List exact table names, columns, and indices from db artifacts]
- [Map to API endpoints and feature IDs]

## Route Map (per feature)
- Feature ID → Ingestion job(s) → Transform(s) → Table(s)/Index(es) → Endpoint(s) → UI View(s)
- Include error handling and idempotency notes.

## Validation
- Cross-check with FEATURE_COMPARISON_pass1.csv
- Each route must have a test checkpoint in the Execution Checklist.

<!-- MERGE_NOTE: Fill in from artifacts/db/pass1/*.md and API spec -->