#!/usr/bin/env python3
"""
Data Journey Mapping Tool
Maps data points through the entire journey: ingest→transform→store→expose→UI→analytics
"""

import json
import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict
import argparse
from datetime import datetime


class DataJourneyMapper:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.data_points = defaultdict(dict)
        self.journeys = []
        self.lineage_data = {}
        self.var_func_map = {}
        
    def load_existing_reports(self):
        """Load existing lineage and mapping reports"""
        # Load lineage data
        lineage_files = [
            self.root_path / "docs/plan/lineage/DATA_LINEAGE_AUTO.json",
            self.root_path / "reports/DATA_LINEAGE.json"
        ]
        
        for lineage_file in lineage_files:
            if lineage_file.exists():
                print(f"Loading lineage data from {lineage_file}")
                with open(lineage_file, 'r') as f:
                    self.lineage_data = json.load(f)
                break
        
        # Load variable-function map
        var_func_file = self.root_path / "reports/VAR_FUNC_MAP.json"
        if var_func_file.exists():
            print(f"Loading variable-function map from {var_func_file}")
            with open(var_func_file, 'r') as f:
                self.var_func_map = json.load(f)
    
    def identify_data_points(self):
        """Identify key data points in the system"""
        data_points = {
            'bills': {
                'name': 'Parliamentary Bills',
                'type': 'legislative',
                'key_fields': ['bill_id', 'title', 'sponsor', 'status', 'text'],
                'sources': ['parliament_api', 'scraper'],
                'transformations': ['parse_xml', 'extract_metadata', 'normalize_text'],
                'storage': ['bills_bill', 'bills_billtext'],
                'api_endpoints': ['/api/v1/bills/', '/api/v1/bills/{id}'],
                'ui_components': ['BillsList', 'BillDetail', 'BillStatusTracker']
            },
            'members': {
                'name': 'Members of Parliament',
                'type': 'person',
                'key_fields': ['member_id', 'name', 'party', 'constituency', 'email'],
                'sources': ['parliament_api', 'scraper'],
                'transformations': ['normalize_names', 'link_constituencies'],
                'storage': ['core_electedmember', 'core_membership'],
                'api_endpoints': ['/api/v1/members/', '/api/v1/members/{id}'],
                'ui_components': ['MPList', 'MPProfile', 'MPVotingRecord']
            },
            'votes': {
                'name': 'Parliamentary Votes',
                'type': 'voting',
                'key_fields': ['vote_id', 'bill_id', 'member_id', 'vote_type', 'date'],
                'sources': ['parliament_api'],
                'transformations': ['aggregate_votes', 'calculate_results'],
                'storage': ['votes_vote', 'votes_ballotentry'],
                'api_endpoints': ['/api/v1/votes/', '/api/v1/voting-records/'],
                'ui_components': ['VotingRecordsList', 'BillVotes', 'MPVotes']
            },
            'committees': {
                'name': 'Parliamentary Committees',
                'type': 'organization',
                'key_fields': ['committee_id', 'name', 'type', 'members'],
                'sources': ['parliament_api', 'scraper'],
                'transformations': ['parse_membership', 'link_members'],
                'storage': ['committees_committee', 'committees_membership'],
                'api_endpoints': ['/api/v1/committees/', '/api/v1/committees/{id}'],
                'ui_components': ['CommitteesList', 'CommitteeMembers', 'CommitteeReports']
            },
            'debates': {
                'name': 'Parliamentary Debates',
                'type': 'transcript',
                'key_fields': ['debate_id', 'date', 'topic', 'speakers', 'transcript'],
                'sources': ['hansard_api', 'scraper'],
                'transformations': ['parse_transcript', 'extract_speakers', 'segment_speeches'],
                'storage': ['debates_debate', 'debates_statement'],
                'api_endpoints': ['/api/v1/debates/', '/api/v1/debates/{date}/{number}'],
                'ui_components': ['DebatesList', 'DebateTranscript', 'MPSpeeches']
            },
            'constituencies': {
                'name': 'Electoral Constituencies',
                'type': 'geographic',
                'key_fields': ['constituency_id', 'name', 'province', 'boundaries'],
                'sources': ['elections_api', 'boundary_files'],
                'transformations': ['parse_boundaries', 'geocode'],
                'storage': ['core_constituency', 'core_boundary'],
                'api_endpoints': ['/api/v1/constituencies/', '/api/v1/represent/'],
                'ui_components': ['ConstituencyMap', 'RepresentativeFinder']
            }
        }
        
        return data_points
    
    def trace_ingestion_paths(self, data_point: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Trace how data is ingested"""
        ingestion_paths = []
        
        # Search for ETL scripts
        etl_patterns = [
            f"**/ingest*{data_point}*.py",
            f"**/{data_point}*loader*.py",
            f"**/{data_point}*scraper*.py",
            "**/etl/**/*.py"
        ]
        
        for pattern in etl_patterns:
            for file_path in self.root_path.glob(pattern):
                if not any(skip in str(file_path) for skip in ['node_modules', 'venv', '__pycache__']):
                    # Analyze the file
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                    # Look for data sources
                    source_patterns = [
                        r'url\s*=\s*["\']([^"\']+)["\']',
                        r'endpoint\s*=\s*["\']([^"\']+)["\']',
                        r'API_URL\s*=\s*["\']([^"\']+)["\']',
                        r'requests\.(get|post)\(["\']([^"\']+)["\']'
                    ]
                    
                    sources = []
                    for pattern in source_patterns:
                        matches = re.findall(pattern, content)
                        sources.extend([m[1] if isinstance(m, tuple) else m for m in matches])
                    
                    # Look for data processing
                    processing_patterns = [
                        r'def\s+(parse|extract|transform|process)_(\w+)',
                        r'(\w+)\.transform\(',
                        r'(\w+)\.parse\('
                    ]
                    
                    processors = []
                    for pattern in processing_patterns:
                        matches = re.findall(pattern, content)
                        processors.extend(matches)
                    
                    if sources or processors:
                        ingestion_paths.append({
                            'file': str(file_path.relative_to(self.root_path)),
                            'type': 'etl_script',
                            'sources': sources[:5],  # Limit to 5
                            'processors': processors[:5],
                            'data_point': data_point
                        })
        
        # Check for scrapers in legacy directory
        legacy_scrapers = self.root_path / "services/etl/legacy-scrapers-ca"
        if legacy_scrapers.exists():
            for scraper_dir in legacy_scrapers.glob("ca_*"):
                if scraper_dir.is_dir():
                    people_file = scraper_dir / "people.py"
                    if people_file.exists() and 'member' in data_point.lower():
                        ingestion_paths.append({
                            'file': str(people_file.relative_to(self.root_path)),
                            'type': 'legacy_scraper',
                            'jurisdiction': scraper_dir.name,
                            'data_point': 'members'
                        })
        
        return ingestion_paths
    
    def trace_transformations(self, data_point: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Trace data transformations"""
        transformations = []
        
        # Look for transformation functions
        for transform_name in config.get('transformations', []):
            # Search in codebase
            if self.var_func_map and 'nodes' in self.var_func_map:
                for node in self.var_func_map['nodes']:
                    if (node.get('type') == 'function' and 
                        transform_name.lower() in node.get('name', '').lower()):
                        transformations.append({
                            'function': node['name'],
                            'file': node.get('file', 'unknown'),
                            'type': 'transform_function',
                            'data_point': data_point
                        })
        
        # Search for data models and serializers
        model_patterns = [
            f"**/models/{data_point}*.py",
            f"**/models.py",
            f"**/schemas/{data_point}*.py",
            f"**/serializers.py"
        ]
        
        for pattern in model_patterns:
            for file_path in self.root_path.glob(pattern):
                if not any(skip in str(file_path) for skip in ['node_modules', 'venv']):
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Look for field definitions
                    field_pattern = r'(\w+)\s*=\s*(?:models\.|fields\.|Field)'
                    fields = re.findall(field_pattern, content)
                    
                    if fields:
                        transformations.append({
                            'file': str(file_path.relative_to(self.root_path)),
                            'type': 'data_model',
                            'fields': fields[:10],  # Limit to 10
                            'data_point': data_point
                        })
        
        return transformations
    
    def trace_storage(self, data_point: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Trace data storage locations"""
        storage_locations = []
        
        # From config
        for table_name in config.get('storage', []):
            storage_locations.append({
                'type': 'database_table',
                'table': table_name,
                'data_point': data_point
            })
        
        # Look for migrations
        migration_patterns = [
            "**/migrations/*_" + data_point + "*.py"
        ] + [
            "**/migrations/*_create_" + table + "*.py" 
            for table in config.get('storage', [])
        ]
        
        for pattern in migration_patterns:
            if isinstance(pattern, list):
                continue
            for file_path in self.root_path.glob(pattern):
                storage_locations.append({
                    'type': 'migration',
                    'file': str(file_path.relative_to(self.root_path)),
                    'data_point': data_point
                })
        
        # Check for cache implementations
        cache_patterns = [
            f"**/*cache*{data_point}*.py",
            f"**/{data_point}*cache*.py"
        ]
        
        for pattern in cache_patterns:
            for file_path in self.root_path.glob(pattern):
                if not any(skip in str(file_path) for skip in ['node_modules', 'venv']):
                    storage_locations.append({
                        'type': 'cache',
                        'file': str(file_path.relative_to(self.root_path)),
                        'data_point': data_point
                    })
        
        return storage_locations
    
    def trace_api_exposure(self, data_point: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Trace API endpoints"""
        api_exposures = []
        
        # From config
        for endpoint in config.get('api_endpoints', []):
            api_exposures.append({
                'type': 'configured_endpoint',
                'endpoint': endpoint,
                'method': 'GET',  # Default assumption
                'data_point': data_point
            })
        
        # Search for route definitions
        route_patterns = [
            r'@(?:app|router)\.(?:get|post|put|delete)\(["\']([^"\']+)["\']',
            r'path\(["\']([^"\']+)["\']',
            r'Route\(["\']([^"\']+)["\']'
        ]
        
        api_files = list(self.root_path.glob("**/api/**/*.py")) + \
                   list(self.root_path.glob("**/routers/**/*.py")) + \
                   list(self.root_path.glob("**/routes/**/*.py"))
        
        for file_path in api_files:
            if not any(skip in str(file_path) for skip in ['node_modules', 'venv']):
                with open(file_path, 'r') as f:
                    content = f.read()
                
                for pattern in route_patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        if data_point in match.lower():
                            api_exposures.append({
                                'type': 'route_definition',
                                'endpoint': match,
                                'file': str(file_path.relative_to(self.root_path)),
                                'data_point': data_point
                            })
        
        return api_exposures
    
    def trace_ui_usage(self, data_point: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Trace UI component usage"""
        ui_usage = []
        
        # From config
        for component in config.get('ui_components', []):
            # Search for component files
            component_patterns = [
                f"**/{component}.tsx",
                f"**/{component}.jsx",
                f"**/{component}.ts",
                f"**/{component}.js"
            ]
            
            for pattern in component_patterns:
                for file_path in self.root_path.glob(pattern):
                    if not any(skip in str(file_path) for skip in ['node_modules', 'dist']):
                        ui_usage.append({
                            'type': 'component_definition',
                            'component': component,
                            'file': str(file_path.relative_to(self.root_path)),
                            'data_point': data_point
                        })
        
        # Search for API calls in UI
        ui_files = list(self.root_path.glob("**/src/**/*.tsx")) + \
                   list(self.root_path.glob("**/src/**/*.jsx"))
        
        api_call_patterns = [
            r'fetch\(["\']([^"\']+' + data_point + '[^"\']+)["\']',
            r'axios\.(?:get|post)\(["\']([^"\']+' + data_point + '[^"\']+)["\']',
            r'api\.(' + data_point + r'\w*)\('
        ]
        
        for file_path in ui_files[:50]:  # Limit to 50 files for performance
            if not any(skip in str(file_path) for skip in ['node_modules', 'dist']):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    for pattern in api_call_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            ui_usage.append({
                                'type': 'api_call',
                                'calls': matches[:3],  # Limit to 3
                                'file': str(file_path.relative_to(self.root_path)),
                                'data_point': data_point
                            })
                except:
                    pass
        
        return ui_usage
    
    def trace_analytics(self, data_point: str) -> List[Dict[str, Any]]:
        """Trace analytics and reporting usage"""
        analytics = []
        
        # Search for analytics/reporting files
        analytics_patterns = [
            f"**/analytics/**/*{data_point}*.py",
            f"**/reports/**/*{data_point}*.py",
            f"**/stats/**/*{data_point}*.py"
        ]
        
        for pattern in analytics_patterns:
            for file_path in self.root_path.glob(pattern):
                analytics.append({
                    'type': 'analytics_script',
                    'file': str(file_path.relative_to(self.root_path)),
                    'data_point': data_point
                })
        
        # Search for dashboard components
        dashboard_patterns = [
            "**/dashboard/**/*.tsx",
            "**/analytics/**/*.tsx",
            "**/stats/**/*.tsx"
        ]
        
        for pattern in dashboard_patterns:
            for file_path in self.root_path.glob(pattern):
                if not any(skip in str(file_path) for skip in ['node_modules']):
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        
                        if data_point in content.lower():
                            analytics.append({
                                'type': 'dashboard_component',
                                'file': str(file_path.relative_to(self.root_path)),
                                'data_point': data_point
                            })
                    except:
                        pass
        
        return analytics
    
    def build_journey(self, data_point: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Build complete journey for a data point"""
        journey = {
            'data_point': data_point,
            'name': config['name'],
            'type': config['type'],
            'key_fields': config['key_fields'],
            'stages': {
                'ingestion': self.trace_ingestion_paths(data_point, config),
                'transformation': self.trace_transformations(data_point, config),
                'storage': self.trace_storage(data_point, config),
                'api_exposure': self.trace_api_exposure(data_point, config),
                'ui_usage': self.trace_ui_usage(data_point, config),
                'analytics': self.trace_analytics(data_point)
            }
        }
        
        # Calculate completeness
        completeness = {
            'ingestion': len(journey['stages']['ingestion']) > 0,
            'transformation': len(journey['stages']['transformation']) > 0,
            'storage': len(journey['stages']['storage']) > 0,
            'api_exposure': len(journey['stages']['api_exposure']) > 0,
            'ui_usage': len(journey['stages']['ui_usage']) > 0,
            'analytics': len(journey['stages']['analytics']) > 0
        }
        
        journey['completeness'] = completeness
        journey['completeness_score'] = sum(completeness.values()) / len(completeness) * 100
        
        return journey
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive data journey report"""
        # Load existing reports
        self.load_existing_reports()
        
        # Identify data points
        data_points = self.identify_data_points()
        
        # Build journeys
        journeys = []
        for data_point, config in data_points.items():
            print(f"Mapping journey for {data_point}...")
            journey = self.build_journey(data_point, config)
            journeys.append(journey)
        
        # Compare with lineage data
        lineage_comparison = {}
        if self.lineage_data:
            # Compare discovered paths with documented lineage
            pass
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'data_points': list(data_points.keys()),
            'journeys': journeys,
            'summary': {
                'total_data_points': len(data_points),
                'complete_journeys': len([j for j in journeys if j['completeness_score'] == 100]),
                'average_completeness': sum(j['completeness_score'] for j in journeys) / len(journeys) if journeys else 0,
                'missing_stages': defaultdict(int)
            },
            'lineage_comparison': lineage_comparison
        }
        
        # Calculate missing stages
        for journey in journeys:
            for stage, complete in journey['completeness'].items():
                if not complete:
                    report['summary']['missing_stages'][stage] += 1
        
        report['summary']['missing_stages'] = dict(report['summary']['missing_stages'])
        
        return report
    
    def export_markdown(self, report: Dict[str, Any], output_path: str):
        """Export report as markdown"""
        with open(output_path, 'w') as f:
            f.write("# Data Journey Map\n\n")
            f.write(f"Generated: {report['generated_at']}\n\n")
            
            f.write("## Summary\n\n")
            summary = report['summary']
            f.write(f"- **Total Data Points**: {summary['total_data_points']}\n")
            f.write(f"- **Complete Journeys**: {summary['complete_journeys']}\n")
            f.write(f"- **Average Completeness**: {summary['average_completeness']:.1f}%\n\n")
            
            if summary['missing_stages']:
                f.write("### Missing Stages\n\n")
                for stage, count in summary['missing_stages'].items():
                    f.write(f"- {stage}: {count} data points missing this stage\n")
                f.write("\n")
            
            f.write("## Data Point Journeys\n\n")
            
            for journey in sorted(report['journeys'], key=lambda x: x['completeness_score'], reverse=True):
                f.write(f"### {journey['name']} ({journey['data_point']})\n\n")
                f.write(f"**Type**: {journey['type']} | ")
                f.write(f"**Completeness**: {journey['completeness_score']:.0f}%\n\n")
                f.write(f"**Key Fields**: {', '.join(journey['key_fields'])}\n\n")
                
                # Journey stages
                f.write("#### Journey Stages\n\n")
                
                # Ingestion
                f.write("##### 1. Ingestion\n")
                if journey['stages']['ingestion']:
                    for ing in journey['stages']['ingestion'][:3]:
                        f.write(f"- **{ing['type']}**: `{ing['file']}`\n")
                        if 'sources' in ing and ing['sources']:
                            f.write(f"  - Sources: {', '.join(ing['sources'][:3])}\n")
                else:
                    f.write("- ❌ No ingestion paths found\n")
                f.write("\n")
                
                # Transformation
                f.write("##### 2. Transformation\n")
                if journey['stages']['transformation']:
                    for trans in journey['stages']['transformation'][:3]:
                        f.write(f"- **{trans['type']}**: `{trans['file']}`\n")
                        if 'fields' in trans:
                            f.write(f"  - Fields: {', '.join(trans['fields'][:5])}\n")
                else:
                    f.write("- ❌ No transformations found\n")
                f.write("\n")
                
                # Storage
                f.write("##### 3. Storage\n")
                if journey['stages']['storage']:
                    for store in journey['stages']['storage'][:3]:
                        f.write(f"- **{store['type']}**: ")
                        if 'table' in store:
                            f.write(f"`{store['table']}`\n")
                        else:
                            f.write(f"`{store['file']}`\n")
                else:
                    f.write("- ❌ No storage locations found\n")
                f.write("\n")
                
                # API Exposure
                f.write("##### 4. API Exposure\n")
                if journey['stages']['api_exposure']:
                    for api in journey['stages']['api_exposure'][:3]:
                        f.write(f"- **{api['type']}**: `{api['endpoint']}`")
                        if 'file' in api:
                            f.write(f" (`{api['file']}`)")
                        f.write("\n")
                else:
                    f.write("- ❌ No API endpoints found\n")
                f.write("\n")
                
                # UI Usage
                f.write("##### 5. UI Usage\n")
                if journey['stages']['ui_usage']:
                    for ui in journey['stages']['ui_usage'][:3]:
                        f.write(f"- **{ui['type']}**: ")
                        if 'component' in ui:
                            f.write(f"{ui['component']} ")
                        f.write(f"(`{ui['file']}`)\n")
                        if 'calls' in ui:
                            f.write(f"  - API calls: {', '.join(ui['calls'][:2])}\n")
                else:
                    f.write("- ❌ No UI usage found\n")
                f.write("\n")
                
                # Analytics
                f.write("##### 6. Analytics\n")
                if journey['stages']['analytics']:
                    for ana in journey['stages']['analytics'][:3]:
                        f.write(f"- **{ana['type']}**: `{ana['file']}`\n")
                else:
                    f.write("- ❌ No analytics found\n")
                f.write("\n---\n\n")
            
            f.write("## Recommendations\n\n")
            f.write("Based on the data journey analysis:\n\n")
            
            incomplete = [j for j in report['journeys'] if j['completeness_score'] < 100]
            if incomplete:
                f.write("### Incomplete Journeys\n\n")
                for journey in incomplete:
                    missing = [stage for stage, complete in journey['completeness'].items() if not complete]
                    if missing:
                        f.write(f"- **{journey['name']}**: Missing {', '.join(missing)}\n")
                f.write("\n")
            
            f.write("### Data Flow Improvements\n\n")
            f.write("1. **Standardize ingestion patterns** - Use consistent ETL framework\n")
            f.write("2. **Document transformations** - Add inline documentation for data processing\n")
            f.write("3. **Centralize API definitions** - Use OpenAPI specifications\n")
            f.write("4. **Component mapping** - Maintain data-to-component mapping\n")
            f.write("5. **Analytics integration** - Add analytics hooks to key data flows\n")


def main():
    parser = argparse.ArgumentParser(description="Map data journeys through the system")
    parser.add_argument("--root", default=".", help="Root directory")
    parser.add_argument("--output-dir", default="reports", help="Output directory")
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Run mapping
    mapper = DataJourneyMapper(args.root)
    report = mapper.generate_report()
    
    # Export
    json_path = output_dir / "DATA_JOURNEY_MAP.json"
    md_path = output_dir / "DATA_JOURNEY_MAP.md"
    
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    mapper.export_markdown(report, str(md_path))
    
    print(f"\nData Journey Mapping Complete:")
    print(f"  Total data points: {report['summary']['total_data_points']}")
    print(f"  Complete journeys: {report['summary']['complete_journeys']}")
    print(f"  Average completeness: {report['summary']['average_completeness']:.1f}%")
    print(f"  Reports saved to:")
    print(f"    - {json_path}")
    print(f"    - {md_path}")


if __name__ == "__main__":
    main()