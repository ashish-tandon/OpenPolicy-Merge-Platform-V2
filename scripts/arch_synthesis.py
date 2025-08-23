#!/usr/bin/env python3
"""
Architecture Synthesis & Alignment Script
Analyzes current architecture and proposes new architecture aligned with future state
"""

import os
import json
import re
from datetime import datetime

def analyze_current_architecture():
    """Analyze current architecture from existing documentation"""
    current_arch = {
        'services': [],
        'databases': [],
        'apis': [],
        'dependencies': [],
        'constraints': []
    }
    
    # Check docker-compose for services
    if os.path.exists('docker-compose.yml'):
        with open('docker-compose.yml', 'r') as f:
            content = f.read()
            # Extract service names
            service_matches = re.findall(r'^\s+(\w+):', content, re.MULTILINE)
            current_arch['services'] = service_matches
    
    # Check for database configurations
    if os.path.exists('services/api-gateway/app/models/openparliament.py'):
        current_arch['databases'].append('PostgreSQL (openparliament schema)')
    
    # Check for API endpoints
    api_files = [
        'services/api-gateway/app/api/v1/bills.py',
        'services/api-gateway/app/api/v1/members.py',
        'services/api-gateway/app/api/v1/committees.py',
        'services/api-gateway/app/api/v1/debates.py',
        'services/api-gateway/app/api/v1/votes.py',
        'services/api-gateway/app/api/v1/search.py'
    ]
    
    for api_file in api_files:
        if os.path.exists(api_file):
            current_arch['apis'].append(os.path.basename(api_file).replace('.py', ''))
    
    # Check for dependencies
    if os.path.exists('services/api-gateway/requirements.txt'):
        with open('services/api-gateway/requirements.txt', 'r') as f:
            content = f.read()
            deps = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
            current_arch['dependencies'] = deps
    
    return current_arch

def analyze_future_state_architecture():
    """Analyze future state architecture from documentation"""
    future_arch = {
        'components': [],
        'interfaces': [],
        'data_contracts': [],
        'slos': [],
        'risks': [],
        'mitigations': []
    }
    
    # Check for future state architecture document
    future_doc = 'docs/validation/FUTURE_STATE_ARCHITECTURE.md'
    if os.path.exists(future_doc):
        with open(future_doc, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Extract components
            component_matches = re.findall(r'component[:\s]+([^\n]+)', content, re.IGNORECASE)
            future_arch['components'] = [c.strip() for c in component_matches]
            
            # Extract interfaces
            interface_matches = re.findall(r'interface[:\s]+([^\n]+)', content, re.IGNORECASE)
            future_arch['interfaces'] = [i.strip() for i in interface_matches]
            
            # Extract SLOs
            slo_matches = re.findall(r'SLO[:\s]+([^\n]+)', content, re.IGNORECASE)
            future_arch['slos'] = [s.strip() for s in slo_matches]
    
    return future_arch

def generate_architecture_proposal():
    """Generate new architecture proposal"""
    current = analyze_current_architecture()
    future = analyze_future_state_architecture()
    
    proposal = {
        'timestamp': datetime.now().isoformat(),
        'current_architecture': current,
        'future_state_architecture': future,
        'proposed_architecture': {
            'services': [
                'api-gateway (enhanced)',
                'user-service (new)',
                'analytics-service (new)',
                'notification-service (new)',
                'export-service (new)',
                'policy-analysis-service (new)'
            ],
            'databases': [
                'PostgreSQL (openparliament + user + analytics schemas)',
                'Redis (caching + sessions)',
                'Elasticsearch (search + analytics)',
                'MongoDB (document storage)'
            ],
            'apis': [
                'REST API Gateway (enhanced)',
                'GraphQL API (new)',
                'WebSocket API (new)',
                'gRPC API (new)'
            ],
            'components': [
                'Authentication & Authorization',
                'User Management',
                'Advanced Analytics',
                'Data Visualization',
                'Multi-language Support',
                'Export/Import Engine',
                'Notification System',
                'Policy Analysis Engine'
            ]
        },
        'alignment_matrix': {
            'current_vs_proposed': {},
            'proposed_vs_future': {},
            'gaps': [],
            'decisions': [],
            'risks': [],
            'mitigations': []
        }
    }
    
    # Build alignment matrix
    for service in current['services']:
        if service in proposal['proposed_architecture']['services']:
            proposal['alignment_matrix']['current_vs_proposed'][service] = 'enhanced'
        else:
            proposal['alignment_matrix']['current_vs_proposed'][service] = 'maintained'
    
    # Identify gaps
    for future_comp in future.get('components', []):
        if not any(future_comp.lower() in prop_comp.lower() for prop_comp in proposal['proposed_architecture']['components']):
            proposal['alignment_matrix']['gaps'].append(future_comp)
    
    return proposal

def main():
    """Main architecture synthesis function"""
    print("=== LOOP D: ARCHITECTURE SYNTHESIS & ALIGNMENT ===")
    
    # Generate architecture proposal
    proposal = generate_architecture_proposal()
    
    # Save results
    os.makedirs('reports', exist_ok=True)
    with open('reports/architecture_proposal.json', 'w') as f:
        json.dump(proposal, f, indent=2)
    
    print("Architecture synthesis completed")
    print("Results saved to reports/architecture_proposal.json")
    
    # Print summary
    print(f"\n=== SUMMARY ===")
    print(f"Current services: {len(proposal['current_architecture']['services'])}")
    print(f"Proposed services: {len(proposal['proposed_architecture']['services'])}")
    print(f"Future components: {len(proposal['future_state_architecture']['components'])}")
    print(f"Alignment gaps: {len(proposal['alignment_matrix']['gaps'])}")

if __name__ == "__main__":
    main()
