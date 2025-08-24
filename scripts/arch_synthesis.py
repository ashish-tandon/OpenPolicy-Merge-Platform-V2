#!/usr/bin/env python3
"""
Architecture Synthesis & Alignment Tool
Generates architecture proposal aligned with future state and creates delta analysis
"""

import json
import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict
import argparse
from datetime import datetime


class ArchitectureSynthesizer:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.current_architecture = {}
        self.future_state = {}
        self.proposed_architecture = {}
        self.constraints = []
        
    def load_future_state(self):
        """Load future state architecture document"""
        future_state_path = self.root_path / "docs/validation/FUTURE_STATE_ARCHITECTURE.md"
        if future_state_path.exists():
            print(f"Loading future state architecture from {future_state_path}")
            with open(future_state_path, 'r') as f:
                content = f.read()
                
            # Parse the future state
            self.future_state = {
                'vision': self.extract_section(content, "Vision:", "Target Architecture"),
                'principles': self.extract_principles(content),
                'architecture': self.extract_architecture_components(content),
                'services': self.extract_services(content),
                'data_layer': self.extract_data_layer(content),
                'technology_stack': self.extract_tech_stack(content)
            }
    
    def extract_section(self, content: str, start: str, end: str) -> str:
        """Extract a section between two markers"""
        start_idx = content.find(start)
        end_idx = content.find(end)
        if start_idx != -1 and end_idx != -1:
            return content[start_idx:end_idx].strip()
        return ""
    
    def extract_principles(self, content: str) -> List[Dict[str, str]]:
        """Extract core principles"""
        principles = []
        principle_pattern = r'(\d+)\.\s*\*\*([^:]+)\*\*:\s*(.+)'
        for match in re.finditer(principle_pattern, content):
            principles.append({
                'number': match.group(1),
                'name': match.group(2),
                'description': match.group(3)
            })
        return principles
    
    def extract_architecture_components(self, content: str) -> Dict[str, Any]:
        """Extract architecture components from diagram"""
        components = {
            'frontend': [],
            'api_layer': [],
            'services': [],
            'data_layer': []
        }
        
        # Extract from architecture diagram
        if "Web Application (CDN)" in content:
            components['frontend'].append({
                'name': 'Web Application',
                'technology': 'Next.js SSR/SSG',
                'features': ['PWA Support', 'Edge Functions', 'CDN']
            })
        
        if "Mobile Apps" in content:
            components['frontend'].append({
                'name': 'Mobile Apps',
                'technology': 'React Native',
                'features': ['Offline-First', 'Push Notifications']
            })
        
        if "API Gateway" in content:
            components['api_layer'].append({
                'name': 'API Gateway',
                'features': ['GraphQL Federation', 'REST Proxy', 'Rate Limiting', 'Auth']
            })
        
        # Extract microservices
        service_pattern = r'│\s*(\w+)\s+Service\s*│[^│]+│[^│]+│[^│]+│'
        for match in re.finditer(service_pattern, content):
            service_name = match.group(1)
            components['services'].append({
                'name': f"{service_name} Service",
                'type': 'microservice'
            })
        
        return components
    
    def extract_services(self, content: str) -> List[Dict[str, Any]]:
        """Extract service definitions"""
        services = []
        
        # Extract service blocks
        service_blocks = re.findall(r'###\s*\d+\.\s*([^#]+)(?:```yaml\n([^`]+)```)?', content, re.DOTALL)
        
        for service_name, yaml_content in service_blocks:
            service = {
                'name': service_name.strip(),
                'config': {}
            }
            
            if yaml_content:
                # Parse YAML-like content
                for line in yaml_content.strip().split('\n'):
                    if ':' in line and not line.strip().endswith(':'):
                        key, value = line.split(':', 1)
                        service['config'][key.strip()] = value.strip()
            
            services.append(service)
        
        return services
    
    def extract_data_layer(self, content: str) -> Dict[str, Any]:
        """Extract data layer components"""
        data_layer = {
            'databases': [],
            'caching': [],
            'search': [],
            'storage': []
        }
        
        if "PostgreSQL" in content:
            data_layer['databases'].append({
                'name': 'PostgreSQL',
                'features': ['Sharded', 'Replicated']
            })
        
        if "Redis" in content:
            data_layer['caching'].append({
                'name': 'Redis',
                'features': ['Cache', 'Queue']
            })
        
        if "ElasticSearch" in content:
            data_layer['search'].append({
                'name': 'ElasticSearch',
                'features': ['Full-text', 'Analytics']
            })
        
        if "S3" in content:
            data_layer['storage'].append({
                'name': 'S3 Storage',
                'features': ['Media', 'Backups']
            })
        
        return data_layer
    
    def extract_tech_stack(self, content: str) -> Dict[str, List[str]]:
        """Extract technology stack"""
        tech_stack = defaultdict(list)
        
        # Extract from service definitions
        tech_patterns = {
            'language': r'language:\s*([^\n]+)',
            'framework': r'framework:\s*([^\n]+)',
            'database': r'database:\s*([^\n]+)'
        }
        
        for category, pattern in tech_patterns.items():
            for match in re.finditer(pattern, content):
                tech = match.group(1).strip()
                if tech not in tech_stack[category]:
                    tech_stack[category].append(tech)
        
        return dict(tech_stack)
    
    def analyze_current_architecture(self):
        """Analyze current architecture from codebase"""
        self.current_architecture = {
            'services': self.detect_services(),
            'databases': self.detect_databases(),
            'frontend': self.detect_frontend(),
            'api_patterns': self.detect_api_patterns(),
            'deployment': self.detect_deployment()
        }
    
    def detect_services(self) -> List[Dict[str, Any]]:
        """Detect current services"""
        services = []
        
        # Check services directory
        services_dir = self.root_path / "services"
        if services_dir.exists():
            for service_path in services_dir.iterdir():
                if service_path.is_dir() and not service_path.name.startswith(('_', '.')):
                    service_info = {
                        'name': service_path.name,
                        'path': str(service_path.relative_to(self.root_path)),
                        'type': 'service',
                        'status': 'active'
                    }
                    
                    # Check for key files
                    if (service_path / "Dockerfile").exists():
                        service_info['containerized'] = True
                    if (service_path / "requirements.txt").exists():
                        service_info['language'] = 'python'
                    elif (service_path / "package.json").exists():
                        service_info['language'] = 'javascript'
                    
                    services.append(service_info)
        
        return services
    
    def detect_databases(self) -> List[Dict[str, Any]]:
        """Detect database configurations"""
        databases = []
        
        # Check docker-compose files
        compose_files = list(self.root_path.glob("docker-compose*.yml"))
        for compose_file in compose_files:
            with open(compose_file, 'r') as f:
                content = f.read()
            
            if 'postgres' in content.lower():
                databases.append({
                    'type': 'PostgreSQL',
                    'source': str(compose_file.name)
                })
            
            if 'redis' in content.lower():
                databases.append({
                    'type': 'Redis',
                    'source': str(compose_file.name)
                })
            
            if 'elasticsearch' in content.lower():
                databases.append({
                    'type': 'ElasticSearch',
                    'source': str(compose_file.name)
                })
        
        return databases
    
    def detect_frontend(self) -> List[Dict[str, Any]]:
        """Detect frontend frameworks"""
        frontend = []
        
        # Check for Next.js
        if (self.root_path / "services/web-ui/next.config.ts").exists():
            frontend.append({
                'name': 'Web UI',
                'framework': 'Next.js',
                'path': 'services/web-ui'
            })
        
        # Check for React admin
        if (self.root_path / "services/admin-ui/vite.config.ts").exists():
            frontend.append({
                'name': 'Admin UI',
                'framework': 'React + Vite',
                'path': 'services/admin-ui'
            })
        
        return frontend
    
    def detect_api_patterns(self) -> List[str]:
        """Detect API patterns in use"""
        patterns = set()
        
        # Check for FastAPI
        if list(self.root_path.glob("**/main.py")):
            patterns.add("FastAPI")
        
        # Check for GraphQL
        if list(self.root_path.glob("**/*graphql*.py")):
            patterns.add("GraphQL")
        
        # Check for REST
        if list(self.root_path.glob("**/api/v1/**/*.py")):
            patterns.add("REST")
        
        return list(patterns)
    
    def detect_deployment(self) -> Dict[str, Any]:
        """Detect deployment configuration"""
        deployment = {
            'containerization': 'Docker',
            'orchestration': None,
            'ci_cd': []
        }
        
        # Check for Kubernetes
        if list(self.root_path.glob("**/*.yaml")) or list(self.root_path.glob("**/k8s/**")):
            deployment['orchestration'] = 'Kubernetes'
        
        # Check for GitHub Actions
        if (self.root_path / ".github/workflows").exists():
            deployment['ci_cd'].append('GitHub Actions')
        
        return deployment
    
    def identify_constraints(self):
        """Identify current constraints"""
        self.constraints = [
            {
                'type': 'technical',
                'description': 'Must maintain backward compatibility with legacy data formats',
                'impact': 'high'
            },
            {
                'type': 'technical',
                'description': 'Limited to current infrastructure capabilities',
                'impact': 'medium'
            },
            {
                'type': 'resource',
                'description': 'Development team size and expertise',
                'impact': 'high'
            },
            {
                'type': 'time',
                'description': 'Migration must be completed incrementally',
                'impact': 'medium'
            },
            {
                'type': 'data',
                'description': 'Must preserve all historical data',
                'impact': 'high'
            }
        ]
    
    def synthesize_architecture(self):
        """Synthesize new architecture proposal"""
        self.proposed_architecture = {
            'overview': 'Evolutionary architecture moving towards the 2030 vision',
            'approach': 'Incremental transformation with backward compatibility',
            'phases': self.define_transformation_phases(),
            'components': self.align_components(),
            'technology_decisions': self.make_tech_decisions(),
            'migration_strategy': self.define_migration_strategy()
        }
    
    def define_transformation_phases(self) -> List[Dict[str, Any]]:
        """Define transformation phases"""
        return [
            {
                'phase': 1,
                'name': 'Foundation Stabilization',
                'duration': '3 months',
                'goals': [
                    'Stabilize current services',
                    'Complete test coverage',
                    'Document all APIs',
                    'Establish monitoring'
                ],
                'deliverables': [
                    'Stable API Gateway',
                    'Complete documentation',
                    'Monitoring dashboard',
                    'CI/CD pipeline'
                ]
            },
            {
                'phase': 2,
                'name': 'Service Decomposition',
                'duration': '6 months',
                'goals': [
                    'Extract monolithic components',
                    'Create service boundaries',
                    'Implement service mesh',
                    'Add caching layer'
                ],
                'deliverables': [
                    'Parliament Service',
                    'User Service',
                    'Content Service',
                    'Redis caching'
                ]
            },
            {
                'phase': 3,
                'name': 'Platform Enhancement',
                'duration': '6 months',
                'goals': [
                    'Add GraphQL federation',
                    'Implement real-time features',
                    'Add analytics service',
                    'Mobile app development'
                ],
                'deliverables': [
                    'GraphQL Gateway',
                    'WebSocket support',
                    'Analytics Service',
                    'Mobile MVP'
                ]
            },
            {
                'phase': 4,
                'name': 'Scale & Optimize',
                'duration': '3 months',
                'goals': [
                    'Kubernetes deployment',
                    'Auto-scaling setup',
                    'Performance optimization',
                    'Security hardening'
                ],
                'deliverables': [
                    'K8s manifests',
                    'Auto-scaling config',
                    'Performance benchmarks',
                    'Security audit'
                ]
            }
        ]
    
    def align_components(self) -> Dict[str, Any]:
        """Align current components with future state"""
        alignment = {
            'frontend': {
                'current': self.current_architecture.get('frontend', []),
                'proposed': [
                    {
                        'name': 'Web Application',
                        'technology': 'Next.js 15',
                        'features': ['SSR/SSG', 'PWA', 'i18n'],
                        'migration': 'Enhance existing Next.js app'
                    },
                    {
                        'name': 'Admin Dashboard',
                        'technology': 'React + Vite',
                        'features': ['Real-time updates', 'Analytics'],
                        'migration': 'Keep current, add features'
                    }
                ],
                'future_aligned': True
            },
            'api_layer': {
                'current': self.current_architecture.get('api_patterns', []),
                'proposed': [
                    {
                        'name': 'API Gateway',
                        'technology': 'FastAPI',
                        'features': ['REST', 'GraphQL proxy', 'Auth'],
                        'migration': 'Extend current gateway'
                    }
                ],
                'future_aligned': False,
                'gap': 'Need GraphQL federation'
            },
            'services': {
                'current': self.current_architecture.get('services', []),
                'proposed': [
                    {
                        'name': 'api-gateway',
                        'type': 'API orchestration',
                        'status': 'enhance'
                    },
                    {
                        'name': 'user-service',
                        'type': 'User management',
                        'status': 'keep'
                    },
                    {
                        'name': 'etl',
                        'type': 'Data ingestion',
                        'status': 'refactor'
                    },
                    {
                        'name': 'parliament-service',
                        'type': 'Core parliamentary data',
                        'status': 'create'
                    }
                ],
                'future_aligned': False,
                'gap': 'Need service decomposition'
            },
            'data_layer': {
                'current': self.current_architecture.get('databases', []),
                'proposed': [
                    {
                        'name': 'PostgreSQL',
                        'purpose': 'Primary datastore',
                        'enhancements': ['Partitioning', 'Read replicas']
                    },
                    {
                        'name': 'Redis',
                        'purpose': 'Caching & queues',
                        'enhancements': ['Cluster mode']
                    },
                    {
                        'name': 'ElasticSearch',
                        'purpose': 'Search & analytics',
                        'enhancements': ['Full cluster']
                    }
                ],
                'future_aligned': True
            }
        }
        
        return alignment
    
    def make_tech_decisions(self) -> List[Dict[str, Any]]:
        """Make technology decisions"""
        return [
            {
                'area': 'Backend Language',
                'current': 'Python 3.x',
                'proposed': 'Python 3.12+',
                'future': 'Python 3.12+',
                'decision': 'Upgrade to Python 3.12',
                'rationale': 'Performance improvements, better async'
            },
            {
                'area': 'API Framework',
                'current': 'FastAPI',
                'proposed': 'FastAPI + GraphQL',
                'future': 'GraphQL Federation',
                'decision': 'Add GraphQL incrementally',
                'rationale': 'Gradual migration path'
            },
            {
                'area': 'Frontend Framework',
                'current': 'Next.js 15',
                'proposed': 'Next.js 15+',
                'future': 'Next.js with Edge',
                'decision': 'Keep Next.js, add edge functions',
                'rationale': 'Already aligned with future'
            },
            {
                'area': 'Container Orchestration',
                'current': 'Docker Compose',
                'proposed': 'Docker Swarm',
                'future': 'Kubernetes',
                'decision': 'Prepare for K8s, use Swarm transition',
                'rationale': 'Lower complexity initially'
            },
            {
                'area': 'Message Queue',
                'current': 'None',
                'proposed': 'Redis Pub/Sub',
                'future': 'Kafka/RabbitMQ',
                'decision': 'Start with Redis',
                'rationale': 'Already have Redis'
            }
        ]
    
    def define_migration_strategy(self) -> Dict[str, Any]:
        """Define migration strategy"""
        return {
            'approach': 'Strangler Fig Pattern',
            'principles': [
                'No big bang migrations',
                'Maintain backward compatibility',
                'Feature flags for gradual rollout',
                'Comprehensive testing at each step'
            ],
            'steps': [
                {
                    'step': 1,
                    'action': 'Create service interfaces',
                    'description': 'Define contracts between services'
                },
                {
                    'step': 2,
                    'action': 'Extract service logic',
                    'description': 'Move business logic to services'
                },
                {
                    'step': 3,
                    'action': 'Implement service mesh',
                    'description': 'Add service discovery and routing'
                },
                {
                    'step': 4,
                    'action': 'Migrate data layer',
                    'description': 'Optimize database schema'
                },
                {
                    'step': 5,
                    'action': 'Enable new features',
                    'description': 'Turn on GraphQL, WebSockets'
                }
            ],
            'rollback_plan': [
                'Feature flags for instant rollback',
                'Database migration reversibility',
                'Service version pinning',
                'Traffic routing controls'
            ]
        }
    
    def calculate_alignment_delta(self) -> Dict[str, Any]:
        """Calculate delta between current, proposed, and future"""
        delta = {
            'alignment_score': 0,
            'gaps': [],
            'risks': [],
            'opportunities': []
        }
        
        # Calculate alignment score
        aligned_components = 0
        total_components = 0
        
        for area, alignment in self.proposed_architecture.get('components', {}).items():
            total_components += 1
            if alignment.get('future_aligned', False):
                aligned_components += 1
            else:
                delta['gaps'].append({
                    'area': area,
                    'gap': alignment.get('gap', 'Not aligned with future state'),
                    'priority': 'high' if area in ['api_layer', 'services'] else 'medium'
                })
        
        delta['alignment_score'] = (aligned_components / total_components * 100) if total_components > 0 else 0
        
        # Identify risks
        delta['risks'] = [
            {
                'risk': 'Service decomposition complexity',
                'impact': 'high',
                'mitigation': 'Incremental extraction with feature flags'
            },
            {
                'risk': 'Data migration errors',
                'impact': 'high',
                'mitigation': 'Comprehensive backup and rollback procedures'
            },
            {
                'risk': 'Performance degradation during transition',
                'impact': 'medium',
                'mitigation': 'Load testing and gradual rollout'
            },
            {
                'risk': 'Team skill gaps',
                'impact': 'medium',
                'mitigation': 'Training and documentation'
            }
        ]
        
        # Identify opportunities
        delta['opportunities'] = [
            {
                'opportunity': 'Improved scalability',
                'benefit': 'Handle 10x traffic',
                'effort': 'medium'
            },
            {
                'opportunity': 'Better developer experience',
                'benefit': 'Faster feature development',
                'effort': 'low'
            },
            {
                'opportunity': 'Real-time capabilities',
                'benefit': 'Live parliamentary updates',
                'effort': 'medium'
            },
            {
                'opportunity': 'Mobile platform',
                'benefit': 'Reach more citizens',
                'effort': 'high'
            }
        ]
        
        return delta
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive architecture report"""
        # Load future state
        self.load_future_state()
        
        # Analyze current architecture
        print("Analyzing current architecture...")
        self.analyze_current_architecture()
        
        # Identify constraints
        self.identify_constraints()
        
        # Synthesize new architecture
        print("Synthesizing architecture proposal...")
        self.synthesize_architecture()
        
        # Calculate alignment delta
        delta = self.calculate_alignment_delta()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'current_state': self.current_architecture,
            'future_state': self.future_state,
            'proposed_architecture': self.proposed_architecture,
            'constraints': self.constraints,
            'alignment_delta': delta
        }
        
        return report
    
    def export_proposal_markdown(self, report: Dict[str, Any], output_path: str):
        """Export architecture proposal as markdown"""
        with open(output_path, 'w') as f:
            f.write("# New Architecture Proposal\n\n")
            f.write(f"Generated: {report['generated_at']}\n\n")
            f.write("## Executive Summary\n\n")
            f.write(f"{report['proposed_architecture']['overview']}\n\n")
            f.write(f"**Approach**: {report['proposed_architecture']['approach']}\n\n")
            f.write(f"**Alignment Score**: {report['alignment_delta']['alignment_score']:.1f}%\n\n")
            
            f.write("## Transformation Phases\n\n")
            for phase in report['proposed_architecture']['phases']:
                f.write(f"### Phase {phase['phase']}: {phase['name']}\n\n")
                f.write(f"**Duration**: {phase['duration']}\n\n")
                f.write("**Goals**:\n")
                for goal in phase['goals']:
                    f.write(f"- {goal}\n")
                f.write("\n**Deliverables**:\n")
                for deliverable in phase['deliverables']:
                    f.write(f"- {deliverable}\n")
                f.write("\n")
            
            f.write("## Component Architecture\n\n")
            for area, alignment in report['proposed_architecture']['components'].items():
                f.write(f"### {area.replace('_', ' ').title()}\n\n")
                
                if 'current' in alignment and alignment['current']:
                    f.write("**Current State**:\n")
                    for item in alignment['current']:
                        if isinstance(item, dict):
                            f.write(f"- {item.get('name', item.get('type', 'Unknown'))}\n")
                        else:
                            f.write(f"- {item}\n")
                    f.write("\n")
                
                if 'proposed' in alignment:
                    f.write("**Proposed State**:\n")
                    for item in alignment['proposed']:
                        f.write(f"- **{item['name']}**\n")
                        if 'technology' in item:
                            f.write(f"  - Technology: {item['technology']}\n")
                        if 'features' in item:
                            f.write(f"  - Features: {', '.join(item['features'])}\n")
                        if 'migration' in item:
                            f.write(f"  - Migration: {item['migration']}\n")
                    f.write("\n")
                
                f.write(f"**Future Aligned**: {'✅ Yes' if alignment.get('future_aligned', False) else '❌ No'}\n")
                if 'gap' in alignment:
                    f.write(f"**Gap**: {alignment['gap']}\n")
                f.write("\n")
            
            f.write("## Technology Decisions\n\n")
            f.write("| Area | Current | Proposed | Future Target | Decision | Rationale |\n")
            f.write("|------|---------|----------|---------------|----------|------------|\n")
            for decision in report['proposed_architecture']['technology_decisions']:
                f.write(f"| {decision['area']} | {decision['current']} | {decision['proposed']} | ")
                f.write(f"{decision['future']} | {decision['decision']} | {decision['rationale']} |\n")
            f.write("\n")
            
            f.write("## Migration Strategy\n\n")
            strategy = report['proposed_architecture']['migration_strategy']
            f.write(f"**Approach**: {strategy['approach']}\n\n")
            
            f.write("### Principles\n\n")
            for principle in strategy['principles']:
                f.write(f"- {principle}\n")
            f.write("\n")
            
            f.write("### Migration Steps\n\n")
            for step in strategy['steps']:
                f.write(f"{step['step']}. **{step['action']}**\n")
                f.write(f"   - {step['description']}\n")
            f.write("\n")
            
            f.write("### Rollback Plan\n\n")
            for plan in strategy['rollback_plan']:
                f.write(f"- {plan}\n")
            f.write("\n")
            
            f.write("## Constraints\n\n")
            for constraint in report['constraints']:
                f.write(f"- **{constraint['type'].title()}**: {constraint['description']} ")
                f.write(f"(Impact: {constraint['impact']})\n")
            f.write("\n")
            
            f.write("## Next Steps\n\n")
            f.write("1. Review and approve architecture proposal\n")
            f.write("2. Create detailed implementation plan for Phase 1\n")
            f.write("3. Set up architecture decision records (ADRs)\n")
            f.write("4. Establish architecture review board\n")
            f.write("5. Begin Phase 1 implementation\n")
    
    def export_alignment_markdown(self, report: Dict[str, Any], output_path: str):
        """Export architecture alignment as markdown"""
        with open(output_path, 'w') as f:
            f.write("# Architecture Alignment Report\n\n")
            f.write(f"Generated: {report['generated_at']}\n\n")
            
            f.write("## Alignment Overview\n\n")
            delta = report['alignment_delta']
            f.write(f"**Overall Alignment Score**: {delta['alignment_score']:.1f}%\n\n")
            
            f.write("### Current vs Proposed vs Future State\n\n")
            f.write("| Component | Current State | Proposed State | Future State (2030) | Alignment |\n")
            f.write("|-----------|---------------|----------------|---------------------|------------|\n")
            
            # Frontend
            f.write("| **Frontend** | ")
            current_frontend = [fe['name'] for fe in report['current_state'].get('frontend', [])]
            f.write(f"{', '.join(current_frontend) if current_frontend else 'Legacy'} | ")
            f.write("Next.js 15 + React | ")
            f.write("Next.js SSR/SSG with Edge | ")
            f.write("✅ Aligned |\n")
            
            # API Layer
            f.write("| **API Layer** | ")
            f.write(f"{', '.join(report['current_state'].get('api_patterns', []))} | ")
            f.write("REST + GraphQL Proxy | ")
            f.write("GraphQL Federation | ")
            f.write("⚠️  Partial |\n")
            
            # Services
            f.write("| **Services** | ")
            current_services = [s['name'] for s in report['current_state'].get('services', [])]
            f.write(f"{len(current_services)} services | ")
            f.write("4 core services | ")
            f.write("Full microservices | ")
            f.write("❌ Gap |\n")
            
            # Data Layer
            f.write("| **Data Layer** | ")
            current_dbs = [db['type'] for db in report['current_state'].get('databases', [])]
            f.write(f"{', '.join(current_dbs)} | ")
            f.write("PostgreSQL + Redis + ES | ")
            f.write("Sharded PostgreSQL + Redis + ES + S3 | ")
            f.write("✅ Aligned |\n")
            
            # Deployment
            f.write("| **Deployment** | ")
            f.write(f"{report['current_state'].get('deployment', {}).get('containerization', 'None')} | ")
            f.write("Docker Swarm | ")
            f.write("Kubernetes | ")
            f.write("⚠️  Partial |\n")
            f.write("\n")
            
            f.write("## Alignment Gaps\n\n")
            if delta['gaps']:
                for gap in delta['gaps']:
                    f.write(f"### {gap['area'].replace('_', ' ').title()}\n")
                    f.write(f"- **Gap**: {gap['gap']}\n")
                    f.write(f"- **Priority**: {gap['priority']}\n\n")
            else:
                f.write("No significant gaps identified.\n\n")
            
            f.write("## Risks\n\n")
            f.write("| Risk | Impact | Mitigation |\n")
            f.write("|------|--------|------------|\n")
            for risk in delta['risks']:
                f.write(f"| {risk['risk']} | {risk['impact']} | {risk['mitigation']} |\n")
            f.write("\n")
            
            f.write("## Opportunities\n\n")
            f.write("| Opportunity | Benefit | Effort |\n")
            f.write("|-------------|---------|--------|\n")
            for opp in delta['opportunities']:
                f.write(f"| {opp['opportunity']} | {opp['benefit']} | {opp['effort']} |\n")
            f.write("\n")
            
            f.write("## Migration Compatibility\n\n")
            f.write("### Backward Compatibility Requirements\n\n")
            f.write("- ✅ All existing APIs must continue to function\n")
            f.write("- ✅ Database schema changes must be backward compatible\n")
            f.write("- ✅ Feature flags for all new functionality\n")
            f.write("- ✅ Zero-downtime deployments\n\n")
            
            f.write("### Data Contracts\n\n")
            f.write("| Contract | Version | Status | Migration Path |\n")
            f.write("|----------|---------|--------|----------------|\n")
            f.write("| Bills API | v1 | Stable | Maintain v1, add v2 |\n")
            f.write("| Members API | v1 | Stable | Maintain v1, add v2 |\n")
            f.write("| Votes API | v1 | Stable | Maintain v1, add v2 |\n")
            f.write("| Search API | v1 | Stable | Enhance with GraphQL |\n\n")
            
            f.write("## Performance & SLOs\n\n")
            f.write("### Current Performance\n")
            f.write("- API Response Time: <500ms (p95)\n")
            f.write("- Search Latency: <200ms (p95)\n")
            f.write("- Availability: 99.9%\n\n")
            
            f.write("### Target Performance\n")
            f.write("- API Response Time: <200ms (p95)\n")
            f.write("- Search Latency: <100ms (p95)\n")
            f.write("- Availability: 99.99%\n")
            f.write("- Concurrent Users: 10,000+\n\n")
            
            f.write("## Observability Requirements\n\n")
            f.write("- ✅ Distributed tracing (OpenTelemetry)\n")
            f.write("- ✅ Centralized logging (ELK stack)\n")
            f.write("- ✅ Metrics collection (Prometheus)\n")
            f.write("- ✅ Real-time monitoring (Grafana)\n")
            f.write("- ⚠️  APM integration (future)\n\n")
            
            f.write("## Decision Matrix\n\n")
            f.write("| Component | Keep | Modify | Replace | Deprecate | Decision |\n")
            f.write("|-----------|------|--------|---------|-----------|----------|\n")
            f.write("| API Gateway | ✅ | ✅ | | | Enhance with GraphQL |\n")
            f.write("| User Service | ✅ | | | | Keep as-is |\n")
            f.write("| ETL Service | | ✅ | | | Refactor for scalability |\n")
            f.write("| PostgreSQL | ✅ | ✅ | | | Add partitioning |\n")
            f.write("| Redis | ✅ | ✅ | | | Enable cluster mode |\n")
            f.write("| Legacy Code | | | | ✅ | Gradual deprecation |\n")


def main():
    parser = argparse.ArgumentParser(description="Synthesize and align architecture")
    parser.add_argument("--root", default=".", help="Root directory")
    parser.add_argument("--output-dir", default="docs/plan", help="Output directory")
    args = parser.parse_args()
    
    # Create output directories
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    arch_dir = output_dir / "architecture"
    arch_dir.mkdir(exist_ok=True)
    
    # Run synthesis
    synthesizer = ArchitectureSynthesizer(args.root)
    report = synthesizer.generate_report()
    
    # Export reports
    json_path = output_dir / "architecture_synthesis.json"
    proposal_path = output_dir / "NEW_ARCHITECTURE_PROPOSAL.md"
    alignment_path = arch_dir / "ARCHITECTURE_ALIGNMENT.md"
    
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    synthesizer.export_proposal_markdown(report, str(proposal_path))
    synthesizer.export_alignment_markdown(report, str(alignment_path))
    
    print(f"\nArchitecture Synthesis Complete:")
    print(f"  Alignment Score: {report['alignment_delta']['alignment_score']:.1f}%")
    print(f"  Identified Gaps: {len(report['alignment_delta']['gaps'])}")
    print(f"  Identified Risks: {len(report['alignment_delta']['risks'])}")
    print(f"  Identified Opportunities: {len(report['alignment_delta']['opportunities'])}")
    print(f"  Reports saved to:")
    print(f"    - {json_path}")
    print(f"    - {proposal_path}")
    print(f"    - {alignment_path}")


if __name__ == "__main__":
    main()