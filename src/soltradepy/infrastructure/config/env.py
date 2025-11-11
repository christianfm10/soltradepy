# Settings: .env loader for configuration settings
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings loaded from environment variables or .env file."""

    moralis_api_key: str
    helius_api_key: str
    database_url: str
    debug_sql: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
    )


@lru_cache
def get_settings() -> Settings:
    """Retrieve the application settings."""
    return Settings()  # type: ignore
