# Comprehensive Testing Strategies

## Executive Summary
This document outlines the testing strategy for the OpenPolicy V2 platform, covering unit, integration, end-to-end, performance, security, and accessibility testing.

## Testing Philosophy
- **Test Pyramid**: 70% unit, 20% integration, 10% E2E
- **Shift Left**: Test early in development cycle
- **Continuous Testing**: Automated tests in CI/CD pipeline
- **Risk-Based**: Focus on critical user journeys
- **Data-Driven**: Use real-world data scenarios

## Test Coverage Goals
- **Overall Coverage**: ≥ 80%
- **Critical Paths**: ≥ 95%
- **API Endpoints**: 100%
- **UI Components**: ≥ 85%
- **Data Pipelines**: ≥ 90%

## Testing Frameworks & Tools

### Backend (Python)
- **Unit Testing**: pytest 7.x
- **Coverage**: pytest-cov
- **Mocking**: pytest-mock, responses
- **API Testing**: pytest + httpx
- **Database**: pytest-postgresql

### Frontend (JavaScript/TypeScript)
- **Unit Testing**: Jest 29.x
- **Component Testing**: React Testing Library
- **E2E Testing**: Playwright
- **Visual Regression**: Percy
- **Coverage**: Istanbul/nyc

### Infrastructure
- **Load Testing**: k6
- **Security**: OWASP ZAP
- **Accessibility**: axe-core
- **Contract Testing**: Pact
- **Monitoring**: Datadog Synthetics

## Test Types & Strategies

### 1. Unit Tests

#### Purpose
Test individual functions, methods, and components in isolation.

#### Scope
- Business logic functions
- Data transformations
- Utility functions
- React components
- API route handlers

#### Example Test Plan
```python
# API Unit Test Example
def test_bill_creation():
    bill = Bill(
        title="Test Act",
        status="first_reading",
        introduction_date=date.today()
    )
    assert bill.is_active() == True
    assert bill.days_since_introduction() >= 0
```

```javascript
// React Component Test Example
test('BillCard displays bill information', () => {
  render(<BillCard bill={mockBill} />);
  expect(screen.getByText('Test Act')).toBeInTheDocument();
  expect(screen.getByText('First Reading')).toBeInTheDocument();
});
```

### 2. Integration Tests

#### Purpose
Test interactions between multiple components/services.

#### Scope
- API endpoint integration
- Database operations
- External service calls
- Authentication flows
- Data pipeline stages

#### Example Test Plan
```python
# API Integration Test
async def test_create_and_retrieve_bill():
    async with AsyncClient(app=app) as client:
        # Create bill
        response = await client.post("/api/v1/bills", json={
            "title": "Integration Test Act",
            "status": "first_reading"
        })
        assert response.status_code == 201
        bill_id = response.json()["id"]
        
        # Retrieve bill
        response = await client.get(f"/api/v1/bills/{bill_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Integration Test Act"
```

### 3. End-to-End Tests

#### Purpose
Test complete user workflows from UI to database.

#### Critical User Journeys
1. **Search for MP by Postal Code**
   - Enter postal code
   - View MP profile
   - Contact MP

2. **Track Bill Progress**
   - Search for bill
   - View bill details
   - See voting history
   - Subscribe to updates

3. **Browse Debates**
   - Select date
   - Read transcript
   - Search speeches
   - View AI summary

#### E2E Test Example (Playwright)
```javascript
test('User can find their MP by postal code', async ({ page }) => {
  await page.goto('/');
  await page.fill('[data-testid="search-input"]', 'K1A 0A6');
  await page.click('[data-testid="search-submit"]');
  
  await expect(page).toHaveURL(/\/search\?postcode=K1A\+0A6/);
  await expect(page.locator('[data-testid="mp-result"]')).toBeVisible();
  await expect(page.locator('[data-testid="mp-name"]')).toContainText('MP Name');
});
```

### 4. Performance Tests

