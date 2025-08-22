# Monitoring and Observability

## Executive Summary
This document outlines the monitoring and observability strategy for the OpenPolicy V2 platform, ensuring system reliability, performance optimization, and rapid incident response.

## Architecture Overview

### Monitoring Stack
- **Metrics**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing**: Jaeger
- **Alerting**: Prometheus AlertManager + PagerDuty
- **Synthetic Monitoring**: Datadog Synthetics
- **Infrastructure**: Node Exporter, cAdvisor, Kubernetes Metrics

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Application │────▶│ Prometheus  │────▶│   Grafana   │
│   Metrics   │     │   Server    │     │ Dashboards  │
└─────────────┘     └─────────────┘     └─────────────┘
                            │
                            ▼
                    ┌─────────────┐     ┌─────────────┐
                    │AlertManager │────▶│  PagerDuty  │
                    └─────────────┘     └─────────────┘
```

## Metrics Collection

### Application Metrics

#### API Gateway Metrics
```python
# FastAPI metrics configuration
from prometheus_client import Counter, Histogram, Gauge
import time

# Request metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# Business metrics
bills_created_total = Counter(
    'bills_created_total',
    'Total bills created',
    ['jurisdiction', 'type']
)

active_users_gauge = Gauge(
    'active_users_count',
    'Number of active users'
)

# Database metrics
db_connection_pool_size = Gauge(
    'db_connection_pool_size',
    'Database connection pool size'
)

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration',
    ['query_type', 'table']
)
```

#### Scraper Metrics
```python
# ETL pipeline metrics
scraper_runs_total = Counter(
    'scraper_runs_total',
    'Total scraper runs',
    ['scraper', 'status']
)

scraper_duration_seconds = Histogram(
    'scraper_duration_seconds',
    'Scraper execution time',
    ['scraper']
)

records_scraped_total = Counter(
    'records_scraped_total',
    'Total records scraped',
    ['scraper', 'entity_type']
)

scraper_errors_total = Counter(
    'scraper_errors_total',
    'Total scraper errors',
    ['scraper', 'error_type']
)
```

### Infrastructure Metrics

#### Kubernetes Metrics
```yaml
# prometheus-config.yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'kubernetes-apiservers'
    kubernetes_sd_configs:
      - role: endpoints
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

#### Node Metrics
```bash
# Node exporter metrics
node_cpu_seconds_total
node_memory_MemAvailable_bytes
node_filesystem_avail_bytes
node_disk_io_time_seconds_total
node_network_receive_bytes_total
node_network_transmit_bytes_total
```

## Logging Strategy

### Log Levels and Standards
```python
# Structured logging configuration
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

# Usage example
logger = structlog.get_logger()

logger.info(
    "bill_created",
    bill_id=bill.id,
    title=bill.title,
    jurisdiction=bill.jurisdiction,
    user_id=current_user.id,
    duration_ms=processing_time
)
```

### Log Aggregation Pipeline
```yaml
# Logstash configuration
input {
  beats {
    port => 5044
  }
  
  # Kubernetes logs
  kubernetes {
    type => "kubernetes"
  }
}

filter {
  # Parse JSON logs
  if [message] =~ /^\{/ {
    json {
      source => "message"
    }
  }
  
  # Add geographic info for IPs
  geoip {
    source => "client_ip"
    target => "geoip"
  }
  
  # Parse user agent
  useragent {
    source => "user_agent"
    target => "ua"
  }
  
  # Extract custom fields
  mutate {
    add_field => {
      "environment" => "%{[kubernetes][namespace]}"
      "service" => "%{[kubernetes][labels][app]}"
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "openpolicy-%{+YYYY.MM.dd}"
  }
}
```

### Log Retention Policy
- **Application Logs**: 30 days
- **Access Logs**: 90 days
- **Error Logs**: 180 days
- **Security Logs**: 365 days
- **Audit Logs**: 7 years

