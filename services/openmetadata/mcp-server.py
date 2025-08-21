#!/usr/bin/env python3
"""
OpenMetadata MCP Server for Cursor Integration
This server runs inside the OpenMetadata container and provides data lineage information
Supports both HTTP endpoints and MCP protocol for mcp-remote integration
"""

import json
import requests
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn
import asyncio
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(title="OpenMetadata MCP Server", version="1.0.0")

class OpenMetadataMCPServer:
    """MCP Server for OpenMetadata integration with Cursor"""
    
    def __init__(self):
        # Inside container, use localhost for OpenMetadata
        self.openmetadata_url = "http://localhost:8585"
        self.auth_token = "admin"
        self.username = "admin@open-metadata.org"
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
    def get_data_lineage(self, entity_id: str) -> Dict[str, Any]:
        """Get data lineage for a specific entity"""
        try:
            url = f"{self.openmetadata_url}/api/v1/lineage/table/{entity_id}"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting lineage for {entity_id}: {e}")
            return {"error": str(e)}
    
    def search_entities(self, query: str) -> List[Dict[str, Any]]:
        """Search for entities in OpenMetadata"""
        try:
            url = f"{self.openmetadata_url}/api/v1/search/query"
            payload = {
                "query": query,
                "index": "table_search_index"
            }
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            logger.error(f"Error searching entities: {e}")
            return []
    
    def get_table_details(self, table_id: str) -> Dict[str, Any]:
        """Get detailed information about a table"""
        try:
            url = f"{self.openmetadata_url}/api/v1/tables/{table_id}"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting table details for {table_id}: {e}")
            return {"error": str(e)}
    
    def get_platform_overview(self) -> Dict[str, Any]:
        """Get overview of the entire platform"""
        try:
            # Get database services
            db_services_url = f"{self.openmetadata_url}/api/v1/services/databaseServices"
            db_response = requests.get(db_services_url, headers=self.headers, timeout=30)
            db_services = db_response.json().get("data", []) if db_response.ok else []
            
            # Get tables
            tables_url = f"{self.openmetadata_url}/api/v1/tables"
            tables_response = requests.get(tables_url, headers=self.headers, timeout=30)
            tables = tables_response.json().get("data", []) if tables_response.ok else []
            
            return {
                "database_services": len(db_services),
                "total_tables": len(tables),
                "last_updated": datetime.now().isoformat(),
                "status": "healthy"
            }
        except Exception as e:
            logger.error(f"Error getting platform overview: {e}")
            return {"error": str(e)}
    
    def get_data_flow_mapping(self) -> Dict[str, Any]:
        """Get complete data flow mapping for the platform"""
        return {
            "data_sources": {
                "scrapers": [
                    "CA_AB_Calgary (https://calgary.ca)",
                    "CA_AB_Edmonton (https://edmonton.ca)",
                    "CA_BC_Vancouver (https://vancouver.ca)",
                    "CA_ON_Toronto (https://toronto.ca)"
                ],
                "databases": [
                    "PostgreSQL (openpolicy schema)",
                    "PostgreSQL (public schema)"
                ]
            },
            "data_flow": {
                "extraction": "Web scrapers extract data from municipal websites",
                "transformation": "Data mapping library transforms raw data",
                "storage": "PostgreSQL stores structured data",
                "api": "API Gateway exposes data via REST endpoints",
                "ui": "Web UI components consume and display data"
            },
            "key_tables": {
                "bills_bill": "Parliamentary bills and legislation",
                "core_politician": "Politician information",
                "core_party": "Political party information",
                "core_session": "Parliamentary session information",
                "core_electedmember": "Elected member information"
            },
            "api_endpoints": [
                "/api/v1/bills",
                "/api/v1/members",
                "/api/v1/sessions",
                "/api/v1/committees",
                "/api/v1/debates"
            ],
            "ui_components": [
                "BillsList (services/web-ui/src/app/bills/page.tsx)",
                "BillDetail (services/web-ui/src/app/bills/[session]/[number]/page.tsx)",
                "MembersList (services/web-ui/src/app/members/page.tsx)",
                "CommitteesList (services/web-ui/src/app/committees/page.tsx)"
            ]
        }
    
    def get_lineage_for_field(self, table_name: str, field_name: str) -> Dict[str, Any]:
        """Get lineage information for a specific field"""
        try:
            # Search for the table
            tables = self.search_entities(f"table:{table_name}")
            if not tables:
                return {"error": f"Table {table_name} not found"}
            
            table_id = tables[0].get("id")
            if not table_id:
                return {"error": "Table ID not found"}
            
            # Get table details
            table_details = self.get_table_details(table_id)
            if "error" in table_details:
                return table_details
            
            # Find the field
            columns = table_details.get("columns", [])
            field_info = None
            for col in columns:
                if col.get("name") == field_name:
                    field_info = col
                    break
            
            if not field_info:
                return {"error": f"Field {field_name} not found in table {table_name}"}
            
            # Get lineage for the table
            lineage = self.get_data_lineage(table_id)
            
            return {
                "table": table_name,
                "field": field_name,
                "field_info": field_info,
                "lineage": lineage,
                "data_flow": self.get_data_flow_mapping()
            }
        except Exception as e:
            logger.error(f"Error getting lineage for field {field_name} in {table_name}: {e}")
            return {"error": str(e)}

