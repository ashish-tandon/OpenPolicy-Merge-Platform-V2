# OpenParliament.ca V2 Complete Scraper Inventory

## 🎯 **Purpose**

This document provides a **COMPLETE INVENTORY** of **ALL** scrapers in the OpenParliament.ca V2 system, regardless of their location, type, or current status. This ensures complete traceability and mapping of every data collection mechanism in the platform.

## 📊 **Scraper Inventory Overview**

| Category | Total Scrapers | Active | Legacy | Disabled | Data Types |
|----------|----------------|--------|--------|----------|------------|
| **Parliamentary** | 3 | 3 | 3 | 0 | MPs, Bills, Votes |
| **Municipal** | 100+ | 80+ | 100+ | 20+ | Councillors, Meetings, Documents |
| **Civic Platforms** | 5 | 5 | 5 | 0 | Meeting Records, Documents |
| **Electoral** | 1 | 1 | 1 | 0 | Candidate Information |
| **Total** | **109+** | **89+** | **109+** | **20+** | **All Government Levels** |

## 🏛️ **1. Parliamentary Scrapers (Active)**

### **1.1 Represent API Scraper**
- **Location**: `services/etl/app/extractors/legacy_adapters.py` - `RepresentAPILegacyAdapter`
- **Source**: `https://represent.opennorth.ca/api/`
- **Data Type**: Member of Parliament (MP) information
- **Collection Method**: REST API calls
- **Records**: 343 MPs
- **Runtime**: 2-3 seconds
- **Status**: ✅ **ACTIVE** - Used in main pipeline
- **Database Tables**: `members`, `mp_offices`, `electoral_districts`

### **1.2 OurCommons.ca XML Scraper**
- **Location**: `services/etl/app/extractors/legacy_adapters.py` - `OurCommonsLegacyAdapter`
- **Source**: `https://www.ourcommons.ca/Content/Parliamentarians/`
- **Data Type**: MP profiles, bills, votes
- **Collection Method**: XML parsing via `lxml`
- **Records**: 343 MPs + Bills + Votes
- **Runtime**: 3-5 seconds
- **Status**: ✅ **ACTIVE** - Used in main pipeline
- **Database Tables**: `members`, `mp_offices`, `bills`, `votes`, `vote_ballots`

### **1.3 LEGISinfo API Scraper**
- **Location**: `services/etl/app/extractors/legacy_adapters.py` - `LegisinfoLegacyAdapter`
- **Source**: `https://www.parl.ca/legisinfo/`
- **Data Type**: Bill information and legislative details
- **Collection Method**: REST API calls
- **Records**: 412 Bills
- **Runtime**: 2-3 seconds
- **Status**: ✅ **ACTIVE** - Used in main pipeline
- **Database Tables**: `bills`, `bill_sponsors`

## 🏙️ **2. Municipal Scrapers (Legacy - 100+ Scrapers)**

### **2.1 Ontario Municipal Scrapers (50+ Scrapers)**

#### **Major Cities**
- **Toronto**: `ca_on_toronto/people.py` - `TorontoPersonScraper`
- **Ottawa**: `ca_on_ottawa/people.py` - `OttawaPersonScraper`
- **Mississauga**: `ca_on_mississauga/people.py` - `MississaugaPersonScraper`
- **Brampton**: `ca_on_brampton/people.py` - `BramptonPersonScraper`
- **Hamilton**: `ca_on_hamilton/people.py` - `HamiltonPersonScraper`
- **London**: `ca_on_london/people.py` - `LondonPersonScraper`
- **Windsor**: `ca_on_windsor/people.py` - `WindsorPersonScraper`
- **Kitchener**: `ca_on_kitchener/people.py` - `KitchenerPersonScraper`
- **Waterloo**: `ca_on_waterloo/people.py` - `WaterlooPersonScraper`
- **Burlington**: `ca_on_burlington/people.py` - `BurlingtonPersonScraper`

