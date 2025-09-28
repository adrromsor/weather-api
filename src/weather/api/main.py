from fastapi import FastAPI
from src.weather.api.routers import health


def create_app() -> FastAPI:
    app = FastAPI(title="Weather API")

    app.include_router(health.router)

    return app


app = create_app()
