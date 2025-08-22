# Comprehensive Testing Strategies - All Features
Generated: 2025-01-19 | Iteration: 2/10

## 🎯 Testing Philosophy
Every feature must be tested through multiple verification layers:
1. **Unit Tests** - Component isolation
2. **Integration Tests** - Service interaction
3. **E2E Tests** - User journey
4. **Visual Tests** - UI consistency
5. **Performance Tests** - Load handling
6. **Security Tests** - Vulnerability scanning
7. **Accessibility Tests** - WCAG compliance

## 📊 Feature-by-Feature Testing Strategy

### 1. Bills System

#### Testing Matrix
| Test Type | Coverage Target | Current | Strategy |
|-----------|----------------|---------|----------|
| Unit | 95% | 20% | Test each model, schema, endpoint |
| Integration | 85% | 10% | API contract tests |
| E2E | 80% | 0% | User journey tests |
| Visual | 100% | 0% | Screenshot comparisons |

#### Detailed Test Cases

**Unit Tests**
```python
# test_bills.py
class TestBillModel:
    def test_bill_creation(self):
        """Test bill can be created with required fields"""
        bill = Bill(
            number="C-123",
            title="Test Act",
            session_id=1
        )
        assert bill.number == "C-123"
    
    def test_bill_validation(self):
        """Test bill validation rules"""
        with pytest.raises(ValidationError):
            Bill(number="")  # Empty number should fail
    
    def test_bill_status_transitions(self):
        """Test valid status transitions"""
        bill = Bill(status="first_reading")
        bill.advance_status()
        assert bill.status == "second_reading"
```

**Integration Tests**
```python
# test_bills_api.py
class TestBillsAPI:
    async def test_create_bill_endpoint(self, client):
        """Test POST /api/v1/bills"""
        response = await client.post("/api/v1/bills", json={
            "number": "C-123",
            "title": "Test Act"
        })
        assert response.status_code == 201
        assert response.json()["number"] == "C-123"
    
    async def test_bills_search(self, client):
        """Test GET /api/v1/bills/search"""
        response = await client.get("/api/v1/bills/search?q=climate")
        assert response.status_code == 200
        assert len(response.json()["results"]) > 0
```

**E2E Tests**
```typescript
// bills.e2e.spec.ts
describe('Bills User Journey', () => {
  it('should allow user to search and view bill details', async () => {
    // Navigate to bills page
    await page.goto('/bills');
    
    // Search for a bill
    await page.fill('[data-testid="bill-search"]', 'climate');
    await page.click('[data-testid="search-button"]');
    
    // Verify results appear
    await expect(page.locator('.bill-result')).toHaveCount(greaterThan(0));
    
    // Click on first result
    await page.click('.bill-result:first-child');
    
    // Verify bill details page
    await expect(page).toHaveURL(/\/bills\/\d+/);
    await expect(page.locator('h1')).toContainText('Bill');
  });
});
```

**Visual Tests**
```javascript
// bills.visual.spec.js
describe('Bills Visual Tests', () => {
  it('should match bill list page snapshot', async () => {
    await page.goto('/bills');
    await expect(page).toHaveScreenshot('bills-list.png');
  });
  
  it('should match bill detail page snapshot', async () => {
    await page.goto('/bills/123');
    await expect(page).toHaveScreenshot('bill-detail.png');
  });
});
```

**Performance Tests**
```javascript
// bills.perf.js
import { check } from 'k6';
import http from 'k6/http';

export let options = {
  stages: [
    { duration: '5m', target: 100 },
    { duration: '10m', target: 100 },
    { duration: '5m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
  },
};

export default function() {
  let response = http.get('http://localhost:8080/api/v1/bills');
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
}
```

### 2. MPs/Members System

#### Testing Strategy
```yaml
test_pyramid:
  unit:
    - Member model validation
    - Electoral district assignment
    - Party affiliation changes
    - Contact info validation
  integration:
    - Member CRUD operations
    - Search by name/riding
    - Party filtering
    - Province filtering
  e2e:
    - Find MP by postal code
    - View MP voting record
    - Contact MP workflow
  visual:
    - MP card component
    - MP detail page layout
    - Mobile responsiveness
```

#### Sample Test Implementation
```python
# test_members.py
class TestMemberSearch:
    @pytest.mark.parametrize("search_term,expected_count", [
        ("trudeau", 1),
        ("toronto", 25),
        ("liberal", 150),
    ])
    async def test_member_search_variations(self, client, search_term, expected_count):
        """Test various search scenarios"""
        response = await client.get(f"/api/v1/members/search?q={search_term}")
        assert len(response.json()["results"]) >= expected_count
```

### 3. Votes System (Currently Broken)

#### Fix Verification Tests
```python
# test_votes_fix.py
class TestVotesAPIFix:
    def test_pydantic_v2_schema(self):
        """Verify Pydantic v2 schema works"""
        from app.schemas.votes import VoteSchema
        
        vote_data = {
            "id": 1,
            "bill_id": 123,
            "result": "passed",
            "yea_count": 200,
            "nay_count": 100
        }
        
        vote = VoteSchema(**vote_data)
        assert vote.model_dump()["id"] == 1
    
    async def test_votes_endpoint_restored(self, client):
        """Verify votes endpoint is working"""
        response = await client.get("/api/v1/votes")
        assert response.status_code == 200  # Currently returns 404
```

### 4. Committees System

#### Data Completeness Tests
```python
# test_committees_data.py
class TestCommitteeData:
    def test_all_committees_loaded(self, db):
        """Verify all 26+ committees are in database"""
        committees = db.query(Committee).count()
        assert committees >= 26, f"Only {committees} committees found, expected 26+"
    
    def test_committee_members_populated(self, db):
        """Verify committee membership data"""
        for committee in db.query(Committee).all():
            assert committee.members.count() > 0, f"{committee.name} has no members"
```

