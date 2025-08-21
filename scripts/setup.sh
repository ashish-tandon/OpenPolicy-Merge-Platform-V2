#!/bin/bash

# 🚀 OpenPolicy Merge Platform V2 - Complete Setup Script
# This script will set up your entire development environment

set -e  # Exit on any error

echo "🎯 OpenPolicy Merge Platform V2 - Setup Script"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+ first."
        exit 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_error "Node.js version 18+ is required. Current version: $(node --version)"
        exit 1
    fi
    print_success "Node.js $(node --version) ✓"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.11+ first."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
        print_error "Python 3.11+ is required. Current version: $PYTHON_VERSION"
        exit 1
    fi
    print_success "Python $PYTHON_VERSION ✓"
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_warning "Docker is not installed. Some features may not work."
    else
        print_success "Docker $(docker --version) ✓"
    fi
    
    # Check Git
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install Git first."
        exit 1
    fi
    print_success "Git $(git --version | cut -d' ' -f3) ✓"
    
    echo ""
}

# Setup environment files
setup_environment() {
    print_status "Setting up environment files..."
    
    # Root .env
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            print_success "Created .env from .env.example"
        else
            print_warning "No .env.example found. You'll need to create .env manually."
        fi
    else
        print_success ".env already exists ✓"
    fi
    
    # API Gateway .env
    if [ ! -f services/api-gateway/.env ]; then
        if [ -f services/api-gateway/.env.example ]; then
            cp services/api-gateway/.env.example services/api-gateway/.env
            print_success "Created services/api-gateway/.env"
        else
            print_warning "No services/api-gateway/.env.example found."
        fi
    else
        print_success "services/api-gateway/.env already exists ✓"
    fi
    
    # User Service .env
    if [ ! -f services/user-service/.env ]; then
        if [ -f services/user-service/.env.example ]; then
            cp services/user-service/.env.example services/user-service/.env
            print_success "Created services/user-service/.env"
        else
            print_warning "No services/user-service/.env.example found."
        fi
    else
        print_success "services/user-service/.env already exists ✓"
    fi
    
    echo ""
}

# Start database services
start_database() {
    print_status "Starting database services..."
    
    if command -v docker &> /dev/null; then
        if docker-compose ps | grep -q "postgres"; then
            print_success "PostgreSQL is already running ✓"
        else
            print_status "Starting PostgreSQL with Docker..."
            docker-compose up -d postgres
            print_success "PostgreSQL started ✓"
            
            print_status "Waiting for database to be ready..."
            sleep 10
        fi
    else
        print_warning "Docker not available. Please start PostgreSQL manually."
    fi
    
    echo ""
}

# Setup Python virtual environments
setup_python_services() {
    print_status "Setting up Python services..."
    
    # API Gateway
    print_status "Setting up API Gateway..."
    cd services/api-gateway
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Created virtual environment for API Gateway"
    fi
    
    source venv/bin/activate
    pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Installed API Gateway dependencies"
    else
        print_warning "No requirements.txt found for API Gateway"
    fi
    deactivate
    cd ../..
    
    # User Service
    print_status "Setting up User Service..."
    cd services/user-service
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Created virtual environment for User Service"
    fi
    
    source venv/bin/activate
    pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Installed User Service dependencies"
    else
        print_warning "No requirements.txt found for User Service"
    fi
    deactivate
    cd ../..
    
    # ETL Service
    print_status "Setting up ETL Service..."
    cd services/etl
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Created virtual environment for ETL Service"
    fi
    
    source venv/bin/activate
    pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        print_success "Installed ETL Service dependencies"
    else
        print_warning "No requirements.txt found for ETL Service"
    fi
    deactivate
    cd ../..
    
    echo ""
}

# Setup Node.js applications
setup_node_apps() {
    print_status "Setting up Node.js applications..."
    
    # Web App
    if [ -d "apps/web" ]; then
        print_status "Setting up Web App..."
        cd apps/web
        if [ ! -d "node_modules" ]; then
            npm install
            print_success "Installed Web App dependencies"
        else
            print_success "Web App dependencies already installed ✓"
        fi
        cd ../..
    fi
    
    # Admin App
    if [ -d "apps/admin" ]; then
        print_status "Setting up Admin App..."
        cd apps/admin
        if [ ! -d "node_modules" ]; then
            npm install
            print_success "Installed Admin App dependencies"
        else
            print_success "Admin App dependencies already installed ✓"
        fi
        cd ../..
    fi
    
    # Mobile App
    if [ -d "apps/mobile" ]; then
        print_status "Setting up Mobile App..."
        cd apps/mobile
        if [ ! -d "node_modules" ]; then
            npm install
            print_success "Installed Mobile App dependencies"
        else
            print_success "Mobile App dependencies already installed ✓"
        fi
        cd ../..
    fi
    
    echo ""
}

