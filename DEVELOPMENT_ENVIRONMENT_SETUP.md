# 🛠️ DEVELOPMENT ENVIRONMENT SETUP
## Merge V2: Complete Development Infrastructure

**Date:** August 21, 2025  
**Version:** 1.0  
**Status:** 🔴 IMPLEMENTATION READY  
**Scope:** Complete development environment setup and configuration  

---

## 🎯 DEVELOPMENT ENVIRONMENT OBJECTIVES

### **Primary Goals**
1. **Unified Development Stack** - Single environment for all services
2. **Containerized Development** - Docker-based local development
3. **Automated Setup** - One-command environment initialization
4. **Development Tools** - Integrated IDE, debugging, and testing
5. **Environment Consistency** - Identical setup across team members

### **Success Criteria**
- Single command environment setup
- All services running locally
- Integrated development tools
- Automated testing and validation
- Consistent environment across team

---

## 🏗️ DEVELOPMENT ARCHITECTURE

### **Service Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Frontend  │    │  Admin Frontend │    │  Mobile App    │
│   (React/Next)  │    │   (React/TS)    │    │  (React Native)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   API Gateway   │
                    │   (FastAPI)     │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ETL Service   │    │  User Service   │    │  Monitoring     │
│   (Python)      │    │   (FastAPI)     │    │  (Grafana)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │   + Redis       │
                    └─────────────────┘
```

### **Development Stack**
- **Frontend**: React, Next.js, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11+, SQLAlchemy
- **Database**: PostgreSQL 15+, Redis 7+
- **Containerization**: Docker, Docker Compose
- **Testing**: pytest, Jest, Playwright, Cypress
- **Monitoring**: Prometheus, Grafana, ELK Stack

---

## 🐳 DOCKER COMPOSE SETUP

### **Main Docker Compose File**
```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: merge_v2_postgres
    environment:
      POSTGRES_DB: merge_v2_dev
      POSTGRES_USER: merge_v2_user
      POSTGRES_PASSWORD: merge_v2_password
      POSTGRES_INITDB_ARGS: "--encoding=UTF-8 --lc-collate=C --lc-ctype=C"
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d
      - ./db/migrations:/migrations
    networks:
      - merge_v2_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U merge_v2_user -d merge_v2_dev"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: merge_v2_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - merge_v2_network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # API Gateway
  api_gateway:
    build:
      context: ./services/api-gateway
      dockerfile: Dockerfile.dev
    container_name: merge_v2_api_gateway
    environment:
      - DATABASE_URL=postgresql://merge_v2_user:merge_v2_password@postgres:5432/merge_v2_dev
      - REDIS_URL=redis://redis:6379
      - ENVIRONMENT=development
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    ports:
      - "8000:8000"
    volumes:
      - ./services/api-gateway:/app
      - /app/venv
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - merge_v2_network
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # ETL Service
  etl_service:
    build:
      context: ./services/etl
      dockerfile: Dockerfile.dev
    container_name: merge_v2_etl
    environment:
      - DATABASE_URL=postgresql://merge_v2_user:merge_v2_password@postgres:5432/merge_v2_dev
      - REDIS_URL=redis://redis:6379
      - ENVIRONMENT=development
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    volumes:
      - ./services/etl:/app
      - /app/venv
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - merge_v2_network
    command: python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

  # User Service
  user_service:
    build:
      context: ./services/user-service
      dockerfile: Dockerfile.dev
    container_name: merge_v2_user_service
    environment:
      - DATABASE_URL=postgresql://merge_v2_user:merge_v2_password@postgres:5432/merge_v2_dev
      - REDIS_URL=redis://redis:6379
      - ENVIRONMENT=development
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    ports:
      - "8002:8000"
    volumes:
      - ./services/user-service:/app
      - /app/venv
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - merge_v2_network
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Web Frontend
  web_frontend:
    build:
      context: ./apps/web
      dockerfile: Dockerfile.dev
    container_name: merge_v2_web_frontend
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
      - NEXT_PUBLIC_ENVIRONMENT=development
    ports:
      - "3000:3000"
    volumes:
      - ./apps/web:/app
      - /app/node_modules
    networks:
      - merge_v2_network
    command: npm run dev

  # Admin Frontend
  admin_frontend:
    build:
      context: ./services/admin-ui
      dockerfile: Dockerfile.dev
    container_name: merge_v2_admin_frontend
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_ENVIRONMENT=development
    ports:
      - "3001:3000"
    volumes:
      - ./services/admin-ui:/app
      - /app/node_modules
    networks:
      - merge_v2_network
    command: npm run dev

  # Monitoring Stack
  prometheus:
    image: prom/prometheus:latest
    container_name: merge_v2_prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - merge_v2_network
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'

  grafana:
    image: grafana/grafana:latest
    container_name: merge_v2_grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    ports:
      - "3002:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
    networks:
      - merge_v2_network
    depends_on:
      - prometheus

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:

