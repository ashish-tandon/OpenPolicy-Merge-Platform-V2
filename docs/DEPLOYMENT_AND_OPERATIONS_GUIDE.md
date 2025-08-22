# Deployment & Operations Guide
**Version**: 1.0  
**Created**: 2025-01-10  
**Iteration**: 1 of 3  
**Operations Depth**: 10x Comprehensive Guide

## Executive Summary

This guide provides comprehensive deployment and operational procedures for the OpenPolicy platform, covering CI/CD pipelines, infrastructure management, monitoring, incident response, and maintenance procedures. The guide ensures reliable, secure, and scalable operations supporting 99.99% uptime.

## 🚀 Deployment Architecture

### Environment Overview

```yaml
environments:
  development:
    purpose: Developer testing
    infrastructure: Kubernetes (dev cluster)
    url: https://dev.openpolicy.ca
    deployment: Continuous
    
  staging:
    purpose: Pre-production testing
    infrastructure: Kubernetes (staging cluster)
    url: https://staging.openpolicy.ca
    deployment: Daily
    
  production:
    purpose: Live environment
    infrastructure: Multi-region Kubernetes
    url: https://openpolicy.ca
    deployment: Blue-green with approval
    
  disaster_recovery:
    purpose: Failover environment
    infrastructure: Separate region
    url: https://dr.openpolicy.ca
    deployment: Synchronized
```

### Deployment Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deployment Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [api-gateway, user-service, etl-service, web-ui]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python/Node
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: |
          ~/.cache/pip
          ~/.npm
        key: ${{ runner.os }}-${{ matrix.service }}-${{ hashFiles('**/requirements.txt', '**/package-lock.json') }}
    
    - name: Install dependencies
      run: |
        cd services/${{ matrix.service }}
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        if [ -f package.json ]; then npm ci; fi
    
    - name: Run tests
      run: |
        cd services/${{ matrix.service }}
        if [ -f pytest.ini ]; then pytest --cov=. --cov-report=xml; fi
        if [ -f package.json ]; then npm test -- --coverage; fi
    
    - name: Security scan
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: 'services/${{ matrix.service }}'
        severity: 'CRITICAL,HIGH'
        
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    
    strategy:
      matrix:
        service: [api-gateway, user-service, etl-service, web-ui]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
      
    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/${{ matrix.service }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=semver,pattern={{major}}.{{minor}}
          type=sha,prefix={{branch}}-
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: services/${{ matrix.service }}
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
        build-args: |
          BUILD_DATE=${{ github.event.head_commit.timestamp }}
          VCS_REF=${{ github.sha }}
          VERSION=${{ steps.meta.outputs.version }}

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    
    steps:
    - name: Deploy to Staging
      uses: azure/k8s-deploy@v4
      with:
        manifests: |
          k8s/overlays/staging
        images: |
          ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
        kubeconfig: ${{ secrets.STAGING_KUBECONFIG }}
        
    - name: Run smoke tests
      run: |
        ./scripts/smoke-tests.sh https://staging.openpolicy.ca
        
    - name: Notify deployment
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        text: 'Staging deployment ${{ job.status }}'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}

  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://openpolicy.ca
    
    steps:
    - name: Blue-Green Deployment
      run: |
        # Deploy to green environment
        kubectl apply -f k8s/overlays/production-green
        
        # Run health checks
        ./scripts/health-check.sh https://green.openpolicy.ca
        
        # Switch traffic
        kubectl patch service openpolicy-lb -p '{"spec":{"selector":{"version":"green"}}}'
        
        # Verify deployment
        ./scripts/verify-deployment.sh https://openpolicy.ca
        
        # Clean up blue environment after 24h
        echo "kubectl delete -f k8s/overlays/production-blue" | at now + 24 hours
