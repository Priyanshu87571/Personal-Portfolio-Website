from fastapi.testclient import TestClient
from app.main import app

def test_health_endpoint_exists():
    # Database-backed smoke tests require the app's configured database.
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

def test_profile_has_expected_identity():
    with TestClient(app) as client:
        response = client.get("/api/profile")
        assert response.status_code == 200
        assert response.json()["name"] == "Priyanshu Raj"
