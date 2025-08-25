"""
Tests for search endpoint alignment - CHK-0302.1 compliance.

Verifies that the search endpoint properly supports all intended parameters
and behavior according to FEAT-001 specification.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import date, datetime
from unittest.mock import patch, Mock

from app.main import app

client = TestClient(app)


class TestSearchEndpointAlignment:
    """Test suite verifying search endpoint alignment with spec"""
    
    def test_search_supports_all_parameters(self):
        """Test that all intended parameters are supported"""
        response = client.get(
            "/api/v1/search",
            params={
                "q": "test query",
                "content_type": "bills",
                "parliament": 44,
                "session": 1,
                "party": "Liberal",
                "member": "John Doe",
                "date__gte": "2023-01-01",
                "date__lte": "2023-12-31",
                "language": "en",
                "sort": "relevance",
                "page": 1,
                "page_size": 20,
                "highlight": True
            }
        )
        
        # Should accept all parameters without error
        assert response.status_code == 200
        data = response.json()
        
        # Verify filters are tracked
        assert "filters_applied" in data
        filters = data["filters_applied"]
        assert filters["content_type"] == "bills"
        assert filters["parliament"] == 44
        assert filters["party"] == "Liberal"
        assert filters["language"] == "en"
    
    def test_content_type_filtering(self):
        """Test content type filtering works correctly"""
        # Test each content type
        for content_type in ["bills", "members", "votes", "debates", "committees", "all"]:
            response = client.get(
                "/api/v1/search",
                params={"q": "test", "content_type": content_type}
            )
            assert response.status_code == 200
            data = response.json()
            
            if content_type != "all":
                # Results should only contain the specified type
                for result in data["results"]:
                    if content_type == "members":
                        assert result["content_type"] == "member"
                    else:
                        assert result["content_type"] == content_type.rstrip('s')
    
    def test_search_result_metadata(self):
        """Test that search results include proper metadata"""
        response = client.get("/api/v1/search", params={"q": "test"})
        assert response.status_code == 200
        data = response.json()
        
        # Each result should have metadata
        for result in data["results"]:
            assert "id" in result
            assert "title" in result
            assert "content_type" in result
            assert "snippet" in result
            assert "url" in result
            assert "relevance_score" in result
            assert 0.0 <= result["relevance_score"] <= 1.0
            
            # Metadata field should exist
            if "metadata" in result and result["metadata"]:
                metadata = result["metadata"]
                
                # Check type-specific metadata
                if result["content_type"] == "bill":
                    assert any(key in metadata for key in ["bill_number", "status", "parliament"])
                elif result["content_type"] == "member":
                    assert any(key in metadata for key in ["party", "riding", "active"])
                elif result["content_type"] == "vote":
                    assert any(key in metadata for key in ["result", "yeas", "nays"])
    
    def test_date_range_filtering(self):
        """Test date range filtering with proper date types"""
        response = client.get(
            "/api/v1/search",
            params={
                "q": "test",
                "date__gte": "2023-01-01",
                "date__lte": "2023-12-31"
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify date filters were applied
        assert data["filters_applied"]["date_from"] == "2023-01-01"
        assert data["filters_applied"]["date_to"] == "2023-12-31"
    
    def test_sorting_options(self):
        """Test all sorting options work correctly"""
        for sort in ["relevance", "date", "-date"]:
            response = client.get(
                "/api/v1/search",
                params={"q": "test", "sort": sort}
            )
            assert response.status_code == 200
            data = response.json()
            
            # With real data, we would verify the order
            # For now, just ensure it doesn't error
            assert "results" in data
    
    def test_pagination(self):
        """Test pagination parameters work correctly"""
        # First page
        response = client.get(
            "/api/v1/search",
            params={"q": "test", "page": 1, "page_size": 10}
        )
        assert response.status_code == 200
        data = response.json()
        
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert "total_pages" in data
        assert "total_results" in data
    
    def test_language_preference(self):
        """Test language preference parameter"""
        for lang in ["en", "fr"]:
            response = client.get(
                "/api/v1/search",
                params={"q": "test", "language": lang}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["filters_applied"]["language"] == lang
    
    def test_highlighting_option(self):
        """Test search term highlighting can be toggled"""
        # With highlighting
        response = client.get(
            "/api/v1/search",
            params={"q": "test", "highlight": True}
        )
        assert response.status_code == 200
        
        # Without highlighting  
        response = client.get(
            "/api/v1/search",
            params={"q": "test", "highlight": False}
        )
        assert response.status_code == 200
    
    def test_minimum_query_length(self):
        """Test that minimum query length is enforced"""
        # Too short
        response = client.get("/api/v1/search", params={"q": "a"})
        assert response.status_code == 422  # Validation error
        
        # Exactly minimum
        response = client.get("/api/v1/search", params={"q": "ab"})
        assert response.status_code == 200
    
    def test_search_suggestions_updated(self):
        """Test that search suggestions endpoint uses updated terminology"""
        response = client.get(
            "/api/v1/search/suggestions",
            params={"q": "test"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Suggestions should use "member" not "politician"
        for suggestion in data["suggestions"]:
            assert suggestion["type"] in ["member", "bill", "committee", "vote"]
            assert "politician" not in suggestion["type"]
    
    def test_all_content_type_returns_mixed_results(self):
        """Test that 'all' content type returns results from multiple types"""
        response = client.get(
            "/api/v1/search",
            params={"q": "parliament", "content_type": "all"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Should not paginate when content_type is "all"
        assert data["page"] == 1
        assert data["total_pages"] == 1
        
        # Results should be sorted by relevance
        if len(data["results"]) > 1:
            relevance_scores = [r["relevance_score"] for r in data["results"]]
            assert relevance_scores == sorted(relevance_scores, reverse=True)


class TestSearchContractCompliance:
    """Verify the search endpoint meets all contract requirements"""
    
    def test_response_schema_compliance(self):
        """Test that response matches the expected schema"""
        response = client.get("/api/v1/search", params={"q": "test"})
        assert response.status_code == 200
        data = response.json()
        
        # Required top-level fields
        required_fields = ["query", "total_results", "results", "page", "page_size", "total_pages"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Optional fields that should be present
        assert "filters_applied" in data
    
    def test_backward_compatibility(self):
        """Test that deprecated fields are still available for backward compatibility"""
        response = client.get("/api/v1/search", params={"q": "bill"})
        assert response.status_code == 200
        data = response.json()
        
        # Old fields should still exist in results (even if None)
        for result in data["results"]:
            assert "politician_name" in result  # Deprecated but present
            assert "bill_number" in result      # Deprecated but present
    
    def test_error_responses_consistent(self):
        """Test that error responses follow consistent format"""
        # Missing required parameter
        response = client.get("/api/v1/search")
        assert response.status_code == 422
        error = response.json()
        assert "detail" in error
        
        # Invalid parameter value
        response = client.get(
            "/api/v1/search",
            params={"q": "test", "content_type": "invalid"}
        )
        assert response.status_code == 422
        error = response.json()
        assert "detail" in error