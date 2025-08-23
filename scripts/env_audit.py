#!/usr/bin/env python3
"""
Environment Audit Tool
Enumerates running services, ports, health, configs, and error patterns
"""

import json
import subprocess
import socket
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import defaultdict
import argparse
from datetime import datetime
import re

# Try to import optional modules
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("Warning: requests module not available, some health checks will be skipped")

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("Warning: psutil module not available, resource monitoring will be limited")


class EnvironmentAuditor:
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path).resolve()
        self.services = []
        self.errors = defaultdict(list)
        self.config_diffs = []
        
    def check_docker_services(self) -> List[Dict[str, Any]]:
        """Check Docker container status"""
        services = []
        
        try:
            # Get running containers
            result = subprocess.run(
                ['docker', 'ps', '--format', '{{json .}}'],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.strip().split('\n'):
                if line:
                    container = json.loads(line)
                    
                    # Get detailed container info
                    inspect_result = subprocess.run(
                        ['docker', 'inspect', container['ID']],
                        capture_output=True,
                        text=True
                    )
                    
                    if inspect_result.returncode == 0:
                        details = json.loads(inspect_result.stdout)[0]
                        
                        # Extract health status
                        health_status = 'unknown'
                        if 'Health' in details['State']:
                            health_status = details['State']['Health']['Status']
                        
                        # Extract port mappings
                        ports = []
                        if details['NetworkSettings']['Ports']:
                            for internal, mappings in details['NetworkSettings']['Ports'].items():
                                if mappings:
                                    for mapping in mappings:
                                        ports.append({
                                            'internal': internal,
                                            'external': f"{mapping['HostIp']}:{mapping['HostPort']}"
                                        })
                        
                        service = {
                            'name': container['Names'],
                            'id': container['ID'][:12],
                            'image': container['Image'],
                            'status': container['Status'],
                            'health': health_status,
                            'created': container['CreatedAt'],
                            'ports': ports,
                            'labels': details['Config']['Labels'],
                            'env_vars': [e.split('=')[0] for e in details['Config']['Env'] if '=' in e],
                            'mounts': details['Mounts'],
                            'restart_policy': details['HostConfig']['RestartPolicy']
                        }
                        
                        services.append(service)
                        
        except subprocess.CalledProcessError as e:
            print(f"Error checking Docker services: {e}")
        except FileNotFoundError:
            print("Docker not found. Skipping container checks.")
            
        return services
    
    def check_system_services(self) -> List[Dict[str, Any]]:
        """Check system services (systemd/init.d)"""
        services = []
        
        # Check systemd services
        try:
            result = subprocess.run(
                ['systemctl', 'list-units', '--type=service', '--all', '--no-pager', '--plain'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n')[1:]:  # Skip header
                    parts = line.split()
                    if len(parts) >= 4:
                        service = {
                            'name': parts[0],
                            'load': parts[1],
                            'active': parts[2],
                            'sub': parts[3],
                            'type': 'systemd',
                            'description': ' '.join(parts[4:]) if len(parts) > 4 else ''
                        }
                        services.append(service)
                        
        except FileNotFoundError:
            print("systemctl not found. Skipping systemd service checks.")
            
        return services
    
    def check_ports(self) -> List[Dict[str, Any]]:
        """Check listening ports"""
        ports = []
        
        try:
            # Use netstat or ss
            commands = [
                ['ss', '-tlnp'],
                ['netstat', '-tlnp']
            ]
            
            for cmd in commands:
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        # Parse output
                        for line in result.stdout.strip().split('\n')[1:]:  # Skip header
                            if 'LISTEN' in line:
                                parts = line.split()
                                if len(parts) >= 4:
                                    local_addr = parts[3]
                                    # Extract port
                                    if ':' in local_addr:
                                        port_num = local_addr.split(':')[-1]
                                        ports.append({
                                            'port': port_num,
                                            'address': local_addr,
                                            'protocol': 'tcp',
                                            'state': 'LISTEN'
                                        })
                        break
                except:
                    continue
                    
        except Exception as e:
            print(f"Error checking ports: {e}")
            
        # Also check common application ports
        common_ports = {
            80: 'HTTP',
            443: 'HTTPS',
            3000: 'React Dev Server',
            5000: 'Flask',
            5432: 'PostgreSQL',
            6379: 'Redis',
            8000: 'Django',
            8080: 'API Gateway',
            8082: 'User Service',
            8585: 'OpenMetadata',
            9200: 'Elasticsearch',
            9300: 'Elasticsearch Cluster'
        }
        
        for port, service in common_ports.items():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                ports.append({
                    'port': port,
                    'service': service,
                    'status': 'open',
                    'checked_at': datetime.now().isoformat()
                })
                
        return ports
    
    def check_service_health(self) -> List[Dict[str, Any]]:
        """Check health endpoints"""
        health_checks = []
        
        if not HAS_REQUESTS:
            # Use curl as fallback
            endpoints = [
                ('http://localhost:8080/healthz', 'API Gateway'),
                ('http://localhost:8082/health', 'User Service'),
                ('http://localhost:8585/api/v1/system/version', 'OpenMetadata'),
                ('http://localhost:9200/_cluster/health', 'Elasticsearch'),
                ('http://localhost:3000', 'Frontend')
            ]
            
            for url, service in endpoints:
                try:
                    result = subprocess.run(
                        ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', url],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if result.returncode == 0:
                        status_code = int(result.stdout.strip()) if result.stdout.strip().isdigit() else 0
                        health_checks.append({
                            'service': service,
                            'url': url,
                            'status_code': status_code,
                            'healthy': 200 <= status_code < 400,
                            'checked_at': datetime.now().isoformat()
                        })
                    else:
                        health_checks.append({
                            'service': service,
                            'url': url,
                            'healthy': False,
                            'error': 'Connection failed',
                            'checked_at': datetime.now().isoformat()
                        })
                except Exception as e:
                    health_checks.append({
                        'service': service,
                        'url': url,
                        'healthy': False,
                        'error': str(e),
                        'checked_at': datetime.now().isoformat()
                    })
        else:
            endpoints = [
                ('http://localhost:8080/healthz', 'API Gateway'),
                ('http://localhost:8082/health', 'User Service'),
                ('http://localhost:8585/api/v1/system/version', 'OpenMetadata'),
                ('http://localhost:9200/_cluster/health', 'Elasticsearch'),
                ('http://localhost:3000', 'Frontend'),
                ('http://localhost:5432', 'PostgreSQL')  # Will fail but we check connection
            ]
            
            for url, service in endpoints:
                try:
                    response = requests.get(url, timeout=5)
                    health_checks.append({
                        'service': service,
                        'url': url,
                        'status_code': response.status_code,
                        'healthy': response.status_code < 400,
                        'response_time': response.elapsed.total_seconds(),
                        'checked_at': datetime.now().isoformat()
                    })
                except requests.exceptions.ConnectionError:
                    health_checks.append({
                        'service': service,
                        'url': url,
                        'healthy': False,
                        'error': 'Connection refused',
                        'checked_at': datetime.now().isoformat()
                    })
                except Exception as e:
                    health_checks.append({
                        'service': service,
                        'url': url,
                        'healthy': False,
                        'error': str(e),
                        'checked_at': datetime.now().isoformat()
                    })
                
        return health_checks
    
    def analyze_logs(self) -> Dict[str, Any]:
        """Analyze recent logs for error patterns"""
        log_analysis = {
            'error_classes': defaultdict(int),
            'error_rates': {},
            'recent_errors': []
        }
        
        # Docker logs
        try:
            result = subprocess.run(
                ['docker', 'ps', '--format', '{{.Names}}'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                containers = result.stdout.strip().split('\n')
                
                for container in containers:
                    if container:
                        # Get last 1000 lines of logs
                        log_result = subprocess.run(
                            ['docker', 'logs', '--tail', '1000', container],
                            capture_output=True,
                            text=True
                        )
                        
                        if log_result.returncode == 0:
                            logs = log_result.stdout + log_result.stderr
                            
                            # Count error patterns
                            error_patterns = {
                                'ERROR': r'(?i)error[:\s]',
                                'EXCEPTION': r'(?i)exception[:\s]',
                                'FAILED': r'(?i)failed[:\s]',
                                'CRITICAL': r'(?i)critical[:\s]',
                                'WARNING': r'(?i)warning[:\s]',
                                'TIMEOUT': r'(?i)timeout',
                                'CONNECTION_ERROR': r'(?i)connection\s+(refused|error)',
                                'AUTH_ERROR': r'(?i)(auth|permission|forbidden)',
                                'DATABASE_ERROR': r'(?i)(database|sql|query)\s+error',
                                'NOT_FOUND': r'(?i)not\s+found|404'
                            }
                            
                            for error_class, pattern in error_patterns.items():
                                matches = len(re.findall(pattern, logs))
                                if matches > 0:
                                    log_analysis['error_classes'][f"{container}_{error_class}"] = matches
                                    
                            # Extract recent errors
                            for match in re.finditer(r'(?i)(error|exception|failed).*', logs):
                                error_line = match.group(0)[:200]  # Limit length
                                log_analysis['recent_errors'].append({
                                    'container': container,
                                    'message': error_line,
                                    'type': 'docker_log'
                                })
                                if len(log_analysis['recent_errors']) >= 50:
                                    break
                                    
        except Exception as e:
            print(f"Error analyzing Docker logs: {e}")
            
        # System logs
        system_logs = [
            '/var/log/syslog',
            '/var/log/messages',
            '/var/log/nginx/error.log',
            '/var/log/apache2/error.log'
        ]
        
        for log_path in system_logs:
            if os.path.exists(log_path):
                try:
                    # Read last 1000 lines
                    result = subprocess.run(
                        ['tail', '-n', '1000', log_path],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        for match in re.finditer(r'(?i)(error|critical|failed).*', result.stdout):
                            log_analysis['recent_errors'].append({
                                'file': log_path,
                                'message': match.group(0)[:200],
                                'type': 'system_log'
                            })
                            if len(log_analysis['recent_errors']) >= 100:
                                break
                                
                except Exception as e:
                    print(f"Error reading {log_path}: {e}")
                    
        return dict(log_analysis)
    
    def check_configurations(self) -> List[Dict[str, Any]]:
        """Check for configuration files and environment variables"""
        configs = []
        
        # Check .env files
        env_files = [
            '.env',
            '.env.local',
            '.env.production',
            '.env.development'
        ]
        
        for env_file in env_files:
            env_path = self.root_path / env_file
            if env_path.exists():
                configs.append({
                    'file': env_file,
                    'type': 'env',
                    'exists': True,
                    'size': env_path.stat().st_size,
                    'modified': datetime.fromtimestamp(env_path.stat().st_mtime).isoformat()
                })
                
        # Check config files
        config_patterns = [
            '**/config.json',
            '**/config.yaml',
            '**/config.yml',
            '**/settings.py',
            '**/docker-compose*.yml',
            '**/nginx.conf',
            '**/.gitignore'
        ]
        
        for pattern in config_patterns:
            for config_path in self.root_path.glob(pattern):
                if not any(skip in str(config_path) for skip in ['node_modules', 'venv', '.git']):
                    configs.append({
                        'file': str(config_path.relative_to(self.root_path)),
                        'type': config_path.suffix[1:] if config_path.suffix else 'unknown',
                        'exists': True,
                        'size': config_path.stat().st_size,
                        'modified': datetime.fromtimestamp(config_path.stat().st_mtime).isoformat()
                    })
                    
        return configs
    
    def check_resources(self) -> Dict[str, Any]:
        """Check system resource usage"""
        resources = {}
        
        try:
            if HAS_PSUTIL:
                # CPU usage
                resources['cpu'] = {
                    'percent': psutil.cpu_percent(interval=1),
                    'count': psutil.cpu_count(),
                    'load_avg': os.getloadavg()
                }
                
                # Memory usage
                mem = psutil.virtual_memory()
                resources['memory'] = {
                    'total': mem.total,
                    'available': mem.available,
                    'percent': mem.percent,
                    'used': mem.used
                }
                
                # Disk usage
                disk = psutil.disk_usage('/')
                resources['disk'] = {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': disk.percent
                }
            else:
                # Use system commands as fallback
                try:
                    # CPU load average
                    resources['cpu'] = {
                        'load_avg': os.getloadavg()
                    }
                    
                    # Get CPU count
                    cpu_result = subprocess.run(['nproc'], capture_output=True, text=True)
                    if cpu_result.returncode == 0:
                        resources['cpu']['count'] = int(cpu_result.stdout.strip())
                except:
                    pass
                
                # Memory using free command
                try:
                    mem_result = subprocess.run(['free', '-b'], capture_output=True, text=True)
                    if mem_result.returncode == 0:
                        lines = mem_result.stdout.strip().split('\n')
                        if len(lines) > 1:
                            mem_parts = lines[1].split()
                            if len(mem_parts) >= 3:
                                total = int(mem_parts[1])
                                used = int(mem_parts[2])
                                resources['memory'] = {
                                    'total': total,
                                    'used': used,
                                    'percent': (used / total * 100) if total > 0 else 0
                                }
                except:
                    pass
                
                # Disk usage using df
                try:
                    disk_result = subprocess.run(['df', '-B1', '/'], capture_output=True, text=True)
                    if disk_result.returncode == 0:
                        lines = disk_result.stdout.strip().split('\n')
                        if len(lines) > 1:
                            disk_parts = lines[1].split()
                            if len(disk_parts) >= 4:
                                resources['disk'] = {
                                    'total': int(disk_parts[1]),
                                    'used': int(disk_parts[2]),
                                    'free': int(disk_parts[3]),
                                    'percent': float(disk_parts[4].strip('%'))
                                }
                except:
                    pass
            
            # Docker stats
            try:
                result = subprocess.run(
                    ['docker', 'stats', '--no-stream', '--format', '{{json .}}'],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    docker_stats = []
                    for line in result.stdout.strip().split('\n'):
                        if line:
                            docker_stats.append(json.loads(line))
                    resources['docker_containers'] = docker_stats
            except:
                pass
                
        except Exception as e:
            print(f"Error checking resources: {e}")
            
        return resources
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive environment audit report"""
        print("Checking Docker services...")
        docker_services = self.check_docker_services()
        
        print("Checking system services...")
        system_services = self.check_system_services()
        
        print("Checking ports...")
        ports = self.check_ports()
        
        print("Checking service health...")
        health_checks = self.check_service_health()
        
        print("Analyzing logs...")
        log_analysis = self.analyze_logs()
        
        print("Checking configurations...")
        configs = self.check_configurations()
        
        print("Checking resources...")
        resources = self.check_resources()
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'docker_services': docker_services,
            'system_services': system_services,
            'ports': ports,
            'health_checks': health_checks,
            'log_analysis': log_analysis,
            'configurations': configs,
            'resources': resources,
            'summary': {
                'total_docker_containers': len(docker_services),
                'healthy_containers': len([s for s in docker_services if s.get('health') == 'healthy']),
                'total_open_ports': len(ports),
                'total_errors_found': sum(log_analysis.get('error_classes', {}).values()),
                'healthy_services': len([h for h in health_checks if h.get('healthy')])
            }
        }
        
        return report
    
    def export_markdown(self, report: Dict[str, Any], output_path: str):
        """Export report as markdown"""
        with open(output_path, 'w') as f:
            f.write("# Environment Audit Report\n\n")
            f.write(f"Generated: {report['generated_at']}\n\n")
            
            f.write("## Summary\n\n")
            summary = report['summary']
            f.write(f"- Docker Containers: {summary['total_docker_containers']} "
                   f"(Healthy: {summary['healthy_containers']})\n")
            f.write(f"- Open Ports: {summary['total_open_ports']}\n")
            f.write(f"- Service Health Checks: {summary['healthy_services']} healthy\n")
            f.write(f"- Total Errors Found: {summary['total_errors_found']}\n\n")
            
            f.write("## Docker Services\n\n")
            if report['docker_services']:
                for service in report['docker_services']:
                    f.write(f"### {service['name']}\n")
                    f.write(f"- **Status**: {service['status']}\n")
                    f.write(f"- **Health**: {service['health']}\n")
                    f.write(f"- **Image**: {service['image']}\n")
                    if service['ports']:
                        f.write("- **Ports**:\n")
                        for port in service['ports']:
                            f.write(f"  - {port['internal']} → {port['external']}\n")
                    f.write("\n")
            else:
                f.write("No Docker services found.\n\n")
            
            f.write("## Service Health Checks\n\n")
            for check in report['health_checks']:
                status = "✅" if check.get('healthy') else "❌"
                f.write(f"- {status} **{check['service']}**: ")
                if check.get('healthy'):
                    f.write(f"Healthy (Status: {check.get('status_code')}, "
                           f"Response Time: {check.get('response_time', 0):.2f}s)\n")
                else:
                    f.write(f"Unhealthy ({check.get('error', 'Unknown error')})\n")
            f.write("\n")
            
            f.write("## Open Ports\n\n")
            if report['ports']:
                f.write("| Port | Service | Status |\n")
                f.write("|------|---------|--------|\n")
                for port in sorted(report['ports'], key=lambda x: int(x.get('port', 0))):
                    f.write(f"| {port.get('port')} | {port.get('service', 'Unknown')} | "
                           f"{port.get('status', 'open')} |\n")
                f.write("\n")
            
            f.write("## Error Analysis\n\n")
            if report['log_analysis']['error_classes']:
                f.write("### Error Classes\n\n")
                for error_class, count in sorted(
                    report['log_analysis']['error_classes'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:20]:
                    f.write(f"- {error_class}: {count} occurrences\n")
                f.write("\n")
            
            f.write("### Recent Errors\n\n")
            for error in report['log_analysis']['recent_errors'][:10]:
                f.write(f"- **{error.get('container', error.get('file', 'Unknown'))}**: "
                       f"{error['message']}\n")
            f.write("\n")
            
            f.write("## Resource Usage\n\n")
            if report['resources']:
                res = report['resources']
                if 'cpu' in res:
                    cpu_info = []
                    if 'percent' in res['cpu']:
                        cpu_info.append(f"{res['cpu']['percent']}%")
                    if 'load_avg' in res['cpu']:
                        cpu_info.append(f"Load: {res['cpu']['load_avg']}")
                    if 'count' in res['cpu']:
                        cpu_info.append(f"CPUs: {res['cpu']['count']}")
                    if cpu_info:
                        f.write(f"- **CPU**: {' | '.join(cpu_info)}\n")
                        
                if 'memory' in res:
                    if 'percent' in res['memory']:
                        f.write(f"- **Memory**: {res['memory']['percent']:.1f}% ")
                        if 'used' in res['memory'] and 'total' in res['memory']:
                            f.write(f"({res['memory']['used'] / (1024**3):.1f}GB / "
                                   f"{res['memory']['total'] / (1024**3):.1f}GB)")
                        f.write("\n")
                    elif 'used' in res['memory'] and 'total' in res['memory']:
                        f.write(f"- **Memory**: {res['memory']['used'] / (1024**3):.1f}GB / "
                               f"{res['memory']['total'] / (1024**3):.1f}GB\n")
                        
                if 'disk' in res:
                    f.write(f"- **Disk**: {res['disk']['percent']:.1f}% "
                           f"({res['disk']['used'] / (1024**3):.1f}GB / "
                           f"{res['disk']['total'] / (1024**3):.1f}GB)\n")
                f.write("\n")
            
            f.write("## Configuration Files\n\n")
            config_types = defaultdict(list)
            for config in report['configurations']:
                config_types[config['type']].append(config)
            
            for config_type, configs in sorted(config_types.items()):
                f.write(f"### {config_type.upper()} Files\n")
                for config in sorted(configs, key=lambda x: x['file'])[:10]:
                    f.write(f"- `{config['file']}` "
                           f"(Modified: {config['modified'][:10]})\n")
                if len(configs) > 10:
                    f.write(f"- ... and {len(configs) - 10} more\n")
                f.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Audit environment and services")
    parser.add_argument("--root", default=".", help="Root directory")
    parser.add_argument("--output-dir", default="reports", help="Output directory")
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Run audit
    auditor = EnvironmentAuditor(args.root)
    report = auditor.generate_report()
    
    # Export
    json_path = output_dir / "ENVIRONMENT_AUDIT.json"
    md_path = output_dir / "ENVIRONMENT_AUDIT.md"
    
    with open(json_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    auditor.export_markdown(report, str(md_path))
    
    print(f"\nEnvironment Audit Complete:")
    print(f"  Reports saved to:")
    print(f"    - {json_path}")
    print(f"    - {md_path}")


if __name__ == "__main__":
    main()