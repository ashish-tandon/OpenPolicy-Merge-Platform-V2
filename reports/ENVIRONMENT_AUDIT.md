# Environment Audit Report

Generated: 2025-08-23T17:53:57.782787

## Summary

- Docker Containers: 0 (Healthy: 0)
- Open Ports: 0
- Service Health Checks: 0 healthy
- Total Errors Found: 0

## Docker Services

No Docker services found.

## Service Health Checks

- ❌ **API Gateway**: Unhealthy (Connection failed)
- ❌ **User Service**: Unhealthy (Connection failed)
- ❌ **OpenMetadata**: Unhealthy (Connection failed)
- ❌ **Elasticsearch**: Unhealthy (Connection failed)
- ❌ **Frontend**: Unhealthy (Connection failed)

## Open Ports

## Error Analysis

### Recent Errors


## Resource Usage

- **CPU**: Load: (0.84033203125, 0.3095703125, 0.109375) | CPUs: 4
- **Memory**: 8.2% (1.3GB / 15.6GB)
- **Disk**: 6.0% (6.1GB / 125.9GB)

## Configuration Files

### CONF Files
- `services/admin-ui/nginx.conf` (Modified: 2025-08-16)
- `services/monitoring-dashboard/nginx.conf` (Modified: 2025-08-16)
- `services/web-ui/nginx.conf` (Modified: 2025-08-16)

### PY Files
- `services/user-service/app/config/settings.py` (Modified: 2025-08-16)

### YML Files
- `docker-compose.dev.yml` (Modified: 2025-08-16)
- `docker-compose.yml` (Modified: 2025-08-16)
- `services/etl/legacy-scrapers-ca/docker/docker-compose.yml` (Modified: 2025-08-16)
- `services/openmetadata/docker-compose-custom.yml` (Modified: 2025-08-16)
- `services/openmetadata/docker-compose-mysql.yml` (Modified: 2025-08-16)
- `services/openmetadata/docker-compose.yml` (Modified: 2025-08-16)
- `services/user-service/docker-compose.mail.yml` (Modified: 2025-08-16)
- `services/user-service/docker-compose.notifico.yml` (Modified: 2025-08-16)
- `services/web-ui/src/components/legacy-assets/bower_components/foundation-sites/customizer/config.yml` (Modified: 2025-08-16)
- `services/web-ui/src/legacy-migration/static/bower_components/foundation-sites/customizer/config.yml` (Modified: 2025-08-16)

