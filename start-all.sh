#!/bin/bash
# 🚀 Start All OpenPolicy Services

echo "🚀 Starting OpenPolicy Merge Platform V2..."

# Start database (if not already running)
echo "🗄️  Checking database status..."
if ! docker-compose ps | grep -q "db.*Up"; then
    echo "Starting database..."
    docker-compose up -d db redis
    echo "⏳ Waiting for database to be ready..."
    sleep 10
else
    echo "Database already running ✓"
fi

# Start API Gateway
echo "⚙️  Starting API Gateway..."
cd services/api-gateway
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
API_PID=$!
cd ../..

# Start User Service (simplified version)
echo "👤 Starting User Service..."
cd services/user-service
source venv/bin/activate
# Start a simple health check endpoint
python -c "
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import threading

app = FastAPI()

@app.get('/health')
async def health_check():
    return JSONResponse({'status': 'healthy', 'service': 'user-service'})

def run_server():
    uvicorn.run(app, host='0.0.0.0', port=8001)

thread = threading.Thread(target=run_server, daemon=True)
thread.start()
" &
USER_PID=$!
cd ../..

# Start Web UI
echo "🌐 Starting Web UI..."
cd services/web-ui
npm run dev &
WEB_PID=$!
cd ../..

# Start Admin UI
echo "⚡ Starting Admin UI..."
cd services/admin-ui
npm run dev &
ADMIN_PID=$!
cd ../..

echo ""
echo "🎉 All services started!"
echo "📊 Services running:"
echo "   - API Gateway: http://localhost:8000"
echo "   - User Service: http://localhost:8001"
echo "   - Web UI: http://localhost:3000"
echo "   - Admin UI: http://localhost:3001"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo '🛑 Stopping all services...'; kill $API_PID $USER_PID $WEB_PID $ADMIN_PID 2>/dev/null; exit" INT
wait
