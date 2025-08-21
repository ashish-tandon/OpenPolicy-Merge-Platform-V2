# 🔗 MCP Integration Setup Guide

## 🎯 **Overview**
This guide explains how to set up the Model Context Protocol (MCP) integration between Cursor, the MCP server running in the OpenMetadata container, and the OpenMetadata API.

## 🔄 **Connection Flow Architecture**

```
Cursor → MCP Proxy (laptop) → MCP Server (container:8084) → OpenMetadata API (container:8585)
```

### **Step-by-Step Flow:**
1. **Cursor** reads MCP configuration from `~/.cursor/mcp.json` or `.cursor/mcp.json`
2. **MCP Proxy** (if configured) forwards requests to the container
3. **MCP Server** (port 8084) receives requests and processes them
4. **MCP Server** calls **OpenMetadata API** (port 8585) to get data lineage
5. **MCP Server** returns formatted responses back to Cursor

## 📁 **Configuration Files**

### **1. Global Cursor MCP Config** (`~/.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "openmetadata": {
      "command": "curl",
      "args": ["-s", "http://localhost:8084/mcp-info"],
      "env": {
        "MCP_SERVER_URL": "http://localhost:8084"
      }
    }
  }
}
```

### **2. Project Cursor MCP Config** (`.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "openmetadata": {
      "command": "curl",
      "args": ["-s", "http://localhost:8084/mcp-info"],
      "env": {
        "MCP_SERVER_URL": "http://localhost:8084"
      }
    }
  }
}
```

### **3. MCP Proxy Config** (`mcp-proxy.servers.json`)
```json
{
  "mcpServers": {
    "openmetadata": {
      "command": "curl",
      "args": ["-s", "http://localhost:8084/mcp-info"],
      "env": {
        "MCP_SERVER_URL": "http://localhost:8084",
        "MCP_PROXY_HOST": "localhost",
        "MCP_PROXY_PORT": "8085"
      }
    }
  },
  "proxy": {
    "enabled": true,
    "host": "localhost",
    "port": 8085,
    "target": "http://localhost:8084"
  }
}
```

## 🐳 **Container Configuration**

### **Dockerfile.mcp**
The container is configured with:
- **Base Image**: `openmetadata/server:1.9.1` (Alpine-based)
- **MCP Server Port**: 8084
- **Python Virtual Environment**: `/opt/mcp-venv`
- **Dependencies**: FastAPI, uvicorn, requests, pydantic

### **Port Mappings**
```yaml
# In docker-compose.yml
openmetadata-server:
  ports:
    - "8585:8585"    # OpenMetadata UI
    - "8084:8084"    # MCP Server
```

## 🚀 **Setup Instructions**

### **Phase 1: Container Setup**
1. **Build the container**:
   ```bash
   docker-compose build openmetadata-server
   ```

2. **Start OpenMetadata services**:
   ```bash
   docker-compose --profile openmetadata up -d
   ```

3. **Wait for services to be ready**:
   ```bash
   # Check container status
   docker-compose ps
   
   # Check MCP server health
   curl http://localhost:8084/health
   ```

### **Phase 2: Cursor Configuration**
1. **Copy global config**:
   ```bash
   cp global-cursor-mcp.json ~/.cursor/mcp.json
   ```

2. **Verify project config**:
   ```bash
   ls -la .cursor/mcp.json
   ```

3. **Restart Cursor** to load MCP configuration

### **Phase 3: Testing**
1. **Run connection test**:
   ```bash
   ./test-mcp-connection.sh
   ```

2. **Test MCP endpoints**:
   ```bash
   # MCP Info
   curl http://localhost:8084/mcp-info
   
   # Health Check
   curl http://localhost:8084/health
   
   # Data Flow
   curl http://localhost:8084/data-flow
   ```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **1. Container Not Starting**
```bash
# Check logs
docker-compose logs openmetadata-server

# Check port conflicts
netstat -tulpn | grep :8084
```

#### **2. MCP Server Not Responding**
```bash
# Check if container is running
docker ps | grep openmetadata

# Check MCP server logs
docker-compose exec openmetadata-server tail -f /opt/mcp-server/mcp-server.log
```

#### **3. Cursor Not Connecting**
```bash
# Verify MCP config exists
ls -la ~/.cursor/mcp.json

# Test MCP server manually
curl http://localhost:8084/mcp-info

# Restart Cursor completely
```

### **Debug Commands**
```bash
# Check all MCP-related processes
ps aux | grep mcp

# Check network connectivity
telnet localhost 8084

# Check Docker network
docker network ls
docker network inspect mergev2_default
```

## 📊 **MCP Server Endpoints**

### **Available Endpoints**
- **`/`** - Root endpoint with server info
- **`/health`** - Health check with OpenMetadata status
- **`/overview`** - Platform overview and statistics
- **`/data-flow`** - Complete data flow mapping
- **`/search`** - Search for entities in OpenMetadata
- **`/lineage`** - Get data lineage for specific entity
- **`/field-lineage`** - Get lineage for specific field
- **`/mcp-info`** - MCP server information for Cursor

### **Example API Calls**
```bash
# Get platform overview
curl http://localhost:8084/overview

# Search for tables
curl -X POST http://localhost:8084/search \
  -H "Content-Type: application/json" \
  -d '{"query": "bills"}'

# Get data lineage
curl -X POST http://localhost:8084/lineage \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "table_id_here"}'
```

## 🔄 **Data Lineage Integration**

### **What Gets Connected**
1. **Data Sources** → **Scrapers** → **Raw Data**
2. **Raw Data** → **ETL** → **Structured Data**
3. **Structured Data** → **Database Tables**
4. **Database Tables** → **API Endpoints**
5. **API Endpoints** → **UI Components**

### **Example Lineage Query**
```bash
# Get lineage for bills table
curl -X POST http://localhost:8084/field-lineage \
  -H "Content-Type: application/json" \
  -d '{"table_name": "bills_bill", "field_name": "title"}'
```

## 🎯 **Next Steps**

### **Immediate Actions**
1. ✅ Build and start OpenMetadata container
2. ✅ Configure Cursor MCP settings
3. ✅ Test MCP server connectivity
4. ✅ Verify data lineage queries

### **Short Term (Next 24 hours)**
1. 🚧 Test MCP tool calls in Cursor
2. 🚧 Verify data lineage accuracy
3. 🚧 Set up monitoring and alerts
4. 🚧 Document any issues found

### **Medium Term (Next week)**
1. 📋 Optimize MCP server performance
2. 📋 Add more data lineage sources
3. 📋 Implement automated testing
4. 📋 Production deployment preparation

## 📞 **Support**

### **If MCP Integration Fails**
1. Check container logs: `docker-compose logs openmetadata-server`
2. Verify port accessibility: `curl http://localhost:8084/health`
3. Test OpenMetadata API: `curl http://localhost:8585/health`
4. Check Cursor configuration: `cat ~/.cursor/mcp.json`

### **Useful Commands**
```bash
# Full system status
./health-check.sh

# MCP connection test
./test-mcp-connection.sh

# Service management
docker-compose ps
docker-compose logs -f [service-name]
docker-compose restart [service-name]
```

---

**🎉 Congratulations!** You now have a complete MCP integration setup that connects Cursor to your OpenMetadata data lineage system.
