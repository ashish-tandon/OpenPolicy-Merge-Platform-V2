# OpenPolicy User Service

A dedicated microservice for user management and authentication, completely separate from legislative data to maintain clean architecture and security boundaries.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER SERVICE ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│ 1. Authentication Layer                                        │
│    • JWT Token Management                                      │
│    • OAuth Integration (Google, GitHub)                        │
│    • Multi-Factor Authentication (SMS, Email, TOTP)            │
│                                                                │
│ 2. User Management Layer                                       │
│    • User CRUD Operations                                      │
│    • Role-Based Access Control                                 │
│    • Profile Management                                        │
│                                                                │
│ 3. Security Layer                                              │
│    • Password Policies                                         │
│    • Session Management                                        │
│    • Rate Limiting                                             │
│                                                                │
│ 4. Data Layer                                                  │
│    • Separate User Database                                    │
│    • Redis for Sessions                                        │
│    • No Legislative Data                                       │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Features

### ✅ **Authentication & Security**
- **JWT Token Management**: Access and refresh tokens with configurable expiration
- **OAuth Integration**: Google and GitHub authentication
- **Multi-Factor Authentication**: SMS OTP, Email OTP, TOTP (Google Authenticator)
- **Password Policies**: Strong password requirements with validation
- **Session Management**: Track and manage user sessions across devices
- **Rate Limiting**: Protect against brute force attacks

### ✅ **User Management**
- **5 User Roles**: Normal, Enterprise, Representative, Moderator, Admin
- **3 Account Types**: Consumer, Internal, Test
- **Profile Management**: Update personal information and preferences
- **Role-Based Access Control**: Granular permissions based on user role
- **User Status Management**: Active, Suspended, Pending, Deactivated

### ✅ **API Endpoints**
- **Authentication**: `/api/v1/auth/*` - Login, register, OAuth, password reset
- **User Management**: `/api/v1/users/*` - Profile, CRUD operations, role updates
- **Health Checks**: `/api/v1/health/*` - Service status and readiness

## 🛠️ Technology Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL (separate from legislative data)
- **Cache/Sessions**: Redis
- **Authentication**: JWT, OAuth2
- **MFA**: Twilio SMS, TOTP
- **Validation**: Pydantic
- **Testing**: pytest

## 📁 Project Structure

```
services/user-service/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── users.py         # User management endpoints
│   │       └── health.py        # Health check endpoints
│   ├── auth/
│   │   ├── jwt_handler.py       # JWT token management
│   │   ├── oauth_handler.py     # OAuth integration
│   │   └── mfa_handler.py       # Multi-factor authentication
│   ├── config/
│   │   └── settings.py          # Configuration management
│   ├── models/
│   │   ├── user.py              # User data model
│   │   ├── otp.py               # OTP model for MFA
│   │   └── user_session.py      # User session tracking
│   └── main.py                  # FastAPI application
├── tests/                       # Test suite
├── docs/                        # Documentation
├── requirements.txt              # Python dependencies
└── README.md                    # This file
```

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
cd services/user-service
pip install -r requirements.txt
```

### 2. **Environment Configuration**
Create a `.env` file:
```bash
# Service Configuration
ENV=local
DEBUG=true
SERVICE_HOST=0.0.0.0
SERVICE_PORT=8081

# Database
USER_DATABASE_URL=postgresql+psycopg://openpolicy:openpolicy@db:5432/openpolicy_users

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production

# OAuth (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Twilio SMS (Optional)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

# Redis
REDIS_URL=redis://redis:6379/1
```

### 3. **Run the Service**
```bash
# Development mode
uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload

# Or use the main.py
python app/main.py
```

### 4. **Access the API**
- **API Documentation**: http://localhost:8081/docs
- **Health Check**: http://localhost:8081/health
- **Root Endpoint**: http://localhost:8081/

## 🔐 Authentication Flow

### **1. User Registration**
```bash
POST /api/v1/auth/register
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "SecurePass123!",
  "phone": "+1234567890",
  "postal_code": "M5A 0H4",
  "role": "normal",
  "account_type": "consumer"
}
```

### **2. User Login**
```bash
POST /api/v1/auth/login
{
  "email": "john.doe@example.com",
  "password": "SecurePass123!"
}
```

### **3. OAuth Login**
```bash
POST /api/v1/auth/oauth/login
{
  "provider": "google",
  "token": "google-id-token"
}
```

### **4. MFA Setup**
```bash
# Request SMS OTP
POST /api/v1/auth/otp/request
{
  "phone": "+1234567890",
  "otp_type": "sms"
}

