#!/bin/bash
# quick_start.sh

set -e

echo "🚀 Quick Start for Merge V2 Development Environment"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if services are already running
if docker ps --format "table {{.Names}}" | grep -q "merge_v2_"; then
    echo "⚠️  Services are already running. Stopping them first..."
    docker-compose -f docker-compose.dev.yml down
fi

# Start services
echo "🔄 Starting services..."
docker-compose -f docker-compose.dev.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Service Status:"
docker-compose -f docker-compose.dev.yml ps

echo ""
echo "🎉 Quick start completed!"
echo ""
echo "Services are running at:"
echo "  - API Gateway: http://localhost:8000"
echo "  - Web Frontend: http://localhost:3000"
echo "  - Admin Frontend: http://localhost:3001"
echo "  - User Service: http://localhost:8002"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana: http://localhost:3002 (admin/admin)"
echo ""
echo "To stop: docker-compose -f docker-compose.dev.yml down"
echo "To view logs: docker-compose -f docker-compose.dev.yml logs -f"
