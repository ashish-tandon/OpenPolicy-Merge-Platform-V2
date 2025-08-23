#!/usr/bin/env python3
"""
Routing Realignment & Optimization Script
Analyzes current routing and proposes optimized routing for new architecture
"""

import os
import json
import re
from datetime import datetime

def analyze_current_routing():
    """Analyze current routing from API files"""
    current_routes = {
        'api_v1': [],
        'health': [],
        'docs': [],
        'openapi': []
    }
    
    # Check API v1 routes
    api_v1_dir = 'services/api-gateway/app/api/v1'
    if os.path.exists(api_v1_dir):
        for file in os.listdir(api_v1_dir):
            if file.endswith('.py'):
                file_path = os.path.join(api_v1_dir, file)
                routes = extract_routes_from_file(file_path)
                current_routes['api_v1'].extend(routes)
    
    # Check main app for additional routes
    main_app = 'services/api-gateway/app/main.py'
    if os.path.exists(main_app):
        with open(main_app, 'r') as f:
            content = f.read()
            # Extract route registrations
            route_matches = re.findall(r'include_router\(([^)]+)\)', content)
            for match in route_matches:
                if 'api/v1' in match:
                    current_routes['api_v1'].append(match.strip())
    
    return current_routes

def extract_routes_from_file(file_path):
    """Extract routes from a single API file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        routes = []
        
        # Look for route decorators
        route_patterns = [
            r'@router\.(get|post|put|patch|delete)\(["\']([^"\']+)["\']',
            r'@app\.(get|post|put|patch|delete)\(["\']([^"\']+)["\']',
            r'@api_router\.(get|post|put|patch|delete)\(["\']([^"\']+)["\']'
        ]
        
        for pattern in route_patterns:
            matches = re.findall(pattern, content)
            for method, path in matches:
                routes.append({
                    'method': method.upper(),
                    'path': path,
                    'file': file_path
                })
        
        return routes
    except Exception:
        return []

def analyze_routing_performance():
    """Analyze routing performance characteristics"""
    performance = {
        'route_count': 0,
        'complexity': 'low',
        'optimization_opportunities': [],
        'bottlenecks': []
    }
    
    # Count total routes
    current_routes = analyze_current_routing()
    total_routes = len(current_routes['api_v1'])
    performance['route_count'] = total_routes
    
    # Assess complexity
    if total_routes < 20:
        performance['complexity'] = 'low'
    elif total_routes < 50:
        performance['complexity'] = 'medium'
    else:
        performance['complexity'] = 'high'
    
    # Identify optimization opportunities
    if total_routes > 0:
        performance['optimization_opportunities'].append('Route caching implementation')
        performance['optimization_opportunities'].append('Middleware optimization')
        performance['optimization_opportunities'].append('Load balancing configuration')
    
    return performance

def propose_optimized_routing():
    """Propose optimized routing structure"""
    current = analyze_current_routing()
    performance = analyze_routing_performance()
    
    proposal = {
        'timestamp': datetime.now().isoformat(),
        'current_routing': current,
        'performance_analysis': performance,
        'optimized_routing': {
            'api_gateway': {
                'health': '/healthz',
                'docs': '/docs',
                'openapi': '/openapi.json',
                'metrics': '/metrics',
                'status': '/status'
            },
            'api_v1': {
                'bills': '/api/v1/bills',
                'members': '/api/v1/members',
                'committees': '/api/v1/committees',
                'debates': '/api/v1/debates',
                'votes': '/api/v1/votes',
                'search': '/api/v1/search',
                'analytics': '/api/v1/analytics',
                'users': '/api/v1/users',
                'notifications': '/api/v1/notifications',
                'exports': '/api/v1/exports',
                'policy': '/api/v1/policy'
            },
            'api_v2': {
                'graphql': '/api/v2/graphql',
                'websocket': '/api/v2/ws',
                'grpc': '/api/v2/grpc'
            },
            'internal': {
                'admin': '/internal/admin',
                'monitoring': '/internal/monitoring',
                'debug': '/internal/debug'
            }
        },
        'routing_optimizations': [
            'Route caching with Redis',
            'Middleware optimization',
            'Load balancing configuration',
            'Rate limiting per endpoint',
            'Circuit breaker implementation',
            'Request/response compression',
            'API versioning strategy',
            'Deprecation handling'
        ],
        'performance_targets': {
            'response_time': '< 200ms (95th percentile)',
            'throughput': '10,000+ requests/second',
            'availability': '99.9% uptime',
            'error_rate': '< 0.1%'
        }
    }
    
    return proposal

def main():
    """Main routing realignment function"""
    print("=== LOOP E: ROUTING REALIGNMENT & OPTIMIZATION ===")
    
    # Generate routing proposal
    proposal = propose_optimized_routing()
    
    # Save results
    os.makedirs('reports', exist_ok=True)
    with open('reports/routing_realignment.json', 'w') as f:
        json.dump(proposal, f, indent=2)
    
    print("Routing realignment completed")
    print("Results saved to reports/routing_realignment.json")
    
    # Print summary
    print(f"\n=== SUMMARY ===")
    print(f"Current routes: {proposal['performance_analysis']['route_count']}")
    print(f"Complexity: {proposal['performance_analysis']['complexity']}")
    print(f"Optimizations proposed: {len(proposal['routing_optimizations'])}")
    print(f"Performance targets: {len(proposal['performance_targets'])}")

if __name__ == "__main__":
    main()