# Verify OTP
POST /api/v1/auth/otp/verify
{
  "phone": "+1234567890",
  "otp": "123456",
  "otp_type": "sms"
}
```

## 🗄️ Database Schema

### **Users Table**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE,
    postal_code VARCHAR(10),
    password_hash VARCHAR(255),
    email_verified_at TIMESTAMP,
    phone_verified_at TIMESTAMP,
    two_factor_enabled BOOLEAN DEFAULT FALSE,
    two_factor_secret VARCHAR(255),
    role VARCHAR(50) DEFAULT 'normal',
    account_type VARCHAR(50) DEFAULT 'consumer',
    status VARCHAR(50) DEFAULT 'active',
    avatar_url VARCHAR(500),
    preferences TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login_at TIMESTAMP,
    deleted_at TIMESTAMP,
    account_deletion_reason TEXT
);
```

### **OTPs Table**
```sql
CREATE TABLE otps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone VARCHAR(20) NOT NULL,
    otp VARCHAR(10) NOT NULL,
    otp_type VARCHAR(20) DEFAULT 'sms',
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    attempts INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    used_at TIMESTAMP
);
```

### **User Sessions Table**
```sql
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    session_token VARCHAR(500) NOT NULL UNIQUE,
    refresh_token VARCHAR(500) UNIQUE,
    token_type VARCHAR(20) DEFAULT 'jwt',
    user_agent TEXT,
    ip_address VARCHAR(45),
    device_type VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_used_at TIMESTAMP DEFAULT NOW(),
    revoked_at TIMESTAMP
);
```

## 🔒 Security Features

### **Password Requirements**
- Minimum 8 characters
- At least one uppercase letter
- At least one number
- At least one special character

### **JWT Security**
- Access tokens expire in 30 minutes
- Refresh tokens expire in 7 days
- Token type validation
- Secure secret key management

### **Rate Limiting**
- 100 requests per minute per IP
- 1000 requests per hour per IP
- Configurable limits per endpoint

### **MFA Security**
- SMS OTP valid for 15 minutes
- Maximum 3 attempts per OTP
- TOTP with Google Authenticator support
- Secure secret generation

## 🧪 Testing

### **Run Tests**
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

### **Test Coverage**
- Unit tests for all authentication handlers
- Integration tests for API endpoints
- Mock database and external services
- Test all user roles and permissions

## 📊 Monitoring & Health

### **Health Endpoints**
- `/health` - Detailed service health
- `/health/ready` - Readiness check
- `/health/live` - Liveness check

### **Metrics**
- Request/response times
- Error rates
- User authentication success/failure
- MFA usage statistics

## 🔄 Integration with Other Services

### **API Gateway**
The User Service integrates with the main API Gateway to provide authentication for all other services.

### **Admin UI**
The Admin UI uses the User Service for user management and authentication.

### **Web UI**
The main Web UI uses the User Service for user authentication and profile management.

### **Legislative Services**
- **No direct data sharing** - User Service is completely separate
- **Authentication only** - Provides JWT tokens for access control
- **Clean boundaries** - Legislative services only know user IDs and roles

## 🚨 Security Considerations

### **Production Deployment**
- Change default JWT secret key
- Use environment variables for all secrets
- Enable HTTPS/TLS
- Configure proper CORS origins
- Set up database connection pooling
- Enable Redis authentication

### **Data Privacy**
- User data is completely separate from legislative data
- No cross-contamination between services
- GDPR compliance ready
- Data retention policies
- User data export/deletion capabilities

## 📈 Future Enhancements

### **Phase 2**
- [ ] Database integration with SQLAlchemy
- [ ] Redis session management
- [ ] Email service integration
- [ ] Audit logging
- [ ] User activity tracking

### **Phase 3**
- [ ] Advanced MFA options
- [ ] Social login providers
- [ ] User analytics dashboard
- [ ] Bulk user operations
- [ ] Advanced role permissions

### **Phase 4**
- [ ] Microservice communication
- [ ] Event-driven architecture
- [ ] Advanced security features
- [ ] Performance optimization
- [ ] Auto-scaling

## 🤝 Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Follow security best practices
5. Maintain separation from legislative data

## 📄 License

This service is part of the OpenPolicy platform and follows the same licensing terms.

---

**Note**: This User Service is designed to be completely independent from legislative data. It provides authentication and user management capabilities while maintaining clean architectural boundaries and security isolation.