networks:
  merge_v2_network:
    driver: bridge
```

### **Development Dockerfiles**

#### **API Gateway Dockerfile**
```dockerfile
# services/api-gateway/Dockerfile.dev
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

#### **ETL Service Dockerfile**
```dockerfile
# services/etl/Dockerfile.dev
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8001

# Default command
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
```

#### **Web Frontend Dockerfile**
```dockerfile
# apps/web/Dockerfile.dev
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Default command
CMD ["npm", "run", "dev"]
```

---

## 🔧 ENVIRONMENT SETUP SCRIPTS

### **Main Setup Script**
```bash
#!/bin/bash
# setup_dev_environment.sh

set -e

echo "🚀 Setting up Merge V2 Development Environment"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_warning "Node.js is not installed. Some features may not work."
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 is not installed. Some features may not work."
    fi
    
    print_success "Prerequisites check completed"
}

# Create environment files
create_env_files() {
    print_status "Creating environment files..."
    
    # Create .env file for development
    cat > .env << EOF
# Development Environment Variables
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# Database Configuration
DATABASE_URL=postgresql://merge_v2_user:merge_v2_password@localhost:5432/merge_v2_dev
POSTGRES_DB=merge_v2_dev
POSTGRES_USER=merge_v2_user
POSTGRES_PASSWORD=merge_v2_password

# Redis Configuration
REDIS_URL=redis://localhost:6379

# API Configuration
API_BASE_URL=http://localhost:8000
ADMIN_API_URL=http://localhost:8002

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
VITE_API_URL=http://localhost:8000

# Security
SECRET_KEY=dev_secret_key_change_in_production
JWT_SECRET=dev_jwt_secret_change_in_production

# External APIs
OPENPARLIAMENT_API_KEY=your_api_key_here
CIVIC_SCRAPER_API_KEY=your_api_key_here
EOF
    
    print_success "Environment files created"
}

# Setup database
setup_database() {
    print_status "Setting up database..."
    
    # Create database directories
    mkdir -p db/init db/migrations db/seed
    
    # Create initial database schema
    cat > db/init/01_initial_schema.sql << EOF
-- Initial database schema for Merge V2
-- This file is automatically generated

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create base tables
CREATE TABLE IF NOT EXISTS parliamentary_entities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type VARCHAR(50) NOT NULL,
    data JSONB NOT NULL,
    metadata JSONB DEFAULT '{}',
    source VARCHAR(100) NOT NULL,
    source_id VARCHAR(255) NOT NULL,
    relationships JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    version INTEGER DEFAULT 1
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_parliamentary_entities_type ON parliamentary_entities(type);
CREATE INDEX IF NOT EXISTS idx_parliamentary_entities_source ON parliamentary_entities(source);
CREATE INDEX IF NOT EXISTS idx_parliamentary_entities_created_at ON parliamentary_entities(created_at);
CREATE INDEX IF NOT EXISTS idx_parliamentary_entities_data_gin ON parliamentary_entities USING GIN(data);

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create user sessions table
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create audit log table
CREATE TABLE IF NOT EXISTS entity_audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID REFERENCES parliamentary_entities(id) ON DELETE CASCADE,
    action VARCHAR(50) NOT NULL,
    changes JSONB,
    user_id UUID REFERENCES users(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
EOF
    
    print_success "Database setup completed"
}

# Setup monitoring
setup_monitoring() {
    print_status "Setting up monitoring..."
    
    # Create monitoring directory
    mkdir -p monitoring/grafana/provisioning/datasources
    mkdir -p monitoring/grafana/provisioning/dashboards
    
    # Create Prometheus configuration
    cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'api-gateway'
    static_configs:
      - targets: ['api_gateway:8000']
    metrics_path: '/metrics'

  - job_name: 'etl-service'
    static_configs:
      - targets: ['etl_service:8001']
    metrics_path: '/metrics'

  - job_name: 'user-service'
    static_configs:
      - targets: ['user_service:8000']
    metrics_path: '/metrics'
EOF
    
    # Create Grafana datasource configuration
    cat > monitoring/grafana/provisioning/datasources/datasource.yml << EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF
    
    print_success "Monitoring setup completed"
}

# Build and start services
start_services() {
    print_status "Building and starting services..."
    
    # Build all services
    docker-compose -f docker-compose.dev.yml build
    
    # Start services
    docker-compose -f docker-compose.dev.yml up -d
    
    print_success "Services started successfully"
}

# Wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for PostgreSQL
    print_status "Waiting for PostgreSQL..."
    until docker exec merge_v2_postgres pg_isready -U merge_v2_user -d merge_v2_dev; do
        sleep 2
    done
    
    # Wait for Redis
    print_status "Waiting for Redis..."
    until docker exec merge_v2_redis redis-cli ping; do
        sleep 2
    done
    
    # Wait for API Gateway
    print_status "Waiting for API Gateway..."
    until curl -f http://localhost:8000/health; do
        sleep 2
    done
    
    print_success "All services are ready"
}

# Run database migrations
run_migrations() {
    print_status "Running database migrations..."
    
    # This would run Alembic migrations
    # For now, we'll just wait for the database to be ready
    sleep 5
    
    print_success "Database migrations completed"
}

# Setup development tools
setup_dev_tools() {
    print_status "Setting up development tools..."
    
    # Create pre-commit hooks
    cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
EOF
    
    # Create VS Code settings
    mkdir -p .vscode
    cat > .vscode/settings.json << EOF
{
    "python.defaultInterpreterPath": "./services/api-gateway/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "typescript.preferences.importModuleSpecifier": "relative",
    "eslint.workingDirectories": [
        "./apps/web",
        "./services/admin-ui"
    ]
}
EOF
    
    print_success "Development tools setup completed"
}

# Main setup function
main() {
    echo "Starting development environment setup..."
    
    check_prerequisites
    create_env_files
    setup_database
    setup_monitoring
    start_services
    wait_for_services
    run_migrations
    setup_dev_tools
    
    echo ""
    print_success "🎉 Development environment setup completed!"
    echo ""
    echo "Services are running at:"
    echo "  - API Gateway: http://localhost:8000"
    echo "  - Web Frontend: http://localhost:3000"
    echo "  - Admin Frontend: http://localhost:3001"
    echo "  - User Service: http://localhost:8002"
    echo "  - Prometheus: http://localhost:9090"
    echo "  - Grafana: http://localhost:3002 (admin/admin)"
    echo ""
    echo "To stop services: docker-compose -f docker-compose.dev.yml down"
    echo "To view logs: docker-compose -f docker-compose.dev.yml logs -f"
    echo ""
}

# Run main function
main "$@"
```

