#!/usr/bin/env python3
"""
Focused OpenPolicy Service Scanner
Scans only the main service files, excluding node_modules
"""

import os
import ast
import json
from pathlib import Path

def scan_python_file(file_path):
    """Scan a single Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        variables = set()
        functions = set()
        classes = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables.add(target.id)
            elif isinstance(node, ast.FunctionDef):
                functions.add(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.add(node.name)
        
        return {
            'file': str(file_path),
            'variables': list(variables),
            'functions': list(functions),
            'classes': list(classes)
        }
    except Exception as e:
        return {
            'file': str(file_path),
            'error': str(e),
            'variables': [],
            'functions': [],
            'classes': []
        }

def main():
    """Main scanning function - focused on main services"""
    results = []
    
    # Focus only on main OpenPolicy services
    focus_dirs = [
        'services/api-gateway',
        'services/etl',
        'services/web-ui',
        'services/user-service',
        'scripts'
    ]
    
    python_files = []
    for focus_dir in focus_dirs:
        if os.path.exists(focus_dir):
            for root, dirs, files in os.walk(focus_dir):
                # Skip node_modules and other unwanted directories
                dirs[:] = [d for d in dirs if d not in ['node_modules', '__pycache__', '.git', 'venv']]
                
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} focused Python files")
    
    # Scan each file
    for file_path in python_files:
        result = scan_python_file(file_path)
        results.append(result)
    
    # Save results
    os.makedirs('reports', exist_ok=True)
    with open('reports/focused_python_scan.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Scanned {len(results)} focused files")
    print(f"Results saved to reports/focused_python_scan.json")
    
    # Print summary
    total_vars = sum(len(r.get('variables', [])) for r in results)
    total_funcs = sum(len(r.get('functions', [])) for r in results)
    total_classes = sum(len(r.get('classes', [])) for r in results)
    
    print(f"\nSummary:")
    print(f"Total variables: {total_vars}")
    print(f"Total functions: {total_funcs}")
    print(f"Total classes: {total_classes}")

if __name__ == "__main__":
    main()
