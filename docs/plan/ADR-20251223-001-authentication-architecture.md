# ADR-20251223-001: Authentication Architecture Consolidation

## Status
Proposed

## Context
The OpenPolicy V2 system currently has multiple authentication implementations:

1. **API Gateway Auth** (`services/api-gateway/app/api/v1/auth.py`)
   - Most complete implementation
   - JWT-based with proper token management
   - User sessions and password reset
   - WebSocket authentication support
   - OAuth models ready but not fully implemented

2. **User Service Auth** (`services/user-service/app/api/v1/auth.py`)
   - Parallel JWT implementation
   - Mock data instead of database integration
   - Duplicate code and functionality
   - Different token structure

3. **Legacy Django Auth** (`services/web-ui/src/legacy-migration/accounts/`)
   - Existing user base
   - Different authentication mechanism
   - Email-based token login
   - Production data

This duplication creates:
- Confusion about which service to use
- Maintenance overhead
- Security risks from inconsistent implementations
- Complex migration path for legacy users

## Decision
We will consolidate all authentication into the API Gateway service as the single source of truth for authentication and authorization.

### Rationale
1. **API Gateway has the most complete implementation** with proper JWT handling, session management, and security features
2. **Central authentication** aligns with microservices best practices
3. **Single point of security** audit and monitoring
4. **Easier to maintain** one implementation vs three
5. **Natural fit** as the gateway already handles all incoming requests

## Consequences

### Positive
- Single source of truth for authentication
- Consistent security policies
- Easier to implement SSO, OAuth, 2FA
- Reduced code duplication
- Clear authentication flow
- Better security monitoring

### Negative
- User Service loses autonomy over auth
- Need to migrate existing User Service endpoints
- Legacy user migration complexity
- All services depend on API Gateway availability

## Implementation Plan

### Phase 1: Document Current State (Week 1)
1. Map all authentication endpoints across services
2. Document token formats and claims
3. Identify all auth-dependent features
4. Create comprehensive test suite

### Phase 2: API Gateway Enhancement (Week 2)
1. Complete OAuth provider integration
2. Implement 2FA support
3. Add user profile management endpoints
4. Enhance session management
5. Add auth metrics and monitoring

### Phase 3: User Service Migration (Week 3)
1. Update User Service to use API Gateway auth
2. Remove duplicate auth code
3. Update all User Service endpoints to validate tokens from API Gateway
4. Implement service-to-service authentication

### Phase 4: Legacy User Migration (Week 4)
1. Create migration script for Django users
2. Map Django user fields to new schema
3. Generate migration tokens for existing users
4. Implement backwards-compatible endpoints
5. Send migration emails to users

### Phase 5: Deprecation (Week 5-6)
1. Mark old auth endpoints as deprecated
2. Monitor usage of legacy endpoints
3. Gradually redirect traffic
4. Remove deprecated code

## Alternatives Considered

### 1. Maintain Separate Auth Services
- **Pros**: Service autonomy, no migration needed
- **Cons**: Duplicate code, inconsistent security, complex user experience
- **Rejected because**: Goes against microservices best practices

### 2. Create Dedicated Auth Microservice
- **Pros**: Clean separation of concerns, specialized service
- **Cons**: Another service to maintain, additional network hop
- **Rejected because**: API Gateway already has solid implementation

### 3. Federate Authentication
- **Pros**: Services can choose auth method
- **Cons**: Very complex, security risks, poor user experience
- **Rejected because**: Over-engineered for our needs

## Security Considerations

1. **Token Validation**: All services must validate tokens with API Gateway
2. **Service Accounts**: Internal service-to-service auth needed
3. **Token Rotation**: Implement refresh token rotation
4. **Audit Logging**: Centralized auth logging
5. **Rate Limiting**: Prevent brute force attacks
6. **CORS**: Proper CORS configuration for web clients

## Monitoring

Track these metrics:
- Authentication success/failure rates
- Token validation performance
- Legacy endpoint usage
- User migration progress
- Service-to-service auth failures

## References
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [Microservices Authentication Patterns](https://microservices.io/patterns/security/access-token.html)