# Initialize server
server = OpenMetadataMCPServer()

# API Models
class SearchRequest(BaseModel):
    query: str

class LineageRequest(BaseModel):
    entity_id: str

class FieldLineageRequest(BaseModel):
    table_name: str
    field_name: str

# MCP Protocol Support
class MCPMessage(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None

def create_mcp_response(request_id: str, result: Any = None, error: Dict[str, Any] = None) -> str:
    """Create an MCP protocol response"""
    response = {
        "jsonrpc": "2.0",
        "id": request_id
    }
    
    if error:
        response["error"] = error
    else:
        response["result"] = result
    
    return json.dumps(response) + "\n"

def create_mcp_notification(method: str, params: Dict[str, Any] = None) -> str:
    """Create an MCP protocol notification"""
    notification = {
        "jsonrpc": "2.0",
        "method": method
    }
    
    if params:
        notification["params"] = params
    
    return json.dumps(notification) + "\n"

# MCP Protocol Endpoints
@app.get("/mcp/sse")
async def mcp_sse():
    """MCP Server-Sent Events endpoint for mcp-remote"""
    
    async def event_stream():
        # Send initial connection message
        yield create_mcp_notification("mcp.server.ready", {
            "server": "openmetadata-mcp",
            "version": "1.0.0"
        })
        
        # Keep connection alive
        while True:
            await asyncio.sleep(30)
            yield create_mcp_notification("mcp.server.ping", {"timestamp": datetime.now().isoformat()})
    
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """MCP protocol endpoint for direct communication"""
    try:
        body = await request.json()
        mcp_message = MCPMessage(**body)
        
        if mcp_message.method == "initialize":
            # Handle MCP initialization
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {},
                    "prompts": {}
                },
                "serverInfo": {
                    "name": "openmetadata-mcp",
                    "version": "1.0.0"
                }
            }
            return create_mcp_response(mcp_message.id, result)
        
        elif mcp_message.method == "tools/list":
            # List available tools
            result = {
                "tools": [
                    {
                        "name": "get_data_lineage",
                        "description": "Get data lineage for an entity",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "entity_id": {"type": "string", "description": "Entity ID to get lineage for"}
                            },
                            "required": ["entity_id"]
                        }
                    },
                    {
                        "name": "search_entities",
                        "description": "Search for entities in OpenMetadata",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Search query"}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "get_platform_overview",
                        "description": "Get platform overview and statistics",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }
                ]
            }
            return create_mcp_response(mcp_message.id, result)
        
        elif mcp_message.method == "tools/call":
            # Handle tool calls
            tool_name = mcp_message.params.get("name")
            arguments = mcp_message.params.get("arguments", {})
            
            if tool_name == "get_data_lineage":
                entity_id = arguments.get("entity_id")
                if entity_id:
                    result = server.get_data_lineage(entity_id)
                    return create_mcp_response(mcp_message.id, result)
                else:
                    error = {"code": -32602, "message": "Missing entity_id parameter"}
                    return create_mcp_response(mcp_message.id, error=error)
            
            elif tool_name == "search_entities":
                query = arguments.get("query")
                if query:
                    result = server.search_entities(query)
                    return create_mcp_response(mcp_message.id, result)
                else:
                    error = {"code": -32602, "message": "Missing query parameter"}
                    return create_mcp_response(mcp_message.id, error=error)
            
            elif tool_name == "get_platform_overview":
                result = server.get_platform_overview()
                return create_mcp_response(mcp_message.id, result)
            
            else:
                error = {"code": -32601, "message": f"Unknown tool: {tool_name}"}
                return create_mcp_response(mcp_message.id, error=error)
        
        else:
            error = {"code": -32601, "message": f"Unknown method: {mcp_message.method}"}
            return create_mcp_response(mcp_message.id, error=error)
    
    except Exception as e:
        logger.error(f"Error processing MCP request: {e}")
        error = {"code": -32603, "message": f"Internal error: {str(e)}"}
        return create_mcp_response("error", error=error)

