"""
Test configuration and fixtures for the API Gateway tests.

This module provides comprehensive test fixtures and configuration
for the API Gateway test suite.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.main import app
from app.database import get_db
from tests.test_config import test_config, test_data_factory, test_utilities


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Mock database session fixture."""
    mock_session = Mock(spec=Session)
    
    # Create a mock bill object for bill ID 1
    mock_bill = Mock()
    mock_bill.id = 1
    mock_bill.number = "C-123"
    mock_bill.name_en = "Test Bill"
    mock_bill.short_title_en = "Test Bill Short"
    mock_bill.status_code = "INTRODUCED"
    mock_bill.introduced = "2024-01-01"
    mock_bill.session_id = "45-1"
    mock_bill.institution = "House"
    mock_bill.sponsor_member_id = None
    
    # Create a comprehensive mock query that handles all the chaining
    def create_chain_mock():
        chain_mock = Mock()
        
        # Mock the filter method to return the same mock for chaining
        def mock_filter(*args, **kwargs):
            return chain_mock
        
        # Mock the first method to return the mock bill for bill queries
        def mock_first():
            return mock_bill
        
        # Mock the all method to return empty lists
        def mock_all():
            return []
        
        # Mock the count method to return 0
        def mock_count():
            return 0
        
        # Mock the offset and limit methods for pagination
        def mock_offset(*args, **kwargs):
            return chain_mock
        
        def mock_limit(*args, **kwargs):
            return chain_mock
        
        def mock_order_by(*args, **kwargs):
            return chain_mock
        
        # Mock the group_by method
        def mock_group_by(*args, **kwargs):
            return chain_mock
        
        # Mock the func method for aggregate functions
        def mock_func(*args, **kwargs):
            func_mock = Mock()
            func_mock.count.return_value = 0
            return func_mock
        
        # Set up the mock methods
        chain_mock.filter = mock_filter
        chain_mock.first = mock_first
        chain_mock.all = mock_all
        chain_mock.count = mock_count
        chain_mock.offset = mock_offset
        chain_mock.limit = mock_limit
        chain_mock.order_by = mock_order_by
        chain_mock.group_by = mock_group_by
        
        return chain_mock
    
    # Create the chain mock
    chain_mock = create_chain_mock()
    
    # Mock the query method to return our chain mock
    mock_session.query.return_value = chain_mock
    
    # Mock db.execute() for raw SQL queries
    mock_result = Mock()
    mock_result.__iter__ = lambda self: iter([])  # Empty results
    mock_session.execute.return_value = mock_result
    
    # Mock SQLAlchemy func for aggregate functions
    mock_session.func = Mock()
    
    return mock_session


@pytest.fixture
def override_get_db(mock_db):
    """Override the database dependency to use mock database."""
    def _override_get_db():
        return mock_db
    
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def test_client() -> TestClient:
    """Get the test client instance."""
    return TestClient(app)


@pytest.fixture
def mock_redis():
    """Mock Redis client fixture."""
    return test_utilities.create_mock_redis_client()


@pytest.fixture
def mock_websocket():
    """Mock WebSocket connection fixture."""
    return test_utilities.create_mock_websocket()


@pytest.fixture
def test_bill_data() -> Dict[str, Any]:
    """Get test bill data."""
    return test_data_factory.create_test_bill()


@pytest.fixture
def test_committee_data() -> Dict[str, Any]:
    """Get test committee data."""
    return test_data_factory.create_test_committee()


@pytest.fixture
def test_member_data() -> Dict[str, Any]:
    """Get test member data."""
    return test_data_factory.create_test_member()


@pytest.fixture
def test_vote_data() -> Dict[str, Any]:
    """Get test vote data."""
    return test_data_factory.create_test_vote()


@pytest.fixture
def test_debate_data() -> Dict[str, Any]:
    """Get test debate data."""
    return test_data_factory.create_test_debate()


@pytest.fixture
def test_statement_data() -> Dict[str, Any]:
    """Get test statement data."""
    return test_data_factory.create_test_statement()


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_settings():
    """Mock application settings for testing."""
    with patch('app.config.settings') as mock_settings:
        mock_settings.SECRET_KEY = test_config.TEST_JWT_SECRET
        mock_settings.DATABASE_URL = test_config.TEST_DATABASE_URL
        mock_settings.REDIS_HOST = test_config.TEST_REDIS_HOST
        mock_settings.REDIS_PORT = test_config.TEST_REDIS_PORT
        yield mock_settings
