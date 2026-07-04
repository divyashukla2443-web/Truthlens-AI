"""
Application entrypoint for TruthLens AI backend.

Creates and configures the FastAPI application instance: logging,
CORS, global exception handling, and router registration.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.constants import API_V1_PREFIX
from app.core.exceptions import AppException
from app.core.logging import configure_logging, logger


def create_application() -> FastAPI:
    """
    Application factory.

    Using a factory (rather than a module-level `app = FastAPI()` only)
    makes the app easy to instantiate multiple times in tests with
    different configuration/overrides.
    """
    configure_logging()

    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.APP_DEBUG,
    )

    # --- CORS ---
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Global exception handler for all AppException subclasses ---
    @application.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
        logger.error(
            f"AppException: {exc.message} | path={request.url.path} | status={exc.status_code}"
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.message,
                "details": exc.details,
            },
        )

    # --- Fallback handler for unhandled exceptions ---
    @application.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(f"Unhandled exception at path={request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "An unexpected internal error occurred."},
        )

    # --- Health check endpoint (foundation-level, no business logic) ---
    @application.get("/health", tags=["System"])
    async def health_check() -> dict:
        """Basic liveness probe for load balancers / container orchestration."""
        return {
            "status": "ok",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV.value,
        }

    # --- Versioned API routes ---
    application.include_router(api_router, prefix=API_V1_PREFIX)

    logger.info(f"{settings.APP_NAME} v{settings.APP_VERSION} application created.")
    return application


app = create_application()
