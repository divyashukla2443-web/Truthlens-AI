"""
Reusable FastAPI dependency-injection functions for TruthLens AI backend.

Database session management lives in `app/db/session.py` and is
re-exported via `app/api/deps.py`. This module retains only
authentication-related dependencies that don't belong to the db layer.
"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.APP_NAME}/auth/login", auto_error=True)


def get_current_user_payload(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Decodes the bearer token from the Authorization header and returns
    its payload.

    Full user-object resolution (payload -> ORM user record) will be
    layered on top of this once the User model and a user repository
    exist (Steps 6-8).
    """
    return decode_access_token(token)
