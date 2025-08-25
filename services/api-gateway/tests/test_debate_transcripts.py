"""
Tests for debate transcript system.

Tests FEAT-018 Debate Transcripts (P1 priority).
"""

import pytest
from datetime import datetime, date, time
from uuid import uuid4
from sqlalchemy.orm import Session
from app.core.debate_transcripts import DebateTranscriptService
from app.models.debate_transcripts import (
    DebateSession, DebateStatement, DebateSpeaker,
    DebateAnnotation, DebateTopic, DebateAnalytics
)
from app.models.users import User
from app.schemas.debate_transcripts import (
    SessionCreate, SessionUpdate, StatementCreate,
    SpeakerUpdate, AnnotationCreate, TopicCreate,
    TranscriptSearchRequest, TranscriptImportRequest
)


class TestDebateTranscriptService:
    """Test debate transcript service functionality."""
    
    @pytest.fixture
    def service(self, db_session):
        """Create service instance."""
        return DebateTranscriptService(db_session)
    
    @pytest.fixture
    def test_user(self, db_session):
        """Create test user."""
        user = User(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            hashed_password="hashed"
        )
        db_session.add(user)
        db_session.commit()
        return user
    
    @pytest.fixture
    def test_session(self, db_session):
        """Create test debate session."""
        session = DebateSession(
            parliament_number=44,
            session_number=1,
            sitting_number=123,
            sitting_date=date(2023, 10, 15),
            document_number="44-1-123",
            language="en",
            is_bilingual=True
        )
        db_session.add(session)
        db_session.commit()
        return session
    
    @pytest.fixture
    def test_speaker(self, db_session):
        """Create test speaker."""
        speaker = DebateSpeaker(
            name="John Doe",
            normalized_name="john doe",
            party="Liberal",
            riding="Test Riding",
            province="ON",
            first_seen=date.today(),
            last_seen=date.today()
        )
        db_session.add(speaker)
        db_session.commit()
        return speaker
    
    def test_create_session(self, service):
        """Test creating debate session."""
        session_data = SessionCreate(
            parliament_number=44,
            session_number=1,
            sitting_number=124,
            sitting_date=date(2023, 10, 16),
            language="en",
            start_time=time(10, 0),
            end_time=time(18, 0)
        )
        
        session = service.create_session(session_data)
        
        assert session.document_number == "44-1-124"
        assert session.parliament_number == 44
        assert session.sitting_date == date(2023, 10, 16)
        assert session.start_time == time(10, 0)
    
    def test_create_duplicate_session(self, service, test_session):
        """Test creating duplicate session fails."""
        session_data = SessionCreate(
            parliament_number=test_session.parliament_number,
            session_number=test_session.session_number,
            sitting_number=test_session.sitting_number,
            sitting_date=test_session.sitting_date
        )
        
        with pytest.raises(Exception) as exc_info:
            service.create_session(session_data)
        
        assert "already exists" in str(exc_info.value)
    
    def test_search_sessions(self, service, test_session):
        """Test searching debate sessions."""
        # Create additional sessions
        for i in range(3):
            session = DebateSession(
                parliament_number=44,
                session_number=1,
                sitting_number=125 + i,
                sitting_date=date(2023, 10, 17 + i),
                document_number=f"44-1-{125 + i}"
            )
            service.db.add(session)
        service.db.commit()
        
        # Search by parliament number
        sessions, total = service.search_sessions(
            parliament_number=44,
            page=1,
            page_size=10
        )
        
        assert total == 4
        assert len(sessions) == 4
        
        # Search by date range
        sessions, total = service.search_sessions(
            start_date=date(2023, 10, 17),
            end_date=date(2023, 10, 18),
            page=1,
            page_size=10
        )
        
        assert total == 2
    
    def test_create_statement(self, service, test_session, test_speaker):
        """Test creating debate statement."""
        statement_data = StatementCreate(
            session_id=test_session.id,
            speaker_id=test_speaker.id,
            statement_type="speech",
            content="Mr. Speaker, I rise today to address this important matter.",
            timestamp=time(10, 15),
            topic="Budget",
            language="en"
        )
        
        statement = service.create_statement(statement_data)
        
        assert statement.sequence_number == 1
        assert statement.word_count == 11
        assert statement.speaker_id == test_speaker.id
        assert statement.topic == "Budget"
        
        # Check session stats updated
        service.db.refresh(test_session)
        assert test_session.total_statements == 1
        assert test_session.total_words == 11
    
    def test_search_statements(self, service, test_session, test_speaker):
        """Test searching statements with full-text search."""
        # Create multiple statements
        statements_data = [
            {
                "content": "Mr. Speaker, we must address climate change urgently.",
                "topic": "Environment",
                "speaker_id": test_speaker.id
            },
            {
                "content": "The budget includes significant funding for healthcare.",
                "topic": "Budget",
                "speaker_id": test_speaker.id
            },
            {
                "content": "Climate action is our government's priority.",
                "topic": "Environment",
                "speaker_id": test_speaker.id
            }
        ]
        
        for data in statements_data:
            stmt = StatementCreate(
                session_id=test_session.id,
                statement_type="speech",
                language="en",
                **data
            )
            service.create_statement(stmt)
        
        # Search by query
        search_request = TranscriptSearchRequest(
            query="climate",
            page=1,
            page_size=10
        )
        
        statements, total, facets = service.search_statements(search_request)
        
        assert total == 2  # Two statements mention "climate"
        assert len(statements) == 2
        
        # Search by topic
        search_request = TranscriptSearchRequest(
            topics=["Environment"],
            page=1,
            page_size=10
        )
        
        statements, total, facets = service.search_statements(search_request)
        
        assert total == 2
    
    def test_get_or_create_speaker(self, service):
        """Test speaker creation and retrieval."""
        # Create new speaker
        speaker1 = service.get_or_create_speaker(
            name="Hon. Jane Smith",
            party="Conservative",
            riding="Test West"
        )
        
        assert speaker1.name == "Hon. Jane Smith"
        assert speaker1.normalized_name == "jane smith"
        assert speaker1.party == "Conservative"
        
        # Get existing speaker
        speaker2 = service.get_or_create_speaker(
            name="Jane Smith",  # Without title
            party="Conservative"
        )
        
        assert speaker2.id == speaker1.id  # Same speaker
    
    def test_add_annotation(self, service, test_session, test_speaker, test_user):
        """Test adding annotations to statements."""
        # Create statement
        statement_data = StatementCreate(
            session_id=test_session.id,
            speaker_id=test_speaker.id,
            statement_type="speech",
            content="The member opposite is mistaken.",
            language="en"
        )
        
        statement = service.create_statement(statement_data)
        
        # Add annotation
        annotation_data = AnnotationCreate(
            statement_id=statement.id,
            annotation_type="correction",
            content="The member was referring to Bill C-123, not C-124.",
            is_official=True
        )
        
        annotation = service.add_annotation(annotation_data, test_user)
        
        assert annotation.statement_id == statement.id
        assert annotation.annotation_type == "correction"
        assert annotation.is_official is True
        assert annotation.created_by == test_user.id
    
    def test_create_topic(self, service):
        """Test creating debate topic."""
        topic_data = TopicCreate(
            name="Housing Policy",
            category="social",
            description="Discussions about housing affordability and policy",
            keywords=["housing", "affordability", "mortgage", "rent"]
        )
        
        topic = service.create_topic(topic_data)
        
        assert topic.name == "Housing Policy"
        assert topic.slug == "housing-policy"
        assert topic.category == "social"
        assert len(topic.keywords) == 4
    
    def test_generate_analytics(self, service, test_session, test_speaker):
        """Test generating session analytics."""
        # Create statements with different speakers
        speaker2 = DebateSpeaker(
            name="Jane Doe",
            normalized_name="jane doe",
            party="Conservative",
            riding="Another Riding"
        )
        service.db.add(speaker2)
        service.db.flush()
        
        # Create statements
        for i in range(5):
            speaker = test_speaker if i % 2 == 0 else speaker2
            stmt = StatementCreate(
                session_id=test_session.id,
                speaker_id=speaker.id,
                statement_type="speech" if i < 3 else "question",
                content=f"This is statement number {i} about important matters.",
                topic="Test Topic" if i < 2 else "Another Topic",
                language="en"
            )
            service.create_statement(stmt)
        
        # Generate analytics
        analytics = service.generate_analytics(test_session.id)
        
        assert analytics.session_id == test_session.id
        assert analytics.question_count == 2
        assert len(analytics.top_words) > 0
        assert "Test Topic" in analytics.topic_distribution
        assert analytics.party_participation["Liberal"] > 0
        assert analytics.party_participation["Conservative"] > 0
    
    def test_import_transcript_json(self, service, test_user):
        """Test importing transcript from JSON."""
        json_content = """
        {
            "statements": [
                {
                    "type": "speech",
                    "content": "Mr. Speaker, this is a test statement.",
                    "speaker_name": "Test MP",
                    "speaker_party": "Liberal",
                    "speaker_riding": "Test Riding",
                    "timestamp": "10:00:00",
                    "topic": "Test Topic"
                },
                {
                    "type": "question",
                    "content": "Can the minister explain this policy?",
                    "speaker_name": "Another MP",
                    "speaker_party": "Conservative",
                    "speaker_riding": "Another Riding"
                }
            ]
        }
        """
        
        import_data = TranscriptImportRequest(
            source="json",
            document_content=json_content,
            parliament_number=44,
            session_number=1,
            sitting_number=200,
            sitting_date=date(2023, 11, 1),
            language="en"
        )
        
        session = service.import_transcript(import_data, test_user)
        
        assert session.document_number == "44-1-200"
        assert session.total_statements == 2
        assert session.total_speakers == 2
        
        # Check statements created
        statements = service.db.query(DebateStatement).filter(
            DebateStatement.session_id == session.id
        ).all()
        
        assert len(statements) == 2
        assert statements[0].speaker.name == "Test MP"
        assert statements[1].statement_type == "question"


