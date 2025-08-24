#!/usr/bin/env python3
"""
Routing Realignment Analysis

Maps endpoints ↔ components ↔ screens and notes variable/function dependencies
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import defaultdict

class RoutingAnalyzer:
    def __init__(self):
        self.routes = defaultdict(dict)
        self.components = defaultdict(dict)
        self.screens = defaultdict(dict)
        self.mappings = []
        self.dependencies = defaultdict(set)
        
    def load_existing_data(self):
        """Load existing data from various sources"""
        # Load var-func map for dependencies
        var_func_file = Path("reports/VAR_FUNC_MAP.json")
        if var_func_file.exists():
            with open(var_func_file, 'r') as f:
                self.var_func_map = json.load(f)
        else:
            self.var_func_map = {"nodes": {}, "edges": []}
            
        # Load flow design for routes
        flow_file = Path("reports/flow_design.json")
        if flow_file.exists():
            with open(flow_file, 'r') as f:
                self.flow_design = json.load(f)
        else:
            self.flow_design = {"features": [], "routing_table": []}
            
        # Load architecture synthesis
        arch_file = Path("docs/plan/architecture_synthesis.json")
        if arch_file.exists():
            with open(arch_file, 'r') as f:
                self.architecture = json.load(f)
        else:
            self.architecture = {}
            
    def analyze_api_routes(self):
        """Analyze API routes from various sources"""
        route_sources = [
            "services/api-gateway/**/*.py",
            "services/*/api/**/*.py",
            "services/*/routes/**/*.py",
            "legacy/*/api/**/*.py"
        ]
        
        for pattern in route_sources:
            for file_path in Path(".").glob(pattern):
                self._extract_routes_from_file(file_path)
                
    def _extract_routes_from_file(self, file_path: Path):
        """Extract route definitions from a Python file"""
        try:
            content = file_path.read_text()
            
            # FastAPI patterns
            fastapi_patterns = [
                r'@app\.(get|post|put|delete|patch)\("([^"]+)"',
                r'@router\.(get|post|put|delete|patch)\("([^"]+)"',
                r'APIRouter\(\s*prefix="([^"]+)"'
            ]
            
            for pattern in fastapi_patterns:
                for match in re.finditer(pattern, content):
                    if match.lastindex == 2:
                        method = match.group(1).upper()
                        path = match.group(2)
                    else:
                        method = "ROUTER"
                        path = match.group(1)
                        
                    route_id = f"{method}:{path}"
                    self.routes[route_id] = {
                        'method': method,
                        'path': path,
                        'file': str(file_path),
                        'line': content[:match.start()].count('\n') + 1,
                        'dependencies': self._extract_route_dependencies(content, match.start())
                    }
                    
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            
    def _extract_route_dependencies(self, content: str, position: int) -> List[str]:
        """Extract function/variable dependencies near a route definition"""
        deps = set()
        
        # Look for function definition containing this route
        lines = content[:position].split('\n')
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip().startswith('def ') or lines[i].strip().startswith('async def '):
                func_match = re.search(r'def\s+(\w+)', lines[i])
                if func_match:
                    deps.add(f"function:{func_match.group(1)}")
                break
                
        # Look for imports used in the function
        import_pattern = r'from\s+(\S+)\s+import\s+([^;]+)'
        for match in re.finditer(import_pattern, content[:position]):
            module = match.group(1)
            imports = match.group(2).split(',')
            for imp in imports:
                imp = imp.strip()
                if imp:
                    deps.add(f"import:{module}.{imp}")
                    
        return list(deps)
        
    def analyze_ui_components(self):
        """Analyze UI components and screens"""
        ui_sources = [
            "services/web-ui/src/**/*.tsx",
            "services/web-ui/src/**/*.jsx",
            "services/admin-ui/src/**/*.tsx",
            "services/admin-ui/src/**/*.jsx",
            "apps/web/**/*.tsx",
            "apps/web/**/*.jsx"
        ]
        
        for pattern in ui_sources:
            for file_path in Path(".").glob(pattern):
                self._extract_components_from_file(file_path)
                
    def _extract_components_from_file(self, file_path: Path):
        """Extract component definitions and API calls from React files"""
        try:
            content = file_path.read_text()
            
            # Component patterns
            component_patterns = [
                r'export\s+(?:default\s+)?(?:function|const)\s+(\w+)',
                r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*[{(]',
                r'function\s+(\w+)\s*\([^)]*\)\s*{',
                r'export\s+{\s*([^}]+)\s*}'
            ]
            
            for pattern in component_patterns:
                for match in re.finditer(pattern, content):
                    comp_name = match.group(1)
                    if comp_name and comp_name[0].isupper():  # React component convention
                        self.components[comp_name] = {
                            'file': str(file_path),
                            'type': 'component',
                            'api_calls': self._extract_api_calls(content),
                            'routes': self._extract_ui_routes(content)
                        }
                        
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            
    def _extract_api_calls(self, content: str) -> List[Dict[str, Any]]:
        """Extract API calls from UI code"""
        api_calls = []
        
        # Patterns for API calls
        api_patterns = [
            r'fetch\s*\(\s*["`\']([^"`\']+)["`\']',
            r'axios\.(get|post|put|delete|patch)\s*\(\s*["`\']([^"`\']+)["`\']',
            r'api\.(get|post|put|delete|patch)\s*\(\s*["`\']([^"`\']+)["`\']'
        ]
        
        for pattern in api_patterns:
            for match in re.finditer(pattern, content):
                if match.lastindex == 2:
                    method = match.group(1).upper()
                    endpoint = match.group(2)
                else:
                    method = "GET"  # Default for fetch
                    endpoint = match.group(1)
                    
                api_calls.append({
                    'method': method,
                    'endpoint': endpoint,
                    'line': content[:match.start()].count('\n') + 1
                })
                
        return api_calls
        
    def _extract_ui_routes(self, content: str) -> List[str]:
        """Extract UI route definitions"""
        routes = []
        
        # React Router patterns
        route_patterns = [
            r'<Route\s+path=["`\']([^"`\']+)["`\']',
            r'path:\s*["`\']([^"`\']+)["`\']',
            r'to=["`\']([^"`\']+)["`\']'
        ]
        
        for pattern in route_patterns:
            for match in re.finditer(pattern, content):
                routes.append(match.group(1))
                
        return routes
        
    def build_mappings(self):
        """Build comprehensive mappings between endpoints, components, and screens"""
        # Map API routes to UI components based on API calls
        for comp_name, comp_data in self.components.items():
            for api_call in comp_data.get('api_calls', []):
                endpoint = api_call['endpoint']
                method = api_call['method']
                
                # Find matching API route
                for route_id, route_data in self.routes.items():
                    if self._match_endpoint(endpoint, route_data['path']):
                        mapping = {
                            'api_route': route_id,
                            'api_path': route_data['path'],
                            'api_file': route_data['file'],
                            'component': comp_name,
                            'component_file': comp_data['file'],
                            'ui_routes': comp_data.get('routes', []),
                            'dependencies': route_data.get('dependencies', [])
                        }
                        self.mappings.append(mapping)
                        
    def _match_endpoint(self, endpoint: str, route_path: str) -> bool:
        """Check if an endpoint matches a route path pattern"""
        # Normalize paths
        endpoint = endpoint.strip('/')
        route_path = route_path.strip('/')
        
        # Convert route parameters to regex
        param_pattern = re.sub(r'{[^}]+}', r'[^/]+', route_path)
        param_pattern = re.sub(r':(\w+)', r'[^/]+', param_pattern)
        
        # Escape special regex characters except our patterns
        param_pattern = re.escape(param_pattern)
        param_pattern = param_pattern.replace(r'\[', '[').replace(r'\]', ']')
        param_pattern = param_pattern.replace(r'\^', '^').replace(r'\+', '+')
        
        try:
            return bool(re.match(f"^{param_pattern}$", endpoint))
        except re.PatternError:
            # If pattern is invalid, do simple string comparison
            return endpoint == route_path
        
    def identify_realignment_needs(self):
        """Identify routing realignment opportunities"""
        realignment = {
            'orphan_routes': [],
            'orphan_components': [],
            'mismatched_patterns': [],
            'optimization_opportunities': []
        }
        
        # Find orphan API routes (no UI component uses them)
        used_routes = {m['api_route'] for m in self.mappings}
        for route_id in self.routes:
            if route_id not in used_routes:
                realignment['orphan_routes'].append({
                    'route': route_id,
                    'path': self.routes[route_id]['path'],
                    'file': self.routes[route_id]['file']
                })
                
        # Find orphan components (make API calls to non-existent routes)
        for comp_name, comp_data in self.components.items():
            for api_call in comp_data.get('api_calls', []):
                matched = False
                for route_id, route_data in self.routes.items():
                    if self._match_endpoint(api_call['endpoint'], route_data['path']):
                        matched = True
                        break
                if not matched:
                    realignment['orphan_components'].append({
                        'component': comp_name,
                        'file': comp_data['file'],
                        'unmapped_endpoint': api_call['endpoint']
                    })
                    
        # Identify pattern mismatches
        api_patterns = defaultdict(int)
        ui_patterns = defaultdict(int)
        
        for route_id, route_data in self.routes.items():
            pattern = re.sub(r'{[^}]+}', '*', route_data['path'])
            pattern = re.sub(r':(\w+)', '*', pattern)
            api_patterns[pattern] += 1
            
        for comp_data in self.components.values():
            for route in comp_data.get('routes', []):
                pattern = re.sub(r'/\d+', '/*', route)
                ui_patterns[pattern] += 1
                
        # Find inconsistent patterns
        all_patterns = set(api_patterns.keys()) | set(ui_patterns.keys())
        for pattern in all_patterns:
            if api_patterns[pattern] != ui_patterns[pattern]:
                realignment['mismatched_patterns'].append({
                    'pattern': pattern,
                    'api_count': api_patterns[pattern],
                    'ui_count': ui_patterns[pattern]
                })
                
        return realignment
        
    def export_report(self):
        """Export routing realignment report"""
        report = {
            'summary': {
                'total_api_routes': len(self.routes),
                'total_ui_components': len(self.components),
                'total_mappings': len(self.mappings),
                'analyzed_at': str(Path.cwd())
            },
            'routes': dict(self.routes),
            'components': dict(self.components),
            'mappings': self.mappings,
            'realignment_needs': self.identify_realignment_needs()
        }
        
        # Save JSON report
        with open('reports/routing_realignment.json', 'w') as f:
            json.dump(report, f, indent=2)
            
        # Generate markdown report
        self._generate_markdown_report(report)
        
        return report
        
    def _generate_markdown_report(self, report: Dict[str, Any]):
        """Generate markdown documentation"""
        with open('docs/plan/ROUTING_REALIGNMENT.md', 'w') as f:
            f.write("# Routing Realignment Analysis\n\n")
            f.write("## Executive Summary\n\n")
            f.write(f"- **Total API Routes**: {report['summary']['total_api_routes']}\n")
            f.write(f"- **Total UI Components**: {report['summary']['total_ui_components']}\n")
            f.write(f"- **Total Mappings**: {report['summary']['total_mappings']}\n")
            f.write(f"- **Analysis Path**: {report['summary']['analyzed_at']}\n\n")
            
            # Endpoint to Component Mappings
            f.write("## Endpoint ↔ Component ↔ Screen Mappings\n\n")
            if report['mappings']:
                for mapping in sorted(report['mappings'], key=lambda m: m['api_path']):
                    f.write(f"### {mapping['api_path']}\n\n")
                    f.write(f"- **API Route**: `{mapping['api_route']}`\n")
                    f.write(f"- **API File**: `{mapping['api_file']}`\n")
                    f.write(f"- **Component**: `{mapping['component']}`\n")
                    f.write(f"- **Component File**: `{mapping['component_file']}`\n")
                    if mapping['ui_routes']:
                        f.write(f"- **UI Routes**: {', '.join(f'`{r}`' for r in mapping['ui_routes'])}\n")
                    if mapping['dependencies']:
                        f.write(f"- **Dependencies**:\n")
                        for dep in mapping['dependencies']:
                            f.write(f"  - {dep}\n")
                    f.write("\n")
            else:
                f.write("*No mappings found*\n\n")
                
            # Realignment Needs
            f.write("## Realignment Needs\n\n")
            realignment = report['realignment_needs']
            
            f.write("### Orphan API Routes\n")
            f.write("Routes with no corresponding UI components:\n\n")
            if realignment['orphan_routes']:
                for orphan in realignment['orphan_routes']:
                    f.write(f"- `{orphan['route']}` - {orphan['path']} ({orphan['file']})\n")
            else:
                f.write("*None found*\n")
            f.write("\n")
            
            f.write("### Orphan Components\n")
            f.write("Components calling non-existent API endpoints:\n\n")
            if realignment['orphan_components']:
                for orphan in realignment['orphan_components']:
                    f.write(f"- `{orphan['component']}` calls `{orphan['unmapped_endpoint']}` ({orphan['file']})\n")
            else:
                f.write("*None found*\n")
            f.write("\n")
            
            f.write("### Pattern Mismatches\n")
            f.write("Routing patterns with API/UI count mismatches:\n\n")
            if realignment['mismatched_patterns']:
                for mismatch in realignment['mismatched_patterns']:
                    f.write(f"- Pattern `{mismatch['pattern']}`: API={mismatch['api_count']}, UI={mismatch['ui_count']}\n")
            else:
                f.write("*None found*\n")
            f.write("\n")
            
            # Routing Architecture
            f.write("## Routing Architecture\n\n")
            f.write("```mermaid\n")
            f.write("graph TD\n")
            f.write("    subgraph API Layer\n")
            for i, (route_id, route) in enumerate(list(report['routes'].items())[:10]):  # Show first 10
                f.write(f"        API{i}[\"{route['method']} {route['path']}\"]\n")
            if len(report['routes']) > 10:
                f.write(f"        APIMore[\"...and {len(report['routes']) - 10} more\"]\n")
            f.write("    end\n")
            f.write("    subgraph UI Layer\n")
            for i, comp_name in enumerate(list(report['components'].keys())[:10]):  # Show first 10
                f.write(f"        UI{i}[{comp_name}]\n")
            if len(report['components']) > 10:
                f.write(f"        UIMore[\"...and {len(report['components']) - 10} more\"]\n")
            f.write("    end\n")
            # Show some connections
            for i, mapping in enumerate(report['mappings'][:5]):  # Show first 5 connections
                f.write(f"    API{i} --> UI{i}\n")
            f.write("```\n\n")
            
            # Recommendations
            f.write("## Recommendations\n\n")
            f.write("1. **Address Orphan Routes**: Review and either remove or create UI components for orphan API routes\n")
            f.write("2. **Fix Orphan Components**: Update component API calls to match existing routes or create missing routes\n")
            f.write("3. **Standardize Patterns**: Align routing patterns between API and UI layers\n")
            f.write("4. **Optimize Dependencies**: Review and minimize cross-module dependencies\n")


def main():
    analyzer = RoutingAnalyzer()
    
    print("Loading existing data...")
    analyzer.load_existing_data()
    
    print("Analyzing API routes...")
    analyzer.analyze_api_routes()
    
    print("Analyzing UI components...")
    analyzer.analyze_ui_components()
    
    print("Building mappings...")
    analyzer.build_mappings()
    
    print("Generating report...")
    report = analyzer.export_report()
    
    print(f"✓ Found {len(report['routes'])} API routes")
    print(f"✓ Found {len(report['components'])} UI components")
    print(f"✓ Created {len(report['mappings'])} mappings")
    print(f"✓ Report saved to docs/plan/ROUTING_REALIGNMENT.md")


if __name__ == "__main__":
    main()