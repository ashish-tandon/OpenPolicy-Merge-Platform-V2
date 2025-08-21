#!/bin/bash

# OpenPolicy Platform - Health Check Script
# This script checks the health of all platform services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TIMEOUT=10

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
check_service() {
    local service_name=$1
    local health_url=$2
    local description=$3
    
    log "Checking $service_name..."
    
    if curl -s --max-time $TIMEOUT "$health_url" > /dev/null 2>&1; then
        success "$service_name: $description"
        return 0
    else
        error "$service_name: $description - NOT RESPONDING"
        return 1
    fi
}

# Database health check
check_database() {
    log "Checking database health..."
    
    if docker-compose exec -T db pg_isready -U openpolicy > /dev/null 2>&1; then
        success "Database: PostgreSQL is ready and accepting connections"
        return 0
    else
        error "Database: PostgreSQL is not ready"
        return 1
    fi
}

# Redis health check
check_redis() {
    log "Checking Redis health..."
    
    if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
        success "Redis: Service is responding to PING"
        return 0
    else
        error "Redis: Service is not responding"
        return 1
    fi
}

# Docker service status check
check_docker_services() {
    log "Checking Docker service status..."
    
    local unhealthy_services=0
    local total_services=0
    
    while IFS= read -r line; do
        if [[ $line =~ mergev2- ]]; then
            total_services=$((total_services + 1))
            
            if [[ $line =~ Up.*healthy ]]; then
                success "Docker: $(echo $line | awk '{print $1}') - Healthy"
            elif [[ $line =~ Up ]]; then
                warning "Docker: $(echo $line | awk '{print $1}') - Running (no health check)"
            elif [[ $line =~ Restarting ]]; then
                error "Docker: $(echo $line | awk '{print $1}') - Restarting"
                unhealthy_services=$((unhealthy_services + 1))
            else
                error "Docker: $(echo $line | awk '{print $1}') - Not running"
                unhealthy_services=$((unhealthy_services + 1))
            fi
        fi
    done < <(docker-compose ps --format "table {{.Names}}\t{{.Status}}")
    
    if [ $unhealthy_services -eq 0 ]; then
        success "All Docker services are running"
    else
        warning "$unhealthy_services out of $total_services services have issues"
    fi
}

# Main health check function
main() {
    log "🔍 Starting OpenPolicy Platform Health Check..."
    echo ""
    
    local overall_health=0
    
    # Check Docker services
    check_docker_services
    if [ $? -ne 0 ]; then
        overall_health=1
    fi
    
    echo ""
    
    # Check database
    check_database
    if [ $? -ne 0 ]; then
        overall_health=1
    fi
    
    echo ""
    
    # Check Redis
    check_redis
    if [ $? -ne 0 ]; then
        overall_health=1
    fi
    
    echo ""
    
    # Check HTTP services
    log "Checking HTTP service health..."
    
    check_service "API Gateway" "http://localhost:8080/health" "REST API service"
    if [ $? -ne 0 ]; then
        overall_health=1
    fi
    
    check_service "User Service" "http://localhost:8082/health" "User management service"
    if [ $? -ne 0 ]; then
        overall_health=1
    fi
    
    check_service "OpenMetadata Server" "http://localhost:8585/health" "Data lineage service"
    if [ $? -ne 0 ]; then
        overall_health=1
    fi
    
    check_service "MCP Server" "http://localhost:8084/health" "Cursor MCP integration"
    if [ $? -ne 0 ]; then
        overall_health=1
    fi
    
    check_service "Elasticsearch" "http://localhost:9200/_cluster/health" "Search and indexing service"
    if [ $? -ne 0 ]; then
        overall_health=1
    fi
    
    check_service "Admin UI" "http://localhost:3000" "Administrative interface"
    if [ $? -ne 0 ]; then
        overall_health=1
    fi
    
    check_service "Web UI" "http://localhost:3001" "Public user interface"
    if [ $? -ne 0 ]; then
        overall_health=1
    fi
    
    echo ""
    
    # Overall health summary
    if [ $overall_health -eq 0 ]; then
        success "🎉 All services are healthy!"
        echo ""
        echo "🌐 Platform Access:"
        echo "• OpenMetadata: http://localhost:8585"
        echo "• MCP Server: http://localhost:8084"
        echo "• API Gateway: http://localhost:8080"
        echo "• Admin UI: http://localhost:3000"
        echo "• Web UI: http://localhost:3001"
    else
        error "⚠️  Some services have health issues"
        echo ""
        echo "🔧 Troubleshooting:"
        echo "• Check service logs: docker-compose logs -f [service-name]"
        echo "• Restart services: docker-compose restart [service-name]"
        echo "• Full restart: docker-compose restart"
        echo "• View status: docker-compose ps"
    fi
    
    return $overall_health
}

# Handle script arguments
case "${1:-}" in
    "quick")
        # Quick health check - just HTTP endpoints
        log "🔍 Quick Health Check (HTTP endpoints only)..."
        echo ""
        
        check_service "API Gateway" "http://localhost:8080/health" "REST API service"
        check_service "OpenMetadata Server" "http://localhost:8585/health" "Data lineage service"
        check_service "MCP Server" "http://localhost:8084/health" "Cursor MCP integration"
        check_service "Admin UI" "http://localhost:3000" "Administrative interface"
        check_service "Web UI" "http://localhost:3001" "Public user interface"
        ;;
    "docker")
        # Docker services only
        check_docker_services
        ;;
    "database")
        # Database health only
        check_database
        check_redis
        ;;
    "http")
        # HTTP services only
        log "🔍 HTTP Services Health Check..."
        echo ""
        
        check_service "API Gateway" "http://localhost:8080/health" "REST API service"
        check_service "User Service" "http://localhost:8082/health" "User management service"
        check_service "OpenMetadata Server" "http://localhost:8585/health" "Data lineage service"
        check_service "MCP Server" "http://localhost:8084/health" "Cursor MCP integration"
        check_service "Elasticsearch" "http://localhost:9200/_cluster/health" "Search and indexing service"
        check_service "Admin UI" "http://localhost:3000" "Administrative interface"
        check_service "Web UI" "http://localhost:3001" "Public user interface"
        ;;
    "full"|"")
        main
        ;;
    *)
        echo "Usage: $0 [quick|docker|database|http|full]"
        echo ""
        echo "Health Check Types:"
        echo "  quick     - Quick HTTP endpoint check only"
        echo "  docker    - Docker service status only"
        echo "  database  - Database and Redis health only"
        echo "  http      - HTTP service health only"
        echo "  full      - Complete health check (default)"
        exit 1
        ;;
esac