# Run database migrations
run_migrations() {
    print_status "Running database migrations..."
    
    if command -v docker &> /dev/null && docker-compose ps | grep -q "postgres"; then
        # API Gateway migrations
        print_status "Running API Gateway migrations..."
        cd services/api-gateway
        source venv/bin/activate
        if command -v alembic &> /dev/null; then
            alembic upgrade head
            print_success "API Gateway migrations completed ✓"
        else
            print_warning "Alembic not found. Please install it first."
        fi
        deactivate
        cd ../..
        
        # User Service migrations
        print_status "Running User Service migrations..."
        cd services/user-service
        source venv/bin/activate
        if command -v alembic &> /dev/null; then
            alembic upgrade head
            print_success "User Service migrations completed ✓"
        else
            print_warning "Alembic not found. Please install it first."
        fi
        deactivate
        cd ../..
    else
        print_warning "Database not running. Skipping migrations."
    fi
    
    echo ""
}

# Create start scripts
create_start_scripts() {
    print_status "Creating start scripts..."
    
    # Start all services script
    cat > start-all.sh << 'EOF'
#!/bin/bash
# 🚀 Start All OpenPolicy Services

echo "🚀 Starting OpenPolicy Merge Platform V2..."

# Start database
echo "🗄️  Starting database..."
docker-compose up -d postgres redis

# Wait for database
echo "⏳ Waiting for database to be ready..."
sleep 10

# Start API Gateway
echo "⚙️  Starting API Gateway..."
cd services/api-gateway
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
API_PID=$!
cd ../..

# Start User Service
echo "👤 Starting User Service..."
cd services/user-service
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001 &
USER_PID=$!
cd ../..

# Start Web App
echo "🌐 Starting Web App..."
cd apps/web
npm run dev &
WEB_PID=$!
cd ../..

# Start Admin App
echo "⚡ Starting Admin App..."
cd apps/admin
npm run dev &
ADMIN_PID=$!
cd ../..

echo ""
echo "🎉 All services started!"
echo "📊 Services running:"
echo "   - API Gateway: http://localhost:8000"
echo "   - User Service: http://localhost:8001"
echo "   - Web App: http://localhost:3000"
echo "   - Admin App: http://localhost:3001"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo '🛑 Stopping all services...'; kill $API_PID $USER_PID $WEB_PID $ADMIN_PID; exit" INT
wait
EOF
    
    chmod +x start-all.sh
    print_success "Created start-all.sh script"
    
    # Stop all services script
    cat > stop-all.sh << 'EOF'
#!/bin/bash
# 🛑 Stop All OpenPolicy Services

echo "🛑 Stopping OpenPolicy services..."

# Stop database
docker-compose down

# Kill any remaining processes
pkill -f "uvicorn app.main:app"
pkill -f "npm run dev"

echo "✅ All services stopped"
EOF
    
    chmod +x stop-all.sh
    print_success "Created stop-all.sh script"
    
    echo ""
}

# Display final instructions
show_final_instructions() {
    echo ""
    echo "🎉 Setup Complete! 🎉"
    echo "====================="
    echo ""
    echo "Your OpenPolicy Merge Platform V2 is now ready!"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Configure your .env files with your database credentials"
    echo "2. Run: ./start-all.sh to start all services"
    echo "3. Run: ./stop-all.sh to stop all services"
    echo ""
    echo "🌐 Access Points:"
    echo "   - Web App: http://localhost:3000"
    echo "   - Admin App: http://localhost:3001"
    echo "   - API Gateway: http://localhost:8000"
    echo "   - API Documentation: http://localhost:8000/docs"
    echo ""
    echo "📚 Documentation:"
    echo "   - Setup Guide: docs/PROJECT_SETUP_AND_DEPLOYMENT_GUIDE.md"
    echo "   - Project Status: docs/FINAL_PROJECT_STATUS.md"
    echo ""
    echo "🚀 Happy coding!"
    echo ""
}

# Main execution
main() {
    echo "🚀 Starting OpenPolicy Merge Platform V2 setup..."
    echo ""
    
    check_prerequisites
    setup_environment
    start_database
    setup_python_services
    setup_node_apps
    run_migrations
    create_start_scripts
    show_final_instructions
}

# Run main function
main "$@"
