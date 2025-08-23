#!/usr/bin/env python3
"""
Environment Audit Script
Checks running services, ports, health, and configuration
"""

import os
import json
import subprocess
from datetime import datetime

def check_docker_services():
    """Check Docker services status"""
    try:
        result = subprocess.run(['docker-compose', 'ps'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
    except FileNotFoundError:
        return "Docker Compose not available"

def check_service_health():
    """Check service health endpoints"""
    health_checks = {
        'API Gateway': 'http://localhost:8000/healthz',
        'OpenMetadata Server': 'http://localhost:8585/api/v1/system/version',
        'OpenMetadata Ingestion': 'http://localhost:8080/health'
    }
    
    results = {}
    for service, url in health_checks.items():
        try:
            result = subprocess.run(['curl', '-s', '-f', url], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                results[service] = {'status': 'healthy', 'response': result.stdout[:100]}
            else:
                results[service] = {'status': 'unhealthy', 'error': result.stderr}
        except Exception as e:
            results[service] = {'status': 'error', 'error': str(e)}
    
    return results

def check_ports():
    """Check which ports are in use"""
    try:
        result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
    except FileNotFoundError:
        return "netstat not available"

def main():
    """Main audit function"""
    print("=== ENVIRONMENT AUDIT ===")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    audit_results = {
        'timestamp': datetime.now().isoformat(),
        'docker_services': check_docker_services(),
        'service_health': check_service_health(),
        'ports': check_ports(),
        'environment': {
            'PWD': os.getcwd(),
            'USER': os.environ.get('USER', 'unknown'),
            'PATH': os.environ.get('PATH', 'unknown')
        }
    }
    
    # Save results
    os.makedirs('reports', exist_ok=True)
    with open('reports/environment_audit.json', 'w') as f:
        json.dump(audit_results, f, indent=2)
    
    print("Environment audit completed")
    print("Results saved to reports/environment_audit.json")
    
    # Print summary
    print("\n=== SUMMARY ===")
    print("Docker services checked")
    print("Service health checked")
    print("Ports checked")
    print("Environment variables captured")

if __name__ == "__main__":
    main()
