# =============================================================================
#  Filename: newsletter_service.py
#
#  Short Description: Main service for orchestrating the newsletter generation workflow
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

import asyncio
import logging
from typing import List, Optional
from datetime import datetime

from ..models.news_models import NewsletterData, NewsArticle, NewsSummary, EditorialArticle
from .news_service import NewsService
from .ai_service import AIService
from .cache_service import CacheService
from ..config import settings

logger = logging.getLogger(__name__)

class NewsletterService:
    """Main service for orchestrating the newsletter generation workflow."""
    
    def __init__(self):
        self.news_service = NewsService()
        self.ai_service = AIService()
        self.cache_service = CacheService()
        logger.info("NewsletterService initialized")
    
    async def generate_newsletter(self, force_refresh: bool = False) -> NewsletterData:
        """Generate complete newsletter with caching."""
        # Check cache first
        if not force_refresh:
            cached_newsletter = await self.cache_service.get_newsletter()
            if cached_newsletter:
                logger.info("Returning cached newsletter.")
                return cached_newsletter
        
        # Generate new newsletter
        newsletter = await self._create_newsletter()
        
        # Cache the result
        await self.cache_service.set_newsletter(newsletter)
        
        return newsletter
    
    async def _create_newsletter(self) -> NewsletterData:
        """Create a new newsletter following the multi-agent workflow."""
        # Step 1: Reporter Agent - Fetch articles
        logger.info("🔍 Reporter Agent: Fetching latest AI news...")
        articles = await self.news_service.fetch_articles()
        
        if not articles:
            logger.warning("No articles found from news service, falling back to mock data.")
            articles = self.news_service._get_mock_articles(settings.max_articles)
            if not articles:
                raise Exception("No articles found even with mock data.")
        
        # Step 2: Editor Agent - Process articles
        logger.info("✏️ Editor Agent: Summarizing articles...")
        summaries = []
        for article in articles:
            summary = await self.ai_service.summarize_article(article)
            summaries.append(summary)
        
        # Step 3: Senior Editor Agent - Create editorial
        logger.info("📝 Senior Editor Agent: Creating editorial narrative...")
        editorial = await self.ai_service.write_editorial(summaries)
        
        # Create final newsletter
        newsletter = NewsletterData(
            editorial=editorial,
            summaries=summaries,
            total_articles=len(summaries),
            version="1.0"
        )
        
        logger.info(f"✅ Newsletter generated with {len(summaries)} articles")
        return newsletter
    
    async def get_newsletter(self, force_refresh: bool = False) -> Optional[NewsletterData]:
        """Get newsletter data (cached or fresh)."""
        try:
            return await self.generate_newsletter(force_refresh)
        except Exception as e:
            logger.error(f"Newsletter generation failed: {e}", exc_info=True)
            return None
    
    async def get_article_by_id(self, article_id: str) -> Optional[dict]:
        """Get specific article by ID."""
        newsletter = await self.get_newsletter()
        if not newsletter:
            return None
        
        for summary in newsletter.summaries:
            if summary.id == article_id:
                return {
                    "id": summary.id,
                    "title": summary.catchy_title,
                    "summary": summary.summary,
                    "key_points": summary.key_points,
                    "url": summary.original_article.url,
                    "thumbnail": summary.original_article.thumbnail,
                    "source": summary.original_article.source,
                    "published_date": summary.original_article.published_date,
                    "relevance_score": summary.relevance_score
                }
        
        return None
    
    async def get_cache_status(self) -> dict:
        """Get cache status and statistics."""
        return await self.cache_service.get_cache_info()
    
    async def clear_cache(self) -> None:
        """Clear all cached data."""
        await self.cache_service.clear_cache()

# Export the instance
newsletter_service = NewsletterService()
