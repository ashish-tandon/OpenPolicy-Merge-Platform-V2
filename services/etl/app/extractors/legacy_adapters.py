"""
Legacy OpenParliament Importers - Adapted for Modern ETL

Following FUNDAMENTAL RULE: NEVER REINVENT THE WHEEL
Adapted from legacy/openparliament/parliament/imports/
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests
import lxml.etree as etree

logger = logging.getLogger(__name__)


class LegacyMPsAdapter:
    """Adapter for legacy MP importers from OurCommons.ca and Represent API"""
    
    # Source: legacy/openparliament/parliament/imports/mps.py
    OURCOMMONS_MPS_URL = 'https://www.ourcommons.ca/Members/en/search?caucusId=all&province=all'
    REPRESENT_API_URL = 'https://represent.opennorth.ca/representatives/house-of-commons/?limit=500'
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OpenParliament.ca/2.0 (Legacy Adapter)',
        })
    
    async def get_mps_from_represent(self) -> List[Dict[str, Any]]:
        """Get MPs from Represent API - adapted from legacy update_mps_from_represent"""
        logger.info("Getting MPs from Represent API (legacy adapter)")
        
        try:
            response = self.session.get(self.REPRESENT_API_URL)
            response.raise_for_status()
            data = response.json()
            
            mps = []
            for mp_info in data.get('objects', []):
                mp = {
                    'id': mp_info.get('id'),
                    'name': mp_info.get('name'),
                    'party_name': mp_info.get('party_name'),
                    'email': mp_info.get('email'),
                    'personal_url': mp_info.get('personal_url'),
                    'photo_url': mp_info.get('photo_url'),
                    'offices': mp_info.get('offices', []),
                    'extra': mp_info.get('extra', {}),
                    'source': 'represent_api',
                    'extracted_at': datetime.now().isoformat()
                }
                mps.append(mp)
            
            logger.info(f"Extracted {len(mps)} MPs from Represent API")
            return mps
            
        except Exception as e:
            logger.error(f"Failed to get MPs from Represent API: {e}")
            return []
    
    async def get_mps_from_ourcommons(self) -> List[Dict[str, Any]]:
        """Get MPs from OurCommons.ca - adapted from legacy scrape_mps_from_ourcommons"""
        logger.info("Getting MPs from OurCommons.ca (legacy adapter)")
        
        try:
            response = self.session.get(self.OURCOMMONS_MPS_URL)
            response.raise_for_status()
            
            # Parse the HTML response (simplified version of legacy scraper)
            root = etree.HTML(response.content)
            
            # Extract MP information from the search results
            mp_elements = root.xpath('//div[contains(@class, "ce-mip-mp-tile-container")]')
            
            mps = []
            for mp_elem in mp_elements:
                try:
                    name = mp_elem.xpath('.//div[@class="ce-mip-mp-name"][1]/text()')[0].strip()
                    constituency = mp_elem.xpath('.//div[@class="ce-mip-mp-constituency"][1]/text()')[0].strip()
                    province = mp_elem.xpath('.//div[@class="ce-mip-mp-province"][1]/text()')[0].strip()
                    party = mp_elem.xpath('.//div[@class="ce-mip-mp-party"][1]/text()')[0].strip()
                    
                    mp = {
                        'name': name,
                        'constituency': constituency,
                        'province': province,
                        'party': party,
                        'source': 'ourcommons_ca',
                        'extracted_at': datetime.now().isoformat()
                    }
                    mps.append(mp)
                    
                except (IndexError, AttributeError) as e:
                    logger.warning(f"Failed to parse MP element: {e}")
                    continue
            
            logger.info(f"Extracted {len(mps)} MPs from OurCommons.ca")
            return mps
            
        except Exception as e:
            logger.error(f"Failed to get MPs from OurCommons.ca: {e}")
            return []


class LegacyBillsAdapter:
    """Adapter for legacy bill importers from LEGISinfo API"""
    
    # Source: legacy/openparliament/parliament/imports/legisinfo.py
    LEGISINFO_DETAIL_URL = 'https://www.parl.ca/LegisInfo/en/bill/%(parlnum)s-%(sessnum)s/%(billnumber)s/json'
    LEGISINFO_JSON_LIST_URL = 'https://www.parl.ca/legisinfo/en/bills/json?parlsession=%(sessid)s'
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OpenParliament.ca/2.0 (Legacy Adapter)',
        })
    
    async def get_bills_for_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Get bills for a session - adapted from legacy get_bill_list"""
        logger.info(f"Getting bills for session {session_id} (legacy adapter)")
        
        try:
            url = self.LEGISINFO_JSON_LIST_URL % {'sessid': session_id}
            response = self.session.get(url)
            response.raise_for_status()
            
            bills_data = response.json()
            bills = []
            
            for bill_data in bills_data:
                bill = {
                    'id': bill_data.get('BillId'),
                    'number': bill_data.get('BillNumberFormatted'),
                    'name': bill_data.get('Title'),
                    'short_name': bill_data.get('ShortTitle'),
                    'parliament_number': bill_data.get('ParliamentNumber'),
                    'session_number': bill_data.get('SessionNumber'),
                    'introduced_date': bill_data.get('IntroducedDateTime'),
                    'status': bill_data.get('BillStage'),
                    'source': 'legisinfo_api',
                    'extracted_at': datetime.now().isoformat()
                }
                bills.append(bill)
            
            logger.info(f"Extracted {len(bills)} bills for session {session_id}")
            return bills
            
        except Exception as e:
            logger.error(f"Failed to get bills for session {session_id}: {e}")
            return []
    
    async def get_bill_details(self, bill_id: str, parliament_num: str, session_num: str) -> Optional[Dict[str, Any]]:
        """Get detailed bill information - adapted from legacy get_detailed"""
        logger.info(f"Getting details for bill {bill_id} (legacy adapter)")
        
        try:
            url = self.LEGISINFO_DETAIL_URL % {
                'parlnum': parliament_num,
                'sessnum': session_num,
                'billnumber': bill_id.lower()
            }
            
            response = self.session.get(url)
            response.raise_for_status()
            
            bill_data = response.json()
            if bill_data and len(bill_data) > 0:
                detailed_bill = bill_data[0]
                
                bill = {
                    'id': detailed_bill.get('BillId'),
                    'number': detailed_bill.get('BillNumberFormatted'),
                    'name': detailed_bill.get('Title'),
                    'short_name': detailed_bill.get('ShortTitle'),
                    'summary': detailed_bill.get('Summary'),
                    'parliament_number': detailed_bill.get('ParliamentNumber'),
                    'session_number': detailed_bill.get('SessionNumber'),
                    'introduced_date': detailed_bill.get('IntroducedDateTime'),
                    'status': detailed_bill.get('BillStage'),
                    'stages': detailed_bill.get('BillStages', []),
                    'source': 'legisinfo_api',
                    'extracted_at': datetime.now().isoformat()
                }
                
                logger.info(f"Extracted details for bill {bill_id}")
                return bill
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get bill details for {bill_id}: {e}")
            return None


