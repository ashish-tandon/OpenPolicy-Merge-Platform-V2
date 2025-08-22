"""
Test configuration and utilities for API Gateway tests.

This module provides centralized test configuration, common fixtures,
and utility functions for the test suite.
"""

import pytest
from typing import Dict, Any
from unittest.mock import Mock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from tests.fixtures.test_database import TestDatabaseConfig
from tests.fixtures.test_utilities import test_assertions, test_data_helpers, test_mock_helpers, test_response_helpers


class TestConfig:
    """Centralized test configuration."""
    
    # Test database settings
    TEST_DATABASE_URL = "sqlite:///./test.db"
    TEST_DATABASE_ECHO = False
    
    # Test API settings
    TEST_API_PREFIX = "/api/v1"
    TEST_TIMEOUT = 30
    
    # Test user credentials
    TEST_USER_ID = "test_user_123"
    TEST_USERNAME = "testuser"
    TEST_EMAIL = "test@example.com"
    TEST_PASSWORD = "testpassword123"
    
    # Test JWT settings
    TEST_JWT_SECRET = "test_secret_key_for_testing_only"
    TEST_JWT_ALGORITHM = "HS256"
    TEST_JWT_EXPIRY = 3600  # 1 hour
    
    # Test WebSocket settings
    TEST_WEBSOCKET_TIMEOUT = 5
    TEST_WEBSOCKET_MAX_CONNECTIONS = 100
    
    # Test Redis settings
    TEST_REDIS_HOST = "localhost"
    TEST_REDIS_PORT = 6379
    TEST_REDIS_DB = 1  # Use different DB for testing
    
    # Test data settings
    TEST_BILL_ID = 1
    TEST_COMMITTEE_ID = 1
    TEST_MEMBER_ID = 1
    TEST_VOTE_SESSION = "45-1"
    TEST_VOTE_NUMBER = 1
    
    # Test pagination
    TEST_PAGE_SIZE = 20
    TEST_MAX_PAGE_SIZE = 100
    
    # Test rate limiting
    TEST_RATE_LIMIT_REQUESTS = 100
    TEST_RATE_LIMIT_WINDOW = 3600  # 1 hour


class TestDataFactory:
    """Factory for creating test data objects."""
    
    @staticmethod
    def create_test_bill(bill_id: int = 1) -> Dict[str, Any]:
        """Create a test bill object."""
        return {
            "id": bill_id,
            "number": f"C-{100 + bill_id}",
            "name_en": f"Test Bill {bill_id}",
            "short_title_en": f"Short Title {bill_id}",
            "status_code": "INTRODUCED",
            "introduced": "2024-01-01",
            "session_id": "45-1",
            "institution": "House",
            "sponsor_member_id": None
        }
    
    @staticmethod
    def create_test_committee(committee_id: int = 1) -> Dict[str, Any]:
        """Create a test committee object."""
        return {
            "id": committee_id,
            "name_en": f"Test Committee {committee_id}",
            "name_fr": f"Comité de test {committee_id}",
            "slug": f"test-committee-{committee_id}",
            "session_id": "45-1",
            "type": "standing"
        }
    
    @staticmethod
    def create_test_member(member_id: int = 1) -> Dict[str, Any]:
        """Create a test member object."""
        return {
            "id": member_id,
            "politician_id": member_id,
            "party_id": 1,
            "riding_id": 1,
            "session_id": "45-1",
            "start_date": "2024-01-01",
            "end_date": None
        }
    
    @staticmethod
    def create_test_vote(vote_number: int = 1) -> Dict[str, Any]:
        """Create a test vote object."""
        return {
            "session_id": "45-1",
            "vote_number": vote_number,
            "bill_id": 1,
            "result": "CARRIED",
            "yea_total": 150,
            "nay_total": 100,
            "paired_count": 5,
            "absent_count": 10,
            "vote_date": "2024-01-01"
        }
    
    @staticmethod
    def create_test_debate(debate_date: str = "2024-01-01") -> Dict[str, Any]:
        """Create a test debate object."""
        return {
            "date": debate_date,
            "debate_number": 1,
            "session_id": "45-1",
            "institution": "House",
            "topic": "Test Debate Topic"
        }
    
    @staticmethod
    def create_test_statement(statement_id: int = 1) -> Dict[str, Any]:
        """Create a test statement object."""
        return {
            "id": statement_id,
            "politician_id": 1,
            "time": "2024-01-01T10:00:00",
            "content_en": f"Test statement content {statement_id}",
            "content_fr": f"Contenu de déclaration de test {statement_id}",
            "sequence": statement_id,
            "bill_debated_id": 1
        }


