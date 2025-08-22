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
    start_services
    wait_for_services
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