## Distributed Tracing

### Jaeger Configuration
```yaml
# jaeger-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: jaeger-config
data:
  config.yaml: |
    service_name: openpolicy
    sampler:
      type: probabilistic
      param: 0.1  # Sample 10% of traces
    reporter:
      log_spans: false
      local_agent_host_port: jaeger-agent:6831
```

### Trace Implementation
```python
# OpenTelemetry setup
from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configure Jaeger exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger-agent",
    agent_port=6831,
)

# Add span processor
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Usage in application
@app.get("/api/v1/bills/{bill_id}")
async def get_bill(bill_id: str):
    with tracer.start_as_current_span("get_bill") as span:
        span.set_attribute("bill.id", bill_id)
        
        # Database query span
        with tracer.start_as_current_span("db_query"):
            bill = await db.get_bill(bill_id)
        
        # Cache check span
        with tracer.start_as_current_span("cache_lookup"):
            cached = await redis.get(f"bill:{bill_id}")
            
        return bill
```

## Alerting Rules

### Critical Alerts (P1)
```yaml
# prometheus-alerts.yaml
groups:
  - name: critical
    interval: 30s
    rules:
      # Service down
      - alert: ServiceDown
        expr: up{job="openpolicy"} == 0
        for: 2m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "Service {{ $labels.instance }} is down"
          description: "{{ $labels.instance }} has been down for more than 2 minutes"
          
      # High error rate
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} over the last 5 minutes"
          
      # Database connection pool exhausted
      - alert: DatabasePoolExhausted
        expr: db_connection_pool_available == 0
        for: 1m
        labels:
          severity: critical
          team: database
        annotations:
          summary: "Database connection pool exhausted"
          description: "No available database connections for {{ $labels.service }}"
```

### Warning Alerts (P2)
```yaml
      # High memory usage
      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.85
        for: 10m
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is {{ $value | humanizePercentage }}"
          
      # Slow API responses
      - alert: SlowAPIResponse
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 10m
        labels:
          severity: warning
          team: platform
        annotations:
          summary: "API responses are slow"
          description: "95th percentile response time is {{ $value }}s"
          
      # Scraper failures
      - alert: ScraperFailures
        expr: rate(scraper_errors_total[1h]) > 0.1
        for: 30m
        labels:
          severity: warning
          team: data
        annotations:
          summary: "High scraper failure rate"
          description: "Scraper {{ $labels.scraper }} failing at {{ $value }} errors/hour"
```

### SLO-Based Alerts
```yaml
      # Availability SLO
      - alert: AvailabilitySLOBreach
        expr: (1 - rate(http_requests_total{status=~"5.."}[1h])) < 0.995
        for: 5m
        labels:
          severity: warning
          team: platform
          slo: availability
        annotations:
          summary: "Availability SLO at risk"
          description: "Current availability: {{ $value | humanizePercentage }}, target: 99.5%"
          
      # Latency SLO
      - alert: LatencySLOBreach
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 10m
        labels:
          severity: warning
          team: platform
          slo: latency
        annotations:
          summary: "Latency SLO breach"
          description: "P95 latency is {{ $value }}s, target: < 1s"
```

## Dashboards

### System Overview Dashboard
```json
{
  "dashboard": {
    "title": "OpenPolicy System Overview",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [{
          "expr": "sum(rate(http_requests_total[5m])) by (service)"
        }]
      },
      {
        "title": "Error Rate",
        "targets": [{
          "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) by (service)"
        }]
      },
      {
        "title": "Response Time (P95)",
        "targets": [{
          "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))"
        }]
      },
      {
        "title": "Active Users",
        "targets": [{
          "expr": "active_users_count"
        }]
      }
    ]
  }
}
```

