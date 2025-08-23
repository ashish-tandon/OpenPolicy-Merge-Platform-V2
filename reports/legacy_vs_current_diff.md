# Legacy vs Current Feature Diff Report

Generated: 2025-08-23T17:54:10.803369

## Summary

- **Total Legacy Features**: 191
- **Matched Features**: 0
- **Unmatched Features**: 139

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
