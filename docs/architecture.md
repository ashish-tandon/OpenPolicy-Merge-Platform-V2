# Architecture Notes

## Canonical Entities
- Jurisdiction (federal, province, municipality)
- Session (parliament, legislature, council term)
- Bill (id, title, summary, status, stage, sponsors)
- Member (person, party, roles, district)
- Vote (bill, date, yeas, nays, result)

## Source → Canonical Mapping (starter)
- **OpenParliament** → Bills, Members, Votes, Sessions (federal)
- **scrapers-ca** → Members, Motions/Bills (provincial/municipal variants)
- **Represent** → District/Boundary metadata & contact info

## Search Strategy
- Postgres FTS on Bills(title, summary) with dictionaries; consider trigram index for fuzzy lookups.

## Data Flow
1. **Extract**: Scrapers run in isolated containers, output to staging tables
2. **Transform**: Normalize to canonical schema, handle jurisdiction-specific variations
3. **Load**: Upsert into production tables with audit trail
4. **Serve**: API Gateway provides unified interface to all data sources

## Technology Stack
- **Backend**: FastAPI + SQLAlchemy + Alembic
- **Database**: PostgreSQL 15+ with FTS
- **ETL**: Prefect or simple invoke/cron
- **Frontend**: Next.js (Web), React Native (Mobile), Next.js (Admin)
- **Infrastructure**: Docker + GitHub Actions + IaC templates
