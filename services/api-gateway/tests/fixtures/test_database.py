"""
Test database configuration and setup.

This module provides test database configuration, setup, and teardown
for integration tests that require a real database.
"""

import pytest
from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models.openparliament import Bill, Committee, CommitteeMeeting, ElectedMember, Party, Riding, VoteQuestion
from app.models.users import User


class TestDatabaseConfig:
    """Configuration for test database."""
    
    # Use in-memory SQLite for testing
    TEST_DATABASE_URL = "sqlite:///:memory:"
    TEST_DATABASE_ECHO = False
    
    # Test data settings
    TEST_BILLS_COUNT = 5
    TEST_COMMITTEES_COUNT = 3
    TEST_MEMBERS_COUNT = 10
    TEST_PARTIES_COUNT = 4
    TEST_RIDINGS_COUNT = 15
    TEST_VOTES_COUNT = 8
    TEST_USERS_COUNT = 3


class TestDatabaseManager:
    """Manages test database lifecycle."""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.test_data = {}
    
    def create_test_engine(self):
        """Create test database engine."""
        self.engine = create_engine(
            TestDatabaseConfig.TEST_DATABASE_URL,
            echo=TestDatabaseConfig.TEST_DATABASE_ECHO,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False}
        )
        return self.engine
    
    def create_tables(self):
        """Create all tables in test database."""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """Drop all tables from test database."""
        Base.metadata.drop_all(bind=self.engine)
    
    def create_session_factory(self):
        """Create session factory for test database."""
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        return self.SessionLocal
    
    def get_test_session(self) -> Session:
        """Get a test database session."""
        if not self.SessionLocal:
            self.create_session_factory()
        return self.SessionLocal()
    
    def setup_test_data(self):
        """Set up test data in the database."""
        session = self.get_test_session()
        
        try:
            # Create test parties
            parties = self._create_test_parties(session)
            self.test_data["parties"] = parties
            
            # Create test ridings
            ridings = self._create_test_ridings(session)
            self.test_data["ridings"] = ridings
            
            # Create test users
            users = self._create_test_users(session)
            self.test_data["users"] = users
            
            # Create test bills
            bills = self._create_test_bills(session)
            self.test_data["bills"] = bills
            
            # Create test committees
            committees = self._create_test_committees(session)
            self.test_data["committees"] = committees
            
            # Create test members
            members = self._create_test_members(session, parties, ridings)
            self.test_data["members"] = members
            
            # Create test votes
            votes = self._create_test_votes(session, bills)
            self.test_data["votes"] = votes
            
            # Create test committee meetings
            meetings = self._create_test_committee_meetings(session, committees)
            self.test_data["meetings"] = meetings
            
            session.commit()
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def _create_test_parties(self, session: Session) -> list[Party]:
        """Create test party data."""
        parties = []
        party_names = [
            ("Liberal Party", "Parti libéral", "Lib", "Lib"),
            ("Conservative Party", "Parti conservateur", "Con", "Con"),
            ("New Democratic Party", "Nouveau Parti démocratique", "NDP", "NPD"),
            ("Bloc Québécois", "Bloc Québécois", "BQ", "BQ")
        ]
        
        for i, (name_en, name_fr, short_en, short_fr) in enumerate(party_names, 1):
            party = Party(
                id=i,
                name_en=name_en,
                name_fr=name_fr,
                short_name_en=short_en,
                short_name_fr=short_fr
            )
            session.add(party)
            parties.append(party)
        
        session.flush()
        return parties
    
    def _create_test_ridings(self, session: Session) -> list[Riding]:
        """Create test riding data."""
        ridings = []
        provinces = ["ON", "QC", "BC", "AB", "NS", "NB", "MB", "SK", "NL", "PE", "NT", "NU", "YT"]
        
        for i in range(1, TestDatabaseConfig.TEST_RIDINGS_COUNT + 1):
            province = provinces[(i - 1) % len(provinces)]
            riding = Riding(
                id=i,
                name_en=f"Test Riding {i}",
                name_fr=f"Circonscription de test {i}",
                province=province,
                population=50000 + (i * 1000)
            )
            session.add(riding)
            ridings.append(riding)
        
        session.flush()
        return ridings
    
    def _create_test_users(self, session: Session) -> list[User]:
        """Create test user data."""
        users = []
        user_data = [
            ("testuser1", "test1@example.com"),
            ("testuser2", "test2@example.com"),
            ("admin", "admin@example.com")
        ]
        
        for i, (username, email) in enumerate(user_data, 1):
            user = User(
                id=f"user_{i}",
                username=username,
                email=email,
                is_active=True
            )
            session.add(user)
            users.append(user)
        
        session.flush()
        return users
    
    def _create_test_bills(self, session: Session) -> list[Bill]:
        """Create test bill data."""
        bills = []
        bill_statuses = ["INTRODUCED", "READING", "COMMITTEE", "REPORT", "THIRD_READING", "PASSED"]
        
        for i in range(1, TestDatabaseConfig.TEST_BILLS_COUNT + 1):
            status = bill_statuses[(i - 1) % len(bill_statuses)]
            bill = Bill(
                id=i,
                number=f"C-{100 + i}",
                name_en=f"Test Bill {i}",
                short_title_en=f"Short Title {i}",
                status_code=status,
                introduced="2024-01-01",
                session_id="45-1",
                institution="House",
                sponsor_member_id=None
            )
            session.add(bill)
            bills.append(bill)
        
        session.flush()
        return bills
    
    def _create_test_committees(self, session: Session) -> list[Committee]:
        """Create test committee data."""
        committees = []
        committee_types = ["standing", "special", "legislative"]
        committee_names = [
            ("Finance Committee", "Comité des finances"),
            ("Health Committee", "Comité de la santé"),
            ("Transport Committee", "Comité des transports")
        ]
        
        for i, (name_en, name_fr) in enumerate(committee_names, 1):
            committee = Committee(
                id=i,
                name_en=name_en,
                name_fr=name_fr,
                slug=f"committee-{i}",
                session_id="45-1",
                type=committee_types[(i - 1) % len(committee_types)]
            )
            session.add(committee)
            committees.append(committee)
        
        session.flush()
        return committees
    
    def _create_test_members(self, session: Session, parties: list[Party], ridings: list[Riding]) -> list[ElectedMember]:
        """Create test elected member data."""
        members = []
        member_names = [
            ("John", "Doe"), ("Jane", "Smith"), ("Bob", "Johnson"),
            ("Alice", "Brown"), ("Charlie", "Wilson"), ("Diana", "Davis"),
            ("Edward", "Miller"), ("Fiona", "Garcia"), ("George", "Martinez"),
            ("Helen", "Anderson")
        ]
        
        for i, _ in enumerate(member_names, 1):
            party = parties[(i - 1) % len(parties)]
            riding = ridings[(i - 1) % len(ridings)]
            
            member = ElectedMember(
                id=i,
                politician_id=i,
                party_id=party.id,
                riding_id=riding.id,
                session_id="45-1",
                start_date="2024-01-01",
                end_date=None
            )
            session.add(member)
            members.append(member)
        
        session.flush()
        return members
    
    def _create_test_votes(self, session: Session, bills: list[Bill]) -> list[VoteQuestion]:
        """Create test vote data."""
        votes = []
        vote_results = ["CARRIED", "DEFEATED", "CARRIED", "DEFEATED"]
        
        for i in range(1, TestDatabaseConfig.TEST_VOTES_COUNT + 1):
            bill = bills[(i - 1) % len(bills)]
            result = vote_results[(i - 1) % len(vote_results)]
            
            vote = VoteQuestion(
                id=i,
                session_id="45-1",
                vote_number=i,
                bill_id=bill.id,
                result=result,
                yea_total=150 + (i * 10),
                nay_total=100 + (i * 5),
                paired_count=i,
                absent_count=i * 2,
                vote_date="2024-01-01"
            )
            session.add(vote)
            votes.append(vote)
        
        session.flush()
        return votes
    
    def _create_test_committee_meetings(self, session: Session, committees: list[Committee]) -> list[CommitteeMeeting]:
        """Create test committee meeting data."""
        meetings = []
        
        for i in range(1, TestDatabaseConfig.TEST_COMMITTEES_COUNT + 1):
            committee = committees[i - 1]
            meeting = CommitteeMeeting(
                id=i,
                committee_id=committee.id,
                number=i,
                session_id="45-1",
                date="2024-01-01",
                has_evidence=True
            )
            session.add(meeting)
            meetings.append(meeting)
        
        session.flush()
        return meetings
    
    def cleanup_test_data(self):
        """Clean up test data."""
        self.test_data.clear()
    
    def get_test_data(self, data_type: str) -> list:
        """Get test data of a specific type."""
        return self.test_data.get(data_type, [])
    
    def get_test_data_by_id(self, data_type: str, item_id: int) -> Any:
        """Get test data item by ID."""
        data_list = self.get_test_data(data_type)
        for item in data_list:
            if item.id == item_id:
                return item
        return None


