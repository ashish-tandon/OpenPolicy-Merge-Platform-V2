#!/usr/bin/env python3
"""
Test Multi-Level Government System for OpenParliament.ca V2
Following FUNDAMENTAL RULE: Testing comprehensive integration of legacy scrapers

This script demonstrates:
- Data mapping library functionality
- Multi-level government structure
- Available data sources and jurisdictions
- Database schema initialization
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add app to path
sys.path.append(str(Path(__file__).parent / "app"))

from app.ingestion.multi_level_government_ingester import MultiLevelGovernmentIngester
from app.data_mapping_library import data_mapping_library, GovernmentLevel, ScraperType
from app.config import get_database_url

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_data_mapping_library():
    """Test the data mapping library functionality"""
    logger.info("🧪 Testing Data Mapping Library")
    
    # Get summary
    summary = data_mapping_library.get_jurisdiction_summary()
    logger.info(f"📊 Jurisdiction Summary:")
    logger.info(f"   - Total Jurisdictions: {summary['total_jurisdictions']}")
    logger.info(f"   - Federal: {summary['by_level']['federal']}")
    logger.info(f"   - Provincial: {summary['by_level']['provincial']}")
    logger.info(f"   - Municipal: {summary['by_level']['municipal']}")
    logger.info(f"   - Total Data Sources: {summary['total_data_sources']}")
    
    # Test jurisdiction queries
    federal_jurisdictions = data_mapping_library.get_jurisdictions_by_level(
        GovernmentLevel.FEDERAL
    )
    logger.info(f"🇨🇦 Federal Jurisdictions: {len(federal_jurisdictions)}")
    for j in federal_jurisdictions:
        logger.info(f"   - {j.name} ({j.short_name})")
    
    provincial_jurisdictions = data_mapping_library.get_jurisdictions_by_level(
        GovernmentLevel.PROVINCIAL
    )
    logger.info(f"🏛️  Provincial Jurisdictions: {len(provincial_jurisdictions)}")
    for j in provincial_jurisdictions[:5]:  # Show first 5
        logger.info(f"   - {j.name} ({j.short_name})")
    if len(provincial_jurisdictions) > 5:
        logger.info(f"   ... and {len(provincial_jurisdictions) - 5} more")
    
    municipal_jurisdictions = data_mapping_library.get_jurisdictions_by_level(
        GovernmentLevel.MUNICIPAL
    )
    logger.info(f"🏘️  Municipal Jurisdictions: {len(municipal_jurisdictions)}")
    
    # Group by province
    by_province = {}
    for j in municipal_jurisdictions:
        province = j.province_territory
        if province not in by_province:
            by_province[province] = []
        by_province[province].append(j)
    
    for province, jurisdictions in by_province.items():
        logger.info(f"   {province}: {len(jurisdictions)} municipalities")
    
    # Test data source queries
    legacy_scrapers = data_mapping_library.get_legacy_scrapers()
    logger.info(f"🔧 Legacy Pupa Scrapers: {len(legacy_scrapers)}")
    
    # Show some examples
    for scraper in legacy_scrapers[:5]:
        logger.info(f"   - {scraper.name} ({scraper.jurisdiction_name})")
        logger.info(f"     Module: {scraper.legacy_module}.{scraper.legacy_class}")
    if len(legacy_scrapers) > 5:
        logger.info(f"   ... and {len(legacy_scrapers) - 5} more")
    
    logger.info("✅ Data mapping library test completed successfully!")

async def test_database_initialization():
    """Test database initialization"""
    logger.info("🗄️  Testing Database Initialization")
    
    database_url = get_database_url()
    logger.info(f"🔗 Database: {database_url}")
    
    try:
        async with MultiLevelGovernmentIngester(database_url) as ingester:
            # Get ingestion summary
            summary = ingester.get_ingestion_summary()
            logger.info("📋 Ingestion Summary:")
            logger.info(summary)
            
            # Initialize database schema
            logger.info("🔧 Initializing database schema...")
            await ingester.initialize_database()
            logger.info("✅ Database schema initialized successfully!")
            
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        return False
    
    logger.info("✅ Database initialization test completed successfully!")
    return True

async def test_ingestion_pipeline():
    """Test the ingestion pipeline (without running actual scrapers)"""
    logger.info("🚀 Testing Ingestion Pipeline")
    
    database_url = get_database_url()
    
    try:
        async with MultiLevelGovernmentIngester(database_url) as ingester:
            # Test federal ingestion (mock)
            logger.info("🇨🇦 Testing federal ingestion pipeline...")
            federal_stats = await ingester.run_federal_ingestion()
            logger.info(f"   - Sources processed: {federal_stats['sources_processed']}")
            logger.info(f"   - Representatives created: {federal_stats['representatives_created']}")
            
            # Test provincial ingestion (mock)
            logger.info("🏛️  Testing provincial ingestion pipeline...")
            provincial_stats = await ingester.run_provincial_ingestion()
            logger.info(f"   - Sources processed: {provincial_stats['sources_processed']}")
            logger.info(f"   - Representatives created: {provincial_stats['representatives_created']}")
            
            # Test municipal ingestion (mock)
            logger.info("🏘️  Testing municipal ingestion pipeline...")
            municipal_stats = await ingester.run_municipal_ingestion()
            logger.info(f"   - Sources processed: {municipal_stats['sources_processed']}")
            logger.info(f"   - Representatives created: {municipal_stats['representatives_created']}")
            
    except Exception as e:
        logger.error(f"❌ Ingestion pipeline test failed: {str(e)}")
        return False
    
    logger.info("✅ Ingestion pipeline test completed successfully!")
    return True

async def generate_mapping_report():
    """Generate comprehensive mapping report"""
    logger.info("📊 Generating Comprehensive Mapping Report")
    
    try:
        report = data_mapping_library.export_mapping_report()
        
        # Save to file
        report_path = Path(__file__).parent / "COMPREHENSIVE_DATA_MAPPING_REPORT.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"📄 Mapping report saved to: {report_path}")
        logger.info(f"📊 Report length: {len(report)} characters")
        
        # Show summary
        lines = report.split('\n')
        logger.info(f"📝 Report sections:")
        for line in lines:
            if line.startswith('## '):
                logger.info(f"   - {line[3:]}")
        
    except Exception as e:
        logger.error(f"❌ Failed to generate mapping report: {str(e)}")
        return False
    
    logger.info("✅ Mapping report generated successfully!")
    return True

async def main():
    """Main test function"""
    logger.info("🚀 Starting Multi-Level Government System Tests")
    logger.info("📋 Following FUNDAMENTAL RULE: Testing comprehensive legacy scraper integration")
    
    # Test 1: Data Mapping Library
    await test_data_mapping_library()
    
    # Test 2: Database Initialization
    db_success = await test_database_initialization()
    if not db_success:
        logger.error("❌ Database initialization failed, skipping remaining tests")
        return
    
    # Test 3: Ingestion Pipeline
    pipeline_success = await test_ingestion_pipeline()
    if not pipeline_success:
        logger.error("❌ Ingestion pipeline test failed")
    
    # Test 4: Generate Mapping Report
    report_success = await generate_mapping_report()
    if not report_success:
        logger.error("❌ Mapping report generation failed")
    
    logger.info("🎉 All multi-level government system tests completed!")
    
    # Final summary
    summary = data_mapping_library.get_jurisdiction_summary()
    logger.info("📊 Final Summary:")
    logger.info(f"   - Total Jurisdictions: {summary['total_jurisdictions']}")
    logger.info(f"   - Total Data Sources: {summary['total_data_sources']}")
    logger.info(f"   - Legacy Pupa Scrapers: {summary['by_type']['pupa_scrapers']}")
    logger.info(f"   - Ready for full ingestion!")

if __name__ == "__main__":
    asyncio.run(main())
