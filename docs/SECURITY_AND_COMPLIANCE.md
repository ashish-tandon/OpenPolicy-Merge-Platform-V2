# Security and Compliance Documentation

## Table of Contents
1. [Security Architecture](#security-architecture)
2. [Authentication & Authorization](#authentication--authorization)
3. [Data Protection](#data-protection)
4. [Privacy Compliance](#privacy-compliance)
5. [Security Controls](#security-controls)
6. [Vulnerability Management](#vulnerability-management)
7. [Incident Response](#incident-response)
8. [Compliance Requirements](#compliance-requirements)
9. [Security Monitoring](#security-monitoring)
10. [Security Best Practices](#security-best-practices)

---

## Security Architecture

### Defense in Depth Strategy
```
┌─────────────────────────────────────────────────────┐
│                   WAF (CloudFlare)                  │
├─────────────────────────────────────────────────────┤
│              Load Balancer (HTTPS Only)             │
├─────────────────────────────────────────────────────┤
│          API Gateway (Rate Limiting, Auth)          │
├─────────────────────────────────────────────────────┤
│     Application Layer (Input Validation, CORS)      │
├─────────────────────────────────────────────────────┤
│      Data Layer (Encryption, Access Control)        │
└─────────────────────────────────────────────────────┘
```

### Security Zones
1. **Public Zone**: CDN, static assets
2. **DMZ**: API Gateway, load balancers
3. **Application Zone**: Web servers, app servers
4. **Data Zone**: Databases, object storage
5. **Management Zone**: Admin interfaces, monitoring

### Network Security
```yaml
# Kubernetes NetworkPolicy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-gateway-policy
spec:
  podSelector:
    matchLabels:
      app: api-gateway
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: web-ui
    - podSelector:
        matchLabels:
          app: load-balancer
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 5432
    - protocol: TCP
      port: 6379
```

---

## Authentication & Authorization

### Authentication Flow
```python
# JWT-based authentication
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Configuration
SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await get_user(username=username)
    if user is None:
        raise credentials_exception
    return user
```

### OAuth2 Integration
```python
# Google OAuth2 configuration
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.environ['GOOGLE_CLIENT_ID'],
    client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/auth/google')
async def google_login(request):
    redirect_uri = request.url_for('google_auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.route('/auth/google/callback')
async def google_auth(request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    
    # Create or update user in database
    db_user = await create_or_update_user(
        email=user['email'],
        name=user['name'],
        picture=user['picture'],
        provider='google'
    )
    
    # Generate JWT
    access_token = create_access_token(data={"sub": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}
```

### Role-Based Access Control (RBAC)
```python
# Permission system
from enum import Enum
from typing import List

class Role(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    GUEST = "guest"

class Permission(str, Enum):
    # Bills
    BILL_READ = "bill:read"
    BILL_WRITE = "bill:write"
    BILL_DELETE = "bill:delete"
    
    # Users
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"
    
    # Scrapers
    SCRAPER_READ = "scraper:read"
    SCRAPER_WRITE = "scraper:write"
    SCRAPER_EXECUTE = "scraper:execute"

# Role-Permission mapping
ROLE_PERMISSIONS = {
    Role.ADMIN: [p for p in Permission],  # All permissions
    Role.MODERATOR: [
        Permission.BILL_READ,
        Permission.BILL_WRITE,
        Permission.USER_READ,
        Permission.SCRAPER_READ,
        Permission.SCRAPER_EXECUTE,
    ],
    Role.USER: [
        Permission.BILL_READ,
        Permission.USER_READ,
    ],
    Role.GUEST: [
        Permission.BILL_READ,
    ],
}

def has_permission(user_role: Role, required_permission: Permission) -> bool:
    return required_permission in ROLE_PERMISSIONS.get(user_role, [])

# Dependency for route protection
def require_permission(permission: Permission):
    async def permission_checker(current_user = Depends(get_current_user)):
        if not has_permission(current_user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return permission_checker

# Usage in routes
@app.delete("/api/v1/bills/{bill_id}")
async def delete_bill(
    bill_id: str,
    current_user = Depends(require_permission(Permission.BILL_DELETE))
):
    # Only admins can delete bills
    return await delete_bill_from_db(bill_id)
```

---

## Data Protection

### Encryption at Rest
```python
# Database field encryption
from cryptography.fernet import Fernet
import base64

class EncryptedField:
    def __init__(self, key: str):
        self.cipher = Fernet(base64.urlsafe_b64encode(key.encode()[:32].ljust(32)))
    
    def encrypt(self, value: str) -> str:
        if value is None:
            return None
        return self.cipher.encrypt(value.encode()).decode()
    
    def decrypt(self, value: str) -> str:
        if value is None:
            return None
        return self.cipher.decrypt(value.encode()).decode()

# Usage in SQLAlchemy models
from sqlalchemy.ext.hybrid import hybrid_property

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID, primary_key=True, default=uuid4)
    email = Column(String, unique=True, nullable=False)
    _phone_encrypted = Column("phone", String)
    _ssn_encrypted = Column("ssn", String)
    
    _encryptor = EncryptedField(os.environ["FIELD_ENCRYPTION_KEY"])
    
    @hybrid_property
    def phone(self):
        return self._encryptor.decrypt(self._phone_encrypted)
    
    @phone.setter
    def phone(self, value):
        self._phone_encrypted = self._encryptor.encrypt(value)
```

### Encryption in Transit
```nginx
# Nginx SSL configuration
server {
    listen 443 ssl http2;
    server_name api.openpolicy.ca;
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/openpolicy.ca/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/openpolicy.ca/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';" always;
    
    location / {
        proxy_pass http://api-gateway:8080;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Data Masking & Anonymization
```python
# PII masking for logs and exports
import re
from typing import Dict, Any

class DataMasker:
    @staticmethod
    def mask_email(email: str) -> str:
        if not email:
            return email
        parts = email.split('@')
        if len(parts) != 2:
            return email
        username = parts[0]
        if len(username) <= 3:
            masked = '*' * len(username)
        else:
            masked = username[:2] + '*' * (len(username) - 3) + username[-1]
        return f"{masked}@{parts[1]}"
    
    @staticmethod
    def mask_phone(phone: str) -> str:
        if not phone:
            return phone
        # Keep area code, mask rest
        cleaned = re.sub(r'\D', '', phone)
        if len(cleaned) >= 10:
            return f"{cleaned[:3]}-***-**{cleaned[-2:]}"
        return '*' * len(phone)
    
    @staticmethod
    def mask_ssn(ssn: str) -> str:
        if not ssn:
            return ssn
        cleaned = re.sub(r'\D', '', ssn)
        if len(cleaned) == 9:
            return f"***-**-{cleaned[-4:]}"
        return '*' * len(ssn)
    
    @classmethod
    def mask_dict(cls, data: Dict[str, Any], fields_to_mask: List[str]) -> Dict[str, Any]:
        masked_data = data.copy()
        for field in fields_to_mask:
            if field in masked_data and masked_data[field]:
                if 'email' in field.lower():
                    masked_data[field] = cls.mask_email(masked_data[field])
                elif 'phone' in field.lower():
                    masked_data[field] = cls.mask_phone(masked_data[field])
                elif 'ssn' in field.lower():
                    masked_data[field] = cls.mask_ssn(masked_data[field])
                else:
                    # Generic masking
                    value = str(masked_data[field])
                    masked_data[field] = value[:2] + '*' * (len(value) - 4) + value[-2:] if len(value) > 4 else '*' * len(value)
        return masked_data
```

---

## Privacy Compliance

### PIPEDA Compliance (Canada)
```python
# Privacy consent management
class ConsentManager:
    CONSENT_TYPES = {
        'data_collection': 'Collection of personal information',
        'data_processing': 'Processing of personal data',
        'marketing': 'Marketing communications',
        'analytics': 'Analytics and performance tracking',
        'third_party': 'Sharing with third parties'
    }
    
    async def record_consent(self, user_id: str, consent_type: str, granted: bool):
        consent = Consent(
            user_id=user_id,
            consent_type=consent_type,
            granted=granted,
            timestamp=datetime.utcnow(),
            ip_address=request.client.host,
            user_agent=request.headers.get('User-Agent')
        )
        await db.save(consent)
    
    async def get_user_consents(self, user_id: str) -> Dict[str, bool]:
        consents = await db.query(Consent).filter_by(user_id=user_id).all()
        return {c.consent_type: c.granted for c in consents}
    
    async def has_consent(self, user_id: str, consent_type: str) -> bool:
        consent = await db.query(Consent).filter_by(
            user_id=user_id,
            consent_type=consent_type
        ).order_by(Consent.timestamp.desc()).first()
        return consent and consent.granted
```

### Data Subject Rights
```python
# PIPEDA/GDPR compliance endpoints
@app.get("/api/v1/privacy/my-data")
async def export_user_data(current_user = Depends(get_current_user)):
    """Export all user data (Right to Access)"""
    user_data = {
        'profile': await get_user_profile(current_user.id),
        'activities': await get_user_activities(current_user.id),
        'votes': await get_user_votes(current_user.id),
        'saved_items': await get_user_saved_items(current_user.id),
        'search_history': await get_user_search_history(current_user.id),
        'consents': await consent_manager.get_user_consents(current_user.id)
    }
    
    # Generate downloadable file
    return FileResponse(
        path=generate_user_data_export(user_data),
        filename=f"user_data_{current_user.id}.json",
        media_type="application/json"
    )

@app.delete("/api/v1/privacy/delete-account")
async def delete_user_account(current_user = Depends(get_current_user)):
    """Delete user account and all associated data (Right to Erasure)"""
    # Anonymize rather than hard delete for data integrity
    await anonymize_user_data(current_user.id)
    await deactivate_user_account(current_user.id)
    
    return {"message": "Account deleted successfully"}

@app.put("/api/v1/privacy/data-portability")
async def export_portable_data(current_user = Depends(get_current_user)):
    """Export data in machine-readable format (Right to Data Portability)"""
    data = await get_portable_user_data(current_user.id)
    
    return Response(
        content=json.dumps(data, indent=2),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=openpolicy_data_{current_user.id}.json"
        }
    )
```

### Privacy Policy Implementation
```python
# Privacy policy versioning
class PrivacyPolicy:
    def __init__(self):
        self.current_version = "2.0"
        self.effective_date = "2024-01-01"
        self.minimum_age = 13
    
    async def user_accepted_current_policy(self, user_id: str) -> bool:
        acceptance = await db.query(PolicyAcceptance).filter_by(
            user_id=user_id,
            policy_version=self.current_version
        ).first()
        return acceptance is not None
    
    async def record_acceptance(self, user_id: str):
        acceptance = PolicyAcceptance(
            user_id=user_id,
            policy_version=self.current_version,
            accepted_at=datetime.utcnow(),
            ip_address=request.client.host
        )
        await db.save(acceptance)

# Middleware to enforce privacy policy acceptance
@app.middleware("http")
async def privacy_policy_middleware(request: Request, call_next):
    if request.url.path.startswith("/api/v1/") and request.method != "GET":
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if token:
            user = await get_user_from_token(token)
            if user and not await privacy_policy.user_accepted_current_policy(user.id):
                return JSONResponse(
                    status_code=403,
                    content={"detail": "Privacy policy acceptance required"}
                )
    return await call_next(request)
```

---

## Security Controls

### Input Validation
```python
# Comprehensive input validation
from pydantic import BaseModel, validator, constr, EmailStr
import bleach

class BillCreate(BaseModel):
    title: constr(min_length=1, max_length=500)
    description: constr(min_length=1, max_length=10000)
    jurisdiction_id: UUID
    
    @validator('title', 'description')
    def sanitize_html(cls, v):
        # Remove any HTML tags
        return bleach.clean(v, tags=[], strip=True)
    
    @validator('title')
    def no_sql_injection(cls, v):
        # Check for common SQL injection patterns
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION', '--', '/*', '*/']
        for keyword in sql_keywords:
            if keyword.lower() in v.lower():
                raise ValueError(f"Invalid content: {keyword}")
        return v

class UserRegistration(BaseModel):
    email: EmailStr
    password: constr(min_length=12, regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]')
    name: constr(min_length=1, max_length=100)
    
    @validator('password')
    def validate_password_strength(cls, v):
        # Check against common passwords
        common_passwords = ['password123', 'admin123', 'qwerty123']
        if v.lower() in [p.lower() for p in common_passwords]:
            raise ValueError("Password is too common")
        return v
```

### Rate Limiting
```python
# API rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per hour", "100 per minute"]
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Different limits for different endpoints
@app.get("/api/v1/bills")
@limiter.limit("200 per minute")
async def list_bills():
    return await get_bills()

@app.post("/api/v1/auth/login")
@limiter.limit("5 per minute")
async def login(credentials: LoginCredentials):
    return await authenticate_user(credentials)

@app.post("/api/v1/export/bulk")
@limiter.limit("10 per hour")
async def bulk_export():
    return await generate_bulk_export()
```

### CORS Configuration
```python
# CORS security settings
from fastapi.middleware.cors import CORSMiddleware

ALLOWED_ORIGINS = [
    "https://openpolicy.ca",
    "https://www.openpolicy.ca",
    "https://app.openpolicy.ca",
]

if os.getenv("ENVIRONMENT") == "development":
    ALLOWED_ORIGINS.extend([
        "http://localhost:3000",
        "http://localhost:8080",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["X-Total-Count", "X-Page-Count"],
    max_age=3600,
)
```

### SQL Injection Prevention
```python
# Safe database queries with SQLAlchemy
from sqlalchemy import text
from sqlalchemy.sql import select

# UNSAFE - Never do this!
# query = f"SELECT * FROM users WHERE email = '{user_input}'"

# SAFE - Using parameterized queries
async def get_user_by_email(email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# SAFE - Using text with bound parameters
async def search_bills(search_term: str, limit: int = 10):
    query = text("""
        SELECT * FROM bills 
        WHERE to_tsvector('english', title || ' ' || description) 
        @@ plainto_tsquery('english', :search_term)
        LIMIT :limit
    """)
    result = await db.execute(
        query,
        {"search_term": search_term, "limit": limit}
    )
    return result.fetchall()
```

---

## Vulnerability Management

### Dependency Scanning
```yaml
# GitHub Actions security scanning
name: Security Scan
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
      
      - name: Python Safety check
        run: |
          pip install safety
          safety check --json
      
      - name: npm audit
        run: |
          cd services/web-ui
          npm audit --production
      
      - name: OWASP Dependency Check
        uses: dependency-check/Dependency-Check_Action@main
        with:
          project: 'OpenPolicy'
          path: '.'
          format: 'HTML'
```

### Security Headers Testing
```python
# Security headers validation
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_security_headers():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        
        # Required security headers
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert response.headers.get("X-XSS-Protection") == "1; mode=block"
        assert "max-age=" in response.headers.get("Strict-Transport-Security", "")
        
        # CSP header
        csp = response.headers.get("Content-Security-Policy")
        assert "default-src" in csp
        assert "script-src" in csp
        
        # No sensitive headers
        assert "Server" not in response.headers
        assert "X-Powered-By" not in response.headers
```

### Penetration Testing Schedule
```markdown
## Quarterly Security Assessments

### Q1 - External Penetration Test
- Scope: Public-facing APIs and web applications
- Duration: 2 weeks
- Provider: Third-party security firm
- Focus: OWASP Top 10, authentication bypass, injection attacks

### Q2 - Internal Security Review
- Scope: Internal APIs, admin interfaces
- Duration: 1 week
- Provider: Internal security team
- Focus: Privilege escalation, lateral movement

### Q3 - Social Engineering Test
- Scope: Email phishing, phone-based attacks
- Duration: 1 week
- Provider: Third-party security firm
- Focus: Employee security awareness

### Q4 - Full Security Audit
- Scope: Complete infrastructure and application
- Duration: 3 weeks
- Provider: Third-party security firm
- Focus: Comprehensive security assessment
```

---

## Incident Response

### Security Incident Response Plan
```python
# Incident detection and response
class SecurityIncidentHandler:
    def __init__(self):
        self.severity_levels = {
            'CRITICAL': 1,  # Data breach, system compromise
            'HIGH': 2,      # Attempted breach, vulnerability exploit
            'MEDIUM': 3,    # Suspicious activity, policy violation
            'LOW': 4        # Minor security event
        }
    
    async def log_security_event(
        self,
        event_type: str,
        severity: str,
        details: dict,
        user_id: str = None,
        ip_address: str = None
    ):
        incident = SecurityIncident(
            event_type=event_type,
            severity=severity,
            details=json.dumps(details),
            user_id=user_id,
            ip_address=ip_address,
            timestamp=datetime.utcnow()
        )
        await db.save(incident)
        
        # Alert based on severity
        if self.severity_levels.get(severity, 4) <= 2:
            await self.send_immediate_alert(incident)
        
        # Block IP if necessary
        if severity == 'CRITICAL' and ip_address:
            await self.block_ip(ip_address)
    
    async def send_immediate_alert(self, incident: SecurityIncident):
        # Send to security team
        await send_email(
            to=SECURITY_TEAM_EMAIL,
            subject=f"[{incident.severity}] Security Incident: {incident.event_type}",
            body=self.format_incident_report(incident)
        )
        
        # Send to PagerDuty for critical incidents
        if incident.severity == 'CRITICAL':
            await pagerduty.trigger_incident(
                title=f"Security Incident: {incident.event_type}",
                details=incident.details
            )
    
    async def block_ip(self, ip_address: str):
        # Add to Redis blacklist
        await redis.sadd("blocked_ips", ip_address)
        
        # Add to WAF rules
        await cloudflare.add_ip_block(ip_address)
```

### Incident Response Procedures
```markdown
## Security Incident Response Procedures

### 1. Detection (0-5 minutes)
- Automated alert received
- Verify incident authenticity
- Assess initial severity
- Start incident timer

### 2. Containment (5-30 minutes)
- Isolate affected systems
- Block malicious IPs/users
- Preserve evidence
- Stop active attacks

### 3. Investigation (30 minutes - 4 hours)
- Analyze logs and traces
- Identify attack vector
- Determine data exposure
- Document timeline

### 4. Eradication (1-8 hours)
- Remove malicious code
- Patch vulnerabilities
- Reset compromised credentials
- Update security rules

### 5. Recovery (2-24 hours)
- Restore from clean backups
- Rebuild affected systems
- Verify system integrity
- Resume normal operations

### 6. Post-Incident (1-7 days)
- Complete incident report
- Notify affected users (if required)
- Update security procedures
- Implement preventive measures
```

---

## Compliance Requirements

### Regulatory Compliance Matrix
| Regulation | Scope | Requirements | Status |
|------------|-------|--------------|---------|
| PIPEDA | Canada - Personal Information | Consent, access rights, security safeguards | ✅ Compliant |
| Provincial Privacy Acts | BC, Alberta, Quebec | Similar to PIPEDA with variations | ✅ Compliant |
| CASL | Canada - Anti-Spam | Email consent, unsubscribe | ✅ Compliant |
| WCAG 2.1 AA | Accessibility | Web accessibility standards | ✅ Compliant |
| PCI DSS | Payment Processing | Card data security | N/A - No payments |

### Audit Logging
```python
# Comprehensive audit logging
class AuditLogger:
    def __init__(self):
        self.logger = structlog.get_logger("audit")
    
    async def log_access(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str,
        action: str,
        result: str,
        ip_address: str
    ):
        await self.logger.info(
            "resource_access",
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            result=result,
            ip_address=ip_address,
            timestamp=datetime.utcnow().isoformat()
        )
    
    async def log_data_export(
        self,
        user_id: str,
        export_type: str,
        record_count: int,
        filters: dict
    ):
        await self.logger.info(
            "data_export",
            user_id=user_id,
            export_type=export_type,
            record_count=record_count,
            filters=filters,
            timestamp=datetime.utcnow().isoformat()
        )
    
    async def log_security_event(
        self,
        event_type: str,
        severity: str,
        user_id: str = None,
        details: dict = None
    ):
        await self.logger.warning(
            "security_event",
            event_type=event_type,
            severity=severity,
            user_id=user_id,
            details=details,
            timestamp=datetime.utcnow().isoformat()
        )
```

---

## Security Monitoring

### Real-time Threat Detection
```python
# Anomaly detection system
class ThreatDetector:
    def __init__(self):
        self.redis = redis.Redis()
        self.thresholds = {
            'failed_logins': 5,
            'api_requests': 1000,
            'data_exports': 10,
            'password_resets': 3
        }
    
    async def check_failed_logins(self, user_id: str, ip_address: str):
        key = f"failed_logins:{user_id}:{ip_address}"
        count = await self.redis.incr(key)
        await self.redis.expire(key, 3600)  # 1 hour window
        
        if count >= self.thresholds['failed_logins']:
            await self.trigger_alert(
                'excessive_failed_logins',
                {'user_id': user_id, 'ip_address': ip_address, 'count': count}
            )
            await self.block_account_temporarily(user_id)
    
    async def check_api_rate(self, user_id: str):
        key = f"api_requests:{user_id}"
        count = await self.redis.incr(key)
        await self.redis.expire(key, 3600)
        
        if count >= self.thresholds['api_requests']:
            await self.trigger_alert(
                'excessive_api_requests',
                {'user_id': user_id, 'count': count}
            )
    
    async def check_data_export_abuse(self, user_id: str):
        key = f"data_exports:{user_id}"
        count = await self.redis.incr(key)
        await self.redis.expire(key, 86400)  # 24 hour window
        
        if count >= self.thresholds['data_exports']:
            await self.trigger_alert(
                'excessive_data_exports',
                {'user_id': user_id, 'count': count}
            )
            await self.flag_account_for_review(user_id)
```

### Security Metrics Dashboard
```python
# Prometheus metrics for security monitoring
from prometheus_client import Counter, Histogram, Gauge

# Security metrics
failed_login_attempts = Counter(
    'security_failed_login_attempts_total',
    'Total failed login attempts',
    ['user_id', 'ip_address']
)

security_incidents = Counter(
    'security_incidents_total',
    'Total security incidents',
    ['severity', 'type']
)

blocked_requests = Counter(
    'security_blocked_requests_total',
    'Total blocked requests',
    ['reason', 'ip_address']
)

active_sessions = Gauge(
    'security_active_sessions',
    'Number of active user sessions'
)

password_strength_score = Histogram(
    'security_password_strength_score',
    'Password strength scores',
    buckets=[0, 20, 40, 60, 80, 100]
)
```

---

## Security Best Practices

### Development Security Guidelines
```python
# Security checklist for developers
SECURITY_CHECKLIST = """
## Pre-Commit Checklist
- [ ] No hardcoded secrets or credentials
- [ ] Input validation on all user inputs
- [ ] Output encoding for all dynamic content
- [ ] Parameterized queries for all database operations
- [ ] Authentication checks on all protected endpoints
- [ ] Authorization checks for resource access
- [ ] Rate limiting on resource-intensive operations
- [ ] Logging does not contain sensitive data
- [ ] Error messages do not leak system information
- [ ] Dependencies are up to date and scanned

## Code Review Security Points
- [ ] OWASP Top 10 vulnerabilities checked
- [ ] Business logic flaws considered
- [ ] Race conditions handled
- [ ] Session management secure
- [ ] File upload restrictions in place
- [ ] XML/JSON parsing limits set
- [ ] Cryptography implemented correctly
- [ ] Secrets management follows standards
- [ ] Third-party integrations validated
- [ ] Security headers configured
"""

# Pre-commit hook for security checks
def security_pre_commit_hook():
    # Check for hardcoded secrets
    secrets_scan = subprocess.run(
        ["git", "secrets", "--scan"],
        capture_output=True
    )
    if secrets_scan.returncode != 0:
        print("❌ Hardcoded secrets detected!")
        return False
    
    # Check for common vulnerabilities
    bandit_scan = subprocess.run(
        ["bandit", "-r", ".", "-f", "json"],
        capture_output=True
    )
    issues = json.loads(bandit_scan.stdout)
    if issues["results"]:
        print("❌ Security issues detected:")
        for issue in issues["results"]:
            print(f"  - {issue['issue_text']} in {issue['filename']}")
        return False
    
    return True
```

### Secure Configuration Management
```python
# Environment variable validation
from pydantic import BaseSettings, validator

class SecuritySettings(BaseSettings):
    # Required security settings
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    FIELD_ENCRYPTION_KEY: str
    DATABASE_ENCRYPTION_KEY: str
    
    # OAuth settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    
    # Security features
    ENABLE_RATE_LIMITING: bool = True
    ENABLE_AUDIT_LOGGING: bool = True
    ENABLE_THREAT_DETECTION: bool = True
    
    # Security thresholds
    MAX_LOGIN_ATTEMPTS: int = 5
    SESSION_TIMEOUT_MINUTES: int = 30
    PASSWORD_MIN_LENGTH: int = 12
    
    @validator('SECRET_KEY', 'JWT_SECRET_KEY', 'FIELD_ENCRYPTION_KEY')
    def validate_key_strength(cls, v):
        if len(v) < 32:
            raise ValueError("Security keys must be at least 32 characters")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Initialize settings
security_settings = SecuritySettings()
```

### Security Training Requirements
```markdown
## Mandatory Security Training

### For All Developers
1. **OWASP Top 10** (Annual)
   - Common vulnerabilities
   - Prevention techniques
   - Hands-on exercises

2. **Secure Coding Practices** (Bi-annual)
   - Language-specific security
   - Framework security features
   - Code review techniques

3. **Privacy and Compliance** (Annual)
   - PIPEDA requirements
   - Data handling procedures
   - Incident response

### For Security Champions
1. **Advanced Application Security** (Annual)
   - Threat modeling
   - Security architecture
   - Penetration testing basics

2. **Incident Response Training** (Bi-annual)
   - Incident handling procedures
   - Forensics basics
   - Communication protocols

### For All Staff
1. **Security Awareness** (Quarterly)
   - Phishing recognition
   - Password security
   - Social engineering
   - Physical security
```

---

## Appendix: Security Contacts

### Internal Contacts
| Role | Name | Email | Phone |
|------|------|-------|-------|
| CISO | Security Lead | security@openpolicy.ca | +1-555-0100 |
| Security Engineer | John Doe | john.doe@openpolicy.ca | +1-555-0101 |
| Privacy Officer | Jane Smith | privacy@openpolicy.ca | +1-555-0102 |

### External Contacts
| Service | Purpose | Contact |
|---------|---------|---------|
| Bug Bounty Program | Vulnerability reports | security@openpolicy.ca |
| Security Firm | Penetration testing | vendor@securityfirm.com |
| Legal Counsel | Privacy/security legal | legal@lawfirm.com |

### Emergency Procedures
```bash
# In case of active security incident
1. Execute: ./scripts/emergency-security-lockdown.sh
2. Contact: Security Lead immediately
3. Document: All actions taken
4. Preserve: Evidence and logs
5. Communicate: Via secure channels only
```