# Global test database manager
test_db_manager = TestDatabaseManager()


@pytest.fixture(scope="session")
def test_database():
    """Set up test database for the test session."""
    # Create test engine and tables
    engine = test_db_manager.create_test_engine()
    test_db_manager.create_tables()
    test_db_manager.create_session_factory()
    
    # Set up test data
    test_db_manager.setup_test_data()
    
    yield test_db_manager
    
    # Cleanup
    test_db_manager.cleanup_test_data()
    test_db_manager.drop_tables()
    engine.dispose()


@pytest.fixture
def test_db_session(test_database):
    """Get a test database session."""
    session = test_database.get_test_session()
    yield session
    session.close()


@pytest.fixture
def override_get_db_test(test_db_session):
    """Override the database dependency to use test database."""
    def _override_get_db():
        return test_db_session
    
    from app.main import app
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


# Test data fixtures
@pytest.fixture
def test_bills(test_database):
    """Get test bills data."""
    return test_database.get_test_data("bills")


@pytest.fixture
def test_committees(test_database):
    """Get test committees data."""
    return test_database.get_test_data("committees")


@pytest.fixture
def test_members(test_database):
    """Get test members data."""
    return test_database.get_test_data("members")


@pytest.fixture
def test_parties(test_database):
    """Get test parties data."""
    return test_database.get_test_data("parties")


@pytest.fixture
def test_ridings(test_database):
    """Get test ridings data."""
    return test_database.get_test_data("ridings")


@pytest.fixture
def test_votes(test_database):
    """Get test votes data."""
    return test_database.get_test_data("votes")


@pytest.fixture
def test_users(test_database):
    """Get test users data."""
    return test_database.get_test_data("users")


@pytest.fixture
def test_committee_meetings(test_database):
    """Get test committee meetings data."""
    return test_database.get_test_data("meetings")
