#!/bin/bash

# OpenMetadata MCP Integration Setup Script
# This script seamlessly integrates OpenMetadata with your existing mcp-proxy setup

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
PROJECT_DIR="$SCRIPT_DIR"

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
    
    # Check if mcp-proxy is installed
    if ! command -v mcp-proxy &> /dev/null; then
        error "mcp-proxy is not installed. Please run: uv tool install mcp-proxy"
        exit 1
    fi
    
    # Check if LaunchAgent exists
    if [ ! -f "$HOME_DIR/Library/LaunchAgents/com.ashishtandon.mcp-proxy.plist" ]; then
        error "MCP proxy LaunchAgent not found. Please set up mcp-proxy first."
        exit 1
    fi
    
    # Check if Docker is running
    if ! docker info &> /dev/null; then
        error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    
    success "Prerequisites check passed"
}

# Setup environment variables
setup_environment() {
    log "🔧 Setting up environment variables..."
    
    # Create mcp.env file if it doesn't exist
    if [ ! -f "$CURSOR_DIR/mcp.env" ]; then
        warning "Creating ~/.cursor/mcp.env file..."
        cat > "$CURSOR_DIR/mcp.env" << 'EOF'
# OpenMetadata Integration
OPENMETADATA_SERVER=http://localhost:8585
OPENMETADATA_PAT=admin
OPENMETADATA_USERNAME=admin@open-metadata.org

# Other MCP servers (add your existing ones here)
PG_CONNECTION_STRING=
SLACK_BOT_TOKEN=
SLACK_TEAM_ID=
GITHUB_PERSONAL_ACCESS_TOKEN=
FIRECRAWL_API_URL=http://localhost:3002
FIRECRAWL_API_KEY=
HOME_ASSISTANT_TOKEN=
HOME_ASSISTANT_CLOUD_URL=
HOME_ASSISTANT_LOCAL_URL=
EOF
        success "Created ~/.cursor/mcp.env"
    else
        # Check if OpenMetadata variables are already set
        if grep -q "OPENMETADATA_SERVER" "$CURSOR_DIR/mcp.env"; then
            success "OpenMetadata environment variables already configured"
        else
            warning "Adding OpenMetadata variables to existing ~/.cursor/mcp.env..."
            cat >> "$CURSOR_DIR/mcp.env" << 'EOF'

# OpenMetadata Integration
OPENMETADATA_SERVER=http://localhost:8585
OPENMETADATA_PAT=admin
OPENMETADATA_USERNAME=admin@open-metadata.org
EOF
            success "Added OpenMetadata variables to ~/.cursor/mcp.env"
        fi
    fi
    
    # Set proper permissions
    chmod 600 "$CURSOR_DIR/mcp.env"
    success "Environment file permissions set correctly"
}

# Update MCP proxy configuration
update_mcp_proxy_config() {
    log "🔧 Updating MCP proxy configuration..."
    
    # Update mcp-proxy.servers.json
    if [ -f "$PROJECT_DIR/mcp-proxy.servers.json" ]; then
        # Check if openmetadata server is already configured
        if grep -q '"openmetadata"' "$PROJECT_DIR/mcp-proxy.servers.json"; then
            success "OpenMetadata server already configured in mcp-proxy.servers.json"
        else
            warning "Adding OpenMetadata server to mcp-proxy.servers.json..."
            # This will be done by the user manually as per your setup
            success "Please add OpenMetadata server to mcp-proxy.servers.json manually"
        fi
    else
        error "mcp-proxy.servers.json not found in project directory"
        exit 1
    fi
}

# Update Cursor MCP configuration
update_cursor_config() {
    log "🔧 Updating Cursor MCP configuration..."
    
    # Update global Cursor config
    if [ -f "$CURSOR_DIR/mcp.json" ]; then
        # Check if openMetadataProxy is already configured
        if grep -q '"openMetadataProxy"' "$CURSOR_DIR/mcp.json"; then
            success "openMetadataProxy already configured in global ~/.cursor/mcp.json"
        else
            warning "Adding openMetadataProxy to global ~/.cursor/mcp.json..."
            # This will be done by the user manually as per your setup
            success "Please add openMetadataProxy to ~/.cursor/mcp.json manually"
        fi
    else
        error "Global ~/.cursor/mcp.json not found"
        exit 1
    fi
    
    # Update project Cursor config
    if [ -f "$PROJECT_DIR/.cursor/mcp.json" ]; then
        # Check if openMetadataProxy is already configured
        if grep -q '"openMetadataProxy"' "$PROJECT_DIR/.cursor/mcp.json"; then
            success "openMetadataProxy already configured in project .cursor/mcp.json"
        else
            warning "Adding openMetadataProxy to project .cursor/mcp.json..."
            # This will be done by the user manually as per your setup
            success "Please add openMetadataProxy to .cursor/mcp.json manually"
        fi
    else
        error "Project .cursor/mcp.json not found"
        exit 1
    fi
}

