from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.weather.application.get_weather.get_weather_query import GetWeatherQuery
from src.weather.application.get_weather.get_weather_query_handler import (
    GetWeatherQueryHandler,
)
from src.weather.infrastructure.in_memory_weather_repository import (
    InMemoryWeatherRepository,
)

router = APIRouter(prefix="/api", tags=["Weather"])
weather_repository = InMemoryWeatherRepository()


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
    result = await handler.execute(query)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Weather report not found for location: {location}",
        )

    return WeatherResponse(
        location=result.location,
        temperature=result.temperature,
        condition=result.condition,
        last_updated=result.last_updated,
    )
