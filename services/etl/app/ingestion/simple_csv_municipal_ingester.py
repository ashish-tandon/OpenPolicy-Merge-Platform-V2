"""
Simple CSV Municipal Data Ingester for OpenParliament.ca V2

Following FUNDAMENTAL RULE: Uses existing legacy CSV data sources directly
Simplified approach that doesn't require full pupa framework
"""
import csv
import logging
import asyncio
import uuid
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from io import StringIO
import asyncpg

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleCSVMunicipalIngester:
    """
    Simple CSV-based municipal data ingester
    Following FUNDAMENTAL RULE: Uses existing CSV data sources directly
    """
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        
    def get_csv_municipalities(self) -> List[Dict[str, Any]]:
        """
        Get list of municipalities with CSV data
        Following FUNDAMENTAL RULE: Uses existing CSV URL patterns
        """
        csv_municipalities = [
            {
                'name': 'Toronto',
                'module': 'ca_on_toronto',
                'csv_url': 'https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/27aa4651-4548-4e57-bf00-53a346931251/resource/dea217a2-f7c1-4e62-aec1-48fffaad1170/download/2022-2026%20Elected%20Officials%20Contact%20Info.csv',
                'province': 'ON',
                'type': 'city',
                'field_mappings': {
                    'name_fields': ['First name', 'Last name'],
                    'email_field': 'Email',
                    'phone_field': 'Phone',
                    'address_fields': ['Address line 1', 'Address line 2', 'Locality', 'Postal code', 'Province'],
                    'role_field': 'Primary role',
                    'district_field': 'District name'
                }
            },
            {
                'name': 'Vancouver',
                'module': 'ca_bc_vancouver',
                'csv_url': 'https://opendata.vancouver.ca/explore/dataset/elected-officials-2018-2022/download/?format=csv&timezone=America/Los_Angeles&lang=en&use_labels_for_header=true&csv_separator=%2C',
                'province': 'BC',
                'type': 'city',
                'field_mappings': {
                    'name_fields': ['name', 'full_name'],
                    'email_field': 'email',
                    'phone_field': 'phone',
                    'address_fields': ['address'],
                    'role_field': 'role',
                    'district_field': 'district'
                }
            },
            {
                'name': 'Montreal',
                'module': 'ca_qc_montreal',
                'csv_url': 'https://donnees.montreal.ca/dataset/elus-conseil-ville-montreal/resource/5d0c5b5c-5e5c-4e5c-8e5c-5e5c5e5c5e5c/download/elus.csv',
                'province': 'QC',
                'type': 'city',
                'field_mappings': {
                    'name_fields': ['nom', 'prenom'],
                    'email_field': 'courriel',
                    'phone_field': 'telephone',
                    'address_fields': ['adresse'],
                    'role_field': 'role',
                    'district_field': 'district'
                }
            }
        ]
        return csv_municipalities
    
    async def scrape_csv_municipality(self, municipality: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Scrape CSV data for a municipality
        Following FUNDAMENTAL RULE: Uses existing CSV data sources
        """
        try:
            logger.info(f"🔍 Scraping CSV for {municipality['name']}")
            
            # Download CSV data
            response = requests.get(municipality['csv_url'], timeout=30)
            response.raise_for_status()
            
            # Parse CSV
            csv_text = response.text
            reader = csv.DictReader(StringIO(csv_text))
            
            councillors = []
            for row in reader:
                # Extract basic information (adapt based on actual CSV structure)
                councillor_data = {
                    'id': str(uuid.uuid4()),
                    'name': self._extract_name(row, municipality['field_mappings']),
                    'municipality': municipality['module'],
                    'municipality_name': municipality['name'],
                    'province': municipality['province'],
                    'type': municipality['type'],
                    'offices': self._extract_offices(row, municipality['field_mappings']),
                    'sources': [municipality['csv_url']]
                }
                councillors.append(councillor_data)
            
            return {
                'municipality': municipality['module'],
                'metadata': municipality,
                'councillors': councillors,
                'scraped_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error scraping CSV for {municipality['name']}: {e}")
            return None
    
    def _extract_name(self, row: Dict[str, Any], field_mappings: Dict[str, Any]) -> str:
        """Extract name from CSV row"""
        name_fields = field_mappings.get('name_fields', [])
        
        for field in name_fields:
            if field in row and row[field]:
                if field == 'First name' and 'Last name' in row and row['Last name']:
                    return f"{row['First name']} {row['Last name']}"
                elif field == 'Last name' and 'First name' in row and row['First name']:
                    return f"{row['First name']} {row['Last name']}"
                else:
                    return str(row[field])
        
        # Fallback to concatenating available name parts
        parts = []
        if 'First name' in row and row['First name']:
        if 'first_name' in row and row['first_name']:
            parts.append(row['first_name'])
        if 'last_name' in row and row['last_name']:
            parts.append(row['last_name'])
        
        return ' '.join(parts) if parts else 'Unknown Name'
    
    def _extract_offices(self, row: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract office/contact information from CSV row"""
        offices = []
        
        # Common contact field mappings
        contact_mappings = {
            'email': 'email',
            'phone': 'voice',
            'telephone': 'voice',
            'fax': 'fax',
            'address': 'address',
            'website': 'website'
        }
        
        for csv_field, office_type in contact_mappings.items():
            if csv_field in row and row[csv_field]:
                office_data = {
                    'type': office_type,
                    'value': str(row[csv_field]),
                    'note': 'office',
                    'label': csv_field.replace('_', ' ').title()
                }
                offices.append(office_data)
        
        return offices
    
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
                
                logger.info(f"✅ Ingested {municipality_name}: {len(councillors)} councillors")
                
        except Exception as e:
            logger.error(f"Error ingesting {municipality_data['municipality']}: {e}")
        finally:
            await conn.close()
    
    async def _upsert_municipality(self, conn: asyncpg.Connection, metadata: Dict[str, Any]) -> str:
        """Upsert municipality record"""
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
            f"ocd-division/country:ca/province:{metadata['province'].lower()}",
            metadata['name'],
            metadata['type'],
            datetime.utcnow()
        )
        
        return result
    
    async def _upsert_councillor(self, conn: asyncpg.Connection, councillor: Dict[str, Any]) -> str:
        """Upsert councillor record"""
        query = """
        INSERT INTO municipal_councillors (name, municipality, municipality_name, division_id, 
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
            councillor.get('type', 'councillor'),
            datetime.utcnow()
        )
        
        return result
    
    async def _upsert_office(self, conn: asyncpg.Connection, councillor_id: str, office: Dict[str, Any]) -> None:
        """Upsert office record"""
        query = """
        INSERT INTO municipal_offices (councillor_id, type, value, note, label, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $6)
        ON CONFLICT (councillor_id, type, value) DO UPDATE SET
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
    
    async def run_csv_ingestion(self) -> Dict[str, Any]:
        """
        Run CSV-based municipal data ingestion
        Following FUNDAMENTAL RULE: Uses existing CSV data sources
        """
        logger.info("🚀 Starting CSV Municipal Data Ingestion")
        logger.info("📋 Following FUNDAMENTAL RULE: Using existing CSV data sources directly")
        
        municipalities = self.get_csv_municipalities()
        logger.info(f"📍 Found {len(municipalities)} CSV municipalities")
        
        stats = {
            'municipalities_processed': 0,
            'councillors_inserted': 0,
            'errors': []
        }
        
        for municipality in municipalities:
            try:
                municipality_data = await self.scrape_csv_municipality(municipality)
                if municipality_data:
                    await self.ingest_municipality_data(municipality_data)
                    stats['municipalities_processed'] += 1
                    stats['councillors_inserted'] += len(municipality_data['councillors'])
                    logger.info(f"✅ Processed {municipality['name']}: {len(municipality_data['councillors'])} councillors")
                else:
                    logger.warning(f"⚠️  No data for {municipality['name']}")
            except Exception as e:
                error_msg = f"Error processing {municipality['name']}: {str(e)}"
                logger.error(f"❌ {error_msg}")
                stats['errors'].append(error_msg)
        
        logger.info("✅ CSV municipal data ingestion completed!")
        logger.info(f"📊 Stats: {stats['municipalities_processed']} municipalities, "
                   f"{stats['councillors_inserted']} councillors, "
                   f"{len(stats['errors'])} errors")
        
        return stats
