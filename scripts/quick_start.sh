#!/usr/bin/env bash
set -euo pipefail

# OpenParliament Quick Start Script
# Gets the system up and running quickly

echo "🚀 OpenParliament Quick Start"
echo "============================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1: Starting development environment...${NC}"
make dev

echo -e "${BLUE}Step 2: Waiting for services to be ready...${NC}"
echo "   This may take a few minutes on first run..."

# Wait for database to be ready
max_attempts=60
attempt=1

while [ $attempt -le $max_attempts ]; do
    if docker compose exec db pg_isready -U openpolicy -d openpolicy >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Database is ready${NC}"
        break
    fi
    
    if [ $attempt -eq $max_attempts ]; then
        echo -e "${YELLOW}⚠️  Database took longer than expected to start${NC}"
        break
    fi
    
    echo "   Waiting for database... (attempt $attempt/$max_attempts)"
    sleep 5
    attempt=$((attempt + 1))
done

# Wait for API Gateway to be ready
echo -e "${BLUE}Step 3: Waiting for API Gateway...${NC}"
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:8080/healthz >/dev/null 2>&1; then
        echo -e "${GREEN}✅ API Gateway is ready${NC}"
        break
    fi
    
    if [ $attempt -eq $max_attempts ]; then
        echo -e "${YELLOW}⚠️  API Gateway took longer than expected to start${NC}"
        break
    fi
    
    echo "   Waiting for API Gateway... (attempt $attempt/$max_attempts)"
    sleep 2
    attempt=$((attempt + 1))
done

echo ""
echo -e "${GREEN}🎉 OpenParliament system is ready!${NC}"
echo ""
echo "🌐 Access your system:"
echo "   - API Documentation: http://localhost:8080/docs"
echo "   - Health Check: http://localhost:8080/healthz"
echo "   - Bills API: http://localhost:8080/api/v1/bills/"
echo "   - Members API: http://localhost:8080/api/v1/members/"
echo ""
echo "📊 Database:"
echo "   - Host: localhost:5432"
echo "   - Database: openpolicy"
echo "   - User: openpolicy"
echo "   - Password: openpolicy"
echo ""
echo "🧪 Test the system:"
echo "   make test-openparliament"
echo ""
echo "📝 View logs:"
echo "   make logs"
echo ""
echo "🛑 Stop services:"
echo "   make down"
echo ""
echo "🚀 Your OpenParliament API is now running!"
