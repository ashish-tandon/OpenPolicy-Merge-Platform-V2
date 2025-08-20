"""
Tests for health and version endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from app.main import app

client = TestClient(app)


def test_healthz():
    """Test health check endpoint."""
    response = client.get("/healthz")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert data["version"] == "0.1.0"
    assert "environment" in data
    assert "database" in data
    
    # Verify timestamp is valid ISO format
    timestamp = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
    assert isinstance(timestamp, datetime)


def test_version():
    """Test version endpoint."""
    response = client.get("/version")
    assert response.status_code == 200
    
    data = response.json()
    assert data["version"] == "0.1.0"
    assert "build_date" in data
    assert "git_commit" in data
    assert "environment" in data
    
    # Verify build_date is valid ISO format
    build_date = datetime.fromisoformat(data["build_date"].replace("Z", "+00:00"))
    assert isinstance(build_date, datetime)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "Welcome to OpenPolicy API"
    assert data["version"] == "0.1.0"
    assert data["docs"] == "/docs"
    assert data["health"] == "/healthz"


def test_healthz_response_structure():
    """Test health endpoint response structure."""
    response = client.get("/healthz")
    data = response.json()
    
    required_fields = ["status", "timestamp", "version", "environment", "database"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"


def test_version_response_structure():
    """Test version endpoint response structure."""
    response = client.get("/version")
    data = response.json()
    
    required_fields = ["version", "build_date", "git_commit", "environment"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    assert data["version"] == "0.1.0"
    assert data["git_commit"] in ["unknown", "development"]  # Allow for different environments
