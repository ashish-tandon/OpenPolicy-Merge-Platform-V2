"""
Test utilities and helper functions.

This module provides common test utilities, assertions, and helper functions
that can be used across different test modules.
"""

from typing import Any, Dict, List
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock

from app.models.openparliament import Bill, Committee, ElectedMember, Party, Riding, VoteQuestion
from app.models.users import User


class TestAssertions:
    """Common test assertions for API responses."""
    
    @staticmethod
    def assert_response_structure(response_data: Dict[str, Any], expected_keys: List[str]):
        """Assert that response contains expected keys."""
        for key in expected_keys:
            assert key in response_data, f"Response missing key: {key}"
    
    @staticmethod
    def assert_pagination_structure(response_data: Dict[str, Any]):
        """Assert that response has proper pagination structure."""
        pagination_keys = ["items", "total", "page", "size", "total_pages"]
        TestAssertions.assert_response_structure(response_data, pagination_keys)
        
        # Check pagination values
        assert isinstance(response_data["total"], int), "total should be integer"
        assert isinstance(response_data["page"], int), "page should be integer"
        assert isinstance(response_data["size"], int), "size should be integer"
        assert isinstance(response_data["total_pages"], int), "total_pages should be integer"
        assert response_data["page"] > 0, "page should be positive"
        assert response_data["size"] > 0, "size should be positive"
        assert response_data["total_pages"] > 0, "total_pages should be positive"
    
    @staticmethod
    def assert_error_response(response_data: Dict[str, Any], expected_status: int = None):
        """Assert that response is an error response."""
        error_keys = ["detail", "error", "message"]
        has_error_key = any(key in response_data for key in error_keys)
        assert has_error_key, "Response should contain error information"
        
        if expected_status:
            assert "status_code" in response_data, "Error response should contain status_code"
            assert response_data["status_code"] == expected_status, f"Expected status {expected_status}"
    
    @staticmethod
    def assert_bill_structure(bill_data: Dict[str, Any]):
        """Assert that bill data has proper structure."""
        bill_keys = ["id", "number", "name_en", "status_code", "introduced", "session_id"]
        TestAssertions.assert_response_structure(bill_data, bill_keys)
        
        # Check data types
        assert isinstance(bill_data["id"], int), "bill id should be integer"
        assert isinstance(bill_data["number"], str), "bill number should be string"
        assert isinstance(bill_data["name_en"], str), "bill name should be string"
        assert isinstance(bill_data["status_code"], str), "bill status should be string"
    
    @staticmethod
    def assert_committee_structure(committee_data: Dict[str, Any]):
        """Assert that committee data has proper structure."""
        committee_keys = ["id", "name_en", "slug", "session_id", "type"]
        TestAssertions.assert_response_structure(committee_data, committee_keys)
        
        # Check data types
        assert isinstance(committee_data["id"], int), "committee id should be integer"
        assert isinstance(committee_data["name_en"], str), "committee name should be string"
        assert isinstance(committee_data["slug"], str), "committee slug should be string"
    
    @staticmethod
    def assert_member_structure(member_data: Dict[str, Any]):
        """Assert that member data has proper structure."""
        member_keys = ["id", "politician_id", "party_id", "riding_id", "session_id"]
        TestAssertions.assert_response_structure(member_data, member_keys)
        
        # Check data types
        assert isinstance(member_data["id"], int), "member id should be integer"
        assert isinstance(member_data["politician_id"], int), "politician_id should be integer"
        assert isinstance(member_data["party_id"], int), "party_id should be integer"
        assert isinstance(member_data["riding_id"], int), "riding_id should be integer"


