# =============================================================================
#  Filename: test_models.py
#
#  Short Description: Tests for Pydantic models
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

import pytest
from datetime import datetime
from src.ReactNewslettr.models.news_models import NewsArticle, NewsSummary, EditorialArticle, NewsletterData
from src.ReactNewslettr.models.api_models import APIResponse, ErrorResponse


class TestNewsArticle:
    """Test NewsArticle model."""
    
    def test_news_article_creation(self):
        """Test creating a NewsArticle."""
        article = NewsArticle(
            title="Test Article",
            url="https://example.com/test",
            snippet="Test snippet",
            source="Test Source"
        )
        
        assert article.title == "Test Article"
        assert str(article.url) == "https://example.com/test"
        assert article.snippet == "Test snippet"
        assert article.source == "Test Source"
    
    def test_news_article_with_optional_fields(self):
        """Test NewsArticle with optional fields."""
        article = NewsArticle(
            title="Test Article",
            url="https://example.com/test",
            snippet="Test snippet",
            source="Test Source",
            thumbnail="https://example.com/image.jpg",
            published_date=datetime.now(),
            full_text="Full article text"
        )
        
        assert article.thumbnail is not None
        assert article.published_date is not None
        assert article.full_text == "Full article text"


class TestNewsSummary:
    """Test NewsSummary model."""
    
    def test_news_summary_creation(self):
        """Test creating a NewsSummary."""
        article = NewsArticle(
            title="Test Article",
            url="https://example.com/test",
            snippet="Test snippet",
            source="Test Source"
        )
        
        summary = NewsSummary(
            id="test_001",
            original_article=article,
            catchy_title="🚀 Exciting Test Article",
            summary="This is a test summary.",
            key_points=["Point 1", "Point 2"],
            relevance_score=0.95
        )
        
        assert summary.id == "test_001"
        assert summary.catchy_title == "🚀 Exciting Test Article"
        assert summary.summary == "This is a test summary."
        assert len(summary.key_points) == 2
        assert summary.relevance_score == 0.95


class TestEditorialArticle:
    """Test EditorialArticle model."""
    
    def test_editorial_article_creation(self):
        """Test creating an EditorialArticle."""
        editorial = EditorialArticle(
            title="Test Editorial",
            content="This is test editorial content.",
            theme="Test Theme"
        )
        
        assert editorial.title == "Test Editorial"
        assert editorial.content == "This is test editorial content."
        assert editorial.theme == "Test Theme"
        assert editorial.author == "AI Editorial Team"


class TestNewsletterData:
    """Test NewsletterData model."""
    
    def test_newsletter_data_creation(self):
        """Test creating NewsletterData."""
        article = NewsArticle(
            title="Test Article",
            url="https://example.com/test",
            snippet="Test snippet",
            source="Test Source"
        )
        
        summary = NewsSummary(
            id="test_001",
            original_article=article,
            catchy_title="Test Title",
            summary="Test summary",
            relevance_score=0.9
        )
        
        editorial = EditorialArticle(
            title="Test Editorial",
            content="Test content",
            theme="Test Theme"
        )
        
        newsletter = NewsletterData(
            editorial=editorial,
            summaries=[summary],
            total_articles=1
        )
        
        assert newsletter.editorial.title == "Test Editorial"
        assert len(newsletter.summaries) == 1
        assert newsletter.total_articles == 1
        assert newsletter.version == "1.0"


class TestAPIResponse:
    """Test APIResponse model."""
    
    def test_api_response_success(self):
        """Test successful API response."""
        response = APIResponse(
            success=True,
            data={"test": "data"},
            message="Success"
        )
        
        assert response.success is True
        assert response.data == {"test": "data"}
        assert response.message == "Success"
    
    def test_api_response_failure(self):
        """Test failed API response."""
        response = APIResponse(
            success=False,
            data=None,
            message="Error occurred"
        )
        
        assert response.success is False
        assert response.data is None
        assert response.message == "Error occurred"


class TestErrorResponse:
    """Test ErrorResponse model."""
    
    def test_error_response_creation(self):
        """Test creating an ErrorResponse."""
        error = ErrorResponse(
            error="ValidationError",
            message="Invalid input",
            details={"field": "title"}
        )
        
        assert error.success is False
        assert error.error == "ValidationError"
        assert error.message == "Invalid input"
        assert error.details == {"field": "title"}
