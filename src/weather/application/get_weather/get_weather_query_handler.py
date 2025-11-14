from src.weather.application.get_weather.get_weather_query import GetWeatherQuery
from src.weather.application.get_weather.get_weather_query_response import (
    GetWeatherQueryResponse,
)
from src.weather.domain.weather_location_not_found_error import (
    WeatherLocationNotFoundError,
)
from src.weather.domain.weather_repository import WeatherRepository


class GetWeatherQueryHandler:
    def __init__(self, repository: WeatherRepository) -> None:
        self._repository = repository

    async def execute(self, query: GetWeatherQuery) -> GetWeatherQueryResponse:
        result = await self._repository.get_weather(location=query.location)
        if result is None:
            raise WeatherLocationNotFoundError(query.location)
        return GetWeatherQueryResponse(
            location=result.location,
            temperature=result.temperature,
            condition=result.condition,
            last_updated=result.last_updated,
        )
