# 🚀 OpenPolicy Merge Platform V2 - Complete Setup & Deployment Guide

## 📋 Project Overview

This is a comprehensive merge of multiple OpenPolicy repositories into a unified monorepo platform. The project includes:

- **Web Applications**: Modern React/Next.js frontends
- **API Services**: FastAPI backend with comprehensive data management
- **ETL Pipeline**: Data extraction and transformation services
- **Admin UI**: Administrative interface for system management
- **Legacy Integration**: 109+ scrapers and data sources
- **Database**: PostgreSQL with Alembic migrations

## 🏗️ Architecture

```
OpenPolicy Merge Platform V2/
├── apps/                    # Frontend applications
│   ├── web/                # Main web interface
│   ├── mobile/             # Mobile application
│   └── admin/              # Admin dashboard
├── services/                # Backend services
│   ├── api-gateway/        # Main API service
│   ├── etl/                # Data pipeline
│   ├── user-service/       # User management
│   └── admin-ui/           # Admin interface
├── packages/                # Shared packages
├── db/                     # Database setup
├── legacy/                  # Legacy code (read-only)
└── docs/                   # Documentation
```

## 🚀 Quick Start

### Prerequisites

- **Node.js**: 18+ (LTS recommended)
- **Python**: 3.11+
- **PostgreSQL**: 14+
- **Docker**: 20.10+
- **Git**: 2.30+

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/ashish-tandon/OpenPolicy-Merge-Platform-V2.git
cd OpenPolicy-Merge-Platform-V2

# Copy environment files
cp .env.example .env
cp services/api-gateway/.env.example services/api-gateway/.env
cp services/user-service/.env.example services/user-service/.env
```

### 2. Database Setup

```bash
# Start PostgreSQL with Docker
docker-compose up -d postgres

# Wait for database to be ready, then run migrations
cd services/api-gateway
alembic upgrade head

cd ../user-service
alembic upgrade head
```

### 3. Backend Services

```bash
# Install Python dependencies
cd services/api-gateway
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start API Gateway
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, start User Service
cd services/user-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### 4. Frontend Applications

```bash
# Install Node.js dependencies
cd apps/web
npm install

# Start development server
npm run dev

# In another terminal, start admin UI
cd apps/admin
npm install
npm run dev
```

### 5. ETL Pipeline

```bash
# Install ETL dependencies
cd services/etl
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run data collection
python collect_data.py
```

## 🔧 Configuration

### Environment Variables

Create `.env` files in each service directory:

```bash
# .env (root)
DATABASE_URL=postgresql://user:password@localhost:5432/openpolicy
REDIS_URL=redis://localhost:6379
ENVIRONMENT=development

# services/api-gateway/.env
DATABASE_URL=postgresql://user:password@localhost:5432/openpolicy
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:3000", "http://localhost:3001"]

# services/user-service/.env
DATABASE_URL=postgresql://user:password@localhost:5432/user_service
JWT_SECRET=your-jwt-secret-here
```

### Database Configuration

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: openpolicy
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

## 🧪 Testing

### Backend Testing

```bash
# API Gateway tests
cd services/api-gateway
pytest tests/ -v

# User Service tests
cd services/user-service
pytest tests/ -v

# ETL tests
cd services/etl
pytest tests/ -v
```

### Frontend Testing

```bash
# Web app tests
cd apps/web
npm test

# Admin UI tests
cd apps/admin
npm test
```

### Integration Tests

```bash
# Run all tests
make test

# Run specific test suites
make test-api
make test-frontend
make test-etl
```

## 🚀 Deployment

### Production Deployment

```bash
# Build Docker images
docker-compose -f docker-compose.prod.yml build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec api-gateway alembic upgrade head
```

### Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n openpolicy
kubectl get services -n openpolicy
```

## 📊 Monitoring & Health Checks

### Health Check Endpoints

- **API Gateway**: `GET /health`
- **User Service**: `GET /health`
- **Database**: `GET /health/db`
- **Redis**: `GET /health/redis`

### Logging

```bash
# View service logs
docker-compose logs -f api-gateway
docker-compose logs -f user-service
docker-compose logs -f postgres
```

## 🔒 Security

### Authentication

- JWT-based authentication
- Role-based access control (RBAC)
- API key management for external services

### Data Protection

- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CORS configuration

## 📈 Performance

### Optimization

- Database connection pooling
- Redis caching
- API rate limiting
- Response compression

### Scaling

- Horizontal scaling with load balancers
- Database read replicas
- CDN for static assets

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check PostgreSQL is running
   - Verify connection string in .env
   - Ensure database exists

2. **Port Conflicts**
   - Check if ports 8000, 8001, 3000, 3001 are available
   - Modify ports in configuration files

3. **Dependency Issues**
   - Clear node_modules and reinstall
   - Recreate Python virtual environments
   - Check Python/Node.js versions

### Getting Help

- Check the logs: `docker-compose logs`
- Review documentation in `/docs/`
- Check GitHub Issues
- Contact the development team

## 🎯 Next Steps

1. **Data Migration**: Import legacy data from scrapers
2. **User Onboarding**: Set up initial admin users
3. **Monitoring**: Configure alerting and dashboards
4. **Backup**: Set up automated database backups
5. **CI/CD**: Configure deployment pipelines

## 📚 Additional Resources

- [API Documentation](http://localhost:8000/docs)
- [Admin Dashboard](http://localhost:3001)
- [Legacy Code Reference](docs/REFERENCE/)
- [Architecture Decisions](docs/ADR/)

---

**🎉 Congratulations! Your OpenPolicy Merge Platform V2 is now ready for production use.**

For support and updates, visit: https://github.com/ashish-tandon/OpenPolicy-Merge-Platform-V2
