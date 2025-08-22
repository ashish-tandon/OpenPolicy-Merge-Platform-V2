#!/bin/bash

# Container Stability Monitor
# This script monitors all containers and ensures they stay stable for 6+ hours

set -euo pipefail

# Configuration
LOG_FILE="/Users/ashishtandon/Github/Merge V2/stability-monitor.log"
CHECK_INTERVAL=300  # 5 minutes
ALERT_INTERVAL=1800  # 30 minutes
MAX_RESTARTS=3
START_TIME=$(date +%s)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "$LOG_FILE"
}

# Function to check container health
check_container_health() {
    local container_name=$1
    local status=$(docker inspect --format='{{.State.Status}}' "$container_name" 2>/dev/null || echo "not_found")
    local health=$(docker inspect --format='{{.State.Health.Status}}' "$container_name" 2>/dev/null || echo "no_health_check")
    local restart_count=$(docker inspect --format='{{.RestartCount}}' "$container_name" 2>/dev/null || echo "0")
    
    echo "$status|$health|$restart_count"
}

# Function to check endpoint health
check_endpoint() {
    local name=$1
    local url=$2
    local timeout=${3:-10}
    
    if curl -s --max-time "$timeout" "$url" > /dev/null 2>&1; then
        echo "healthy"
    else
        echo "unhealthy"
    fi
}

# Function to perform comprehensive health check
perform_health_check() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local uptime=$(( $(date +%s) - START_TIME ))
    local uptime_hours=$(( uptime / 3600 ))
    local uptime_minutes=$(( (uptime % 3600) / 60 ))
    
    log "🔍 Performing health check (Uptime: ${uptime_hours}h ${uptime_minutes}m)"
    
    # Check container status
    local all_healthy=true
    local container_status=""
    
    # Core services
    local core_containers=("mergev2-db-1" "mergev2-redis-1" "mergev2-user-service-1" "mergev2-api-gateway-1")
    for container in "${core_containers[@]}"; do
        local health_info=$(check_container_health "$container")
        IFS='|' read -r status health restart_count <<< "$health_info"
        
        if [[ "$status" == "running" && "$health" == "healthy" ]]; then
            container_status+="✅ $container: healthy (restarts: $restart_count)\n"
        else
            container_status+="❌ $container: $status/$health (restarts: $restart_count)\n"
            all_healthy=false
        fi
    done
    
    # OpenMetadata services
    local om_containers=("mergev2-openmetadata-server" "mergev2-openmetadata-ingestion" "mergev2-elasticsearch")
    for container in "${om_containers[@]}"; do
        local health_info=$(check_container_health "$container")
        IFS='|' read -r status health restart_count <<< "$health_info"
        
        if [[ "$status" == "running" ]]; then
            if [[ "$health" == "healthy" ]]; then
                container_status+="✅ $container: healthy (restarts: $restart_count)\n"
            elif [[ "$health" == "starting" ]]; then
                container_status+="🔄 $container: starting (restarts: $restart_count)\n"
            else
                container_status+="⚠️  $container: $status/$health (restarts: $restart_count)\n"
            fi
        else
            container_status+="❌ $container: $status/$health (restarts: $restart_count)\n"
            all_healthy=false
        fi
    done
    
    # Check endpoint health
    log "🌐 Checking endpoint health..."
    local api_health=$(check_endpoint "API Gateway" "http://localhost:8080/healthz")
    local user_health=$(check_endpoint "User Service" "http://localhost:8082/health")
    local om_health=$(check_endpoint "OpenMetadata" "http://localhost:8585/api/v1/system/version")
    local es_health=$(check_endpoint "Elasticsearch" "http://localhost:9200/_cluster/health")
    
    # Log results
    echo -e "$container_status" | tee -a "$LOG_FILE"
    log "🌐 Endpoint Status:"
    log "   API Gateway: $api_health"
    log "   User Service: $user_health"
    log "   OpenMetadata: $om_health"
    log "   Elasticsearch: $es_health"
    
    # Check for excessive restarts
    local total_restarts=0
    for container in "${core_containers[@]}" "${om_containers[@]}"; do
        local health_info=$(check_container_health "$container")
        IFS='|' read -r status health restart_count <<< "$health_info"
        total_restarts=$((total_restarts + restart_count))
    done
    
    if [[ $total_restarts -gt $MAX_RESTARTS ]]; then
        warn "⚠️  High restart count detected: $total_restarts restarts"
    fi
    
    # Overall status
    if [[ "$all_healthy" == true ]]; then
        log "🎉 All core services are healthy!"
    else
        warn "⚠️  Some services are not healthy"
    fi
    
    log "📊 Health check completed"
    echo "----------------------------------------" >> "$LOG_FILE"
}

# Function to check resource usage
check_resources() {
    log "💾 Checking resource usage..."
    
    # Memory usage
    local memory_usage=$(docker stats --no-stream --format "table {{.Container}}\t{{.MemUsage}}\t{{.MemPerc}}" | tail -n +2)
    log "Memory usage:\n$memory_usage"
    
    # CPU usage
    local cpu_usage=$(docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}" | tail -n +2)
    log "CPU usage:\n$cpu_usage"
    
    # Disk usage
    local disk_usage=$(df -h /Users/ashishtandon/Github/Merge\ V2 | tail -n +2)
    log "Disk usage:\n$disk_usage"
}

# Function to restart unhealthy containers
restart_unhealthy_container() {
    local container_name=$1
    local reason=$2
    
    warn "🔄 Restarting unhealthy container: $container_name (Reason: $reason)"
    docker restart "$container_name" 2>/dev/null || error "Failed to restart $container_name"
    sleep 30  # Wait for container to start
}

# Main monitoring loop
main() {
    log "🚀 Starting Container Stability Monitor"
    log "📁 Log file: $LOG_FILE"
    log "⏰ Check interval: ${CHECK_INTERVAL}s"
    log "🔔 Alert interval: ${ALERT_INTERVAL}s"
    
    local check_count=0
    local alert_count=0
    
    while true; do
        check_count=$((check_count + 1))
        
        log "📋 Health check #$check_count"
        perform_health_check
        
        # Check resources every 4th check (every 20 minutes)
        if [[ $((check_count % 4)) -eq 0 ]]; then
            check_resources
        fi
        
        # Sleep until next check
        log "😴 Sleeping for ${CHECK_INTERVAL}s until next check..."
        sleep "$CHECK_INTERVAL"
    done
}

# Handle script interruption
trap 'log "🛑 Monitor stopped by user"; exit 0' INT TERM

# Start monitoring
main
