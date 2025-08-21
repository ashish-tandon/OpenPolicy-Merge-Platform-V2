"""
Legacy Data Ingester for OpenParliament.ca V2

Following FUNDAMENTAL RULE: Uses existing legacy data structure
Source: data/legacy_adapted/legacy_collected_*.json
"""
import json
import logging
import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import asyncpg
import os
from dataclasses import dataclass

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class IngestionStats:
    """Statistics for data ingestion run"""
    mps_inserted: int = 0
    mps_updated: int = 0
    bills_inserted: int = 0
    bills_updated: int = 0
    votes_inserted: int = 0
    votes_updated: int = 0
    offices_inserted: int = 0
    ballots_inserted: int = 0
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []

class LegacyDataIngester:
    """
    Ingests legacy OpenParliament data into database
    Following FUNDAMENTAL RULE: Uses existing data structure from legacy adapters
    """
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.stats = IngestionStats()
        
    async def ingest_json_file(self, json_file_path: str) -> IngestionStats:
        """
        Ingest a JSON file produced by legacy adapters
        
        Args:
            json_file_path: Path to JSON file with collected legacy data
            
        Returns:
            IngestionStats: Statistics about the ingestion run
        """
        logger.info(f"🚀 Starting ingestion of {json_file_path}")
        logger.info("📋 Following FUNDAMENTAL RULE: Using legacy data structure")
        
        # Load JSON data
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        # Connect to database
        conn = await asyncpg.connect(self.database_url)
        
        try:
            # Start transaction
            async with conn.transaction():
                # Record data collection run
                run_id = await self._record_collection_run(conn, json_file_path, data)
                
                # Ingest MPs
                if 'mps' in data:
                    await self._ingest_mps(conn, data['mps'])
                
                # Ingest bills
                if 'bills' in data:
                    await self._ingest_bills(conn, data['bills'])
                
                # Skip vote ingestion - requires complex mapping to existing votes table schema
                # if 'votes' in data:
                #     await self._ingest_votes(conn, data['votes'])
                
                # Update collection run as completed
                await self._complete_collection_run(conn, run_id)
                
        except Exception as e:
            logger.error(f"❌ Error during ingestion: {e}")
            self.stats.errors.append(str(e))
            raise
        finally:
            await conn.close()
        
        logger.info("✅ Data ingestion completed successfully!")
        logger.info(f"📊 Stats: {self.stats.mps_inserted} MPs, {self.stats.bills_inserted} bills, {self.stats.votes_inserted} votes")
        
        return self.stats
    
    async def _record_collection_run(self, conn: asyncpg.Connection, json_file: str, data: Dict[str, Any]) -> int:
        """Record the start of a data collection run using existing data_collection table"""
        mps_count = len(data.get('mps', []))
        bills_count = len(data.get('bills', []))
        votes_count = len(data.get('votes', []))
        
        # Use existing data_collection table structure
        run_id = await conn.fetchval("""
            INSERT INTO data_collection 
            (scraper_id, data_type, source_url, collected_at, processed)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
        """, 1, 'legacy_full', json_file, datetime.utcnow(), False)
        
        logger.info(f"📝 Started collection run {run_id} for {mps_count} MPs, {bills_count} bills, {votes_count} votes")
        return run_id
    
    async def _complete_collection_run(self, conn: asyncpg.Connection, run_id: int):
        """Mark collection run as completed using existing data_collection table"""
        await conn.execute("""
            UPDATE data_collection 
            SET processed = $1, processed_at = $2
            WHERE id = $3
        """, True, datetime.utcnow(), run_id)
    
    async def _ingest_mps(self, conn: asyncpg.Connection, mps_data: List[Dict[str, Any]]):
        """Ingest MP data following legacy structure"""
        logger.info(f"👥 Ingesting {len(mps_data)} MPs from legacy data")
        
        for mp_data in mps_data:
            try:
                # Check if MP already exists by name and party
                existing_mp = await conn.fetchrow("""
                    SELECT id FROM representatives 
                    WHERE name = $1 AND party = $2
                """, mp_data['name'], mp_data.get('party_name', ''))
                
                if existing_mp:
                    # Update existing MP
                    mp_id = existing_mp['id']
                    await conn.execute("""
                        UPDATE representatives SET 
                            email = $1, 
                            image_url = $2,
                            website = $3,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = $4
                    """, 
                    mp_data.get('email'),
                    mp_data.get('photo_url'),
                    mp_data.get('personal_url'),
                    mp_id)
                    
                    self.stats.mps_updated += 1
                else:
                    # Insert new MP
                    mp_id = await conn.fetchval("""
                        INSERT INTO representatives 
                        (id, jurisdiction_id, name, party, district, email, image_url, website, role, created_at, updated_at)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                        RETURNING id
                    """,
                    str(uuid.uuid4()),
                    '48d4cd4d-c28c-44bf-887a-1a76948e3c04',  # Federal jurisdiction ID
                    mp_data['name'],
                    mp_data.get('party_name', ''),
                    mp_data.get('riding', ''),
                    mp_data.get('email'),
                    mp_data.get('photo_url'),
                    mp_data.get('personal_url'),
                    'MP')  # Federal MPs have role 'MP'
                    
                    self.stats.mps_inserted += 1
                
                # Skip office insertion - no office tables exist in current schema
                # if 'offices' in mp_data:
                #     await self._ingest_mp_offices(conn, mp_id, mp_data['offices'])
                    
            except Exception as e:
                error_msg = f"Error ingesting MP {mp_data.get('name', 'Unknown')}: {e}"
                logger.error(error_msg)
                self.stats.errors.append(error_msg)
    
    async def _ingest_mp_offices(self, conn: asyncpg.Connection, mp_id: int, offices: List[Dict[str, Any]]):
        """Ingest MP office data"""
        # Clear existing offices for this MP
        await conn.execute("DELETE FROM mp_offices WHERE mp_id = $1", mp_id)
        
        for office in offices:
            await conn.execute("""
                INSERT INTO mp_offices 
                (mp_id, office_type, telephone, fax, postal_address)
                VALUES ($1, $2, $3, $4, $5)
            """,
            mp_id,
            office.get('type', 'unknown'),
            office.get('tel'),
            office.get('fax'),
            office.get('postal'))
            
            self.stats.offices_inserted += 1
    
    async def _ingest_bills(self, conn: asyncpg.Connection, bills_data: List[Dict[str, Any]]):
        """Ingest bill data following legacy structure"""
        logger.info(f"📄 Ingesting {len(bills_data)} bills from legacy data")
        
        for bill_data in bills_data:
            try:
                # Check if bill already exists by bill_number
                existing_bill = await conn.fetchrow("""
                    SELECT id FROM bills 
                    WHERE bill_number = $1
                """, 
                bill_data.get('number'))
                
                if existing_bill:
                    # Update existing bill
                    bill_id = existing_bill['id']
                    await conn.execute("""
                        UPDATE bills SET 
                            title = $1,
                            status = $2,
                            external_id = $3,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = $4
                    """,
                    bill_data.get('name') or f"Bill {bill_data.get('number', 'Unknown')}",  # Use name or generate from number
                    bill_data.get('status') or 'INTRODUCED',  # Default to INTRODUCED if no status
                    str(bill_data.get('id')),  # Use the legacy ID as external_id
                    bill_id)
                    
                    self.stats.bills_updated += 1
                else:
                    # Insert new bill
                    bill_id = await conn.fetchval("""
                        INSERT INTO bills 
                        (id, jurisdiction_id, bill_number, title, status, external_id, created_at, updated_at)
                        VALUES ($1, $2, $3, $4, $5, $6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                        RETURNING id
                    """,
                    str(uuid.uuid4()),
                    '48d4cd4d-c28c-44bf-887a-1a76948e3c04',  # Federal jurisdiction ID
                    bill_data.get('number'),
                    bill_data.get('name') or f"Bill {bill_data.get('number', 'Unknown')}",  # Use name or generate from number
                    bill_data.get('status') or 'INTRODUCED',  # Default to INTRODUCED if no status
                    str(bill_data.get('id')))  # Use the legacy ID as external_id
                    
                    self.stats.bills_inserted += 1
                    
            except Exception as e:
                error_msg = f"Error ingesting bill {bill_data.get('number', 'Unknown')}: {e}"
                logger.error(error_msg)
                self.stats.errors.append(error_msg)
    
    async def _ingest_votes(self, conn: asyncpg.Connection, votes_data: List[Dict[str, Any]]):
        """Ingest vote data following legacy structure"""
        logger.info(f"🗳️ Ingesting {len(votes_data)} votes from legacy data")
        
        for vote_data in votes_data:
            try:
                # Check if vote already exists
                existing_vote = await conn.fetchrow("""
                    SELECT id FROM votes 
                    WHERE parliament_number = $1 AND session_number = $2 AND vote_number = $3
                """, 
                vote_data.get('parliament_number'),
                vote_data.get('session_number'),
                vote_data.get('vote_number'))
                
                if existing_vote:
                    # Update existing vote
                    vote_id = existing_vote['id']
                    await conn.execute("""
                        UPDATE votes SET 
                            description = $1,
                            result = $2,
                            vote_type = $3,
                            yea_count = $4,
                            nay_count = $5,
                            paired_count = $6,
                            legacy_source = $7,
                            extracted_at = $8,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = $9
                    """,
                    vote_data.get('description'),
                    vote_data.get('result'),
                    vote_data.get('vote_type'),
                    vote_data.get('yea_count'),
                    vote_data.get('nay_count'),
                    vote_data.get('paired_count'),
                    vote_data.get('source'),
                    vote_data.get('extracted_at'),
                    vote_id)
                    
                    self.stats.votes_updated += 1
                else:
                    # Insert new vote
                    vote_id = await conn.fetchval("""
                        INSERT INTO votes 
                        (description, result, parliament_number, session_number, vote_number,
                         vote_type, yea_count, nay_count, paired_count, legacy_source,
                         extracted_at, created_at, updated_at)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                        RETURNING id
                    """,
                    vote_data.get('description'),
                    vote_data.get('result'),
                    vote_data.get('parliament_number'),
                    vote_data.get('session_number'),
                    vote_data.get('vote_number'),
                    vote_data.get('vote_type'),
                    vote_data.get('yea_count'),
                    vote_data.get('nay_count'),
                    vote_data.get('paired_count'),
                    vote_data.get('source'),
                    vote_data.get('extracted_at'))
                    
                    self.stats.votes_inserted += 1
                
                # Insert vote ballots if available
                if 'ballots' in vote_data:
                    await self._ingest_vote_ballots(conn, vote_id, vote_data['ballots'])
                    
            except Exception as e:
                error_msg = f"Error ingesting vote {vote_data.get('vote_number', 'Unknown')}: {e}"
                logger.error(error_msg)
                self.stats.errors.append(error_msg)
    
    async def _ingest_vote_ballots(self, conn: asyncpg.Connection, vote_id: int, ballots: List[Dict[str, Any]]):
        """Ingest individual MP vote ballots"""
        # Clear existing ballots for this vote
        await conn.execute("DELETE FROM vote_ballots WHERE vote_id = $1", vote_id)
        
        for ballot in ballots:
            # Find MP by name
            mp_row = await conn.fetchrow("""
                SELECT id FROM members WHERE name = $1 LIMIT 1
            """, ballot.get('mp_name'))
            
            if mp_row:
                await conn.execute("""
                    INSERT INTO vote_ballots 
                    (vote_id, member_id, ballot)
                    VALUES ($1, $2, $3)
                """,
                vote_id,
                mp_row['id'],
                ballot.get('ballot'))
                
                self.stats.ballots_inserted += 1


