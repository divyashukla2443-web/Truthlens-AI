"""
Security primitives for TruthLens AI backend.

Provides password hashing/verification and JWT access token creation
and decoding. This module contains only reusable primitives — actual
authentication business logic (login flow, user lookup, etc.) belongs
in a future `app/services/auth_service.py`, not here.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import UnauthorizedException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Hashes a plaintext password using bcrypt."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a bcrypt hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
    extra_claims: Optional[dict[str, Any]] = None,
) -> str:
    """
    Creates a signed JWT access token.

    Args:
        subject: The token subject, typically the user's unique identifier.
        expires_delta: Optional custom expiration window. Defaults to
            `settings.ACCESS_TOKEN_EXPIRE_MINUTES` if not provided.
        extra_claims: Optional additional claims to embed in the token
            (e.g. roles, permissions).

    Returns:
        Encoded JWT as a string.
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode: dict[str, Any] = {"sub": subject, "exp": expire}
    if extra_claims:
        to_encode.update(extra_claims)

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decodes and validates a JWT access token.

    Raises:
        UnauthorizedException: If the token is invalid, malformed, or expired.

    Returns:
        The decoded token payload.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as exc:
        raise UnauthorizedException(message="Invalid or expired authentication token.") from exc
