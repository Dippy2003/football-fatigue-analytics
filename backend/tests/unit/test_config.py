"""Tests for application settings safeguards."""

import pytest
from pydantic import ValidationError
from pytest import MonkeyPatch

from app.core.config import Settings


def test_settings_have_safe_local_defaults() -> None:
    settings = Settings()

    assert settings.database_url.startswith("sqlite:///")
    assert settings.enable_uploads is False
    assert settings.cors_allowed_origins == ["http://localhost:5173"]
    assert settings.is_production is False


def test_settings_parse_environment_values(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("ENABLE_UPLOADS", "false")
    monkeypatch.setenv("CORS_ALLOWED_ORIGINS", '["https://playerpulse.example"]')

    settings = Settings()

    assert settings.is_production is True
    assert settings.enable_uploads is False
    assert settings.cors_allowed_origins == ["https://playerpulse.example"]


@pytest.mark.parametrize(
    "origin", ["*", "http://playerpulse.example", "http://localhost:5173"]
)
def test_production_rejects_unsafe_cors_origins(origin: str) -> None:
    with pytest.raises(ValidationError, match="explicit HTTPS"):
        Settings(app_env="production", cors_allowed_origins=[origin])
