import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ─── Auth helpers ────────────────────────────────────────────────────────────

def get_auth_token():
    # Try register, ignore if already exists
    client.post(
        "/api/v1/auth/register",
        json={"email": "testuser@sentinelpy.com", "password": "testpass123"}
    )
    # Always login
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "testuser@sentinelpy.com", "password": "testpass123"}
    )
    return response.json()["access_token"]

def auth_headers():
    token = get_auth_token()
    return {"Authorization": f"Bearer {token}"}

# ─── Health check ─────────────────────────────────────────────────────────────

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_scan_status():
    response = client.get("/api/v1/scan/status")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"

# ─── Auth tests ───────────────────────────────────────────────────────────────
def test_register():
    import time
    response = client.post(
        "/api/v1/auth/register",
        json={"email": f"newuser_{int(time.time())}@test.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_register_duplicate_email():
    client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@test.com", "password": "password123"}
    )
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@test.com", "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_success():
    client.post(
        "/api/v1/auth/register",
        json={"email": "login@test.com", "password": "password123"}
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@test.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@test.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401

# ─── Scan tests ───────────────────────────────────────────────────────────────

def test_start_scan_unauthenticated():
    response = client.post(
        "/api/v1/scan/start",
        json={"target": "192.168.1.1", "ports": [22, 80, 443]}
    )
    assert response.status_code == 401

def test_start_scan_authenticated():
    response = client.post(
        "/api/v1/scan/start",
        json={"target": "192.168.1.1", "ports": [22, 80, 443]},
        headers=auth_headers()
    )
    assert response.status_code == 200
    assert "scan_id" in response.json()
    assert response.json()["target"] == "192.168.1.1"

def test_start_scan_invalid_data():
    response = client.post(
        "/api/v1/scan/start",
        json={"target": "192.168.1.1", "ports": "invalid"},
        headers=auth_headers()
    )
    assert response.status_code == 422

def test_get_scan_history_authenticated():
    response = client.get(
        "/api/v1/scan/history",
        headers=auth_headers()
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_scan_history_unauthenticated():
    response = client.get("/api/v1/scan/history")
    assert response.status_code == 401

def test_get_scan_not_found():
    response = client.get(
        "/api/v1/scan/99999",
        headers=auth_headers()
    )
    assert response.status_code == 404

def test_scan_history_pagination():
    response = client.get(
        "/api/v1/scan/history?limit=2&skip=0",
        headers=auth_headers()
    )
    assert response.status_code == 200
    assert len(response.json()) <= 2

def test_scan_history_invalid_limit():
    response = client.get(
        "/api/v1/scan/history?limit=999",
        headers=auth_headers()
    )
    assert response.status_code == 422