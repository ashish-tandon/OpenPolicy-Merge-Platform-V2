#!/usr/bin/env python3
"""
Variable → Function → Module Mapping Tool
Builds a comprehensive graph of code relationships across the codebase
"""

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from collections import defaultdict
import argparse


class CodeMapper:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.nodes = defaultdict(dict)  # {id: {type, name, file, language, ...}}
        self.edges = []  # [{from, to, type, ...}]
        self.node_id_counter = 0
        self.node_id_map = {}  # {(type, name, file): node_id}
        
    def get_or_create_node(self, node_type: str, name: str, file_path: str, 
                          language: str, **kwargs) -> int:
        """Get existing node ID or create new node"""
        key = (node_type, name, str(file_path))
        if key in self.node_id_map:
            return self.node_id_map[key]
        
        node_id = self.node_id_counter
        self.node_id_counter += 1
        self.nodes[node_id] = {
            "id": node_id,
            "type": node_type,
            "name": name,
            "file": str(file_path.relative_to(self.root_path)),
            "language": language,
            **kwargs
        }
        self.node_id_map[key] = node_id
        return node_id
    
    def add_edge(self, from_id: int, to_id: int, edge_type: str, **kwargs):
        """Add edge between nodes"""
        self.edges.append({
            "from": from_id,
            "to": to_id,
            "type": edge_type,
            **kwargs
        })
    
    def analyze_python_file(self, file_path: Path):
        """Analyze Python file using AST"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, str(file_path))
            
            # Current scope tracking
            current_module = self.get_or_create_node(
                "module", file_path.stem, file_path, "python"
            )
            
            class PythonVisitor(ast.NodeVisitor):
                def __init__(self, mapper, file_path, module_id):
                    self.mapper = mapper
                    self.file_path = file_path
                    self.module_id = module_id
                    self.current_function = None
                    self.current_class = None
                    
                def visit_FunctionDef(self, node):
                    func_id = self.mapper.get_or_create_node(
                        "function", node.name, self.file_path, "python",
                        line=node.lineno, parent_class=self.current_class
                    )
                    self.mapper.add_edge(self.module_id, func_id, "defines")
                    
                    # Analyze function parameters
                    for arg in node.args.args:
                        var_id = self.mapper.get_or_create_node(
                            "variable", arg.arg, self.file_path, "python",
                            scope=node.name, line=arg.lineno if hasattr(arg, 'lineno') else node.lineno
                        )
                        self.mapper.add_edge(func_id, var_id, "parameter")
                    
                    old_func = self.current_function
                    self.current_function = func_id
                    self.generic_visit(node)
                    self.current_function = old_func
                
                def visit_ClassDef(self, node):
                    class_id = self.mapper.get_or_create_node(
                        "class", node.name, self.file_path, "python",
                        line=node.lineno
                    )
                    self.mapper.add_edge(self.module_id, class_id, "defines")
                    
                    old_class = self.current_class
                    self.current_class = node.name
                    self.generic_visit(node)
                    self.current_class = old_class
                
                def visit_Assign(self, node):
                    # Handle variable assignments
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            var_id = self.mapper.get_or_create_node(
                                "variable", target.id, self.file_path, "python",
                                line=node.lineno, scope=self.current_function or self.module_id
                            )
                            if self.current_function:
                                self.mapper.add_edge(self.current_function, var_id, "defines")
                            else:
                                self.mapper.add_edge(self.module_id, var_id, "defines")
                    self.generic_visit(node)
                
                def visit_Call(self, node):
                    # Track function calls
                    if isinstance(node.func, ast.Name):
                        call_target = self.mapper.get_or_create_node(
                            "function", node.func.id, self.file_path, "python",
                            is_call_target=True
                        )
                        if self.current_function:
                            self.mapper.add_edge(self.current_function, call_target, "calls")
                        else:
                            self.mapper.add_edge(self.module_id, call_target, "calls")
                    elif isinstance(node.func, ast.Attribute):
                        # Method calls
                        method_name = node.func.attr
                        call_target = self.mapper.get_or_create_node(
                            "method", method_name, self.file_path, "python",
                            is_call_target=True
                        )
                        if self.current_function:
                            self.mapper.add_edge(self.current_function, call_target, "calls")
                    self.generic_visit(node)
                
                def visit_Import(self, node):
                    for alias in node.names:
                        import_id = self.mapper.get_or_create_node(
                            "import", alias.name, self.file_path, "python",
                            alias=alias.asname
                        )
                        self.mapper.add_edge(self.module_id, import_id, "imports")
                
                def visit_ImportFrom(self, node):
                    module = node.module or ""
                    for alias in node.names:
                        import_id = self.mapper.get_or_create_node(
                            "import", f"{module}.{alias.name}", self.file_path, "python",
                            alias=alias.asname
                        )
                        self.mapper.add_edge(self.module_id, import_id, "imports")
            
            visitor = PythonVisitor(self, file_path, current_module)
            visitor.visit(tree)
            
        except Exception as e:
            print(f"Error analyzing Python file {file_path}: {e}")
    
    def analyze_javascript_file(self, file_path: Path):
        """Analyze JavaScript/TypeScript file using regex patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            current_module = self.get_or_create_node(
                "module", file_path.stem, file_path, "javascript"
            )
            
            # Function declarations: function name() or const name = function
            func_pattern = r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?function|\b(\w+)\s*:\s*(?:async\s+)?function)'
            for match in re.finditer(func_pattern, content):
                func_name = match.group(1) or match.group(2) or match.group(3)
                if func_name:
                    func_id = self.get_or_create_node(
                        "function", func_name, file_path, "javascript"
                    )
                    self.add_edge(current_module, func_id, "defines")
            
            # Arrow functions: const name = () =>
            arrow_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>'
            for match in re.finditer(arrow_pattern, content):
                func_name = match.group(1)
                func_id = self.get_or_create_node(
                    "function", func_name, file_path, "javascript"
                )
                self.add_edge(current_module, func_id, "defines")
            
            # Variable declarations
            var_pattern = r'(?:const|let|var)\s+(\w+)(?:\s*[:=])?'
            for match in re.finditer(var_pattern, content):
                var_name = match.group(1)
                var_id = self.get_or_create_node(
                    "variable", var_name, file_path, "javascript"
                )
                self.add_edge(current_module, var_id, "defines")
            
            # Class declarations
            class_pattern = r'class\s+(\w+)'
            for match in re.finditer(class_pattern, content):
                class_name = match.group(1)
                class_id = self.get_or_create_node(
                    "class", class_name, file_path, "javascript"
                )
                self.add_edge(current_module, class_id, "defines")
            
            # Import statements
            import_pattern = r'import\s+(?:{([^}]+)}|(\w+))\s+from\s+[\'"]([^\'"]+)[\'"]'
            for match in re.finditer(import_pattern, content):
                imports = match.group(1) or match.group(2)
                module_path = match.group(3)
                if imports:
                    for imp in imports.split(','):
                        imp = imp.strip()
                        import_id = self.get_or_create_node(
                            "import", f"{module_path}.{imp}", file_path, "javascript"
                        )
                        self.add_edge(current_module, import_id, "imports")
            
            # Export statements
            export_pattern = r'export\s+(?:default\s+)?(?:function|class|const|let|var)?\s*(\w+)'
            for match in re.finditer(export_pattern, content):
                export_name = match.group(1)
                if export_name:
                    export_id = self.get_or_create_node(
                        "export", export_name, file_path, "javascript"
                    )
                    self.add_edge(current_module, export_id, "exports")
                    
        except Exception as e:
            print(f"Error analyzing JavaScript file {file_path}: {e}")
    
    def analyze_sql_file(self, file_path: Path):
        """Analyze SQL file for tables and columns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().upper()
            
            current_module = self.get_or_create_node(
                "module", file_path.stem, file_path, "sql"
            )
            
            # CREATE TABLE statements
            table_pattern = r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:(\w+)\.)?(\w+)'
            for match in re.finditer(table_pattern, content):
                schema = match.group(1) or 'public'
                table_name = match.group(2)
                table_id = self.get_or_create_node(
                    "table", f"{schema}.{table_name}".lower(), file_path, "sql"
                )
                self.add_edge(current_module, table_id, "creates")
            
            # ALTER TABLE statements
            alter_pattern = r'ALTER\s+TABLE\s+(?:(\w+)\.)?(\w+)'
            for match in re.finditer(alter_pattern, content):
                schema = match.group(1) or 'public'
                table_name = match.group(2)
                table_id = self.get_or_create_node(
                    "table", f"{schema}.{table_name}".lower(), file_path, "sql"
                )
                self.add_edge(current_module, table_id, "alters")
                
        except Exception as e:
            print(f"Error analyzing SQL file {file_path}: {e}")
    
    def analyze_codebase(self):
        """Analyze entire codebase"""
        print(f"Analyzing codebase at {self.root_path}")
        
        # Define file patterns to analyze
        patterns = {
            "python": ["**/*.py"],
            "javascript": ["**/*.js", "**/*.jsx", "**/*.ts", "**/*.tsx"],
            "sql": ["**/*.sql", "**/migrations/*.sql"]
        }
        
        # Skip these directories
        skip_dirs = {'.git', 'node_modules', 'venv', '__pycache__', '.pytest_cache', 
                    'dist', 'build', '.next', 'coverage', '.nyc_output'}
        
        for language, file_patterns in patterns.items():
            for pattern in file_patterns:
                for file_path in self.root_path.rglob(pattern):
                    # Skip if in ignored directory
                    if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
                        continue
                    
                    print(f"  Analyzing {file_path.relative_to(self.root_path)}")
                    
                    if language == "python":
                        self.analyze_python_file(file_path)
                    elif language == "javascript":
                        self.analyze_javascript_file(file_path)
                    elif language == "sql":
                        self.analyze_sql_file(file_path)
    
    def generate_hotspots(self) -> Dict[str, Any]:
        """Identify high-degree nodes (hotspots)"""
        # Count edges for each node
        in_degree = defaultdict(int)
        out_degree = defaultdict(int)
        
        for edge in self.edges:
            out_degree[edge["from"]] += 1
            in_degree[edge["to"]] += 1
        
        # Find hotspots
        hotspots = {
            "most_called_functions": [],
            "most_used_variables": [],
            "most_importing_modules": [],
            "most_imported_modules": []
        }
        
        for node_id, node in self.nodes.items():
            total_degree = in_degree[node_id] + out_degree[node_id]
            
            if node["type"] == "function" and in_degree[node_id] > 5:
                hotspots["most_called_functions"].append({
                    "name": node["name"],
                    "file": node["file"],
                    "call_count": in_degree[node_id]
                })
            
            if node["type"] == "variable" and total_degree > 10:
                hotspots["most_used_variables"].append({
                    "name": node["name"],
                    "file": node["file"],
                    "usage_count": total_degree
                })
            
            if node["type"] == "module" and out_degree[node_id] > 20:
                hotspots["most_importing_modules"].append({
                    "name": node["name"],
                    "file": node["file"],
                    "import_count": out_degree[node_id]
                })
        
        # Sort hotspots
        for key in hotspots:
            hotspots[key] = sorted(
                hotspots[key], 
                key=lambda x: x.get("call_count", x.get("usage_count", x.get("import_count", 0))),
                reverse=True
            )[:10]  # Top 10
        
        return hotspots
    
    def export_json(self, output_path: str):
        """Export graph to JSON"""
        data = {
            "nodes": list(self.nodes.values()),
            "edges": self.edges,
            "hotspots": self.generate_hotspots(),
            "stats": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "node_types": defaultdict(int),
                "edge_types": defaultdict(int)
            }
        }
        
        # Calculate stats
        for node in self.nodes.values():
            data["stats"]["node_types"][node["type"]] += 1
        
        for edge in self.edges:
            data["stats"]["edge_types"][edge["type"]] += 1
        
        # Convert defaultdict to regular dict for JSON serialization
        data["stats"]["node_types"] = dict(data["stats"]["node_types"])
        data["stats"]["edge_types"] = dict(data["stats"]["edge_types"])
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Exported to {output_path}")
        return data
    
    def export_dot(self, output_path: str):
        """Export graph to Graphviz DOT format"""
        with open(output_path, 'w') as f:
            f.write("digraph CodeMap {\n")
            f.write("  rankdir=LR;\n")
            f.write("  node [shape=box];\n\n")
            
            # Define node styles by type
            node_styles = {
                "module": 'shape=folder,style=filled,fillcolor=lightblue',
                "class": 'shape=box,style=filled,fillcolor=lightgreen',
                "function": 'shape=ellipse,style=filled,fillcolor=lightyellow',
                "variable": 'shape=circle,style=filled,fillcolor=lightgray',
                "table": 'shape=cylinder,style=filled,fillcolor=lightcoral',
                "import": 'shape=diamond,style=filled,fillcolor=lavender',
                "export": 'shape=diamond,style=filled,fillcolor=lightpink'
            }
            
            # Write nodes
            for node_id, node in self.nodes.items():
                label = f"{node['name']}\\n({node['file']})"
                style = node_styles.get(node['type'], '')
                f.write(f'  n{node_id} [label="{label}",{style}];\n')
            
            f.write("\n")
            
            # Write edges
            edge_styles = {
                "defines": 'color=blue',
                "calls": 'color=red',
                "imports": 'color=green,style=dashed',
                "exports": 'color=purple,style=dashed',
                "uses": 'color=gray',
                "parameter": 'color=orange'
            }
            
            for edge in self.edges:
                style = edge_styles.get(edge['type'], '')
                f.write(f'  n{edge["from"]} -> n{edge["to"]} [{style},label="{edge["type"]}"];\n')
            
            f.write("}\n")
        
        print(f"Exported DOT to {output_path}")
        
        # Try to generate PNG if Graphviz is available
        try:
            png_path = output_path.replace('.dot', '.png')
            subprocess.run(['dot', '-Tpng', output_path, '-o', png_path], check=True)
            print(f"Generated PNG at {png_path}")
        except subprocess.CalledProcessError:
            print("Could not generate PNG (Graphviz not available)")
        except FileNotFoundError:
            print("Could not generate PNG (Graphviz 'dot' command not found)")


def main():
    parser = argparse.ArgumentParser(description="Generate variable→function→module mapping")
    parser.add_argument("--root", default=".", help="Root directory to analyze")
    parser.add_argument("--output-dir", default="reports", help="Output directory")
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Run analysis
    mapper = CodeMapper(args.root)
    mapper.analyze_codebase()
    
    # Export results
    json_path = output_dir / "VAR_FUNC_MAP.json"
    dot_path = output_dir / "VAR_FUNC_MAP.dot"
    
    data = mapper.export_json(str(json_path))
    mapper.export_dot(str(dot_path))
    
    # Print summary
    print("\nSummary:")
    print(f"  Total nodes: {data['stats']['total_nodes']}")
    print(f"  Total edges: {data['stats']['total_edges']}")
    print("\nNode types:")
    for node_type, count in data['stats']['node_types'].items():
        print(f"  {node_type}: {count}")
    print("\nEdge types:")
    for edge_type, count in data['stats']['edge_types'].items():
        print(f"  {edge_type}: {count}")
    
    if data['hotspots']['most_called_functions']:
        print("\nTop called functions:")
        for func in data['hotspots']['most_called_functions'][:5]:
            print(f"  {func['name']} ({func['file']}): {func['call_count']} calls")


if __name__ == "__main__":
    main()