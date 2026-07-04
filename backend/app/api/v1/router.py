"""
Top-level router aggregator for API v1.

Individual feature routers (auth, users, analysis, etc.) will be
created in future sprints under `app/api/v1/endpoints/` and included
here. This file currently exposes an empty `api_router` so that
`app/main.py` has a stable import target from the start, without
depending on any business-logic routes existing yet.
"""

from fastapi import APIRouter

api_router = APIRouter()

# Future routers will be included like:
# from app.api.v1.endpoints import auth, users
# api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
