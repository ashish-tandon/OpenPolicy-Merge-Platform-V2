"""
Monitoring Dashboard Backend API

Provides real-time container and service monitoring information
"""

import asyncio
import json
import subprocess
import time
from datetime import datetime
from typing import Dict, List, Any
import docker
import psutil
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Monitoring Dashboard API",
    description="Real-time system monitoring and health status API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
docker_client = None
last_update = None
cache_duration = 5  # seconds

def get_docker_client():
    """Get Docker client instance"""
    global docker_client
    if docker_client is None:
        try:
            docker_client = docker.from_env()
        except Exception as e:
            logger.error(f"Failed to connect to Docker: {e}")
            return None
    return docker_client

def get_container_info(container) -> Dict[str, Any]:
    """Extract container information"""
    try:
        # Get container stats
        stats = container.stats(stream=False)
        
        # Calculate CPU and memory usage
        cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
        system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
        
        cpu_percent = 0.0
        if system_delta > 0:
            cpu_percent = (cpu_delta / system_delta) * len(stats['cpu_stats']['cpu_usage']['percpu_usage']) * 100.0
        
        # Memory usage
        memory_usage = stats['memory_stats']['usage']
        memory_limit = stats['memory_stats']['limit']
        memory_percent = (memory_usage / memory_limit) * 100.0 if memory_limit > 0 else 0.0
        
        # Network stats
        network_stats = stats.get('networks', {})
        network_rx = sum(net.get('rx_bytes', 0) for net in network_stats.values())
        network_tx = sum(net.get('tx_bytes', 0) for net in network_stats.values())
        
        return {
            "id": container.id,
            "name": container.name,
            "image": container.image.tags[0] if container.image.tags else container.image.id,
            "status": container.status,
            "state": container.status,
            "ports": format_ports(container.ports),
            "created": container.attrs['Created'],
            "cpu_percent": round(cpu_percent, 2),
            "memory_percent": round(memory_percent, 2),
            "memory_usage": format_bytes(memory_usage),
            "memory_limit": format_bytes(memory_limit),
            "network_rx": format_bytes(network_rx),
            "network_tx": format_bytes(network_tx),
            "health": get_container_health(container),
            "labels": container.labels,
            "command": container.attrs['Config']['Cmd'],
            "working_dir": container.attrs['Config']['WorkingDir'],
            "environment": container.attrs['Config']['Env'][:5] if container.attrs['Config']['Env'] else []
        }
    except Exception as e:
        logger.error(f"Error getting container info for {container.name}: {e}")
        return {
            "id": container.id,
            "name": container.name,
            "image": container.image.tags[0] if container.image.tags else container.image.id,
            "status": container.status,
            "state": container.status,
            "ports": format_ports(container.ports),
            "created": container.attrs['Created'],
            "error": str(e)
        }

def format_ports(ports: Dict) -> str:
    """Format container ports"""
    if not ports:
        return "N/A"
    
    formatted = []
    for container_port, host_bindings in ports.items():
        if host_bindings:
            for binding in host_bindings:
                formatted.append(f"{binding['HostPort']}:{container_port}")
        else:
            formatted.append(container_port)
    
    return ", ".join(formatted)

def format_bytes(bytes_value: int) -> str:
    """Format bytes to human readable format"""
    if bytes_value == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    while bytes_value >= 1024 and unit_index < len(units) - 1:
        bytes_value /= 1024.0
        unit_index += 1
    
    return f"{bytes_value:.1f} {units[unit_index]}"

def get_container_health(container) -> str:
    """Get container health status"""
    try:
        health = container.attrs['State'].get('Health', {})
        if health:
            return health.get('Status', 'unknown')
        return 'healthy' if container.status == 'running' else 'unhealthy'
    except:
        return 'unknown'

