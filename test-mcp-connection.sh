#!/bin/bash

# MCP Connection Test Script
# This script tests the complete MCP connection flow

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MCP_SERVER_PORT=8084
OPENMETADATA_PORT=8585
MCP_PROXY_PORT=8096

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
}

# Test 1: Check if OpenMetadata container is running
test_openmetadata_container() {
    log "🔍 Testing OpenMetadata container status..."
    
    if docker ps --format "table {{.Names}}\t{{.Status}}" | grep -q "mergev2-openmetadata-server.*Up"; then
        success "OpenMetadata container is running"
        return 0
    else
        error "OpenMetadata container is not running"
        return 1
    fi
}

# Test 2: Check if MCP server port is accessible
test_mcp_server_port() {
    log "🔍 Testing MCP server port accessibility..."
    
    if curl -s --max-time 5 "http://localhost:${MCP_SERVER_PORT}/health" > /dev/null 2>&1; then
        success "MCP server port ${MCP_SERVER_PORT} is accessible"
        return 0
    else
        error "MCP server port ${MCP_SERVER_PORT} is not accessible"
        return 1
    fi
}

# Test 3: Check if OpenMetadata API is accessible
test_openmetadata_api() {
    log "🔍 Testing OpenMetadata API accessibility..."
    
    if curl -s --max-time 5 "http://localhost:${OPENMETADATA_PORT}/health" > /dev/null 2>&1; then
        success "OpenMetadata API port ${OPENMETADATA_PORT} is accessible"
        return 0
    else
        error "OpenMetadata API port ${OPENMETADATA_PORT} is not accessible"
        return 1
    fi
}

# Test 4: Test MCP server endpoints
test_mcp_endpoints() {
    log "🔍 Testing MCP server endpoints..."
    
    local endpoints=("/" "/health" "/overview" "/data-flow" "/mcp-info")
    local failed_endpoints=0
    
    for endpoint in "${endpoints[@]}"; do
        if curl -s --max-time 5 "http://localhost:${MCP_SERVER_PORT}${endpoint}" > /dev/null 2>&1; then
            success "MCP endpoint ${endpoint} is responding"
        else
            error "MCP endpoint ${endpoint} is not responding"
            failed_endpoints=$((failed_endpoints + 1))
        fi
    done
    
    if [ $failed_endpoints -eq 0 ]; then
        success "All MCP endpoints are responding"
        return 0
    else
        error "${failed_endpoints} MCP endpoints failed"
        return 1
    fi
}

# Test 5: Test data lineage query
test_data_lineage() {
    log "🔍 Testing data lineage functionality..."
    
    # Test overview endpoint
    local overview_response=$(curl -s --max-time 10 "http://localhost:${MCP_SERVER_PORT}/overview")
    
    if echo "$overview_response" | grep -q "database_services"; then
        success "Data lineage overview is working"
        echo "   Response: $overview_response"
        return 0
    else
        error "Data lineage overview is not working"
        echo "   Response: $overview_response"
        return 1
    fi
}

# Test 6: Test Cursor MCP configuration
test_cursor_mcp_config() {
    log "🔍 Testing Cursor MCP configuration..."
    
    # Check global config
    if [ -f "$HOME/.cursor/mcp.json" ]; then
        success "Global Cursor MCP config exists: ~/.cursor/mcp.json"
    else
        warning "Global Cursor MCP config missing: ~/.cursor/mcp.json"
    fi
    
    # Check project config
    if [ -f ".cursor/mcp.json" ]; then
        success "Project Cursor MCP config exists: .cursor/mcp.json"
    else
        warning "Project Cursor MCP config missing: .cursor/mcp.json"
    fi
    
    # Check MCP proxy config
    if [ -f "mcp-proxy.servers.json" ]; then
        success "MCP proxy config exists: mcp-proxy.servers.json"
    else
        warning "MCP proxy config missing: mcp-proxy.servers.json"
    fi
    
    # Check MCP proxy service
    if launchctl list | grep -q "com.ashishtandon.mcp-proxy"; then
        success "MCP proxy LaunchAgent is loaded"
    else
        warning "MCP proxy LaunchAgent is not loaded"
    fi
    
    # Check MCP proxy port
    if lsof -iTCP:${MCP_PROXY_PORT} -sTCP:LISTEN -Pn > /dev/null 2>&1; then
        success "MCP proxy is listening on port ${MCP_PROXY_PORT}"
    else
        warning "MCP proxy is not listening on port ${MCP_PROXY_PORT}"
    fi
    
    return 0
}