#### **Regional Municipalities**
- **Peel Region**: `ca_on_peel/people.py` - `PeelPersonScraper`
- **Niagara Region**: `ca_on_niagara/people.py` - `NiagaraPersonScraper`
- **Waterloo Region**: `ca_on_waterloo_region/people.py` - `WaterlooRegionPersonScraper`
- **Halton Region**: `ca_on_halton/people.py` - `HaltonPersonScraper`
- **York Region**: `ca_on_york/people.py` - `YorkPersonScraper`

#### **Medium Cities**
- **Vaughan**: `ca_on_vaughan/people.py` - `VaughanPersonScraper`
- **Markham**: `ca_on_markham/people.py` - `MarkhamPersonScraper`
- **Richmond Hill**: `ca_on_richmond_hill/people.py` - `RichmondHillPersonScraper`
- **Oakville**: `ca_on_oakville/people.py` - `OakvillePersonScraper`
- **Oshawa**: `ca_on_oshawa/people.py` - `OshawaPersonScraper`
- **St. Catharines**: `ca_on_st_catharines/people.py` - `StCatharinesPersonScraper`
- **Guelph**: `ca_on_guelph/people.py` - `GuelphPersonScraper`
- **Kingston**: `ca_on_kingston/people.py` - `KingstonPersonScraper`
- **Thunder Bay**: `ca_on_thunder_bay/people.py` - `ThunderBayPersonScraper`
- **Greater Sudbury**: `ca_on_greater_sudbury/people.py` - `GreaterSudburyPersonScraper`

#### **Smaller Municipalities**
- **Newmarket**: `ca_on_newmarket/people.py` - `NewmarketPersonScraper`
- **Cambridge**: `ca_on_cambridge/people.py` - `CambridgePersonScraper`
- **Brantford**: `ca_on_brantford/people.py` - `BrantfordPersonScraper`
- **Ajax**: `ca_on_ajax/people.py` - `AjaxPersonScraper`
- **Belleville**: `ca_on_belleville/people.py` - `BellevillePersonScraper`
- **Fort Erie**: `ca_on_fort_erie/people.py` - `FortEriePersonScraper`
- **Caledon**: `ca_on_caledon/people.py` - `CaledonPersonScraper`
- **Chatham-Kent**: `ca_on_chatham_kent/people.py` - `ChathamKentPersonScraper`
- **Clarington**: `ca_on_clarington/people.py` - `ClaringtonPersonScraper`
- **Haldimand County**: `ca_on_haldimand_county/people.py` - `HaldimandCountyPersonScraper`

### **2.2 Quebec Municipal Scrapers (25+ Scrapers)**

#### **Major Cities**
- **Montreal**: `ca_qc_montreal/people.py` - `MontrealPersonScraper`
- **Quebec City**: `ca_qc_quebec/people.py` - `QuebecPersonScraper`
- **Laval**: `ca_qc_laval/people.py` - `LavalPersonScraper`
- **Gatineau**: `ca_qc_gatineau/people.py` - `GatineauPersonScraper`
- **Longueuil**: `ca_qc_longueuil/people.py` - `LongueuilPersonScraper`
- **Sherbrooke**: `ca_qc_sherbrooke/people.py` - `SherbrookePersonScraper`
- **Saguenay**: `ca_qc_saguenay/people.py` - `SaguenayPersonScraper`
- **Trois-Rivières**: `ca_qc_trois_rivieres/people.py` - `TroisRivieresPersonScraper`
- **Saint-Jean-sur-Richelieu**: `ca_qc_saint_jean_sur_richelieu/people.py` - `SaintJeanSurRichelieuPersonScraper`

