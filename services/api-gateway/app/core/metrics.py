from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
import time

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
DB_CONNECTION_GAUGE = Gauge('database_connections_active', 'Active database connections')
BUSINESS_ENTITIES_GAUGE = Gauge('business_entities_total', 'Total business entities')
CACHE_HIT_RATIO = Gauge('cache_hit_ratio', 'Cache hit ratio')

def setup_metrics(app: FastAPI):
    """Setup Prometheus metrics middleware."""
    
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
    
    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint."""
        return Response(
            content=generate_latest(),
            media_type="text/plain"
        )
