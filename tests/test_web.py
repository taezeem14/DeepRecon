"""Unit tests for Web UI FastAPI endpoints and REST APIs."""

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


def test_api_status():
    client = TestClient(app)
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "metrics" in data
    assert "tor" in data
    assert "ai" in data


def test_api_sessions():
    client = TestClient(app)
    response = client.get("/api/sessions")
    assert response.status_code == 200
    data = response.json()
    assert "sessions" in data
    assert isinstance(data["sessions"], list)


def test_api_tor_renew():
    client = TestClient(app)
    response = client.post("/api/tor/renew")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "tor_ip" in data


def test_api_stop_scan():
    client = TestClient(app)
    response = client.post("/api/scan/1/stop")
    assert response.status_code == 200
    data = response.json()
    assert data.get("success") is True


def test_api_stop_all_scans():
    client = TestClient(app)
    response = client.post("/api/scan/stop")
    assert response.status_code == 200
    data = response.json()
    assert data.get("success") is True


def test_api_session_notes_and_export():
    client = TestClient(app)
    # Start a scan to create a session
    resp = client.post("/api/scan", data={"url": "http://testtarget12345.onion", "session_name": "TEST_SESSION_EXPORT"})
    assert resp.status_code == 200
    sid = resp.json()["session_id"]

    # Test update notes
    patch_resp = client.patch(f"/api/sessions/{sid}/notes", data={"notes": "High value threat target"})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["success"] is True

    # Verify notes persisted in get_session
    get_resp = client.get(f"/api/sessions/{sid}")
    assert get_resp.status_code == 200
    assert get_resp.json()["session"]["notes"] == "High value threat target"

    # Test JSON export
    export_json = client.get(f"/api/sessions/{sid}/export?fmt=json")
    assert export_json.status_code == 200
    assert "session" in export_json.json()

    # Test CSV export
    export_csv = client.get(f"/api/sessions/{sid}/export?fmt=csv")
    assert export_csv.status_code == 200
    assert "text/csv" in export_csv.headers["content-type"]

    # Test Cascade Delete
    del_resp = client.delete(f"/api/sessions/{sid}")
    assert del_resp.status_code == 200
    assert del_resp.json()["success"] is True


def test_api_reports_path_traversal_blocked():
    client = TestClient(app)
    # Test path traversal attempts
    resp1 = client.get("/reports/../../etc/passwd")
    assert resp1.status_code in (400, 404)

    resp2 = client.get("/reports/..%2F..%2Fconfig.py")
    assert resp2.status_code in (400, 404)


def test_api_purge_sessions():
    client = TestClient(app)
    purge_resp = client.delete("/api/sessions/purge")
    assert purge_resp.status_code == 200
    assert purge_resp.json()["success"] is True


