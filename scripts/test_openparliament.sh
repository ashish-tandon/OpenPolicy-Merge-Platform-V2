#!/usr/bin/env bash
set -euo pipefail

# OpenParliament System Test Script
# Tests the complete OpenParliament integration

echo "🧪 Testing OpenParliament System Integration"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    if [ "$status" = "OK" ]; then
        echo -e "${GREEN}✅ $message${NC}"
    elif [ "$status" = "WARN" ]; then
        echo -e "${YELLOW}⚠️  $message${NC}"
    else
        echo -e "${RED}❌ $message${NC}"
    fi
}

# Check if services are running
echo ""
echo "1. Checking service status..."

if docker compose ps | grep -q "Up"; then
    print_status "OK" "Services are running"
else
    print_status "WARN" "Services not running. Starting them..."
    make dev
    sleep 10
fi

# Wait for services to be healthy
echo ""
echo "2. Waiting for services to be healthy..."

max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:8080/healthz >/dev/null 2>&1; then
        print_status "OK" "API Gateway is healthy"
        break
    fi
    
    if [ $attempt -eq $max_attempts ]; then
        print_status "ERROR" "API Gateway failed to become healthy after $max_attempts attempts"
        exit 1
    fi
    
    echo "   Attempt $attempt/$max_attempts: Waiting for API Gateway..."
    sleep 2
    attempt=$((attempt + 1))
done

# Test database connection
echo ""
echo "3. Testing database connection..."

if docker compose exec db pg_isready -U openpolicy -d openpolicy >/dev/null 2>&1; then
    print_status "OK" "Database is ready"
else
    print_status "ERROR" "Database is not ready"
    exit 1
fi

# Test API endpoints
echo ""
echo "4. Testing API endpoints..."

# Test health endpoint
if curl -f http://localhost:8080/healthz >/dev/null 2>&1; then
    print_status "OK" "Health endpoint (/healthz)"
else
    print_status "ERROR" "Health endpoint failed"
fi

# Test version endpoint
if curl -f http://localhost:8080/version >/dev/null 2>&1; then
    print_status "OK" "Version endpoint (/version)"
else
    print_status "ERROR" "Version endpoint failed"
fi

# Test bills endpoint
if curl -f http://localhost:8080/api/v1/bills/ >/dev/null 2>&1; then
    print_status "OK" "Bills endpoint (/api/v1/bills/)"
else
    print_status "ERROR" "Bills endpoint failed"
fi

# Test members endpoint
if curl -f http://localhost:8080/api/v1/members/ >/dev/null 2>&1; then
    print_status "OK" "Members endpoint (/api/v1/members/)"
else
    print_status "ERROR" "Members endpoint failed"
fi

# Test API documentation
if curl -f http://localhost:8080/docs >/dev/null 2>&1; then
    print_status "OK" "API documentation (/docs)"
else
    print_status "ERROR" "API documentation failed"
fi

# Test database schema
echo ""
echo "5. Testing database schema..."

