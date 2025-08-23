#!/usr/bin/env python3
"""
Bug Audit Script
Aggregates bugs from existing files, logs, and issue trackers
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

def scan_bug_files():
    """Scan existing bug-related files"""
    bug_files = []
    
    # Look for bug-related files
    bug_patterns = [
        '**/bug*.md',
        '**/BUG*.md',
        '**/error*.md',
        '**/ERROR*.md',
        '**/issue*.md',
        '**/ISSUE*.md'
    ]
    
    for pattern in bug_patterns:
        for file_path in Path('.').glob(pattern):
            if file_path.is_file():
                bug_files.append(str(file_path))
    
    return bug_files

def extract_bugs_from_file(file_path):
    """Extract bug information from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        bugs = []
        
        # Look for bug patterns
        bug_patterns = [
            r'BUG[:\s]+([^\n]+)',
            r'Error[:\s]+([^\n]+)',
            r'Issue[:\s]+([^\n]+)',
            r'Problem[:\s]+([^\n]+)',
            r'Failed[:\s]+([^\n]+)'
        ]
        
        for pattern in bug_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                bugs.append({
                    'type': 'bug',
                    'description': match.strip(),
                    'source_file': file_path,
                    'extracted_at': datetime.now().isoformat()
                })
        
        return bugs
    except Exception as e:
        return [{
            'type': 'error',
            'description': f"Failed to read file: {str(e)}",
            'source_file': file_path,
            'extracted_at': datetime.now().isoformat()
        }]

def scan_error_logs():
    """Scan for error logs and recent errors"""
    error_logs = []
    
    # Look for common log files
    log_patterns = [
        '**/*.log',
        '**/logs/*',
        '**/error*.txt',
        '**/ERROR*.txt'
    ]
    
    for pattern in log_patterns:
        for file_path in Path('.').glob(pattern):
            if file_path.is_file() and file_path.stat().st_size < 1024*1024:  # Skip large files
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Look for error patterns
                    error_lines = []
                    for line in content.split('\n'):
                        if any(keyword in line.lower() for keyword in ['error', 'exception', 'failed', 'bug']):
                            error_lines.append(line.strip())
                    
                    if error_lines:
                        error_logs.append({
                            'log_file': str(file_path),
                            'error_lines': error_lines[:10],  # Limit to first 10
                            'extracted_at': datetime.now().isoformat()
                        })
                except:
                    continue
    
    return error_logs

def main():
    """Main bug audit function"""
    print("=== BUG AUDIT ===")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Scan for bug files
    bug_files = scan_bug_files()
    print(f"Found {len(bug_files)} bug-related files")
    
    # Extract bugs from files
    all_bugs = []
    for file_path in bug_files:
        bugs = extract_bugs_from_file(file_path)
        all_bugs.extend(bugs)
    
    # Scan error logs
    error_logs = scan_error_logs()
    print(f"Found {len(error_logs)} error log files")
    
    # Compile audit results
    audit_results = {
        'timestamp': datetime.now().isoformat(),
        'bug_files_found': bug_files,
        'bugs_extracted': all_bugs,
        'error_logs': error_logs,
        'summary': {
            'total_bug_files': len(bug_files),
            'total_bugs_found': len(all_bugs),
            'total_error_logs': len(error_logs)
        }
    }
    
    # Save results
    os.makedirs('reports', exist_ok=True)
    with open('reports/bug_audit.json', 'w') as f:
        json.dump(audit_results, f, indent=2)
    
    print("Bug audit completed")
    print("Results saved to reports/bug_audit.json")
    
    # Print summary
    print(f"\n=== SUMMARY ===")
    print(f"Bug files: {len(bug_files)}")
    print(f"Bugs extracted: {len(all_bugs)}")
    print(f"Error logs: {len(error_logs)}")

if __name__ == "__main__":
    main()
