# Settings: .env loader for configuration settings
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings loaded from environment variables or .env file."""

    moralis_api_key: str
    database_url: str
    debug_sql: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()
