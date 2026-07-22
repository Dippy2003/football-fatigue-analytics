"""Standard safe API error responses and request identifiers."""

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response


async def request_id_middleware(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    """Attach a bounded caller or generated request ID to every response."""
    supplied = request.headers.get("X-Request-ID", "")
    request_id = supplied if 0 < len(supplied) <= 100 else str(uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


def _body(
    request: Request, *, code: str, message: str, details: object
) -> dict[str, object]:
    return {
        "code": code,
        "message": message,
        "details": details,
        "request_id": request.state.request_id,
        "timestamp": datetime.now(UTC).isoformat(),
    }


async def http_exception_handler(request: Request, error: Exception) -> JSONResponse:
    """Convert deliberate HTTP errors to the public error contract."""
    if not isinstance(error, HTTPException):
        raise error
    message = str(error.detail) if isinstance(error.detail, str) else "Request failed."
    return JSONResponse(
        status_code=error.status_code,
        content=_body(
            request,
            code=f"http_{error.status_code}",
            message=message,
            details=None if isinstance(error.detail, str) else error.detail,
        ),
        headers=error.headers,
    )


async def validation_exception_handler(
    request: Request, error: Exception
) -> JSONResponse:
    """Return bounded field validation details without a stack trace."""
    if not isinstance(error, RequestValidationError):
        raise error
    details = [
        {"location": list(item["loc"]), "message": item["msg"], "type": item["type"]}
        for item in error.errors()
    ]
    return JSONResponse(
        status_code=422,
        content=_body(
            request,
            code="validation_error",
            message="Request validation failed.",
            details=details,
        ),
    )