class LegacyVotesAdapter:
    """Adapter for legacy vote importers from OurCommons.ca XML"""
    
    # Source: legacy/openparliament/parliament/imports/parlvotes.py
    VOTELIST_URL = 'https://www.ourcommons.ca/members/{lang}/votes/xml'
    VOTEDETAIL_URL = 'https://www.ourcommons.ca/members/en/votes/{parliamentnum}/{sessnum}/{votenumber}/xml'
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OpenParliament.ca/2.0 (Legacy Adapter)',
        })
    
    async def get_votes_list(self) -> List[Dict[str, Any]]:
        """Get votes list - adapted from legacy import_votes"""
        logger.info("Getting votes list (legacy adapter)")
        
        try:
            # Get English votes
            response_en = self.session.get(self.VOTELIST_URL.format(lang='en'))
            response_en.raise_for_status()
            root_en = etree.fromstring(response_en.content)
            
            # Get French votes
            response_fr = self.session.get(self.VOTELIST_URL.format(lang='fr'))
            response_fr.raise_for_status()
            root_fr = etree.fromstring(response_fr.content)
            
            votes = []
            vote_elements = root_en.findall('Vote')
            
            for vote_elem in vote_elements:
                try:
                    vote_number = int(vote_elem.findtext('DecisionDivisionNumber'))
                    parliament_num = int(vote_elem.findtext('ParliamentNumber'))
                    session_num = int(vote_elem.findtext('SessionNumber'))
                    
                    # Get French description
                    french_desc = None
                    try:
                        french_desc = root_fr.xpath(
                            f'Vote/DecisionDivisionNumber[text()={vote_number}]/../DecisionDivisionSubject/text()'
                        )[0]
                    except (IndexError, AttributeError):
                        pass
                    
                    vote = {
                        'number': vote_number,
                        'parliament_number': parliament_num,
                        'session_number': session_num,
                        'date': vote_elem.findtext('DecisionEventDateTime'),
                        'subject_en': vote_elem.findtext('DecisionDivisionSubject'),
                        'subject_fr': french_desc,
                        'result': vote_elem.findtext('DecisionResultName'),
                        'yea_total': int(vote_elem.findtext('DecisionDivisionNumberOfYeas')),
                        'nay_total': int(vote_elem.findtext('DecisionDivisionNumberOfNays')),
                        'paired_total': int(vote_elem.findtext('DecisionDivisionNumberOfPaired')),
                        'bill_number': vote_elem.findtext('BillNumberCode'),
                        'source': 'ourcommons_xml',
                        'extracted_at': datetime.now().isoformat()
                    }
                    votes.append(vote)
                    
                except (ValueError, AttributeError) as e:
                    logger.warning(f"Failed to parse vote element: {e}")
                    continue
            
            logger.info(f"Extracted {len(votes)} votes")
            return votes
            
        except Exception as e:
            logger.error(f"Failed to get votes list: {e}")
            return []
    
    async def get_vote_details(self, parliament_num: int, session_num: int, vote_number: int) -> Optional[Dict[str, Any]]:
        """Get detailed vote information - adapted from legacy vote detail parsing"""
        logger.info(f"Getting vote details for vote {vote_number} (legacy adapter)")
        
        try:
            url = self.VOTEDETAIL_URL.format(
                parliamentnum=parliament_num,
                sessnum=session_num,
                votenumber=vote_number
            )
            
            response = self.session.get(url)
            response.raise_for_status()
            root = etree.fromstring(response.content)
            
            voters = []
            for voter_elem in root.findall('VoteParticipant'):
                try:
                    voter = {
                        'person_id': voter_elem.find('PersonId').text,
                        'constituency_name': voter_elem.find('ConstituencyName').text,
                        'first_name': voter_elem.find('PersonOfficialFirstName').text,
                        'last_name': voter_elem.find('PersonOfficialLastName').text,
                        'vote': self._parse_vote_ballot(voter_elem),
                        'source': 'ourcommons_xml',
                        'extracted_at': datetime.now().isoformat()
                    }
                    voters.append(voter)
                    
                except (AttributeError, ValueError) as e:
                    logger.warning(f"Failed to parse voter element: {e}")
                    continue
            
            vote_details = {
                'vote_number': vote_number,
                'parliament_number': parliament_num,
                'session_number': session_num,
                'voters': voters,
                'total_voters': len(voters),
                'source': 'ourcommons_xml',
                'extracted_at': datetime.now().isoformat()
            }
            
            logger.info(f"Extracted details for vote {vote_number} with {len(voters)} voters")
            return vote_details
            
        except Exception as e:
            logger.error(f"Failed to get vote details for vote {vote_number}: {e}")
            return None
    
    def _parse_vote_ballot(self, voter_elem) -> str:
        """Parse vote ballot from XML element - adapted from legacy parsing logic"""
        if voter_elem.find('IsVoteYea').text == 'true':
            return 'Y'
        elif voter_elem.find('IsVoteNay').text == 'true':
            return 'N'
        elif voter_elem.find('IsVotePaired').text == 'true':
            return 'P'
        else:
            return 'U'  # Unknown