# HTTP API Endpoints (for backward compatibility)
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "OpenMetadata MCP Server",
        "version": "1.0.0",
        "status": "running",
        "protocols": ["http", "mcp"]
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    try:
        overview = server.get_platform_overview()
        if "error" not in overview:
            return {"status": "healthy", "details": overview}
        else:
            return {"status": "unhealthy", "error": overview["error"]}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/overview")
async def get_overview():
    """Get platform overview"""
    return server.get_platform_overview()

@app.get("/data-flow")
async def get_data_flow():
    """Get data flow mapping"""
    return server.get_data_flow_mapping()

@app.post("/search")
async def search_entities(request: SearchRequest):
    """Search for entities"""
    return server.search_entities(request.query)

@app.post("/lineage")
async def get_lineage(request: LineageRequest):
    """Get data lineage for entity"""
    return server.get_data_lineage(request.entity_id)

@app.post("/field-lineage")
async def get_field_lineage(request: FieldLineageRequest):
    """Get lineage for specific field"""
    return server.get_lineage_for_field(request.table_name, request.field_name)

@app.get("/mcp-info")
async def get_mcp_info():
    """Get MCP server information for Cursor integration"""
    return {
        "server_name": "openmetadata-mcp",
        "server_type": "mcp",
        "protocols": ["http", "mcp"],
        "endpoints": {
            "http": {
                "health": "/health",
                "overview": "/overview",
                "data_flow": "/data-flow",
                "search": "/search",
                "lineage": "/lineage",
                "field_lineage": "/field-lineage"
            },
            "mcp": {
                "sse": "/mcp/sse",
                "protocol": "/mcp"
            }
        },
        "cursor_integration": {
            "config_file": "~/.cursor/mcp.json",
            "project_config": ".cursor/mcp.json",
            "mcp_proxy": "http://127.0.0.1:8096/servers/openmetadata/sse",
            "connection": {
                "host": "localhost",
                "port": 8084,
                "protocol": "http"
            }
        }
    }

if __name__ == "__main__":
    logger.info("🚀 Starting OpenMetadata MCP Server...")
    logger.info(f"Server will be available at: http://0.0.0.0:8084")
    logger.info("📋 MCP Info: GET /mcp-info")
    logger.info("🏥 Health Check: GET /health")
    logger.info("🔗 MCP Protocol: POST /mcp, GET /mcp/sse")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8084,
        log_level="info"
    )
