from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel

from src.weather.application.get_weather.get_weather_query import GetWeatherQuery
from src.weather.application.get_weather.get_weather_query_handler import (
    GetWeatherQueryHandler,
)
from src.weather.domain.weather_location_not_found_error import (
    WeatherLocationNotFoundError,
)
from src.weather.domain.weather_repository import WeatherRepository

router = APIRouter(prefix="/api", tags=["Weather"])


class WeatherResponse(BaseModel):
    location: str
    temperature: float
    condition: str
    last_updated: str


def get_weather_repository(request: Request) -> WeatherRepository:
    return request.app.state.weather_repository


def get_weather_query_handler(
    repository: WeatherRepository = Depends(get_weather_repository),
) -> GetWeatherQueryHandler:
    return GetWeatherQueryHandler(repository)


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
