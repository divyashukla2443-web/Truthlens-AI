"""
Application configuration for TruthLens AI backend.

Uses pydantic-settings to load and validate configuration from environment
variables (and a local .env file in development). This is the single
source of truth for runtime configuration — no module should read
`os.environ` directly outside of this file.
"""

from functools import lru_cache
from typing import List
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import (
    DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES,
    DEFAULT_API_TITLE,
    DEFAULT_TOKEN_ALGORITHM,
    Environment,
    LogLevel,
)
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    """
    Strongly-typed application settings, populated from environment
    variables. Field names correspond to variables defined in
    `.env.example`.
    """
    model_config = SettingsConfigDict(
    env_file=str(ENV_FILE),
    env_file_encoding="utf-8",
    case_sensitive=True,
    extra="ignore",
)

    # --- Application ---
    APP_NAME: str = DEFAULT_API_TITLE
    APP_ENV: Environment = Environment.DEVELOPMENT
    APP_DEBUG: bool = True
    APP_VERSION: str = "0.1.0"

    # --- Server ---
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # --- Security ---
    SECRET_KEY: str
    ALGORITHM: str = DEFAULT_TOKEN_ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES: int = DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES

    # --- Database ---
    DATABASE_URL: str

    # --- CORS ---
    CORS_ORIGINS: str = ""

    # --- Logging ---
    LOG_LEVEL: LogLevel = LogLevel.INFO

    @property
    def cors_origins_list(self) -> List[str]:
        """Parses the comma-separated CORS_ORIGINS string into a list."""
        if not self.CORS_ORIGINS:
            return []
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        """Convenience flag for production-specific behavior."""
        return self.APP_ENV == Environment.PRODUCTION


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    Using lru_cache ensures environment variables are parsed once per
    process rather than on every access, while remaining easily
    overridable in tests via dependency overrides.
    """
    return Settings()


settings = get_settings()
