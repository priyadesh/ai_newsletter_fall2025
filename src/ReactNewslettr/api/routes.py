# =============================================================================
#  Filename: routes.py
#
#  Short Description: API routes for the newsletter application
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

from fastapi import APIRouter, HTTPException, status, Query
from datetime import datetime
from typing import Optional

from ..services.newsletter_service import newsletter_service
from ..services.cache_service import CacheService
from ..models.api_models import APIResponse, ErrorResponse
from ..models.news_models import NewsletterData
from ..config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

cache_service_instance = CacheService()


@router.get("/health", response_model=APIResponse, summary="Health Check")
async def health_check():
    try:
        openai_status = "connected" if settings.has_openai_key else "disconnected"
        serpapi_status = "connected" if settings.has_serpapi_key else "disconnected"
        newsapi_status = "connected" if settings.has_newsapi_key else "disconnected"
        
        overall_status = "healthy" if settings.has_openai_key else "degraded"
        if not settings.has_any_news_source:
            overall_status = "demo_mode"
        
        return APIResponse(
            success=True,
            message="System health check completed",
            data={
                "status": overall_status,
                "version": settings.app_version,
                "timestamp": datetime.now().isoformat(),
                "mode": "demo" if settings.is_demo_mode else "production",
                "services": {
                    "openai": openai_status,
                    "serpapi": serpapi_status,
                    "newsapi": newsapi_status,
                    "cache": "active"
                },
                "configuration": {
                    "max_articles": settings.max_articles,
                    "cache_ttl_minutes": settings.cache_ttl_minutes,
                    "news_query": settings.news_query
                }
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="HealthCheckError",
                message="Health check failed",
                details={"error": str(e)}
            ).model_dump()
        )


@router.get("/newsletter", response_model=APIResponse, summary="Generate Latest AI News Newsletter")
async def get_newsletter(force_refresh: bool = Query(False, description="Force refresh of cached data")):
    """Generate the latest AI news newsletter with editorial and article summaries."""
    try:
        if force_refresh:
            await newsletter_service.clear_cache()
            logger.info("Cache cleared due to force_refresh parameter")
        
        newsletter_data: NewsletterData = await newsletter_service.generate_newsletter(force_refresh=force_refresh)
        
        return APIResponse(
            success=True,
            message="Latest AI News Newsletter generated successfully",
            data=newsletter_data
        )
    except Exception as e:
        logger.error(f"Error generating newsletter: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="NewsletterGenerationError",
                message="Failed to generate newsletter",
                details={"error": str(e)}
            ).model_dump()
        )


@router.post("/newsletter/regenerate", response_model=APIResponse, summary="Regenerate Newsletter")
async def regenerate_newsletter():
    """Forces a complete regeneration of the newsletter, bypassing and clearing the cache."""
    try:
        logger.info("Initiating full newsletter regeneration (cache bypass).")
        newsletter_data = await newsletter_service.generate_newsletter(force_refresh=True)
        return APIResponse(
            success=True,
            message="Newsletter regenerated successfully",
            data=newsletter_data
        )
    except Exception as e:
        logger.error(f"Error regenerating newsletter: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="NewsletterRegenerationError",
                message="Failed to regenerate newsletter",
                details={"error": str(e)}
            ).model_dump()
        )


@router.get("/newsletter/{article_id}", response_model=APIResponse, summary="Get Individual Article")
async def get_article(article_id: str):
    """Get details for a specific article by ID."""
    try:
        article = await newsletter_service.get_article_by_id(article_id)
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorResponse(
                    error="ArticleNotFoundError",
                    message="Article not found",
                    details={"article_id": article_id}
                ).model_dump()
            )
        
        return APIResponse(
            success=True,
            message="Article retrieved successfully",
            data=article
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving article {article_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="ArticleRetrievalError",
                message="Failed to retrieve article",
                details={"error": str(e), "article_id": article_id}
            ).model_dump()
        )


@router.delete("/cache", response_model=APIResponse, summary="Clear Cache")
async def clear_cache():
    """Clear the newsletter cache to force fresh data generation."""
    try:
        await newsletter_service.clear_cache()
        return APIResponse(
            success=True,
            message="Cache cleared successfully",
            data=None
        )
    except Exception as e:
        logger.error(f"Error clearing cache: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="CacheClearError",
                message="Failed to clear cache",
                details={"error": str(e)}
            ).model_dump()
        )


@router.get("/config", response_model=APIResponse, summary="Get Configuration")
async def get_config():
    """Get current system configuration (without sensitive data)."""
    try:
        return APIResponse(
            success=True,
            message="Configuration retrieved successfully",
            data={
                "app_name": settings.app_name,
                "app_version": settings.app_version,
                "max_articles": settings.max_articles,
                "cache_ttl_minutes": settings.cache_ttl_minutes,
                "news_query": settings.news_query,
                "mode": "demo" if settings.is_demo_mode else "production",
                "has_openai_key": settings.has_openai_key,
                "has_serpapi_key": settings.has_serpapi_key,
                "has_newsapi_key": settings.has_newsapi_key,
                "has_any_news_source": settings.has_any_news_source
            }
        )
    except Exception as e:
        logger.error(f"Error retrieving config: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorResponse(
                error="ConfigRetrievalError",
                message="Failed to retrieve configuration",
                details={"error": str(e)}
            ).model_dump()
        )
