#!/bin/bash
# 🚀 Single Command to Restart OpenPolicy Merge Platform V2

echo "🔄 Restarting OpenPolicy Merge Platform V2..."

# Stop all services
echo "🛑 Stopping all services..."
./stop-all.sh 2>/dev/null || true

# Clear any remaining processes
pkill -f "uvicorn app.main:app" 2>/dev/null || true
pkill -f "npm run dev" 2>/dev/null || true
pkill -f "python -c" 2>/dev/null || true

# Clear Python cache files
echo "🧹 Clearing Python cache..."
find services -name "*.pyc" -delete 2>/dev/null || true
find services -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Wait a moment
sleep 2

# Start all services
echo "🚀 Starting all services..."
./start-all.sh

echo "✅ Deployment restart complete!"
echo "📊 Services should be available at:"
echo "   - API Gateway: http://localhost:8000"
echo "   - User Service: http://localhost:8001"
echo "   - Web UI: http://localhost:3000"
echo "   - Admin UI: http://localhost:3001"
echo "   - API Docs: http://localhost:8000/docs"
