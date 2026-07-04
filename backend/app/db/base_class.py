"""
Declarative base class for TruthLens AI SQLAlchemy models.

All ORM models (created in future sprints under `app/models/`) must
inherit from `Base`. Keeping this in its own module avoids circular
imports between the session module and model modules.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Shared declarative base for all database models.

    Using SQLAlchemy 2.0's `DeclarativeBase` style gives full typing
    support for model attributes when models are defined later.
    """

    pass
