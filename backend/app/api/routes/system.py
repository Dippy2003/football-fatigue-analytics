"""Operational system endpoints."""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from app import __version__

router = APIRouter(prefix="/api/v1", tags=["system"])


class HealthResponse(BaseModel):
    """Liveness response returned without checking dependencies."""

    status: Literal["ok"]


class ReadinessResponse(BaseModel):
    """Dependency readiness state."""

    status: Literal["ready"]
    checks: dict[str, Literal["ok"]]


class VersionResponse(BaseModel):
    """Public build identity."""

    name: Literal["PlayerPulse API"]
    version: str
    api_version: Literal["v1"]


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check API liveness",
)
def health() -> HealthResponse:
    """Return success when the process can serve HTTP requests."""
    return HealthResponse(status="ok")


@router.get(
    "/readiness",
    response_model=ReadinessResponse,
    summary="Check service readiness",
)
def readiness() -> ReadinessResponse:
    """Report dependencies required by the Day 1 application shell."""
    return ReadinessResponse(status="ready", checks={"application": "ok"})


@router.get(
    "/version",
    response_model=VersionResponse,
    summary="Read build version",
)
def version() -> VersionResponse:
    """Expose a safe public application version."""
    return VersionResponse(
        name="PlayerPulse API",
        version=__version__,
        api_version="v1",
    )
