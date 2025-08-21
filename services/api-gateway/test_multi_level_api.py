#!/usr/bin/env python3
"""
Simple test script for Multi-Level Government API endpoints
"""

import asyncio
import sys
from pathlib import Path

# Add app to path
sys.path.append(str(Path(__file__).parent / "app"))

from fastapi.testclient import TestClient
from app.main import app

def test_multi_level_government_api():
    """Test the multi-level government API endpoints"""
    client = TestClient(app)
    
    print("🧪 Testing Multi-Level Government API Endpoints")
    print("=" * 50)
    
    # Test 1: Government Levels
    print("\n1. Testing Government Levels endpoint...")
    try:
        response = client.get("/api/v1/multi-level-government/government-levels")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {len(data.get('items', []))} government levels")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    
    # Test 2: Jurisdictions
    print("\n2. Testing Jurisdictions endpoint...")
    try:
        response = client.get("/api/v1/multi-level-government/jurisdictions")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {len(data.get('items', []))} jurisdictions")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    
    # Test 3: Representatives
    print("\n3. Testing Representatives endpoint...")
    try:
        response = client.get("/api/v1/multi-level-government/representatives")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {len(data.get('items', []))} representatives")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    
    # Test 4: System Stats
    print("\n4. Testing System Stats endpoint...")
    try:
        response = client.get("/api/v1/multi-level-government/stats/system")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    
    # Test 5: Offices
    print("\n5. Testing Offices endpoint...")
    try:
        response = client.get("/api/v1/multi-level-government/offices")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {len(data.get('items', []))} offices")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    
    # Test 6: Bills
    print("\n6. Testing Bills endpoint...")
    try:
        response = client.get("/api/v1/multi-level-government/bills")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {len(data.get('items', []))} bills")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    
    # Test 7: Data Sources
    print("\n7. Testing Data Sources endpoint...")
    try:
        response = client.get("/api/v1/multi-level-government/data-sources")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {len(data.get('items', []))} data sources")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ Multi-Level Government API test completed!")

if __name__ == "__main__":
    test_multi_level_government_api()