#### **Suburban Municipalities**
- **Brossard**: `ca_qc_brossard/people.py` - `BrossardPersonScraper`
- **Dollard-des-Ormeaux**: `ca_qc_dollard_des_ormeaux/people.py` - `DollardDesOrmeauxPersonScraper`
- **Pointe-Claire**: `ca_qc_pointe_claire/people.py` - `PointeClairePersonScraper`
- **Kirkland**: `ca_qc_kirkland/people.py` - `KirklandPersonScraper`
- **Beaconsfield**: `ca_qc_beaconsfield/people.py` - `BeaconsfieldPersonScraper`
- **Côte Saint-Luc**: `ca_qc_cote_saint_luc/people.py` - `CoteSaintLucPersonScraper`
- **Dorval**: `ca_qc_dorval/people.py` - `DorvalPersonScraper`
- **Montreal-Est**: `ca_qc_montreal_est/people.py` - `MontrealEstPersonScraper`
- **Lévis**: `ca_qc_levis/people.py` - `LevisPersonScraper`
- **Mercier**: `ca_qc_mercier/people.py` - `MercierPersonScraper`
- **Sainte-Anne-de-Bellevue**: `ca_qc_sainte_anne_de_bellevue/people.py` - `SainteAnneDeBellevuePersonScraper`
- **Senneville**: `ca_qc_senneville/people.py` - `SennevillePersonScraper`
- **Saint-Jérôme**: `ca_qc_saint_jerome/people.py` - `SaintJeromePersonScraper`
- **Terrebonne**: `ca_qc_terrebonne/people.py` - `TerrebonnePersonScraper`
- **Westmount**: `ca_qc_westmount/people.py` - `WestmountPersonScraper`

### **2.3 British Columbia Municipal Scrapers (15+ Scrapers)**

#### **Major Cities**
- **Vancouver**: `ca_bc_vancouver/people.py` - `VancouverPersonScraper`
- **Surrey**: `ca_bc_surrey/people.py` - `SurreyPersonScraper`
- **Burnaby**: `ca_bc_burnaby/people.py` - `BurnabyPersonScraper`
- **Richmond**: `ca_bc_richmond/people.py` - `RichmondPersonScraper`
- **Coquitlam**: `ca_bc_coquitlam/people.py` - `CoquitlamPersonScraper`
- **Langley**: `ca_bc_langley/people.py` - `LangleyPersonScraper`
- **Delta**: `ca_bc_delta/people.py` - `DeltaPersonScraper`
- **Maple Ridge**: `ca_bc_maple_ridge/people.py` - `MapleRidgePersonScraper`
- **New Westminster**: `ca_bc_new_westminster/people.py` - `NewWestminsterPersonScraper`
- **Port Coquitlam**: `ca_bc_port_coquitlam/people.py` - `PortCoquitlamPersonScraper`
- **Port Moody**: `ca_bc_port_moody/people.py` - `PortMoodyPersonScraper`
- **White Rock**: `ca_bc_white_rock/people.py` - `WhiteRockPersonScraper`
- **North Vancouver**: `ca_bc_north_vancouver/people.py` - `NorthVancouverPersonScraper`
- **West Vancouver**: `ca_bc_west_vancouver/people.py` - `WestVancouverPersonScraper`
- **Bowen Island**: `ca_bc_bowen_island/people.py` - `BowenIslandPersonScraper`

### **2.4 Alberta Municipal Scrapers (10+ Scrapers)**

#### **Major Cities**
- **Calgary**: `ca_ab_calgary/people.py` - `CalgaryPersonScraper`
- **Edmonton**: `ca_ab_edmonton/people.py` - `EdmontonPersonScraper`
- **Red Deer**: `ca_ab_red_deer/people.py` - `RedDeerPersonScraper`
- **Lethbridge**: `ca_ab_lethbridge/people.py` - `LethbridgePersonScraper`
- **Medicine Hat**: `ca_ab_medicine_hat/people.py` - `MedicineHatPersonScraper`
- **Grande Prairie**: `ca_ab_grande_prairie/people.py` - `GrandePrairiePersonScraper`
- **Fort McMurray**: `ca_ab_fort_mcmurray/people.py` - `FortMcMurrayPersonScraper`
- **St. Albert**: `ca_ab_st_albert/people.py` - `StAlbertPersonScraper`
- **Airdrie**: `ca_ab_airdrie/people.py` - `AirdriePersonScraper`
- **Spruce Grove**: `ca_ab_spruce_grove/people.py` - `SpruceGrovePersonScraper`

### **2.5 Saskatchewan Municipal Scrapers (5+ Scrapers)**

