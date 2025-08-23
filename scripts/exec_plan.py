#!/usr/bin/env python3
"""
Execution Plan Generator

Generates comprehensive to-do lists grouped by Gates:
- G1: Structure/Index
- G2: Parity
- G3: Architecture Harmony
- G4: Test Strategy
- G5: Release Readiness
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict
from datetime import datetime

class ExecutionPlanGenerator:
    def __init__(self):
        self.todos = defaultdict(list)
        self.checklist_counter = 0
        self.data_sources = {}
        
    def load_all_data(self):
        """Load all available analysis data"""
        data_files = {
            'var_func_map': 'reports/VAR_FUNC_MAP.json',
            'bug_audit': 'reports/BUG_AUDIT.json',
            'env_audit': 'reports/ENVIRONMENT_AUDIT.json',
            'data_journey': 'reports/DATA_JOURNEY_MAP.json',
            'flow_design': 'reports/flow_design.json',
            'routing': 'reports/routing_realignment.json',
            'architecture': 'docs/plan/architecture_synthesis.json',
            'legacy_diff': 'reports/legacy_vs_current_diff.md'
        }
        
        for key, file_path in data_files.items():
            path = Path(file_path)
            if path.exists():
                if file_path.endswith('.json'):
                    with open(path, 'r') as f:
                        self.data_sources[key] = json.load(f)
                else:
                    with open(path, 'r') as f:
                        self.data_sources[key] = f.read()
            else:
                self.data_sources[key] = None
                
    def generate_gate1_todos(self):
        """G1: Structure/Index - File organization, naming, documentation"""
        gate = "G1: Structure/Index"
        
        # Directory structure tasks
        structure_tasks = [
            "Audit and standardize directory structure across all services",
            "Create consistent naming conventions for files and directories",
            "Implement monorepo structure with clear boundaries",
            "Establish shared libraries location and structure",
            "Define service boundary rules and dependencies",
            "Create service-specific README files with consistent format",
            "Implement consistent .gitignore patterns across services",
            "Create index files for each major directory",
            "Establish import path conventions and aliases",
            "Document directory ownership and responsibility matrix"
        ]
        
        # Documentation tasks
        doc_tasks = [
            "Create comprehensive API documentation for all endpoints",
            "Document all environment variables and configuration",
            "Create architecture decision records (ADRs) for key decisions",
            "Document data flow diagrams for all major features",
            "Create onboarding documentation for new developers",
            "Document deployment procedures for each service",
            "Create troubleshooting guides for common issues",
            "Document security policies and procedures",
            "Create performance tuning documentation",
            "Document disaster recovery procedures"
        ]
        
        # Code organization tasks
        code_tasks = [
            "Refactor duplicate code into shared libraries",
            "Standardize error handling across all services",
            "Implement consistent logging format and levels",
            "Create shared type definitions for cross-service communication",
            "Standardize API response formats",
            "Implement consistent validation patterns",
            "Create shared utility functions library",
            "Standardize configuration management approach",
            "Implement consistent dependency injection patterns",
            "Create shared constants and enums"
        ]
        
        # Based on var_func_map analysis
        if self.data_sources.get('var_func_map'):
            hotspots = self.data_sources['var_func_map'].get('hotspots', {})
            
            # Add tasks for high-degree nodes
            for category, items in hotspots.items():
                if isinstance(items, list):
                    for item in items[:5]:  # Top 5 hotspots
                        if isinstance(item, dict) and 'name' in item:
                            degree = item.get('degree', item.get('count', 'many'))
                            self.add_todo(gate, f"Refactor high-usage {category}: {item['name']} (used {degree} times)")
                    
        # Based on routing analysis
        if self.data_sources.get('routing'):
            routing = self.data_sources['routing']
            orphans = routing.get('realignment_needs', {})
            
            for orphan in orphans.get('orphan_routes', [])[:10]:
                self.add_todo(gate, f"Document or remove orphan route: {orphan['path']}")
                
        # Add all predefined tasks
        for task in structure_tasks + doc_tasks + code_tasks:
            self.add_todo(gate, task)
            
    def generate_gate2_todos(self):
        """G2: Parity - Feature completeness, legacy migration"""
        gate = "G2: Parity"
        
        # Feature parity tasks
        feature_tasks = [
            "Complete migration of all legacy bill tracking features",
            "Implement full member profile functionality",
            "Migrate voting record analysis features",
            "Implement committee tracking and reports",
            "Complete constituency mapping features",
            "Migrate debate transcription features",
            "Implement notification system for bill updates",
            "Complete search functionality across all entities",
            "Migrate data export features",
            "Implement API versioning for backward compatibility"
        ]
        
        # Data migration tasks
        data_tasks = [
            "Migrate all historical bill data",
            "Transfer member voting records",
            "Import committee membership history",
            "Migrate debate transcripts archive",
            "Transfer constituency boundary data",
            "Import historical session data",
            "Migrate user accounts and preferences",
            "Transfer saved searches and alerts",
            "Import analytics and usage data",
            "Migrate third-party integrations"
        ]
        
        # Based on legacy_diff analysis
        if self.data_sources.get('legacy_diff'):
            # Parse legacy diff to extract unmatched features
            diff_content = self.data_sources['legacy_diff']
            if "Unmatched Legacy Features" in diff_content:
                lines = diff_content.split('\n')
                for i, line in enumerate(lines):
                    if line.strip().startswith('- ') and 'legacy' in line.lower():
                        feature = line.strip('- ')
                        self.add_todo(gate, f"Implement legacy feature: {feature}")
                        
        # Based on data journey analysis
        if self.data_sources.get('data_journey'):
            journeys = self.data_sources['data_journey'].get('data_points', [])
            if isinstance(journeys, list):
                for journey in journeys:
                    if isinstance(journey, dict):
                        entity = journey.get('data_point', 'Unknown')
                        completeness = journey.get('completeness', {})
                        for stage, complete in completeness.items():
                            if not complete:
                                self.add_todo(gate, f"Complete {stage} implementation for {entity}")
                        
        # Add all predefined tasks
        for task in feature_tasks + data_tasks:
            self.add_todo(gate, task)
            
    def generate_gate3_todos(self):
        """G3: Architecture Harmony - Consistency, patterns, best practices"""
        gate = "G3: Architecture Harmony"
        
        # Architecture alignment tasks
        arch_tasks = [
            "Implement consistent microservice communication patterns",
            "Standardize service discovery and registration",
            "Implement circuit breaker pattern for all external calls",
            "Create shared authentication/authorization service",
            "Implement distributed tracing across all services",
            "Standardize health check endpoints",
            "Implement consistent caching strategy",
            "Create shared message queue patterns",
            "Standardize database connection pooling",
            "Implement consistent rate limiting"
        ]
        
        # Technology standardization
        tech_tasks = [
            "Upgrade all services to latest framework versions",
            "Standardize Node.js version across services",
            "Implement consistent TypeScript configuration",
            "Standardize linting and formatting rules",
            "Upgrade all dependencies to latest stable versions",
            "Implement consistent build processes",
            "Standardize Docker base images",
            "Implement consistent logging libraries",
            "Standardize monitoring and metrics collection",
            "Implement consistent error tracking"
        ]
        
        # Based on architecture synthesis
        if self.data_sources.get('architecture'):
            arch_data = self.data_sources['architecture']
            alignment = arch_data.get('alignment_delta', {})
            
            for gap in alignment.get('gaps', []):
                self.add_todo(gate, f"Address architecture gap: {gap}")
                
            for risk in alignment.get('risks', []):
                self.add_todo(gate, f"Mitigate architecture risk: {risk}")
                
        # Performance optimization
        perf_tasks = [
            "Implement database query optimization",
            "Add caching layers for frequently accessed data",
            "Optimize API response payloads",
            "Implement pagination for all list endpoints",
            "Add database indexing strategy",
            "Implement connection pooling optimization",
            "Add CDN for static assets",
            "Implement image optimization pipeline",
            "Add response compression",
            "Implement lazy loading strategies"
        ]
        
        # Add all predefined tasks
        for task in arch_tasks + tech_tasks + perf_tasks:
            self.add_todo(gate, task)
            
    def generate_gate4_todos(self):
        """G4: Test Strategy - Testing, quality assurance, monitoring"""
        gate = "G4: Test Strategy"
        
        # Testing infrastructure
        test_infra_tasks = [
            "Set up comprehensive unit test suites for all services",
            "Implement integration testing framework",
            "Create end-to-end test automation",
            "Set up performance testing infrastructure",
            "Implement security testing automation",
            "Create load testing scenarios",
            "Set up API contract testing",
            "Implement visual regression testing for UI",
            "Create smoke test suites",
            "Set up continuous testing in CI/CD"
        ]
        
        # Test coverage tasks
        coverage_tasks = [
            "Achieve 80% code coverage for critical services",
            "Write tests for all API endpoints",
            "Create test cases for error scenarios",
            "Implement tests for edge cases",
            "Write tests for data validation logic",
            "Create tests for authentication flows",
            "Implement tests for rate limiting",
            "Write tests for caching behavior",
            "Create tests for database transactions",
            "Implement tests for message queue processing"
        ]
        
        # Based on bug audit
        if self.data_sources.get('bug_audit'):
            bugs = self.data_sources['bug_audit'].get('bugs', [])
            
            # Group bugs by type
            bug_types = defaultdict(int)
            for bug in bugs:
                bug_types[bug.get('error_type', 'unknown')] += 1
                
            for bug_type, count in sorted(bug_types.items(), key=lambda x: x[1], reverse=True):
                self.add_todo(gate, f"Create tests to prevent {bug_type} bugs (found {count} instances)")
                
        # Monitoring tasks
        monitoring_tasks = [
            "Implement application performance monitoring",
            "Set up error tracking and alerting",
            "Create custom metrics dashboards",
            "Implement log aggregation and analysis",
            "Set up uptime monitoring",
            "Create SLA tracking dashboards",
            "Implement user experience monitoring",
            "Set up database performance monitoring",
            "Create API usage analytics",
            "Implement cost monitoring and optimization"
        ]
        
        # Add all predefined tasks
        for task in test_infra_tasks + coverage_tasks + monitoring_tasks:
            self.add_todo(gate, task)
            
    def generate_gate5_todos(self):
        """G5: Release Readiness - Deployment, operations, maintenance"""
        gate = "G5: Release Readiness"
        
        # Deployment tasks
        deploy_tasks = [
            "Create production deployment pipelines",
            "Implement blue-green deployment strategy",
            "Set up rollback procedures",
            "Create deployment smoke tests",
            "Implement feature flags for gradual rollout",
            "Set up canary deployment capability",
            "Create deployment runbooks",
            "Implement zero-downtime deployment",
            "Set up deployment monitoring",
            "Create deployment approval workflows"
        ]
        
        # Operations tasks
        ops_tasks = [
            "Create operational runbooks for all services",
            "Implement automated backup procedures",
            "Set up disaster recovery processes",
            "Create incident response procedures",
            "Implement automated scaling policies",
            "Set up security scanning in CI/CD",
            "Create operational dashboards",
            "Implement automated certificate renewal",
            "Set up compliance monitoring",
            "Create capacity planning processes"
        ]
        
        # Based on environment audit
        if self.data_sources.get('env_audit'):
            env_data = self.data_sources['env_audit']
            
            # Add tasks for unhealthy services
            services = env_data.get('services', {})
            if isinstance(services, dict):
                for service, status in services.items():
                    if isinstance(status, dict) and status.get('status') != 'running':
                        self.add_todo(gate, f"Fix and ensure {service} service is production-ready")
                    
            # Add tasks for missing health checks
            health_checks = env_data.get('health_checks', [])
            if isinstance(health_checks, list):
                for health in health_checks:
                    if isinstance(health, dict) and not health.get('healthy', False):
                        service = health.get('service', 'Unknown')
                        self.add_todo(gate, f"Implement proper health check for {service}")
            elif isinstance(health_checks, dict):
                for service, health in health_checks.items():
                    if isinstance(health, dict) and not health.get('healthy', False):
                        self.add_todo(gate, f"Implement proper health check for {service}")
                    
        # Documentation tasks
        doc_tasks = [
            "Create production deployment documentation",
            "Document rollback procedures",
            "Create troubleshooting guides",
            "Document monitoring and alerting setup",
            "Create security incident response plan",
            "Document backup and recovery procedures",
            "Create performance tuning guide",
            "Document scaling procedures",
            "Create cost optimization guide",
            "Document compliance requirements"
        ]
        
        # Add all predefined tasks
        for task in deploy_tasks + ops_tasks + doc_tasks:
            self.add_todo(gate, task)
            
    def add_todo(self, gate: str, task: str, priority: str = "medium"):
        """Add a todo item with proper formatting"""
        self.checklist_counter += 1
        todo = {
            'id': f"EXEC-{self.checklist_counter:04d}",
            'gate': gate,
            'task': task,
            'priority': priority,
            'status': 'pending',
            'dependencies': [],
            'estimated_effort': 'TBD',
            'assigned_to': 'TBD'
        }
        self.todos[gate].append(todo)
        
    def generate_crosslinks(self):
        """Generate crosslinks between related todos"""
        # Link testing todos to bug fixes
        test_todos = [t for todos in self.todos.values() for t in todos if 'test' in t['task'].lower()]
        bug_todos = [t for todos in self.todos.values() for t in todos if 'bug' in t['task'].lower() or 'fix' in t['task'].lower()]
        
        for test_todo in test_todos[:10]:  # Limit crosslinks
            for bug_todo in bug_todos[:5]:
                if any(word in test_todo['task'].lower() for word in bug_todo['task'].lower().split()):
                    test_todo['dependencies'].append(bug_todo['id'])
                    
    def export_execution_plan(self):
        """Export the execution plan"""
        # Generate all gate todos
        self.generate_gate1_todos()
        self.generate_gate2_todos()
        self.generate_gate3_todos()
        self.generate_gate4_todos()
        self.generate_gate5_todos()
        self.generate_crosslinks()
        
        # Create summary statistics
        summary = {
            'total_todos': self.checklist_counter,
            'by_gate': {gate: len(todos) for gate, todos in self.todos.items()},
            'generated_at': datetime.now().isoformat(),
            'data_sources': list(self.data_sources.keys())
        }
        
        # Export JSON
        output = {
            'summary': summary,
            'todos': dict(self.todos)
        }
        
        with open('reports/execution_plan.json', 'w') as f:
            json.dump(output, f, indent=2)
            
        # Generate markdown
        self._generate_markdown_report(summary)
        
        return summary
        
    def _generate_markdown_report(self, summary: Dict[str, Any]):
        """Generate markdown execution plan"""
        with open('docs/plan/EXEC_PLAN_TODOS.md', 'w') as f:
            f.write("# OpenPolicy V2 Execution Plan\n\n")
            f.write("## Executive Summary\n\n")
            f.write(f"- **Total TODOs**: {summary['total_todos']}\n")
            f.write(f"- **Generated**: {summary['generated_at']}\n")
            f.write("- **Gates**:\n")
            for gate, count in summary['by_gate'].items():
                f.write(f"  - {gate}: {count} tasks\n")
            f.write("\n")
            
            # Write detailed todos by gate
            for gate, todos in self.todos.items():
                f.write(f"## {gate}\n\n")
                f.write(f"**Total Tasks**: {len(todos)}\n\n")
                
                # Group by priority
                priority_groups = defaultdict(list)
                for todo in todos:
                    priority_groups[todo['priority']].append(todo)
                    
                for priority in ['critical', 'high', 'medium', 'low']:
                    if priority in priority_groups:
                        f.write(f"### {priority.capitalize()} Priority\n\n")
                        for todo in priority_groups[priority]:
                            f.write(f"- **[{todo['id']}]** {todo['task']}\n")
                            if todo['dependencies']:
                                f.write(f"  - Dependencies: {', '.join(todo['dependencies'])}\n")
                        f.write("\n")
                        
            # Write implementation strategy
            f.write("## Implementation Strategy\n\n")
            f.write("### Phase 1: Foundation (Gates 1-2)\n")
            f.write("1. Establish consistent structure and documentation\n")
            f.write("2. Achieve feature parity with legacy system\n")
            f.write("3. Complete data migration\n\n")
            
            f.write("### Phase 2: Optimization (Gate 3)\n")
            f.write("1. Align architecture with best practices\n")
            f.write("2. Optimize performance and scalability\n")
            f.write("3. Standardize technology stack\n\n")
            
            f.write("### Phase 3: Quality (Gate 4)\n")
            f.write("1. Implement comprehensive testing\n")
            f.write("2. Set up monitoring and alerting\n")
            f.write("3. Achieve quality metrics\n\n")
            
            f.write("### Phase 4: Production (Gate 5)\n")
            f.write("1. Prepare for production deployment\n")
            f.write("2. Implement operational procedures\n")
            f.write("3. Complete documentation\n\n")
            
            # Write success criteria
            f.write("## Success Criteria\n\n")
            f.write("- **G1**: All code organized, documented, and indexed\n")
            f.write("- **G2**: 100% feature parity with legacy system\n")
            f.write("- **G3**: Architecture aligned with future state vision\n")
            f.write("- **G4**: 80%+ test coverage, all critical paths tested\n")
            f.write("- **G5**: Production-ready with full operational support\n\n")
            
            # Write risk mitigation
            f.write("## Risk Mitigation\n\n")
            f.write("1. **Scope Creep**: Strictly prioritize tasks by gate\n")
            f.write("2. **Technical Debt**: Address incrementally through gates\n")
            f.write("3. **Resource Constraints**: Focus on automation and tooling\n")
            f.write("4. **Quality Issues**: Gate 4 ensures comprehensive testing\n")
            f.write("5. **Operational Risks**: Gate 5 ensures production readiness\n")


def main():
    generator = ExecutionPlanGenerator()
    
    print("Loading all analysis data...")
    generator.load_all_data()
    
    print("Generating execution plan...")
    summary = generator.export_execution_plan()
    
    print(f"✓ Generated {summary['total_todos']} TODO items")
    print("✓ TODO breakdown by gate:")
    for gate, count in summary['by_gate'].items():
        print(f"  - {gate}: {count} tasks")
    print("✓ Report saved to docs/plan/EXEC_PLAN_TODOS.md")


if __name__ == "__main__":
    main()