class TestDataHelpers:
    """Helper functions for creating and manipulating test data."""
    
    @staticmethod
    def create_mock_bill(bill_id: int = 1, **kwargs) -> Mock:
        """Create a mock bill with default values."""
        mock_bill = Mock(spec=Bill)
        mock_bill.id = bill_id
        mock_bill.number = kwargs.get("number", f"C-{100 + bill_id}")
        mock_bill.name_en = kwargs.get("name_en", f"Test Bill {bill_id}")
        mock_bill.short_title_en = kwargs.get("short_title_en", f"Short Title {bill_id}")
        mock_bill.status_code = kwargs.get("status_code", "INTRODUCED")
        mock_bill.introduced = kwargs.get("introduced", "2024-01-01")
        mock_bill.session_id = kwargs.get("session_id", "45-1")
        mock_bill.institution = kwargs.get("institution", "House")
        mock_bill.sponsor_member_id = kwargs.get("sponsor_member_id")
        
        # Add relationships if provided
        if "committee" in kwargs:
            mock_bill.committee = kwargs["committee"]
        if "votes" in kwargs:
            mock_bill.votes = kwargs["votes"]
        
        return mock_bill
    
    @staticmethod
    def create_mock_committee(committee_id: int = 1, **kwargs) -> Mock:
        """Create a mock committee with default values."""
        mock_committee = Mock(spec=Committee)
        mock_committee.id = committee_id
        mock_committee.name_en = kwargs.get("name_en", f"Test Committee {committee_id}")
        mock_committee.name_fr = kwargs.get("name_fr", f"Comité de test {committee_id}")
        mock_committee.slug = kwargs.get("slug", f"committee-{committee_id}")
        mock_committee.session_id = kwargs.get("session_id", "45-1")
        mock_committee.type = kwargs.get("type", "standing")
        
        # Add relationships if provided
        if "meetings" in kwargs:
            mock_committee.meetings = kwargs["meetings"]
        
        return mock_committee
    
    @staticmethod
    def create_mock_member(member_id: int = 1, **kwargs) -> Mock:
        """Create a mock elected member with default values."""
        mock_member = Mock(spec=ElectedMember)
        mock_member.id = member_id
        mock_member.politician_id = kwargs.get("politician_id", member_id)
        mock_member.party_id = kwargs.get("party_id", 1)
        mock_member.riding_id = kwargs.get("riding_id", 1)
        mock_member.session_id = kwargs.get("session_id", "45-1")
        mock_member.start_date = kwargs.get("start_date", "2024-01-01")
        mock_member.end_date = kwargs.get("end_date")
        
        # Add relationships if provided
        if "party" in kwargs:
            mock_member.party = kwargs["party"]
        if "riding" in kwargs:
            mock_member.riding = kwargs["riding"]
        
        return mock_member
    
    @staticmethod
    def create_mock_party(party_id: int = 1, **kwargs) -> Mock:
        """Create a mock party with default values."""
        mock_party = Mock(spec=Party)
        mock_party.id = party_id
        mock_party.name_en = kwargs.get("name_en", f"Test Party {party_id}")
        mock_party.name_fr = kwargs.get("name_fr", f"Parti de test {party_id}")
        mock_party.short_name_en = kwargs.get("short_name_en", f"TP{party_id}")
        mock_party.short_name_fr = kwargs.get("short_name_fr", f"PT{party_id}")
        
        return mock_party
    
    @staticmethod
    def create_mock_riding(riding_id: int = 1, **kwargs) -> Mock:
        """Create a mock riding with default values."""
        mock_riding = Mock(spec=Riding)
        mock_riding.id = riding_id
        mock_riding.name_en = kwargs.get("name_en", f"Test Riding {riding_id}")
        mock_riding.name_fr = kwargs.get("name_fr", f"Circonscription de test {riding_id}")
        mock_riding.province = kwargs.get("province", "ON")
        mock_riding.population = kwargs.get("population", 50000 + (riding_id * 1000))
        
        return mock_riding
    
    @staticmethod
    def create_mock_vote(vote_id: int = 1, **kwargs) -> Mock:
        """Create a mock vote with default values."""
        mock_vote = Mock(spec=VoteQuestion)
        mock_vote.id = vote_id
        mock_vote.session_id = kwargs.get("session_id", "45-1")
        mock_vote.vote_number = kwargs.get("vote_number", vote_id)
        mock_vote.bill_id = kwargs.get("bill_id", 1)
        mock_vote.result = kwargs.get("result", "CARRIED")
        mock_vote.yea_total = kwargs.get("yea_total", 150 + (vote_id * 10))
        mock_vote.nay_total = kwargs.get("nay_total", 100 + (vote_id * 5))
        mock_vote.paired_count = kwargs.get("paired_count", vote_id)
        mock_vote.absent_count = kwargs.get("absent_count", vote_id * 2)
        mock_vote.vote_date = kwargs.get("vote_date", "2024-01-01")
        
        return mock_vote
    
    @staticmethod
    def create_mock_user(user_id: str = "user_1", **kwargs) -> Mock:
        """Create a mock user with default values."""
        mock_user = Mock(spec=User)
        mock_user.id = user_id
        mock_user.username = kwargs.get("username", f"testuser{user_id.split('_')[-1]}")
        mock_user.email = kwargs.get("email", f"test{user_id.split('_')[-1]}@example.com")
        mock_user.is_active = kwargs.get("is_active", True)
        mock_user.is_verified = kwargs.get("is_verified", True)
        
        return mock_user


