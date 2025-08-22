"""
Database test fixtures for API Gateway tests.

This module provides database-related test fixtures, mock data,
and utilities for testing database operations.
"""

import pytest
from unittest.mock import Mock, MagicMock
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool

from app.database import get_db, Base
from app.models.openparliament import Bill, Committee, CommitteeMeeting, ElectedMember, Party, Riding, VoteQuestion
from app.models.users import User, PasswordResetToken, UserSession
from tests.test_config import test_data_factory


class DatabaseTestFixtures:
    """Database test fixtures and utilities."""
    
    @staticmethod
    def create_mock_bill(bill_id: int = 1) -> Mock:
        """Create a mock Bill object."""
        mock_bill = Mock(spec=Bill)
        mock_bill.id = bill_id
        mock_bill.number = f"C-{100 + bill_id}"
        mock_bill.name_en = f"Test Bill {bill_id}"
        mock_bill.short_title_en = f"Short Title {bill_id}"
        mock_bill.status_code = "INTRODUCED"
        mock_bill.introduced = "2024-01-01"
        mock_bill.session_id = "45-1"
        mock_bill.institution = "House"
        mock_bill.sponsor_member_id = None
        mock_bill.sponsor_politician_id = None
        
        return mock_bill
    
    @staticmethod
    def create_mock_committee(committee_id: int = 1) -> Mock:
        """Create a mock Committee object."""
        mock_committee = Mock(spec=Committee)
        mock_committee.id = committee_id
        mock_committee.name_en = f"Test Committee {committee_id}"
        mock_committee.name_fr = f"Comité de test {committee_id}"
        mock_committee.slug = f"test-committee-{committee_id}"
        mock_committee.session_id = "45-1"
        mock_committee.type = "standing"
        
        return mock_committee
    
    @staticmethod
    def create_mock_committee_meeting(meeting_id: int = 1, committee_id: int = 1) -> Mock:
        """Create a mock CommitteeMeeting object."""
        mock_meeting = Mock(spec=CommitteeMeeting)
        mock_meeting.id = meeting_id
        mock_meeting.committee_id = committee_id
        mock_meeting.number = meeting_id
        mock_meeting.session_id = "45-1"
        mock_meeting.date = "2024-01-01"
        mock_meeting.has_evidence = True
        
        return mock_meeting
    
    @staticmethod
    def create_mock_elected_member(member_id: int = 1) -> Mock:
        """Create a mock ElectedMember object."""
        mock_member = Mock(spec=ElectedMember)
        mock_member.id = member_id
        mock_member.politician_id = member_id
        mock_member.party_id = 1
        mock_member.riding_id = 1
        mock_member.session_id = "45-1"
        mock_member.start_date = "2024-01-01"
        mock_member.end_date = None
        
        # Mock politician relationship
        mock_politician = Mock()
        mock_politician.name_given = "John"
        mock_politician.name_family = "Doe"
        mock_politician.name = "John Doe"
        mock_member.politician = mock_politician
        
        # Mock party relationship
        mock_party = Mock()
        mock_party.name_en = "Test Party"
        mock_party.name_fr = "Parti de test"
        mock_member.party = mock_party
        
        # Mock riding relationship
        mock_riding = Mock()
        mock_riding.name_en = "Test Riding"
        mock_riding.name_fr = "Circonscription de test"
        mock_member.riding = mock_riding
        
        return mock_member
    
    @staticmethod
    def create_mock_party(party_id: int = 1) -> Mock:
        """Create a mock Party object."""
        mock_party = Mock(spec=Party)
        mock_party.id = party_id
        mock_party.name_en = f"Test Party {party_id}"
        mock_party.name_fr = f"Parti de test {party_id}"
        mock_party.short_name_en = f"TP{party_id}"
        mock_party.short_name_fr = f"PT{party_id}"
        
        return mock_party
    
    @staticmethod
    def create_mock_riding(riding_id: int = 1) -> Mock:
        """Create a mock Riding object."""
        mock_riding = Mock(spec=Riding)
        mock_riding.id = riding_id
        mock_riding.name_en = f"Test Riding {riding_id}"
        mock_riding.name_fr = f"Circonscription de test {riding_id}"
        mock_riding.province = "ON"
        mock_riding.population = 100000
        
        return mock_riding
    
    @staticmethod
    def create_mock_vote_question(vote_id: int = 1) -> Mock:
        """Create a mock VoteQuestion object."""
        mock_vote = Mock(spec=VoteQuestion)
        mock_vote.id = vote_id
        mock_vote.session_id = "45-1"
        mock_vote.vote_number = vote_id
        mock_vote.bill_id = 1
        mock_vote.result = "CARRIED"
        mock_vote.yea_total = 150
        mock_vote.nay_total = 100
        mock_vote.paired_count = 5
        mock_vote.absent_count = 10
        mock_vote.vote_date = "2024-01-01"
        
        return mock_vote
    
    @staticmethod
    def create_mock_user(user_id: str = "test_user_123") -> Mock:
        """Create a mock User object."""
        mock_user = Mock(spec=User)
        mock_user.id = user_id
        mock_user.username = "testuser"
        mock_user.email = "test@example.com"
        mock_user.is_active = True
        mock_user.created_at = "2024-01-01T00:00:00"
        
        return mock_user
    
    @staticmethod
    def create_mock_password_reset_token(token_id: str = "test_token_123") -> Mock:
        """Create a mock PasswordResetToken object."""
        mock_token = Mock(spec=PasswordResetToken)
        mock_token.id = token_id
        mock_token.user_id = "test_user_123"
        mock_token.token = "test_reset_token"
        mock_token.expires_at = "2024-12-31T23:59:59"
        mock_token.is_used = False
        
        return mock_token
    
    @staticmethod
    def create_mock_user_session(session_id: str = "test_session_123") -> Mock:
        """Create a mock UserSession object."""
        mock_session = Mock(spec=UserSession)
        mock_session.id = session_id
        mock_session.user_id = "test_user_123"
        mock_session.created_at = "2024-01-01T00:00:00"
        mock_session.last_activity = "2024-01-01T12:00:00"
        mock_session.is_active = True
        
        return mock_session


