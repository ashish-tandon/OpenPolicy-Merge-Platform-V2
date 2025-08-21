#!/bin/bash

# OpenMetadata Startup Script for OpenPolicy Platform
# This script starts the OpenMetadata service and configures data lineage

echo "🚀 Starting OpenMetadata Service for Data Lineage Tracking..."

# Check if we're in the right directory
if [ ! -f "docker-compose-custom.yml" ]; then
    echo "❌ Error: docker-compose-custom.yml not found. Please run from services/openmetadata directory."
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if the mergev2 network exists
if ! docker network ls | grep -q "mergev2_default"; then
    echo "❌ Error: mergev2_default network not found. Please start the main platform first."
    echo "💡 Run: cd /Users/ashishtandon/Github/Merge\ V2 && docker-compose up -d"
    exit 1
fi

echo "✅ Docker environment ready"
echo "✅ Network mergev2_default found"

# Start OpenMetadata services
echo "🔧 Starting OpenMetadata services..."
docker-compose -f docker-compose-custom.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for OpenMetadata services to be ready..."
sleep 30

# Check service status
echo "🔍 Checking service status..."
docker-compose -f docker-compose-custom.yml ps

# Display access information
echo ""
echo "🎉 OpenMetadata Service Started Successfully!"
echo "================================================"
echo "🌐 OpenMetadata UI: http://localhost:8585"
echo "   Username: admin@open-metadata.org"
echo "   Password: admin"
echo ""
echo "🌐 Airflow UI: http://localhost:8080"
echo "   Username: admin"
echo "   Password: admin"
echo ""
echo "📊 Data Lineage Configuration: data-lineage-config.yml"
echo "🔧 Docker Compose: docker-compose-custom.yml"
echo ""
echo "📋 Next Steps:"
echo "1. Open http://localhost:8585 in your browser"
echo "2. Log in with admin@open-metadata.org / admin"
echo "3. Configure data sources using the lineage config"
echo "4. Set up ingestion workflows for data tracking"
echo ""
echo "🛑 To stop: docker-compose -f docker-compose-custom.yml down"
echo "🔄 To restart: docker-compose -f docker-compose-custom.yml restart"
