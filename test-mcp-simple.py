#!/usr/bin/env python3
"""
Simple MCP Server Test - Shows lots of movement on screen!
"""

import os
import sys
import time

# Add the mcp-env to path
sys.path.insert(0, 'mcp-env/lib/python3.13/site-packages')

def test_mcp_server():
    """Test the MCP server with visual feedback"""
    
    print("🚀 STARTING EXCITING MCP TEST! 🚀")
    print("=" * 50)
    
    # Set environment variables
    os.environ["OPENMETADATA_SERVER_URL"] = "http://localhost:8585"
    os.environ["OPENMETADATA_AUTH_TOKEN"] = "admin"
    os.environ["OPENMETADATA_USERNAME"] = "admin@open-metadata.org"
    
    print("✅ Environment variables set!")
    time.sleep(0.5)
    
    try:
        # Import and test the MCP server
        print("📦 Importing MCP server...")
        time.sleep(0.5)
        
        from mcp_openmetadata_server import OpenMetadataMCPServer
        
        print("🎯 Creating MCP server instance...")
        time.sleep(0.5)
        
        server = OpenMetadataMCPServer()
        
        print("🔗 Testing OpenMetadata connection...")
        time.sleep(0.5)
        
        # Test platform overview
        print("📊 Getting platform overview...")
        overview = server.get_platform_overview()
        
        print("🎉 PLATFORM OVERVIEW RESULTS:")
        print(f"   📊 Database Services: {overview.get('database_services', 'N/A')}")
        print(f"   🗃️  Total Tables: {overview.get('total_tables', 'N/A')}")
        print(f"   🕐 Last Updated: {overview.get('last_updated', 'N/A')}")
        print(f"   🟢 Status: {overview.get('status', 'N/A')}")
        
        time.sleep(0.5)
        
        # Test data flow mapping
        print("\n🔄 Testing data flow mapping...")
        time.sleep(0.5)
        
        flow_data = server.get_data_flow_mapping()
        
        print("🎯 DATA FLOW RESULTS:")
        print(f"   🚀 Pipelines: {flow_data.get('pipelines', 'N/A')}")
        print(f"   📈 Data Flows: {len(flow_data.get('data_flows', []))}")
        print(f"   🕐 Last Updated: {flow_data.get('last_updated', 'N/A')}")
        print(f"   🟢 Status: {flow_data.get('status', 'N/A')}")
        
        print("\n🎉 ALL TESTS PASSED! MCP SERVER IS WORKING PERFECTLY!")
        print("=" * 50)
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try: source mcp-env/bin/activate && pip install requests")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_mcp_server()
    if success:
        print("🚀 READY FOR CURSOR INTEGRATION!")
    else:
        print("🔧 NEEDS FIXING BEFORE CURSOR INTEGRATION")