### Business Metrics Dashboard
```json
{
  "dashboard": {
    "title": "OpenPolicy Business Metrics",
    "panels": [
      {
        "title": "Bills Created Today",
        "targets": [{
          "expr": "increase(bills_created_total[1d])"
        }]
      },
      {
        "title": "Search Queries",
        "targets": [{
          "expr": "rate(search_queries_total[1h])"
        }]
      },
      {
        "title": "Most Viewed Bills",
        "targets": [{
          "expr": "topk(10, bill_views_total)"
        }]
      },
      {
        "title": "User Engagement",
        "targets": [{
          "expr": "rate(user_actions_total[1h]) by (action_type)"
        }]
      }
    ]
  }
}
```

### Infrastructure Dashboard
```json
{
  "dashboard": {
    "title": "Infrastructure Health",
    "panels": [
      {
        "title": "CPU Usage",
        "targets": [{
          "expr": "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
        }]
      },
      {
        "title": "Memory Usage",
        "targets": [{
          "expr": "(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100"
        }]
      },
      {
        "title": "Disk Usage",
        "targets": [{
          "expr": "(1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100"
        }]
      },
      {
        "title": "Network I/O",
        "targets": [{
          "expr": "rate(node_network_receive_bytes_total[5m])",
          "legendFormat": "RX - {{ instance }}"
        }, {
          "expr": "rate(node_network_transmit_bytes_total[5m])",
          "legendFormat": "TX - {{ instance }}"
        }]
      }
    ]
  }
}
```

## Synthetic Monitoring

### API Health Checks
```javascript
// Datadog Synthetics configuration
{
  "name": "OpenPolicy API Health Check",
  "type": "api",
  "subtype": "http",
  "config": {
    "request": {
      "url": "https://api.openpolicy.ca/health",
      "method": "GET",
      "timeout": 10
    },
    "assertions": [
      {
        "type": "statusCode",
        "operator": "is",
        "target": 200
      },
      {
        "type": "responseTime",
        "operator": "lessThan",
        "target": 1000
      },
      {
        "type": "body",
        "operator": "contains",
        "target": "\"status\":\"healthy\""
      }
    ]
  },
  "locations": ["aws:ca-central-1", "aws:us-east-1"],
  "options": {
    "tick_every": 60,
    "min_failure_duration": 120,
    "min_location_failed": 1
  }
}
```

### User Journey Tests
```javascript
// Critical user journey monitoring
{
  "name": "Search for MP by Postal Code",
  "type": "browser",
  "config": {
    "steps": [
      {
        "type": "goToUrl",
        "url": "https://openpolicy.ca"
      },
      {
        "type": "typeText",
        "selector": "[data-testid='search-input']",
        "text": "K1A 0A6"
      },
      {
        "type": "click",
        "selector": "[data-testid='search-submit']"
      },
      {
        "type": "waitForElement",
        "selector": "[data-testid='mp-result']",
        "timeout": 5000
      },
      {
        "type": "assertElementContent",
        "selector": "[data-testid='mp-name']",
        "content": ".*"
      }
    ]
  },
  "locations": ["aws:ca-central-1"],
  "options": {
    "device_ids": ["laptop_large", "mobile_small"],
    "tick_every": 300
  }
}
```

## Log Analysis Queries

### Common Kibana Queries
```json
// Find all 5xx errors
{
  "query": {
    "match": {
      "status": {
        "query": "5*"
      }
    }
  },
  "sort": [{"@timestamp": {"order": "desc"}}]
}

// Find slow queries
{
  "query": {
    "range": {
      "duration_ms": {
        "gte": 1000
      }
    }
  }
}

// User activity by geography
{
  "aggs": {
    "user_locations": {
      "terms": {
        "field": "geoip.country_name",
        "size": 50
      }
    }
  }
}

// Error rate by service
{
  "aggs": {
    "services": {
      "terms": {
        "field": "service"
      },
      "aggs": {
        "error_rate": {
          "filter": {
            "range": {
              "status": {
                "gte": 500
              }
            }
          }
        }
      }
    }
  }
}
```

