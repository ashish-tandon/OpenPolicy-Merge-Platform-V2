#!/usr/bin/env python3
"""
Data Collection Script for OpenParliament.ca V2

Following FUNDAMENTAL RULE: Uses legacy OpenParliament importers
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.extractors.legacy_adapters import LegacyDataCollectionTask

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def main():
    """Main data collection function"""
    logger.info("🚀 Starting OpenParliament.ca V2 data collection...")
    logger.info("📋 Following FUNDAMENTAL RULE: Using legacy OpenParliament importers")
    
    try:
        # Create data collection task
        task = LegacyDataCollectionTask(output_dir="data")
        
        # Run full data collection
        await task.run_full_collection()
        
        logger.info("✅ Data collection completed successfully!")
        logger.info("📁 Check the 'data/legacy_adapted/' directory for collected data")
        
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