async def main():
    """Main entry point for legacy data ingestion"""
    # Database URL from environment
    database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/openparliament')
    
    # Find the latest collected data file
    data_dir = Path('data/legacy_adapted')
    json_files = list(data_dir.glob('legacy_collected_*.json'))
    
    if not json_files:
        logger.error("❌ No legacy data files found in data/legacy_adapted/")
        return
    
    # Use the most recent file
    latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
    logger.info(f"📂 Using latest data file: {latest_file}")
    
    # Create ingester and run
    ingester = LegacyDataIngester(database_url)
    stats = await ingester.ingest_json_file(str(latest_file))
    
    # Print final statistics
    logger.info("🎉 Ingestion Complete!")
    logger.info(f"📊 Final Stats:")
    logger.info(f"   MPs: {stats.mps_inserted} inserted, {stats.mps_updated} updated")
    logger.info(f"   Bills: {stats.bills_inserted} inserted, {stats.bills_updated} updated")  
    logger.info(f"   Votes: {stats.votes_inserted} inserted, {stats.votes_updated} updated")
    logger.info(f"   Offices: {stats.offices_inserted} inserted")
    logger.info(f"   Ballots: {stats.ballots_inserted} inserted")
    
    if stats.errors:
        logger.warning(f"⚠️ {len(stats.errors)} errors occurred during ingestion")
        for error in stats.errors[:5]:  # Show first 5 errors
            logger.warning(f"   {error}")


if __name__ == "__main__":
    asyncio.run(main())
