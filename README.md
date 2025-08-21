# 🚀 OpenPolicy Merge Platform V2

> **Status**: ✅ **COMPLETE - READY FOR PRODUCTION**  
> A comprehensive merge of multiple OpenPolicy repositories into a unified, modern monorepo platform.

## 🎯 Project Overview

OpenPolicy Merge Platform V2 is the successful consolidation of **13 repositories** into a unified, production-ready platform that includes:

- 🌐 **Modern Web Applications** (Next.js, React, TypeScript)
- ⚙️ **Backend Services** (FastAPI, PostgreSQL, Redis)
- 📊 **ETL Pipeline** (109+ Canadian municipal scrapers)
- 🎨 **Admin Dashboard** (Comprehensive administrative interface)
- 📚 **Legacy Integration** (All historical data preserved)
- 🗄️ **Database Infrastructure** (PostgreSQL with migrations)

## 🏆 What's Been Accomplished

- ✅ **13 repositories successfully merged** into unified monorepo
- ✅ **All legacy code preserved** in `/legacy/` directory
- ✅ **120+ OpenParliament.ca features** successfully migrated
- ✅ **109+ municipal scrapers** integrated and functional
- ✅ **Modern architecture** with FastAPI + React stack
- ✅ **Complete documentation** and deployment guides
- ✅ **Production-ready infrastructure** with monitoring

## 🚀 Quick Start

### Prerequisites

- **Node.js**: 18+ (LTS recommended)
- **Python**: 3.11+
- **PostgreSQL**: 14+
- **Docker**: 20.10+ (optional but recommended)

### One-Command Setup

```bash
# Clone the repository
git clone https://github.com/ashish-tandon/OpenPolicy-Merge-Platform-V2.git
cd OpenPolicy-Merge-Platform-V2

# Run the automated setup script
./scripts/setup.sh
```

### Manual Setup

```bash
# 1. Environment setup
cp .env.example .env
cp services/api-gateway/.env.example services/api-gateway/.env
cp services/user-service/.env.example services/user-service/.env

# 2. Start database
docker-compose up -d postgres

# 3. Install dependencies
cd services/api-gateway && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cd ../user-service && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cd ../../apps/web && npm install
cd ../admin && npm install

# 4. Run migrations
cd ../../services/api-gateway && source venv/bin/activate && alembic upgrade head
cd ../user-service && source venv/bin/activate && alembic upgrade head

# 5. Start services
./start-all.sh
```

## 🌐 Access Points

Once running, access your platform at:

- **Web Application**: http://localhost:3000
- **Admin Dashboard**: http://localhost:3001
- **API Gateway**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **User Service**: http://localhost:8001

## 🏗️ Architecture

```
OpenPolicy Merge Platform V2/
├── 🎨 apps/                    # Frontend applications
│   ├── web/                    # Main web interface (Next.js)
│   ├── mobile/                 # Mobile application (React Native)
│   └── admin/                  # Admin dashboard (React)
├── ⚙️ services/                # Backend services
│   ├── api-gateway/            # Main API service (FastAPI)
│   ├── etl/                    # Data pipeline (Python)
│   ├── user-service/           # User management (FastAPI)
│   └── admin-ui/               # Admin interface (React)
├── 📦 packages/                # Shared packages
├── 🗄️ db/                     # Database setup
├── 📚 legacy/                  # Legacy code (read-only)
└── 📖 docs/                    # Documentation
```

## 📚 Documentation

- **[Complete Setup Guide](docs/PROJECT_SETUP_AND_DEPLOYMENT_GUIDE.md)** - Step-by-step deployment instructions
- **[Project Status](docs/FINAL_PROJECT_STATUS.md)** - Comprehensive project completion summary
- **[API Documentation](http://localhost:8000/docs)** - Interactive API reference
- **[Architecture Decisions](docs/ADR/)** - Technical decision records

## 🔧 Development

### Running Tests

```bash
# Backend tests
cd services/api-gateway && pytest tests/ -v
cd services/user-service && pytest tests/ -v

# Frontend tests
cd apps/web && npm test
cd apps/admin && npm test
```

### Development Commands

```bash
# Start all services
./start-all.sh

# Stop all services
./stop-all.sh

# View logs
docker-compose logs -f

# Run migrations
cd services/api-gateway && alembic upgrade head
```

## 🚀 Deployment

### Production

```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose exec api-gateway alembic upgrade head
```

### Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s/

# Check status
kubectl get pods -n openpolicy
```

## 🌟 Key Features

- **Unified Platform**: Single codebase for all OpenPolicy functionality
- **Modern Stack**: FastAPI + React + TypeScript + PostgreSQL
- **Data Integration**: 109+ municipal scrapers and legacy systems
- **Admin Interface**: Comprehensive system administration
- **API First**: RESTful APIs with OpenAPI documentation
- **Scalable**: Containerized with Kubernetes support
- **Secure**: JWT authentication, RBAC, and security best practices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the `/docs/` directory
- **Issues**: [GitHub Issues](https://github.com/ashish-tandon/OpenPolicy-Merge-Platform-V2/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ashish-tandon/OpenPolicy-Merge-Platform-V2/discussions)

## 🎉 Project Status

**The OpenPolicy Merge Platform V2 project is now COMPLETE and ready for production deployment.**

This represents the successful consolidation of years of development work into a modern, maintainable platform that preserves all legacy functionality while providing a foundation for future development.

---

**🚀 Ready to deploy? Follow the [Complete Setup Guide](docs/PROJECT_SETUP_AND_DEPLOYMENT_GUIDE.md) to get your platform running in production!**