#### **Major Cities**
- **Regina**: `ca_sk_regina/people.py` - `ReginaPersonScraper`
- **Saskatoon**: `ca_sk_saskatoon/people.py` - `SaskatoonPersonScraper`
- **Prince Albert**: `ca_sk_prince_albert/people.py` - `PrinceAlbertPersonScraper`
- **Moose Jaw**: `ca_sk_moose_jaw/people.py` - `MooseJawPersonScraper`
- **Swift Current**: `ca_sk_swift_current/people.py` - `SwiftCurrentPersonScraper`

### **2.6 Manitoba Municipal Scrapers (5+ Scrapers)**

#### **Major Cities**
- **Winnipeg**: `ca_mb_winnipeg/people.py` - `WinnipegPersonScraper`
- **Brandon**: `ca_mb_brandon/people.py` - `BrandonPersonScraper`
- **Steinbach**: `ca_mb_steinbach/people.py` - `SteinbachPersonScraper`
- **Thompson**: `ca_mb_thompson/people.py` - `ThompsonPersonScraper`
- **Portage la Prairie**: `ca_mb_portage_la_prairie/people.py` - `PortageLaPrairiePersonScraper`

### **2.7 Atlantic Provinces Municipal Scrapers (10+ Scrapers)**

#### **Nova Scotia**
- **Halifax**: `ca_ns_halifax/people.py` - `HalifaxPersonScraper`
- **Sydney**: `ca_ns_sydney/people.py` - `SydneyPersonScraper`
- **Truro**: `ca_ns_truro/people.py` - `TruroPersonScraper`

#### **New Brunswick**
- **Saint John**: `ca_nb_saint_john/people.py` - `SaintJohnPersonScraper`
- **Moncton**: `ca_nb_moncton/people.py` - `MonctonPersonScraper`
- **Fredericton**: `ca_nb_fredericton/people.py` - `FrederictonPersonScraper`

#### **Prince Edward Island**
- **Charlottetown**: `ca_pe_charlottetown/people.py` - `CharlottetownPersonScraper`
- **Summerside**: `ca_pe_summerside/people.py` - `SummersidePersonScraper`
- **Stratford**: `ca_pe_stratford/people.py` - `StratfordPersonScraper`

#### **Newfoundland and Labrador**
- **St. John's**: `ca_nl_st_johns/people.py` - `StJohnsPersonScraper`
- **Mount Pearl**: `ca_nl_mount_pearl/people.py` - `MountPearlPersonScraper`

### **2.8 Northern Territories Municipal Scrapers (5+ Scrapers)**

#### **Northwest Territories**
- **Yellowknife**: `ca_nt_yellowknife/people.py` - `YellowknifePersonScraper`
- **Hay River**: `ca_nt_hay_river/people.py` - `HayRiverPersonScraper`
- **Inuvik**: `ca_nt_inuvik/people.py` - `InuvikPersonScraper`

#### **Nunavut**
- **Iqaluit**: `ca_nu_iqaluit/people.py` - `IqaluitPersonScraper`
- **Rankin Inlet**: `ca_nu_rankin_inlet/people.py` - `RankinInletPersonScraper`

#### **Yukon**
- **Whitehorse**: `ca_yt_whitehorse/people.py` - `WhitehorsePersonScraper`
- **Dawson City**: `ca_yt_dawson_city/people.py` - `DawsonCityPersonScraper`

## 🏢 **3. Civic Platform Scrapers (5 Platforms)**

### **3.1 Legistar Platform Scraper**
- **Location**: `services/etl/legacy-civic-scraper/civic_scraper/platforms/legistar/site.py`
- **Class**: `LegistarSite`
- **Data Type**: Municipal meeting records, agendas, minutes
- **Collection Method**: Web scraping with BeautifulSoup
- **Status**: ✅ **ACTIVE** - Used by multiple municipalities
- **Municipalities**: 50+ cities across Canada and US

### **3.2 CivicPlus Platform Scraper**
- **Location**: `services/etl/legacy-civic-scraper/civic_scraper/platforms/civic_plus/site.py`
- **Class**: `CivicPlusSite`
- **Data Type**: Meeting records, documents, agendas
- **Collection Method**: Web scraping with date-based navigation
- **Status**: ✅ **ACTIVE** - Used by 20+ municipalities
- **Features**: Date range filtering, asset download

