from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    VISUAL_CROSSING_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )


settings = Settings()
