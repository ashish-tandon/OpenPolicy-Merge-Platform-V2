# API Gateway

FastAPI-based API gateway for the OpenPolicy platform, providing unified access to parliamentary and civic data from multiple jurisdictions.

## Features

- **FastAPI**: Modern, fast web framework with automatic OpenAPI documentation
- **SQLAlchemy**: ORM with Alembic for database migrations
- **Pydantic**: Data validation and serialization
- **PostgreSQL**: Primary database with full-text search capabilities
- **Redis**: Caching and session storage
- **OpenAPI 3.1**: API-first development with automatic documentation

## Architecture

The API Gateway serves as the central entry point for all client applications:

- **Web UI** (Next.js) - Public parliamentary data browsing
- **Mobile App** (React Native) - On-the-go access to civic information
- **Admin Console** (Next.js) - Administrative functions and data management
- **External Integrations** - Third-party applications and data consumers

## Data Sources

- **OpenParliament**: Federal parliamentary data (bills, votes, members)
- **Provincial/Municipal Scrapers**: Regional legislative information
- **Represent API**: Electoral district boundaries and contact information
- **ETL Pipeline**: Normalized and processed data from various sources

## Development

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 15+

### Local Development

1. **Start the development environment:**
   ```bash
   make dev
   ```

2. **Run database migrations:**
   ```bash
   make migrate
   ```

3. **Seed the database:**
   ```bash
   make seed
   ```

4. **Run tests:**
   ```bash
   make test
   ```

5. **Format code:**
   ```bash
   make fmt
   ```

### API Documentation

Once the service is running, visit:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **OpenAPI Schema**: http://localhost:8080/openapi.json

## Project Structure

```
services/api-gateway/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection and session
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── api/                 # API route handlers
│   ├── services/            # Business logic
│   └── utils/               # Utility functions
├── tests/                   # Test suite
├── alembic/                 # Database migrations
├── requirements.txt          # Python dependencies
└── Dockerfile               # Container configuration
```

## API Endpoints

### Core Endpoints
- `GET /healthz` - Health check
- `GET /version` - API version information
- `GET /bills` - List and search bills
- `GET /bills/{id}` - Bill details
- `GET /members` - List elected officials
- `GET /members/{id}` - Member details
- `GET /votes` - Voting records
- `GET /sessions` - Parliamentary sessions

### Search & Filtering
- Full-text search on bill titles and summaries
- Jurisdiction-based filtering (federal, provincial, municipal)
- Session and date range filtering
- Pagination support

## Database Schema

The API Gateway uses a canonical data model that normalizes data from various sources:

- **Jurisdictions**: Federal, provincial, and municipal levels
- **Sessions**: Parliamentary terms and legislative periods
- **Bills**: Legislation with status tracking and full text
- **Members**: Elected officials with party affiliations and roles
- **Votes**: Voting records with detailed breakdowns

## Testing

Run the test suite with:
```bash
make test              # All tests
make test-api          # API tests only
make test-coverage     # Tests with coverage report
```

## Deployment

The service is containerized and can be deployed using:
- Docker Compose (development)
- Kubernetes (production)
- Docker Swarm (staging)

## Monitoring

- Health check endpoint for load balancers
- Structured logging with configurable levels
- Metrics collection for performance monitoring
- Error tracking and alerting
