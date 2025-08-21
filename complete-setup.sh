#!/bin/bash

# Complete OpenMetadata MCP Integration Setup Script
# This script builds, starts, tests, and configures everything

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOME_DIR="$HOME"
CURSOR_DIR="$HOME_DIR/.cursor"

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    return 1
}

# Check prerequisites
check_prerequisites() {
    log "🔍 Checking prerequisites..."
    
    # Check if Docker is running
    if ! docker info &> /dev/null; then
        error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    
    # Check if docker-compose is available
    if ! command -v docker-compose &> /dev/null; then
        error "docker-compose is not available. Please install Docker Compose."
        exit 1
    fi
    
    # Check if we're in the right directory
    if [ ! -f "docker-compose.yml" ]; then
        error "docker-compose.yml not found. Please run this script from the project root."
        exit 1
    fi
    
    success "Prerequisites check passed"
}

# Build all containers
build_containers() {
    log "🔨 Building all containers..."
    
    # Build OpenMetadata container first
    log "Building OpenMetadata container with MCP server..."
    if docker-compose build openmetadata-server; then
        success "OpenMetadata container built successfully"
    else
        error "Failed to build OpenMetadata container"
        exit 1
    fi
    
    # Build other services
    log "Building other services..."
    if docker-compose build; then
        success "All containers built successfully"
    else
        error "Failed to build some containers"
        exit 1
    fi
}

# Start all services
start_all_services() {
    log "🚀 Starting all services..."
    
    # Start all services with profiles
    if docker-compose --profile openmetadata --profile frontend up -d; then
        success "All services started successfully"
    else
        error "Failed to start some services"
        exit 1
    fi
    
    # Wait for services to be ready
    log "⏳ Waiting for services to be ready..."
    sleep 90
    
    # Check container status
    log "🔍 Checking container status..."
    docker-compose ps
}

# Test database connectivity
test_database() {
    log "🧪 Testing database connectivity..."
    
    # Wait for database to be ready
    log "Waiting for database to be ready..."
    for i in $(seq 1 30); do
        if docker-compose exec -T db pg_isready -U openpolicy > /dev/null 2>&1; then
            success "Database is ready!"
            break
        fi
        
        if [ $i -eq 30 ]; then
            error "Database failed to become ready"
            return 1
        fi
        
        warning "Database not ready yet, waiting... (attempt $i/30)"
        sleep 10
    done
    
    # Test database connection
    if docker-compose exec -T db psql -U openpolicy -d openpolicy -c "SELECT version();" > /dev/null 2>&1; then
        success "Database connection test passed"
    else
        error "Database connection test failed"
        return 1
    fi
}

# Test Redis connectivity
test_redis() {
    log "🧪 Testing Redis connectivity..."
    
    # Wait for Redis to be ready
    log "Waiting for Redis to be ready..."
    for i in $(seq 1 20); do
        if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
            success "Redis is ready!"
            break
        fi
        
        if [ $i -eq 20 ]; then
            error "Redis failed to become ready"
            return 1
        fi
        
        warning "Redis not ready yet, waiting... (attempt $i/20)"
        sleep 5
    done
    
    # Test Redis connection
    if docker-compose exec -T redis redis-cli ping | grep -q "PONG"; then
        success "Redis connection test passed"
    else
        error "Redis connection test failed"
        return 1
    fi
}

# Test API services
test_api_services() {
    log "🧪 Testing API services..."
    
    # Test API Gateway
    log "Testing API Gateway..."
    for i in $(seq 1 20); do
        if curl -s --max-time 5 "http://localhost:8080/healthz" > /dev/null 2>&1; then
            success "API Gateway is responding"
            break
        fi
        
        if [ $i -eq 20 ]; then
            error "API Gateway is not responding"
            return 1
        fi
        
        warning "API Gateway not ready yet, waiting... (attempt $i/20)"
        sleep 5
    done
    
    # Test User Service
    log "Testing User Service..."
    for i in $(seq 1 20); do
        if curl -s --max-time 5 "http://localhost:8082/health" > /dev/null 2>&1; then
            success "User Service is responding"
            break
        fi
        
        if [ $i -eq 20 ]; then
            error "User Service is not responding"
            return 1
        fi
        
        warning "User Service not ready yet, waiting... (attempt $i/20)"
        sleep 5
    done
}

