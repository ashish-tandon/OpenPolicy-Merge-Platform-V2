#!/bin/bash

echo "🚀 Starting OpenParliament.ca V2 with crash protection..."

# Kill any existing Next.js processes
pkill -f "next dev" 2>/dev/null
sleep 2

# Clear Next.js cache if it exists
if [ -d ".next" ]; then
    echo "🧹 Clearing Next.js cache..."
    rm -rf .next
fi

# Set environment variables for stability
export NODE_OPTIONS="--max-old-space-size=2048 --no-warnings"
export NEXT_TELEMETRY_DISABLED=1

# Start the development server with monitoring
while true; do
    echo "🔄 Starting Next.js development server..."
    npm run dev
    
    if [ $? -eq 0 ]; then
        echo "✅ Server exited normally"
        break
    else
        echo "❌ Server crashed, restarting in 5 seconds..."
        sleep 5
    fi
done