def get_system_resources() -> Dict[str, Any]:
    """Get system resource usage"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Network I/O
        network = psutil.net_io_counters()
        network_rx = format_bytes(network.bytes_recv)
        network_tx = format_bytes(network.bytes_sent)
        
        return {
            "cpu": round(cpu_percent, 2),
            "memory": round(memory.percent, 2),
            "memory_used": format_bytes(memory.used),
            "memory_total": format_bytes(memory.total),
            "disk": round(disk.percent, 2),
            "disk_used": format_bytes(disk.used),
            "disk_total": format_bytes(disk.total),
            "network_rx": network_rx,
            "network_tx": network_tx,
            "network": f"{network_rx}/s ↓ {network_tx}/s ↑"
        }
    except Exception as e:
        logger.error(f"Error getting system resources: {e}")
        return {"error": str(e)}

async def check_service_health(service_name: str, url: str) -> Dict[str, Any]:
    """Check service health endpoint"""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        response_time = (time.time() - start_time) * 1000
        
        return {
            "name": service_name,
            "url": url,
            "status": "healthy" if response.status_code < 400 else "unhealthy",
            "status_code": response.status_code,
            "response_time": round(response_time, 2),
            "last_check": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "name": service_name,
            "url": url,
            "status": "error",
            "error": str(e),
            "last_check": datetime.now().isoformat()
        }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Monitoring Dashboard API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/containers - Get container information",
            "/services - Get service health status",
            "/resources - Get system resource usage",
            "/health - Get API health status"
        ]
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "docker_connected": get_docker_client() is not None
    }

@app.get("/containers")
async def get_containers():
    """Get all container information"""
    try:
        client = get_docker_client()
        if not client:
            raise HTTPException(status_code=500, detail="Docker not accessible")
        
        containers = []
        for container in client.containers.list(all=True):
            container_info = get_container_info(container)
            containers.append(container_info)
        
        return {
            "containers": containers,
            "total": len(containers),
            "running": len([c for c in containers if c['state'] == 'running']),
            "stopped": len([c for c in containers if c['state'] == 'stopped']),
            "restarting": len([c for c in containers if c['state'] == 'restarting']),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting containers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/services")
async def get_services():
    """Get service health status"""
    try:
        # Define services to check
        services = [
            {"name": "API Gateway", "url": "http://api-gateway:8000/healthz"},
            {"name": "User Service", "url": "http://user-service:8000/health"},
            {"name": "ETL Service", "url": "http://etl:8083/health"},
            {"name": "Web UI", "url": "http://web-ui:80/"},
            {"name": "Database", "url": "http://db:5432"}
        ]
        
        # Check all services concurrently
        health_checks = []
        for service in services:
            health_check = await check_service_health(service["name"], service["url"])
            health_checks.append(health_check)
        
        healthy_count = len([s for s in health_checks if s['status'] == 'healthy'])
        total_count = len(health_checks)
        
        return {
            "services": health_checks,
            "total": total_count,
            "healthy": healthy_count,
            "unhealthy": total_count - healthy_count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting services: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/resources")
async def get_resources():
    """Get system resource usage"""
    try:
        resources = get_system_resources()
        resources["timestamp"] = datetime.now().isoformat()
        return resources
    except Exception as e:
        logger.error(f"Error getting resources: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs/{container_name}")
async def get_container_logs(container_name: str, tail: int = 100):
    """Get container logs"""
    try:
        client = get_docker_client()
        if not client:
            raise HTTPException(status_code=500, detail="Docker not accessible")
        
        try:
            container = client.containers.get(container_name)
            logs = container.logs(tail=tail, timestamps=True).decode('utf-8')
            
            # Parse logs into structured format
            log_entries = []
            for line in logs.strip().split('\n'):
                if line:
                    try:
                        # Docker logs format: 2024-01-01T12:00:00.000000000Z message
                        timestamp_end = line.find(' ')
                        if timestamp_end > 0:
                            timestamp = line[:timestamp_end]
                            message = line[timestamp_end + 1:]
                            log_entries.append({
                                "timestamp": timestamp,
                                "message": message,
                                "level": "info"
                            })
                    except:
                        log_entries.append({
                            "timestamp": datetime.now().isoformat(),
                            "message": line,
                            "level": "info"
                        })
            
            return {
                "container": container_name,
                "logs": log_entries,
                "total": len(log_entries),
                "timestamp": datetime.now().isoformat()
            }
        except docker.errors.NotFound:
            raise HTTPException(status_code=404, detail=f"Container {container_name} not found")
            
    except Exception as e:
        logger.error(f"Error getting container logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/{container_name}")
async def get_container_stats(container_name: str):
    """Get real-time container stats"""
    try:
        client = get_docker_client()
        if not client:
            raise HTTPException(status_code=500, detail="Docker not accessible")
        
        try:
            container = client.containers.get(container_name)
            stats = container.stats(stream=False)
            
            # Calculate CPU usage
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
            
            cpu_percent = 0.0
            if system_delta > 0:
                cpu_percent = (cpu_delta / system_delta) * len(stats['cpu_stats']['cpu_usage']['percpu_usage']) * 100.0
            
            # Memory usage
            memory_usage = stats['memory_stats']['usage']
            memory_limit = stats['memory_stats']['limit']
            memory_percent = (memory_usage / memory_limit) * 100.0 if memory_limit > 0 else 0.0
            
            # Network stats
            network_stats = stats.get('networks', {})
            network_rx = sum(net.get('rx_bytes', 0) for net in network_stats.values())
            network_tx = sum(net.get('tx_bytes', 0) for net in network_stats.values())
            
            return {
                "container": container_name,
                "cpu_percent": round(cpu_percent, 2),
                "memory_percent": round(memory_percent, 2),
                "memory_usage": format_bytes(memory_usage),
                "memory_limit": format_bytes(memory_limit),
                "network_rx": format_bytes(network_rx),
                "network_tx": format_bytes(network_tx),
                "timestamp": datetime.now().isoformat()
            }
        except docker.errors.NotFound:
            raise HTTPException(status_code=404, detail=f"Container {container_name} not found")
            
    except Exception as e:
        logger.error(f"Error getting container stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8083)