# Test OpenMetadata services
test_openmetadata() {
    log "🧪 Testing OpenMetadata services..."
    
    # Test Elasticsearch
    log "Testing Elasticsearch..."
    for i in $(seq 1 30); do
        if curl -s --max-time 5 "http://localhost:9200/_cluster/health" > /dev/null 2>&1; then
            success "Elasticsearch is responding"
            break
        fi
        
        if [ $i -eq 30 ]; then
            error "Elasticsearch is not responding"
            return 1
        fi
        
        warning "Elasticsearch not ready yet, waiting... (attempt $i/30)"
        sleep 10
    done
    
    # Test OpenMetadata Server
    log "Testing OpenMetadata Server..."
    for i in $(seq 1 30); do
        if curl -s --max-time 5 "http://localhost:8585/health" > /dev/null 2>&1; then
            success "OpenMetadata Server is responding"
            break
        fi
        
        if [ $i -eq 30 ]; then
            error "OpenMetadata Server is not responding"
            return 1
        fi
        
        warning "OpenMetadata Server not ready yet, waiting... (attempt $i/30)"
        sleep 10
    done
    
    # Test MCP Server
    log "Testing MCP Server..."
    for i in $(seq 1 30); do
        if curl -s --max-time 5 "http://localhost:8084/health" > /dev/null 2>&1; then
            success "MCP Server is responding"
            break
        fi
        
        if [ $i -eq 30 ]; then
            error "MCP Server is not responding"
            return 1
        fi
        
        warning "MCP Server not ready yet, waiting... (attempt $i/30)"
        sleep 10
    done
    
    # Test OpenMetadata Ingestion (Airflow)
    log "Testing OpenMetadata Ingestion..."
    for i in $(seq 1 30); do
        if curl -s --max-time 5 "http://localhost:8083/health" > /dev/null 2>&1; then
            success "OpenMetadata Ingestion is responding"
            break
        fi
        
        if [ $i -eq 30 ]; then
            error "OpenMetadata Ingestion is not responding"
            return 1
        fi
        
        warning "OpenMetadata Ingestion not ready yet, waiting... (attempt $i/30)"
        sleep 10
    done
}

# Test frontend services
test_frontend() {
    log "🧪 Testing frontend services..."
    
    # Test Admin UI
    log "Testing Admin UI..."
    for i in $(seq 1 20); do
        if curl -s --max-time 5 "http://localhost:3000" > /dev/null 2>&1; then
            success "Admin UI is responding"
            break
        fi
        
        if [ $i -eq 20 ]; then
            error "Admin UI is not responding"
            return 1
        fi
        
        warning "Admin UI not ready yet, waiting... (attempt $i/20)"
        sleep 5
    done
    
    # Test Web UI
    log "Testing Web UI..."
    for i in $(seq 1 20); do
        if curl -s --max-time 5 "http://localhost:3001" > /dev/null 2>&1; then
            success "Web UI is responding"
            break
        fi
        
        if [ $i -eq 20 ]; then
            error "Web UI is not responding"
            return 1
        fi
        
        warning "Web UI not ready yet, waiting... (attempt $i/20)"
        sleep 5
    done
}

# Auto-open monitoring dashboard
auto_open_monitoring() {
    log "🖥️  Auto-opening monitoring dashboard..."
    
    # Wait a bit for the dashboard to be fully ready
    sleep 5
    
    # Check if monitoring dashboard is accessible
    if curl -s --max-time 5 "http://localhost:8087" > /dev/null 2>&1; then
        success "Monitoring dashboard is ready!"
        
        # Try to auto-open in browser (macOS)
        if command -v open > /dev/null 2>&1; then
            log "🌐 Opening monitoring dashboard in your default browser..."
            open "http://localhost:8087"
            success "Monitoring dashboard opened! This is your main monitoring page."
        else
            log "🌐 Please manually open: http://localhost:8087"
            log "   This is your MAIN MONITORING PAGE!"
        fi
    else
        warning "Monitoring dashboard not ready yet, please open manually: http://localhost:8087"
    fi
}

# Test MCP integration
test_mcp_integration() {
    log "🧪 Testing MCP integration..."
    
    # Test MCP endpoints
    log "Testing MCP endpoints..."
    
    # Test MCP health
    if curl -s --max-time 10 "http://localhost:8084/health" > /dev/null; then
        success "MCP health endpoint is working"
    else
        error "MCP health endpoint is not working"
        return 1
    fi
    
    # Test MCP info
    if curl -s --max-time 10 "http://localhost:8084/mcp-info" > /dev/null; then
        success "MCP info endpoint is working"
    else
        error "MCP info endpoint is not working"
        return 1
    fi
    
    # Test MCP protocol endpoint
    if curl -s --max-time 10 "http://localhost:8084/mcp/sse" > /dev/null; then
        success "MCP SSE endpoint is working"
    else
        error "MCP SSE endpoint is not working"
        return 1
    fi
    
    success "MCP integration test passed"
}

