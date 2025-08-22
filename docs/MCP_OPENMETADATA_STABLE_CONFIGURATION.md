# MCP OpenMetadata Stable Configuration Guide

## 🚨 CRITICAL: Settings That Must Remain Untouched

This document outlines the **stable, working configuration** for your OpenMetadata MCP integration. **DO NOT CHANGE** these settings unless you have a specific reason and understand the implications.

## 📁 File Locations & Permissions

### 1. Core MCP Configuration Files
```
.cursor/mcp.json                    # Cursor's local MCP config - DO NOT MODIFY
mcp-openmetadata-server.py          # Core MCP server script - DO NOT MODIFY
mcp-env/                           # Python virtual environment - DO NOT DELETE
requirements-mcp.txt                # Python dependencies - DO NOT MODIFY
```

### 2. System-Level MCP Files (DO NOT TOUCH)
```
/Users/ashishtandon/Github/CursorMCP/           # Original MCP setup - PRESERVE
/Users/ashishtandon/.local/bin/mcp-proxy        # System MCP proxy - PRESERVE
~/Library/LaunchAgents/com.ashishtandon.mcp-proxy.plist  # LaunchAgent - PRESERVE
```

## ⚙️ Configuration Settings That Must Stay Unchanged

### 1. Environment Variables (DO NOT MODIFY)
```bash
OPENMETADATA_SERVER_URL=http://localhost:8585
OPENMETADATA_AUTH_TOKEN=admin
OPENMETADATA_USERNAME=admin@open-metadata.org
```

**Why These Must Stay:** These are hardcoded in your OpenMetadata server configuration and changing them will break the connection.

### 2. Port Assignments (DO NOT MODIFY)
```
OpenMetadata Server: 8585
MCP Server: 8084 (if using Docker)
MCP Proxy: 8096 (system default)
```

**Why These Must Stay:** These ports are configured in your Docker Compose and system services. Changing them requires updating multiple configuration files.

### 3. Python Dependencies (DO NOT MODIFY)
```
requests>=2.31.0
flask>=2.3.0
flask-cors>=4.0.0
```

**Why These Must Stay:** These are the minimum required packages for your MCP server to function. Removing any will cause import errors.

## 🔒 Docker Compose Settings (DO NOT MODIFY)

### OpenMetadata Service Configuration
```yaml
# These environment variables MUST remain exactly as configured:
environment:
  - DB_DRIVER_CLASS=org.postgresql.Driver
  - DB_SCHEME=postgresql
  - DB_PARAMS=allowPublicKeyRetrieval=true&useSSL=false&serverTimezone=UTC
  - DB_USER=openpolicy
  - DB_USER_PASSWORD=openpolicy
  - DB_HOST=db
  - DB_PORT=5432
  - OM_DATABASE=openmetadata
  - ELASTICSEARCH_HOST=elasticsearch
  - ELASTICSEARCH_PORT=9200
  - ELASTICSEARCH_SCHEME=http
  - ELASTICSEARCH_USER=elastic
  - ELASTICSEARCH_PASSWORD=changeme
  - OPENMETADATA_CLUSTER_NAME=openmetadata
  - SERVER_PORT=8585
  - LOG_LEVEL=INFO
  - AUTHORIZER_CLASS_NAME=org.openmetadata.service.security.DefaultAuthorizer
  - AUTHORIZER_REQUEST_FILTER=org.openmetadata.service.security.JwtFilter
  - AUTHORIZER_ADMIN_PRINCIPALS=[admin]
  - AUTHORIZER_ALLOWED_REGISTRATION_DOMAIN=["all"]
  - AUTHENTICATION_PROVIDER=basic
  - AUTHENTICATION_RESPONSE_TYPE=id_token
  - AUTHENTICATION_ENABLE_SELF_SIGNUP=true
  - MIGRATION_LIMIT_PARAM=1200
```

**Why These Must Stay:** These settings ensure OpenMetadata connects to PostgreSQL instead of MySQL and properly initializes the database schema.