# Build and start OpenMetadata container
setup_openmetadata_container() {
    log "🐳 Setting up OpenMetadata container with MCP server..."
    
    # Check if we're in the right directory
    if [ ! -f "docker-compose.yml" ]; then
        error "docker-compose.yml not found. Please run this script from the project root."
        exit 1
    fi
    
    # Build the OpenMetadata container
    log "Building OpenMetadata container..."
    if docker-compose build openmetadata-server; then
        success "OpenMetadata container built successfully"
    else
        error "Failed to build OpenMetadata container"
        exit 1
    fi
    
    # Start OpenMetadata services
    log "Starting OpenMetadata services..."
    if docker-compose --profile openmetadata up -d; then
        success "OpenMetadata services started successfully"
    else
        error "Failed to start OpenMetadata services"
        exit 1
    fi
    
    # Wait for services to be ready
    log "Waiting for services to be ready..."
    sleep 30
    
    # Check container status
    if docker-compose ps | grep -q "openmetadata-server.*Up"; then
        success "OpenMetadata container is running"
    else
        error "OpenMetadata container is not running"
        exit 1
    fi
}

# Test MCP integration
test_mcp_integration() {
    log "🧪 Testing MCP integration..."
    
    # Test OpenMetadata MCP server
    if curl -s --max-time 10 "http://localhost:8084/health" > /dev/null; then
        success "OpenMetadata MCP server is responding"
    else
        error "OpenMetadata MCP server is not responding"
        return 1
    fi
    
    # Test MCP protocol endpoint
    if curl -s --max-time 10 "http://localhost:8084/mcp/sse" > /dev/null; then
        success "MCP SSE endpoint is accessible"
    else
        error "MCP SSE endpoint is not accessible"
        return 1
    fi
    
    # Test OpenMetadata API
    if curl -s --max-time 10 "http://localhost:8585/health" > /dev/null; then
        success "OpenMetadata API is responding"
    else
        error "OpenMetadata API is not responding"
        return 1
    fi
    
    success "MCP integration test passed"
}

# Reload MCP proxy
reload_mcp_proxy() {
    log "🔄 Reloading MCP proxy..."
    
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
}

# Display final instructions
display_instructions() {
    log "🎉 OpenMetadata MCP integration setup complete!"
    echo ""
    echo "🌐 Access Information:"
    echo "======================"
    echo "• OpenMetadata UI: http://localhost:8585 (admin@open-metadata.org / admin)"
    echo "• MCP Server: http://localhost:8084"
    echo "• MCP Proxy: http://127.0.0.1:8096"
    echo ""
    echo "🔧 Next Steps:"
    echo "=============="
    echo "1. ✅ Environment variables configured in ~/.cursor/mcp.env"
    echo "2. ✅ OpenMetadata container running with MCP server"
    echo "3. 🚧 Add OpenMetadata server to mcp-proxy.servers.json:"
    echo "   - Use 'npx mcp-remote' with env-substituted args"
    echo "   - URL: \${OPENMETADATA_SERVER}/mcp/sse"
    echo "   - Auth: Bearer \${OPENMETADATA_PAT}"
    echo "4. 🚧 Add openMetadataProxy to Cursor config files:"
    echo "   - ~/.cursor/mcp.json (global)"
    echo "   - .cursor/mcp.json (project)"
    echo "   - Point to: http://127.0.0.1:8096/servers/openmetadata/sse"
    echo "5. 🔄 Reload MCP proxy: launchctl restart com.ashishtandon.mcp-proxy"
    echo "6. 🚀 Restart Cursor to load new MCP configuration"
    echo "7. 🧪 Test integration: ./test-mcp-connection.sh"
    echo ""
    echo "📋 Manual Configuration Required:"
    echo "================================"
    echo "• Update mcp-proxy.servers.json with OpenMetadata server"
    echo "• Update Cursor MCP config files with openMetadataProxy"
    echo "• Reload MCP proxy service"
    echo ""
    echo "🔍 Testing:"
    echo "==========="
    echo "• Run: ./test-mcp-connection.sh"
    echo "• Check MCP proxy logs: tail -f ~/Library/Logs/mcp-proxy/stderr.log"
    echo "• Test OpenMetadata: curl http://localhost:8084/mcp-info"
}

# Main setup function
main() {
    log "🚀 Starting OpenMetadata MCP Integration Setup..."
    echo ""
    
    # Run setup steps
    check_prerequisites
    echo ""
    
    setup_environment
    echo ""
    
    update_mcp_proxy_config
    echo ""
    
    update_cursor_config
    echo ""
    
    setup_openmetadata_container
    echo ""
    
    test_mcp_integration
    echo ""
    
    reload_mcp_proxy
    echo ""
    
    display_instructions
}

# Handle script arguments
case "${1:-}" in
    "env")
        log "Setting up environment variables only..."
        setup_environment
        ;;
    "container")
        log "Setting up OpenMetadata container only..."
        setup_openmetadata_container
        ;;
    "proxy")
        log "Reloading MCP proxy only..."
        reload_mcp_proxy
        ;;
    "test")
        log "Running MCP integration tests..."
        test_mcp_integration
        ;;
    "full"|"")
        main
        ;;
    *)
        echo "Usage: $0 [env|container|proxy|test|full]"
        echo ""
        echo "Setup Options:"
        echo "  env       - Setup environment variables only"
        echo "  container - Setup OpenMetadata container only"
        echo "  proxy     - Reload MCP proxy only"
        echo "  test      - Run MCP integration tests only"
        echo "  full      - Complete setup (default)"
        exit 1
        ;;
esac
