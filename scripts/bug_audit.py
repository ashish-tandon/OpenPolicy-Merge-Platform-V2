#!/usr/bin/env python3
"""
Bug Audit Tool
Aggregates bugs from multiple sources and links to features/checklist IDs
"""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import defaultdict
import hashlib
import difflib
import argparse
from datetime import datetime


class BugAuditor:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.bugs = []
        self.feature_mapping = {}
        self.checklist_mapping = {}
        
    def load_feature_mapping(self):
        """Load feature mapping from unified feature mapping doc"""
        feature_map_path = self.root_path / "docs/plan/features/FEATURE_MAPPING_UNIFIED.md"
        if feature_map_path.exists():
            print(f"Loading feature mapping from {feature_map_path}")
            with open(feature_map_path, 'r') as f:
                content = f.read()
                # Extract feature IDs and names
                feature_pattern = r'(?:###|##)\s*(\w+-\d+)[:|\s]+(.+?)(?:\n|$)'
                for match in re.finditer(feature_pattern, content):
                    feature_id = match.group(1)
                    feature_name = match.group(2).strip()
                    self.feature_mapping[feature_id] = feature_name
        
    def load_checklist_mapping(self):
        """Load checklist IDs from validation docs"""
        validation_dir = self.root_path / "docs/validation"
        if validation_dir.exists():
            for file_path in validation_dir.glob("*.md"):
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Extract checklist IDs
                    checklist_pattern = r'(\d+(?:\.\d+)*)\.\s+(.+?)(?:\n|$)'
                    for match in re.finditer(checklist_pattern, content):
                        checklist_id = match.group(1)
                        checklist_desc = match.group(2).strip()
                        self.checklist_mapping[checklist_id] = checklist_desc
    
    def fingerprint_bug(self, bug: Dict[str, Any]) -> str:
        """Generate fingerprint for bug deduplication"""
        # Create fingerprint from title + error type + file path
        components = []
        
        if 'title' in bug:
            components.append(bug['title'].lower().strip())
        elif 'message' in bug:
            components.append(bug['message'].lower().strip()[:100])
        
        if 'error_type' in bug:
            components.append(bug['error_type'])
        
        if 'file' in bug:
            components.append(os.path.basename(bug['file']))
        
        if 'stack_trace' in bug and bug['stack_trace']:
            # Extract key stack frames
            stack_lines = bug['stack_trace'].split('\n')[:3]
            components.extend(stack_lines)
        
        fingerprint_str = '|'.join(components)
        return hashlib.md5(fingerprint_str.encode()).hexdigest()
    
    def fuzzy_match_title(self, title1: str, title2: str, threshold: float = 0.8) -> bool:
        """Check if two bug titles are similar"""
        ratio = difflib.SequenceMatcher(None, title1.lower(), title2.lower()).ratio()
        return ratio >= threshold
    
    def deduplicate_bugs(self):
        """Remove duplicate bugs based on fingerprints and fuzzy matching"""
        seen_fingerprints = {}
        seen_titles = []
        unique_bugs = []
        
        for bug in self.bugs:
            fingerprint = self.fingerprint_bug(bug)
            
            # Check fingerprint
            if fingerprint in seen_fingerprints:
                # Merge information
                existing_bug = seen_fingerprints[fingerprint]
                if 'occurrences' not in existing_bug:
                    existing_bug['occurrences'] = 1
                existing_bug['occurrences'] += 1
                continue
            
            # Check fuzzy title match
            bug_title = bug.get('title', bug.get('message', ''))
            is_duplicate = False
            for seen_title, seen_bug in seen_titles:
                if self.fuzzy_match_title(bug_title, seen_title):
                    if 'occurrences' not in seen_bug:
                        seen_bug['occurrences'] = 1
                    seen_bug['occurrences'] += 1
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                seen_fingerprints[fingerprint] = bug
                seen_titles.append((bug_title, bug))
                unique_bugs.append(bug)
        
        self.bugs = unique_bugs
    
    def link_to_features(self, bug: Dict[str, Any]) -> List[str]:
        """Try to link bug to feature IDs"""
        linked_features = []
        
        bug_text = ' '.join([
            str(bug.get('title', '')),
            str(bug.get('message', '')),
            str(bug.get('file', '')),
            str(bug.get('component', ''))
        ]).lower()
        
        # Check for feature keywords
        feature_keywords = {
            'AUTH': ['auth', 'login', 'user', 'permission'],
            'BILL': ['bill', 'legislation'],
            'VOTE': ['vote', 'voting', 'ballot'],
            'MP': ['member', 'mp', 'politician'],
            'DEBATE': ['debate', 'speech', 'hansard'],
            'COMMITTEE': ['committee', 'meeting'],
            'SEARCH': ['search', 'query', 'filter'],
            'UI': ['ui', 'interface', 'display', 'render'],
            'API': ['api', 'endpoint', 'request'],
            'DB': ['database', 'query', 'migration']
        }
        
        for feature_prefix, keywords in feature_keywords.items():
            if any(keyword in bug_text for keyword in keywords):
                # Find matching feature IDs
                for feature_id, feature_name in self.feature_mapping.items():
                    if feature_id.startswith(feature_prefix):
                        linked_features.append(feature_id)
                        break
        
        return linked_features
    
    def link_to_checklist(self, bug: Dict[str, Any]) -> List[str]:
        """Try to link bug to checklist IDs"""
        linked_checklists = []
        
        # Map bug types to checklist sections
        checklist_map = {
            'syntax': ['1.1', '1.2'],  # Code quality
            'import': ['2.1', '2.2'],  # Dependencies
            'type': ['1.3', '1.4'],     # Type safety
            'security': ['3.1', '3.2'], # Security
            'test': ['4.1', '4.2'],     # Testing
            'api': ['5.1', '5.2'],      # API
            'ui': ['6.1', '6.2'],       # UI/UX
            'performance': ['7.1', '7.2'], # Performance
            'database': ['8.1', '8.2']  # Database
        }
        
        bug_type = bug.get('error_type', '').lower()
        bug_text = (bug.get('title', '') + ' ' + bug.get('message', '')).lower()
        
        for key, checklist_ids in checklist_map.items():
            if key in bug_type or key in bug_text:
                linked_checklists.extend(checklist_ids)
        
        return linked_checklists
    
    def collect_from_bandit(self):
        """Collect security issues from Bandit report"""
        bandit_files = [
            self.root_path / "bandit_report.json",
            self.root_path / "bug_reports_20250821_200022/bandit_report.json"
        ]
        
        for bandit_file in bandit_files:
            if bandit_file.exists():
                print(f"Loading Bandit report from {bandit_file}")
                with open(bandit_file, 'r') as f:
                    data = json.load(f)
                    for result in data.get('results', []):
                        bug = {
                            'source': 'bandit',
                            'error_type': 'security',
                            'severity': result.get('issue_severity', 'unknown'),
                            'confidence': result.get('issue_confidence', 'unknown'),
                            'title': result.get('issue_text', 'Security Issue'),
                            'message': result.get('issue_text', ''),
                            'file': result.get('filename', ''),
                            'line': result.get('line_number', 0),
                            'code': result.get('code', ''),
                            'test_id': result.get('test_id', ''),
                            'test_name': result.get('test_name', '')
                        }
                        self.bugs.append(bug)
    
    def collect_from_safety(self):
        """Collect dependency vulnerabilities from Safety report"""
        safety_files = [
            self.root_path / "safety_report.json",
            self.root_path / "bug_reports_20250821_200022/safety_report.json"
        ]
        
        for safety_file in safety_files:
            if safety_file.exists():
                print(f"Loading Safety report from {safety_file}")
                try:
                    with open(safety_file, 'r') as f:
                        content = f.read()
                        # Try to parse as JSON first
                        if content.strip().startswith('[') or content.strip().startswith('{'):
                            data = json.loads(content)
                            if isinstance(data, list):
                                for vuln in data:
                                    bug = {
                                        'source': 'safety',
                                        'error_type': 'vulnerability',
                                        'severity': 'high',
                                        'title': f"Vulnerable dependency: {vuln.get('package', 'unknown')}",
                                        'message': vuln.get('advisory', ''),
                                        'package': vuln.get('package', ''),
                                        'installed_version': vuln.get('installed_version', ''),
                                        'affected_versions': vuln.get('affected_versions', ''),
                                        'cve': vuln.get('cve', '')
                                    }
                                    self.bugs.append(bug)
                        else:
                            # Parse text format
                            vuln_pattern = r'Package:\s*(\S+)\s*CVE:\s*(\S+)\s*Installed Version:\s*(\S+)\s*Advisory:\s*(.+?)(?=Package:|$)'
                            for match in re.finditer(vuln_pattern, content, re.DOTALL):
                                bug = {
                                    'source': 'safety',
                                    'error_type': 'vulnerability',
                                    'severity': 'high',
                                    'title': f"Vulnerable dependency: {match.group(1)}",
                                    'message': match.group(4).strip(),
                                    'package': match.group(1),
                                    'cve': match.group(2),
                                    'installed_version': match.group(3)
                                }
                                self.bugs.append(bug)
                except Exception as e:
                    print(f"Error parsing Safety report {safety_file}: {e}")
    
    def collect_from_logs(self):
        """Collect errors from application logs"""
        log_patterns = [
            "**/*.log",
            "**/logs/*.log",
            "docker-compose*.log"
        ]
        
        error_patterns = [
            r'(?i)error:\s*(.+)',
            r'(?i)exception:\s*(.+)',
            r'(?i)failed:\s*(.+)',
            r'(?i)critical:\s*(.+)',
            r'(?i)fatal:\s*(.+)'
        ]
        
        for pattern in log_patterns:
            for log_file in self.root_path.glob(pattern):
                if log_file.stat().st_size > 10 * 1024 * 1024:  # Skip files > 10MB
                    continue
                
                try:
                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        for error_pattern in error_patterns:
                            for match in re.finditer(error_pattern, content):
                                bug = {
                                    'source': 'logs',
                                    'error_type': 'runtime',
                                    'severity': 'medium',
                                    'title': f"Runtime error in {log_file.name}",
                                    'message': match.group(1)[:500],  # Limit message length
                                    'file': str(log_file.relative_to(self.root_path))
                                }
                                self.bugs.append(bug)
                except Exception as e:
                    print(f"Error reading log file {log_file}: {e}")
    
    def collect_from_issue_trackers(self):
        """Collect from GitHub issues if available"""
        # This would integrate with GitHub API
        # For now, check for local issue files
        issue_files = [
            self.root_path / "docs/bugs/BUGS_RECONCILIATION.md",
            self.root_path / "ISSUES.md",
            self.root_path / "TODO.md"
        ]
        
        for issue_file in issue_files:
            if issue_file.exists():
                print(f"Loading issues from {issue_file}")
                with open(issue_file, 'r') as f:
                    content = f.read()
                    
                    # Extract bug patterns
                    bug_patterns = [
                        r'(?:BUG|Bug|bug):\s*(.+?)(?:\n|$)',
                        r'(?:ERROR|Error):\s*(.+?)(?:\n|$)',
                        r'(?:ISSUE|Issue):\s*(.+?)(?:\n|$)',
                        r'- \[ \]\s*(?:Fix|fix)\s+(.+?)(?:\n|$)'
                    ]
                    
                    for pattern in bug_patterns:
                        for match in re.finditer(pattern, content):
                            bug = {
                                'source': 'issues',
                                'error_type': 'tracked',
                                'severity': 'medium',
                                'title': match.group(1).strip(),
                                'message': match.group(1).strip(),
                                'file': str(issue_file.relative_to(self.root_path))
                            }
                            self.bugs.append(bug)
    
    def collect_from_tests(self):
        """Collect test failures"""
        test_report_patterns = [
            "**/test-results.xml",
            "**/pytest-report.xml",
            "**/jest-results.json",
            "**/.pytest_cache/v/cache/lastfailed"
        ]
        
        for pattern in test_report_patterns:
            for report_file in self.root_path.glob(pattern):
                # Parse test reports based on format
                if report_file.suffix == '.xml':
                    # Parse JUnit XML format
                    pass
                elif report_file.suffix == '.json':
                    # Parse JSON test results
                    try:
                        with open(report_file, 'r') as f:
                            data = json.load(f)
                            # Extract test failures
                    except:
                        pass
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive bug audit report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_bugs': len(self.bugs),
            'by_source': defaultdict(int),
            'by_severity': defaultdict(int),
            'by_type': defaultdict(int),
            'linked_features': defaultdict(list),
            'linked_checklists': defaultdict(list),
            'bugs': []
        }
        
        # Analyze bugs
        for bug in self.bugs:
            # Add feature and checklist links
            bug['linked_features'] = self.link_to_features(bug)
            bug['linked_checklists'] = self.link_to_checklist(bug)
            
            # Update statistics
            report['by_source'][bug.get('source', 'unknown')] += 1
            report['by_severity'][bug.get('severity', 'unknown')] += 1
            report['by_type'][bug.get('error_type', 'unknown')] += 1
            
            for feature_id in bug['linked_features']:
                report['linked_features'][feature_id].append(bug.get('title', ''))
            
            for checklist_id in bug['linked_checklists']:
                report['linked_checklists'][checklist_id].append(bug.get('title', ''))
            
            report['bugs'].append(bug)
        
        # Convert defaultdicts to regular dicts
        report['by_source'] = dict(report['by_source'])
        report['by_severity'] = dict(report['by_severity'])
        report['by_type'] = dict(report['by_type'])
        report['linked_features'] = dict(report['linked_features'])
        report['linked_checklists'] = dict(report['linked_checklists'])
        
        return report
    
    def export_markdown(self, report: Dict[str, Any], output_path: str):
        """Export report as markdown"""
        with open(output_path, 'w') as f:
            f.write("# Bug Audit Report\n\n")
            f.write(f"Generated: {report['generated_at']}\n\n")
            f.write(f"Total Bugs Found: **{report['total_bugs']}**\n\n")
            
            f.write("## Summary\n\n")
            
            f.write("### By Source\n")
            for source, count in sorted(report['by_source'].items()):
                f.write(f"- {source}: {count}\n")
            f.write("\n")
            
            f.write("### By Severity\n")
            severity_order = ['critical', 'high', 'medium', 'low', 'unknown']
            for severity in severity_order:
                if severity in report['by_severity']:
                    f.write(f"- {severity}: {report['by_severity'][severity]}\n")
            f.write("\n")
            
            f.write("### By Type\n")
            for bug_type, count in sorted(report['by_type'].items()):
                f.write(f"- {bug_type}: {count}\n")
            f.write("\n")
            
            f.write("## Feature Impact\n\n")
            if report['linked_features']:
                for feature_id, bugs in sorted(report['linked_features'].items()):
                    feature_name = self.feature_mapping.get(feature_id, 'Unknown Feature')
                    f.write(f"### {feature_id}: {feature_name}\n")
                    f.write(f"Affected by {len(bugs)} bugs:\n")
                    for bug_title in bugs[:5]:  # Show first 5
                        f.write(f"- {bug_title}\n")
                    if len(bugs) > 5:
                        f.write(f"- ... and {len(bugs) - 5} more\n")
                    f.write("\n")
            else:
                f.write("No bugs linked to specific features.\n\n")
            
            f.write("## Checklist Items Affected\n\n")
            if report['linked_checklists']:
                for checklist_id, bugs in sorted(report['linked_checklists'].items()):
                    checklist_desc = self.checklist_mapping.get(checklist_id, 'Unknown Item')
                    f.write(f"### {checklist_id}: {checklist_desc}\n")
                    f.write(f"Related to {len(bugs)} bugs:\n")
                    for bug_title in bugs[:5]:  # Show first 5
                        f.write(f"- {bug_title}\n")
                    if len(bugs) > 5:
                        f.write(f"- ... and {len(bugs) - 5} more\n")
                    f.write("\n")
            else:
                f.write("No bugs linked to checklist items.\n\n")
            
            f.write("## Detailed Bug List\n\n")
            
            # Group by severity
            bugs_by_severity = defaultdict(list)
            for bug in report['bugs']:
                bugs_by_severity[bug.get('severity', 'unknown')].append(bug)
            
            for severity in severity_order:
                if severity in bugs_by_severity:
                    f.write(f"### {severity.upper()} Severity\n\n")
                    for i, bug in enumerate(bugs_by_severity[severity][:20]):  # Limit to 20 per severity
                        f.write(f"#### Bug #{i+1}: {bug.get('title', 'Untitled')}\n")
                        f.write(f"- **Source**: {bug.get('source', 'unknown')}\n")
                        f.write(f"- **Type**: {bug.get('error_type', 'unknown')}\n")
                        if bug.get('file'):
                            f.write(f"- **File**: `{bug['file']}`\n")
                        if bug.get('line'):
                            f.write(f"- **Line**: {bug['line']}\n")
                        if bug.get('message') and bug['message'] != bug.get('title'):
                            f.write(f"- **Details**: {bug['message'][:200]}...\n")
                        if bug.get('linked_features'):
                            f.write(f"- **Linked Features**: {', '.join(bug['linked_features'])}\n")
                        if bug.get('linked_checklists'):
                            f.write(f"- **Checklist Items**: {', '.join(bug['linked_checklists'])}\n")
                        f.write("\n")
                    
                    if len(bugs_by_severity[severity]) > 20:
                        f.write(f"... and {len(bugs_by_severity[severity]) - 20} more {severity} bugs\n\n")


