#!/usr/bin/env python3
"""
Test Simple CSV Municipal Data Ingestion

Following FUNDAMENTAL RULE: Tests the simplified CSV approach
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent / "app"))

from app.ingestion.simple_csv_municipal_ingester import SimpleCSVMunicipalIngester
from app.config import get_database_url

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_csv_ingestion():
    """Test CSV municipal data ingestion."""
    logger.info("🧪 Testing CSV Municipal Data Ingestion")
    logger.info("📋 Following FUNDAMENTAL RULE: Using existing CSV data sources directly")
    
    try:
        # Get database URL
        database_url = get_database_url()
        logger.info(f"🔗 Database: {database_url}")
        
        # Create ingester
        ingester = SimpleCSVMunicipalIngester(database_url)
        
        # Get available CSV municipalities
        municipalities = ingester.get_csv_municipalities()
        logger.info(f"📍 Found {len(municipalities)} CSV municipalities:")
        
        for i, municipality in enumerate(municipalities):
            logger.info(f"   {i+1}. {municipality['name']} ({municipality['province']})")
            logger.info(f"      URL: {municipality['csv_url']}")
        
        # Test CSV scraping for first municipality
        if municipalities:
            test_municipality = municipalities[0]
            logger.info(f"🔍 Testing CSV scraping for {test_municipality['name']}")
            
            municipality_data = await ingester.scrape_csv_municipality(test_municipality)
            if municipality_data:
                logger.info(f"✅ Scraped {test_municipality['name']}: {len(municipality_data['councillors'])} councillors")
                
                # Show sample councillor data
                if municipality_data['councillors']:
                    councillor = municipality_data['councillors'][0]
                    logger.info(f"📋 Sample councillor: {councillor['name']}")
                    logger.info(f"   Municipality: {councillor['municipality_name']}")
                    logger.info(f"   Offices: {len(councillor['offices'])}")
                    
                    for office in councillor['offices'][:2]:  # Show first 2 offices
                        logger.info(f"   - {office['type']}: {office['value']}")
            else:
                logger.warning(f"⚠️  No data scraped for {test_municipality['name']}")
        
        logger.info("✅ CSV municipal data ingestion test completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_csv_ingestion())
