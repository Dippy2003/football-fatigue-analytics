"""Operational system endpoints."""

from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["system"])


class HealthResponse(BaseModel):
    """Liveness response returned without checking dependencies."""

    status: Literal["ok"]


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check API liveness",
)
def health() -> HealthResponse:
    """Return success when the process can serve HTTP requests."""
    return HealthResponse(status="ok")

