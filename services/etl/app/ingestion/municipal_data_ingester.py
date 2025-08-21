"""
Municipal Data Ingester for OpenParliament.ca V2

Following FUNDAMENTAL RULE: Uses existing legacy scraper infrastructure from scrapers-ca
Source: legacy-scrapers-ca/ directory with 100+ municipal scrapers
"""
import json
import logging
import asyncio
import uuid
import importlib
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import asyncpg
import sys
from dataclasses import dataclass

# Monkey patch for Python 3.13 compatibility
if not hasattr(importlib, 'find_loader'):
    importlib.find_loader = lambda name: importlib.util.find_spec(name)

# Add legacy scrapers to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'legacy-scrapers-ca'))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class MunicipalIngestionStats:
    """Statistics for municipal data ingestion run"""
    municipalities_processed: int = 0
    councillors_inserted: int = 0
    councillors_updated: int = 0
    offices_inserted: int = 0
    offices_updated: int = 0
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []

class MunicipalDataIngester:
    """
    Ingests municipal data using existing legacy scraper infrastructure
    Following FUNDAMENTAL RULE: Uses existing scraper classes and utilities
    """
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.stats = MunicipalIngestionStats()
        self.legacy_scrapers_path = os.path.join(
            os.path.dirname(__file__), '..', '..', 'legacy-scrapers-ca'
        )
        
    def get_available_municipalities(self) -> List[str]:
        """
        Get list of available municipal scrapers
        Following FUNDAMENTAL RULE: Uses existing module discovery logic
        """
        municipalities = []
        for item in os.listdir(self.legacy_scrapers_path):
            item_path = os.path.join(self.legacy_scrapers_path, item)
            if (os.path.isdir(item_path) and 
                os.path.exists(os.path.join(item_path, '__init__.py')) and
                os.path.exists(os.path.join(item_path, 'people.py')) and
                item.startswith('ca_')):
                municipalities.append(item)
        return sorted(municipalities)
    
    def get_municipality_metadata(self, municipality_name: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a municipality using existing legacy logic
        Following FUNDAMENTAL RULE: Reuses existing metadata extraction
        """
        try:
            # Import the municipality module
            module = importlib.import_module(f"{municipality_name}.people")
            
            # Find any scraper class (PersonScraper, CanadianScraper, etc.)
            scraper_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (hasattr(attr, '__bases__') and 
                    any('Scraper' in base.__name__ for base in attr.__bases__)):
                    scraper_class = attr
                    break
            
            if not scraper_class:
                return None
                
            # Extract metadata using existing patterns
            metadata = {
                'name': getattr(scraper_class, 'name', municipality_name),
                'division_id': getattr(scraper_class, 'division_id', None),
                'division_name': getattr(scraper_class, 'division_name', None),
                'classification': getattr(scraper_class, 'classification', 'legislature'),
                'csv_url': getattr(scraper_class, 'csv_url', None),
                'scraper_class': scraper_class.__name__,
                'module_name': municipality_name
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error getting metadata for {municipality_name}: {e}")
            return None
    
    async def scrape_municipality_data(self, municipality_name: str) -> Optional[Dict[str, Any]]:
        """
        Scrape data for a municipality using existing legacy scraper
        Following FUNDAMENTAL RULE: Uses existing scraper classes
        """
        try:
            metadata = self.get_municipality_metadata(municipality_name)
            if not metadata:
                return None
                
            logger.info(f"🔍 Scraping {municipality_name}: {metadata['name']}")
            
            # Import and instantiate the scraper
            module = importlib.import_module(f"{municipality_name}.people")
            scraper_class = getattr(module, metadata['scraper_class'])
            
            # Create scraper instance
            scraper = scraper_class()
            
            # Scrape the data using existing methods
            if hasattr(scraper, 'scrape'):
                people = list(scraper.scrape())
            else:
                # Fallback for CSV scrapers
                people = list(scraper._scrape())
            
            # Transform to our format
            councillors = []
            for person in people:
                councillor_data = {
                    'id': str(uuid.uuid4()),
                    'name': person.name,
                    'municipality': municipality_name,
                    'municipality_name': metadata['name'],
                    'division_id': metadata.get('division_id'),
                    'division_name': metadata.get('division_name'),
                    'classification': metadata.get('classification'),
                    'offices': [],
                    'sources': []
                }
                
                # Extract contact information
                if hasattr(person, 'contact_details'):
                    for contact in person.contact_details:
                        office_data = {
                            'type': contact.get('type', 'unknown'),
                            'value': contact.get('value', ''),
                            'note': contact.get('note', ''),
                            'label': contact.get('label', '')
                        }
                        councillor_data['offices'].append(office_data)
                
                # Extract sources
                if hasattr(person, 'sources'):
                    councillor_data['sources'] = [str(source) for source in person.sources]
                
                councillors.append(councillor_data)
            
            return {
                'municipality': municipality_name,
                'metadata': metadata,
                'councillors': councillors,
                'scraped_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error scraping {municipality_name}: {e}")
            self.stats.errors.append(f"{municipality_name}: {str(e)}")
            return None
    
    async def ingest_municipality_data(self, municipality_data: Dict[str, Any]) -> None:
        """
        Ingest scraped municipality data into database
        Following FUNDAMENTAL RULE: Uses existing database schema
        """
        try:
            conn = await asyncpg.connect(self.database_url)
            
            async with conn.transaction():
                municipality_name = municipality_data['municipality']
                councillors = municipality_data['councillors']
                
                # Insert municipality record if it doesn't exist
                await self._upsert_municipality(conn, municipality_data['metadata'])
                
                # Insert councillors and their offices
                for councillor in councillors:
                    councillor_id = await self._upsert_councillor(conn, councillor)
                    
                    # Insert offices
                    for office in councillor['offices']:
                        await self._upsert_office(conn, councillor_id, office)
                
                self.stats.municipalities_processed += 1
                self.stats.councillors_inserted += len(councillors)
                
        except Exception as e:
            logger.error(f"Error ingesting {municipality_data['municipality']}: {e}")
            self.stats.errors.append(f"Ingestion error for {municipality_data['municipality']}: {str(e)}")
        finally:
            await conn.close()
    
    async def _upsert_municipality(self, conn: asyncpg.Connection, metadata: Dict[str, Any]) -> str:
        """Upsert municipality record"""
        # Use existing municipalities table or create if needed
        query = """
        INSERT INTO municipalities (name, division_id, division_name, classification, 
                                 created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $5)
        ON CONFLICT (name) DO UPDATE SET
            division_id = EXCLUDED.division_id,
            division_name = EXCLUDED.division_name,
            classification = EXCLUDED.classification,
            updated_at = $5
        RETURNING id
        """
        
        result = await conn.fetchval(
            query,
            metadata['name'],
            metadata.get('division_id'),
            metadata.get('division_name'),
            metadata.get('classification'),
            datetime.utcnow()
        )
        
        return result
    
    async def _upsert_councillor(self, conn: asyncpg.Connection, councillor: Dict[str, Any]) -> str:
        """Upsert councillor record"""
        # Use existing members table or create if needed
        query = """
        INSERT INTO members (name, municipality, municipality_name, division_id, 
                           division_name, classification, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $7)
        ON CONFLICT (name, municipality) DO UPDATE SET
            municipality_name = EXCLUDED.municipality_name,
            division_id = EXCLUDED.division_id,
            division_name = EXCLUDED.division_name,
            classification = EXCLUDED.classification,
            updated_at = $7
        RETURNING id
        """
        
        result = await conn.fetchval(
            query,
            councillor['name'],
            councillor['municipality'],
            councillor['municipality_name'],
            councillor.get('division_id'),
            councillor.get('division_name'),
            councillor.get('classification'),
            datetime.utcnow()
        )
        
        return result
    
    async def _upsert_office(self, conn: asyncpg.Connection, councillor_id: str, office: Dict[str, Any]) -> None:
        """Upsert office record"""
        # Use existing offices table or create if needed
        query = """
        INSERT INTO offices (member_id, type, value, note, label, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $6)
        ON CONFLICT (member_id, type, value) DO UPDATE SET
            note = EXCLUDED.note,
            label = EXCLUDED.label,
            updated_at = $6
        """
        
        await conn.execute(
            query,
            councillor_id,
            office['type'],
            office['value'],
            office.get('note'),
            office.get('label'),
            datetime.utcnow()
        )
    
    async def run_full_ingestion(self) -> MunicipalIngestionStats:
        """
        Run full municipal data ingestion using all available scrapers
        Following FUNDAMENTAL RULE: Uses existing scraper infrastructure
        """
        logger.info("🚀 Starting full municipal data ingestion")
        logger.info("📋 Following FUNDAMENTAL RULE: Using existing legacy scraper infrastructure")
        
        municipalities = self.get_available_municipalities()
        logger.info(f"📍 Found {len(municipalities)} municipal scrapers")
        
        # Process municipalities in batches to avoid memory issues
        batch_size = 10
        for i in range(0, len(municipalities), batch_size):
            batch = municipalities[i:i + batch_size]
            logger.info(f"🔄 Processing batch {i//batch_size + 1}/{(len(municipalities) + batch_size - 1)//batch_size}")
            
            # Scrape and ingest batch
            for municipality in batch:
                try:
                    municipality_data = await self.scrape_municipality_data(municipality)
                    if municipality_data:
                        await self.ingest_municipality_data(municipality_data)
                        logger.info(f"✅ Processed {municipality}: {len(municipality_data['councillors'])} councillors")
                    else:
                        logger.warning(f"⚠️  No data for {municipality}")
                except Exception as e:
                    logger.error(f"❌ Error processing {municipality}: {e}")
                    self.stats.errors.append(f"Processing error for {municipality}: {str(e)}")
            
            # Small delay between batches
            await asyncio.sleep(1)
        
        logger.info("✅ Municipal data ingestion completed!")
        logger.info(f"📊 Stats: {self.stats.municipalities_processed} municipalities, "
                   f"{self.stats.councillors_inserted} councillors, "
                   f"{len(self.stats.errors)} errors")
        
        return self.stats

# For backward compatibility
MunicipalIngestionStats = MunicipalIngestionStats
