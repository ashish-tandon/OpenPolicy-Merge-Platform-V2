#!/usr/bin/env python3
"""
OpenMetadata MCP Server for Cursor Integration
This server provides data lineage information to Cursor via MCP protocol
"""

import json
import requests
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenMetadataMCPServer:
    """MCP Server for OpenMetadata integration with Cursor"""
    
    def __init__(self):
        self.openmetadata_url = os.getenv("OPENMETADATA_SERVER_URL", "http://localhost:8585")
        self.auth_token = os.getenv("OPENMETADATA_AUTH_TOKEN", "admin")
        self.username = os.getenv("OPENMETADATA_USERNAME", "admin@open-metadata.org")
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
    
    def get_service_details(self, service_id: str) -> Dict[str, Any]:
        """Get detailed information about a service"""
        try:
            url = f"{self.openmetadata_url}/api/v1/services/databaseServices/{service_id}"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting service details for {service_id}: {e}")
            return {"error": str(e)}
    
    def get_data_quality(self, table_id: str) -> Dict[str, Any]:
        """Get data quality metrics for a table"""
        try:
            url = f"{self.openmetadata_url}/api/v1/tables/{table_id}/quality"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting data quality for {table_id}: {e}")
            return {"error": str(e)}
    
    def get_ingestion_status(self) -> Dict[str, Any]:
        """Get status of ingestion workflows"""
        try:
            url = f"{self.openmetadata_url}/api/v1/ingestion"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting ingestion status: {e}")
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
            
            # Get ingestion status
            ingestion_status = self.get_ingestion_status()
            
            return {
                "database_services": len(db_services),
                "total_tables": len(tables),
                "ingestion_status": ingestion_status,
                "last_updated": datetime.now().isoformat()
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

def main():
    """Main function to run the MCP server"""
    server = OpenMetadataMCPServer()
    
    print("🚀 OpenMetadata MCP Server for Cursor")
    print("=====================================")
    print(f"Connected to: {server.openmetadata_url}")
    print(f"Username: {server.username}")
    print("")
    
    # Test connection
    try:
        overview = server.get_platform_overview()
        if "error" not in overview:
            print("✅ Connection successful!")
            print(f"Database services: {overview.get('database_services', 0)}")
            print(f"Total tables: {overview.get('total_tables', 0)}")
        else:
            print(f"❌ Connection failed: {overview['error']}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    
    print("")
    print("Available commands:")
    print("- get_data_lineage(entity_id)")
    print("- search_entities(query)")
    print("- get_table_details(table_id)")
    print("- get_service_details(service_id)")
    print("- get_data_quality(table_id)")
    print("- get_ingestion_status()")
    print("- get_platform_overview()")
    print("- get_data_flow_mapping()")
    print("- get_lineage_for_field(table_name, field_name)")
    
    # Interactive mode
    while True:
        try:
            command = input("\nEnter command (or 'quit' to exit): ").strip()
            if command.lower() == 'quit':
                break
            
            # Parse and execute command
            if command.startswith("get_lineage_for_field"):
                # Extract parameters
                parts = command.split("(")[1].split(")")[0].split(",")
                table_name = parts[0].strip().strip('"\'')
                field_name = parts[1].strip().strip('"\'')
                result = server.get_lineage_for_field(table_name, field_name)
                print(json.dumps(result, indent=2))
            
            elif command.startswith("search_entities"):
                query = command.split("(")[1].split(")")[0].strip().strip('"\'')
                result = server.search_entities(query)
                print(json.dumps(result, indent=2))
            
            elif command.startswith("get_platform_overview"):
                result = server.get_platform_overview()
                print(json.dumps(result, indent=2))
            
            elif command.startswith("get_data_flow_mapping"):
                result = server.get_data_flow_mapping()
                print(json.dumps(result, indent=2))
            
            else:
                print("Unknown command. Available commands:")
                print("- get_lineage_for_field(table_name, field_name)")
                print("- search_entities(query)")
                print("- get_platform_overview()")
                print("- get_data_flow_mapping()")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
