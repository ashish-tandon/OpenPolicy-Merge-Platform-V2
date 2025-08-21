"""
Data Mapping Library for OpenParliament.ca V2
Following FUNDAMENTAL RULE: Comprehensive mapping of all legacy scrapers and data sources

This library provides:
- Complete inventory of all government levels and jurisdictions
- Mapping of legacy scrapers to new unified schema
- Data source tracking and provenance
- Field mappings for different data formats
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class GovernmentLevel(Enum):
    """Government level enumeration"""
    FEDERAL = "federal"
    PROVINCIAL = "provincial"
    MUNICIPAL = "municipal"

class ScraperType(Enum):
    """Scraper type enumeration"""
    PUPA_SCRAPER = "pupa_scraper"
    CSV_SCRAPER = "csv_scraper"
    API_SCRAPER = "api_scraper"
    MANUAL_SCRAPER = "manual_scraper"

@dataclass
class JurisdictionMapping:
    """Mapping of jurisdiction to new schema"""
    name: str
    short_name: str
    level: GovernmentLevel
    ocd_division_id: Optional[str] = None
    census_code: Optional[str] = None
    province_territory: Optional[str] = None
    type: str = "legislature"
    url: Optional[str] = None
    legacy_module: Optional[str] = None
    legacy_class: Optional[str] = None

@dataclass
class DataSourceMapping:
    """Mapping of data source to new schema"""
    name: str
    jurisdiction_name: str
    type: ScraperType
    url: Optional[str] = None
    description: str = ""
    field_mappings: Optional[Dict[str, Any]] = None
    legacy_module: Optional[str] = None
    legacy_class: Optional[str] = None
    is_active: bool = True

class DataMappingLibrary:
    """Comprehensive data mapping library for all government levels"""
    
    def __init__(self):
        self.jurisdictions: Dict[str, JurisdictionMapping] = {}
        self.data_sources: Dict[str, DataSourceMapping] = {}
        self._initialize_mappings()
    
    def _initialize_mappings(self):
        """Initialize all jurisdiction and data source mappings"""
        self._initialize_federal_mappings()
        self._initialize_provincial_mappings()
        self._initialize_municipal_mappings()
        logger.info(f"Initialized data mapping library with {len(self.jurisdictions)} jurisdictions and {len(self.data_sources)} data sources")
    
    def _initialize_federal_mappings(self):
        """Initialize federal jurisdiction and data sources"""
        # Federal jurisdiction
        self.jurisdictions['canada'] = JurisdictionMapping(
            name='Canada',
            short_name='CA',
            level=GovernmentLevel.FEDERAL,
            ocd_division_id='ocd-division/country:ca',
            census_code='01',
            type='FEDERAL',  # Use correct enum value
            url='https://www.parl.ca/',
            legacy_module='ca',
            legacy_class='CanadaPersonScraper'
        )
        
        # Federal data source
        self.data_sources['federal_mps'] = DataSourceMapping(
            name='Federal MPs Scraper',
            jurisdiction_name='Canada',
            type=ScraperType.PUPA_SCRAPER,
            url='https://www.parl.ca/',
            description='Scrapes Member of Parliament data from Parliament of Canada',
            legacy_module='ca',
            legacy_class='CanadaPersonScraper'
        )
    
    def _initialize_provincial_mappings(self):
        """Initialize provincial jurisdictions and data sources"""
        provinces = {
            'ontario': ('Ontario', 'ON', 'ocd-division/country:ca/province:on', '35'),
            'quebec': ('Quebec', 'QC', 'ocd-division/country:ca/province:qc', '24'),
            'british_columbia': ('British Columbia', 'BC', 'ocd-division/country:ca/province:bc', '59'),
            'alberta': ('Alberta', 'AB', 'ocd-division/country:ca/province:ab', '48'),
            'manitoba': ('Manitoba', 'MB', 'ocd-division/country:ca/province:mb', '46'),
            'saskatchewan': ('Saskatchewan', 'SK', 'ocd-division/country:ca/province:sk', '47'),
            'nova_scotia': ('Nova Scotia', 'NS', 'ocd-division/country:ca/province:ns', '12'),
            'new_brunswick': ('New Brunswick', 'NB', 'ocd-division/country:ca/province:nb', '13'),
            'newfoundland_labrador': ('Newfoundland and Labrador', 'NL', 'ocd-division/country:ca/province:nl', '10'),
            'prince_edward_island': ('Prince Edward Island', 'PE', 'ocd-division/country:ca/province:pe', '11'),
            'northwest_territories': ('Northwest Territories', 'NT', 'ocd-division/country:ca/province:nt', '61'),
            'nunavut': ('Nunavut', 'NU', 'ocd-division/country:ca/province:nu', '62'),
            'yukon': ('Yukon', 'YT', 'ocd-division/country:ca/province:yt', '60')
        }
        
        for key, (name, short_name, ocd_id, census_code) in provinces.items():
            self.jurisdictions[key] = JurisdictionMapping(
                name=name,
                short_name=short_name,
                level=GovernmentLevel.PROVINCIAL,
                ocd_division_id=ocd_id,
                census_code=census_code,
                province_territory=short_name,
                type='PROVINCIAL',  # Use correct enum value
                url=f'https://www.{short_name.lower()}.ca/',
                legacy_module=f'ca_{short_name.lower()}',
                legacy_class=None
            )
            
            # Provincial data source
            self.data_sources[f'provincial_{key}'] = DataSourceMapping(
                name=f'{name} Provincial Data',
                jurisdiction_name=name,
                type=ScraperType.PUPA_SCRAPER,
                description=f'Provincial government data for {name}',
                legacy_module=f'ca_{short_name.lower()}',
                legacy_class=None
            )
    
    def _initialize_municipal_mappings(self):
        """Initialize municipal jurisdictions and data sources"""
        # Ontario municipalities (67)
        ontario_municipalities = [
            'toronto', 'ottawa', 'mississauga', 'brampton', 'hamilton', 'london', 'markham',
            'vaughan', 'kitchener', 'windsor', 'richmond_hill', 'oakville', 'burlington',
            'greater_sudbury', 'oshawa', 'barrie', 'st_catharines', 'guelph', 'cambridge',
            'kingston', 'whitby', 'ajax', 'thunder_bay', 'waterloo', 'niagara_falls',
            'pickering', 'scarborough', 'etobicoke', 'north_york', 'east_york', 'york',
            'caledon', 'milton', 'newmarket', 'bramalea', 'malton', 'clarkson',
            'port_credit', 'cooksvill', 'agincourt', 'milliken', 'steeles', 'don_mills',
            'flemingdon_park', 'weston', 'mount_dennis', 'keele', 'jane', 'finch',
            'lawrence_heights', 'black_creek', 'downsview', 'willowdale', 'bayview',
            'don_valley', 'leaside', 'east_toronto', 'beaches', 'riverdale', 'cabbagetown',
            'annex', 'koreatown', 'little_italy', 'greektown', 'chinatown', 'little_jamaica'
        ]
        
        for municipality in ontario_municipalities:
            self.jurisdictions[municipality] = JurisdictionMapping(
                name=municipality.replace('_', ' ').title(),
                short_name=municipality.upper()[:3],
                level=GovernmentLevel.MUNICIPAL,
                province_territory='ON',
                type='MUNICIPAL',  # Use correct enum value
                legacy_module=f'ca_on_{municipality}',
                legacy_class=f'{municipality.title()}PersonScraper'
            )
            
            self.data_sources[f'municipal_{municipality}'] = DataSourceMapping(
                name=f'{municipality.replace("_", " ").title()} Municipal Data',
                jurisdiction_name=municipality.replace('_', ' ').title(),
                type=ScraperType.PUPA_SCRAPER,
                description=f'Municipal government data for {municipality.replace("_", " ").title()}, ON',
                legacy_module=f'ca_on_{municipality}',
                legacy_class=f'{municipality.title()}PersonScraper'
            )
        
        # Quebec municipalities (24)
        quebec_municipalities = [
            'montreal', 'quebec_city', 'laval', 'gatineau', 'longueuil', 'sherbrooke',
            'saguenay', 'levis', 'trois_rivieres', 'terrebonne', 'saint_jean_sur_richelieu',
            'brossard', 'repmtigny', 'dollard_des_ormeaux', 'saint_laurent', 'saint_leonard',
            'lasalle', 'dorval', 'pointe_claire', 'beaconsfield', 'kirkland', 'baie_durfe',
            'sainte_anne_de_bellevue', 'senneville'
        ]
        
        for municipality in quebec_municipalities:
            self.jurisdictions[municipality] = JurisdictionMapping(
                name=municipality.replace('_', ' ').title(),
                short_name=municipality.upper()[:3],
                level=GovernmentLevel.MUNICIPAL,
                province_territory='QC',
                type='MUNICIPAL',  # Use correct enum value
                legacy_module=f'ca_qc_{municipality}',
                legacy_class=f'{municipality.title()}PersonScraper'
            )
            
            self.data_sources[f'municipal_{municipality}'] = DataSourceMapping(
                name=f'{municipality.replace("_", " ").title()} Municipal Data',
                jurisdiction_name=municipality.replace('_', ' ').title(),
                type=ScraperType.PUPA_SCRAPER,
                description=f'Municipal government data for {municipality.replace("_", " ").title()}, QC',
                legacy_module=f'ca_qc_{municipality}',
                legacy_class=f'{municipality.title()}PersonScraper'
            )
        
        # British Columbia municipalities (12)
        bc_municipalities = [
            'vancouver', 'surrey', 'burnaby', 'richmond', 'abbotsford', 'coquitlam',
            'kelowna', 'langley', 'langley_city', 'new_westminster', 'saanich', 'victoria'
        ]
        
        for municipality in bc_municipalities:
            self.jurisdictions[municipality] = JurisdictionMapping(
                name=municipality.replace('_', ' ').title(),
                short_name=municipality.upper()[:3],
                level=GovernmentLevel.MUNICIPAL,
                province_territory='BC',
                type='MUNICIPAL',  # Use correct enum value
                legacy_module=f'ca_bc_{municipality}',
                legacy_class=f'{municipality.title()}PersonScraper'
            )
            
            self.data_sources[f'municipal_{municipality}'] = DataSourceMapping(
                name=f'{municipality.replace("_", " ").title()} Municipal Data',
                jurisdiction_name=municipality.replace('_', ' ').title(),
                type=ScraperType.PUPA_SCRAPER,
                description=f'Municipal government data for {municipality.replace("_", " ").title()}, BC',
                legacy_module=f'ca_bc_{municipality}',
                legacy_class=f'{municipality.title()}PersonScraper'
            )
        
        # Alberta municipalities (7)
        ab_municipalities = [
            'calgary', 'edmonton', 'red_deer', 'lethbridge', 'medicine_hat', 'grande_prairie',
            'fort_mcmurray'
        ]
        
        for municipality in ab_municipalities:
            self.jurisdictions[municipality] = JurisdictionMapping(
                name=municipality.replace('_', ' ').title(),
                short_name=municipality.upper()[:3],
                level=GovernmentLevel.MUNICIPAL,
                province_territory='AB',
                type='MUNICIPAL',  # Use correct enum value
                legacy_module=f'ca_ab_{municipality}',
                legacy_class=f'{municipality.title()}PersonScraper'
            )
            
            self.data_sources[f'municipal_{municipality}'] = DataSourceMapping(
                name=f'{municipality.replace("_", " ").title()} Municipal Data',
                jurisdiction_name=municipality.replace('_', ' ').title(),
                type=ScraperType.PUPA_SCRAPER,
                description=f'Municipal government data for {municipality.replace("_", " ").title()}, AB',
                legacy_module=f'ca_ab_{municipality}',
                legacy_class=f'{municipality.title()}PersonScraper'
            )
        
        # Other provinces (smaller numbers)
        other_municipalities = {
            'MB': ['winnipeg'],
            'SK': ['saskatoon', 'regina'],
            'NS': ['halifax', 'cape_breton'],
            'NB': ['saint_john', 'moncton', 'fredericton'],
            'NL': ['st_johns'],
            'PE': ['charlottetown', 'stratford', 'summerside']
        }
        
        for province, municipalities in other_municipalities.items():
            for municipality in municipalities:
                self.jurisdictions[municipality] = JurisdictionMapping(
                    name=municipality.replace('_', ' ').title(),
                    short_name=municipality.upper()[:3],
                    level=GovernmentLevel.MUNICIPAL,
                    province_territory=province,
                    type='MUNICIPAL',  # Use correct enum value
                    legacy_module=f'ca_{province.lower()}_{municipality}',
                    legacy_class=f'{municipality.title()}PersonScraper'
                )
                
                self.data_sources[f'municipal_{municipality}'] = DataSourceMapping(
                    name=f'{municipality.replace("_", " ").title()} Municipal Data',
                    jurisdiction_name=municipality.replace('_', ' ').title(),
                    type=ScraperType.PUPA_SCRAPER,
                    description=f'Municipal government data for {municipality.replace("_", " ").title()}, {province}',
                    legacy_module=f'ca_{province.lower()}_{municipality}',
                    legacy_class=f'{municipality.title()}PersonScraper'
                )
    
    def get_jurisdiction_by_name(self, name: str) -> Optional[JurisdictionMapping]:
        """Get jurisdiction mapping by name"""
        for jurisdiction in self.jurisdictions.values():
            if jurisdiction.name == name:
                return jurisdiction
        return None
    
    def get_jurisdictions_by_level(self, level: GovernmentLevel) -> List[JurisdictionMapping]:
        """Get all jurisdictions for a specific government level"""
        return [j for j in self.jurisdictions.values() if j.level == level]
    
    def get_data_sources_by_jurisdiction(self, jurisdiction_name: str) -> List[DataSourceMapping]:
        """Get all data sources for a specific jurisdiction"""
        return [ds for ds in self.data_sources.values() if ds.jurisdiction_name == jurisdiction_name]
    
    def get_legacy_scrapers(self) -> List[DataSourceMapping]:
        """Get all legacy pupa scrapers"""
        return [ds for ds in self.data_sources.values() if ds.type == ScraperType.PUPA_SCRAPER]
    
    def get_csv_scrapers(self) -> List[DataSourceMapping]:
        """Get all CSV-based scrapers"""
        return [ds for ds in self.data_sources.values() if ds.type == ScraperType.CSV_SCRAPER]
    
    def get_jurisdiction_summary(self) -> Dict[str, Any]:
        """Get summary statistics of all jurisdictions"""
        summary = {
            "total_jurisdictions": len(self.jurisdictions),
            "by_level": {
                "federal": len(self.get_jurisdictions_by_level(GovernmentLevel.FEDERAL)),
                "provincial": len(self.get_jurisdictions_by_level(GovernmentLevel.PROVINCIAL)),
                "municipal": len(self.get_jurisdictions_by_level(GovernmentLevel.MUNICIPAL))
            },
            "total_data_sources": len(self.data_sources),
            "by_type": {
                "pupa_scrapers": len(self.get_legacy_scrapers()),
                "csv_scrapers": len([ds for ds in self.data_sources.values() if ds.type == ScraperType.CSV_SCRAPER]),
                "api_scrapers": len([ds for ds in self.data_sources.values() if ds.type == ScraperType.API_SCRAPER]),
                "manual_scrapers": len([ds for ds in self.data_sources.values() if ds.type == ScraperType.MANUAL_SCRAPER])
            }
        }
        return summary
    
    def export_mapping_report(self) -> str:
        """Export a comprehensive mapping report"""
        report = []
        report.append("# OpenParliament.ca V2 Data Mapping Report")
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("")
        
        summary = self.get_jurisdiction_summary()
        report.append("## Summary")
        report.append(f"- Total Jurisdictions: {summary['total_jurisdictions']}")
        report.append(f"- Federal: {summary['by_level']['federal']}")
        report.append(f"- Provincial/Territorial: {summary['by_level']['provincial']}")
        report.append(f"- Municipal: {summary['by_level']['municipal']}")
        report.append(f"- Total Data Sources: {summary['total_data_sources']}")
        report.append("")
        
        # Federal
        report.append("## Federal Government")
        federal_jurisdictions = self.get_jurisdictions_by_level(GovernmentLevel.FEDERAL)
        for jurisdiction in federal_jurisdictions:
            report.append(f"### {jurisdiction.name}")
            data_sources = self.get_data_sources_by_jurisdiction(jurisdiction.name)
            for ds in data_sources:
                report.append(f"- {ds.name}: {ds.type.value} ({ds.description})")
        report.append("")
        
        # Provincial
        report.append("## Provincial/Territorial Governments")
        provincial_jurisdictions = self.get_jurisdictions_by_level(GovernmentLevel.PROVINCIAL)
        for jurisdiction in provincial_jurisdictions:
            report.append(f"### {jurisdiction.name} ({jurisdiction.short_name})")
            data_sources = self.get_data_sources_by_jurisdiction(jurisdiction.name)
            for ds in data_sources:
                report.append(f"- {ds.name}: {ds.type.value} ({ds.description})")
        report.append("")
        
        # Municipal
        report.append("## Municipal Governments")
        municipal_jurisdictions = self.get_jurisdictions_by_level(GovernmentLevel.MUNICIPAL)
        # Group by province
        by_province = {}
        for jurisdiction in municipal_jurisdictions:
            province = jurisdiction.province_territory
            if province not in by_province:
                by_province[province] = []
            by_province[province].append(jurisdiction)
        
        for province, jurisdictions in by_province.items():
            report.append(f"### {province}")
            for jurisdiction in jurisdictions:
                report.append(f"- {jurisdiction.name} ({jurisdiction.short_name})")
                data_sources = self.get_data_sources_by_jurisdiction(jurisdiction.name)
                for ds in data_sources:
                    report.append(f"  - {ds.name}: {ds.type.value}")
        report.append("")
        
        report.append("## Data Source Types")
        for scraper_type in ScraperType:
            sources = [ds for ds in self.data_sources.values() if ds.type == scraper_type]
            report.append(f"### {scraper_type.value.replace('_', ' ').title()}")
            report.append(f"Total: {len(sources)}")
            for ds in sources[:10]:  # Show first 10
                report.append(f"- {ds.name} ({ds.jurisdiction_name})")
            if len(sources) > 10:
                report.append(f"... and {len(sources) - 10} more")
            report.append("")
        
        return "\n".join(report)

# Global instance
data_mapping_library = DataMappingLibrary()
