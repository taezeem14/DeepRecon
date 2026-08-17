"""Unit tests for Web UI FastAPI endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient
from web.app import app


def test_web_index():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "DeepRecon" in response.text
    assert "Indexed Pages" in response.text


def test_web_search():
    client = TestClient(app)
    response = client.get("/search?q=test")
    assert response.status_code == 200
    assert "DeepRecon Search" in response.text