```

## 🏗️ Infrastructure as Code

### Terraform Configuration

```hcl
# infrastructure/main.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
  
  backend "s3" {
    bucket         = "openpolicy-terraform-state"
    key            = "infrastructure/terraform.tfstate"
    region         = "ca-central-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

# VPC Configuration
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "openpolicy-${var.environment}"
  cidr = var.vpc_cidr
  
  azs             = data.aws_availability_zones.available.names
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets
  
  enable_nat_gateway   = true
  enable_vpn_gateway   = true
  enable_dns_hostnames = true
  
  tags = {
    Environment = var.environment
    Terraform   = "true"
  }
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.15.3"
  
  cluster_name    = "openpolicy-${var.environment}"
  cluster_version = "1.28"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  enable_irsa = true
  
  eks_managed_node_groups = {
    general = {
      desired_size = 3
      min_size     = 3
      max_size     = 10
      
      instance_types = ["t3.large"]
      
      k8s_labels = {
        Environment = var.environment
        NodeGroup   = "general"
      }
    }
    
    compute_optimized = {
      desired_size = 2
      min_size     = 0
      max_size     = 5
      
      instance_types = ["c5.2xlarge"]
      
      taints = [{
        key    = "compute-optimized"
        value  = "true"
        effect = "NO_SCHEDULE"
      }]
      
      k8s_labels = {
        Environment = var.environment
        NodeGroup   = "compute"
      }
    }
  }
}

# RDS PostgreSQL
module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "6.1.1"
  
  identifier = "openpolicy-${var.environment}"
  
  engine            = "postgres"
  engine_version    = "15.4"
  instance_class    = var.db_instance_class
  allocated_storage = 100
  storage_encrypted = true
  
  db_name  = "openpolicy"
  username = "openpolicy_admin"
  port     = "5432"
  
  vpc_security_group_ids = [module.rds_security_group.security_group_id]
  
  maintenance_window = "Mon:00:00-Mon:03:00"
  backup_window      = "03:00-06:00"
  
  backup_retention_period = 30
  
  enabled_cloudwatch_logs_exports = ["postgresql"]
  
  create_db_subnet_group = true
  subnet_ids             = module.vpc.database_subnets
  
  deletion_protection = var.environment == "production"
}

# ElastiCache Redis
module "redis" {
  source = "terraform-aws-modules/elasticache/aws"
  
  cluster_id               = "openpolicy-${var.environment}"
  engine                   = "redis"
  node_type                = "cache.r6g.large"
  number_cache_nodes       = 3
  parameter_group_family   = "redis7"
  engine_version           = "7.0"
  port                     = 6379
  
  maintenance_window       = "sun:05:00-sun:06:00"
  snapshot_retention_limit = 7
  
  subnet_ids = module.vpc.private_subnets
  
  security_group_ids = [module.redis_security_group.security_group_id]
}
```

### Kubernetes Manifests

```yaml
# k8s/base/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: openpolicy
  labels:
    name: openpolicy
    istio-injection: enabled

---
# k8s/base/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: openpolicy-config
  namespace: openpolicy
data:
  APP_ENV: "production"
  API_VERSION: "v1"
  LOG_LEVEL: "info"
  ENABLE_METRICS: "true"
  ENABLE_TRACING: "true"

---
# k8s/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  namespace: openpolicy
  labels:
    app: api-gateway
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: api-gateway
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: api-gateway
        image: ghcr.io/openpolicy/api-gateway:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
        - containerPort: 8080
          name: metrics
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: redis-credentials
              key: url
        envFrom:
        - configMapRef:
            name: openpolicy-config
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        volumeMounts:
        - name: app-secrets
          mountPath: /app/secrets
          readOnly: true
      volumes:
      - name: app-secrets
        secret:
          secretName: app-secrets
          defaultMode: 0400
```

## 📊 Monitoring & Observability

### Metrics Collection

```yaml
# monitoring/prometheus-values.yaml
prometheus:
  prometheusSpec:
    serviceMonitorSelector:
      matchLabels:
        app.kubernetes.io/part-of: openpolicy
    
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: fast-ssd
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 100Gi
    
    retention: 30d
    retentionSize: 95GB
    
    resources:
      requests:
        memory: 2Gi
        cpu: 1
      limits:
        memory: 4Gi
        cpu: 2
    
    additionalScrapeConfigs:
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
```

### Alerting Rules

```yaml
# monitoring/alerts.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: openpolicy-alerts
  namespace: monitoring
