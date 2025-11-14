from abc import ABC, abstractmethod

from src.weather.domain.weather import Weather


class WeatherRepository(ABC):
    @abstractmethod
    async def get_weather(self, location: str) -> Weather | None:
        raise NotImplementedError
