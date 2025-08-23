#!/usr/bin/env python3
"""
Simple Python Code Scanner
Scans Python files for variables, functions, and classes
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
    """Main scanning function"""
    results = []
    
    # Find all Python files
    python_files = []
    for root, dirs, files in os.walk('services'):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} Python files")
    
    # Scan each file
    for file_path in python_files:
        result = scan_python_file(file_path)
        results.append(result)
    
    # Save results
    os.makedirs('reports', exist_ok=True)
    with open('reports/python_scan.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Scanned {len(results)} files")
    print(f"Results saved to reports/python_scan.json")

if __name__ == "__main__":
    main()
