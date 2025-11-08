from abc import ABC, abstractmethod


class WeatherRepository(ABC):
    @abstractmethod
    async def get_weather(self, location: str):
        raise NotImplementedError
