#!/usr/bin/env python3
"""
Test Municipal Data Ingestion

Following FUNDAMENTAL RULE: Tests the existing legacy scraper infrastructure
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.append(str(Path(__file__).parent / "app"))

from app.ingestion import MunicipalDataIngester
from app.config import get_database_url

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_municipal_ingestion():
    """Test municipal data ingestion with a small sample."""
    logger.info("🧪 Testing Municipal Data Ingestion")
    logger.info("📋 Following FUNDAMENTAL RULE: Using existing legacy scraper infrastructure")
    
    try:
        # Get database URL
        database_url = get_database_url()
        logger.info(f"🔗 Database: {database_url}")
        
        # Create ingester
        ingester = MunicipalDataIngester(database_url)
        
        # Get available municipalities
        municipalities = ingester.get_available_municipalities()
        logger.info(f"📍 Found {len(municipalities)} municipal scrapers")
        
        # Test with first 3 municipalities only
        test_municipalities = municipalities[:3]
        logger.info(f"🧪 Testing with first 3 municipalities: {test_municipalities}")
        
        # Test metadata extraction
        for municipality in test_municipalities:
            metadata = ingester.get_municipality_metadata(municipality)
            if metadata:
                logger.info(f"✅ {municipality}: {metadata['name']} ({metadata['scraper_class']})")
            else:
                logger.warning(f"⚠️  {municipality}: No metadata found")
        
        # Test scraping one municipality
        if test_municipalities:
            test_municipality = test_municipalities[0]
            logger.info(f"🔍 Testing scraping for {test_municipality}")
            
            municipality_data = await ingester.scrape_municipality_data(test_municipality)
            if municipality_data:
                logger.info(f"✅ Scraped {test_municipality}: {len(municipality_data['councillors'])} councillors")
                
                # Show sample councillor data
                if municipality_data['councillors']:
                    councillor = municipality_data['councillors'][0]
                    logger.info(f"📋 Sample councillor: {councillor['name']}")
                    logger.info(f"   Municipality: {councillor['municipality_name']}")
                    logger.info(f"   Offices: {len(councillor['offices'])}")
                    
                    for office in councillor['offices'][:2]:  # Show first 2 offices
                        logger.info(f"   - {office['type']}: {office['value']}")
            else:
                logger.warning(f"⚠️  No data scraped for {test_municipality}")
        
        logger.info("✅ Municipal data ingestion test completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_municipal_ingestion())