class TestMockHelpers:
    """Helper functions for creating and configuring mocks."""
    
    @staticmethod
    def create_mock_db_session() -> Mock:
        """Create a mock database session."""
        mock_session = Mock()
        
        # Mock query method
        mock_query = Mock()
        mock_session.query.return_value = mock_query
        
        # Mock execute method
        mock_execute = Mock()
        mock_session.execute.return_value = mock_execute
        
        # Mock add method
        mock_session.add = Mock()
        
        # Mock commit method
        mock_session.commit = Mock()
        
        # Mock rollback method
        mock_session.rollback = Mock()
        
        # Mock close method
        mock_session.close = Mock()
        
        return mock_session
    
    @staticmethod
    def create_mock_redis_client() -> Mock:
        """Create a mock Redis client."""
        mock_redis = Mock()
        
        # Mock async methods
        mock_redis.get_redis_info = AsyncMock(return_value={
            "redis_version": "6.0.0",
            "connected_clients": 10,
            "used_memory": "1.5M"
        })
        
        mock_redis.publish_event = AsyncMock(return_value=1)
        mock_redis.subscribe_to_channel = AsyncMock(return_value=True)
        mock_redis.unsubscribe_from_channel = AsyncMock(return_value=True)
        
        return mock_redis
    
    @staticmethod
    def create_mock_websocket() -> Mock:
        """Create a mock WebSocket connection."""
        mock_ws = Mock()
        
        # Mock send_text method
        mock_ws.send_text = AsyncMock()
        
        # Mock send_json method
        mock_ws.send_json = AsyncMock()
        
        # Mock close method
        mock_ws.close = AsyncMock()
        
        # Mock state attribute
        mock_ws.state = {}
        
        return mock_ws
    
    @staticmethod
    def create_mock_connection_manager() -> Mock:
        """Create a mock WebSocket connection manager."""
        mock_cm = Mock()
        
        # Mock async methods
        mock_cm.broadcast_to_room = AsyncMock(return_value=None)
        mock_cm.broadcast_to_all = AsyncMock(return_value=None)
        mock_cm.send_personal_message = AsyncMock(return_value=None)
        mock_cm.disconnect = AsyncMock(return_value=None)
        
        return mock_cm


class TestResponseHelpers:
    """Helper functions for testing API responses."""
    
    @staticmethod
    def make_request(client: TestClient, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """Make a request and return the response data."""
        method_map = {
            "GET": client.get,
            "POST": client.post,
            "PUT": client.put,
            "DELETE": client.delete,
            "PATCH": client.patch
        }
        
        request_method = method_map.get(method.upper())
        if not request_method:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response = request_method(url, **kwargs)
        return response.json() if response.content else {}
    
    @staticmethod
    def assert_status_code(response, expected_status: int):
        """Assert that response has expected status code."""
        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}"
    
    @staticmethod
    def assert_response_contains(response_data: Dict[str, Any], expected_data: Dict[str, Any]):
        """Assert that response contains expected data."""
        for key, value in expected_data.items():
            assert key in response_data, f"Response missing key: {key}"
            assert response_data[key] == value, f"Value mismatch for {key}: expected {value}, got {response_data[key]}"
    
    @staticmethod
    def assert_list_response_structure(response_data: Dict[str, Any], item_validator=None):
        """Assert that response is a proper list response."""
        assert "items" in response_data, "Response should contain 'items' key"
        assert isinstance(response_data["items"], list), "Items should be a list"
        
        if item_validator and response_data["items"]:
            for item in response_data["items"]:
                item_validator(item)


# Global instances for easy access
test_assertions = TestAssertions()
test_data_helpers = TestDataHelpers()
test_mock_helpers = TestMockHelpers()
test_response_helpers = TestResponseHelpers()
