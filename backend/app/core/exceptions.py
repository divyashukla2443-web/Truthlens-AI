"""
Centralized custom exception hierarchy for TruthLens AI backend.

All application-specific exceptions should inherit from `AppException`
so they can be caught and translated into consistent HTTP responses by
a single global exception handler (wired up in `app/main.py`).
"""

from typing import Any, Optional


class AppException(Exception):
    """
    Base class for all application-specific exceptions.

    Attributes:
        message: Human-readable error description.
        status_code: HTTP status code to return to the client.
        details: Optional additional context for debugging or client use.
    """

    def __init__(
        self,
        message: str = "An unexpected error occurred.",
        status_code: int = 500,
        details: Optional[Any] = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class NotFoundException(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str = "Resource not found.", details: Optional[Any] = None) -> None:
        super().__init__(message=message, status_code=404, details=details)


class UnauthorizedException(AppException):
    """Raised when authentication is missing or invalid."""

    def __init__(self, message: str = "Authentication required.", details: Optional[Any] = None) -> None:
        super().__init__(message=message, status_code=401, details=details)


class ForbiddenException(AppException):
    """Raised when an authenticated user lacks permission for an action."""

    def __init__(self, message: str = "You do not have permission to perform this action.", details: Optional[Any] = None) -> None:
        super().__init__(message=message, status_code=403, details=details)


class ValidationException(AppException):
    """Raised when input data fails business-level validation."""

    def __init__(self, message: str = "Validation failed.", details: Optional[Any] = None) -> None:
        super().__init__(message=message, status_code=422, details=details)


class ConflictException(AppException):
    """Raised when a request conflicts with the current state of a resource."""

    def __init__(self, message: str = "Resource conflict.", details: Optional[Any] = None) -> None:
        super().__init__(message=message, status_code=409, details=details)


class DatabaseException(AppException):
    """Raised when a database operation fails unexpectedly."""

    def __init__(self, message: str = "A database error occurred.", details: Optional[Any] = None) -> None:
        super().__init__(message=message, status_code=500, details=details)
