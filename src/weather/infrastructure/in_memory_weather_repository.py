from typing import override

from src.weather.domain.weather import Weather
from src.weather.domain.weather_repository import WeatherRepository


class InMemoryWeatherRepository(WeatherRepository):
    @override
    async def get_weather(self, location: str) -> Weather | None:
        return Weather.from_primitives(
            location=location,
            temperature=17.7,
            condition="cloudy",
            last_updated="2025-11-08T19:49:10",
        )
