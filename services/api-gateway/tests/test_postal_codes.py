"""
Tests for postal code endpoints.

Verifies:
- RESTful endpoint works correctly
- Old endpoint redirects to new endpoint
- Proper error handling
- Contract adherence
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import httpx

from app.main import app

client = TestClient(app)


class TestPostalCodeEndpoints:
    """Test suite for postal code endpoints - CHK-0302.2 compliance"""
    
    @pytest.fixture
    def mock_represent_response(self):
        """Mock response from Represent Canada API"""
        return {
            "representatives_centroid": [
                {
                    "name": "John Doe",
                    "party_name": "Liberal Party",
                    "district_name": "Test Riding",
                    "elected_office": "MP",
                    "url": "https://example.com/john-doe",
                    "photo_url": "https://example.com/photo.jpg",
                    "email": "john.doe@parl.gc.ca",
                    "offices": [{
                        "tel": "613-555-1234"
                    }],
                    "related": {
                        "boundary_set_name": "Federal electoral districts (House of Commons)"
                    }
                }
            ]
        }
    
    def test_restful_postal_code_endpoint_success(self, mock_represent_response):
        """Test that the RESTful endpoint works correctly"""
        with patch('httpx.Client') as mock_client_class:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_represent_response
            mock_client.get.return_value = mock_response
            mock_client_class.return_value.__enter__.return_value = mock_client
            
            # Test with space in postal code
            response = client.get("/api/v1/postal-codes/K1A 0A6/members")
            assert response.status_code == 200
            data = response.json()
            
            # Verify response structure
            assert "postcode" in data
            assert data["postcode"] == "K1A0A6"  # Should be cleaned
            assert "representatives" in data
            assert len(data["representatives"]) == 1
            assert data["representatives"][0]["name"] == "John Doe"
            assert data["representatives"][0]["party"] == "Liberal Party"
            assert data["total_count"] == 1
            assert data["source"] == "Represent Canada API"
            
            # Verify the correct API was called
            mock_client.get.assert_called_once_with(
                "https://represent.opennorth.ca/postcodes/K1A0A6/"
            )
    
    def test_restful_postal_code_endpoint_without_space(self, mock_represent_response):
        """Test RESTful endpoint with postal code without space"""
        with patch('httpx.Client') as mock_client_class:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_represent_response
            mock_client.get.return_value = mock_response
            mock_client_class.return_value.__enter__.return_value = mock_client
            
            response = client.get("/api/v1/postal-codes/K1A0A6/members")
            assert response.status_code == 200
            data = response.json()
            assert data["postcode"] == "K1A0A6"
    
    def test_deprecated_endpoint_redirects(self):
        """Test that the old non-RESTful endpoint redirects to the new one"""
        # The old endpoint should redirect
        response = client.get(
            "/api/v1/search/postcode/K1A0A6",
            follow_redirects=False  # Don't follow redirects automatically
        )
        
        # Should get a redirect status
        assert response.status_code == 307  # Temporary redirect
        
        # Check redirect location
        assert "location" in response.headers
        assert response.headers["location"] == "/api/v1/postal-codes/K1A0A6/members"
    
    def test_invalid_postal_code_format(self):
        """Test validation of postal code format"""
        # Too short
        response = client.get("/api/v1/postal-codes/K1A/members")
        assert response.status_code == 400
        assert "Invalid postal code format" in response.json()["detail"]
        
        # Too long
        response = client.get("/api/v1/postal-codes/K1A0A6B/members")
        assert response.status_code == 400
        
        # Invalid pattern
        response = client.get("/api/v1/postal-codes/123456/members")
        assert response.status_code == 400
        assert "Canadian format" in response.json()["detail"]
    
    def test_postal_code_not_found(self):
        """Test handling of postal code not found"""
        with patch('httpx.Client') as mock_client_class:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.status_code = 404
            mock_client.get.return_value = mock_response
            mock_client_class.return_value.__enter__.return_value = mock_client
            
            response = client.get("/api/v1/postal-codes/Z9Z9Z9/members")
            assert response.status_code == 404
            assert "No representatives found" in response.json()["detail"]
    
    def test_external_api_timeout(self):
        """Test handling of external API timeout"""
        with patch('httpx.Client') as mock_client_class:
            mock_client = Mock()
            mock_client.get.side_effect = httpx.TimeoutException("Timeout")
            mock_client_class.return_value.__enter__.return_value = mock_client
            
            response = client.get("/api/v1/postal-codes/K1A0A6/members")
            assert response.status_code == 504
            assert "timed out" in response.json()["detail"]
    
    def test_external_api_error(self):
        """Test handling of external API errors"""
        with patch('httpx.Client') as mock_client_class:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.status_code = 500
            mock_client.get.return_value = mock_response
            mock_client_class.return_value.__enter__.return_value = mock_client
            
            response = client.get("/api/v1/postal-codes/K1A0A6/members")
            assert response.status_code == 500
            assert "Error calling Represent API" in response.json()["detail"]
    
    def test_filters_federal_mps_only(self):
        """Test that only federal MPs are returned, not provincial/municipal"""
        mixed_response = {
            "representatives_centroid": [
                {
                    "name": "John Federal",
                    "party_name": "Liberal Party",
                    "district_name": "Test Riding",
                    "elected_office": "MP",
                    "related": {"boundary_set_name": "Federal electoral districts"}
                },
                {
                    "name": "Jane Provincial",
                    "party_name": "PC Party",
                    "district_name": "Provincial Riding",
                    "elected_office": "MPP",
                    "related": {"boundary_set_name": "Provincial electoral districts"}
                },
                {
                    "name": "Bob Municipal",
                    "party_name": "Independent",
                    "district_name": "Ward 5",
                    "elected_office": "Councillor",
                    "related": {"boundary_set_name": "Municipal wards"}
                }
            ]
        }
        
        with patch('httpx.Client') as mock_client_class:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mixed_response
            mock_client.get.return_value = mock_response
            mock_client_class.return_value.__enter__.return_value = mock_client
            
            response = client.get("/api/v1/postal-codes/K1A0A6/members")
            assert response.status_code == 200
            data = response.json()
            
            # Should only have the federal MP
            assert data["total_count"] == 1
            assert len(data["representatives"]) == 1
            assert data["representatives"][0]["name"] == "John Federal"
            assert data["representatives"][0]["level"] == "Federal"


class TestPostalCodeContractCompliance:
    """Verify API contract compliance for CHK-0302.2"""
    
    def test_response_schema_compliance(self):
        """Test that response matches the expected schema"""
        with patch('httpx.Client') as mock_client_class:
            mock_client = Mock()
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "representatives_centroid": [{
                    "name": "Test MP",
                    "party_name": "Test Party",
                    "district_name": "Test District",
                    "elected_office": "MP"
                }]
            }
            mock_client.get.return_value = mock_response
            mock_client_class.return_value.__enter__.return_value = mock_client
            
            response = client.get("/api/v1/postal-codes/K1A0A6/members")
            assert response.status_code == 200
            data = response.json()
            
            # Required fields in response
            required_fields = ["postcode", "representatives", "total_count", "source", "timestamp"]
            for field in required_fields:
                assert field in data, f"Missing required field: {field}"
            
            # Representative structure
            if data["representatives"]:
                rep = data["representatives"][0]
                rep_fields = ["name", "party", "riding", "level", "url", "photo_url", "email", "phone"]
                for field in rep_fields:
                    assert field in rep, f"Missing representative field: {field}"
    
    def test_error_response_format(self):
        """Test that error responses follow consistent format"""
        response = client.get("/api/v1/postal-codes/123/members")
        assert response.status_code == 400
        error = response.json()
        assert "detail" in error
        assert isinstance(error["detail"], str)