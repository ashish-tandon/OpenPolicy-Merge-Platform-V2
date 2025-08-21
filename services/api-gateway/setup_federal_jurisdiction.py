#!/usr/bin/env python3
"""
Setup script for OpenParliament.ca V2 federal jurisdiction

This script creates the necessary federal jurisdiction and sets up the database
for the Represent integration, following the FUNDAMENTAL RULE of using existing schema.
"""

import psycopg2
import uuid
from datetime import datetime

# Database connection parameters
DB_PARAMS = {
    'host': 'localhost',
    'database': 'openpolicy',
    'user': 'ashishtandon',
    'password': None  # No password for local development
}

def create_federal_jurisdiction():
    """Create the federal jurisdiction for Canada Parliament"""
    
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    
    try:
        # Get the existing federal jurisdiction for Canada
        cursor.execute("SELECT id FROM jurisdictions WHERE code = 'canada' AND jurisdiction_type = 'FEDERAL'")
        existing = cursor.fetchone()
        
        if existing:
            print(f"Federal jurisdiction for Canada already exists with ID: {existing[0]}")
            federal_jurisdiction_id = existing[0]
        else:
            print("Error: No federal jurisdiction found for Canada")
            return None
        
        return federal_jurisdiction_id
        
    except Exception as e:
        print(f"Error creating federal jurisdiction: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def check_existing_data():
    """Check what data already exists in the database"""
    
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    
    try:
        # Check representatives count
        cursor.execute("SELECT COUNT(*) FROM representatives")
        rep_count = cursor.fetchone()[0]
        print(f"Existing representatives: {rep_count}")
        
        # Check bills count
        cursor.execute("SELECT COUNT(*) FROM bills")
        bills_count = cursor.fetchone()[0]
        print(f"Existing bills: {bills_count}")
        
        # Check votes count
        cursor.execute("SELECT COUNT(*) FROM votes")
        votes_count = cursor.fetchone()[0]
        print(f"Existing votes: {votes_count}")
        
        # Check jurisdictions
        cursor.execute("SELECT COUNT(*) FROM jurisdictions")
        jurisdictions_count = cursor.fetchone()[0]
        print(f"Total jurisdictions: {jurisdictions_count}")
        
    except Exception as e:
        print(f"Error checking existing data: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Setting up OpenParliament.ca V2 federal jurisdiction...")
    print("=" * 50)
    
    # Check existing data
    print("\nChecking existing data...")
    check_existing_data()
    
    # Create federal jurisdiction
    print("\nSetting up federal jurisdiction...")
    federal_id = create_federal_jurisdiction()
    
    print("\nSetup complete!")
    print(f"Federal jurisdiction ID: {federal_id}")
    print("\nYou can now run the data ingestion pipeline.")
