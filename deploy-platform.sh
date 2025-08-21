#!/bin/bash

# OpenPolicy Platform - Comprehensive Deployment Script
# This script orchestrates the deployment of all platform components

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PLATFORM_NAME="OpenPolicy Platform"
TIMEOUT=300  # 5 minutes timeout for health checks

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Health check function
wait_for_service() {
    local service_name=$1
    local health_url=$2
    local max_attempts=$3
    
    log "Waiting for $service_name to be healthy..."
    
    for i in $(seq 1 $max_attempts); do
        if curl -s "$health_url" > /dev/null 2>&1; then
            success "$service_name is healthy!"
            return 0
        fi
        
        if [ $i -eq $max_attempts ]; then
            error "$service_name failed to become healthy after $max_attempts attempts"
            return 1
        fi
        
        warning "Attempt $i/$max_attempts: $service_name not ready yet, waiting..."
        sleep 10
    done
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed or not in PATH"
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        error "Docker daemon is not running"
        exit 1
    fi
    
    success "Prerequisites check passed"
}

# Phase 1: Foundation Services
deploy_foundation() {
    log "🚀 Phase 1: Deploying Foundation Services"
    
    # Start database and Redis
    log "Starting database and Redis..."
    docker-compose up -d db redis
    
    # Wait for database to be ready
    log "Waiting for database to be ready..."
    for i in $(seq 1 30); do
        if docker-compose exec -T db pg_isready -U openpolicy > /dev/null 2>&1; then
            success "Database is ready!"
            break
        fi
        
        if [ $i -eq 30 ]; then
            error "Database failed to become ready"
            exit 1
        fi
        
        warning "Database not ready yet, waiting... (attempt $i/30)"
        sleep 10
    done
    
    # Start API Gateway and User Service
    log "Starting API Gateway and User Service..."
    docker-compose up -d api-gateway user-service
    
    # Wait for services to be healthy
    wait_for_service "API Gateway" "http://localhost:8080/health" 30
    wait_for_service "User Service" "http://localhost:8082/health" 30
    
    success "Foundation services deployed successfully"
}

# Phase 2: Data Layer
deploy_data_layer() {
    log "🚀 Phase 2: Deploying Data Layer"
    
    # Start ETL service
    log "Starting ETL service..."
    docker-compose up -d etl
    
    # Wait for ETL service to be healthy
    wait_for_service "ETL Service" "http://localhost:8083/health" 30
    
    success "Data layer deployed successfully"
}

# Phase 3: Metadata Layer
deploy_metadata_layer() {
    log "🚀 Phase 3: Deploying Metadata Layer"
    
    # Start OpenMetadata services
    log "Starting OpenMetadata services..."
    docker-compose --profile openmetadata up -d
    
    # Wait for OpenMetadata server to be ready
    wait_for_service "OpenMetadata Server" "http://localhost:8585/health" 60
    
    # Wait for Elasticsearch to be ready
    wait_for_service "Elasticsearch" "http://localhost:9200/_cluster/health" 30
    
    # Wait for MCP server to be ready
    wait_for_service "MCP Server" "http://localhost:8084/health" 30
    
    success "Metadata layer deployed successfully"
}

# Phase 4: User Interfaces
deploy_user_interfaces() {
    log "🚀 Phase 4: Deploying User Interfaces"
    
    # Start UI services
    log "Starting Admin UI and Web UI..."
    docker-compose up -d admin-ui web-ui
    
    # Wait for UI services to be ready
    wait_for_service "Admin UI" "http://localhost:3000" 30
    wait_for_service "Web UI" "http://localhost:3001" 30
    
    success "User interfaces deployed successfully"
}

