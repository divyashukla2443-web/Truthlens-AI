"""
Centralized logging configuration for TruthLens AI backend.

Uses loguru for structured, readable logging in development and
JSON-friendly output in production. Configured once at application
startup via `configure_logging()`.
"""

import sys

from loguru import logger

from app.core.config import settings
from app.core.constants import Environment


def configure_logging() -> None:
    """
    Configures the global loguru logger based on current settings.

    - Development: human-readable, colorized console output.
    - Production/Staging: structured (serialized) output suitable for
      log aggregation systems (e.g. ELK, CloudWatch, Datadog).
    """
    logger.remove()  # Remove default handler to avoid duplicate logs

    if settings.APP_ENV == Environment.PRODUCTION or settings.APP_ENV == Environment.STAGING:
        logger.add(
            sys.stdout,
            level=settings.LOG_LEVEL.value,
            serialize=True,
            backtrace=False,
            diagnose=False,
        )
    else:
        logger.add(
            sys.stdout,
            level=settings.LOG_LEVEL.value,
            colorize=True,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
                "- <level>{message}</level>"
            ),
            backtrace=True,
            diagnose=settings.APP_DEBUG,
        )

    logger.info(f"Logging configured for environment: {settings.APP_ENV.value}")


__all__ = ["logger", "configure_logging"]
