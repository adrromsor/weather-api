from fastapi import status
from fastapi.testclient import TestClient

from src.weather.delivery.api.main import app

client = TestClient(app)


def test_weather_router() -> None:
    location = "london"

    with TestClient(app) as client:
        response = client.get(f"/api/weather/{location}")
        data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert data["location"] == location
        assert "temperature" in data
        assert isinstance(data["temperature"], float)
        assert "condition" in data
        assert "last_updated" in data
