"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.routes.datasets import router as dataset_router
from app.api.routes.system import router as system_router
from app.core.config import Settings, get_settings
from app.core.logging import configure_logging


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create an isolated PlayerPulse application instance."""
    resolved_settings = settings or get_settings()
    configure_logging(resolved_settings)
    application = FastAPI(
        title="PlayerPulse API",
        summary="Explainable football workload and performance indicators",
        description=(
            "Performance analytics decision support. PlayerPulse is not a medical "
            "diagnostic tool."
        ),
        version=resolved_settings.app_version or __version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/api/v1/openapi.json",
    )
    application.state.settings = resolved_settings
    application.add_middleware(
        CORSMiddleware,
        allow_origins=resolved_settings.cors_allowed_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Accept", "Authorization", "Content-Type", "X-Request-ID"],
    )
    application.include_router(system_router)
    application.include_router(dataset_router)
    return application


app = create_app()
