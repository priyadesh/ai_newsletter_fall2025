# =============================================================================
#  Filename: config.py
#
#  Short Description: Application configuration and settings management
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
    # API Keys
    openai_api_key: str = Field(
        ...,
        env="OPENAI_API_KEY",
        description="Your OpenAI API key for AI processing."
    )
    
    serpapi_api_key: Optional[str] = Field(
        None,
        env="SERPAPI_API_KEY", 
        description="Your SerpAPI key for news search."
    )
    
    newsapi_api_key: Optional[str] = Field(
        None,
        env="NEWSAPI_API_KEY",
        description="Your NewsAPI key for alternative news source."
    )
    
    # Application Settings
    app_name: str = Field("AI News Newsletter", env="APP_NAME")
    app_version: str = Field("1.0.0", env="APP_VERSION")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    cache_ttl_minutes: int = Field(10, env="CACHE_TTL_MINUTES")
    max_articles: int = Field(10, env="MAX_ARTICLES")
    news_query: str = Field("AI artificial intelligence machine learning tech news", env="NEWS_QUERY")
    
    # Server Settings
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8080, env="PORT")
    reload: bool = Field(True, env="RELOAD")
    
    @property
    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is properly configured."""
        return bool(self.openai_api_key and self.openai_api_key != "your_openai_api_key_here")
    
    @property
    def has_serpapi_key(self) -> bool:
        """Check if SerpAPI key is properly configured."""
        return bool(self.serpapi_api_key and self.serpapi_api_key != "your_serpapi_key_here")
    
    @property
    def has_newsapi_key(self) -> bool:
        """Check if NewsAPI key is properly configured."""
        return bool(self.newsapi_api_key and self.newsapi_api_key != "your_newsapi_key_here")
    
    @property
    def has_any_news_source(self) -> bool:
        """Check if any news source is configured."""
        return self.has_serpapi_key or self.has_newsapi_key
    
    @property
    def is_demo_mode(self) -> bool:
        """Check if running in demo mode (no real API keys)."""
        return not (self.has_openai_key and self.has_any_news_source)


# Global settings instance
settings = Settings()