#### Targets
- **Page Load**: < 3 seconds (P95)
- **API Response**: < 500ms (P95)
- **Search Results**: < 1 second
- **Concurrent Users**: 10,000+
- **Database Queries**: < 100ms

#### k6 Load Test Example
```javascript
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 1000 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
  },
};

export default function() {
  let response = http.get('https://api.openpolicy.ca/v1/bills');
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
}
```

### 5. Security Tests

#### OWASP Top 10 Coverage
- A01: Broken Access Control
- A02: Cryptographic Failures
- A03: Injection
- A04: Insecure Design
- A05: Security Misconfiguration
- A06: Vulnerable Components
- A07: Authentication Failures
- A08: Data Integrity Failures
- A09: Logging Failures
- A10: SSRF

#### Security Test Plan
```yaml
# OWASP ZAP Configuration
contexts:
  - name: OpenPolicy API
    urls:
      - https://api.openpolicy.ca
    authentication:
      method: jwt
      parameters:
        loginUrl: https://api.openpolicy.ca/auth/login
    tests:
      - sql_injection
      - xss
      - broken_authentication
      - sensitive_data_exposure
      - xxe
      - broken_access_control
      - security_misconfiguration
```

### 6. Accessibility Tests

#### WCAG 2.1 AA Compliance
- **Perceivable**: Alt text, color contrast
- **Operable**: Keyboard navigation, focus indicators
- **Understandable**: Clear labels, error messages
- **Robust**: Semantic HTML, ARIA

#### Automated Testing
```javascript
// axe-core integration
test('Homepage is accessible', async () => {
  const { container } = render(<HomePage />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### 7. Contract Tests

#### API Contract Testing
```javascript
// Pact consumer test
describe('Bills API Contract', () => {
  it('returns bill details', async () => {
    await provider.addInteraction({
      state: 'a bill exists',
      uponReceiving: 'a request for bill details',
      withRequest: {
        method: 'GET',
        path: '/api/v1/bills/123',
      },
      willRespondWith: {
        status: 200,
        body: {
          id: '123',
          title: like('Sample Act'),
          status: term({
            matcher: 'first_reading|second_reading|third_reading|royal_assent',
            generate: 'first_reading'
          }),
        },
      },
    });
  });
});
```

### 8. Data Quality Tests

#### ETL Pipeline Validation
```python
def test_scraper_data_quality():
    # Run scraper
    data = scraper.extract_members()
    
    # Validate required fields
    for member in data:
        assert member.get('name') is not None
        assert member.get('riding') is not None
        assert member.get('party') is not None
        
    # Validate data formats
    assert all(re.match(r'^[A-Z0-9]{3}$', m.get('postal_code', '')) 
              for m in data if m.get('postal_code'))
    
    # Check for duplicates
    names = [m['name'] for m in data]
    assert len(names) == len(set(names))
```

## Test Data Management

### Test Data Strategy
1. **Synthetic Data**: Generated test data for unit tests
2. **Anonymized Production Data**: For integration/E2E tests
3. **Fixtures**: Predefined test scenarios
4. **Seed Data**: Consistent baseline for testing

### Test Database Management
```yaml
# docker-compose.test.yml
services:
  test-db:
    image: postgres:15
    environment:
      POSTGRES_DB: openpolicy_test
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    volumes:
      - ./test/fixtures:/docker-entrypoint-initdb.d
```

## CI/CD Integration

### GitHub Actions Workflow
```yaml
name: Test Suite
on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Python Tests
        run: |
          pip install -r requirements-test.txt
          pytest --cov=app --cov-report=xml
      
      - name: Run JavaScript Tests
        run: |
          npm ci
          npm run test:unit -- --coverage

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        options: --health-cmd pg_isready
    steps:
      - name: Run Integration Tests
        run: |
          pytest tests/integration/
          npm run test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run E2E Tests
        run: |
          npx playwright install
          npm run test:e2e

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - name: OWASP ZAP Scan
        uses: zaproxy/action-full-scan@v0.4.0
        with:
          target: 'https://staging.openpolicy.ca'