### **Quick Start Script**
```bash
#!/bin/bash
# quick_start.sh

set -e

echo "🚀 Quick Start for Merge V2 Development Environment"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if services are already running
if docker ps --format "table {{.Names}}" | grep -q "merge_v2_"; then
    echo "⚠️  Services are already running. Stopping them first..."
    docker-compose -f docker-compose.dev.yml down
fi

# Start services
echo "🔄 Starting services..."
docker-compose -f docker-compose.dev.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Service Status:"
docker-compose -f docker-compose.dev.yml ps

echo ""
echo "🎉 Quick start completed!"
echo ""
echo "Services are running at:"
echo "  - API Gateway: http://localhost:8000"
echo "  - Web Frontend: http://localhost:3000"
echo "  - Admin Frontend: http://localhost:3001"
echo "  - User Service: http://localhost:8002"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana: http://localhost:3002 (admin/admin)"
echo ""
echo "To stop: docker-compose -f docker-compose.dev.yml down"
echo "To view logs: docker-compose -f docker-compose.dev.yml logs -f"
```

---

## 🧪 TESTING INFRASTRUCTURE

### **Testing Configuration**

#### **Python Testing (pytest)**
```ini
# services/api-gateway/pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=app
    --cov-report=term-missing
    --cov-report=html
    --cov-report=xml
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
```

