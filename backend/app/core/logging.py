"""Structured logging with sensitive-field redaction."""

import logging
import sys
from typing import Any, cast

import structlog
from structlog.types import EventDict, Processor

from app.core.config import Settings

SENSITIVE_FIELD_PARTS = frozenset(
    {"authorization", "cookie", "database_url", "password", "secret", "token"}
)


def redact_sensitive_values(
    _logger: Any, _method_name: str, event_dict: EventDict
) -> EventDict:
    """Replace values for log fields that may contain credentials."""
    for key in tuple(event_dict):
        normalized_key = str(key).casefold()
        if any(part in normalized_key for part in SENSITIVE_FIELD_PARTS):
            event_dict[key] = "[redacted]"
    return event_dict


def configure_logging(settings: Settings) -> None:
    """Configure standard-library and structlog JSON output."""
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=settings.log_level,
        force=True,
    )

    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        redact_sensitive_values,
        structlog.processors.JSONRenderer(),
    ]
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelNamesMapping()[settings.log_level]
        ),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger() -> structlog.stdlib.BoundLogger:
    """Return a configured application logger."""
    return cast(structlog.stdlib.BoundLogger, structlog.get_logger())
