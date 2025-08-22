# Operational Runbooks

## Table of Contents
1. [Deployment Runbook](#deployment-runbook)
2. [Rollback Procedures](#rollback-procedures)
3. [Incident Response](#incident-response)
4. [Database Operations](#database-operations)
5. [Monitoring & Alerts](#monitoring--alerts)
6. [Maintenance Procedures](#maintenance-procedures)
7. [Disaster Recovery](#disaster-recovery)
8. [Security Operations](#security-operations)

---

## Deployment Runbook

### Pre-Deployment Checklist
- [ ] All tests passing in CI/CD pipeline
- [ ] Security scan completed
- [ ] Database migrations reviewed
- [ ] Change log updated
- [ ] Stakeholders notified
- [ ] Rollback plan prepared
- [ ] Monitoring alerts configured

### Standard Deployment Process

#### 1. Pre-Production Deployment
```bash
# 1. Connect to deployment server
ssh deploy@staging.openpolicy.ca

# 2. Pull latest code
cd /opt/openpolicy
git fetch origin
git checkout tags/v2.1.0

# 3. Run database migrations (dry run)
docker-compose exec api-gateway alembic upgrade head --sql

# 4. Apply database migrations
docker-compose exec api-gateway alembic upgrade head

# 5. Update environment variables
cp .env.staging .env

# 6. Build and deploy containers
docker-compose build --no-cache
docker-compose up -d

# 7. Run health checks
./scripts/health-check.sh staging

# 8. Run smoke tests
./scripts/smoke-tests.sh staging
```

#### 2. Production Deployment (Blue-Green)
```bash
# 1. Deploy to green environment
kubectl apply -f k8s/green-deployment.yaml

# 2. Wait for green to be ready
kubectl wait --for=condition=ready pod -l app=openpolicy,env=green --timeout=300s

# 3. Run health checks on green
./scripts/health-check.sh green.openpolicy.ca

# 4. Switch traffic to green
kubectl patch service openpolicy -p '{"spec":{"selector":{"env":"green"}}}'

# 5. Monitor for 15 minutes
watch -n 5 kubectl top pods -l app=openpolicy

# 6. If stable, remove blue deployment
kubectl delete deployment openpolicy-blue
```

### Deployment Verification
```bash
# API Health Check
curl -s https://api.openpolicy.ca/health | jq .

# Database Connectivity
docker-compose exec api-gateway python -c "from app.database import engine; print(engine.execute('SELECT 1').scalar())"

# Redis Connectivity
docker-compose exec api-gateway python -c "import redis; r=redis.from_url('redis://redis:6379'); print(r.ping())"

# Scraper Status
curl -s https://api.openpolicy.ca/api/v1/data-sources | jq '.data[] | {name: .name, last_run: .last_updated}'
```

---

## Rollback Procedures

### Immediate Rollback (< 5 minutes)
```bash
# For Kubernetes deployments
kubectl rollout undo deployment/openpolicy

# For Docker Compose deployments
git checkout tags/v2.0.0  # Previous version
docker-compose up -d --force-recreate
```

### Database Rollback
```bash
# 1. Stop application servers
docker-compose stop api-gateway web-ui

# 2. Rollback database migration
docker-compose exec api-gateway alembic downgrade -1

# 3. Deploy previous version
git checkout tags/v2.0.0
docker-compose up -d

# 4. Verify rollback
./scripts/health-check.sh production
```

### Data Rollback
```sql
-- Restore from backup (within 24 hours)
pg_restore -h localhost -U postgres -d openpolicy -c /backups/openpolicy_2024_01_20.dump

-- Point-in-time recovery
SELECT pg_create_restore_point('before_deployment_v2.1.0');
-- After issue detected
SELECT pg_switch_wal();
RESTORE DATABASE openpolicy TO 'before_deployment_v2.1.0';
```

---

## Incident Response

### Severity Levels
- **SEV1**: Complete service outage
- **SEV2**: Major functionality broken
- **SEV3**: Minor functionality impaired
- **SEV4**: Cosmetic issues

### SEV1 Response Playbook

#### 1. Initial Response (0-5 minutes)
```bash
# Check service status
kubectl get pods -l app=openpolicy
kubectl describe pods -l app=openpolicy

# Check recent logs
kubectl logs -l app=openpolicy --tail=100

# Check database
psql -h db.openpolicy.ca -U postgres -c "SELECT count(*) FROM bills;"

# Check external dependencies
curl -s https://www.parl.ca/robots.txt
```

#### 2. Triage (5-15 minutes)
```bash
# Identify error patterns
kubectl logs -l app=openpolicy | grep ERROR | tail -50

# Check resource usage
kubectl top nodes
kubectl top pods

# Database locks
psql -c "SELECT * FROM pg_stat_activity WHERE state = 'active';"

# Redis status
redis-cli ping
redis-cli info stats
```

#### 3. Mitigation (15-30 minutes)
```bash
# Scale up if resource constrained
kubectl scale deployment openpolicy --replicas=10

# Clear cache if data issues
redis-cli FLUSHDB

# Restart problematic pods
kubectl delete pod -l app=openpolicy,component=scraper

# Enable maintenance mode
kubectl set env deployment/openpolicy MAINTENANCE_MODE=true
```

### Communication Template
```
Subject: [SEV1] OpenPolicy Service Degradation

Status: Investigating | Identified | Monitoring | Resolved
Time: 2024-01-20 14:30 EST
Impact: Users unable to access bill information
Affected Services: API Gateway, Bill Search

Current Status:
- API returning 503 errors
- Database connection pool exhausted
- Team investigating root cause

Next Update: In 15 minutes or when status changes

Actions Taken:
- Increased connection pool size
- Restarted affected services
- Enabled detailed logging
```

---

## Database Operations

### Backup Procedures
```bash
# Daily automated backup (cron: 0 2 * * *)
#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR="/backups/postgres"

# Full backup
pg_dump -h localhost -U postgres -Fc openpolicy > "${BACKUP_DIR}/openpolicy_${DATE}.dump"

# Verify backup
pg_restore -l "${BACKUP_DIR}/openpolicy_${DATE}.dump" > /dev/null || exit 1

# Upload to S3
aws s3 cp "${BACKUP_DIR}/openpolicy_${DATE}.dump" s3://openpolicy-backups/postgres/

# Clean old backups (keep 30 days)
find ${BACKUP_DIR} -name "*.dump" -mtime +30 -delete
```

### Database Maintenance
```sql
-- Weekly maintenance (Sunday 3 AM)
-- Vacuum and analyze all tables
VACUUM ANALYZE;

-- Reindex large tables
REINDEX TABLE bills;
REINDEX TABLE votes;
REINDEX TABLE debates;

-- Update statistics
ANALYZE bills;
ANALYZE votes;
ANALYZE elected_members;
```

### Connection Pool Management
```python
# Monitor connection usage
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Check pool status
print(f"Pool size: {engine.pool.size()}")
print(f"Checked out: {engine.pool.checked_out()}")
print(f"Overflow: {engine.pool.overflow()}")
```

---

## Monitoring & Alerts

### Key Metrics to Monitor

#### Application Metrics
```yaml
# Prometheus alerts
groups:
  - name: openpolicy
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
          
      - alert: SlowAPIResponse
        expr: histogram_quantile(0.95, http_request_duration_seconds_bucket) > 1
        for: 5m
        annotations:
          summary: "API response time > 1s at P95"
          
      - alert: ScraperFailure
        expr: scraper_last_success_timestamp < (time() - 86400)
        for: 1h
        annotations:
          summary: "Scraper hasn't run successfully in 24 hours"
```

#### Infrastructure Metrics
```bash
# CPU Usage
kubectl top nodes

# Memory Usage
free -h

# Disk Usage
df -h

# Database Connections
psql -c "SELECT count(*) FROM pg_stat_activity;"

# Redis Memory
redis-cli info memory | grep used_memory_human
```

### Alert Response Procedures

#### High CPU Usage (> 80%)
1. Identify top consumers: `kubectl top pods --sort-by=cpu`
2. Check for runaway processes: `kubectl exec <pod> -- top`
3. Scale horizontally if needed: `kubectl scale deployment <name> --replicas=+2`
4. Investigate code for inefficiencies

#### Database Lock Alert
```sql
-- Find blocking queries
SELECT 
    blocking.pid AS blocking_pid,
    blocking.query AS blocking_query,
    blocked.pid AS blocked_pid,
    blocked.query AS blocked_query
FROM pg_stat_activity AS blocked
JOIN pg_stat_activity AS blocking ON blocking.pid = ANY(pg_blocking_pids(blocked.pid));

-- Kill blocking query if necessary
SELECT pg_terminate_backend(<blocking_pid>);
```

---

## Maintenance Procedures

### Scheduled Maintenance Window
**Time**: Sundays 02:00-04:00 EST (low traffic period)

#### Pre-Maintenance
```bash
# 1. Notify users (24 hours before)
./scripts/send-maintenance-notification.sh

# 2. Enable maintenance mode
kubectl set env deployment/web-ui MAINTENANCE_MODE=true

# 3. Stop data ingestion
kubectl scale deployment openpolicy-scrapers --replicas=0
```

#### During Maintenance
```bash
# 1. Database maintenance
docker-compose exec postgres psql -U postgres -d openpolicy -c "VACUUM FULL ANALYZE;"

# 2. Clear old logs
find /var/log/openpolicy -name "*.log" -mtime +30 -delete

# 3. Update dependencies
docker-compose exec api-gateway pip install -r requirements.txt --upgrade

# 4. Clean Docker resources
docker system prune -af
```

#### Post-Maintenance
```bash
# 1. Disable maintenance mode
kubectl set env deployment/web-ui MAINTENANCE_MODE=false

# 2. Restart services
kubectl rollout restart deployment/openpolicy

# 3. Resume data ingestion
kubectl scale deployment openpolicy-scrapers --replicas=3

# 4. Run health checks
./scripts/full-health-check.sh

# 5. Send completion notification
./scripts/send-maintenance-complete.sh
```

### Certificate Renewal
```bash
# Auto-renewal with Let's Encrypt (monthly check)
certbot renew --nginx --quiet

# Manual renewal if needed
certbot certonly --nginx -d openpolicy.ca -d api.openpolicy.ca -d www.openpolicy.ca

# Verify renewal
echo | openssl s_client -servername openpolicy.ca -connect openpolicy.ca:443 2>/dev/null | openssl x509 -noout -dates
```

---

## Disaster Recovery

### RTO/RPO Targets
- **RTO** (Recovery Time Objective): 4 hours
- **RPO** (Recovery Point Objective): 1 hour

### Disaster Scenarios

#### Complete Data Center Failure
```bash
# 1. Activate DR site
terraform apply -var="environment=dr" -auto-approve

# 2. Restore database from backup
aws s3 cp s3://openpolicy-backups/postgres/latest.dump /tmp/
pg_restore -h dr-db.openpolicy.ca -U postgres -d openpolicy /tmp/latest.dump

# 3. Update DNS
aws route53 change-resource-record-sets --hosted-zone-id Z123456 --change-batch file://dr-dns-change.json

# 4. Verify services
./scripts/dr-health-check.sh
```

#### Database Corruption
```bash
# 1. Stop all services
kubectl scale deployment --all --replicas=0

# 2. Restore from backup
pg_restore -h localhost -U postgres -d openpolicy_restore /backups/postgres/latest.dump

# 3. Verify data integrity
psql -d openpolicy_restore -f /scripts/data-integrity-check.sql

# 4. Switch to restored database
psql -c "ALTER DATABASE openpolicy RENAME TO openpolicy_corrupt;"
psql -c "ALTER DATABASE openpolicy_restore RENAME TO openpolicy;"

# 5. Restart services
kubectl scale deployment --all --replicas=3
```

### Recovery Testing
```bash
# Monthly DR drill
./scripts/dr-drill.sh --scenario=datacenter-failure --dry-run

# Quarterly full DR test
./scripts/dr-drill.sh --scenario=complete-recovery --target=dr-environment
```

---

## Security Operations

### Security Incident Response

#### Suspected Breach
```bash
# 1. Isolate affected systems
kubectl cordon node-1
kubectl drain node-1 --ignore-daemonsets

# 2. Capture forensic data
kubectl exec <pod> -- tar czf /tmp/forensics.tar.gz /var/log /tmp
kubectl cp <pod>:/tmp/forensics.tar.gz ./forensics/

# 3. Review access logs
grep "401\|403" /var/log/nginx/access.log | tail -100
kubectl logs -l app=openpolicy | grep -E "auth|login|token" | tail -100

# 4. Check for unauthorized changes
git log --since="1 hour ago" --all
kubectl get events --sort-by='.lastTimestamp' | tail -20
```

#### Password Rotation
```bash
# 1. Database passwords
psql -c "ALTER USER api_user WITH PASSWORD 'new_secure_password';"

# 2. Update application secrets
kubectl create secret generic db-credentials \
  --from-literal=password='new_secure_password' \
  --dry-run=client -o yaml | kubectl apply -f -

# 3. Rotate API keys
python scripts/rotate_api_keys.py --service=all

# 4. Update Redis password
redis-cli CONFIG SET requirepass "new_redis_password"
```

### Security Scanning
```bash
# Weekly vulnerability scan
trivy image openpolicy/api-gateway:latest
trivy image openpolicy/web-ui:latest

# SAST scanning
bandit -r services/api-gateway/
npm audit --prefix services/web-ui/

# Dependency checking
safety check -r requirements.txt
npm audit fix --prefix services/web-ui/
```

---

## Appendix: Emergency Contacts

### Escalation Matrix
| Role | Name | Phone | Email |
|------|------|--------|--------|
| On-Call Engineer | Rotation | See PagerDuty | oncall@openpolicy.ca |
| Tech Lead | John Smith | +1-555-0123 | john@openpolicy.ca |
| DevOps Lead | Jane Doe | +1-555-0124 | jane@openpolicy.ca |
| Database Admin | Bob Wilson | +1-555-0125 | bob@openpolicy.ca |
| Security Lead | Alice Brown | +1-555-0126 | alice@openpolicy.ca |

### External Vendors
| Service | Support Number | Account # |
|---------|---------------|-----------|
| AWS | 1-800-xxx-xxxx | 12345 |
| Datadog | 1-866-xxx-xxxx | 67890 |
| PagerDuty | 1-844-xxx-xxxx | 11111 |

### Useful Commands Cheatsheet
```bash
# Quick diagnostics
alias pod-status='kubectl get pods -l app=openpolicy'
alias logs='kubectl logs -l app=openpolicy --tail=50'
alias db-check='psql -h localhost -U postgres -c "SELECT version();"'
alias cache-check='redis-cli ping'
alias api-health='curl -s https://api.openpolicy.ca/health | jq .'

# Emergency scripts location
/opt/openpolicy/emergency-scripts/
├── force-rollback.sh
├── emergency-scale.sh
├── clear-all-caches.sh
├── restore-from-backup.sh
└── enable-maintenance.sh
```