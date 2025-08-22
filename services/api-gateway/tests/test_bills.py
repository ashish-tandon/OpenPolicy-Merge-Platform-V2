"""
Tests for bills API endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestBillsAPI:
    """Test cases for bills API endpoints."""
    
    def test_list_bills_empty(self, override_get_db):
        """Test listing bills when database is empty."""
        response = client.get("/api/v1/bills/")
        assert response.status_code == 200
        
        data = response.json()
        assert "bills" in data
        assert "pagination" in data
        assert data["bills"] == []
        assert data["pagination"]["total"] == 0
    
    def test_list_bills_with_pagination(self, override_get_db):
        """Test bills endpoint with pagination parameters."""
        response = client.get("/api/v1/bills/?page=2&page_size=10")
        assert response.status_code == 200
        
        data = response.json()
        assert data["pagination"]["page"] == 2
        assert data["pagination"]["page_size"] == 10
    
    def test_list_bills_invalid_pagination(self, override_get_db):
        """Test bills endpoint with invalid pagination."""
        response = client.get("/api/v1/bills/?page=0&page_size=200")
        assert response.status_code == 422  # Validation error
    
    def test_get_bill_detail_not_found(self, override_get_db):
        """Test getting bill detail for non-existent bill."""
        response = client.get("/api/v1/bills/99999")
        assert response.status_code == 404
        assert "Bill not found" in response.json()["detail"]
    
    def test_bill_suggestions_empty(self, override_get_db):
        """Test bill suggestions when no matches found."""
        response = client.get("/api/v1/bills/suggestions?q=nonexistent")
        assert response.status_code == 200
        data = response.json()
        assert "suggestions" in data
        assert data["suggestions"] == []
    
    def test_bill_suggestions_invalid_query(self, override_get_db):
        """Test bill suggestions with invalid query."""
        response = client.get("/api/v1/bills/suggestions?q=")
        assert response.status_code == 422  # Validation error for empty query
    
    def test_bills_summary_empty(self, override_get_db):
        """Test bills summary when database is empty."""
        response = client.get("/api/v1/bills/summary/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_bills"] == 0
        assert data["status_breakdown"] == {}
        assert data["session_breakdown"] == {}


class TestBillsSearch:
    """Test cases for bill search functionality."""
    
    def test_search_bills_no_query(self, override_get_db):
        """Test search bills without search query."""
        response = client.get("/api/v1/bills/?q=")
        assert response.status_code == 200
    
    def test_search_bills_with_query(self, override_get_db):
        """Test search bills with search query."""
        response = client.get("/api/v1/bills/?q=test")
        assert response.status_code == 200
    
    def test_filter_bills_by_parliament(self, override_get_db):
        """Test filtering bills by parliament number."""
        response = client.get("/api/v1/bills/?parliament=44")
        assert response.status_code == 200
    
    def test_filter_bills_by_session(self, override_get_db):
        """Test filtering bills by session number."""
        response = client.get("/api/v1/bills/?session=1")
        assert response.status_code == 200
    
    def test_filter_bills_by_status(self, override_get_db):
        """Test filtering bills by status."""
        response = client.get("/api/v1/bills/?status=introduced")
        assert response.status_code == 200


class TestBillsValidation:
    """Test cases for bill validation."""
    
    def test_bills_page_validation(self, override_get_db):
        """Test page parameter validation."""
        response = client.get("/api/v1/bills/?page=0")
        assert response.status_code == 422
    
    def test_bills_page_size_validation(self, override_get_db):
        """Test page_size parameter validation."""
        response = client.get("/api/v1/bills/?page_size=0")
        assert response.status_code == 422


class TestBillsErrorHandling:
    """Test cases for bill error handling."""
    
    def test_bills_database_error(self, override_get_db):
        """Test handling of database errors."""
        # This test would need more sophisticated mocking
        # For now, just ensure the endpoint exists
        response = client.get("/api/v1/bills/")
        assert response.status_code == 200
    
    def test_bills_invalid_bill_id(self, override_get_db):
        """Test handling of invalid bill IDs."""
        response = client.get("/api/v1/bills/99999")
        assert response.status_code == 404


# Mock data for testing
@pytest.fixture
def mock_bill_data():
    """Mock bill data for testing."""
    return {
        "id": "test-uuid",
        "bill_number": "C-123",
        "title": "Test Bill",
        "summary": "A test bill for testing purposes",
        "status": "introduced",
        "introduced_date": "2024-01-01"
    }


@pytest.fixture
def mock_pagination_data():
    """Mock pagination data for testing."""
    return {
        "page": 1,
        "page_size": 20,
        "total": 0,
        "pages": 0
    }
