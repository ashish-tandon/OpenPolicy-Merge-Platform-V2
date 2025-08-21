"""
Multi-Level Government Data Ingester for OpenParliament.ca V2
Following FUNDAMENTAL RULE: Properly integrating legacy pupa scrapers with new unified schema

This ingester handles:
- Federal Parliament data (MPs, bills, votes)
- Provincial/Territorial government data
- Municipal government data (100+ cities)
- Data provenance tracking across all levels
"""

import asyncio
import logging
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import asyncpg
import importlib.util
import uuid

# Import compatibility layer first to patch pupa.utils
from .pupa_compatibility import patch_pupa_utils
patch_pupa_utils()

# Import Pupa scraper wrapper
from .pupa_scraper_wrapper import PupaScraperWrapper

# Add legacy scrapers to path
LEGACY_SCRAPERS_PATH = Path(__file__).parent.parent.parent / "legacy-scrapers-ca"
sys.path.insert(0, str(LEGACY_SCRAPERS_PATH))

from ..data_mapping_library import (
    data_mapping_library, 
    GovernmentLevel, 
    ScraperType,
    JurisdictionMapping,
    DataSourceMapping
)

logger = logging.getLogger(__name__)

class MultiLevelGovernmentIngester:
    """Comprehensive ingester for all government levels"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.mapping_library = data_mapping_library
        self.connection: Optional[asyncpg.Connection] = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.connection = await asyncpg.connect(self.database_url)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.connection:
            await self.connection.close()
    
    async def initialize_database(self):
        """Initialize government levels and jurisdictions in database"""
        logger.info("🗄️  Initializing multi-level government database schema")
        
        # Insert government levels
        await self._insert_government_levels()
        
        # Insert jurisdictions
        await self._insert_jurisdictions()
        
        # Insert data sources
        await self._insert_data_sources()
        
        logger.info("✅ Database initialization completed")
    
    async def _insert_government_levels(self):
        """Insert government levels into database"""
        levels = [
            ("federal", "Federal", "Federal government of Canada"),
            ("provincial", "Provincial/Territorial", "Provincial and territorial governments"),
            ("municipal", "Municipal", "Municipal governments and local authorities")
        ]
        
        for name, display_name, description in levels:
            await self.connection.execute("""
                INSERT INTO government_levels (name, display_name, description)
                VALUES ($1, $2, $3)
                ON CONFLICT (name) DO UPDATE SET
                    display_name = EXCLUDED.display_name,
                    description = EXCLUDED.description,
                    updated_at = NOW()
            """, name, display_name, description)
        
        logger.info(f"✅ Inserted {len(levels)} government levels")
    
    async def _insert_jurisdictions(self):
        """Insert jurisdiction records"""
        logger.info("🗺️  Inserting jurisdictions...")
        
        jurisdictions_data = []
        for jurisdiction in self.mapping_library.jurisdictions.values():
            # Generate code from name (lowercase, underscore-separated)
            code = jurisdiction.name.lower().replace(' ', '_').replace('-', '_')
            
            jurisdictions_data.append({
                'name': jurisdiction.name,
                'code': code,
                'short_name': jurisdiction.short_name,
                'ocd_division_id': jurisdiction.ocd_division_id,
                'census_code': jurisdiction.census_code,
                'province': jurisdiction.province_territory,  # Use 'province' to match existing schema
                'jurisdiction_type': jurisdiction.type,  # Use 'jurisdiction_type' to match existing schema
                'url': jurisdiction.url,
                'level_id': await self._get_government_level_id(jurisdiction.level.value)
            })
        
        # Insert jurisdictions
        for jurisdiction_data in jurisdictions_data:
            # Check if jurisdiction already exists
            existing_id = await self.connection.fetchval(
                "SELECT id FROM jurisdictions WHERE name = $1",
                jurisdiction_data['name']
            )
            
            if existing_id:
                # Update existing jurisdiction
                await self.connection.execute("""
                    UPDATE jurisdictions SET
                        code = $2,
                        short_name = $3,
                        ocd_division_id = $4,
                        census_code = $5,
                        province = $6,
                        jurisdiction_type = $7,
                        url = $8,
                        level_id = $9,
                        updated_at = NOW()
                    WHERE id = $1
                """, 
                    existing_id,
                    jurisdiction_data['code'],
                    jurisdiction_data['short_name'],
                    jurisdiction_data['ocd_division_id'],
                    jurisdiction_data['census_code'],
                    jurisdiction_data['province'],
                    jurisdiction_data['jurisdiction_type'],
                    jurisdiction_data['url'],
                    jurisdiction_data['level_id']
                )
            else:
                # Insert new jurisdiction with generated UUID
                new_id = str(uuid.uuid4())
                await self.connection.execute("""
                    INSERT INTO jurisdictions (
                        id, name, code, short_name, ocd_division_id, census_code, 
                        province, jurisdiction_type, url, level_id
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                """, 
                    new_id,
                    jurisdiction_data['name'],
                    jurisdiction_data['code'],
                    jurisdiction_data['short_name'],
                    jurisdiction_data['ocd_division_id'],
                    jurisdiction_data['census_code'],
                    jurisdiction_data['province'],
                    jurisdiction_data['jurisdiction_type'],
                    jurisdiction_data['url'],
                    jurisdiction_data['level_id']
                )
        
        logger.info(f"✅ Processed {len(jurisdictions_data)} jurisdictions")
    
    async def _get_government_level_id(self, level_name: str) -> int:
        """Get government level ID by name"""
        return await self.connection.fetchval(
            "SELECT id FROM government_levels WHERE name = $1",
            level_name
        )
    
    async def _insert_data_sources(self):
        """Insert data source records"""
        logger.info("📡 Inserting data sources...")
        
        data_sources_data = []
        for data_source in self.mapping_library.data_sources.values():
            # Get jurisdiction ID
            jurisdiction_id = await self.connection.fetchval(
                "SELECT id FROM jurisdictions WHERE name = $1",
                data_source.jurisdiction_name
            )
            
            data_sources_data.append({
                'name': data_source.name,
                'description': data_source.description,
                'url': data_source.url,
                'type': data_source.type.value,
                'jurisdiction_id': jurisdiction_id,
                'legacy_module': data_source.legacy_module,
                'legacy_class': data_source.legacy_class,
                'is_active': data_source.is_active
            })
        
        # Insert data sources
        for data_source_data in data_sources_data:
            # Check if data source already exists
            existing_id = await self.connection.fetchval(
                "SELECT id FROM data_sources WHERE name = $1",
                data_source_data['name']
            )
            
            if existing_id:
                # Update existing data source
                await self.connection.execute("""
                    UPDATE data_sources SET
                        description = $2,
                        url = $3,
                        type = $4,
                        jurisdiction_id = $5,
                        legacy_module = $6,
                        legacy_class = $7,
                        is_active = $8,
                        updated_at = NOW()
                    WHERE id = $1
                """, 
                    existing_id,
                    data_source_data['description'],
                    data_source_data['url'],
                    data_source_data['type'],
                    data_source_data['jurisdiction_id'],
                    data_source_data['legacy_module'],
                    data_source_data['legacy_class'],
                    data_source_data['is_active']
                )
            else:
                # Insert new data source
                await self.connection.execute("""
                    INSERT INTO data_sources (
                        name, description, url, type, jurisdiction_id,
                        legacy_module, legacy_class, is_active
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """, 
                    data_source_data['name'],
                    data_source_data['description'],
                    data_source_data['url'],
                    data_source_data['type'],
                    data_source_data['jurisdiction_id'],
                    data_source_data['legacy_module'],
                    data_source_data['legacy_class'],
                    data_source_data['is_active']
                )
        
        logger.info(f"✅ Processed {len(data_sources_data)} data sources")
    
    async def run_federal_ingestion(self) -> Dict[str, Any]:
        """Run federal government data ingestion"""
        logger.info("🇨🇦 Starting federal government data ingestion")
        
        # Get federal data sources
        federal_sources = [
            ds for ds in self.mapping_library.data_sources.values()
            if ds.jurisdiction_name == "Canada"
        ]
        
        stats = {
            "sources_processed": 0,
            "representatives_created": 0,
            "representatives_updated": 0,
            "offices_created": 0,
            "errors": []
        }
        
        for source in federal_sources:
            try:
                if source.type == ScraperType.PUPA_SCRAPER:
                    source_stats = await self._run_pupa_scraper(source)
                    stats["sources_processed"] += 1
                    stats["representatives_created"] += source_stats.get("representatives_created", 0)
                    stats["representatives_updated"] += source_stats.get("representatives_updated", 0)
                    stats["offices_created"] += source_stats.get("offices_created", 0)
                elif source.type == ScraperType.API_SCRAPER:
                    source_stats = await self._run_api_scraper(source)
                    stats["sources_processed"] += 1
                    stats["representatives_created"] += source_stats.get("representatives_created", 0)
                    stats["representatives_updated"] += source_stats.get("representatives_updated", 0)
                    stats["offices_created"] += source_stats.get("offices_created", 0)
            except Exception as e:
                error_msg = f"Error processing {source.name}: {str(e)}"
                logger.error(error_msg)
                stats["errors"].append(error_msg)
        
        logger.info(f"✅ Federal ingestion completed: {stats['representatives_created']} representatives created")
        return stats
    
    async def run_provincial_ingestion(self) -> Dict[str, Any]:
        """Run provincial/territorial government data ingestion"""
        logger.info("🏛️  Starting provincial/territorial government data ingestion")
        
        # Get provincial data sources
        provincial_sources = [
            ds for ds in self.mapping_library.data_sources.values()
            if ds.type == ScraperType.PUPA_SCRAPER and 
            any(ds.jurisdiction_name == j.name for j in self.mapping_library.get_jurisdictions_by_level(GovernmentLevel.PROVINCIAL))
        ]
        
        stats = {
            "sources_processed": 0,
            "representatives_created": 0,
            "representatives_updated": 0,
            "offices_created": 0,
            "errors": []
        }
        
        for source in provincial_sources:
            try:
                source_stats = await self._run_pupa_scraper(source)
                stats["sources_processed"] += 1
                stats["representatives_created"] += source_stats.get("representatives_created", 0)
                stats["representatives_updated"] += source_stats.get("representatives_updated", 0)
                stats["offices_created"] += source_stats.get("offices_created", 0)
            except Exception as e:
                error_msg = f"Error processing {source.name}: {str(e)}"
                logger.error(error_msg)
                stats["errors"].append(error_msg)
        
        logger.info(f"✅ Provincial ingestion completed: {stats['representatives_created']} representatives created")
        return stats
    
    async def run_municipal_ingestion(self) -> Dict[str, Any]:
        """Run municipal government data ingestion"""
        logger.info("🏘️  Starting municipal government data ingestion")
        
        # Get municipal data sources
        municipal_sources = [
            ds for ds in self.mapping_library.data_sources.values()
            if ds.type == ScraperType.PUPA_SCRAPER and 
            any(ds.jurisdiction_name == j.name for j in self.mapping_library.get_jurisdictions_by_level(GovernmentLevel.MUNICIPAL))
        ]
        
        stats = {
            "sources_processed": 0,
            "representatives_created": 0,
            "representatives_updated": 0,
            "offices_created": 0,
            "errors": []
        }
        
        # Process in batches to avoid overwhelming the system
        batch_size = 10
        for i in range(0, len(municipal_sources), batch_size):
            batch = municipal_sources[i:i + batch_size]
            logger.info(f"Processing municipal batch {i//batch_size + 1}/{(len(municipal_sources) + batch_size - 1)//batch_size}")
            
            for source in batch:
                try:
                    source_stats = await self._run_pupa_scraper(source)
                    stats["sources_processed"] += 1
                    stats["representatives_created"] += source_stats.get("representatives_created", 0)
                    stats["representatives_updated"] += source_stats.get("representatives_updated", 0)
                    stats["offices_created"] += source_stats.get("offices_created", 0)
                except Exception as e:
                    error_msg = f"Error processing {source.name}: {str(e)}"
                    logger.error(error_msg)
                    stats["errors"].append(error_msg)
            
            # Small delay between batches
            await asyncio.sleep(1)
        
        logger.info(f"✅ Municipal ingestion completed: {stats['representatives_created']} representatives created")
        return stats
    
    async def _run_pupa_scraper(self, data_source: DataSourceMapping) -> Dict[str, Any]:
        """Run a legacy pupa scraper"""
        if not data_source.legacy_module or not data_source.legacy_class:
            logger.warning(f"Missing legacy module/class for {data_source.name}")
            return {
                "representatives_created": 0,
                "representatives_updated": 0,
                "offices_created": 0,
                "error": "Missing legacy module/class"
            }
        
        try:
            # Import the legacy scraper module
            module_path = LEGACY_SCRAPERS_PATH / data_source.legacy_module / "people.py"
            if not module_path.exists():
                logger.warning(f"Legacy scraper file not found: {module_path}")
                return {
                    "representatives_created": 0,
                    "representatives_updated": 0,
                    "offices_created": 0,
                    "error": "Scraper file not found"
                }
            
            # Import the scraper class
            spec = importlib.util.spec_from_file_location(
                f"{data_source.legacy_module}.people",
                module_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get the scraper class
            scraper_class = getattr(module, data_source.legacy_class, None)
            if not scraper_class:
                logger.warning(f"Scraper class {data_source.legacy_class} not found in {data_source.legacy_module}")
                return {
                    "representatives_created": 0,
                    "representatives_updated": 0,
                    "offices_created": 0,
                    "error": "Scraper class not found"
                }
            
            # Create scraper instance with proper context
            # Note: This is a simplified approach - full pupa integration would require more setup
            logger.info(f"🔍 Running legacy scraper: {data_source.legacy_module}.{data_source.legacy_class}")
            
            # Try to instantiate and run the scraper using the wrapper
            try:
                # Determine jurisdiction type from data source name
                jurisdiction_type = "legislature"  # default
                if "Provincial" in data_source.name:
                    jurisdiction_type = "provincial"
                elif "Municipal" in data_source.name:
                    jurisdiction_type = "municipal"
                elif "Federal" in data_source.name:
                    jurisdiction_type = "federal"
                
                # Use the Pupa scraper wrapper
                with PupaScraperWrapper() as wrapper:
                    result = wrapper.run_scraper(
                        scraper_class, 
                        data_source.jurisdiction_name, 
                        jurisdiction_type
                    )
                
                if result["status"] == "success":
                    logger.info(f"✅ Successfully ran scraper: {scraper_class.__name__}")
                else:
                    logger.warning(f"Scraper {scraper_class.__name__} failed: {result.get('error', 'Unknown error')}")
                
                return result
                
            except Exception as scraper_error:
                logger.warning(f"Could not run scraper {scraper_class.__name__}: {str(scraper_error)}")
                return {
                    "representatives_created": 0,
                    "representatives_updated": 0,
                    "offices_created": 0,
                    "scraper_class": scraper_class.__name__,
                    "status": "instantiation_failed",
                    "error": str(scraper_error)
                }
            
        except Exception as e:
            logger.error(f"Error running pupa scraper {data_source.name}: {str(e)}")
            return {
                "representatives_created": 0,
                "representatives_updated": 0,
                "offices_created": 0,
                "error": str(e)
            }
    
    async def _run_api_scraper(self, data_source: DataSourceMapping) -> Dict[str, Any]:
        """Run an API-based scraper"""
        logger.info(f"🔌 Running API scraper: {data_source.name}")
        # TODO: Implement API scraping logic
        return {
            "representatives_created": 0,
            "representatives_updated": 0,
            "offices_created": 0
        }
    
    async def run_full_ingestion(self) -> Dict[str, Any]:
        """Run full multi-level government ingestion"""
        logger.info("🚀 Starting full multi-level government data ingestion")
        
        start_time = datetime.now()
        
        # Initialize database
        await self.initialize_database()
        
        # Run ingestion for each level
        federal_stats = await self.run_federal_ingestion()
        provincial_stats = await self.run_provincial_ingestion()
        municipal_stats = await self.run_municipal_ingestion()
        
        # Compile overall stats
        total_stats = {
            "federal": federal_stats,
            "provincial": provincial_stats,
            "municipal": municipal_stats,
            "total_representatives_created": (
                federal_stats["representatives_created"] +
                provincial_stats["representatives_created"] +
                municipal_stats["representatives_created"]
            ),
            "total_representatives_updated": (
                federal_stats["representatives_updated"] +
                provincial_stats["representatives_updated"] +
                municipal_stats["representatives_updated"]
            ),
            "total_offices_created": (
                federal_stats["offices_created"] +
                provincial_stats["offices_created"] +
                municipal_stats["offices_created"]
            ),
            "start_time": start_time,
            "end_time": datetime.now(),
            "duration_seconds": (datetime.now() - start_time).total_seconds()
        }
        
        # Log ingestion
        await self._log_ingestion("full_multi_level_ingestion", "success", total_stats)
        
        logger.info(f"🎉 Full ingestion completed in {total_stats['duration_seconds']:.2f} seconds")
        logger.info(f"📊 Total: {total_stats['total_representatives_created']} representatives created")
        
        return total_stats
    
    async def _log_ingestion(self, operation: str, status: str, stats: Dict[str, Any]):
        """Log ingestion operation to database"""
        try:
            await self.connection.execute("""
                INSERT INTO ingestion_logs (
                    data_source_id, operation, status, records_processed,
                    records_created, records_updated, records_failed,
                    started_at, completed_at, duration_seconds, metadata
                ) VALUES (
                    (SELECT id FROM data_sources WHERE name = 'System' LIMIT 1),
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10
                )
            """, operation, status, 
                 stats.get("total_representatives_created", 0) + stats.get("total_representatives_updated", 0),
                 stats.get("total_representatives_created", 0),
                 stats.get("total_representatives_updated", 0),
                 len(stats.get("errors", [])),
                 stats.get("start_time"),
                 stats.get("end_time"),
                 stats.get("duration_seconds"),
                 stats)
        except Exception as e:
            logger.error(f"Error logging ingestion: {str(e)}")
    
    def get_ingestion_summary(self) -> str:
        """Get summary of available data sources and jurisdictions"""
        summary = self.mapping_library.get_jurisdiction_summary()
        
        report = []
        report.append("# Multi-Level Government Ingestion Summary")
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("")
        report.append("## Available Jurisdictions")
        report.append(f"- **Federal**: {summary['by_level']['federal']}")
        report.append(f"- **Provincial/Territorial**: {summary['by_level']['provincial']}")
        report.append(f"- **Municipal**: {summary['by_level']['municipal']}")
        report.append(f"- **Total**: {summary['total_jurisdictions']}")
        report.append("")
        report.append("## Available Data Sources")
        report.append(f"- **Pupa Scrapers**: {summary['by_type']['pupa_scrapers']}")
        report.append(f"- **CSV Scrapers**: {summary['by_type']['csv_scrapers']}")
        report.append(f"- **API Scrapers**: {summary['by_type']['api_scrapers']}")
        report.append(f"- **Manual Scrapers**: {summary['by_type']['manual_scrapers']}")
        report.append(f"- **Total**: {summary['total_data_sources']}")
        report.append("")
        report.append("## Next Steps")
        report.append("1. Run `run_full_ingestion()` to process all data sources")
        report.append("2. Monitor ingestion logs for progress and errors")
        report.append("3. Verify data quality and completeness")
        report.append("4. Integrate with frontend for display")
        
        return "\n".join(report)
