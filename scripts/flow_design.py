#!/usr/bin/env python3
"""
Flow Design & Feature Inventory Tool
Enumerates features from origin repositories and builds flow design
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


class FlowDesigner:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.features = defaultdict(dict)
        self.flows = defaultdict(list)
        self.existing_mapping = {}
        self.var_func_map = {}
        
    def load_existing_data(self):
        """Load existing feature mapping and var-func map"""
        # Load feature mapping
        feature_map_path = self.root_path / "docs/plan/features/FEATURE_MAPPING_UNIFIED.md"
        if feature_map_path.exists():
            print(f"Loading feature mapping from {feature_map_path}")
            with open(feature_map_path, 'r') as f:
                content = f.read()
                
            # Parse features
            current_feature = None
            for line in content.split('\n'):
                if line.startswith('## Feature:'):
                    feature_name = line.replace('## Feature:', '').strip()
                    current_feature = feature_name
                    self.existing_mapping[current_feature] = {'lines': []}
                elif line.startswith('- ID:') and current_feature:
                    feature_id = line.replace('- ID:', '').strip()
                    self.existing_mapping[current_feature]['id'] = feature_id
                elif current_feature:
                    self.existing_mapping[current_feature]['lines'].append(line)
        
        # Load var-func map
        var_func_path = self.root_path / "reports/VAR_FUNC_MAP.json"
        if var_func_path.exists():
            print(f"Loading var-func map from {var_func_path}")
            with open(var_func_path, 'r') as f:
                self.var_func_map = json.load(f)
    
    def scan_legacy_features(self) -> Dict[str, Any]:
        """Scan legacy directories for features"""
        legacy_features = defaultdict(list)
        
        # Legacy patterns to look for
        legacy_dirs = [
            "legacy",
            "services/etl/legacy-scrapers-ca",
            "services/etl/legacy-civic-scraper"
        ]
        
        feature_patterns = {
            'scraper': r'class\s+(\w+Scraper)',
            'loader': r'class\s+(\w+Loader)',
            'parser': r'class\s+(\w+Parser)',
            'ingester': r'class\s+(\w+Ingester)',
            'api': r'@(?:app|router)\.(?:get|post|put|delete)\(["\']([^"\']+)["\']',
            'model': r'class\s+(\w+)\(.*Model.*\):',
            'view': r'class\s+(\w+View)',
            'component': r'(?:class|function|const)\s+(\w+)(?:Component|Page|Form|List|Detail)'
        }
        
        for legacy_dir in legacy_dirs:
            dir_path = self.root_path / legacy_dir
            if dir_path.exists():
                print(f"Scanning {legacy_dir} for features...")
                
                # Scan Python files
                for py_file in dir_path.rglob("*.py"):
                    if '__pycache__' in str(py_file):
                        continue
                        
                    try:
                        with open(py_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Extract features based on patterns
                        for feature_type, pattern in feature_patterns.items():
                            matches = re.findall(pattern, content)
                            for match in matches:
                                feature_info = {
                                    'name': match,
                                    'type': feature_type,
                                    'file': str(py_file.relative_to(self.root_path)),
                                    'legacy': True
                                }
                                legacy_features[feature_type].append(feature_info)
                                
                        # Look for specific feature indicators
                        if 'bill' in content.lower():
                            legacy_features['bills'].append({
                                'file': str(py_file.relative_to(self.root_path)),
                                'type': 'bill_related'
                            })
                        if 'member' in content.lower() or 'politician' in content.lower():
                            legacy_features['members'].append({
                                'file': str(py_file.relative_to(self.root_path)),
                                'type': 'member_related'
                            })
                        if 'vote' in content.lower() or 'ballot' in content.lower():
                            legacy_features['votes'].append({
                                'file': str(py_file.relative_to(self.root_path)),
                                'type': 'vote_related'
                            })
                            
                    except Exception as e:
                        print(f"Error reading {py_file}: {e}")
        
        return dict(legacy_features)
    
    def extract_state_transitions(self) -> Dict[str, List[Dict[str, Any]]]:
        """Extract state transitions from code"""
        transitions = defaultdict(list)
        
        # Search for state machine patterns
        state_patterns = [
            r'STATUS_CHOICES\s*=\s*[\[\(]([^\]\)]+)[\]\)]',
            r'STATES\s*=\s*\{([^}]+)\}',
            r'transitions\s*=\s*\{([^}]+)\}',
            r'workflow\s*=\s*\{([^}]+)\}'
        ]
        
        # Search in models and schemas
        for pattern_path in ["**/models/**/*.py", "**/schemas/**/*.py"]:
            for file_path in self.root_path.glob(pattern_path):
                if 'venv' in str(file_path) or 'node_modules' in str(file_path):
                    continue
                    
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    for pattern in state_patterns:
                        matches = re.findall(pattern, content, re.DOTALL)
                        if matches:
                            transitions[str(file_path.stem)].append({
                                'file': str(file_path.relative_to(self.root_path)),
                                'states': matches[0],
                                'type': 'state_definition'
                            })
                    
                    # Look for specific state transitions
                    transition_methods = re.findall(r'def\s+(transition_to_\w+|change_status_to_\w+|set_\w+_status)', content)
                    if transition_methods:
                        transitions[str(file_path.stem)].append({
                            'file': str(file_path.relative_to(self.root_path)),
                            'methods': transition_methods,
                            'type': 'transition_methods'
                        })
                        
                except Exception as e:
                    pass
        
        return dict(transitions)
    
    def build_routing_tables(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build routing tables from API definitions"""
        routing_tables = defaultdict(list)
        
        # Find API route files
        api_patterns = [
            "**/api/**/*.py",
            "**/routers/**/*.py",
            "**/routes/**/*.py",
            "**/urls.py"
        ]
        
        for pattern in api_patterns:
            for file_path in self.root_path.glob(pattern):
                if 'venv' in str(file_path) or 'node_modules' in str(file_path):
                    continue
                    
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Extract routes
                    route_patterns = [
                        # FastAPI/Flask style
                        r'@(?:app|router|api)\.(?P<method>get|post|put|patch|delete)\(["\'](?P<path>[^"\']+)["\'].*?\)\s*(?:async\s+)?def\s+(?P<handler>\w+)',
                        # Django style
                        r'path\(["\'](?P<path>[^"\']+)["\'],\s*(?P<handler>\w+)',
                        # Express style (JS/TS)
                        r'router\.(?P<method>get|post|put|patch|delete)\(["\'](?P<path>[^"\']+)["\']'
                    ]
                    
                    for pattern in route_patterns:
                        for match in re.finditer(pattern, content):
                            route_info = {
                                'method': match.group('method') if 'method' in match.groupdict() else 'GET',
                                'path': match.group('path'),
                                'handler': match.group('handler') if 'handler' in match.groupdict() else 'unknown',
                                'file': str(file_path.relative_to(self.root_path))
                            }
                            
                            # Categorize by feature
                            path = match.group('path').lower()
                            if 'bill' in path:
                                routing_tables['bills'].append(route_info)
                            elif 'member' in path or 'mp' in path:
                                routing_tables['members'].append(route_info)
                            elif 'vote' in path or 'voting' in path:
                                routing_tables['votes'].append(route_info)
                            elif 'committee' in path:
                                routing_tables['committees'].append(route_info)
                            elif 'debate' in path:
                                routing_tables['debates'].append(route_info)
                            else:
                                routing_tables['general'].append(route_info)
                                
                except Exception as e:
                    pass
        
        return dict(routing_tables)
    
    def map_feature_dependencies(self, feature_name: str) -> Dict[str, Any]:
        """Map dependencies for a feature using var-func map"""
        dependencies = {
            'modules': set(),
            'functions': set(),
            'imports': set(),
            'database_tables': set()
        }
        
        if self.var_func_map and 'nodes' in self.var_func_map:
            # Find nodes related to the feature
            feature_keywords = feature_name.lower().split()
            
            for node in self.var_func_map['nodes']:
                node_name = node.get('name', '').lower()
                node_file = node.get('file', '').lower()
                
                if any(keyword in node_name or keyword in node_file for keyword in feature_keywords):
                    if node['type'] == 'module':
                        dependencies['modules'].add(node['file'])
                    elif node['type'] == 'function':
                        dependencies['functions'].add(f"{node['name']} ({node['file']})")
                    elif node['type'] == 'import':
                        dependencies['imports'].add(node['name'])
                    elif node['type'] == 'table':
                        dependencies['database_tables'].add(node['name'])
        
        # Convert sets to lists for JSON serialization
        return {k: list(v) for k, v in dependencies.items()}
    
    def build_feature_flow(self, feature_name: str, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build complete flow for a feature"""
        flow = {
            'feature': feature_name,
            'id': feature_data.get('id', f'F{len(self.features) + 1:03d}'),
            'states': [],
            'transitions': [],
            'inputs': [],
            'outputs': [],
            'routes': [],
            'dependencies': self.map_feature_dependencies(feature_name),
            'ui_components': [],
            'data_flow': []
        }
        
        # Add states and transitions
        state_data = self.extract_state_transitions()
        for entity, transitions in state_data.items():
            if feature_name.lower() in entity.lower():
                for trans in transitions:
                    if trans['type'] == 'state_definition':
                        flow['states'].append({
                            'entity': entity,
                            'states': trans['states'],
                            'source': trans['file']
                        })
                    elif trans['type'] == 'transition_methods':
                        flow['transitions'].extend(trans['methods'])
        
        # Add routes
        routing_data = self.build_routing_tables()
        for category, routes in routing_data.items():
            if category.lower() in feature_name.lower() or feature_name.lower() in category.lower():
                flow['routes'].extend(routes)
        
        # Determine inputs and outputs based on routes
        for route in flow['routes']:
            if route['method'] in ['GET']:
                flow['outputs'].append({
                    'endpoint': route['path'],
                    'method': route['method'],
                    'type': 'api_response'
                })
            elif route['method'] in ['POST', 'PUT', 'PATCH']:
                flow['inputs'].append({
                    'endpoint': route['path'],
                    'method': route['method'],
                    'type': 'api_request'
                })
        
        # Add UI components from existing mapping
        if feature_name in self.existing_mapping:
            for line in self.existing_mapping[feature_name].get('lines', []):
                if 'UI Views/Components:' in line:
                    components = line.replace('- UI Views/Components:', '').strip().split(', ')
                    flow['ui_components'] = components
        
        # Build data flow sequence
        flow['data_flow'] = [
            {'step': 1, 'action': 'User Interaction', 'component': 'UI Component'},
            {'step': 2, 'action': 'API Request', 'component': 'Frontend'},
            {'step': 3, 'action': 'Route Handler', 'component': 'API Gateway'},
            {'step': 4, 'action': 'Business Logic', 'component': 'Service Layer'},
            {'step': 5, 'action': 'Data Access', 'component': 'Database'},
            {'step': 6, 'action': 'Response Formation', 'component': 'Service Layer'},
            {'step': 7, 'action': 'API Response', 'component': 'API Gateway'},
            {'step': 8, 'action': 'UI Update', 'component': 'Frontend'}
        ]
        
        return flow
    
    def generate_legacy_vs_current_diff(self, legacy_features: Dict[str, Any]) -> Dict[str, Any]:
        """Generate diff between legacy features and current implementation"""
        diff_report = {
            'summary': {
                'total_legacy_features': 0,
                'matched_features': 0,
                'unmatched_features': 0,
                'new_features': 0
            },
            'matched': [],
            'unmatched': [],
            'gaps': []
        }
        
        # Count legacy features
        for category, features in legacy_features.items():
            diff_report['summary']['total_legacy_features'] += len(features)
        
        # Get current features from existing mapping
        current_features = set(self.existing_mapping.keys())
        
        # Match features
        legacy_feature_names = set()
        for category, features in legacy_features.items():
            for feature in features:
                if 'name' in feature:
                    legacy_feature_names.add(feature['name'])
                    
                    # Try to match with current features
                    matched = False
                    for current in current_features:
                        if (feature['name'].lower() in current.lower() or 
                            current.lower() in feature['name'].lower()):
                            diff_report['matched'].append({
                                'legacy': feature['name'],
                                'current': current,
                                'legacy_file': feature.get('file', 'unknown')
                            })
                            matched = True
                            diff_report['summary']['matched_features'] += 1
                            break
                    
                    if not matched:
                        diff_report['unmatched'].append({
                            'legacy': feature['name'],
                            'type': feature.get('type', 'unknown'),
                            'file': feature.get('file', 'unknown')
                        })
                        diff_report['summary']['unmatched_features'] += 1
        
        # Identify gaps and generate decimal checklist items
        checklist_counter = defaultdict(int)
        for unmatched in diff_report['unmatched']:
            feature_type = unmatched['type']
            base_checklist = {
                'scraper': '2.1',
                'loader': '2.2',
                'parser': '2.3',
                'ingester': '2.4',
                'api': '3.1',
                'model': '1.1',
                'view': '4.1',
                'component': '4.2'
            }.get(feature_type, '5.1')
            
            checklist_counter[base_checklist] += 1
            checklist_id = f"{base_checklist}.{checklist_counter[base_checklist]}"
            
            diff_report['gaps'].append({
                'feature': unmatched['legacy'],
                'type': feature_type,
                'checklist_id': checklist_id,
                'action': f"Implement {feature_type} for {unmatched['legacy']}",
                'priority': 'P2' if feature_type in ['scraper', 'loader'] else 'P3'
            })
        
        return diff_report
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive flow design report"""
        # Load existing data
        self.load_existing_data()
        
        # Scan legacy features
        print("Scanning legacy features...")
        legacy_features = self.scan_legacy_features()
        
        # Build flows for existing features
        print("Building feature flows...")
        flows = {}
        for feature_name, feature_data in self.existing_mapping.items():
            flows[feature_name] = self.build_feature_flow(feature_name, feature_data)
        
        # Extract state transitions and routing
        state_transitions = self.extract_state_transitions()
        routing_tables = self.build_routing_tables()
        
        # Generate legacy vs current diff
        print("Generating legacy vs current diff...")
        diff_report = self.generate_legacy_vs_current_diff(legacy_features)
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'features': {
                'existing': list(self.existing_mapping.keys()),
                'legacy': legacy_features,
                'total_existing': len(self.existing_mapping),
                'total_legacy': sum(len(features) for features in legacy_features.values())
            },
            'flows': flows,
            'state_transitions': state_transitions,
            'routing_tables': routing_tables,
            'diff_report': diff_report
        }
        
        return report
    
    def export_flow_design_markdown(self, report: Dict[str, Any], output_path: str):
        """Export flow design as markdown"""
        with open(output_path, 'w') as f:
            f.write("# Flow Design Document\n\n")
            f.write(f"Generated: {report['generated_at']}\n\n")
            f.write("## Table of Contents\n\n")
            f.write("1. [Feature Overview](#feature-overview)\n")
            f.write("2. [Feature Flows](#feature-flows)\n")
            f.write("3. [State Transitions](#state-transitions)\n")
            f.write("4. [Routing Tables](#routing-tables)\n")
            f.write("5. [Legacy Feature Mapping](#legacy-feature-mapping)\n\n")
            
            f.write("## Feature Overview\n\n")
            f.write(f"- **Existing Features**: {report['features']['total_existing']}\n")
            f.write(f"- **Legacy Features Found**: {report['features']['total_legacy']}\n\n")
            
            f.write("## Feature Flows\n\n")
            
            for feature_name, flow in report['flows'].items():
                f.write(f"### {feature_name}\n\n")
                f.write(f"**Feature ID**: {flow['id']}\n\n")
                
                # States
                if flow['states']:
                    f.write("#### States\n\n")
                    for state_info in flow['states']:
                        f.write(f"- **{state_info['entity']}**: {state_info['states'][:100]}...\n")
                        f.write(f"  - Source: `{state_info['source']}`\n")
                    f.write("\n")
                
                # Transitions
                if flow['transitions']:
                    f.write("#### State Transitions\n\n")
                    for transition in flow['transitions'][:5]:
                        f.write(f"- `{transition}`\n")
                    if len(flow['transitions']) > 5:
                        f.write(f"- ... and {len(flow['transitions']) - 5} more\n")
                    f.write("\n")
                
                # Routes
                if flow['routes']:
                    f.write("#### API Routes\n\n")
                    f.write("| Method | Path | Handler | File |\n")
                    f.write("|--------|------|---------|------|\n")
                    for route in flow['routes'][:5]:
                        f.write(f"| {route['method']} | {route['path']} | {route['handler']} | `{route['file']}` |\n")
                    if len(flow['routes']) > 5:
                        f.write(f"\n... and {len(flow['routes']) - 5} more routes\n")
                    f.write("\n")
                
                # Data Flow
                f.write("#### Data Flow Sequence\n\n")
                f.write("```mermaid\nsequenceDiagram\n")
                for step in flow['data_flow']:
                    if step['step'] < len(flow['data_flow']):
                        next_step = flow['data_flow'][step['step']]
                        f.write(f"    {step['component']}->>+{next_step['component']}: {step['action']}\n")
                f.write("```\n\n")
                
                # Dependencies
                if any(flow['dependencies'].values()):
                    f.write("#### Dependencies\n\n")
                    if flow['dependencies']['modules']:
                        f.write(f"- **Modules**: {len(flow['dependencies']['modules'])} modules\n")
                    if flow['dependencies']['functions']:
                        f.write(f"- **Functions**: {len(flow['dependencies']['functions'])} functions\n")
                    if flow['dependencies']['database_tables']:
                        f.write(f"- **Tables**: {', '.join(flow['dependencies']['database_tables'][:3])}\n")
                    f.write("\n")
                
                f.write("---\n\n")
            
            f.write("## State Transitions\n\n")
            for entity, transitions in report['state_transitions'].items():
                f.write(f"### {entity}\n\n")
                for trans in transitions:
                    f.write(f"- **Type**: {trans['type']}\n")
                    f.write(f"- **File**: `{trans['file']}`\n")
                    if 'methods' in trans:
                        f.write(f"- **Methods**: {', '.join(trans['methods'][:3])}\n")
                    f.write("\n")
            
            f.write("## Routing Tables\n\n")
            for category, routes in report['routing_tables'].items():
                if routes:
                    f.write(f"### {category.title()}\n\n")
                    f.write("| Method | Path | File |\n")
                    f.write("|--------|------|------|\n")
                    for route in routes[:10]:
                        f.write(f"| {route['method']} | {route['path']} | `{route['file']}` |\n")
                    if len(routes) > 10:
                        f.write(f"\n... and {len(routes) - 10} more routes\n")
                    f.write("\n")
            
            f.write("## Legacy Feature Mapping\n\n")
            f.write(f"- **Total Legacy Features**: {report['diff_report']['summary']['total_legacy_features']}\n")
            f.write(f"- **Matched**: {report['diff_report']['summary']['matched_features']}\n")
            f.write(f"- **Unmatched**: {report['diff_report']['summary']['unmatched_features']}\n\n")
            
            if report['diff_report']['unmatched']:
                f.write("### Unmatched Legacy Features\n\n")
                for unmatched in report['diff_report']['unmatched'][:20]:
                    f.write(f"- **{unmatched['legacy']}** ({unmatched['type']})\n")
                    f.write(f"  - File: `{unmatched['file']}`\n")
                if len(report['diff_report']['unmatched']) > 20:
                    f.write(f"\n... and {len(report['diff_report']['unmatched']) - 20} more\n")
    
    def export_diff_markdown(self, diff_report: Dict[str, Any], output_path: str):
        """Export legacy vs current diff as markdown"""
        with open(output_path, 'w') as f:
            f.write("# Legacy vs Current Feature Diff Report\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            f.write("## Summary\n\n")
            summary = diff_report['summary']
            f.write(f"- **Total Legacy Features**: {summary['total_legacy_features']}\n")
            f.write(f"- **Matched Features**: {summary['matched_features']}\n")
            f.write(f"- **Unmatched Features**: {summary['unmatched_features']}\n\n")
            
            if diff_report['matched']:
                f.write("## Matched Features\n\n")
                f.write("| Legacy Feature | Current Feature | Legacy File |\n")
                f.write("|----------------|-----------------|-------------|\n")
                for match in diff_report['matched'][:20]:
                    f.write(f"| {match['legacy']} | {match['current']} | `{match['legacy_file']}` |\n")
                if len(diff_report['matched']) > 20:
                    f.write(f"\n... and {len(diff_report['matched']) - 20} more matches\n")
                f.write("\n")
            
            if diff_report['unmatched']:
                f.write("## Unmatched Legacy Features\n\n")
                f.write("| Feature | Type | File |\n")
                f.write("|---------|------|------|\n")
                for unmatched in diff_report['unmatched'][:30]:
                    f.write(f"| {unmatched['legacy']} | {unmatched['type']} | `{unmatched['file']}` |\n")
                if len(diff_report['unmatched']) > 30:
                    f.write(f"\n... and {len(diff_report['unmatched']) - 30} more unmatched features\n")
                f.write("\n")
            
            if diff_report['gaps']:
                f.write("## Implementation Gaps (Decimal Checklist Items)\n\n")
                f.write("| Checklist ID | Feature | Type | Priority | Action |\n")
                f.write("|--------------|---------|------|----------|---------|\n")
                
                # Group by priority
                gaps_by_priority = defaultdict(list)
                for gap in diff_report['gaps']:
                    gaps_by_priority[gap['priority']].append(gap)
                
                for priority in ['P1', 'P2', 'P3', 'P4']:
                    if priority in gaps_by_priority:
                        for gap in gaps_by_priority[priority][:20]:
                            f.write(f"| {gap['checklist_id']} | {gap['feature']} | {gap['type']} | {gap['priority']} | {gap['action']} |\n")
                
                total_gaps = len(diff_report['gaps'])
                shown_gaps = min(80, total_gaps)
                if total_gaps > shown_gaps:
                    f.write(f"\n... and {total_gaps - shown_gaps} more gaps\n")


def main():
    parser = argparse.ArgumentParser(description="Build flow design from feature inventory")
    parser.add_argument("--root", default=".", help="Root directory")
    parser.add_argument("--output-dir", default="docs/plan", help="Output directory")
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create reports directory
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Run flow design
    designer = FlowDesigner(args.root)
    report = designer.generate_report()
    
    # Export reports
    json_path = reports_dir / "flow_design.json"
    flow_md_path = output_dir / "FLOW_DESIGN.md"
    diff_md_path = reports_dir / "legacy_vs_current_diff.md"
    
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    designer.export_flow_design_markdown(report, str(flow_md_path))
    designer.export_diff_markdown(report['diff_report'], str(diff_md_path))
    
    print(f"\nFlow Design Complete:")
    print(f"  Existing features: {report['features']['total_existing']}")
    print(f"  Legacy features found: {report['features']['total_legacy']}")
    print(f"  Matched features: {report['diff_report']['summary']['matched_features']}")
    print(f"  Unmatched features: {report['diff_report']['summary']['unmatched_features']}")
    print(f"  Reports saved to:")
    print(f"    - {json_path}")
    print(f"    - {flow_md_path}")
    print(f"    - {diff_md_path}")


if __name__ == "__main__":
    main()