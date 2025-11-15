import json
import logging

from redis.asyncio import Redis

from src.weather.domain.weather import Weather
from src.weather.domain.weather_repository import WeatherRepository

logger = logging.getLogger(__name__)


class RedisWeatherRepository(WeatherRepository):
    _CACHE_TTL_SECONDS = 10 * 60

    def __init__(self, client: Redis, source_repository: WeatherRepository) -> None:
        self._client = client
        self._source_repository = source_repository

    def _get_client_key(self, location: str) -> str:
        return f"weather:{location.lower().strip()}"

    async def get_weather(self, location: str) -> Weather | None:
        cache_key = self._get_client_key(location)

        try:
            cached = await self._client.get(cache_key)
            if cached:
                return Weather.from_primitives(**json.loads(cached))
        except Exception as e:
            logger.error(f"Redis GET error: {e}")

        weather = await self._source_repository.get_weather(location)

        if weather:
            try:
                await self._client.set(
                    cache_key,
                    json.dumps(weather.to_primitives()),
                    self._CACHE_TTL_SECONDS,
                )
            except Exception as e:
                logger.error(f"Redis SETEX error: {e}")

        return weather
