from datetime import datetime

from fastapi import status
from fastapi.testclient import TestClient

from src.weather.delivery.api.main import app

client = TestClient(app)


def test_health_router_check_returns_ok():
    response = client.get("/api/health")
    data = response.json()
    timestamp = datetime.fromisoformat(data["timestamp"])

    assert response.status_code == status.HTTP_200_OK
    assert data["status"] == "ok"
    assert isinstance(timestamp, datetime)
