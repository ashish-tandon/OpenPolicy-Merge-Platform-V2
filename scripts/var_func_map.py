#!/usr/bin/env python3
"""
Variable → Function → Module Mapping Script
Scans codebase for variables, functions, modules and builds dependency graph
"""

import os
import re
import json
import ast
import glob
from pathlib import Path
from typing import Dict, List, Set, Any
from collections import defaultdict

class CodeMapper:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.nodes = []
        self.edges = []
        self.feature_map = {}
        self.endpoint_map = {}
        
    def scan_python_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse Python file using AST"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            variables = set()
            functions = set()
            classes = set()
            imports = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            variables.add(target.id)
                elif isinstance(node, ast.FunctionDef):
                    functions.add(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.add(node.name)
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module)
            
            return {
                'file': str(file_path.relative_to(self.root_dir)),
                'language': 'python',
                'variables': list(variables),
                'functions': list(functions),
                'classes': list(classes),
                'imports': list(imports)
            }
        except Exception as e:
            return {
                'file': str(file_path.relative_to(self.root_dir)),
                'language': 'python',
                'error': str(e),
                'variables': [],
                'functions': [],
                'classes': [],
                'imports': []
            }
    
    def scan_js_ts_file(self, file_path: Path) -> Dict[str, Any]:
        """Scan JS/TS file using regex patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract variables (const, let, var)
            var_pattern = r'\b(?:const|let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\b'
            variables = set(re.findall(var_pattern, content))
            
            # Extract functions
            func_pattern = r'\b(?:function|async\s+function)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\b'
            functions = set(re.findall(func_pattern, content))
            
            # Extract arrow functions
            arrow_pattern = r'\b([a-zA-Z_$][a-zA-Z0-9_$]*)\s*[:=]\s*(?:async\s*)?\([^)]*\)\s*=>'
            arrow_funcs = set(re.findall(arrow_pattern, content))
            functions.update(arrow_funcs)
            
            # Extract classes
            class_pattern = r'\bclass\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\b'
            classes = set(re.findall(class_pattern, content))
            
            # Extract imports/exports
            import_pattern = r'\b(?:import|export)\s+(?:{[^}]*}|\*|[a-zA-Z_$][a-zA-Z0-9_$]*)\s+from\s+[\'"]([^\'"]+)[\'"]'
            imports = set(re.findall(import_pattern, content))
            
            return {
                'file': str(file_path.relative_to(self.root_dir)),
                'language': 'typescript' if file_path.suffix == '.ts' else 'javascript',
                'variables': list(variables),
                'functions': list(functions),
                'classes': list(classes),
                'imports': list(imports)
            }
        except Exception as e:
            return {
                'file': str(file_path.relative_to(self.root_dir)),
                'language': 'typescript' if file_path.suffix == '.ts' else 'javascript',
                'error': str(e),
                'variables': [],
                'functions': [],
                'classes': [],
                'imports': []
            }
    
    def scan_sql_file(self, file_path: Path) -> Dict[str, Any]:
        """Scan SQL file for table/column references"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract table names
            table_pattern = r'\b(?:FROM|JOIN|UPDATE|INSERT\s+INTO|CREATE\s+TABLE)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b'
            tables = set(re.findall(table_pattern, content, re.IGNORECASE))
            
            # Extract column names
            column_pattern = r'\b(?:SELECT|WHERE|SET|VALUES)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b'
            columns = set(re.findall(column_pattern, content, re.IGNORECASE))
            
            return {
                'file': str(file_path.relative_to(self.root_dir)),
                'language': 'sql',
                'tables': list(tables),
                'columns': list(columns),
                'variables': [],
                'functions': [],
                'classes': [],
                'imports': []
            }
        except Exception as e:
            return {
                'file': str(file_path.relative_to(self.root_dir)),
                'language': 'sql',
                'error': str(e),
                'tables': [],
                'columns': [],
                'variables': [],
                'functions': [],
                'classes': [],
                'imports': []
            }
    
    def scan_yaml_yml_file(self, file_path: Path) -> Dict[str, Any]:
        """Scan YAML files for configuration variables"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract key names (simplified YAML parsing)
            key_pattern = r'^(\s*)([a-zA-Z_][a-zA-Z0-9_-]*)\s*:'
            keys = set()
            for line in content.split('\n'):
                match = re.match(key_pattern, line)
                if match:
                    keys.add(match.group(2))
            
            return {
                'file': str(file_path.relative_to(self.root_dir)),
                'language': 'yaml',
                'variables': list(keys),
                'functions': [],
                'classes': [],
                'imports': []
            }
        except Exception as e:
            return {
                'file': str(file_path.relative_to(self.root_dir)),
                'language': 'yaml',
                'error': str(e),
                'variables': [],
                'functions': [],
                'classes': [],
                'imports': []
            }
    
    def scan_file(self, file_path: Path) -> Dict[str, Any]:
        """Route file to appropriate scanner based on extension"""
        suffix = file_path.suffix.lower()
        
        if suffix in ['.py']:
            return self.scan_python_file(file_path)
        elif suffix in ['.js', '.ts', '.jsx', '.tsx']:
            return self.scan_js_ts_file(file_path)
        elif suffix in ['.sql']:
            return self.scan_sql_file(file_path)
        elif suffix in ['.yml', '.yaml']:
            return self.scan_yaml_yml_file(file_path)
        else:
            return None
    
    def build_graph(self):
        """Build the complete dependency graph"""
        # Scan all source files
        source_patterns = [
            'services/**/*.py',
            'services/**/*.js',
            'services/**/*.ts',
            'services/**/*.jsx',
            'services/**/*.tsx',
            'services/**/*.sql',
            'services/**/*.yml',
            'services/**/*.yaml',
            'scripts/*.py',
            'scripts/*.sh'
        ]
        
        all_files = []
        for pattern in source_patterns:
            all_files.extend(glob.glob(pattern, recursive=True))
        
        print(f"Scanning {len(all_files)} source files...")
        
        # Process each file
        for file_path in all_files:
            path = Path(file_path)
            if path.is_file():
                result = self.scan_file(path)
                if result:
                    self.nodes.append(result)
        
        # Build edges (dependencies)
        self.build_edges()
        
        return {
            'nodes': self.nodes,
            'edges': self.edges,
            'metadata': {
                'total_files': len(self.nodes),
                'languages': list(set(node['language'] for node in self.nodes)),
                'total_variables': sum(len(node.get('variables', [])) for node in self.nodes),
                'total_functions': sum(len(node.get('functions', [])) for node in self.nodes),
                'total_classes': sum(len(node.get('classes', [])) for node in self.nodes)
            }
        }
    
    def build_edges(self):
        """Build dependency edges between nodes"""
        # Build import/use relationships
        for i, node in enumerate(self.nodes):
            if 'imports' in node:
                for imp in node['imports']:
                    # Find target node
                    for j, target in enumerate(self.nodes):
                        if target['file'].endswith(imp) or imp in target['file']:
                            self.edges.append({
                                'from': i,
                                'to': j,
                                'type': 'imports',
                                'label': f"imports {imp}"
                            })
        
        # Build function call relationships (simplified)
        for i, node in enumerate(self.nodes):
            if 'functions' in node:
                for func in node['functions']:
                    # Look for function calls in other nodes
                    for j, target in enumerate(self.nodes):
                        if i != j and 'variables' in target:
                            if func in target['variables']:
                                self.edges.append({
                                    'from': j,
                                    'to': i,
                                    'type': 'calls',
                                    'label': f"calls {func}"
                                })
    
    def generate_dot(self, output_file: str):
        """Generate Graphviz DOT file"""
        dot_content = ["digraph CodeMap {"]
        dot_content.append("  rankdir=LR;")
        dot_content.append("  node [shape=box, style=filled];")
        
        # Add nodes
        for i, node in enumerate(self.nodes):
            color = {
                'python': 'lightblue',
                'typescript': 'lightgreen',
                'javascript': 'lightyellow',
                'sql': 'lightcoral',
                'yaml': 'lightpink'
            }.get(node['language'], 'white')
            
            label = f"{node['file']}\\n{node['language']}"
            dot_content.append(f'  {i} [label="{label}", fillcolor="{color}"];')
        
        # Add edges
        for edge in self.edges:
            dot_content.append(f'  {edge["from"]} -> {edge["to"]} [label="{edge["label"]}"];')
        
        dot_content.append("}")
        
        with open(output_file, 'w') as f:
            f.write('\n'.join(dot_content))
        
        print(f"Generated DOT file: {output_file}")
    
    def save_json(self, output_file: str):
        """Save the complete graph as JSON"""
        graph = self.build_graph()
        
        with open(output_file, 'w') as f:
            json.dump(graph, f, indent=2)
        
        print(f"Generated JSON file: {output_file}")
        return graph

def main():
    mapper = CodeMapper()
    
    # Generate outputs
    json_file = "reports/VAR_FUNC_MAP.json"
    dot_file = "reports/VAR_FUNC_MAP.dot"
    
    os.makedirs("reports", exist_ok=True)
    
    # Generate JSON
    graph = mapper.save_json(json_file)
    
    # Generate DOT
    mapper.generate_dot(dot_file)
    
    # Try to generate PNG if Graphviz is available
    try:
        import subprocess
        result = subprocess.run(['dot', '-Tpng', dot_file, '-o', 'reports/VAR_FUNC_MAP.png'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("Generated PNG file: reports/VAR_FUNC_MAP.png")
        else:
            print("Graphviz not available, PNG generation skipped")
    except FileNotFoundError:
        print("Graphviz not available, PNG generation skipped")
    
    # Print summary
    print(f"\n=== SCANNING COMPLETE ===")
    print(f"Files scanned: {graph['metadata']['total_files']}")
    print(f"Languages found: {', '.join(graph['metadata']['languages'])}")
    print(f"Total variables: {graph['metadata']['total_variables']}")
    print(f"Total functions: {graph['metadata']['total_functions']}")
    print(f"Total classes: {graph['metadata']['total_classes']}")
    print(f"Total edges: {len(graph['edges'])}")

if __name__ == "__main__":
    main()