class TestDebateTranscriptEndpoints:
    """Test debate transcript API endpoints."""
    
    def test_list_sessions(self, client):
        """Test listing debate sessions."""
        response = client.get("/api/v1/debate-transcripts/sessions")
        
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "pagination" in data
    
    def test_search_statements(self, client, db_session):
        """Test searching debate statements."""
        # Create test data
        session = DebateSession(
            parliament_number=44,
            session_number=1,
            sitting_number=100,
            sitting_date=date(2023, 10, 1),
            document_number="44-1-100"
        )
        db_session.add(session)
        
        speaker = DebateSpeaker(
            name="Test Speaker",
            normalized_name="test speaker",
            party="Liberal"
        )
        db_session.add(speaker)
        db_session.flush()
        
        statement = DebateStatement(
            session_id=session.id,
            speaker_id=speaker.id,
            sequence_number=1,
            statement_type="speech",
            content="This is about healthcare policy.",
            word_count=5,
            topic="Healthcare"
        )
        db_session.add(statement)
        db_session.commit()
        
        # Search
        response = client.get(
            "/api/v1/debate-transcripts/statements/search",
            params={"query": "healthcare"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) > 0
        assert data["results"][0]["content"] == "This is about healthcare policy."
    
    def test_get_session_analytics(self, client, db_session):
        """Test getting session analytics."""
        # Create test session
        session = DebateSession(
            id=uuid4(),
            parliament_number=44,
            session_number=1,
            sitting_number=101,
            sitting_date=date(2023, 10, 2),
            document_number="44-1-101"
        )
        db_session.add(session)
        db_session.commit()
        
        response = client.get(
            f"/api/v1/debate-transcripts/sessions/{session.id}/analytics"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "top_words" in data
        assert "topic_distribution" in data
        assert "sentiment_scores" in data
    
    def test_save_search(self, client, auth_headers):
        """Test saving a search."""
        response = client.post(
            "/api/v1/debate-transcripts/searches",
            json={
                "name": "Climate Debates",
                "query": "climate change",
                "filters": {
                    "topics": ["Environment"],
                    "start_date": "2023-01-01"
                },
                "is_public": False,
                "email_alerts": True
            },
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Climate Debates"
        assert data["email_alerts"] is True
    
    def test_export_transcript(self, client, db_session):
        """Test exporting transcript."""
        # Create test session with statements
        session = DebateSession(
            id=uuid4(),
            parliament_number=44,
            session_number=1,
            sitting_number=102,
            sitting_date=date(2023, 10, 3),
            document_number="44-1-102"
        )
        db_session.add(session)
        
        speaker = DebateSpeaker(
            name="Export Test Speaker",
            normalized_name="export test speaker"
        )
        db_session.add(speaker)
        db_session.flush()
        
        statement = DebateStatement(
            session_id=session.id,
            speaker_id=speaker.id,
            sequence_number=1,
            statement_type="speech",
            content="This is test content for export.",
            word_count=6
        )
        db_session.add(statement)
        db_session.commit()
        
        # Export as JSON
        response = client.post(
            "/api/v1/debate-transcripts/export",
            json={
                "session_id": str(session.id),
                "format": "json",
                "include_annotations": False,
                "include_analytics": False
            }
        )
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        
        # Export as TXT
        response = client.post(
            "/api/v1/debate-transcripts/export",
            json={
                "session_id": str(session.id),
                "format": "txt"
            }
        )
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain"