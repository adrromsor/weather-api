from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from src.shared.redis_client import get_redis_client
from src.weather.delivery.api.routers import health, weather
from src.weather.infrastructure.redis_weather_repository import RedisWeatherRepository
from src.weather.infrastructure.visual_crossing_weather_repository import (
    VisualCrossingWeatherRepository,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = get_redis_client()
    visual_crossing_repo = VisualCrossingWeatherRepository()
    caching_repo = RedisWeatherRepository(
        client=redis_client, source_repository=visual_crossing_repo
    )

    app.state.redis_client = redis_client
    app.state.weather_repository = caching_repo

    yield

    await app.state.redis_client.close()


def create_app() -> FastAPI:
    app = FastAPI(title="Weather API", lifespan=lifespan)

    app.include_router(health.router)
    app.include_router(weather.router)

    return app


app = create_app()
