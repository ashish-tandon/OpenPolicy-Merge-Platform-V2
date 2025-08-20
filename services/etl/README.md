# ETL Service - OpenParliament.ca V2

**Following FUNDAMENTAL RULE: NEVER REINVENT THE WHEEL** 🚨

This ETL service adapts existing OpenParliament.ca legacy importers for modern use, rather than creating new implementations from scratch.

## What We're Doing

Instead of building new data collection tools, we're:

1. **Adapting existing legacy importers** from `legacy/openparliament/parliament/imports/`
2. **Modernizing the interfaces** to use async/await and modern Python patterns
3. **Preserving proven data collection logic** that's already tested and working
4. **Adding modern error handling and logging** while keeping the core logic intact

## Legacy Sources Adapted

- **MPs**: `legacy/openparliament/parliament/imports/mps.py`
  - OurCommons.ca scraper
  - Represent API integration
  
- **Bills**: `legacy/openparliament/parliament/imports/legisinfo.py`
  - LEGISinfo API integration
  - Bill status tracking
  
- **Votes**: `legacy/openparliament/parliament/imports/parlvotes.py`
  - OurCommons.ca XML vote data
  - Individual MP voting records

## Quick Start

```bash
# Install dependencies
make install

# Collect parliamentary data
make collect-data

# View help
make help
```

## Data Collection

The service collects:

- **Members of Parliament** (current and historical)
- **Bills and legislation** (status, text, sponsors)
- **Voting records** (all votes with individual MP ballots)
- **Committee information** (members, meetings, reports)

## Output

Data is saved to `data/legacy_adapted/` in JSON format with timestamps.

## Why This Approach?

1. **Proven reliability**: Legacy importers have been running for years
2. **Data quality**: Already handles edge cases and data validation
3. **Maintenance**: No need to maintain duplicate logic
4. **Speed**: Get comprehensive data collection working immediately

## Development

```bash
# Set up development environment
make setup

# Run with live reload
make dev

# Run tests
make test
```

## Architecture

```
Legacy OpenParliament Importers (Django-based)
                    ↓
            Legacy Adapters (Modern Python)
                    ↓
            Data Collection Tasks
                    ↓
            JSON Output Files
```

This approach ensures we get the best of both worlds: proven data collection logic with modern Python tooling.
