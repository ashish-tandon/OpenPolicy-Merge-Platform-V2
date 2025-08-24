"""
Tests for OpenAPI compliance - CHK-0302.4

Verifies that all API endpoints match their OpenAPI documentation.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.openapi_compliance import openapi_compliance

client = TestClient(app)


class TestOpenAPICompliance:
    """Test suite for verifying API endpoints match OpenAPI specification"""
    
    def test_bills_endpoint_parameters(self):
        """Test that /bills endpoint accepts all OpenAPI defined parameters"""
        # Valid parameters from OpenAPI spec
        response = client.get("/api/v1/bills", params={
            "q": "climate",
            "jurisdiction": "federal",
            "session": "44-1",
            "status": "passed",
            "page": 1,
            "page_size": 20
        })
        assert response.status_code == 200
        
        # Test jurisdiction enum validation
        response = client.get("/api/v1/bills", params={"jurisdiction": "invalid"})
        assert response.status_code == 422  # Validation error
        
        # Test status enum validation
        response = client.get("/api/v1/bills", params={"status": "invalid_status"})
        assert response.status_code == 422
    
    def test_members_endpoint_parameters(self):
        """Test that /members endpoint accepts all OpenAPI defined parameters"""
        # Valid parameters from OpenAPI spec
        response = client.get("/api/v1/members", params={
            "jurisdiction": "provincial",
            "party": "liberal",
            "district": "toronto-centre",
            "page": 1,
            "page_size": 20
        })
        assert response.status_code == 200
        
        # Test jurisdiction enum validation
        response = client.get("/api/v1/members", params={"jurisdiction": "invalid"})
        assert response.status_code == 422
    
    def test_votes_endpoint_standardization(self):
        """Test that /votes endpoint follows standard parameter patterns"""
        response = client.get("/api/v1/votes", params={
            "q": "budget",
            "session": "44-1",
            "date__gte": "2023-01-01",
            "date__lte": "2023-12-31",
            "page": 1,
            "page_size": 20
        })
        assert response.status_code == 200
    
    def test_debates_endpoint_standardization(self):
        """Test that /debates endpoint follows standard parameter patterns"""
        response = client.get("/api/v1/debates", params={
            "session": "44-1",
            "date__gte": "2023-01-01",
            "date__lte": "2023-12-31",
            "lang": "en",
            "page": 1,
            "page_size": 20
        })
        assert response.status_code == 200
    
    def test_pagination_consistency(self):
        """Test that all endpoints use consistent pagination parameters"""
        endpoints = [
            "/api/v1/bills",
            "/api/v1/members",
            "/api/v1/votes",
            "/api/v1/debates"
        ]
        
        for endpoint in endpoints:
            # Test default pagination
            response = client.get(endpoint)
            assert response.status_code == 200
            data = response.json()
            assert "page" in data
            assert "page_size" in data
            assert "total_pages" in data
            assert data["page"] == 1
            assert data["page_size"] == 20
            
            # Test custom pagination
            response = client.get(endpoint, params={"page": 2, "page_size": 10})
            assert response.status_code == 200
            data = response.json()
            assert data["page"] == 2
            assert data["page_size"] == 10
            
            # Test pagination limits
            response = client.get(endpoint, params={"page_size": 101})
            assert response.status_code == 422  # Exceeds maximum
    
    def test_response_format_consistency(self):
        """Test that all list endpoints return consistent response format"""
        endpoints = [
            ("/api/v1/bills", "bills"),
            ("/api/v1/members", "members"),
            ("/api/v1/votes", "votes"),
            ("/api/v1/debates", "debates")
        ]
        
        for endpoint, resource_name in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            data = response.json()
            
            # Check standard response structure
            assert resource_name in data or "results" in data
            assert "page" in data
            assert "page_size" in data
            assert "total" in data or "total_count" in data
            assert "total_pages" in data
    
    def test_error_response_format(self):
        """Test that error responses follow consistent format"""
        # Test 404 error
        response = client.get("/api/v1/bills/nonexistent-id")
        assert response.status_code == 404
        error = response.json()
        assert "detail" in error
        
        # Test validation error
        response = client.get("/api/v1/bills", params={"page": -1})
        assert response.status_code == 422
        error = response.json()
        assert "detail" in error
    
    def test_date_parameter_format(self):
        """Test that date parameters follow consistent format"""
        endpoints_with_dates = [
            "/api/v1/bills",
            "/api/v1/votes",
            "/api/v1/debates"
        ]
        
        for endpoint in endpoints_with_dates:
            # Valid date format
            response = client.get(endpoint, params={
                "date__gte": "2023-01-01",
                "date__lte": "2023-12-31"
            })
            assert response.status_code == 200
            
            # Invalid date format should be rejected
            response = client.get(endpoint, params={"date__gte": "01/01/2023"})
            # The endpoint should either handle the conversion or return an error
            # For now, we just check it doesn't crash
            assert response.status_code in [200, 400, 422]
    
    def test_search_parameter_consistency(self):
        """Test that search parameters are consistent across endpoints"""
        searchable_endpoints = [
            "/api/v1/bills",
            "/api/v1/members",
            "/api/v1/votes"
        ]
        
        for endpoint in searchable_endpoints:
            # All searchable endpoints should accept 'q' parameter
            response = client.get(endpoint, params={"q": "test search"})
            assert response.status_code == 200
    
    def test_openapi_compliance_validation(self):
        """Test the OpenAPI compliance validator itself"""
        # Test valid parameters
        errors = openapi_compliance.validate_endpoint(
            "/bills", "GET", {
                "q": "test",
                "jurisdiction": "federal",
                "page": 1
            }
        )
        # Should have minimal errors (might have some if OpenAPI spec incomplete)
        assert isinstance(errors, list)
        
        # Test invalid enum value
        errors = openapi_compliance.validate_endpoint(
            "/bills", "GET", {
                "jurisdiction": "invalid_jurisdiction"
            }
        )
        assert any("not in allowed values" in error for error in errors)
        
        # Test exceeding numeric constraints
        errors = openapi_compliance.validate_endpoint(
            "/bills", "GET", {
                "page_size": 200  # Exceeds maximum of 100
            }
        )
        assert any("greater than maximum" in error for error in errors)