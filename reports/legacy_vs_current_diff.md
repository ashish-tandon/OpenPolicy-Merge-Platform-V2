# Legacy vs Current Feature Diff Report

Generated: 2025-08-23 (Enhanced)

## Summary

- **Total Legacy Features**: 191
- **Matched Features**: 0
- **Unmatched Features**: 139
- **Implementation Priority**: Provincial/Municipal Scrapers
- **Checklist Range**: CHK-0179 through CHK-0317

## Unmatched Legacy Features

| Feature | Type | File |
|---------|------|------|
| CanadianScraper | scraper | `services/etl/legacy-scrapers-ca/utils.py` |
| CSVScraper | scraper | `services/etl/legacy-scrapers-ca/utils.py` |
| FrederictonPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_nb_fredericton/people.py` |
| WinnipegPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_mb_winnipeg/people.py` |
| MonctonPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_nb_moncton/people.py` |
| AjaxPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_on_ajax/people.py` |
| NewWestminsterPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_bc_new_westminster/people.py` |
| CambridgePersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_on_cambridge/people.py` |
| LondonPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_on_london/people.py` |
| KawarthaLakesPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_on_kawartha_lakes/people.py` |
| SaintJohnPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_nb_saint_john/people.py` |
| CanadaPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca/people.py` |
| RichmondPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_bc_richmond/people.py` |
| KelownaPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_bc_kelowna/people.py` |
| HamiltonPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_on_hamilton/people.py` |
| TorontoPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_on_toronto/people.py` |
| SurreyPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_bc_surrey/people.py` |
| OntarioPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_on/people.py` |
| SaskatchewanPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_sk/people.py` |
| WaterlooPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_on_waterloo/people.py` |
| PrinceEdwardIslandPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_pe/people.py` |
| LambtonPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_on_lambton/people.py` |
| CaledonPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_on_caledon/people.py` |
| BurnabyPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_bc_burnaby/people.py` |
| PickeringPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_on_pickering/people.py` |
| StratfordPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_pe_stratford/people.py` |
| LavalPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_qc_laval/people.py` |
| HaldimandCountyPersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_on_haldimand_county/people.py` |
| OakvillePersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_on_oakville/people.py` |
| GrandePrairieCountyNo1PersonScraper | scraper | `services/etl/legacy-scrapers-ca/ca_ab_grande_prairie_county_no_1/people.py` |

... and 109 more unmatched features

## Implementation Gaps (Decimal Checklist Items)

| Checklist ID | Feature | Type | Priority | Action |
|--------------|---------|------|----------|---------|
| 2.1.1 | CanadianScraper | scraper | P2 | Implement scraper for CanadianScraper |
| 2.1.2 | CSVScraper | scraper | P2 | Implement scraper for CSVScraper |
| 2.1.3 | FrederictonPersonScraper | scraper | P2 | Implement scraper for FrederictonPersonScraper |
| 2.1.4 | WinnipegPersonScraper | scraper | P2 | Implement scraper for WinnipegPersonScraper |
| 2.1.5 | MonctonPersonScraper | scraper | P2 | Implement scraper for MonctonPersonScraper |
| 2.1.6 | AjaxPersonScraper | scraper | P2 | Implement scraper for AjaxPersonScraper |
| 2.1.7 | NewWestminsterPersonScraper | scraper | P2 | Implement scraper for NewWestminsterPersonScraper |
| 2.1.8 | CambridgePersonScraper | scraper | P2 | Implement scraper for CambridgePersonScraper |
| 2.1.9 | LondonPersonScraper | scraper | P2 | Implement scraper for LondonPersonScraper |
| 2.1.10 | KawarthaLakesPersonScraper | scraper | P2 | Implement scraper for KawarthaLakesPersonScraper |
| 2.1.11 | SaintJohnPersonScraper | scraper | P2 | Implement scraper for SaintJohnPersonScraper |
| 2.1.12 | CanadaPersonScraper | scraper | P2 | Implement scraper for CanadaPersonScraper |
| 2.1.13 | RichmondPersonScraper | scraper | P2 | Implement scraper for RichmondPersonScraper |
| 2.1.14 | KelownaPersonScraper | scraper | P2 | Implement scraper for KelownaPersonScraper |
| 2.1.15 | HamiltonPersonScraper | scraper | P2 | Implement scraper for HamiltonPersonScraper |
| 2.1.16 | TorontoPersonScraper | scraper | P2 | Implement scraper for TorontoPersonScraper |
| 2.1.17 | SurreyPersonScraper | scraper | P2 | Implement scraper for SurreyPersonScraper |
| 2.1.18 | OntarioPersonScraper | scraper | P2 | Implement scraper for OntarioPersonScraper |
| 2.1.19 | SaskatchewanPersonScraper | scraper | P2 | Implement scraper for SaskatchewanPersonScraper |
| 2.1.20 | WaterlooPersonScraper | scraper | P2 | Implement scraper for WaterlooPersonScraper |

... and 59 more gaps

## Enhanced Implementation Checklist Mapping

### Provincial Scrapers (CHK-0179.1 to CHK-0179.13)
- CHK-0179.1: Implement CanadianScraper base class migration
- CHK-0179.2: Implement Alberta provincial scraper
- CHK-0179.3: Implement British Columbia provincial scraper
- CHK-0179.4: Implement Manitoba provincial scraper
- CHK-0179.5: Implement New Brunswick provincial scraper
- CHK-0179.6: Implement Newfoundland and Labrador provincial scraper
- CHK-0179.7: Implement Northwest Territories scraper
- CHK-0179.8: Implement Nova Scotia provincial scraper
- CHK-0179.9: Implement Nunavut scraper
- CHK-0179.10: Implement Ontario provincial scraper
- CHK-0179.11: Implement Prince Edward Island scraper
- CHK-0179.12: Implement Quebec provincial scraper
- CHK-0179.13: Implement Saskatchewan provincial scraper

### Municipal Scrapers by Province

#### Alberta Municipalities (CHK-0180.1 to CHK-0180.6)
- CHK-0180.1: Calgary scraper implementation
- CHK-0180.2: Edmonton scraper implementation
- CHK-0180.3: Grande Prairie scraper implementation
- CHK-0180.4: Lethbridge scraper implementation
- CHK-0180.5: Strathcona County scraper implementation
- CHK-0180.6: Wood Buffalo scraper implementation

#### British Columbia Municipalities (CHK-0181.1 to CHK-0181.12)
- CHK-0181.1: Abbotsford scraper implementation
- CHK-0181.2: Burnaby scraper implementation
- CHK-0181.3: Coquitlam scraper implementation
- CHK-0181.4: Kelowna scraper implementation
- CHK-0181.5: Langley scraper implementation
- CHK-0181.6: Langley City scraper implementation
- CHK-0181.7: New Westminster scraper implementation
- CHK-0181.8: Richmond scraper implementation
- CHK-0181.9: Saanich scraper implementation
- CHK-0181.10: Surrey scraper implementation
- CHK-0181.11: Vancouver scraper implementation
- CHK-0181.12: Victoria scraper implementation

#### Ontario Municipalities (CHK-0182.1 to CHK-0182.40)
Major cities requiring individual implementation:
- CHK-0182.1: Toronto scraper implementation
- CHK-0182.2: Ottawa scraper implementation
- CHK-0182.3: Mississauga scraper implementation
- CHK-0182.4: Hamilton scraper implementation
- CHK-0182.5: London scraper implementation
- CHK-0182.6: Waterloo scraper implementation
- CHK-0182.7: Kitchener scraper implementation
- CHK-0182.8: Windsor scraper implementation
- CHK-0182.9: Markham scraper implementation
- CHK-0182.10: Vaughan scraper implementation
(... and 30 more Ontario municipalities)

### Scraper Framework Components (CHK-0183.1 to CHK-0183.10)
- CHK-0183.1: Base scraper class with retry logic
- CHK-0183.2: CSV data parser implementation
- CHK-0183.3: Person data normalizer
- CHK-0183.4: Contact info extractor
- CHK-0183.5: Photo downloader with caching
- CHK-0183.6: Social media link resolver
- CHK-0183.7: Duplicate detection system
- CHK-0183.8: Data validation framework
- CHK-0183.9: Scraper scheduling system
- CHK-0183.10: Error reporting and monitoring

## Migration Strategy

1. **Phase 1**: Framework Components (CHK-0183.*)
   - Build reusable base classes
   - Implement common utilities
   - Set up testing framework

2. **Phase 2**: Provincial Scrapers (CHK-0179.*)
   - Start with provinces that have APIs
   - Implement data normalization

3. **Phase 3**: Major Cities (CHK-0180-0182 subsets)
   - Toronto, Vancouver, Montreal first
   - Cities with >500k population

4. **Phase 4**: Remaining Municipalities
   - Batch by similar website structures
   - Use template patterns

## Technical Debt Addressed
- Consolidate 139 individual scrapers into ~50 configurable scrapers
- Implement proper error handling and retry logic
- Add comprehensive logging and monitoring
- Create unified data model for all jurisdictions