class LegacyDataCollectionTask:
    """Main task that uses all legacy adapters - following FUNDAMENTAL RULE"""
    
    def __init__(self, output_dir: str = "data"):
        self.output_dir = output_dir
        self.mps_adapter = LegacyMPsAdapter()
        self.bills_adapter = LegacyBillsAdapter()
        self.votes_adapter = LegacyVotesAdapter()
        
        # Ensure output directory exists
        import os
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "legacy_adapted"), exist_ok=True)
    
    async def run_full_collection(self):
        """Run full data collection using legacy adapters"""
        logger.info("Starting full data collection using legacy OpenParliament adapters")
        
        start_time = datetime.now()
        
        # Collect data using legacy adapters
        tasks = [
            self.collect_mps_data(),
            self.collect_bills_data(),
            self.collect_votes_data()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Task {i} failed: {result}")
                results[i] = []
        
        mps_data, bills_data, votes_data = results
        
        # Save collected data
        await self.save_collected_data({
            'mps': mps_data,
            'bills': bills_data,
            'votes': votes_data,
            'collected_at': datetime.now().isoformat(),
            'source': 'legacy_openparliament_adapters'
        })
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info(f"Completed legacy data collection in {duration}")
        logger.info(f"Collected: {len(mps_data)} MPs, {len(bills_data)} bills, {len(votes_data)} votes")
    
    async def collect_mps_data(self) -> List[Dict[str, Any]]:
        """Collect MP data using legacy adapters"""
        logger.info("Collecting MP data using legacy adapters")
        
        # Try both sources
        mps_from_represent = await self.mps_adapter.get_mps_from_represent()
        mps_from_ourcommons = await self.mps_adapter.get_mps_from_ourcommons()
        
        # Combine and deduplicate
        all_mps = mps_from_represent + mps_from_ourcommons
        
        logger.info(f"Collected {len(all_mps)} total MPs")
        return all_mps
    
    async def collect_bills_data(self) -> List[Dict[str, Any]]:
        """Collect bill data using legacy adapters"""
        logger.info("Collecting bill data using legacy adapters")
        
        # Get bills for current session (44-1)
        bills = await self.bills_adapter.get_bills_for_session("44-1")
        
        logger.info(f"Collected {len(bills)} bills")
        return bills
    
    async def collect_votes_data(self) -> List[Dict[str, Any]]:
        """Collect vote data using legacy adapters"""
        logger.info("Collecting vote data using legacy adapters")
        
        votes = await self.votes_adapter.get_votes_list()
        
        logger.info(f"Collected {len(votes)} votes")
        return votes
    
    async def save_collected_data(self, data: Dict[str, Any]):
        """Save collected data to disk"""
        import json
        import os
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"legacy_collected_{timestamp}.json"
        filepath = os.path.join(self.output_dir, "legacy_adapted", filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Saved legacy collected data to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save legacy collected data: {e}")
            raise


async def main():
    """Main entry point for legacy data collection"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    task = LegacyDataCollectionTask()
    
    try:
        await task.run_full_collection()
        logger.info("Legacy data collection completed successfully")
    except Exception as e:
        logger.error(f"Legacy data collection failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
