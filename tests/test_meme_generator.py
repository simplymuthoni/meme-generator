"""
Tests for the meme generator API
"""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path

from app.main import app
from app.services.meme_service import meme_service

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns API info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert data["status"] == "running"


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "ai_configured" in data


def test_get_templates():
    """Test retrieving available templates"""
    response = client.get("/api/meme/templates")
    assert response.status_code == 200
    data = response.json()
    assert "templates" in data
    assert "count" in data
    assert isinstance(data["templates"], list)


def test_generate_meme_missing_template():
    """Test meme generation with non-existent template"""
    payload = {
        "template_name": "nonexistent_template",
        "top_text": "Test Text",
        "bottom_text": "More Test Text"
    }
    response = client.post("/api/meme/generate", json=payload)
    assert response.status_code == 400


def test_generate_meme_validation():
    """Test request validation"""
    # Missing required field
    payload = {
        "bottom_text": "Test"
    }
    response = client.post("/api/meme/generate", json=payload)
    assert response.status_code == 422  # Validation error


def test_meme_service_get_templates():
    """Test meme service template listing"""
    templates = meme_service.get_available_templates()
    assert isinstance(templates, list)


def test_meme_service_generate_invalid_template():
    """Test meme service with invalid template"""
    success, message, path = meme_service.generate_meme(
        template_name="invalid_template_xyz",
        top_text="Test",
        bottom_text="Test"
    )
    assert not success
    assert "not found" in message.lower()
    assert path is None


# Integration test (requires template files)
@pytest.mark.skipif(
    not Path("app/static/templates").exists() or 
    not list(Path("app/static/templates").glob("*")),
    reason="No template files available"
)
def test_generate_meme_with_template():
    """Test actual meme generation if templates exist"""
    templates = meme_service.get_available_templates()
    if templates:
        template = templates[0]
        payload = {
            "template_name": template,
            "top_text": "Test Top Text",
            "bottom_text": "Test Bottom Text"
        }
        response = client.post("/api/meme/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "meme_url" in data
