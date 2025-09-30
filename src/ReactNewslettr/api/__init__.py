# =============================================================================
#  Filename: __init__.py
#
#  Short Description: API package initialization
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

from .main import app
from .routes import router

__all__ = ["app", "router"]
