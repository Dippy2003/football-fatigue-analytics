"""Tests for application settings safeguards."""

from app.core.config import Settings
from pytest import MonkeyPatch


def test_settings_have_safe_local_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.database_url.startswith("sqlite:///")
    assert settings.enable_uploads is False
    assert settings.cors_allowed_origins == ["http://localhost:5173"]
    assert settings.is_production is False


def test_settings_parse_environment_values(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("ENABLE_UPLOADS", "false")
    monkeypatch.setenv("CORS_ALLOWED_ORIGINS", '["https://playerpulse.example"]')

    settings = Settings(_env_file=None)

    assert settings.is_production is True
    assert settings.enable_uploads is False
    assert settings.cors_allowed_origins == ["https://playerpulse.example"]
