from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    VISUAL_CROSSING_API_KEY: str = ""
    VISUAL_CROSSING_BASE_URL: str = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )


settings = Settings()
