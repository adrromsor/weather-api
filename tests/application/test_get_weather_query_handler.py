import pytest

from src.weather.application.get_weather.get_weather_query import GetWeatherQuery
from src.weather.application.get_weather.get_weather_query_handler import (
    GetWeatherQueryHandler,
)
from src.weather.application.get_weather.get_weather_query_response import (
    GetWeatherQueryResponse,
)
from src.weather.infrastructure.in_memory_weather_repository import (
    InMemoryWeatherRepository,
)


@pytest.mark.asyncio
async def test_should_return_current_weather() -> None:
    repository = InMemoryWeatherRepository()
    handler = GetWeatherQueryHandler(repository=repository)
    query = GetWeatherQuery(location="London")

    result = await handler.execute(query)

    assert result is not None
    assert isinstance(result, GetWeatherQueryResponse)