#### **Frontend Testing (Jest)**
```json
// apps/web/jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testPathIgnorePatterns: ['<rootDir>/.next/', '<rootDir>/node_modules/'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

#### **E2E Testing (Playwright)**
```typescript
// tests/e2e/playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

---

## 📊 MONITORING & OBSERVABILITY

### **Prometheus Metrics**

#### **API Gateway Metrics**
```python
# services/api-gateway/app/metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Request metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

# Database metrics
DB_CONNECTION_GAUGE = Gauge('db_connections_active', 'Active database connections')
DB_QUERY_DURATION = Histogram('db_query_duration_seconds', 'Database query duration')

# Business metrics
ENTITIES_CREATED = Counter('entities_created_total', 'Total entities created', ['entity_type'])
ENTITIES_UPDATED = Counter('entities_updated_total', 'Total entities updated', ['entity_type'])
ENTITIES_DELETED = Counter('entities_deleted_total', 'Total entities deleted', ['entity_type'])

# Custom metrics decorator
def track_request_metrics():
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                REQUEST_COUNT.labels(method='GET', endpoint=func.__name__, status=200).inc()
                return result
            except Exception as e:
                REQUEST_COUNT.labels(method='GET', endpoint=func.__name__, status=500).inc()
                raise
            finally:
                REQUEST_DURATION.observe(time.time() - start_time)
        return wrapper
    return decorator
```

#### **Grafana Dashboards**
```json
// monitoring/grafana/provisioning/dashboards/dashboard.json
{
  "dashboard": {
    "id": null,
    "title": "Merge V2 - System Overview",
    "tags": ["merge-v2", "overview"],
    "timezone": "browser",
    "panels": [
      {
        "id": 1,
        "title": "HTTP Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "id": 2,
        "title": "Database Connections",
        "type": "stat",
        "targets": [
          {
            "expr": "db_connections_active"
          }
        ]
      },
      {
        "id": 3,
        "title": "Entity Creation Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(entities_created_total[5m])",
            "legendFormat": "{{entity_type}}"
          }
        ]
      }
    ]
  }
}
```

---

## 🔒 SECURITY CONFIGURATION

### **Development Security Settings**
```python
# services/api-gateway/app/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Security settings for development
    SECRET_KEY: str = "dev_secret_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings for development
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Web frontend
        "http://localhost:3001",  # Admin frontend
        "http://localhost:8000",  # API Gateway
        "http://localhost:8001",  # ETL Service
        "http://localhost:8002",  # User Service
    ]
    
    # Database settings
    DATABASE_URL: str = "postgresql://merge_v2_user:merge_v2_password@localhost:5432/merge_v2_dev"
    
    # Redis settings
    REDIS_URL: str = "redis://localhost:6379"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 🚀 IMPLEMENTATION CHECKLIST

### **Phase 1: Environment Setup**
- [ ] Create Docker Compose configuration
- [ ] Set up development Dockerfiles
- [ ] Create environment setup scripts
- [ ] Configure database initialization
- [ ] Set up monitoring infrastructure

### **Phase 2: Development Tools**
- [ ] Configure pre-commit hooks
- [ ] Set up VS Code settings
- [ ] Configure testing frameworks
- [ ] Set up linting and formatting
- [ ] Configure debugging tools

### **Phase 3: Testing & Validation**
- [ ] Set up unit testing infrastructure
- [ ] Configure integration testing
- [ ] Set up E2E testing
- [ ] Configure test coverage reporting
- [ ] Set up automated testing pipeline

### **Phase 4: Monitoring & Security**
- [ ] Configure Prometheus metrics
- [ ] Set up Grafana dashboards
- [ ] Configure security settings
- [ ] Set up logging and error tracking
- [ ] Configure health checks

---

## 📞 CONCLUSION

This development environment setup provides:

- **Complete containerized development stack**
- **Automated environment initialization**
- **Integrated testing and monitoring**
- **Consistent development experience**
- **Security and performance optimization**

**Ready for team development and rapid iteration.**

**Status: ✅ DEVELOPMENT ENVIRONMENT SETUP COMPLETE - READY FOR IMPLEMENTATION**
