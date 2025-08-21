#!/bin/bash

# OpenMetadata Service Startup Script
# This script starts the OpenMetadata service with the main platform

echo "🚀 Starting OpenMetadata Service for Data Lineage Tracking..."

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found. Please run from the root directory."
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Start the main platform first (if not already running)
echo "🔧 Ensuring main platform is running..."
docker-compose up -d db api-gateway user-service redis

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 20

# Create OpenMetadata databases
echo "🔧 Creating OpenMetadata databases..."
docker exec mergev2-db-1 psql -U openpolicy -d openpolicy -c "CREATE DATABASE IF NOT EXISTS openmetadata;" 2>/dev/null || true
docker exec mergev2-db-1 psql -U openpolicy -d openpolicy -c "CREATE DATABASE IF NOT EXISTS airflow;" 2>/dev/null || true

# Start OpenMetadata services
echo "🔧 Starting OpenMetadata services..."
docker-compose --profile openmetadata up -d

# Wait for services to be ready
echo "⏳ Waiting for OpenMetadata services to be ready..."
sleep 45

# Check service status
echo "🔍 Checking service status..."
docker-compose --profile openmetadata ps

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
echo "📊 Data Lineage Configuration: services/openmetadata/data-lineage-config.yml"
echo "🔧 Docker Compose Profile: openmetadata"
echo ""
echo "📋 Next Steps:"
echo "1. Open http://localhost:8585 in your browser"
echo "2. Log in with admin@open-metadata.org / admin"
echo "3. Configure data sources using the lineage config"
echo "4. Set up ingestion workflows for data tracking"
echo ""
echo "🛑 To stop: docker-compose --profile openmetadata down"
echo "🔄 To restart: docker-compose --profile openmetadata restart"
echo "📊 To view logs: docker-compose --profile openmetadata logs -f"