def main():
    parser = argparse.ArgumentParser(description="Audit bugs from multiple sources")
    parser.add_argument("--root", default=".", help="Root directory to analyze")
    parser.add_argument("--output-dir", default="reports", help="Output directory")
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Run audit
    auditor = BugAuditor(args.root)
    
    # Load mappings
    auditor.load_feature_mapping()
    auditor.load_checklist_mapping()
    
    # Collect bugs from all sources
    print("Collecting bugs from various sources...")
    auditor.collect_from_bandit()
    auditor.collect_from_safety()
    auditor.collect_from_logs()
    auditor.collect_from_issue_trackers()
    auditor.collect_from_tests()
    
    print(f"Found {len(auditor.bugs)} bugs before deduplication")
    
    # Deduplicate
    auditor.deduplicate_bugs()
    print(f"Reduced to {len(auditor.bugs)} unique bugs after deduplication")
    
    # Generate report
    report = auditor.generate_report()
    
    # Export
    json_path = output_dir / "BUG_AUDIT.json"
    md_path = output_dir / "BUG_AUDIT.md"
    
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    auditor.export_markdown(report, str(md_path))
    
    print(f"\nBug Audit Complete:")
    print(f"  Total bugs: {report['total_bugs']}")
    print(f"  Reports saved to:")
    print(f"    - {json_path}")
    print(f"    - {md_path}")


if __name__ == "__main__":
    main()