"""
Metrics for Merge V2 API Gateway
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
import time

# Request metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration'
)

# Database metrics
DB_CONNECTION_GAUGE = Gauge(
    'db_connections_active',
    'Active database connections'
)

DB_QUERY_DURATION = Histogram(
    'db_query_duration_seconds',
    'Database query duration'
)

# Business metrics
ENTITIES_CREATED = Counter(
    'entities_created_total',
    'Total entities created',
    ['entity_type']
)

ENTITIES_UPDATED = Counter(
    'entities_updated_total',
    'Total entities updated',
    ['entity_type']
)

ENTITIES_DELETED = Counter(
    'entities_deleted_total',
    'Total entities deleted',
    ['entity_type']
)

# Cache metrics
CACHE_HITS = Counter(
    'cache_hits_total',
    'Total cache hits'
)

CACHE_MISSES = Counter(
    'cache_misses_total',
    'Total cache misses'
)

def setup_metrics(app: FastAPI):
    """Setup metrics for the FastAPI application"""
    
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Record metrics
        duration = time.time() - start_time
        endpoint = request.url.path
        
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()
        
        REQUEST_DURATION.observe(duration)
        
        return response

def get_metrics():
    """Get current metrics"""
    return generate_latest()
