"""FastAPI application entry point."""

from fastapi import FastAPI

from app import __version__


def create_app() -> FastAPI:
    """Create an isolated PlayerPulse application instance."""
    return FastAPI(
        title="PlayerPulse API",
        summary="Explainable football workload and performance indicators",
        description=(
            "Performance analytics decision support. PlayerPulse is not a medical "
            "diagnostic tool."
        ),
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/api/v1/openapi.json",
    )


app = create_app()