class MockDatabaseSession:
    """Mock database session for testing."""
    
    def __init__(self):
        self.mock_data = {}
        self.query_results = {}
        self.execution_results = []
        self._setup_default_mocks()
    
    def _setup_default_mocks(self):
        """Set up default mock data."""
        # Create default mock objects
        self.mock_data["bill_1"] = DatabaseTestFixtures.create_mock_bill(1)
        self.mock_data["committee_1"] = DatabaseTestFixtures.create_mock_committee(1)
        self.mock_data["member_1"] = DatabaseTestFixtures.create_mock_elected_member(1)
        self.mock_data["party_1"] = DatabaseTestFixtures.create_mock_party(1)
        self.mock_data["riding_1"] = DatabaseTestFixtures.create_mock_riding(1)
        self.mock_data["vote_1"] = DatabaseTestFixtures.create_mock_vote_question(1)
        self.mock_data["user_1"] = DatabaseTestFixtures.create_mock_user("test_user_123")
        
        # Set up query results
        self.query_results = {
            "bills": [self.mock_data["bill_1"]],
            "committees": [self.mock_data["bill_1"]],
            "members": [self.mock_data["member_1"]],
            "parties": [self.mock_data["party_1"]],
            "ridings": [self.mock_data["riding_1"]],
            "votes": [self.mock_data["vote_1"]],
            "users": [self.mock_data["user_1"]]
        }
    
    def query(self, model_class):
        """Mock the query method."""
        mock_query = Mock()
        
        # Mock filter method
        def mock_filter(*args, **kwargs):
            # Check if filtering by ID
            for arg in args:
                if hasattr(arg, 'left') and hasattr(arg.left, 'key') and arg.left.key == 'id':
                    if hasattr(arg.right, 'value'):
                        id_value = arg.right.value
                        if model_class == Bill and id_value == 1:
                            mock_query.first.return_value = self.mock_data["bill_1"]
                        elif model_class == Committee and id_value == 1:
                            mock_query.first.return_value = self.mock_data["committee_1"]
                        elif model_class == ElectedMember and id_value == 1:
                            mock_query.first.return_value = self.mock_data["member_1"]
                        else:
                            mock_query.first.return_value = None
                        return mock_query
            
            # Default filter behavior
            return mock_query
        
        # Mock other query methods
        mock_query.filter = mock_filter
        mock_query.first.return_value = None
        mock_query.all.return_value = []
        mock_query.count.return_value = 0
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.group_by.return_value = mock_query
        mock_query.join.return_value = mock_query
        
        # Mock func for aggregate functions
        def mock_func(*args, **kwargs):
            func_mock = Mock()
            func_mock.count.return_value = 0
            return func_mock
        
        mock_query.func = mock_func
        
        return mock_query
    
    def execute(self, query):
        """Mock the execute method."""
        mock_result = Mock()
        mock_result.__iter__ = lambda self: iter([])
        mock_result.fetchall.return_value = []
        mock_result.fetchone.return_value = None
        return mock_result
    
    def commit(self):
        """Mock the commit method."""
        pass
    
    def rollback(self):
        """Mock the rollback method."""
        pass
    
    def close(self):
        """Mock the close method."""
        pass


# Global fixtures
database_fixtures = DatabaseTestFixtures()


@pytest.fixture
def mock_db_session():
    """Get a mock database session."""
    return MockDatabaseSession()


@pytest.fixture
def mock_bill():
    """Get a mock bill object."""
    return database_fixtures.create_mock_bill()


@pytest.fixture
def mock_committee():
    """Get a mock committee object."""
    return database_fixtures.create_mock_committee()


@pytest.fixture
def mock_member():
    """Get a mock elected member object."""
    return database_fixtures.create_mock_elected_member()


@pytest.fixture
def mock_party():
    """Get a mock party object."""
    return database_fixtures.create_mock_party()


@pytest.fixture
def mock_riding():
    """Get a mock riding object."""
    return database_fixtures.create_mock_riding()


@pytest.fixture
def mock_vote():
    """Get a mock vote question object."""
    return database_fixtures.create_mock_vote_question()


@pytest.fixture
def mock_user():
    """Get a mock user object."""
    return database_fixtures.create_mock_user()


@pytest.fixture
def mock_password_reset_token():
    """Get a mock password reset token object."""
    return database_fixtures.create_mock_password_reset_token()


@pytest.fixture
def mock_user_session():
    """Get a mock user session object."""
    return database_fixtures.create_mock_user_session()


@pytest.fixture
def override_get_db(mock_db_session):
    """Override the database dependency to use mock database."""
    from app.database import get_db
    
    def _override_get_db():
        return mock_db_session
    
    from app.main import app
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()
