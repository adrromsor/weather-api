from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.shared.redis_client import get_redis_client
from src.weather.application.get_weather.get_weather_query import GetWeatherQuery
from src.weather.application.get_weather.get_weather_query_handler import (
    GetWeatherQueryHandler,
)
from src.weather.domain.weather_location_not_found_error import (
    WeatherLocationNotFoundError,
)
from src.weather.infrastructure.redis_weather_repository import RedisWeatherRepository
from src.weather.infrastructure.visual_crossing_weather_repository import (
    VisualCrossingWeatherRepository,
)

router = APIRouter(prefix="/api", tags=["Weather"])

weather_repository = RedisWeatherRepository(
    client=get_redis_client(), source_repository=VisualCrossingWeatherRepository()
)


class WeatherResponse(BaseModel):
    location: str
    temperature: float
    condition: str
    last_updated: str


def get_weather_query_handler() -> GetWeatherQueryHandler:
    return GetWeatherQueryHandler(weather_repository)


@router.get("/weather/{location}", status_code=status.HTTP_200_OK)
async def get_weather(
    location: str,
    handler: GetWeatherQueryHandler = Depends(get_weather_query_handler),
) -> WeatherResponse:
    query = GetWeatherQuery(location)

    try:
        result = await handler.execute(query)
    except WeatherLocationNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))

    return WeatherResponse(
        location=result.location,
        temperature=result.temperature,
        condition=result.condition,
        last_updated=result.last_updated,
    )
