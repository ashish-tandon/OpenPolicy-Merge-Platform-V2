#!/usr/bin/env python3
"""
Legacy Data Ingestion Runner for OpenParliament.ca V2

Following FUNDAMENTAL RULE: Loads existing legacy data into database
Usage: python ingest_legacy_data.py [--file path/to/data.json]
"""
import asyncio
import argparse
import logging
import os
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from ingestion.legacy_data_ingester import LegacyDataIngester

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    """Main entry point for legacy data ingestion"""
    parser = argparse.ArgumentParser(description='Ingest legacy OpenParliament data into database')
    parser.add_argument('--file', '-f', help='Path to JSON file with legacy data')
    parser.add_argument('--database-url', help='Database URL (default: from DATABASE_URL env var)')
    
    args = parser.parse_args()
    
    # Database URL
    database_url = args.database_url or os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/openparliament')
    
    # Find data file
    if args.file:
        json_file = args.file
    else:
        # Find the latest collected data file
        data_dir = Path('data/legacy_adapted')
        if not data_dir.exists():
            logger.error("❌ No data/legacy_adapted/ directory found")
            logger.info("💡 Run the data collection first: python collect_data.py")
            return 1
        
        json_files = list(data_dir.glob('legacy_collected_*.json'))
        
        if not json_files:
            logger.error("❌ No legacy data files found in data/legacy_adapted/")
            logger.info("💡 Run the data collection first: python collect_data.py")
            return 1
        
        # Use the most recent file
        json_file = str(max(json_files, key=lambda f: f.stat().st_mtime))
    
    logger.info(f"🚀 Starting legacy data ingestion")
    logger.info(f"📂 Data file: {json_file}")
    logger.info(f"🗄️ Database: {database_url.split('@')[-1] if '@' in database_url else database_url}")
    logger.info("📋 Following FUNDAMENTAL RULE: Using existing legacy data structure")
    
    try:
        # Create ingester and run
        ingester = LegacyDataIngester(database_url)
        stats = await ingester.ingest_json_file(json_file)
        
        # Print final statistics
        logger.info("🎉 Legacy Data Ingestion Complete!")
        logger.info(f"📊 Final Results:")
        logger.info(f"   👥 MPs: {stats.mps_inserted} inserted, {stats.mps_updated} updated")
        logger.info(f"   📄 Bills: {stats.bills_inserted} inserted, {stats.bills_updated} updated")  
        logger.info(f"   🗳️ Votes: {stats.votes_inserted} inserted, {stats.votes_updated} updated")
        logger.info(f"   🏢 Offices: {stats.offices_inserted} inserted")
        logger.info(f"   ☑️ Ballots: {stats.ballots_inserted} inserted")
        
        if stats.errors:
            logger.warning(f"⚠️ {len(stats.errors)} errors occurred during ingestion")
            for error in stats.errors[:5]:  # Show first 5 errors
                logger.warning(f"   {error}")
            return 1
        
        logger.info("✅ All data successfully ingested into database!")
        return 0
        
    except Exception as e:
        logger.error(f"❌ Fatal error during ingestion: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