class TestUtilities:
    """Utility functions for tests."""
    
    @staticmethod
    def create_mock_db_session() -> Mock:
        """Create a mock database session."""
        mock_session = Mock(spec=Session)
        
        # Mock query method
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        
        # Mock common query methods
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        mock_query.all.return_value = []
        mock_query.count.return_value = 0
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.group_by.return_value = mock_query
        
        return mock_session
    
    @staticmethod
    def create_mock_redis_client() -> Mock:
        """Create a mock Redis client."""
        mock_redis = Mock()
        
        # Mock Redis methods
        mock_redis.ping.return_value = True
        mock_redis.publish.return_value = 1
        mock_redis.pubsub.return_value = Mock()
        mock_redis.info.return_value = {
            "redis_version": "6.0.0",
            "connected_clients": 1,
            "used_memory_human": "1M"
        }
        
        return mock_redis
    
    @staticmethod
    def create_mock_websocket() -> Mock:
        """Create a mock WebSocket connection."""
        mock_ws = Mock()
        
        # Mock WebSocket methods
        mock_ws.accept.return_value = None
        mock_ws.send_text.return_value = None
        mock_ws.receive_text.return_value = '{"type": "ping"}'
        mock_ws.close.return_value = None
        
        # Mock WebSocket state
        mock_ws.state = Mock()
        mock_ws.query_params = {}
        mock_ws.headers = {}
        
        return mock_ws
    
    @staticmethod
    def assert_response_structure(response_data: Dict[str, Any], expected_keys: list[str]):
        """Assert that response has expected structure."""
        for key in expected_keys:
            assert key in response_data, f"Missing key: {key}"
    
    @staticmethod
    def assert_pagination_structure(pagination: Dict[str, Any]):
        """Assert that pagination object has correct structure."""
        required_keys = ["page", "page_size", "total", "pages"]
        TestUtilities.assert_response_structure(pagination, required_keys)
        
        # Validate pagination values
        assert pagination["page"] >= 1
        assert pagination["page_size"] >= 1
        assert pagination["total"] >= 0
        assert pagination["pages"] >= 0
    
    @staticmethod
    def assert_error_response(response_data: Dict[str, Any], expected_status: str = "error"):
        """Assert that response is an error response."""
        assert "detail" in response_data, "Error response missing 'detail' field"
        if expected_status != "error":
            assert response_data.get("status") == expected_status


# Test markers for pytest
pytestmark = [
    pytest.mark.api,  # Mark all tests as API tests by default
    pytest.mark.fast,  # Mark all tests as fast by default
]


# Global test configuration
test_config = TestConfig()
test_data_factory = TestDataFactory()
test_utilities = TestUtilities()


# Common test fixtures
@pytest.fixture(scope="session")
def test_app():
    """Get the test application instance."""
    return app


@pytest.fixture(scope="session")
def test_client(test_app):
    """Get the test client instance."""
    return TestClient(test_app)


@pytest.fixture(scope="function")
def mock_db():
    """Get a mock database session."""
    return test_utilities.create_mock_db_session()


@pytest.fixture(scope="function")
def mock_redis():
    """Get a mock Redis client."""
    return test_utilities.create_mock_redis_client()


@pytest.fixture(scope="function")
def mock_websocket():
    """Get a mock WebSocket connection."""
    return test_utilities.create_mock_websocket()


@pytest.fixture(scope="function")
def test_bill_data():
    """Get test bill data."""
    return test_data_factory.create_test_bill()


@pytest.fixture(scope="function")
def test_committee_data():
    """Get test committee data."""
    return test_data_factory.create_test_committee()


@pytest.fixture(scope="function")
def test_member_data():
    """Get test member data."""
    return test_data_factory.create_test_member()


@pytest.fixture(scope="function")
def test_vote_data():
    """Get test vote data."""
    return test_data_factory.create_test_vote()


@pytest.fixture(scope="function")
def test_debate_data():
    """Get test debate data."""
    return test_data_factory.create_test_debate()


@pytest.fixture(scope="function")
def test_statement_data():
    """Get test statement data."""
    return test_data_factory.create_test_statement()
