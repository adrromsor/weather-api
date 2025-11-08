from fastapi import FastAPI

from src.weather.delivery.api.routers import health, weather


def create_app() -> FastAPI:
    app = FastAPI(title="Weather API")

    app.include_router(health.router)
    app.include_router(weather.router)

    return app


app = create_app()
