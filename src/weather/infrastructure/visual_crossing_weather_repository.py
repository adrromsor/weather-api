import logging
from datetime import datetime, timezone
from typing import Any

from httpx import AsyncClient, AsyncHTTPTransport, HTTPError

from src.config import settings
from src.weather.domain.weather import Weather
from src.weather.domain.weather_location_not_found_error import (
    WeatherLocationNotFoundError,
)
from src.weather.domain.weather_repository import WeatherRepository

logger = logging.getLogger(__name__)


class VisualCrossingWeatherRepository(WeatherRepository):
    def __init__(
        self,
        api_key: str = settings.VISUAL_CROSSING_API_KEY,
        base_url: str = settings.VISUAL_CROSSING_BASE_URL,
    ):
        self._api_key = api_key
        self._base_url = base_url
        self._transport = AsyncHTTPTransport(retries=3)

    async def get_weather(self, location: str) -> Weather | None:
        if not self._api_key:
            logger.warning("No Visual Crossing API key provided.")
            return None
        try:
            async with AsyncClient(
                base_url=self._base_url, transport=self._transport, timeout=10.0
            ) as client:
                response = await client.get(
                    f"/{location}",
                    params={
                        "unitGroup": "metric",
                        "key": self._api_key,
                        "contentType": "json",
                    },
                )

                if response.status_code in (400, 404):
                    raise WeatherLocationNotFoundError(location)

                response.raise_for_status()
                data = response.json()

                return self._map_to_domain(data)

        except HTTPError as e:
            logger.error(f"HTTP error communicating with Visual Crossing: {e}")
            raise
        except WeatherLocationNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    def _map_to_domain(self, data: dict[str, Any]) -> Weather | None:
        current = data.get("currentConditions", {})
        epoch_time = current.get("datetimeEpoch", 0)
        dt = datetime.fromtimestamp(epoch_time, tz=timezone.utc)
        last_updated = dt.strftime("%Y-%m-%d %H:%M:%S")

        return Weather.from_primitives(
            location=str(data.get("resolvedAddress", data.get("address"))),
            temperature=current.get("temp"),
            condition=current.get("conditions", "Unknown"),
            last_updated=last_updated,
        )