## Performance Optimization

### Query Optimization Monitoring
```sql
-- Slow query log analysis
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    min_time,
    max_time
FROM pg_stat_statements
WHERE mean_time > 100  -- queries averaging > 100ms
ORDER BY mean_time DESC
LIMIT 20;

-- Missing indexes
SELECT
    schemaname,
    tablename,
    attname,
    n_distinct,
    most_common_vals
FROM pg_stats
WHERE schemaname = 'public'
    AND n_distinct > 100
    AND NOT EXISTS (
        SELECT 1 FROM pg_indexes
        WHERE tablename = pg_stats.tablename
        AND indexdef LIKE '%' || attname || '%'
    );
```

### Cache Hit Rates
```python
# Monitor Redis cache effectiveness
cache_hit_rate = Gauge(
    'cache_hit_rate',
    'Cache hit rate percentage',
    ['cache_type']
)

# Calculate and expose metrics
def update_cache_metrics():
    info = redis_client.info()
    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    total = hits + misses
    
    if total > 0:
        hit_rate = (hits / total) * 100
        cache_hit_rate.labels(cache_type='redis').set(hit_rate)
```

## Capacity Planning

### Resource Utilization Trends
```promql
# Predict when disk will be full
predict_linear(node_filesystem_avail_bytes[7d], 7*24*60*60) < 0

# CPU usage trend
avg_over_time(
  100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
[7d])

# Memory growth rate
deriv(node_memory_MemAvailable_bytes[1h])
```

### Scaling Triggers
```yaml
# HPA configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: openpolicy-api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-gateway
  minReplicas: 3
  maxReplicas: 50
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "1000"
```

## Incident Investigation Tools

### Log Correlation
```bash
# Find all logs related to a specific request ID
kubectl logs -l app=openpolicy --since=1h | grep "request_id=abc123"

# Aggregate errors by type
kubectl logs -l app=openpolicy --since=1h | \
  grep ERROR | \
  awk -F'error_type=' '{print $2}' | \
  awk '{print $1}' | \
  sort | uniq -c | sort -rn

# Find logs around a specific timestamp
kubectl logs -l app=openpolicy --since-time="2024-01-20T14:00:00Z" --until-time="2024-01-20T14:30:00Z"
```

### Trace Analysis
```python
# Find slow traces
from jaeger_client import Config

def get_slow_traces(service_name, min_duration_ms=1000):
    config = Config(
        config={
            'sampler': {'type': 'const', 'param': 1},
            'local_agent': {
                'reporting_host': 'jaeger-agent',
                'reporting_port': '6831',
            },
        },
        service_name=service_name,
    )
    
    tracer = config.initialize_tracer()
    
    # Query Jaeger for slow traces
    response = requests.get(
        f"http://jaeger-query:16686/api/traces",
        params={
            "service": service_name,
            "minDuration": f"{min_duration_ms}ms",
            "limit": 100
        }
    )
    
    return response.json()
```

## Continuous Improvement

### Weekly Review Metrics
1. **Availability**: Actual vs SLO target
2. **Performance**: P50, P95, P99 latencies
3. **Error Budget**: Remaining budget for the month
4. **Alert Noise**: False positive rate
5. **MTTR**: Mean time to recovery by incident type

### Monthly Reporting Template
```markdown
# OpenPolicy Monitoring Report - [Month Year]

## Executive Summary
- Overall availability: X%
- Average response time: Xms
- Total incidents: X (P1: X, P2: X)
- MTTR: X minutes

## Key Metrics
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Availability | 99.5% | X% | ✅/❌ |
| P95 Latency | <1s | Xs | ✅/❌ |
| Error Rate | <0.5% | X% | ✅/❌ |

## Incidents
| Date | Severity | Duration | Root Cause | Action Items |
|------|----------|----------|------------|--------------|
| | | | | |

## Improvements Implemented
- 
- 

## Planned Improvements
- 
- 
```