# =============================================================================
#  Filename: __init__.py
#
#  Short Description: ReactNewslettr package initialization
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

from svlearn.config.configuration import ConfigurationMixin
from dotenv import load_dotenv

load_dotenv()

# Load configuration
config = ConfigurationMixin().load_config()

# Package version
__version__ = "1.0.0"

# Main application
from .api.main import app

__all__ = ["app", "config", "__version__"]
