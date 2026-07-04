"""
API-layer dependency re-exports for TruthLens AI backend.

Route modules under `app/api/v1/endpoints/` should import dependencies
from here rather than reaching into `app/core/dependencies.py` or
`app/db/session.py` directly. This gives a single, stable import
surface for the API layer and lets the underlying implementation
change without touching route files.
"""

from app.core.dependencies import get_current_user_payload
from app.db.session import get_db

__all__ = ["get_db", "get_current_user_payload"]