## 🚫 What You Should NEVER Change

### 1. Database Configuration
- **NEVER** change `DB_DRIVER_CLASS` from `org.postgresql.Driver`
- **NEVER** change `DB_SCHEME` from `postgresql`
- **NEVER** change `DB_HOST` from `db` (Docker service name)
- **NEVER** change `OM_DATABASE` from `openmetadata`

### 2. Authentication Settings
- **NEVER** change `OPENMETADATA_AUTH_TOKEN` from `admin`
- **NEVER** change `OPENMETADATA_USERNAME` from `admin@open-metadata.org`
- **NEVER** change `AUTHENTICATION_PROVIDER` from `basic`

### 3. Port Mappings
- **NEVER** change the `8585` port for OpenMetadata
- **NEVER** change the `5432` port for PostgreSQL
- **NEVER** change the `9200` port for Elasticsearch

### 4. Service Dependencies
- **NEVER** remove the `depends_on` relationships in Docker Compose
- **NEVER** change the service names (`db`, `elasticsearch`, `openmetadata-server`)

## ✅ What You CAN Safely Modify

### 1. Log Levels
```yaml
- LOG_LEVEL=INFO  # Can be changed to DEBUG, WARN, or ERROR
```

### 2. Timeout Values
```yaml
- MIGRATION_LIMIT_PARAM=1200  # Can be increased if migrations are slow
```

### 3. UI Customizations
- Nginx configurations for admin-ui and web-ui
- Health endpoint responses
- Static file serving

### 4. MCP Server Enhancements
- Adding new MCP methods to `mcp-openmetadata-server.py`
- Adding new data extraction capabilities
- Improving error handling and logging

## 🚨 Troubleshooting: When Things Break

### If OpenMetadata Won't Start
1. **Check the database connection** - Ensure PostgreSQL is running
2. **Verify environment variables** - All must match exactly
3. **Check port conflicts** - Ensure 8585 is not in use
4. **Review logs** - Use `docker logs openmetadata-server`

### If MCP Connection Fails
1. **Verify OpenMetadata is running** - Check `http://localhost:8585`
2. **Check Python environment** - Ensure `mcp-env` is activated
3. **Verify dependencies** - Run `pip list` in `mcp-env`
4. **Test direct connection** - Use the test script

### If Docker Services Won't Start
1. **Clean up Docker state** - Run `docker-compose down`
2. **Remove lingering containers** - `docker rm -f $(docker ps -aq)`
3. **Remove networks** - `docker network rm openpolicy-network`
4. **Restart fresh** - `docker-compose up -d`

## 📋 Configuration Validation Checklist

Before making ANY changes, verify these are correct:

- [ ] OpenMetadata server accessible at `http://localhost:8585`
- [ ] PostgreSQL running and accessible to OpenMetadata
- [ ] Elasticsearch running and accessible to OpenMetadata
- [ ] MCP server can import required Python modules
- [ ] Environment variables match exactly
- [ ] Port assignments are correct
- [ ] Docker services have proper dependencies

## 🔄 Safe Modification Process

If you MUST make changes:

1. **Document current state** - Take screenshots or notes
2. **Make ONE change at a time** - Don't change multiple things
3. **Test immediately** - Verify the change works
4. **Rollback if needed** - Revert to the last working state
5. **Update this document** - Keep it current with working configuration

## 📞 Emergency Contacts

If you break something and can't fix it:

1. **Check this document first** - Look for what you might have changed
2. **Review recent changes** - What did you modify last?
3. **Use the troubleshooting section** - Follow the steps above
4. **Restore from backup** - Use your last known working configuration

## 🎯 Summary

**The golden rule:** If it's working, don't fix it. Your OpenMetadata MCP integration is currently stable and functional. The settings documented above have been tested and proven to work together. Changing any of these "untouchable" settings will likely break your system and require troubleshooting to restore functionality.

**Remember:** The goal is to have a working system, not a perfect configuration. Focus on using the system rather than optimizing it unless you have a specific need.
