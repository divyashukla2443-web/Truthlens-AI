"""
Application-wide constants for TruthLens AI backend.

Centralizing constants avoids magic strings/numbers scattered across the
codebase and gives a single point of change for values referenced in
multiple modules.
"""

from enum import Enum


class Environment(str, Enum):
    """Supported application runtime environments."""

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class LogLevel(str, Enum):
    """Supported logging verbosity levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# --- API Metadata ---
API_V1_PREFIX = "/api/v1"
DEFAULT_API_TITLE = "TruthLens AI API"

# --- Security Defaults ---
DEFAULT_TOKEN_ALGORITHM = "HS256"
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Pagination Defaults ---
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