# Reload MCP proxy
reload_mcp_proxy() {
    log "🔄 Reloading MCP proxy..."
    
    # Check if LaunchAgent exists
    if [ -f "$HOME_DIR/Library/LaunchAgents/com.ashishtandon.mcp-proxy.plist" ]; then
        # Reload LaunchAgent
        if launchctl reload "$HOME_DIR/Library/LaunchAgents/com.ashishtandon.mcp-proxy.plist"; then
            success "MCP proxy LaunchAgent reloaded"
        else
            warning "Failed to reload MCP proxy LaunchAgent"
        fi
        
        # Restart service
        if launchctl restart com.ashishtandon.mcp-proxy; then
            success "MCP proxy service restarted"
        else
            warning "Failed to restart MCP proxy service"
        fi
        
        # Wait for service to be ready
        log "Waiting for MCP proxy to be ready..."
        sleep 10
        
        # Check if proxy is listening
        if lsof -iTCP:8096 -sTCP:LISTEN -Pn > /dev/null 2>&1; then
            success "MCP proxy is listening on port 8096"
        else
            warning "MCP proxy is not listening on port 8096"
        fi
    else
        warning "MCP proxy LaunchAgent not found. Please set up mcp-proxy first."
    fi
}

# Test complete integration
test_complete_integration() {
    log "🧪 Testing complete integration..."
    
    # Test MCP proxy integration
    log "Testing MCP proxy integration..."
    if curl -s --max-time 10 "http://127.0.0.1:8096/servers/openmetadata/sse" > /dev/null; then
        success "MCP proxy OpenMetadata endpoint is accessible"
    else
        warning "MCP proxy OpenMetadata endpoint is not accessible"
    fi
    
    # Run comprehensive tests if available
    if [ -f "./test-mcp-connection.sh" ]; then
        log "Running comprehensive tests..."
        if ./test-mcp-connection.sh; then
            success "Comprehensive tests passed"
        else
            warning "Some comprehensive tests failed"
        fi
    else
        warning "Comprehensive test script not found"
    fi
}

# Display final status
display_final_status() {
    log "🎉 Setup process completed!"
    echo ""
    echo "🌐 Service Status:"
    echo "=================="
    docker-compose ps
    echo ""
    echo "🔍 Access Information:"
    echo "======================"
    echo "• 🆕 MONITORING DASHBOARD: http://localhost:8087 (MAIN MONITORING PAGE!)"
    echo "• Database: localhost:5432 (openpolicy/openpolicy)"
    echo "• Redis: localhost:6379"
    echo "• API Gateway: http://localhost:8080"
    echo "• User Service: http://localhost:8082"
    echo "• Elasticsearch: http://localhost:9200"
    echo "• OpenMetadata UI: http://localhost:8585 (admin@open-metadata.org / admin)"
    echo "• MCP Server: http://localhost:8084"
    echo "• Airflow: http://localhost:8083 (admin/admin)"
    echo "• Admin UI: http://localhost:3000"
    echo "• Web UI: http://localhost:3001"
    echo ""
    echo "🔧 MCP Integration:"
    echo "==================="
    echo "• MCP Server: Running on port 8084"
    echo "• MCP Protocol: Supported at /mcp and /mcp/sse"
    echo "• Cursor Integration: Configured in ~/.cursor/mcp.json"
    echo "• MCP Proxy: Should be running on port 8096"
    echo ""
    echo "🧪 Testing:"
    echo "==========="
    echo "• Run: ./test-mcp-connection.sh"
    echo "• Check logs: docker-compose logs -f [service-name]"
    echo "• Health check: ./health-check.sh"
}

# Main setup function
main() {
    log "🚀 Starting Complete OpenMetadata MCP Integration Setup..."
    echo ""
    
    # Run all setup steps
    check_prerequisites
    echo ""
    
    build_containers
    echo ""
    
    start_all_services
    echo ""
    
    test_database
    echo ""
    
    test_redis
    echo ""
    
    test_api_services
    echo ""
    
    test_openmetadata
    echo ""
    
    test_frontend
    echo ""
    
    auto_open_monitoring
    echo ""
    
    test_mcp_integration
    echo ""
    
    reload_mcp_proxy
    echo ""
    
    test_complete_integration
    echo ""
    
    display_final_status
}

# Handle script arguments
case "${1:-}" in
    "build")
        log "Building containers only..."
        check_prerequisites
        build_containers
        ;;
    "start")
        log "Starting services only..."
        check_prerequisites
        start_all_services
        echo ""
        auto_open_monitoring
        ;;
    "test")
        log "Running tests only..."
        test_database
        test_redis
        test_api_services
        test_openmetadata
        test_frontend
        test_mcp_integration
        ;;
    "mcp")
        log "Testing MCP integration only..."
        test_mcp_integration
        reload_mcp_proxy
        test_complete_integration
        ;;
    "full"|"")
        main
        ;;
    *)
        echo "Usage: $0 [build|start|test|mcp|full]"
        echo ""
        echo "Setup Options:"
        echo "  build     - Build containers only"
        echo "  start     - Start services only"
        echo "  test      - Run tests only"
        echo "  mcp       - Test MCP integration only"
        echo "  full      - Complete setup (default)"
        exit 1
        ;;
esac