spec:
  groups:
  - name: api.rules
    interval: 30s
    rules:
    - alert: HighRequestLatency
      expr: |
        histogram_quantile(0.95,
          sum(rate(http_request_duration_seconds_bucket[5m])) by (service, le)
        ) > 0.5
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: High request latency on {{ $labels.service }}
        description: "95th percentile latency is {{ $value }}s"
    
    - alert: HighErrorRate
      expr: |
        sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
        /
        sum(rate(http_requests_total[5m])) by (service)
        > 0.05
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: High error rate on {{ $labels.service }}
        description: "Error rate is {{ $value | humanizePercentage }}"
    
    - alert: PodCrashLooping
      expr: |
        rate(kube_pod_container_status_restarts_total[15m]) > 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: Pod {{ $labels.pod }} is crash looping
        description: "Pod has restarted {{ $value }} times in the last 15 minutes"
    
  - name: database.rules
    interval: 30s
    rules:
    - alert: DatabaseConnectionPoolExhausted
      expr: |
        pg_stat_database_numbackends{datname="openpolicy"}
        /
        pg_settings_max_connections
        > 0.8
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: Database connection pool near exhaustion
        description: "{{ $value | humanizePercentage }} of connections used"
    
    - alert: DatabaseSlowQueries
      expr: |
        rate(pg_stat_statements_mean_exec_time_seconds[5m]) > 1
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: Database queries are slow
        description: "Average query time is {{ $value }}s"
    
    - alert: DatabaseReplicationLag
      expr: |
        pg_replication_lag_seconds > 10
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: Database replication lag is high
        description: "Replication lag is {{ $value }}s"
