"""FastAPI application entry point."""

from fastapi import FastAPI

from app import __version__
from app.api.routes.system import router as system_router


def create_app() -> FastAPI:
    """Create an isolated PlayerPulse application instance."""
    application = FastAPI(
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
    application.include_router(system_router)
    return application


app = create_app()
