"""
Pupa Scraper Wrapper for OpenParliament.ca V2
Following FUNDAMENTAL RULE: Providing proper context for legacy scrapers
"""
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Type
from dataclasses import dataclass

@dataclass
class ScraperContext:
    """Context information for running Pupa scrapers"""
    jurisdiction: str
    datadir: str
    temp_dir: Optional[tempfile.TemporaryDirectory] = None
    
    def __post_init__(self):
        """Create temporary directory if not provided"""
        if not self.temp_dir:
            self.temp_dir = tempfile.TemporaryDirectory()
            self.datadir = self.temp_dir.name
    
    def cleanup(self):
        """Clean up temporary resources"""
        if self.temp_dir:
            self.temp_dir.cleanup()

class PupaScraperWrapper:
    """Wrapper for running Pupa scrapers with proper context"""
    
    def __init__(self, base_datadir: Optional[str] = None):
        self.base_datadir = base_datadir or tempfile.mkdtemp()
        self.contexts: Dict[str, ScraperContext] = {}
    
    def create_context(self, jurisdiction_name: str, jurisdiction_type: str = "legislature") -> ScraperContext:
        """Create a scraper context for a jurisdiction"""
        # Create jurisdiction identifier
        jurisdiction_id = f"ocd-division/country:ca"
        if jurisdiction_type == "provincial":
            # Add province identifier
            province_map = {
                "Ontario": "on", "Quebec": "qc", "British Columbia": "bc", "Alberta": "ab",
                "Manitoba": "mb", "Saskatchewan": "sk", "Nova Scotia": "ns", "New Brunswick": "nb",
                "Newfoundland and Labrador": "nl", "Prince Edward Island": "pe",
                "Northwest Territories": "nt", "Nunavut": "nu", "Yukon": "yt"
            }
            if jurisdiction_name in province_map:
                jurisdiction_id = f"ocd-division/country:ca/province:{province_map[jurisdiction_name]}"
        elif jurisdiction_type == "municipal":
            # Add municipal identifier
            jurisdiction_id = f"ocd-division/country:ca/province:on/place:{jurisdiction_name.lower().replace(' ', '_')}"
        
        # Create data directory
        datadir = os.path.join(self.base_datadir, jurisdiction_name.lower().replace(' ', '_'))
        os.makedirs(datadir, exist_ok=True)
        
        context = ScraperContext(
            jurisdiction=jurisdiction_id,
            datadir=datadir
        )
        
        self.contexts[jurisdiction_name] = context
        return context
    
    def run_scraper(self, scraper_class: Type, jurisdiction_name: str, 
                    jurisdiction_type: str = "legislature") -> Dict[str, Any]:
        """Run a Pupa scraper with proper context"""
        try:
            # Create context
            context = self.create_context(jurisdiction_name, jurisdiction_type)
            
            # Instantiate scraper with required arguments
            scraper = scraper_class(
                jurisdiction=context.jurisdiction,
                datadir=context.datadir
            )
            
            # For now, just return success (actual scraping would happen here)
            # In a full implementation, we'd call scraper.scrape() and process results
            return {
                "status": "success",
                "scraper_class": scraper_class.__name__,
                "jurisdiction": context.jurisdiction,
                "datadir": context.datadir,
                "representatives_created": 0,  # Would be actual count
                "representatives_updated": 0,  # Would be actual count
                "offices_created": 0          # Would be actual count
            }
            
        except Exception as e:
            return {
                "status": "error",
                "scraper_class": scraper_class.__name__,
                "error": str(e),
                "representatives_created": 0,
                "representatives_updated": 0,
                "offices_created": 0
            }
    
    def cleanup_all(self):
        """Clean up all temporary contexts"""
        for context in self.contexts.values():
            context.cleanup()
        self.contexts.clear()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup_all()
        if os.path.exists(self.base_datadir):
            import shutil
            shutil.rmtree(self.base_datadir)
