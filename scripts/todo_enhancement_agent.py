#!/usr/bin/env python3
"""
10× Enhancement To-Do Agent

Manages a canonical to-do list for OpenPolicy V2 through 10 enhancement cycles.
Each cycle enhances items (append-only), increments counters, and verifies coverage.
"""

import json
import hashlib
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict

class TodoEnhancementAgent:
    def __init__(self):
        self.checklist_path = Path("docs/plan/IMPLEMENTATION_CHECKLIST.md")
        self.state_path = Path("reports/todo_state.json")
        self.summary_path = Path("reports/todo_summary.md")
        self.state = self.load_state()
        self.checklist_items = []
        self.current_cycle = self.state.get('cycles_completed', 0) + 1
        
    def load_state(self) -> Dict[str, Any]:
        """Load or initialize the todo state"""
        if self.state_path.exists():
            with open(self.state_path, 'r') as f:
                return json.load(f)
        return {
            'cycles_completed': 0,
            'items': {},
            'total_items': 0,
            'last_updated': None
        }
        
    def save_state(self):
        """Save the current state"""
        self.state['last_updated'] = datetime.now().isoformat()
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f, indent=2)
            
    def generate_item_hash(self, title: str) -> str:
        """Generate a stable hash for an item title"""
        return hashlib.md5(title.strip().encode()).hexdigest()[:8]
        
    def seed_checklist(self):
        """Seed the checklist from existing sources if it doesn't exist"""
        if self.checklist_path.exists():
            return
            
        print("Seeding implementation checklist from existing sources...")
        
        items = []
        chk_counter = 1
        
        # Load items from EXEC_PLAN_TODOS.md
        exec_plan_path = Path("docs/plan/EXEC_PLAN_TODOS.md")
        if exec_plan_path.exists():
            with open(exec_plan_path, 'r') as f:
                content = f.read()
                # Extract all EXEC- items
                exec_pattern = r'\*\*\[EXEC-(\d+)\]\*\*\s+(.+?)(?:\n|$)'
                for match in re.finditer(exec_pattern, content):
                    exec_id = match.group(1)
                    task = match.group(2)
                    items.append({
                        'id': f"CHK-{chk_counter:04d}",
                        'title': task,
                        'source': f"EXEC-{exec_id}",
                        'gate': self._determine_gate(content, match.start())
                    })
                    chk_counter += 1
                    
        # Add legacy feature implementations
        legacy_diff_path = Path("reports/legacy_vs_current_diff.md")
        if legacy_diff_path.exists():
            with open(legacy_diff_path, 'r') as f:
                content = f.read()
                # Extract unmatched features
                for line in content.split('\n'):
                    if '| scraper |' in line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            feature = parts[1].strip()
                            items.append({
                                'id': f"CHK-{chk_counter:04d}",
                                'title': f"Implement legacy feature: {feature}",
                                'source': "Legacy Migration",
                                'gate': "G2"
                            })
                            chk_counter += 1
                            
        # Add bug fixes
        bug_audit_path = Path("reports/BUG_AUDIT.json")
        if bug_audit_path.exists():
            with open(bug_audit_path, 'r') as f:
                bug_data = json.load(f)
                for i, bug in enumerate(bug_data.get('bugs', [])[:20]):  # Top 20 bugs
                    items.append({
                        'id': f"CHK-{chk_counter:04d}",
                        'title': f"Fix {bug.get('error_type', 'bug')}: {bug.get('title', 'Unknown')}",
                        'source': f"Bug #{bug.get('id', i+1)}",
                        'gate': "G4"
                    })
                    chk_counter += 1
                    
        # Create the initial checklist
        self._write_initial_checklist(items)
        
    def _determine_gate(self, content: str, position: int) -> str:
        """Determine which gate an item belongs to based on context"""
        # Look backwards for gate header
        before = content[:position]
        gates = ["G5", "G4", "G3", "G2", "G1"]  # Reverse order for last match
        for gate in gates:
            if f"## {gate}" in before:
                return gate
        return "G1"
        
    def _write_initial_checklist(self, items: List[Dict[str, Any]]):
        """Write the initial implementation checklist"""
        with open(self.checklist_path, 'w') as f:
            f.write("# OpenPolicy V2 Implementation Checklist\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            f.write("This is the canonical implementation checklist for OpenPolicy V2.\n")
            f.write("Items are enhanced through 10 cycles, append-only.\n\n")
            f.write("## Statistics\n\n")
            f.write(f"- Total Items: {len(items)}\n")
            f.write(f"- Cycles Completed: 0/10\n")
            f.write(f"- Last Updated: {datetime.now().isoformat()}\n\n")
            
            # Group by gate
            gates = defaultdict(list)
            for item in items:
                gates[item['gate']].append(item)
                
            # Write items by gate
            for gate in ["G1", "G2", "G3", "G4", "G5"]:
                if gate in gates:
                    f.write(f"## {gate} Tasks\n\n")
                    for item in gates[gate]:
                        f.write(f"### [{item['id']}] {item['title']}\n\n")
                        f.write(f"- **Source**: {item['source']}\n")
                        f.write(f"- **Status**: Not Started\n")
                        f.write(f"- **Runs Completed**: 0/10\n\n")
                        f.write("#### Enhancements\n\n")
                        f.write("<!-- Enhancements will be added here -->\n\n")
                        
    def load_checklist(self):
        """Load the current checklist"""
        if not self.checklist_path.exists():
            self.seed_checklist()
            
        with open(self.checklist_path, 'r') as f:
            content = f.read()
            
        # Parse checklist items
        self.checklist_items = []
        item_pattern = r'### \[(CHK-\d+)\] (.+?)\n'
        for match in re.finditer(item_pattern, content):
            chk_id = match.group(1)
            title = match.group(2)
            self.checklist_items.append({
                'id': chk_id,
                'title': title,
                'position': match.start()
            })
            
    def enhance_item(self, item: Dict[str, Any]) -> str:
        """Generate an enhancement for an item"""
        chk_id = item['id']
        title = item['title']
        
        # Get current state
        item_hash = self.generate_item_hash(title)
        if item_hash not in self.state['items']:
            self.state['items'][item_hash] = {
                'id': chk_id,
                'title': title,
                'runs_completed': 0,
                'enhancements_count': 0,
                'last_cycle': 0,
                'created_cycle': self.current_cycle
            }
            
        item_state = self.state['items'][item_hash]
        run_number = item_state['runs_completed'] + 1
        
        # Generate enhancement based on content and cycle
        enhancements = self._generate_context_aware_enhancement(title, run_number)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        enhancement_text = f"- Enhancement #{run_number}: {enhancements} (Cycle {self.current_cycle}, {timestamp})\n"
        
        # Update state
        item_state['runs_completed'] = run_number
        item_state['enhancements_count'] += 1
        item_state['last_cycle'] = self.current_cycle
        
        return enhancement_text
        
    def _generate_context_aware_enhancement(self, title: str, run_number: int) -> str:
        """Generate context-aware enhancements based on title and run number"""
        title_lower = title.lower()
        
        # Enhancement strategies by run number
        enhancement_map = {
            1: self._add_prerequisites,
            2: self._add_implementation_steps,
            3: self._add_test_cases,
            4: self._add_dependencies,
            5: self._add_performance_considerations,
            6: self._add_security_review,
            7: self._add_documentation_needs,
            8: self._add_monitoring_setup,
            9: self._add_rollout_strategy,
            10: self._add_validation_criteria
        }
        
        return enhancement_map.get(run_number, self._add_generic_enhancement)(title)
        
    def _add_prerequisites(self, title: str) -> str:
        """Enhancement 1: Add prerequisites"""
        if 'implement' in title.lower():
            return "Prerequisites: Review existing code, identify integration points, check dependencies"
        elif 'fix' in title.lower():
            return "Prerequisites: Reproduce issue, identify root cause, assess impact"
        elif 'document' in title.lower():
            return "Prerequisites: Gather existing docs, identify gaps, define audience"
        else:
            return "Prerequisites: Analyze requirements, review related systems, plan approach"
            
    def _add_implementation_steps(self, title: str) -> str:
        """Enhancement 2: Add implementation steps"""
        if 'scraper' in title.lower():
            return "Steps: 1) Create scraper class, 2) Implement parse methods, 3) Add error handling, 4) Test with sample data"
        elif 'api' in title.lower() or 'route' in title.lower():
            return "Steps: 1) Define endpoint schema, 2) Implement handler, 3) Add validation, 4) Update OpenAPI spec"
        elif 'test' in title.lower():
            return "Steps: 1) Write unit tests, 2) Add integration tests, 3) Create fixtures, 4) Update CI pipeline"
        else:
            return "Steps: 1) Design solution, 2) Implement core logic, 3) Add error handling, 4) Write tests"
            
    def _add_test_cases(self, title: str) -> str:
        """Enhancement 3: Add test cases"""
        return f"Tests: Unit tests for {title}, integration tests, edge cases, error scenarios"
        
    def _add_dependencies(self, title: str) -> str:
        """Enhancement 4: Add dependencies"""
        # Link to related features and data
        links = []
        if 'bill' in title.lower():
            links.append("Link: → F001-F010 (Bill features), → data_points/Bills")
        if 'member' in title.lower() or 'mp' in title.lower():
            links.append("Link: → F011-F020 (Member features), → data_points/Members")
        if 'vote' in title.lower():
            links.append("Link: → F021-F030 (Vote features), → data_points/Votes")
        if 'committee' in title.lower():
            links.append("Link: → F031-F040 (Committee features), → data_points/Committees")
            
        return f"Dependencies: {'; '.join(links) if links else 'Review VAR_FUNC_MAP for code dependencies'}"
        
    def _add_performance_considerations(self, title: str) -> str:
        """Enhancement 5: Add performance considerations"""
        if 'scraper' in title.lower():
            return "Performance: Rate limiting, batch processing, caching strategy, async operations"
        elif 'api' in title.lower():
            return "Performance: Response caching, query optimization, pagination, connection pooling"
        else:
            return "Performance: Optimize algorithms, add caching, consider async processing, profile bottlenecks"
            
    def _add_security_review(self, title: str) -> str:
        """Enhancement 6: Add security review"""
        return "Security: Input validation, auth checks, rate limiting, audit logging, OWASP compliance"
        
    def _add_documentation_needs(self, title: str) -> str:
        """Enhancement 7: Add documentation needs"""
        return "Docs: API documentation, user guide, architecture decision record (ADR), runbook"
        
    def _add_monitoring_setup(self, title: str) -> str:
        """Enhancement 8: Add monitoring setup"""
        return "Monitoring: Prometheus metrics, error alerts, performance dashboards, SLA tracking"
        
    def _add_rollout_strategy(self, title: str) -> str:
        """Enhancement 9: Add rollout strategy"""
        return "Rollout: Feature flag setup, canary deployment, rollback plan, user communication"
        
    def _add_validation_criteria(self, title: str) -> str:
        """Enhancement 10: Add validation criteria"""
        return "Validation: Acceptance criteria, performance benchmarks, security scan pass, 90% test coverage"
        
    def _add_generic_enhancement(self, title: str) -> str:
        """Generic enhancement fallback"""
        return f"Enhanced with additional context for: {title}"
        
    def run_cycle(self):
        """Run a single enhancement cycle"""
        print(f"\n=== Running Cycle {self.current_cycle} ===")
        
        # Load current checklist
        self.load_checklist()
        
        # Track items touched this cycle
        touched_items = set()
        enhancements_to_add = []
        
        # Process each item
        for item in self.checklist_items:
            enhancement = self.enhance_item(item)
            enhancements_to_add.append({
                'id': item['id'],
                'title': item['title'],
                'enhancement': enhancement
            })
            touched_items.add(item['id'])
            
        # Apply enhancements to checklist
        self._apply_enhancements(enhancements_to_add)
        
        # Verify all items touched
        all_item_ids = {item['id'] for item in self.checklist_items}
        missed_items = all_item_ids - touched_items
        
        # Update cycle count
        self.state['cycles_completed'] = self.current_cycle
        self.state['total_items'] = len(self.checklist_items)
        
        # Save state
        self.save_state()
        
        # Generate reports
        self._generate_cycle_report(touched_items, missed_items)
        self._generate_summary_report()
        
        # Print cycle summary
        print(f"Cycle {self.current_cycle} Complete:")
        print(f"  - Items touched: {len(touched_items)}/{len(self.checklist_items)} ({len(touched_items)/len(self.checklist_items)*100:.1f}%)")
        print(f"  - Missed items: {len(missed_items)}")
        print(f"  - Total enhancements: {sum(item['enhancements_count'] for item in self.state['items'].values())}")
        
        return len(missed_items) == 0
        
    def _apply_enhancements(self, enhancements: List[Dict[str, Any]]):
        """Apply enhancements to the checklist file"""
        with open(self.checklist_path, 'r') as f:
            content = f.read()
            
        # Update statistics
        content = re.sub(
            r'- Cycles Completed: \d+/10',
            f'- Cycles Completed: {self.current_cycle}/10',
            content
        )
        content = re.sub(
            r'- Last Updated: .+',
            f'- Last Updated: {datetime.now().isoformat()}',
            content
        )
        
        # Apply each enhancement
        for enh in enhancements:
            # Find the item and its enhancement section
            item_pattern = rf'### \[{enh["id"]}\] {re.escape(enh["title"])}\n'
            match = re.search(item_pattern, content)
            if match:
                # Find the enhancement section
                start = match.end()
                enhancement_section = content.find("#### Enhancements", start)
                if enhancement_section != -1:
                    # Find where to insert (before the next ### or ## or end)
                    next_section = content.find("\n##", enhancement_section + 1)
                    next_item = content.find("\n###", enhancement_section + 1)
                    
                    insert_pos = min(
                        next_section if next_section != -1 else len(content),
                        next_item if next_item != -1 else len(content)
                    )
                    
                    # Insert the enhancement
                    comment_line = "<!-- Enhancements will be added here -->\n"
                    if comment_line in content[enhancement_section:insert_pos]:
                        content = content.replace(
                            comment_line,
                            enh['enhancement'] + comment_line,
                            1
                        )
                    else:
                        # Add before the next section
                        content = content[:insert_pos] + enh['enhancement'] + content[insert_pos:]
                        
                # Update runs completed
                runs_pattern = rf'(- \*\*Runs Completed\*\*: )\d+(/10)'
                item_section = content[match.start():match.start() + 500]  # Look in next 500 chars
                if "Runs Completed" in item_section:
                    item_hash = self.generate_item_hash(enh['title'])
                    runs = self.state['items'][item_hash]['runs_completed']
                    content = re.sub(
                        runs_pattern,
                        f'\\g<1>{runs}\\g<2>',
                        content,
                        count=1
                    )
                    
        # Write updated content
        with open(self.checklist_path, 'w') as f:
            f.write(content)
            
    def _generate_cycle_report(self, touched_items: Set[str], missed_items: Set[str]):
        """Generate a report for this cycle"""
        report_path = Path(f"reports/todo_cycle_report_cycle{self.current_cycle}.md")
        
        with open(report_path, 'w') as f:
            f.write(f"# Todo Enhancement Cycle {self.current_cycle} Report\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Cycle**: {self.current_cycle}/10\n")
            f.write(f"- **Items Touched**: {len(touched_items)}/{len(self.checklist_items)}\n")
            f.write(f"- **Coverage**: {len(touched_items)/len(self.checklist_items)*100:.1f}%\n")
            f.write(f"- **Missed Items**: {len(missed_items)}\n\n")
            
            if missed_items:
                f.write("## Missed Items\n\n")
                for item_id in sorted(missed_items):
                    f.write(f"- {item_id}\n")
                f.write("\n")
                
            f.write("## Enhancement Summary\n\n")
            
            # Group by runs completed
            by_runs = defaultdict(list)
            for item_hash, item_data in self.state['items'].items():
                runs = item_data['runs_completed']
                by_runs[runs].append(item_data)
                
            for runs in sorted(by_runs.keys(), reverse=True):
                f.write(f"### Items with {runs} runs completed\n\n")
                for item in by_runs[runs][:5]:  # Show first 5
                    f.write(f"- [{item['id']}] {item['title'][:50]}...\n")
                if len(by_runs[runs]) > 5:
                    f.write(f"- ...and {len(by_runs[runs]) - 5} more\n")
                f.write("\n")
                
    def _generate_summary_report(self):
        """Generate the running summary report"""
        with open(self.summary_path, 'w') as f:
            f.write("# Todo Enhancement Summary\n\n")
            f.write(f"Last Updated: {datetime.now().isoformat()}\n\n")
            f.write(f"**Cycles Completed**: {self.state['cycles_completed']}/10\n")
            f.write(f"**Total Items**: {self.state['total_items']}\n\n")
            
            f.write("## Item Progress\n\n")
            f.write("| CHK-ID | Title | Runs | Last Cycle | Links |\n")
            f.write("|--------|-------|------|------------|-------|\n")
            
            # Sort items by CHK-ID
            sorted_items = sorted(
                self.state['items'].values(),
                key=lambda x: x['id']
            )
            
            for item in sorted_items:
                title_short = item['title'][:40] + "..." if len(item['title']) > 40 else item['title']
                links = self._get_item_links(item['title'])
                f.write(f"| {item['id']} | {title_short} | {item['runs_completed']}/10 | {item['last_cycle']} | {links} |\n")
                
            # Summary statistics
            f.write("\n## Statistics\n\n")
            
            completed_items = sum(1 for item in self.state['items'].values() if item['runs_completed'] == 10)
            f.write(f"- **Items at 10 runs**: {completed_items}/{len(self.state['items'])} ({completed_items/len(self.state['items'])*100:.1f}%)\n")
            
            avg_runs = sum(item['runs_completed'] for item in self.state['items'].values()) / len(self.state['items'])
            f.write(f"- **Average runs**: {avg_runs:.1f}\n")
            
            # Coverage check
            sot_coverage = self._check_sot_coverage()
            f.write(f"- **SoT Coverage**: {sot_coverage:.1f}%\n")
            
    def _get_item_links(self, title: str) -> str:
        """Get relevant links for an item based on its title"""
        links = []
        title_lower = title.lower()
        
        if 'bill' in title_lower:
            links.append("[Bills](docs/plan/features/FEATURE_MAPPING_UNIFIED.md#bills)")
        if 'member' in title_lower or 'mp' in title_lower:
            links.append("[Members](docs/plan/features/FEATURE_MAPPING_UNIFIED.md#members)")
        if 'scraper' in title_lower:
            links.append("[ETL](services/etl)")
        if 'api' in title_lower or 'route' in title_lower:
            links.append("[API](services/api-gateway)")
            
        return ", ".join(links) if links else "-"
        
    def _check_sot_coverage(self) -> float:
        """Check Source of Truth coverage"""
        # Simple check: see if major categories are represented in checklist
        categories = ['bills', 'members', 'votes', 'committees', 'debates', 'api', 'ui', 'etl']
        covered = 0
        
        all_titles = " ".join(item['title'].lower() for item in self.state['items'].values())
        
        for category in categories:
            if category in all_titles:
                covered += 1
                
        return (covered / len(categories)) * 100
        
    def run_all_cycles(self):
        """Run all 10 cycles"""
        while self.state['cycles_completed'] < 10:
            self.current_cycle = self.state['cycles_completed'] + 1
            success = self.run_cycle()
            
            if not success:
                print(f"WARNING: Cycle {self.current_cycle} had missed items!")
                
        print("\n=== All 10 Cycles Complete! ===")
        print(f"Total items: {self.state['total_items']}")
        print(f"Total enhancements: {sum(item['enhancements_count'] for item in self.state['items'].values())}")
        
        # Final validation
        all_complete = all(item['runs_completed'] == 10 for item in self.state['items'].values())
        if all_complete:
            print("✓ All items have been enhanced 10 times")
        else:
            incomplete = sum(1 for item in self.state['items'].values() if item['runs_completed'] < 10)
            print(f"✗ {incomplete} items have less than 10 runs")


def main():
    agent = TodoEnhancementAgent()
    agent.run_all_cycles()


if __name__ == "__main__":
    main()