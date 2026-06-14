import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_scan_status():
    response = client.get("/api/v1/scan/status")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"

def test_start_scan():
    response = client.post(
        "/api/v1/scan/start",
        json={"target": "192.168.1.1", "ports": [22, 80, 443]}
    )
    assert response.status_code == 200
    assert response.json()["target"] == "192.168.1.1"
    assert "scan_id" in response.json()

def test_start_scan_invalid_data():
    response = client.post(
        "/api/v1/scan/start",
        json={"target": "192.168.1.1", "ports": "invalid"}
    )
    assert response.status_code == 422

def test_get_scan_not_found():
    response = client.get("/api/v1/scan/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Scan not found"

def test_get_scan_history():
    response = client.get("/api/v1/scan/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_scan_history_pagination():
    response = client.get("/api/v1/scan/history?limit=2&skip=0")
    assert response.status_code == 200
    assert len(response.json()) <= 2

def test_scan_history_invalid_limit():
    response = client.get("/api/v1/scan/history?limit=999")
    assert response.status_code == 422