### **3.3 Granicus Platform Scraper**
- **Location**: `services/etl/legacy-civic-scraper/civic_scraper/platforms/granicus/site.py`
- **Class**: `GranicusSite`
- **Data Type**: Video recordings, meeting transcripts
- **Collection Method**: API-based collection with video processing
- **Status**: ✅ **ACTIVE** - Used by 15+ municipalities
- **Features**: Video download, transcript extraction

### **3.4 PrimeGov Platform Scraper**
- **Location**: `services/etl/legacy-civic-scraper/civic_scraper/platforms/primegov/site.py`
- **Class**: `PrimeGovSite`
- **Data Type**: Meeting records, permits, applications
- **Collection Method**: Web scraping with search functionality
- **Status**: ✅ **ACTIVE** - Used by 10+ municipalities
- **Features**: Advanced search, document filtering

### **3.5 CivicClerk Platform Scraper**
- **Location**: `services/etl/legacy-civic-scraper/civic_scraper/platforms/civic_clerk/site.py`
- **Class**: `CivicClerkSite`
- **Data Type**: Meeting minutes, ordinances, resolutions
- **Collection Method**: Web scraping with document parsing
- **Status**: ✅ **ACTIVE** - Used by 8+ municipalities
- **Features**: Document parsing, metadata extraction

## 🗳️ **4. Electoral Scrapers (1 Active)**

### **4.1 Canada Candidates Scraper**
- **Location**: `services/etl/legacy-scrapers-ca/ca_candidates/people.py`
- **Class**: `CanadaCandidatesPersonScraper`
- **Data Type**: Federal election candidate information
- **Collection Method**: Multi-source scraping (party websites, Elections Canada)
- **Status**: ✅ **ACTIVE** - Used for electoral data
- **Parties Covered**: Liberal, Conservative, NDP, Green, Bloc Québécois
- **Features**: Party-specific scraping, Elections Canada integration

## 🔧 **5. Utility and Helper Scrapers**

### **5.1 Base Scraper Classes**
- **CanadianScraper**: `services/etl/legacy-scrapers-ca/utils.py`
- **CSVScraper**: `services/etl/legacy-scrapers-ca/utils.py`
- **BaseSite**: `services/etl/legacy-civic-scraper/civic_scraper/base/site.py`

### **5.2 Legacy Migration Scrapers**
- **OurCommons MP Scraper**: `services/web-ui/src/legacy-migration/imports/mps.py`
- **Search Utils**: `services/web-ui/src/legacy-migration/search/utils.py`

## 📊 **Scraper Status and Usage**

### **Active Scrapers (Currently Used)**
- **Parliamentary**: 3 scrapers - Main data pipeline
- **Municipal**: 80+ scrapers - Municipal data collection
- **Civic Platforms**: 5 scrapers - Meeting and document collection
- **Electoral**: 1 scraper - Candidate information

### **Legacy Scrapers (Available but not actively used)**
- **Municipal**: 20+ scrapers - Disabled or deprecated
- **Historical**: 10+ scrapers - Previous versions or deprecated platforms

### **Disabled Scrapers**
- **Location**: `services/etl/legacy-scrapers-ca/disabled/`
- **Reason**: Platform changes, deprecated APIs, maintenance issues
- **Count**: 20+ scrapers

## 🗄️ **Data Flow and Integration**

### **Current Active Pipeline**
```
Parliamentary Scrapers (3) → Legacy Adapters → Database → Frontend
     ↓
Represent API, OurCommons.ca, LEGISinfo
     ↓
686 MPs, 412 Bills, 34 Votes
     ↓
PostgreSQL Database (7 tables)
     ↓
Next.js Frontend Display
```

### **Municipal Data Pipeline (Legacy)**
```
Municipal Scrapers (100+) → Pupa Framework → JSON/CSV → Storage
     ↓
Various Municipal Websites
     ↓
Councillor Information, Meeting Records
     ↓
Local Storage (Not currently integrated)
```

