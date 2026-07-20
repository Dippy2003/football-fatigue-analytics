"""Typed environment configuration."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_env: Literal["development", "test", "production"] = "development"
    app_version: str = "0.1.0"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    database_url: str = "sqlite:///./playerpulse.db"
    cors_allowed_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173"]
    )
    enable_uploads: bool = False
    max_upload_mb: int = Field(default=25, ge=1, le=100)
    max_import_files: int = Field(default=5, ge=1, le=20)
    max_import_rows: int = Field(default=2_000_000, ge=1, le=10_000_000)
    processing_concurrency: int = Field(default=1, ge=1, le=4)
    data_root: Path = Path("../data")
    model_root: Path = Path("../models")
    synthetic_seed: int = 20_260_720

    @property
    def is_production(self) -> bool:
        """Return whether production safeguards should apply."""
        return self.app_env == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide immutable settings snapshot."""
    return Settings()
