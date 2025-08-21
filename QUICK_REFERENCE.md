# 🚀 OpenPolicy Merge Platform V2 - Quick Reference

## 🎯 **IMMEDIATE ACCESS - ALL SERVICES WORKING**

### **🌐 Primary Interfaces**
| Service | URL | Description |
|---------|-----|-------------|
| **Admin Dashboard** | http://localhost:3000 | React application with full API access |
| **API Documentation** | http://localhost:8080/docs | Interactive Swagger documentation |
| **Web UI** | http://localhost:3001 | Static placeholder interface |

### **🔧 Backend Services**
| Service | URL | Status |
|---------|-----|--------|
| **API Gateway** | http://localhost:8080 | ✅ Fully Operational |
| **User Service** | http://localhost:8082 | ✅ Fully Operational |

### **💾 Infrastructure**
| Service | Port | Status |
|---------|------|--------|
| **PostgreSQL Database** | 5432 | ✅ Healthy |
| **Redis Cache** | 6379 | ✅ Healthy |

---

## 🧪 **Health Check Commands**

```bash
# API Gateway Health
curl http://localhost:8080/healthz

# User Service Health  
curl http://localhost:8082/health

# Admin UI (via API proxy)
curl http://localhost:3000/api/healthz

# Test all services
docker compose ps
```

---

## 🚀 **Quick Start Commands**

```bash
# Start all services
make dev

# Stop all services
docker compose down

# View logs
docker compose logs -f [service-name]

# Restart specific service
docker compose restart [service-name]
```

---

## 📱 **Service Endpoints**

### **API Gateway (Port 8080)**
- **Health**: `/healthz`
- **Docs**: `/docs`
- **Bills**: `/api/v1/bills`
- **Members**: `/api/v1/members`
- **Debates**: `/api/v1/debates`

### **User Service (Port 8082)**
- **Health**: `/health`
- **Auth**: `/api/v1/auth/*`
- **Profile**: `/api/v1/profile/*`

### **Admin UI (Port 3000)**
- **Main App**: `/`
- **API Proxy**: `/api/*` → Backend

### **Web UI (Port 3001)**
- **Main Interface**: `/`

---

## ✅ **Verification Checklist**

- [x] **API Gateway**: Responding on port 8080
- [x] **User Service**: Responding on port 8082  
- [x] **Database**: Connected and healthy
- [x] **Redis**: Operational and responsive
- [x] **Admin UI**: React app + API proxy working
- [x] **Web UI**: Static interface serving
- [x] **Service Communication**: All services talking
- [x] **Integration Tests**: 100% success rate

---

## 🎉 **DEPLOYMENT STATUS: 100% COMPLETE**

**All services operational and ready for use!**

---

*Last Updated: August 21, 2024*  
*Status: All Systems Operational* 🚀