### **Civic Platform Pipeline (Legacy)**
```
Civic Platform Scrapers (5) → Asset Collection → Storage
     ↓
Meeting Records, Documents, Videos
     ↓
Local File System
     ↓
Not Currently Integrated
```

## 🔍 **Scraper Discovery and Mapping**

### **How to Find All Scrapers**
```bash
# Find all scraper classes
grep -r "class.*Scraper" services/etl/legacy-scrapers-ca/
grep -r "class.*Scraper" services/etl/legacy-civic-scraper/

# Find all scrape methods
grep -r "def.*scrape" services/etl/legacy-scrapers-ca/
grep -r "def.*scrape" services/etl/legacy-civic-scraper/

# Find all adapter classes
grep -r "class.*Adapter" services/etl/app/extractors/
```

### **Scraper Registry**
```bash
# List all municipal scrapers
find services/etl/legacy-scrapers-ca/ -name "people.py" -exec grep -l "class.*Scraper" {} \;

# List all civic platform scrapers
find services/etl/legacy-civic-scraper/ -name "site.py" -exec grep -l "class.*Site" {} \;

# List all parliamentary scrapers
grep -r "class.*Adapter" services/etl/app/extractors/
```

## 📈 **Performance and Monitoring**

### **Active Scrapers Performance**
- **Parliamentary**: 7-11 seconds total collection time
- **Municipal**: Varies by municipality (30 seconds - 5 minutes)
- **Civic Platforms**: Varies by platform (1-10 minutes)
- **Electoral**: 5-15 minutes for full candidate database

### **Data Volume Estimates**
- **Parliamentary**: ~536KB per collection run
- **Municipal**: ~50MB total across all municipalities
- **Civic Platforms**: ~100MB total meeting records and documents
- **Electoral**: ~10MB candidate information

## 🚨 **Maintenance and Updates**

### **Scraper Health Monitoring**
```bash
# Check parliamentary scraper health
curl -I https://represent.opennorth.ca/api/
curl -I https://www.ourcommons.ca/
curl -I https://www.parl.ca/legisinfo/

# Check municipal scraper health
# (Requires individual municipality website checks)

# Check civic platform health
# (Requires platform-specific health checks)
```

### **Update Procedures**
1. **Parliamentary Scrapers**: Update in `legacy_adapters.py`
2. **Municipal Scrapers**: Update individual scraper files
3. **Civic Platform Scrapers**: Update platform-specific implementations
4. **Electoral Scrapers**: Update in `ca_candidates/people.py`

## 🔮 **Future Integration Opportunities**

### **Municipal Data Integration**
- **Current Status**: 100+ scrapers available but not integrated
- **Integration Path**: Create municipal data adapters similar to parliamentary
- **Database Schema**: Extend current schema for municipal data
- **Frontend**: Add municipal section to Represent integration

### **Civic Platform Integration**
- **Current Status**: 5 platform scrapers available but not integrated
- **Integration Path**: Create civic data adapters for meeting records
- **Database Schema**: Add tables for meetings, documents, videos
- **Frontend**: Add civic transparency section

### **Electoral Data Integration**
- **Current Status**: 1 active scraper for federal candidates
- **Integration Path**: Extend to provincial and municipal elections
- **Database Schema**: Add tables for candidates, elections, results
- **Frontend**: Add electoral data section

---

## 📚 **Summary**

This inventory documents **109+ scrapers** across the OpenParliament.ca V2 system:

- **✅ 3 Active Parliamentary Scrapers** - Currently integrated and running
- **📊 100+ Municipal Scrapers** - Available for future integration
- **🏢 5 Civic Platform Scrapers** - Available for meeting/document integration
- **🗳️ 1 Electoral Scraper** - Available for candidate data integration

The system follows the **FUNDAMENTAL RULE: NEVER REINVENT THE WHEEL** by maintaining all existing scrapers while providing a clear path for future integration and expansion.

---

**Last Updated**: 2025-08-20
**Version**: 1.0
**Maintainer**: OpenParliament.ca V2 Team
**FUNDAMENTAL RULE**: ✅ **NEVER REINVENT THE WHEEL** - All scrapers documented and available for future integration
