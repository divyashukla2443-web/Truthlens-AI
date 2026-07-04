"""
Database engine and session management for TruthLens AI backend.

Provides the SQLAlchemy engine, a session factory, and the `get_db`
dependency used by FastAPI routes to obtain a request-scoped database
session.
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# `pool_pre_ping` guards against stale connections being handed out
# after periods of idleness (common with cloud-hosted Postgres).
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.APP_DEBUG,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a database session and guarantees
    it is closed after the request completes, even if an exception
    is raised.

    Usage:
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
