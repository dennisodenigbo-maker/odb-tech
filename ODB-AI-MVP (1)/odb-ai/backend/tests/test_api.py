from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_marks_prototype():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["live_cloud"] is False

def test_estimate_formula():
    response = client.post("/api/v1/estimate", json={
        "compute_hours": 100,
        "compute_hourly_usd": 0.2,
        "model_calls": 50000,
        "model_cost_per_1000_calls_usd": 0.1,
        "storage_gb": 50,
        "storage_usd_per_gb_month": 0.02
    })
    assert response.status_code == 200
    data = response.json()
    assert data["components"]["compute"] == 20
    assert data["components"]["model_api"] == 5
    assert data["components"]["storage"] == 1
    assert data["subtotal"] == 26
    assert data["estimate_type"] == "illustrative"
