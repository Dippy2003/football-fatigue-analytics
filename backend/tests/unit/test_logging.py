"""Tests for safe structured logging."""

from app.core.logging import redact_sensitive_values


def test_sensitive_log_fields_are_redacted() -> None:
    event = {
        "event": "configuration_loaded",
        "database_url": "postgresql://user:password@example.test/db",
        "access_token": "private-token",
        "request_id": "safe-request-id",
    }

    redacted = redact_sensitive_values(None, "info", event)

    assert redacted["database_url"] == "[redacted]"
    assert redacted["access_token"] == "[redacted]"
    assert redacted["request_id"] == "safe-request-id"