# Check if openparliament schema exists
schema_check=$(docker compose exec db psql -U openpolicy -d openpolicy -t -c "
    SELECT EXISTS (
        SELECT 1 FROM information_schema.schemata 
        WHERE schema_name = 'openparliament'
    );
" | tr -d ' ')

if [ "$schema_check" = "t" ]; then
    print_status "OK" "OpenParliament schema exists"
else
    print_status "ERROR" "OpenParliament schema missing"
fi

# Check if tables exist
tables_check=$(docker compose exec db psql -U openpolicy -d openpolicy -t -c "
    SELECT COUNT(*) FROM information_schema.tables 
    WHERE table_schema = 'openparliament';
" | tr -d ' ')

if [ "$tables_check" -gt 0 ]; then
    print_status "OK" "OpenParliament tables exist ($tables_check tables)"
else
    print_status "ERROR" "No OpenParliament tables found"
fi

# Test sample data
echo ""
echo "6. Testing sample data..."

# Check if we have sample data
bills_count=$(docker compose exec db psql -U openpolicy -d openpolicy -t -c "
    SELECT COUNT(*) FROM openparliament.bills;
" | tr -d ' ')

members_count=$(docker compose exec db psql -U openpolicy -d openpolicy -t -c "
    SELECT COUNT(*) FROM openparliament.members;
" | tr -d ' ')

parties_count=$(docker compose exec db psql -U openpolicy -d openpolicy -t -c "
    SELECT COUNT(*) FROM openparliament.parties;
" | tr -d ' ')

if [ "$bills_count" -gt 0 ]; then
    print_status "OK" "Sample bills data: $bills_count bills"
else
    print_status "WARN" "No sample bills data found"
fi

if [ "$members_count" -gt 0 ]; then
    print_status "OK" "Sample members data: $members_count MPs"
else
    print_status "WARN" "No sample members data found"
fi

if [ "$parties_count" -gt 0 ]; then
    print_status "OK" "Sample parties data: $parties_count parties"
else
    print_status "WARN" "No sample parties data found"
fi

# Test full-text search
echo ""
echo "7. Testing full-text search..."

search_test=$(docker compose exec db psql -U openpolicy -d openpolicy -t -c "
    SELECT COUNT(*) FROM openparliament.bills 
    WHERE to_tsvector('english', title || ' ' || COALESCE(summary, '')) @@ plainto_tsquery('english', 'covid');
" | tr -d ' ')

if [ "$search_test" -gt 0 ]; then
    print_status "OK" "Full-text search working (found $search_test COVID-related bills)"
else
    print_status "WARN" "Full-text search test returned no results"
fi

# Test API with real data
echo ""
echo "8. Testing API with real data..."

# Test bills list
bills_response=$(curl -s http://localhost:8080/api/v1/bills/)
if echo "$bills_response" | grep -q "items"; then
    print_status "OK" "Bills API returning data"
else
    print_status "ERROR" "Bills API not returning expected format"
fi

# Test members list
members_response=$(curl -s http://localhost:8080/api/v1/members/)
if echo "$members_response" | grep -q "items"; then
    print_status "OK" "Members API returning data"
else
    print_status "ERROR" "Members API not returning expected format"
fi

# Test search functionality
search_response=$(curl -s "http://localhost:8080/api/v1/bills/?q=covid")
if echo "$search_response" | grep -q "items"; then
    print_status "OK" "Search functionality working"
else
    print_status "WARN" "Search functionality test failed"
fi

# Final summary
echo ""
echo "🎯 OpenParliament System Test Summary"
echo "====================================="

if [ "$schema_check" = "t" ] && [ "$tables_check" -gt 0 ]; then
    print_status "OK" "Database schema: COMPLETE"
else
    print_status "ERROR" "Database schema: INCOMPLETE"
fi

if curl -f http://localhost:8080/healthz >/dev/null 2>&1; then
    print_status "OK" "API Gateway: RUNNING"
else
    print_status "ERROR" "API Gateway: FAILED"
fi

if [ "$bills_count" -gt 0 ] && [ "$members_count" -gt 0 ]; then
    print_status "OK" "Sample data: LOADED"
else
    print_status "WARN" "Sample data: MISSING"
fi

echo ""
echo "🌐 Access your OpenParliament API:"
echo "   - API Documentation: http://localhost:8080/docs"
echo "   - Health Check: http://localhost:8080/healthz"
echo "   - Bills API: http://localhost:8080/api/v1/bills/"
echo "   - Members API: http://localhost:8080/api/v1/members/"
echo ""
echo "📊 Database Status:"
echo "   - Host: localhost:5432"
echo "   - Database: openpolicy"
echo "   - User: openpolicy"
echo "   - Password: openpolicy"
echo ""
echo "🎉 OpenParliament integration test complete!"