# Verify deployment
verify_deployment() {
    log "🔍 Verifying deployment..."
    
    # Check all services are running
    log "Checking service status..."
    docker-compose ps
    
    # Test key endpoints
    log "Testing key endpoints..."
    
    # API Gateway
    if curl -s "http://localhost:8080/health" > /dev/null; then
        success "API Gateway is responding"
    else
        error "API Gateway is not responding"
    fi
    
    # OpenMetadata
    if curl -s "http://localhost:8585/health" > /dev/null; then
        success "OpenMetadata is responding"
    else
        error "OpenMetadata is not responding"
    fi
    
    # MCP Server
    if curl -s "http://localhost:8084/health" > /dev/null; then
        success "MCP Server is responding"
    else
        error "MCP Server is not responding"
    fi
    
    # Admin UI
    if curl -s "http://localhost:3000" > /dev/null; then
        success "Admin UI is responding"
    else
        error "Admin UI is not responding"
    fi
    
    # Web UI
    if curl -s "http://localhost:3001" > /dev/null; then
        success "Web UI is responding"
    else
        error "Web UI is not responding"
    fi
    
    success "Deployment verification completed"
}

# Display access information
display_access_info() {
    log "🎉 $PLATFORM_NAME Deployment Complete!"
    echo ""
    echo "🌐 Access Information:"
    echo "======================"
    echo "• OpenMetadata UI: http://localhost:8585 (admin@open-metadata.org / admin)"
    echo "• MCP Server: http://localhost:8084"
    echo "• API Gateway: http://localhost:8080"
    echo "• Admin UI: http://localhost:3000"
    echo "• Web UI: http://localhost:3001"
    echo "• Elasticsearch: http://localhost:9200"
    echo ""
    echo "🔧 MCP Integration:"
    echo "==================="
    echo "• Copy global-cursor-mcp.json to ~/.cursor/mcp.json"
    echo "• Restart Cursor to enable MCP integration"
    echo "• Test with: curl http://localhost:8084/mcp-info"
    echo ""
    echo "📊 Monitoring:"
    echo "=============="
    echo "• Service status: docker-compose ps"
    echo "• Service logs: docker-compose logs -f [service-name]"
    echo "• Health checks: ./health-check.sh"
}

# Main deployment function
main() {
    log "🚀 Starting $PLATFORM_NAME deployment..."
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Deploy in phases
    deploy_foundation
    deploy_data_layer
    deploy_metadata_layer
    deploy_user_interfaces
    
    # Verify deployment
    verify_deployment
    
    # Display access information
    display_access_info
    
    success "🎉 $PLATFORM_NAME deployment completed successfully!"
}

# Handle script arguments
case "${1:-}" in
    "foundation")
        log "Deploying only foundation services..."
        check_prerequisites
        deploy_foundation
        ;;
    "data")
        log "Deploying foundation and data layer..."
        check_prerequisites
        deploy_foundation
        deploy_data_layer
        ;;
    "metadata")
        log "Deploying foundation, data, and metadata layers..."
        check_prerequisites
        deploy_foundation
        deploy_data_layer
        deploy_metadata_layer
        ;;
    "full"|"")
        main
        ;;
    "verify")
        verify_deployment
        ;;
    "status")
        docker-compose ps
        ;;
    "logs")
        docker-compose logs -f "${2:-}"
        ;;
    "stop")
        log "Stopping all services..."
        docker-compose down
        ;;
    "restart")
        log "Restarting all services..."
        docker-compose restart
        ;;
    *)
        echo "Usage: $0 [foundation|data|metadata|full|verify|status|logs|stop|restart]"
        echo ""
        echo "Phases:"
        echo "  foundation  - Deploy only foundation services (db, redis, api-gateway, user-service)"
        echo "  data        - Deploy foundation + data layer (ETL)"
        echo "  metadata    - Deploy foundation + data + metadata layers (OpenMetadata)"
        echo "  full        - Deploy complete platform (default)"
        echo ""
        echo "Management:"
        echo "  verify      - Verify deployment health"
        echo "  status      - Show service status"
        echo "  logs        - Show service logs"
        echo "  stop        - Stop all services"
        echo "  restart     - Restart all services"
        exit 1
        ;;
esac
