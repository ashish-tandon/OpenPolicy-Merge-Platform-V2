# ETL Service

Data extraction, transformation, and loading service for the OpenPolicy platform. Handles ingestion of parliamentary and civic data from multiple sources into a unified canonical schema.

## Overview

The ETL service is responsible for:

1. **Extract**: Pull data from various sources (OpenParliament, scrapers-ca, Represent API)
2. **Transform**: Normalize data to canonical schema, handle jurisdiction-specific variations
3. **Load**: Upsert data into production tables with audit trail and error handling

## Data Sources

### OpenParliament (Federal)
- **Source**: Django-based parliamentary data system
- **Data**: Bills, votes, members, sessions from Canadian Parliament
- **Format**: Database exports, API calls, or direct database access
- **Frequency**: Daily updates during parliamentary sessions

### Provincial/Municipal Scrapers
- **Source**: opencivicdata/scrapers-ca repository
- **Data**: Regional legislative information from provinces and cities
- **Format**: Scraped HTML/JSON from government websites
- **Frequency**: Weekly updates, varies by jurisdiction

### Represent API
- **Source**: represent.opennorth.ca
- **Data**: Electoral district boundaries, contact information
- **Format**: REST API with JSON responses
- **Frequency**: As needed for district updates

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   ETL Service   │    │  Canonical DB   │
│                 │    │                 │    │                 │
│ • OpenParliament│───▶│ • Extractors    │───▶│ • Bills         │
│ • scrapers-ca   │    │ • Normalizers   │    │ • Members       │
│ • Represent API │    │ • Loaders       │    │ • Votes         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Canonical Schema

The ETL service transforms data into a unified schema:

### Core Entities
- **Jurisdiction**: Federal, provincial, municipal levels
- **Session**: Parliamentary terms and legislative periods
- **Bill**: Legislation with status tracking and metadata
- **Member**: Elected officials with party affiliations
- **Vote**: Voting records with detailed breakdowns

### Data Quality
- **Idempotency**: All loaders support upsert semantics
- **Audit Trail**: Track data provenance and transformation history
- **Error Handling**: Comprehensive logging and retry mechanisms
- **Validation**: Pydantic models for data validation

## Development

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Docker and Docker Compose

### Local Development

1. **Start the development environment:**
   ```bash
   make dev
   ```

2. **Run ETL tests:**
   ```bash
   make test-etl
   ```

3. **Seed the database:**
   ```bash
   make seed
   ```

4. **Run specific ETL tasks:**
   ```bash
   docker compose --profile etl run --rm etl python -m etl.tasks.openparliament
   ```

### Project Structure

```
services/etl/
├── app/
│   ├── __init__.py
│   ├── extractors/          # Data source extractors
│   │   ├── openparliament.py
│   │   ├── scrapers_ca.py
│   │   └── represent.py
│   ├── normalizers/         # Data transformation logic
│   │   ├── bills.py
│   │   ├── members.py
│   │   └── votes.py
│   ├── loaders/             # Database loaders
│   │   ├── base.py
│   │   ├── bills.py
│   │   └── members.py
│   ├── models/              # Pydantic models
│   ├── utils/               # Utility functions
│   └── tasks/               # ETL task definitions
├── tests/                   # Test suite
├── requirements.txt          # Python dependencies
└── Dockerfile               # Container configuration
```

## ETL Tasks

### OpenParliament Ingestion
```bash
# Extract and load federal parliamentary data
python -m etl.tasks.openparliament --full-sync

# Incremental update
python -m etl.tasks.openparliament --since 2024-01-01
```

### Provincial Scrapers
```bash
# Run scrapers for specific jurisdictions
python -m etl.tasks.scrapers_ca --jurisdiction ON

# Run all provincial scrapers
python -m etl.tasks.scrapers_ca --all
```

### Represent API Hydration
```bash
# Update district boundaries and contact info
python -m etl.tasks.represent --districts

# Update office information
python -m etl.tasks.represent --offices
```

## Configuration

Environment variables control ETL behavior:

```bash
# Database
DATABASE_URL=postgresql+psycopg://user:pass@host:port/db

# ETL Settings
ETL_BATCH_SIZE=1000
ETL_MAX_RETRIES=3
ETL_RETRY_DELAY=5

# External APIs
REPRESENT_API_URL=https://represent.opennorth.ca/api/v1
REPRESENT_API_KEY=your-api-key

# Logging
LOG_LEVEL=INFO
```

## Monitoring

### Metrics
- Rows processed per source
- Processing duration
- Error rates and types
- Data quality indicators

### Logging
- Structured logging with correlation IDs
- Error details with stack traces
- Performance metrics
- Data lineage tracking

### Health Checks
- Database connectivity
- External API availability
- Task queue status
- Storage capacity

## Testing

Run the ETL test suite:

```bash
# All tests
make test-etl

# Specific test categories
pytest tests/test_extractors/ -v
pytest tests/test_normalizers/ -v
pytest tests/test_loaders/ -v

# With coverage
pytest --cov=app --cov-report=html
```

## Deployment

The ETL service can be deployed using:

- **Docker Compose**: Development and testing
- **Kubernetes**: Production with CronJob for scheduled runs
- **AWS Lambda**: Serverless for small datasets
- **Prefect**: Workflow orchestration for complex pipelines

## Future Enhancements

- **Real-time Streaming**: Kafka integration for live updates
- **Machine Learning**: Automated data quality scoring
- **Advanced Scheduling**: DAG-based workflow management
- **Data Lineage**: End-to-end data flow tracking
- **Performance Optimization**: Parallel processing and caching