```

### Logging Architecture

```yaml
# logging/fluent-bit-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: logging
data:
  fluent-bit.conf: |
    [SERVICE]
        Flush         5
        Log_Level     info
        Daemon        off
        
    [INPUT]
        Name              tail
        Path              /var/log/containers/*.log
        Parser            docker
        Tag               kube.*
        Refresh_Interval  5
        
    [FILTER]
        Name                kubernetes
        Match               kube.*
        Kube_URL            https://kubernetes.default.svc:443
        Kube_CA_File        /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        Kube_Token_File     /var/run/secrets/kubernetes.io/serviceaccount/token
        Merge_Log           On
        Keep_Log            Off
        
    [FILTER]
        Name    modify
        Match   kube.*
        Add     environment ${ENVIRONMENT}
        Add     cluster ${CLUSTER_NAME}
        
    [OUTPUT]
        Name            es
        Match           kube.*
        Host            elasticsearch.logging.svc.cluster.local
        Port            9200
        Index           openpolicy-${ENVIRONMENT}
        Logstash_Format On
        Retry_Limit     10
        
    [OUTPUT]
        Name            s3
        Match           kube.*
        bucket          openpolicy-logs-${ENVIRONMENT}
        region          ca-central-1
        use_put_object  On
        total_file_size 50M
        compression     gzip
```

### Distributed Tracing

```yaml
# tracing/jaeger-values.yaml
jaeger:
  create: true
  spec:
    strategy: production
    storage:
      type: elasticsearch
      options:
        es:
          server-urls: https://elasticsearch.logging.svc.cluster.local:9200
          index-prefix: jaeger
          
    ingress:
      enabled: true
      hosts:
        - jaeger.openpolicy.ca
      tls:
        - secretName: jaeger-tls
          hosts:
            - jaeger.openpolicy.ca
            
    collector:
      maxReplicas: 5
      resources:
        limits:
          cpu: 1
          memory: 1Gi
        requests:
          cpu: 500m
          memory: 512Mi
          
    query:
      replicas: 2
      resources:
        limits:
          cpu: 500m
          memory: 512Mi
```

## 🚨 Incident Response

### Runbook Template

```markdown
# Runbook: High API Latency

## Alert Details
- **Alert**: HighRequestLatency
- **Severity**: Warning/Critical
- **Service**: API Gateway

## Impact
- User-facing API responses are slow
- Possible timeout errors
- Degraded user experience

## Diagnosis Steps

1. **Check current latency**
   ```bash
   kubectl exec -n monitoring prometheus-0 -- \
     promtool query instant \
     'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))'
   ```

2. **Identify slow endpoints**
   ```bash
   kubectl logs -n openpolicy -l app=api-gateway --tail=1000 | \
     grep -E "duration_ms=[0-9]{4,}" | \
     jq -r '.endpoint + " " + .duration_ms' | \
     sort -k2 -nr | head -20
   ```

3. **Check database performance**
   ```sql
   SELECT query, mean_exec_time, calls
   FROM pg_stat_statements
   WHERE mean_exec_time > 100
   ORDER BY mean_exec_time DESC
   LIMIT 10;
   ```

4. **Verify resource usage**
   ```bash
   kubectl top pods -n openpolicy
   kubectl describe hpa -n openpolicy
   ```

## Resolution Steps

### Immediate Actions
1. **Scale up pods**
   ```bash
   kubectl scale deployment api-gateway -n openpolicy --replicas=10
   ```

2. **Clear cache if corrupted**
   ```bash
   kubectl exec -n openpolicy redis-master-0 -- redis-cli FLUSHDB
   ```

3. **Enable circuit breaker**
   ```bash
   kubectl patch configmap api-config -n openpolicy \
     -p '{"data":{"CIRCUIT_BREAKER_ENABLED":"true"}}'
   kubectl rollout restart deployment api-gateway -n openpolicy
   ```

### Long-term Fixes
1. Optimize slow queries
2. Implement better caching
3. Add read replicas
4. Review indexing strategy

## Escalation
- **L1**: On-call engineer (PagerDuty)
- **L2**: Backend team lead
- **L3**: Platform architect
- **L4**: CTO

## Post-Incident
1. Update runbook with findings
2. Create JIRA tickets for improvements
3. Schedule post-mortem meeting
```

### Disaster Recovery

```bash
#!/bin/bash
# disaster-recovery.sh

set -euo pipefail

ENVIRONMENT=$1
BACKUP_ID=$2

echo "Starting disaster recovery for $ENVIRONMENT"

# 1. Verify backup exists
if ! aws s3 ls s3://openpolicy-backups/$ENVIRONMENT/$BACKUP_ID/; then
    echo "ERROR: Backup $BACKUP_ID not found"
    exit 1
fi

# 2. Scale down applications
kubectl scale deployment --all -n openpolicy --replicas=0

# 3. Restore database
echo "Restoring database..."
kubectl exec -n openpolicy postgres-0 -- \
    pg_restore -d openpolicy -c -v \
    /backup/$BACKUP_ID/database.dump

# 4. Restore Redis state
echo "Restoring Redis..."
kubectl exec -n openpolicy redis-master-0 -- \
    redis-cli --rdb /backup/$BACKUP_ID/redis.rdb

# 5. Restore persistent volumes
echo "Restoring volumes..."
for pvc in $(kubectl get pvc -n openpolicy -o name); do
    kubectl exec -n openpolicy backup-restore-pod -- \
        tar -xzf /backup/$BACKUP_ID/${pvc##*/}.tar.gz -C /restore/
done

# 6. Update configuration
kubectl apply -f /backup/$BACKUP_ID/config/

# 7. Scale up applications
kubectl scale deployment --all -n openpolicy --replicas=3

# 8. Run health checks
./scripts/health-check.sh

echo "Disaster recovery completed"
```

## 🔧 Maintenance Procedures

### Database Maintenance

```sql
-- Weekly maintenance script
-- maintenance/weekly-db-maintenance.sql

