#!/usr/bin/env python3
"""
Municipal Data Ingestion Script for OpenParliament.ca V2

Following FUNDAMENTAL RULE: Uses existing legacy scraper infrastructure
Runs all 100+ municipal scrapers to collect councillor data
"""

import asyncio
import logging
import os
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

async def main():
    """Main ingestion function"""
    logger.info("🚀 Starting Municipal Data Ingestion")
    logger.info("📋 Following FUNDAMENTAL RULE: Using existing legacy scraper infrastructure")
    
    try:
        # Get database URL
        database_url = get_database_url()
        logger.info(f"🔗 Database: {database_url}")
        
        # Create ingester
        ingester = MunicipalDataIngester(database_url)
        
        # Get available municipalities
        municipalities = ingester.get_available_municipalities()
        logger.info(f"📍 Found {len(municipalities)} municipal scrapers:")
        
        # Show first 10 municipalities as preview
        for i, municipality in enumerate(municipalities[:10]):
            logger.info(f"   {i+1:2d}. {municipality}")
        if len(municipalities) > 10:
            logger.info(f"   ... and {len(municipalities) - 10} more")
        
        # Run full ingestion
        stats = await ingester.run_full_ingestion()
        
        # Print final statistics
        logger.info("=" * 60)
        logger.info("📊 INGESTION COMPLETED - FINAL STATISTICS")
        logger.info("=" * 60)
        logger.info(f"Municipalities Processed: {stats.municipalities_processed}")
        logger.info(f"Councillors Inserted:    {stats.councillors_inserted}")
        logger.info(f"Councillors Updated:     {stats.councillors_updated}")
        logger.info(f"Offices Inserted:        {stats.offices_inserted}")
        logger.info(f"Offices Updated:         {stats.offices_updated}")
        logger.info(f"Errors:                  {len(stats.errors)}")
        
        if stats.errors:
            logger.warning("⚠️  Errors encountered:")
            for error in stats.errors[:10]:  # Show first 10 errors
                logger.warning(f"   - {error}")
            if len(stats.errors) > 10:
                logger.warning(f"   ... and {len(stats.errors) - 10} more errors")
        
        logger.info("=" * 60)
        logger.info("✅ Municipal data ingestion completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Fatal error during ingestion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