```

## Test Reporting

### Metrics to Track
- **Test Coverage**: Line, branch, function coverage
- **Test Execution Time**: Track slow tests
- **Flaky Tests**: Monitor intermittent failures
- **Defect Density**: Bugs per feature/module
- **Test Automation ROI**: Time saved vs invested

### Dashboard Example
```
┌─────────────────────────────────────────┐
│           Test Coverage Trends          │
├─────────────────────────────────────────┤
│ Component     │ Current │ Target │ Δ    │
├───────────────┼─────────┼────────┼──────┤
│ API Gateway   │ 87%     │ 85%    │ +2%  │
│ Web UI        │ 73%     │ 85%    │ -12% │
│ ETL Pipeline  │ 91%     │ 90%    │ +1%  │
│ Scrapers      │ 68%     │ 80%    │ -12% │
└─────────────────────────────────────────┘
```

## Test Environments

### Environment Strategy
1. **Local**: Developer machines (Docker)
2. **CI**: Automated test runs (GitHub Actions)
3. **Staging**: Pre-production testing
4. **Production**: Smoke tests only

### Environment Configuration
```python
# config/test.py
class TestConfig:
    TESTING = True
    DATABASE_URL = "postgresql://test:test@localhost/openpolicy_test"
    REDIS_URL = "redis://localhost:6379/1"
    ELASTICSEARCH_URL = "http://localhost:9200"
    EXTERNAL_API_MOCK = True
    RATE_LIMIT_ENABLED = False
```

## Test Maintenance

### Best Practices
1. **DRY**: Reusable test utilities and fixtures
2. **Isolation**: Tests should not depend on each other
3. **Deterministic**: Same input = same output
4. **Fast**: Optimize slow tests
5. **Clear**: Descriptive test names
6. **Maintained**: Regular test review and updates

### Test Review Checklist
- [ ] New features have corresponding tests
- [ ] Tests follow naming conventions
- [ ] No hardcoded test data
- [ ] Proper test cleanup
- [ ] Appropriate use of mocks
- [ ] Coverage targets met
- [ ] No flaky tests introduced

## Risk-Based Testing

### Critical Features (P0)
1. User Authentication
2. Search Functionality
3. Bill/Vote Display
4. MP Contact System
5. Data Integrity

### High Priority (P1)
1. Email Notifications
2. API Rate Limiting
3. Mobile Responsiveness
4. Accessibility Compliance
5. Performance SLAs

### Test Prioritization Matrix
```
         Impact
    High │ P0 │ P1 │
         ├────┼────┤
    Low  │ P2 │ P3 │
         └────┴────┘
         Low  High
         Likelihood
```

## Continuous Improvement

### Metrics for Success
1. **Defect Escape Rate**: < 5%
2. **Test Automation Coverage**: > 80%
3. **Mean Time to Detection**: < 1 hour
4. **Test Execution Time**: < 30 minutes
5. **False Positive Rate**: < 2%

### Quarterly Review Process
1. Analyze test metrics
2. Review flaky tests
3. Update test strategies
4. Train team on new tools
5. Optimize slow tests

## Appendix: Test Commands

### Running Tests Locally
```bash
# Backend unit tests
pytest tests/unit/ -v

# Backend integration tests
pytest tests/integration/ -v

# Frontend unit tests
npm run test:unit

# Frontend E2E tests
npm run test:e2e

# All tests with coverage
./scripts/run-all-tests.sh --coverage

# Specific feature tests
pytest -k "test_bill" -v
npm run test -- --testNamePattern="Bill"
```

### Debugging Tests
```bash
# Run with debugging
pytest --pdb tests/unit/test_bills.py

# Verbose output
pytest -vvs tests/

# Run specific test
pytest tests/unit/test_bills.py::test_bill_creation

# JavaScript debugging
npm run test:debug
```