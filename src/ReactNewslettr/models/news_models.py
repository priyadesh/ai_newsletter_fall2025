# =============================================================================
#  Filename: news_models.py
#
#  Short Description: Pydantic models for news articles and newsletter data
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


class NewsArticle(BaseModel):
    """Raw news article from external API."""
    
    title: str = Field(..., description="Article title")
    url: HttpUrl = Field(..., description="Source URL")
    snippet: str = Field(..., description="Article snippet or excerpt")
    thumbnail: Optional[HttpUrl] = Field(None, description="Article thumbnail image URL")
    source: str = Field(..., description="News source name")
    published_date: Optional[datetime] = Field(None, description="Publication date")
    full_text: Optional[str] = Field(None, description="Full article text if available")
    
    model_config = {"json_schema_extra": {"example": {
        "title": "OpenAI Releases GPT-5 with Enhanced Reasoning",
        "url": "https://example.com/news/gpt5-release",
        "snippet": "OpenAI announces GPT-5 with improved reasoning capabilities...",
        "thumbnail": "https://example.com/images/gpt5.jpg",
        "source": "TechCrunch",
        "published_date": "2025-01-27T10:00:00Z",
        "full_text": "Full article content here..."
    }}}


class NewsSummary(BaseModel):
    """Processed news summary with editorial enhancements."""
    
    id: str = Field(..., description="Unique identifier for the summary")
    original_article: NewsArticle = Field(..., description="Original article data")
    catchy_title: str = Field(..., description="Editor-created catchy title")
    summary: str = Field(..., description="2-3 sentence summary")
    key_points: List[str] = Field(default_factory=list, description="Key points extracted")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="AI relevance score")
    
    model_config = {"json_schema_extra": {"example": {
        "id": "summary_001",
        "original_article": {
            "title": "OpenAI Releases GPT-5",
            "url": "https://example.com/news/gpt5-release",
            "snippet": "OpenAI announces GPT-5...",
            "source": "TechCrunch"
        },
        "catchy_title": "🚀 GPT-5: The Next Evolution in AI Reasoning",
        "summary": "OpenAI has unveiled GPT-5, featuring significantly enhanced reasoning capabilities that push the boundaries of AI understanding. The new model demonstrates improved performance in complex problem-solving tasks.",
        "key_points": ["Enhanced reasoning", "Better problem-solving", "Improved performance"],
        "relevance_score": 0.95
    }}}


class EditorialArticle(BaseModel):
    """Creative editorial content for the newsletter."""
    
    title: str = Field(..., description="Editorial headline")
    content: str = Field(..., description="200-300 word editorial content")
    theme: str = Field(..., description="Main theme or narrative")
    author: str = Field(default="AI Editorial Team", description="Editorial author")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    
    model_config = {"json_schema_extra": {"example": {
        "title": "The AI Revolution: Where We Stand Today",
        "content": "As we navigate through 2025, the AI landscape continues to evolve at breakneck speed...",
        "theme": "AI Progress and Future",
        "author": "AI Editorial Team"
    }}}


class NewsletterData(BaseModel):
    """Complete newsletter data structure."""
    
    editorial: EditorialArticle = Field(..., description="Main editorial article")
    summaries: List[NewsSummary] = Field(..., description="List of news summaries")
    generated_at: datetime = Field(default_factory=datetime.now, description="Generation timestamp")
    version: str = Field(default="1.0", description="Newsletter version")
    total_articles: int = Field(..., description="Total number of articles processed")
    
    model_config = {"json_schema_extra": {"example": {
        "editorial": {
            "title": "The AI Revolution: Where We Stand Today",
            "content": "As we navigate through 2025...",
            "theme": "AI Progress"
        },
        "summaries": [],
        "total_articles": 10,
        "version": "1.0"
    }}}
