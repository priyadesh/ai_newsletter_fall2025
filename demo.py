# =============================================================================
#  Filename: demo.py
#
#  Short Description: Demo script to showcase AI News Newsletter features
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

import asyncio
import json
from datetime import datetime
from src.ReactNewslettr.services.newsletter_service import NewsletterService
from src.ReactNewslettr.services.news_service import NewsService
from src.ReactNewslettr.services.ai_service import AIService


async def demo_newsletter_system():
    """Demonstrate the AI News Newsletter system capabilities."""
    
    print("🤖 AI News Newsletter - System Demo")
    print("=" * 50)
    
    # Initialize services
    print("\n📦 Initializing services...")
    newsletter_service = NewsletterService()
    news_service = NewsService()
    ai_service = AIService()
    
    # Demo 1: Fetch Articles
    print("\n🔍 Demo 1: Fetching Articles (Reporter Agent)")
    print("-" * 30)
    
    articles = await news_service.fetch_articles()
    print(f"✅ Fetched {len(articles)} articles")
    
    for i, article in enumerate(articles[:3], 1):
        print(f"\n📰 Article {i}:")
        print(f"   Title: {article.title}")
        print(f"   Source: {article.source}")
        print(f"   URL: {article.url}")
    
    # Demo 2: Process Articles
    print("\n✏️ Demo 2: Processing Articles (Editor Agent)")
    print("-" * 30)
    
    summaries = await ai_service.process_articles(articles[:3])  # Process first 3
    
    for summary in summaries:
        print(f"\n📝 Summary:")
        print(f"   ID: {summary.id}")
        print(f"   Catchy Title: {summary.catchy_title}")
        print(f"   Summary: {summary.summary[:100]}...")
        print(f"   Relevance: {summary.relevance_score:.2f}")
    
    # Demo 3: Create Editorial
    print("\n📝 Demo 3: Creating Editorial (Senior Editor Agent)")
    print("-" * 30)
    
    editorial = await ai_service.create_editorial(summaries)
    print(f"✅ Editorial Created:")
    print(f"   Title: {editorial.title}")
    print(f"   Theme: {editorial.theme}")
    print(f"   Content: {editorial.content[:200]}...")
    
    # Demo 4: Full Newsletter
    print("\n📰 Demo 4: Complete Newsletter Generation")
    print("-" * 30)
    
    newsletter = await newsletter_service.generate_newsletter()
    print(f"✅ Newsletter Generated:")
    print(f"   Editorial: {newsletter.editorial.title}")
    print(f"   Articles: {len(newsletter.summaries)}")
    print(f"   Generated: {newsletter.generated_at}")
    
    # Demo 5: Cache Status
    print("\n💾 Demo 5: Cache Status")
    print("-" * 30)
    
    cache_status = await newsletter_service.get_cache_status()
    print(f"✅ Cache Info:")
    print(f"   Size: {cache_status['size']}")
    print(f"   TTL: {cache_status['ttl_minutes']} minutes")
    print(f"   Hit Rate: {cache_status['hit_rate']:.2%}")
    
    print("\n�� Demo Complete!")
    print("=" * 50)
    print("🌐 Visit http://localhost:8080 to see the web interface")
    print("📚 Visit http://localhost:8080/docs for API documentation")


if __name__ == "__main__":
    print("Starting AI News Newsletter Demo...")
    print("Make sure the server is running: python main.py")
    print()
    
    try:
        asyncio.run(demo_newsletter_system())
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Make sure you have:")
        print("1. Set OPENAI_API_KEY in .env file")
        print("2. Started the server with: python main.py")