-- Vacuum and analyze tables
VACUUM ANALYZE bills;
VACUUM ANALYZE votes;
VACUUM ANALYZE users;
VACUUM ANALYZE member_votes;

-- Update statistics
ANALYZE;

-- Check for bloat
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS external_size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 20;

-- Reindex if needed
REINDEX INDEX CONCURRENTLY idx_bills_search;
REINDEX INDEX CONCURRENTLY idx_votes_bill_result;

-- Check slow queries
SELECT 
    query,
    calls,
    mean_exec_time,
    total_exec_time
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Archive old data
INSERT INTO archive.activity_logs
SELECT * FROM activity_logs
WHERE created_at < NOW() - INTERVAL '90 days';

DELETE FROM activity_logs
WHERE created_at < NOW() - INTERVAL '90 days';
```

### Certificate Renewal

```bash
#!/bin/bash
# maintenance/cert-renewal.sh

# Check certificate expiry
echo "Checking certificate expiry..."
kubectl get certificate -n openpolicy -o json | \
    jq -r '.items[] | select(.status.renewalTime < (now | strftime("%Y-%m-%dT%H:%M:%SZ"))) | .metadata.name'

# Trigger renewal
for cert in $(kubectl get certificate -n openpolicy -o name); do
    kubectl annotate $cert -n openpolicy \
        cert-manager.io/issue-temporary-certificate="true" \
        --overwrite
done

# Verify renewal
sleep 60
kubectl get certificate -n openpolicy

# Update ingress
kubectl rollout restart deployment nginx-ingress-controller -n ingress-nginx
```

## 📈 Capacity Planning

### Resource Monitoring

```python
# scripts/capacity-monitor.py
import prometheus_client
import pandas as pd
from datetime import datetime, timedelta

class CapacityMonitor:
    def __init__(self, prometheus_url):
        self.prom = prometheus_client.PrometheusConnect(url=prometheus_url)
        
    def analyze_resource_usage(self, days=30):
        """Analyze resource usage trends"""
        
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        # CPU usage
        cpu_query = """
            avg by (pod) (
                rate(container_cpu_usage_seconds_total[5m])
            )
        """
        cpu_data = self.prom.custom_query_range(
            query=cpu_query,
            start_time=start_time,
            end_time=end_time,
            step='1h'
        )
        
        # Memory usage
        memory_query = """
            avg by (pod) (
                container_memory_working_set_bytes
            )
        """
        memory_data = self.prom.custom_query_range(
            query=memory_query,
            start_time=start_time,
            end_time=end_time,
            step='1h'
        )
        
        # Request rate
        request_query = """
            sum(rate(http_requests_total[5m]))
        """
        request_data = self.prom.custom_query_range(
            query=request_query,
            start_time=start_time,
            end_time=end_time,
            step='1h'
        )
        
        return self.generate_capacity_report(cpu_data, memory_data, request_data)
    
    def generate_capacity_report(self, cpu_data, memory_data, request_data):
        """Generate capacity planning report"""
        
        report = {
            "current_usage": {
                "cpu": self.calculate_percentile(cpu_data, 95),
                "memory": self.calculate_percentile(memory_data, 95),
                "requests_per_second": self.calculate_average(request_data)
            },
            "growth_rate": {
                "cpu": self.calculate_growth_rate(cpu_data),
                "memory": self.calculate_growth_rate(memory_data),
                "requests": self.calculate_growth_rate(request_data)
            },
            "predictions": {
                "cpu_exhaustion": self.predict_exhaustion(cpu_data, limit=1000),
                "memory_exhaustion": self.predict_exhaustion(memory_data, limit=64*1024*1024*1024),
                "scale_requirement": self.predict_scaling_needs(request_data)
            },
            "recommendations": self.generate_recommendations()
        }
        
        return report