### 5. Search System

#### Postal Code Integration Tests
```python
# test_search_postal.py
class TestPostalCodeSearch:
    @pytest.mark.parametrize("postal_code,expected_mp", [
        ("K1A0A6", "Parliament Hill"),
        ("M5V3A8", "Spadina-Fort York"),
        ("V6B2W2", "Vancouver Centre"),
    ])
    async def test_postal_code_lookup(self, client, postal_code, expected_mp):
        """Test MP lookup by postal code"""
        response = await client.get(f"/api/v1/search/mp?postal={postal_code}")
        assert response.status_code == 200
        assert expected_mp in response.json()["riding"]
```

### 6. User Authentication

#### Security Test Suite
```python
# test_auth_security.py
class TestAuthSecurity:
    def test_password_hashing(self):
        """Verify passwords are properly hashed"""
        from app.core.security import hash_password, verify_password
        
        password = "TestPass123!"
        hashed = hash_password(password)
        
        assert password not in hashed
        assert verify_password(password, hashed)
    
    def test_jwt_token_expiry(self):
        """Verify JWT tokens expire correctly"""
        from app.core.auth import create_access_token
        from datetime import timedelta
        
        token = create_access_token(
            data={"sub": "user@example.com"},
            expires_delta=timedelta(minutes=1)
        )
        
        # Wait and verify expiration
        time.sleep(61)
        with pytest.raises(ExpiredSignatureError):
            decode_token(token)
    
    def test_sql_injection_prevention(self, client):
        """Verify SQL injection is prevented"""
        malicious_input = "'; DROP TABLE users; --"
        response = client.post("/api/v1/auth/login", json={
            "email": malicious_input,
            "password": "test"
        })
        assert response.status_code == 422  # Validation error
```

### 7. Email Alerts (To Be Implemented)

#### Test-Driven Development Tests
```python
# test_email_alerts_tdd.py
class TestEmailAlerts:
    @pytest.mark.skip(reason="Feature not implemented")
    async def test_alert_subscription(self, client):
        """Test user can subscribe to bill alerts"""
        response = await client.post("/api/v1/alerts/subscribe", json={
            "email": "user@example.com",
            "alert_type": "bill_updates",
            "keywords": ["climate", "health"]
        })
        assert response.status_code == 201
    
    @pytest.mark.skip(reason="Feature not implemented")
    async def test_alert_delivery(self, client, mock_email):
        """Test alerts are delivered when triggered"""
        # Create alert subscription
        # Create matching bill
        # Verify email sent
        pass
```

### 8. Real-time Features

#### WebSocket Tests
```python
# test_websocket.py
class TestWebSocket:
    @pytest.mark.skip(reason="WebSocket not implemented")
    async def test_house_status_updates(self, websocket_client):
        """Test real-time House status updates"""
        async with websocket_client.connect("/ws/house-status") as websocket:
            # Send subscription
            await websocket.send_json({"action": "subscribe"})
            
            # Trigger status change
            await trigger_house_status_change("in_session")
            
            # Verify update received
            data = await websocket.receive_json()
            assert data["status"] == "in_session"
```

## 📱 UI Verification Strategies

### 1. Component Testing
```typescript
// Button.test.tsx
describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
  
  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### 2. Accessibility Testing
```javascript
// a11y.test.js
describe('Accessibility Tests', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<BillsPage />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
  
  it('supports keyboard navigation', async () => {
    render(<Navigation />);
    const firstLink = screen.getByText('Bills');
    firstLink.focus();
    fireEvent.keyDown(firstLink, { key: 'Tab' });
    expect(screen.getByText('MPs')).toHaveFocus();
  });
});
```

### 3. Cross-browser Testing
```javascript
// crossbrowser.conf.js
module.exports = {
  browsers: [
    'chrome@latest',
    'firefox@latest',
    'safari@latest',
    'edge@latest',
    'chrome@latest:Android',
    'safari@latest:iOS'
  ],
  testMatch: '**/*.crossbrowser.spec.js'
};
```

## 🎯 Test Coverage Goals

| Component | Unit | Integration | E2E | Visual | Current | Target |
|-----------|------|-------------|-----|--------|---------|---------|
| Bills | 95% | 85% | 80% | 100% | 20% | 85% |
| Members | 95% | 85% | 80% | 100% | 15% | 85% |
| Votes | 95% | 85% | 80% | 100% | 0% | 85% |
| Committees | 90% | 80% | 75% | 100% | 10% | 80% |
| Search | 90% | 85% | 85% | 100% | 25% | 85% |
| Auth | 100% | 95% | 90% | 100% | 40% | 95% |
| Debates | 90% | 80% | 75% | 100% | 5% | 80% |

## 🔧 Testing Infrastructure

### Required Tools
1. **Backend**: pytest, pytest-asyncio, pytest-cov, factory-boy
2. **Frontend**: Jest, React Testing Library, Playwright
3. **API**: Postman/Newman, Pact
4. **Performance**: k6, Locust
5. **Security**: OWASP ZAP, Snyk
6. **Visual**: Percy, Chromatic

### CI/CD Pipeline
```yaml
test_pipeline:
  - stage: unit_tests
    parallel: true
    jobs:
      - pytest backend
      - jest frontend
  - stage: integration_tests
    jobs:
      - api contract tests
      - database tests
  - stage: e2e_tests
    jobs:
      - playwright tests
  - stage: performance_tests
    jobs:
      - k6 load tests
  - stage: security_scan
    jobs:
      - owasp scan
      - dependency check
```

---
End of Iteration 2/10