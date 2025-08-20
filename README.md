# OpenPolicy Merge Platform V2

A unified, test-driven monorepo for parliamentary and civic data from multiple jurisdictions across Canada. This platform merges data from federal, provincial, and municipal sources into a clean, modern API with comprehensive testing and documentation.

## 🎯 Project Overview

**Goal**: Transform multi-repo chaos into a clean, test-driven monorepo with strict testing, clear APIs, and repeatable data pipelines.

### Data Sources
- **Federal**: [OpenParliament](https://github.com/michaelmulley/openparliament) - Historical parliamentary data
- **Provincial/Municipal**: [scrapers-ca](https://github.com/opencivicdata/scrapers-ca) - Regional legislative scrapers
- **Infrastructure**: [open-policy-infra](https://github.com/rarewox/open-policy-infra) - Deployment utilities
- **UIs**: Admin console, mobile app, and web interface
- **External**: [Represent API](https://represent.opennorth.ca) - Electoral district data

### Architecture
- **Monorepo**: pnpm workspaces (JS/TS) + Python packages
- **API Gateway**: FastAPI with OpenAPI 3.1 spec-first workflow
- **Database**: PostgreSQL 15+ with full-text search
- **ETL**: Prefect or simple invoke/cron for data ingestion
- **Frontend**: Next.js (Web), React Native (Mobile), Admin (Next.js)
- **CI/CD**: GitHub Actions with comprehensive testing

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+ (optional, for frontend development)
- Git

### 1. Clone and Setup
```bash
git clone https://github.com/ashish-tandon/OpenPolicyMergePlatformV2.git
cd OpenPolicyMergePlatformV2

# Copy environment template
cp .env.example .env

# Setup development environment
make setup
```

### 2. Start Services
```bash
# Start all services (PostgreSQL, API Gateway, Redis)
make dev

# Check service health
make health
```

### 3. Access the Platform
- **API Documentation**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/healthz
- **Database**: localhost:5432 (user: openpolicy, db: openpolicy)

## 📁 Project Structure

```
.
├── apps/                    # Frontend applications
│   ├── web/                # Next.js web UI
│   ├── mobile/             # React Native mobile app
│   └── admin/              # Admin console
├── services/                # Backend services
│   ├── api-gateway/        # FastAPI + OpenAPI-first
│   ├── etl/                # Data ingestion orchestration
│   └── op-import/          # OpenParliament bridge
├── packages/                # Shared packages
│   ├── ui-kit/             # Shared React components
│   ├── ts-config/          # Shared TypeScript config
│   └── eslint-config/      # Shared lint rules
├── legacy/                  # Imported source code
│   ├── openparliament/     # Federal parliamentary data
│   ├── scrapers-ca/        # Provincial/municipal scrapers
│   └── civic-scraper/      # Civic data utilities
├── infra/                   # Infrastructure as Code
├── db/                      # Database migrations and seeds
├── tests/                   # Test suites
├── docs/                    # Documentation
└── scripts/                 # Utility scripts
```

## 🛠️ Development

### Available Commands
```bash
make help                    # Show all available commands
make dev                     # Start development environment
make test                    # Run all tests
make fmt                     # Format code
make lint                    # Lint code
make migrate                 # Run database migrations
make seed                    # Seed database with sample data
```

### Repository Import Strategy
We use a hybrid approach:
- **Git Subtree** (preserves history): OpenParliament, scrapers-ca, civic-scraper
- **Manual Copy** (faster): UI components, infrastructure templates

```bash
# Clone all source repositories for analysis
make vendor

# Import selected repos with history
make subtree-import
```

### API Development
1. **Update OpenAPI spec** (`openapi.yaml`)
2. **Implement endpoint** in FastAPI
3. **Write tests** (unit + integration)
4. **Update documentation**

### Database Changes
```bash
# Create new migration
make migrate-create

# Apply migrations
make migrate

# Reset database (DESTRUCTIVE)
make db-reset
```

## 🧪 Testing

### Test Coverage Requirements
- **API Gateway**: 85%+ statement coverage
- **ETL Services**: 85%+ statement coverage
- **Critical Modules**: 95%+ branch coverage

### Running Tests
```bash
# All tests
make test

# API tests only
make test-api

# ETL tests only
make test-etl

# With coverage report
make test-coverage
```

## 📊 Data Pipeline

### ETL Flow
1. **Extract**: Pull from OpenParliament, scrapers, Represent API
2. **Transform**: Normalize to canonical schema
3. **Load**: Upsert into PostgreSQL with audit trail

### Canonical Schema
- **Jurisdiction**: Federal, provincial, municipal levels
- **Session**: Parliamentary terms and legislative periods
- **Bill**: Legislation with status tracking
- **Member**: Elected officials with party affiliations
- **Vote**: Voting records with detailed breakdowns

## 🚀 Deployment

### Local Development
```bash
make dev          # Start all services
make logs         # View service logs
make shell        # Open shell in API container
make psql         # Connect to database
```

### Production
- **Kubernetes**: Use `infra/` templates
- **Docker Swarm**: Adapt `docker-compose.yml`
- **Cloud**: AWS, GCP, or Azure with managed PostgreSQL

## 📚 Documentation

- **[Instructions](docs/instructions.md)**: Cursor-editable project guide
- **[Architecture](docs/architecture.md)**: System design and decisions
- **[API Reference](openapi.yaml)**: OpenAPI 3.1 specification
- **[ADR](docs/ADR/)**: Architecture Decision Records

## 🔧 Configuration

### Environment Variables
Key configuration options in `.env`:
```bash
# Database
DATABASE_URL=postgresql+psycopg://user:pass@host:port/db

# API Settings
API_HOST=0.0.0.0
API_PORT=8080

# External APIs
REPRESENT_API_URL=https://represent.opennorth.ca/api/v1
REPRESENT_API_KEY=your-api-key

# Feature Flags
FEATURE_SEARCH_ENABLED=true
FEATURE_COMMENTS_ENABLED=false
```

## 🤝 Contributing

### Development Workflow
1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Implement** with tests
4. **Format** code (`make fmt`)
5. **Test** thoroughly (`make test`)
6. **Commit** using conventional commits
7. **Push** and create pull request

### Commit Convention
```
feat: add new bill search endpoint
fix: resolve database connection issue
docs: update API documentation
test: add integration tests for ETL
ci: configure GitHub Actions
```

## 📋 Roadmap

### Phase 1: Foundation (Week 1-2)
- [x] Project structure and configuration
- [ ] Repository import and analysis
- [ ] Database schema baseline
- [ ] Basic API endpoints

### Phase 2: Data Ingestion (Week 3-4)
- [ ] OpenParliament ETL pipeline
- [ ] Provincial scrapers integration
- [ ] Represent API hydration
- [ ] Data quality monitoring

### Phase 3: API Development (Week 5-6)
- [ ] Bills, members, votes endpoints
- [ ] Search and filtering
- [ ] Pagination and caching
- [ ] API documentation

### Phase 4: Frontend Integration (Week 7-8)
- [ ] Web UI connection
- [ ] Mobile app integration
- [ ] Admin console
- [ ] End-to-end testing

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/ashish-tandon/OpenPolicyMergePlatformV2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ashish-tandon/OpenPolicyMergePlatformV2/discussions)
- **Documentation**: Check `docs/` directory first

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenParliament** team for federal parliamentary data
- **OpenCivicData** for provincial/municipal scrapers
- **Represent** for electoral district data
- **FastAPI** and **PostgreSQL** communities

---

**OpenPolicy Merge Platform V2** - Building the future of civic data access 🏛️🇨🇦