```

### Auto-scaling Configuration

```yaml
# k8s/base/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-gateway-hpa
  namespace: openpolicy
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-gateway
  minReplicas: 3
  maxReplicas: 20
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 4
        periodSeconds: 30
      selectPolicy: Max
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
        averageValue: "100"
  - type: Object
    object:
      metric:
        name: response_time_p95
      describedObject:
        apiVersion: v1
        kind: Service
        name: api-gateway
      target:
        type: Value
        value: "500m"
```

## 🔒 Security Operations

### Security Scanning

```yaml
# .github/workflows/security-scan.yml
name: Security Scanning

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  push:
    branches: [main, develop]

jobs:
  container-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'ghcr.io/openpolicy/api-gateway:latest'
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'CRITICAL,HIGH,MEDIUM'
        
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
        
  dependency-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run OWASP dependency check
      uses: dependency-check/Dependency-Check_Action@main
      with:
        project: 'openpolicy'
        path: '.'
        format: 'ALL'
        args: >
          --enableRetired
          --enableExperimental
          
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: dependency-check-report
        path: reports/
        
  infrastructure-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Checkov Infrastructure Scan
      uses: bridgecrewio/checkov-action@master
      with:
        directory: infrastructure/
        framework: terraform
        output_format: sarif
        output_file_path: checkov.sarif
        
    - name: Upload Checkov results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: checkov.sarif
```

### Secret Rotation

```python
#!/usr/bin/env python3
# scripts/rotate-secrets.py

import boto3
import kubernetes
import base64
from datetime import datetime, timedelta

class SecretRotator:
    def __init__(self):
        self.k8s = kubernetes.client.CoreV1Api()
        self.secrets_manager = boto3.client('secretsmanager')
        
    def rotate_database_password(self):
        """Rotate database password"""
        
        # Generate new password
        new_password = self.generate_secure_password()
        
        # Update database
        self.update_database_password(new_password)
        
        # Update Kubernetes secret
        secret = self.k8s.read_namespaced_secret(
            name='database-credentials',
            namespace='openpolicy'
        )
        
        secret.data['password'] = base64.b64encode(
            new_password.encode()
        ).decode()
        
        self.k8s.patch_namespaced_secret(
            name='database-credentials',
            namespace='openpolicy',
            body=secret
        )
        
        # Update AWS Secrets Manager
        self.secrets_manager.update_secret(
            SecretId='openpolicy/database/password',
            SecretString=new_password
        )
        
        # Restart deployments
        self.restart_deployments(['api-gateway', 'user-service'])
        
    def rotate_api_keys(self):
        """Rotate API keys"""
        
        # Get all API keys older than 90 days
        old_keys = self.get_old_api_keys(days=90)
        
        for key in old_keys:
            # Generate new key
            new_key = self.generate_api_key()
            
            # Update key in database
            self.update_api_key(key['id'], new_key)
            
            # Notify key owner
            self.notify_key_rotation(key['owner'], new_key)
            
            # Schedule old key deletion
            self.schedule_key_deletion(key['id'], days=7)
    
    def generate_secure_password(self, length=32):
        """Generate cryptographically secure password"""
        import secrets
        import string
        
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        
        return password
