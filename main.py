# =============================================================================
#  Filename: main.py
#
#  Short Description: Main entry point for the AI News Newsletter FastAPI application
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

import uvicorn
import logging
from src.ReactNewslettr.config import settings

# Configure logging
logging.basicConfig(level=settings.log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"🚀 Starting AI News Newsletter v{settings.app_version}")
    logger.info(f"📡 Server will be available at http://{settings.host}:{settings.port}")
    logger.info(f"📚 API documentation at http://{settings.host}:{settings.port}/docs")
    logger.info(f"🔄 Cache TTL: {settings.cache_ttl_minutes} minutes")
    logger.info("-" * 50)
    
    uvicorn.run(
        "src.ReactNewslettr.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