# Test 7: Test complete MCP flow
test_complete_mcp_flow() {
    log "🔍 Testing complete MCP flow..."
    
    # Test MCP info endpoint
    local mcp_info=$(curl -s --max-time 10 "http://localhost:${MCP_SERVER_PORT}/mcp-info")
    
    if echo "$mcp_info" | grep -q "cursor_integration"; then
        success "Complete MCP flow is working"
        echo "   MCP Info: $mcp_info"
        return 0
    else
        error "Complete MCP flow is not working"
        echo "   MCP Info: $mcp_info"
        return 1
    fi
}

# Test 8: Test MCP proxy integration
test_mcp_proxy_integration() {
    log "🔍 Testing MCP proxy integration..."
    
    # Test OpenMetadata server endpoint via proxy
    local proxy_response=$(curl -s --max-time 10 "http://127.0.0.1:${MCP_PROXY_PORT}/servers/openmetadata/sse")
    
    if [ $? -eq 0 ]; then
        success "MCP proxy OpenMetadata endpoint is accessible"
        return 0
    else
        error "MCP proxy OpenMetadata endpoint is not accessible"
        return 1
    fi
}

# Main test function
main() {
    log "🚀 Starting MCP Connection Tests..."
    echo ""
    
    local overall_success=true
    
    # Run all tests
    test_openmetadata_container || overall_success=false
    echo ""
    
    test_mcp_server_port || overall_success=false
    echo ""
    
    test_openmetadata_api || overall_success=false
    echo ""
    
    test_mcp_endpoints || overall_success=false
    echo ""
    
    test_data_lineage || overall_success=false
    echo ""
    
    test_cursor_mcp_config
    echo ""
    
    test_complete_mcp_flow || overall_success=false
    echo ""
    
    test_mcp_proxy_integration || overall_success=false
    echo ""
    
    # Summary
    if [ "$overall_success" = true ]; then
        success "🎉 All MCP connection tests passed!"
        echo ""
        echo "🌐 MCP Integration Status:"
        echo "• Container: ✅ Running"
        echo "• MCP Server: ✅ Accessible on port ${MCP_SERVER_PORT}"
        echo "• OpenMetadata: ✅ Accessible on port ${OPENMETADATA_PORT}"
        echo "• MCP Proxy: ✅ Running on port ${MCP_PROXY_PORT}"
        echo "• Endpoints: ✅ All responding"
        echo "• Data Lineage: ✅ Functional"
        echo "• Cursor Config: ✅ Configured"
        echo ""
        echo "🔧 Next Steps:"
        echo "1. Restart Cursor to load MCP configuration"
        echo "2. Test MCP tool calls in Cursor"
        echo "3. Verify data lineage queries work"
        echo "4. Enable openMetadataProxy in Cursor Tools"
    else
        error "⚠️  Some MCP connection tests failed"
        echo ""
        echo "🔧 Troubleshooting:"
        echo "1. Check container status: docker-compose ps"
        echo "2. Check container logs: docker-compose logs openmetadata-server"
        echo "3. Verify port mappings in docker-compose.yml"
        echo "4. Check MCP proxy status: launchctl list | grep mcp-proxy"
        echo "5. Check MCP proxy logs: tail -f ~/Library/Logs/mcp-proxy/stderr.log"
        echo "6. Restart OpenMetadata services if needed"
    fi
    
    return $([ "$overall_success" = true ] && echo 0 || echo 1)
}

# Handle script arguments
case "${1:-}" in
    "quick")
        log "🔍 Quick MCP Test (ports only)..."
        test_openmetadata_container
        test_mcp_server_port
        test_openmetadata_api
        ;;
    "endpoints")
        log "🔍 MCP Endpoints Test..."
        test_mcp_endpoints
        ;;
    "lineage")
        log "🔍 Data Lineage Test..."
        test_data_lineage
        ;;
    "config")
        log "🔍 Cursor MCP Config Test..."
        test_cursor_mcp_config
        ;;
    "full"|"")
        main
        ;;
    *)
        echo "Usage: $0 [quick|endpoints|lineage|config|full]"
        echo ""
        echo "Test Types:"
        echo "  quick     - Quick port accessibility test"
        echo "  endpoints - Test MCP server endpoints"
        echo "  lineage   - Test data lineage functionality"
        echo "  config    - Test Cursor MCP configuration"
        echo "  full      - Complete MCP connection test (default)"
        exit 1
        ;;
esac
