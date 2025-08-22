# Testing Guide for API Gateway

This document provides comprehensive guidance on testing the API Gateway service, including how to run tests, write new tests, and understand the testing architecture.

## Table of Contents

- [Overview](#overview)
- [Testing Architecture](#testing-architecture)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [Test Fixtures](#test-fixtures)
- [Test Utilities](#test-utilities)
- [Coverage and Reporting](#coverage-and-reporting)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The API Gateway test suite is designed to provide comprehensive coverage of all functionality, including:

- **Unit Tests**: Test individual functions and methods in isolation
- **Integration Tests**: Test API endpoints and database interactions
- **WebSocket Tests**: Test real-time communication features
- **Authentication Tests**: Test security and authorization
- **Performance Tests**: Test response times and scalability

## Testing Architecture

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Global test configuration
├── test_config.py           # Test configuration and utilities
├── fixtures/                # Test fixtures and mock data
│   ├── __init__.py
│   ├── database.py          # Database test fixtures
│   ├── test_database.py     # Test database setup
│   └── test_utilities.py    # Test utility functions
├── test_websocket.py        # WebSocket tests
├── test_comprehensive_api.py # Comprehensive API tests
└── run_tests.py             # Test runner script
```

### Key Components

1. **Test Configuration** (`test_config.py`): Centralized test settings and data factories
2. **Database Fixtures** (`fixtures/database.py`): Mock database sessions and test data
3. **Test Database** (`fixtures/test_database.py`): Real test database setup for integration tests
4. **Test Utilities** (`fixtures/test_utilities.py`): Common test helpers and assertions
5. **Test Runner** (`run_tests.py`): Script for running tests with various options

## Running Tests

### Quick Start

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/test_websocket.py

# Run tests with specific markers
python -m pytest -m "api and not slow"
```

### Using the Test Runner Script

```bash
# Run all tests
python run_tests.py --all

# Run unit tests with coverage
python run_tests.py --unit --coverage

# Run integration tests verbosely
python run_tests.py --integration --verbose

# Run tests with specific markers
python run_tests.py --markers api websocket

# Run code quality checks
python run_tests.py --quality

# Run specific test file
python run_tests.py --file tests/test_bills.py
```

### Test Markers

The test suite uses pytest markers to categorize tests:

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.api`: API endpoint tests
- `@pytest.mark.websocket`: WebSocket tests
- `@pytest.mark.database`: Database tests
- `@pytest.mark.auth`: Authentication tests
- `@pytest.mark.slow`: Slow-running tests
- `@pytest.mark.fast`: Fast-running tests

### Environment Variables

Set these environment variables for testing:

```bash
export TESTING=true
export TEST_DATABASE_URL="sqlite:///./test.db"
export TEST_REDIS_HOST="localhost"
export TEST_REDIS_PORT=6379
export TEST_REDIS_DB=1
```

## Writing Tests

### Test File Structure

```python
"""
Tests for bills API endpoints.

This module tests the bills-related API functionality including
CRUD operations, search, and filtering.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock

from app.models.openparliament import Bill
from tests.fixtures.database import mock_bill
from tests.fixtures.test_utilities import test_assertions


class TestBillsAPI:
    """Test bills API endpoints."""
    
    def test_get_bills_list(self, test_client: TestClient, mock_db):
        """Test getting list of bills."""
        # Arrange
        mock_bills = [mock_bill(id=1), mock_bill(id=2)]
        mock_db.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_bills
        mock_db.query.return_value.filter.return_value.count.return_value = 2
        
        # Act
        response = test_client.get("/api/v1/bills/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        test_assertions.assert_pagination_structure(data)
        assert len(data["items"]) == 2
    
    def test_get_bill_detail(self, test_client: TestClient, mock_db):
        """Test getting bill details."""
        # Arrange
        bill = mock_bill(id=1)
        mock_db.query.return_value.filter.return_value.first.return_value = bill
        
        # Act
        response = test_client.get("/api/v1/bills/1")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        test_assertions.assert_bill_structure(data)
        assert data["id"] == 1
    
    def test_get_bill_not_found(self, test_client: TestClient, mock_db):
        """Test getting non-existent bill."""
        # Arrange
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act
        response = test_client.get("/api/v1/bills/999")
        
        # Assert
        assert response.status_code == 404
        test_assertions.assert_error_response(response.json(), 404)
```

### Test Naming Conventions

- **Test classes**: `Test{Feature}API` (e.g., `TestBillsAPI`)
- **Test methods**: `test_{action}_{scenario}` (e.g., `test_get_bills_list`)
- **Test files**: `test_{feature}.py` (e.g., `test_bills.py`)

### Test Structure (AAA Pattern)

1. **Arrange**: Set up test data and mocks
2. **Act**: Execute the function/endpoint being tested
3. **Assert**: Verify the expected outcomes

### Using Test Fixtures

```python
def test_with_fixtures(self, test_client, mock_db, test_bill_data):
    """Test using fixtures."""
    # Use test_client for making HTTP requests
    # Use mock_db for database mocking
    # Use test_bill_data for test data
    
    response = test_client.get("/api/v1/bills/")
    assert response.status_code == 200
```

## Test Fixtures

### Database Fixtures

```python
@pytest.fixture
def mock_db_session():
    """Get a mock database session."""
    return MockDatabaseSession()

@pytest.fixture
def test_bills(test_database):
    """Get test bills data."""
    return test_database.get_test_data("bills")
```

### Mock Fixtures

```python
@pytest.fixture
def mock_redis():
    """Get a mock Redis client."""
    return test_mock_helpers.create_mock_redis_client()

@pytest.fixture
def mock_websocket():
    """Get a mock WebSocket connection."""
    return test_mock_helpers.create_mock_websocket()
```

### Test Data Fixtures

```python
@pytest.fixture
def test_bill_data():
    """Get test bill data."""
    return test_data_factory.create_test_bill()

@pytest.fixture
def test_committee_data():
    """Get test committee data."""
    return test_data_factory.create_test_committee()
```

## Test Utilities

### Assertions

```python
from tests.fixtures.test_utilities import test_assertions

# Assert response structure
test_assertions.assert_response_structure(response_data, ["id", "name", "status"])

# Assert pagination structure
test_assertions.assert_pagination_structure(response_data)

# Assert error response
test_assertions.assert_error_response(response_data, 404)

# Assert specific data structures
test_assertions.assert_bill_structure(bill_data)
test_assertions.assert_committee_structure(committee_data)
```

### Data Helpers

```python
from tests.fixtures.test_utilities import test_data_helpers

# Create mock objects
mock_bill = test_data_helpers.create_mock_bill(id=1, status="ACTIVE")
mock_committee = test_data_helpers.create_mock_committee(id=1, type="standing")
```

### Mock Helpers

```python
from tests.fixtures.test_utilities import test_mock_helpers

# Create mock database session
mock_db = test_mock_helpers.create_mock_db_session()

# Create mock Redis client
mock_redis = test_mock_helpers.create_mock_redis_client()

# Create mock WebSocket
mock_ws = test_mock_helpers.create_mock_websocket()
```

### Response Helpers

```python
from tests.fixtures.test_utilities import test_response_helpers

# Make HTTP requests
response_data = test_response_helpers.make_request(
    client, "GET", "/api/v1/bills/"
)

# Assert status codes
test_response_helpers.assert_status_code(response, 200)

# Assert response content
test_response_helpers.assert_response_contains(
    response_data, {"total": 10, "page": 1}
)
```

## Coverage and Reporting

### Running Coverage

```bash
# Run tests with coverage
python -m pytest --cov=app --cov-report=term-missing

# Generate HTML coverage report
python -m pytest --cov=app --cov-report=html

# Generate XML coverage report for CI
python -m pytest --cov=app --cov-report=xml
```

### Coverage Configuration

Coverage is configured in `pytest.ini`:

```ini
[tool:pytest]
addopts = 
    --cov=app
    --cov-report=term-missing
    --cov-report=html
    --cov-report=xml
    --cov-fail-under=85
```

### Coverage Targets

- **Overall coverage**: 85% minimum
- **Critical modules**: 95% minimum
- **New code**: 90% minimum

## Best Practices

### Test Organization

1. **Group related tests** in test classes
2. **Use descriptive test names** that explain the scenario
3. **Keep tests independent** - no shared state between tests
4. **Use appropriate test markers** for categorization

### Mocking Strategy

1. **Mock external dependencies** (databases, APIs, services)
2. **Use realistic mock data** that matches production schemas
3. **Test edge cases** and error conditions
4. **Verify mock interactions** when relevant

### Database Testing

1. **Use in-memory SQLite** for fast unit tests
2. **Use real database** for integration tests
3. **Clean up test data** after each test
4. **Test database constraints** and relationships

### API Testing

1. **Test all HTTP methods** (GET, POST, PUT, DELETE)
2. **Test response status codes** and error handling
3. **Test request validation** and error messages
4. **Test authentication** and authorization

### WebSocket Testing

1. **Test connection lifecycle** (connect, disconnect, reconnect)
2. **Test message handling** and broadcasting
3. **Test authentication** and room management
4. **Test error handling** and edge cases

## Troubleshooting

### Common Issues

#### Import Errors

```bash
# Ensure you're in the correct directory
cd services/api-gateway

# Install test dependencies
pip install -r requirements-test.txt

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Database Connection Issues

```bash
# Check database URL
echo $TEST_DATABASE_URL

# Use in-memory database for testing
export TEST_DATABASE_URL="sqlite:///:memory:"
```

#### Redis Connection Issues

```bash
# Check Redis connection
redis-cli ping

# Use mock Redis for testing
export TEST_REDIS_HOST="localhost"
export TEST_REDIS_PORT=6379
```

#### Test Failures

1. **Check test logs** for detailed error messages
2. **Verify mock setup** and return values
3. **Check test data** and fixtures
4. **Ensure clean test environment**

### Debugging Tests

```python
# Add debug prints
print(f"Response: {response.json()}")

# Use pytest -s for output
python -m pytest -s tests/test_bills.py

# Use pytest --pdb for debugging
python -m pytest --pdb tests/test_bills.py

# Use ipdb for interactive debugging
import ipdb; ipdb.set_trace()
```

### Performance Issues

1. **Use appropriate test markers** (`@pytest.mark.slow`)
2. **Run tests in parallel** with `pytest-xdist`
3. **Profile slow tests** to identify bottlenecks
4. **Use test isolation** to prevent interference

## Contributing

When adding new tests:

1. **Follow the existing patterns** and conventions
2. **Add appropriate test markers** for categorization
3. **Update this documentation** if adding new features
4. **Ensure test coverage** meets minimum requirements
5. **Run the full test suite** before submitting changes

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
- [WebSocket Testing](https://websockets.readthedocs.io/en/stable/intro.html#testing)
