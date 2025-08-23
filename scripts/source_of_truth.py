#!/usr/bin/env python3
"""
Source of Truth Document Generator

Creates the comprehensive OpenPolicy V2 Source of Truth document
with Alignment Delta and Crosslinks Appendix sections
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict
from datetime import datetime

class SourceOfTruthGenerator:
    def __init__(self):
        self.data_sources = {}
        self.alignment_delta = {}
        self.crosslinks = defaultdict(set)
        self.document_sections = []
        
    def load_all_reports(self):
        """Load all generated reports and analysis data"""
        report_files = {
            'var_func_map': ('reports/VAR_FUNC_MAP.json', 'json'),
            'bug_audit': ('reports/BUG_AUDIT.json', 'json'),
            'env_audit': ('reports/ENVIRONMENT_AUDIT.json', 'json'),
            'data_journey': ('reports/DATA_JOURNEY_MAP.json', 'json'),
            'flow_design': ('reports/flow_design.json', 'json'),
            'routing': ('reports/routing_realignment.json', 'json'),
            'architecture': ('docs/plan/architecture_synthesis.json', 'json'),
            'execution_plan': ('reports/execution_plan.json', 'json'),
            'feature_mapping': ('docs/plan/features/FEATURE_MAPPING_UNIFIED.md', 'text'),
            'legacy_diff': ('reports/legacy_vs_current_diff.md', 'text'),
            'flow_design_doc': ('docs/plan/FLOW_DESIGN.md', 'text'),
            'routing_doc': ('docs/plan/ROUTING_REALIGNMENT.md', 'text'),
            'arch_proposal': ('docs/plan/NEW_ARCHITECTURE_PROPOSAL.md', 'text'),
            'exec_plan_doc': ('docs/plan/EXEC_PLAN_TODOS.md', 'text')
        }
        
        for key, (file_path, file_type) in report_files.items():
            path = Path(file_path)
            if path.exists():
                with open(path, 'r') as f:
                    if file_type == 'json':
                        self.data_sources[key] = json.load(f)
                    else:
                        self.data_sources[key] = f.read()
            else:
                print(f"Warning: {file_path} not found")
                self.data_sources[key] = None
                
    def calculate_alignment_delta(self):
        """Calculate comprehensive alignment delta across all dimensions"""
        self.alignment_delta = {
            'architecture': self._calc_architecture_alignment(),
            'features': self._calc_feature_alignment(),
            'data_flow': self._calc_data_flow_alignment(),
            'routing': self._calc_routing_alignment(),
            'quality': self._calc_quality_alignment(),
            'operations': self._calc_operations_alignment()
        }
        
    def _calc_architecture_alignment(self) -> Dict[str, Any]:
        """Calculate architecture alignment delta"""
        if not self.data_sources.get('architecture'):
            return {'score': 0, 'gaps': ['Architecture data not available']}
            
        arch_data = self.data_sources['architecture']
        alignment = arch_data.get('alignment_delta', {})
        
        return {
            'score': alignment.get('alignment_score', 0),
            'gaps': alignment.get('gaps', []),
            'risks': alignment.get('risks', []),
            'opportunities': alignment.get('opportunities', []),
            'phase': arch_data.get('proposed_architecture', {}).get('transformation_phases', {}).get('current_phase', 'Unknown')
        }
        
    def _calc_feature_alignment(self) -> Dict[str, Any]:
        """Calculate feature alignment between legacy and current"""
        if not self.data_sources.get('flow_design'):
            return {'score': 0, 'gaps': ['Flow design data not available']}
            
        flow_data = self.data_sources['flow_design']
        legacy_diff = flow_data.get('legacy_vs_current_diff', {})
        
        total_legacy = len(legacy_diff.get('legacy_features', []))
        matched = len(legacy_diff.get('matched_features', []))
        score = (matched / total_legacy * 100) if total_legacy > 0 else 0
        
        return {
            'score': score,
            'total_legacy_features': total_legacy,
            'matched_features': matched,
            'unmatched_features': len(legacy_diff.get('unmatched_features', [])),
            'gaps': [f['name'] for f in legacy_diff.get('unmatched_features', [])[:10]]  # Top 10 gaps
        }
        
    def _calc_data_flow_alignment(self) -> Dict[str, Any]:
        """Calculate data flow completeness"""
        if not self.data_sources.get('data_journey'):
            return {'score': 0, 'gaps': ['Data journey data not available']}
            
        journey_data = self.data_sources['data_journey']
        summary = journey_data.get('summary', {})
        
        return {
            'score': summary.get('average_completeness', 0),
            'complete_journeys': summary.get('complete_journeys', 0),
            'total_data_points': summary.get('data_points_mapped', 0),
            'gaps': self._extract_data_gaps(journey_data)
        }
        
    def _extract_data_gaps(self, journey_data: Dict[str, Any]) -> List[str]:
        """Extract specific data flow gaps"""
        gaps = []
        data_points = journey_data.get('data_points', [])
        if isinstance(data_points, list):
            for journey in data_points:
                if isinstance(journey, dict):
                    entity = journey.get('data_point', 'Unknown')
                    completeness = journey.get('completeness', {})
                    if isinstance(completeness, dict):
                        for stage, complete in completeness.items():
                            if not complete:
                                gaps.append(f"{entity}: {stage} not implemented")
        return gaps[:10]  # Top 10 gaps
        
    def _calc_routing_alignment(self) -> Dict[str, Any]:
        """Calculate routing alignment between API and UI"""
        if not self.data_sources.get('routing'):
            return {'score': 0, 'gaps': ['Routing data not available']}
            
        routing_data = self.data_sources['routing']
        summary = routing_data.get('summary', {})
        realignment = routing_data.get('realignment_needs', {})
        
        total_routes = summary.get('total_api_routes', 0)
        orphan_routes = len(realignment.get('orphan_routes', []))
        score = ((total_routes - orphan_routes) / total_routes * 100) if total_routes > 0 else 0
        
        return {
            'score': score,
            'total_api_routes': total_routes,
            'total_ui_components': summary.get('total_ui_components', 0),
            'mappings': summary.get('total_mappings', 0),
            'orphan_routes': orphan_routes,
            'orphan_components': len(realignment.get('orphan_components', [])),
            'gaps': [r['path'] for r in realignment.get('orphan_routes', [])[:5]]
        }
        
    def _calc_quality_alignment(self) -> Dict[str, Any]:
        """Calculate quality metrics alignment"""
        if not self.data_sources.get('bug_audit'):
            return {'score': 0, 'gaps': ['Bug audit data not available']}
            
        bug_data = self.data_sources['bug_audit']
        summary = bug_data.get('summary', {})
        
        total_bugs = summary.get('total_unique_bugs', 0)
        critical_bugs = summary.get('by_severity', {}).get('critical', 0)
        high_bugs = summary.get('by_severity', {}).get('high', 0)
        
        # Quality score based on bug severity distribution
        if total_bugs > 0:
            critical_weight = (critical_bugs / total_bugs) * 50
            high_weight = (high_bugs / total_bugs) * 30
            score = max(0, 100 - critical_weight - high_weight)
        else:
            score = 100
            
        return {
            'score': score,
            'total_bugs': total_bugs,
            'critical_bugs': critical_bugs,
            'high_bugs': high_bugs,
            'test_coverage': 'TBD',  # Would need actual test coverage data
            'gaps': list(summary.get('by_type', {}).keys())[:5]
        }
        
    def _calc_operations_alignment(self) -> Dict[str, Any]:
        """Calculate operational readiness"""
        if not self.data_sources.get('env_audit'):
            return {'score': 0, 'gaps': ['Environment audit data not available']}
            
        env_data = self.data_sources['env_audit']
        
        # Count healthy services
        health_checks = env_data.get('health_checks', [])
        if isinstance(health_checks, list):
            healthy = sum(1 for h in health_checks if h.get('healthy', False))
            total = len(health_checks)
        else:
            healthy = sum(1 for h in health_checks.values() if h.get('healthy', False))
            total = len(health_checks)
            
        score = (healthy / total * 100) if total > 0 else 0
        
        return {
            'score': score,
            'healthy_services': healthy,
            'total_services': total,
            'docker_available': env_data.get('docker', {}).get('available', False),
            'gaps': self._extract_ops_gaps(env_data)
        }
        
    def _extract_ops_gaps(self, env_data: Dict[str, Any]) -> List[str]:
        """Extract operational gaps"""
        gaps = []
        
        if not env_data.get('docker', {}).get('available', False):
            gaps.append('Docker not available')
            
        # Check for unhealthy services
        health_checks = env_data.get('health_checks', [])
        if isinstance(health_checks, list):
            for check in health_checks:
                if not check.get('healthy', False):
                    gaps.append(f"Service unhealthy: {check.get('service', 'Unknown')}")
        else:
            for service, check in health_checks.items():
                if not check.get('healthy', False):
                    gaps.append(f"Service unhealthy: {service}")
                    
        return gaps[:10]
        
    def build_crosslinks(self):
        """Build comprehensive crosslinks between all components"""
        # Features to Components
        if self.data_sources.get('flow_design'):
            flow_data = self.data_sources['flow_design']
            features = flow_data.get('features', [])
            if isinstance(features, list):
                for feature in features:
                    if isinstance(feature, dict):
                        feature_id = feature.get('id')
                        if feature_id:
                            for comp in feature.get('ui_components', []):
                                if comp:
                                    self.crosslinks['features_to_components'].add((feature_id, comp))
                            for dep in feature.get('dependencies', []):
                                if dep:
                                    self.crosslinks['feature_dependencies'].add((feature_id, dep))
                    
        # Routes to Components
        if self.data_sources.get('routing'):
            routing_data = self.data_sources['routing']
            mappings = routing_data.get('mappings', [])
            if isinstance(mappings, list):
                for mapping in mappings:
                    if isinstance(mapping, dict):
                        route = mapping.get('api_route')
                        component = mapping.get('component')
                        if route and component:
                            self.crosslinks['routes_to_components'].add((route, component))
                
        # Bugs to Features
        if self.data_sources.get('bug_audit'):
            bug_data = self.data_sources['bug_audit']
            bugs = bug_data.get('bugs', [])
            if isinstance(bugs, list):
                for bug in bugs:
                    if isinstance(bug, dict):
                        bug_id = bug.get('id', bug.get('fingerprint'))
                        if bug_id:
                            for feature_id in bug.get('affected_features', []):
                                if feature_id:
                                    self.crosslinks['bugs_to_features'].add((bug_id, feature_id))
                    
        # Tasks to Gates
        if self.data_sources.get('execution_plan'):
            exec_data = self.data_sources['execution_plan']
            todos = exec_data.get('todos', {})
            if isinstance(todos, dict):
                for gate, tasks in todos.items():
                    if isinstance(tasks, list):
                        for task in tasks:
                            if isinstance(task, dict):
                                task_id = task.get('id')
                                if task_id:
                                    self.crosslinks['tasks_to_gates'].add((task_id, gate))
                                    for dep in task.get('dependencies', []):
                                        if dep:
                                            self.crosslinks['task_dependencies'].add((task_id, dep))
                        
    def generate_document(self):
        """Generate the source of truth document"""
        with open('docs/plan/OPENPOLICY_V2_SOURCE_OF_TRUTH.md', 'w') as f:
            # Header
            f.write("# OpenPolicy V2 Source of Truth\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            f.write("This document serves as the comprehensive source of truth for the OpenPolicy V2 platform, ")
            f.write("aggregating all analysis, planning, and alignment information.\n\n")
            
            # Table of Contents
            f.write("## Table of Contents\n\n")
            f.write("1. [Executive Summary](#executive-summary)\n")
            f.write("2. [System Overview](#system-overview)\n")
            f.write("3. [Current State Analysis](#current-state-analysis)\n")
            f.write("4. [Alignment Delta](#alignment-delta)\n")
            f.write("5. [Implementation Roadmap](#implementation-roadmap)\n")
            f.write("6. [Crosslinks Appendix](#crosslinks-appendix)\n\n")
            
            # Executive Summary
            f.write("## Executive Summary\n\n")
            self._write_executive_summary(f)
            
            # System Overview
            f.write("## System Overview\n\n")
            self._write_system_overview(f)
            
            # Current State Analysis
            f.write("## Current State Analysis\n\n")
            self._write_current_state(f)
            
            # Alignment Delta
            f.write("## Alignment Delta\n\n")
            self._write_alignment_delta(f)
            
            # Implementation Roadmap
            f.write("## Implementation Roadmap\n\n")
            self._write_roadmap(f)
            
            # Crosslinks Appendix
            f.write("## Crosslinks Appendix\n\n")
            self._write_crosslinks(f)
            
    def _write_executive_summary(self, f):
        """Write executive summary section"""
        # Calculate overall health score
        scores = []
        for category, delta in self.alignment_delta.items():
            if isinstance(delta, dict) and 'score' in delta:
                scores.append(delta['score'])
        overall_score = sum(scores) / len(scores) if scores else 0
        
        f.write(f"### Overall Platform Health: {overall_score:.1f}%\n\n")
        
        f.write("**Key Metrics:**\n")
        for category, delta in self.alignment_delta.items():
            if isinstance(delta, dict) and 'score' in delta:
                f.write(f"- {category.replace('_', ' ').title()}: {delta['score']:.1f}%\n")
        f.write("\n")
        
        # Summary statistics
        if self.data_sources.get('var_func_map'):
            stats = self.data_sources['var_func_map'].get('statistics', {})
            f.write("**Codebase Statistics:**\n")
            f.write(f"- Total Nodes: {stats.get('total_nodes', 0):,}\n")
            f.write(f"- Total Edges: {stats.get('total_edges', 0):,}\n")
            f.write(f"- Files Analyzed: {stats.get('files_analyzed', 0):,}\n\n")
            
        if self.data_sources.get('execution_plan'):
            exec_summary = self.data_sources['execution_plan'].get('summary', {})
            f.write("**Execution Plan:**\n")
            f.write(f"- Total TODOs: {exec_summary.get('total_todos', 0)}\n")
            f.write("- By Gate:\n")
            for gate, count in exec_summary.get('by_gate', {}).items():
                f.write(f"  - {gate}: {count} tasks\n")
            f.write("\n")
            
    def _write_system_overview(self, f):
        """Write system overview section"""
        f.write("### Architecture\n\n")
        if self.data_sources.get('architecture'):
            arch_data = self.data_sources['architecture']
            current = arch_data.get('current_architecture', {})
            
            f.write("**Current State:**\n")
            f.write(f"- Type: {current.get('type', 'Unknown')}\n")
            f.write(f"- Services: {len(current.get('services', []))}\n")
            f.write(f"- Technologies: {', '.join(current.get('technologies', {}).keys())}\n\n")
            
            proposed = arch_data.get('proposed_architecture', {})
            if proposed:
                f.write("**Proposed State:**\n")
                phases = proposed.get('transformation_phases', {})
                if phases:
                    f.write(f"- Current Phase: {phases.get('current_phase', 'Unknown')}\n")
                    f.write(f"- Total Phases: {len(phases.get('phases', []))}\n")
                f.write("\n")
                
        f.write("### Features\n\n")
        if self.data_sources.get('flow_design'):
            flow_data = self.data_sources['flow_design']
            f.write(f"- Total Features: {len(flow_data.get('features', []))}\n")
            f.write(f"- Legacy Features Found: {len(flow_data.get('legacy_features', []))}\n")
            diff = flow_data.get('legacy_vs_current_diff', {})
            f.write(f"- Feature Parity: {len(diff.get('matched_features', []))} / {len(diff.get('legacy_features', []))}\n\n")
            
        f.write("### Data Management\n\n")
        if self.data_sources.get('data_journey'):
            journey_data = self.data_sources['data_journey']
            summary = journey_data.get('summary', {})
            f.write(f"- Data Points Mapped: {summary.get('data_points_mapped', 0)}\n")
            f.write(f"- Average Completeness: {summary.get('average_completeness', 0):.1f}%\n")
            f.write(f"- Complete Journeys: {summary.get('complete_journeys', 0)}\n\n")
            
    def _write_current_state(self, f):
        """Write current state analysis section"""
        f.write("### Environment Status\n\n")
        if self.data_sources.get('env_audit'):
            env_data = self.data_sources['env_audit']
            f.write(f"- Docker Available: {'Yes' if env_data.get('docker', {}).get('available', False) else 'No'}\n")
            
            # Resource usage
            resources = env_data.get('resources', {})
            if resources:
                f.write("- Resource Usage:\n")
                if 'cpu' in resources:
                    f.write(f"  - CPU: {resources['cpu'].get('percent', 'N/A')}%\n")
                if 'memory' in resources:
                    f.write(f"  - Memory: {resources['memory'].get('percent', 'N/A')}%\n")
                if 'disk' in resources:
                    f.write(f"  - Disk: {resources['disk'].get('percent', 'N/A')}%\n")
            f.write("\n")
            
        f.write("### Quality Metrics\n\n")
        if self.data_sources.get('bug_audit'):
            bug_data = self.data_sources['bug_audit']
            summary = bug_data.get('summary', {})
            f.write(f"- Total Unique Bugs: {summary.get('total_unique_bugs', 0)}\n")
            f.write("- By Severity:\n")
            for severity, count in summary.get('by_severity', {}).items():
                f.write(f"  - {severity.capitalize()}: {count}\n")
            f.write("- By Type:\n")
            for bug_type, count in list(summary.get('by_type', {}).items())[:5]:
                f.write(f"  - {bug_type}: {count}\n")
            f.write("\n")
            
    def _write_alignment_delta(self, f):
        """Write alignment delta section"""
        f.write("This section presents the comprehensive alignment analysis across all system dimensions.\n\n")
        
        for category, delta in self.alignment_delta.items():
            if isinstance(delta, dict):
                f.write(f"### {category.replace('_', ' ').title()} Alignment\n\n")
                f.write(f"**Score: {delta.get('score', 0):.1f}%**\n\n")
                
                # Write specific metrics
                for key, value in delta.items():
                    if key not in ['score', 'gaps', 'risks', 'opportunities']:
                        f.write(f"- {key.replace('_', ' ').title()}: {value}\n")
                f.write("\n")
                
                # Write gaps
                if delta.get('gaps'):
                    f.write("**Gaps:**\n")
                    for gap in delta['gaps'][:10]:  # Top 10 gaps
                        f.write(f"- {gap}\n")
                    if len(delta['gaps']) > 10:
                        f.write(f"- ...and {len(delta['gaps']) - 10} more\n")
                    f.write("\n")
                    
                # Write risks
                if delta.get('risks'):
                    f.write("**Risks:**\n")
                    for risk in delta['risks'][:5]:
                        f.write(f"- {risk}\n")
                    f.write("\n")
                    
                # Write opportunities
                if delta.get('opportunities'):
                    f.write("**Opportunities:**\n")
                    for opp in delta['opportunities'][:5]:
                        f.write(f"- {opp}\n")
                    f.write("\n")
                    
    def _write_roadmap(self, f):
        """Write implementation roadmap section"""
        if self.data_sources.get('execution_plan'):
            exec_data = self.data_sources['execution_plan']
            
            f.write("### Implementation Gates\n\n")
            for gate, tasks in exec_data.get('todos', {}).items():
                f.write(f"#### {gate}\n\n")
                f.write(f"**Total Tasks: {len(tasks)}**\n\n")
                
                # Show first 5 tasks
                f.write("Key Tasks:\n")
                for task in tasks[:5]:
                    f.write(f"- [{task['id']}] {task['task']}\n")
                if len(tasks) > 5:
                    f.write(f"- ...and {len(tasks) - 5} more tasks\n")
                f.write("\n")
                
        f.write("### Migration Strategy\n\n")
        if self.data_sources.get('architecture'):
            arch_data = self.data_sources['architecture']
            strategy = arch_data.get('proposed_architecture', {}).get('migration_strategy', {})
            
            if strategy:
                f.write(f"**Approach:** {strategy.get('approach', 'Unknown')}\n")
                f.write(f"**Duration:** {strategy.get('estimated_duration', 'TBD')}\n\n")
                
                if strategy.get('key_milestones'):
                    f.write("**Key Milestones:**\n")
                    for milestone in strategy['key_milestones']:
                        f.write(f"- {milestone}\n")
                    f.write("\n")
                    
    def _write_crosslinks(self, f):
        """Write crosslinks appendix section"""
        f.write("This appendix provides comprehensive crosslinks between all system components, ")
        f.write("enabling traceability and impact analysis.\n\n")
        
        # Features to Components
        if self.crosslinks['features_to_components']:
            f.write("### Features → Components\n\n")
            feature_groups = defaultdict(list)
            for feature_id, component in self.crosslinks['features_to_components']:
                feature_groups[feature_id].append(component)
                
            for feature_id, components in list(feature_groups.items())[:10]:
                f.write(f"- **{feature_id}**: {', '.join(components)}\n")
            if len(feature_groups) > 10:
                f.write(f"- ...and {len(feature_groups) - 10} more features\n")
            f.write("\n")
            
        # Routes to Components
        if self.crosslinks['routes_to_components']:
            f.write("### API Routes → Components\n\n")
            route_groups = defaultdict(list)
            for route, component in self.crosslinks['routes_to_components']:
                route_groups[route].append(component)
                
            for route, components in list(route_groups.items())[:10]:
                f.write(f"- **{route}**: {', '.join(components)}\n")
            if len(route_groups) > 10:
                f.write(f"- ...and {len(route_groups) - 10} more routes\n")
            f.write("\n")
            
        # Feature Dependencies
        if self.crosslinks['feature_dependencies']:
            f.write("### Feature Dependencies\n\n")
            dep_groups = defaultdict(list)
            for feature_id, dep in self.crosslinks['feature_dependencies']:
                dep_groups[feature_id].append(dep)
                
            for feature_id, deps in list(dep_groups.items())[:10]:
                f.write(f"- **{feature_id}** depends on: {', '.join(deps)}\n")
            if len(dep_groups) > 10:
                f.write(f"- ...and {len(dep_groups) - 10} more features with dependencies\n")
            f.write("\n")
            
        # Task Dependencies
        if self.crosslinks['task_dependencies']:
            f.write("### Task Dependencies\n\n")
            task_dep_groups = defaultdict(list)
            for task_id, dep in self.crosslinks['task_dependencies']:
                task_dep_groups[task_id].append(dep)
                
            for task_id, deps in list(task_dep_groups.items())[:10]:
                f.write(f"- **{task_id}** depends on: {', '.join(deps)}\n")
            if len(task_dep_groups) > 10:
                f.write(f"- ...and {len(task_dep_groups) - 10} more tasks with dependencies\n")
            f.write("\n")
            
        # Summary statistics
        f.write("### Crosslink Statistics\n\n")
        for link_type, links in self.crosslinks.items():
            f.write(f"- {link_type.replace('_', ' ').title()}: {len(links)} links\n")
            
    def generate_manifest(self):
        """Generate the organizer manifest"""
        manifest = {
            'generated_at': datetime.now().isoformat(),
            'pass_number': 2,  # Will be updated by the runner
            'reports_generated': [],
            'documents_created': [],
            'alignment_summary': self.alignment_delta,
            'crosslink_counts': {k: len(v) for k, v in self.crosslinks.items()},
            'data_sources': list(self.data_sources.keys()),
            'execution_summary': {}
        }
        
        # List all generated reports
        reports_dir = Path('reports')
        for report in reports_dir.glob('*.json'):
            manifest['reports_generated'].append({
                'name': report.name,
                'path': str(report),
                'size': report.stat().st_size
            })
            
        for report in reports_dir.glob('*.md'):
            manifest['reports_generated'].append({
                'name': report.name,
                'path': str(report),
                'size': report.stat().st_size
            })
            
        # List all created documents
        docs_dir = Path('docs/plan')
        for doc in docs_dir.glob('*.md'):
            manifest['documents_created'].append({
                'name': doc.name,
                'path': str(doc),
                'size': doc.stat().st_size
            })
            
        # Add execution summary
        if self.data_sources.get('execution_plan'):
            exec_summary = self.data_sources['execution_plan'].get('summary', {})
            manifest['execution_summary'] = {
                'total_todos': exec_summary.get('total_todos', 0),
                'by_gate': exec_summary.get('by_gate', {})
            }
            
        # Save manifest
        with open('reports/organizer_manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)
            
        return manifest


def main():
    generator = SourceOfTruthGenerator()
    
    print("Loading all reports and data...")
    generator.load_all_reports()
    
    print("Calculating alignment delta...")
    generator.calculate_alignment_delta()
    
    print("Building crosslinks...")
    generator.build_crosslinks()
    
    print("Generating source of truth document...")
    generator.generate_document()
    
    print("Generating organizer manifest...")
    manifest = generator.generate_manifest()
    
    print("\n✓ Source of Truth document created: docs/plan/OPENPOLICY_V2_SOURCE_OF_TRUTH.md")
    print("✓ Organizer manifest created: reports/organizer_manifest.json")
    print(f"\nAlignment Summary:")
    for category, delta in generator.alignment_delta.items():
        if isinstance(delta, dict) and 'score' in delta:
            print(f"  - {category}: {delta['score']:.1f}%")


if __name__ == "__main__":
    main()