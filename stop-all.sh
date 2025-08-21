#!/bin/bash
# 🛑 Stop All OpenPolicy Services

echo "🛑 Stopping OpenPolicy services..."

# Kill any remaining processes
pkill -f "uvicorn app.main:app"
pkill -f "npm run dev"
pkill -f "python -c"

echo "✅ All services stopped"