```

## 📊 Operations Dashboard

### Grafana Dashboard Configuration

```json
{
  "dashboard": {
    "title": "OpenPolicy Operations Dashboard",
    "panels": [
      {
        "title": "Service Health",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "targets": [{
          "expr": "up{job=~\"openpolicy.*\"}",
          "legendFormat": "{{job}} - {{instance}}"
        }]
      },
      {
        "title": "Request Rate",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [{
          "expr": "sum(rate(http_requests_total[5m])) by (service)",
          "legendFormat": "{{service}}"
        }]
      },
      {
        "title": "Error Rate",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
        "targets": [{
          "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) by (service) / sum(rate(http_requests_total[5m])) by (service)",
          "legendFormat": "{{service}}"
        }]
      },
      {
        "title": "Response Time (p95)",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8},
        "targets": [{
          "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (service, le))",
          "legendFormat": "{{service}}"
        }]
      },
      {
        "title": "Database Connections",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16},
        "targets": [{
          "expr": "pg_stat_database_numbackends{datname=\"openpolicy\"}",
          "legendFormat": "Active Connections"
        }]
      },
      {
        "title": "Redis Memory Usage",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 16},
        "targets": [{
          "expr": "redis_memory_used_bytes / redis_memory_max_bytes",
          "legendFormat": "Memory Usage %"
        }]
      }
    ]
  }
}
```

## 🔄 Continuous Improvement

### Performance Optimization Cycle

```python
# scripts/performance-optimizer.py
class PerformanceOptimizer:
    def analyze_slow_endpoints(self):
        """Identify and optimize slow endpoints"""
        
        # Get slow endpoints from monitoring
        slow_endpoints = self.prometheus.query("""
            topk(10, 
                histogram_quantile(0.95,
                    sum(rate(http_request_duration_seconds_bucket[24h])) 
                    by (endpoint, le)
                )
            )
        """)
        
        for endpoint in slow_endpoints:
            # Analyze database queries
            queries = self.analyze_endpoint_queries(endpoint)
            
            # Generate optimization recommendations
            recommendations = {
                "endpoint": endpoint,
                "current_p95": endpoint['value'],
                "slow_queries": queries,
                "suggestions": [
                    self.suggest_index_optimization(queries),
                    self.suggest_caching_strategy(endpoint),
                    self.suggest_query_optimization(queries)
                ]
            }
            
            # Create JIRA ticket
            self.create_optimization_ticket(recommendations)
    
    def automated_optimization(self):
        """Apply automated optimizations"""
        
        # Auto-create missing indexes
        missing_indexes = self.detect_missing_indexes()
        for index in missing_indexes:
            if self.is_safe_to_create(index):
                self.create_index(index)
                
        # Auto-adjust connection pools
        pool_stats = self.get_connection_pool_stats()
        if pool_stats['usage'] > 0.8:
            self.increase_pool_size()
            
        # Auto-scale based on predictions
        predicted_load = self.predict_next_hour_load()
        if predicted_load > self.current_capacity * 0.8:
            self.trigger_prescaling(predicted_load)
```

## 🎯 SLA Management

### SLA Monitoring

```yaml
# monitoring/sla-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: sla-monitoring
spec:
  groups:
  - name: sla.rules
    interval: 30s
    rules:
    - record: sla:availability
      expr: |
        avg_over_time(up{job=~"openpolicy.*"}[5m])
        
    - record: sla:latency_p99
      expr: |
        histogram_quantile(0.99,
          sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
        )
        
    - record: sla:error_rate
      expr: |
        sum(rate(http_requests_total{status=~"5.."}[5m]))
        /
        sum(rate(http_requests_total[5m]))
        
    - alert: SLAViolation
      expr: |
        sla:availability < 0.999
        or sla:latency_p99 > 1
        or sla:error_rate > 0.01
      for: 5m
      labels:
        severity: critical
        team: platform
      annotations:
        summary: SLA violation detected
        description: |
          Availability: {{ $value }}
          Required: 99.9%
```

## 📋 Operations Checklist

### Daily Operations
- [ ] Check service health dashboard
- [ ] Review overnight alerts
- [ ] Verify backup completion
- [ ] Check certificate expiry
- [ ] Review security alerts
- [ ] Monitor resource usage

### Weekly Operations
- [ ] Database maintenance
- [ ] Security patching
- [ ] Capacity review
- [ ] Cost optimization
- [ ] Performance analysis
- [ ] Incident review

### Monthly Operations
- [ ] Disaster recovery test
- [ ] Security audit
- [ ] Access review
- [ ] Documentation update
- [ ] Training review
- [ ] SLA reporting

---
**Operations Maturity**: Level 3 (Defined)  
**Target Maturity**: Level 5 (Optimized)  
**Review Frequency**: Weekly  
**Iteration**: 1 of 3