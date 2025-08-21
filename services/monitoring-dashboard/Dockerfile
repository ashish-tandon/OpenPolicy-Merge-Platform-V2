FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend application
COPY backend/ ./backend/

# Copy frontend dashboard
COPY dashboard/ ./dashboard/

# Copy nginx configuration
COPY nginx.conf ./nginx.conf

# Install nginx
RUN apt-get update && apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Configure nginx to serve the dashboard
RUN echo 'server { listen 80; server_name localhost; root /app/dashboard; index index.html; location / { try_files $uri $uri/ /index.html; } location /api/ { proxy_pass http://localhost:8083/; proxy_set_header Host $host; proxy_set_header X-Real-IP $remote_addr; proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; proxy_set_header X-Forwarded-Proto $scheme; } }' > /etc/nginx/sites-available/default

# Create startup script
RUN echo '#!/bin/bash\n\
echo "🚀 Starting Monitoring Dashboard Backend..."\n\
cd /app/backend\n\
python -m uvicorn app:app --host 0.0.0.0 --port 8083 &\n\
echo "✅ Backend started in background"\n\
echo "🚀 Starting Nginx..."\n\
nginx -g "daemon off;"' > /start.sh && \
chmod +x /start.sh

# Expose ports
EXPOSE 80 8083

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Start both services
CMD ["/start.sh"]
