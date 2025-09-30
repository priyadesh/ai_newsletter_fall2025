# =============================================================================
#  Filename: cache_service.py
#
#  Short Description: File-based caching utilities for newsletters
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

import os
import json
import asyncio
from typing import Optional, Any
from datetime import datetime, date
from pathlib import Path
import re

from ..models.news_models import NewsletterData
from ..config import settings


class CacheService:
    """Service for file-based caching newsletter data with date-based storage."""
    
    def __init__(self):
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        self._lock = asyncio.Lock()
    
    def _get_cache_file_path(self, cache_date: date = None) -> Path:
        """Get the cache file path for a specific date."""
        if cache_date is None:
            cache_date = date.today()
        filename = f"newsletter_{cache_date.strftime('%Y-%m-%d')}.json"
        return self.cache_dir / filename
    
    async def get_newsletter(self, cache_date: date = None) -> Optional[NewsletterData]:
        """Get cached newsletter data for a specific date."""
        async with self._lock:
            cache_file = self._get_cache_file_path(cache_date)
            
            if not cache_file.exists():
                return None
            
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Pydantic will automatically validate and convert the data
                return NewsletterData.model_validate(data)
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Error reading cache file {cache_file}: {e}")
                return None
    
    async def set_newsletter(self, newsletter: NewsletterData, cache_date: date = None) -> None:
        """Cache newsletter data for a specific date."""
        async with self._lock:
            cache_file = self._get_cache_file_path(cache_date)
            
            try:
                # Use mode='json' to properly serialize HttpUrl and other Pydantic types as strings
                data = newsletter.model_dump(mode='json')
                
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, default=str)
                
                print(f"Newsletter cached to {cache_file}")
            except Exception as e:
                print(f"Error writing cache file {cache_file}: {e}")
    
    async def has_cached_newsletter(self, cache_date: date = None) -> bool:
        """Check if newsletter is cached for a specific date."""
        cache_file = self._get_cache_file_path(cache_date)
        return cache_file.exists()
    
    async def get_cache_info(self) -> dict:
        """Get cache statistics and info."""
        cache_files = list(self.cache_dir.glob("newsletter_*.json"))
        
        return {
            "cache_directory": str(self.cache_dir),
            "total_cached_days": len(cache_files),
            "cached_files": [f.name for f in cache_files],
            "today_cached": await self.has_cached_newsletter(),
            "cache_files": [
                {
                    "filename": f.name,
                    "date": f.stem.replace("newsletter_", ""),
                    "size_bytes": f.stat().st_size if f.exists() else 0,
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat() if f.exists() else None
                }
                for f in cache_files
            ]
        }
    
    async def clear_cache(self) -> None:
        """Clear all cached data."""
        async with self._lock:
            cache_files = list(self.cache_dir.glob("newsletter_*.json"))
            for cache_file in cache_files:
                try:
                    cache_file.unlink()
                    print(f"Deleted cache file: {cache_file}")
                except Exception as e:
                    print(f"Error deleting cache file {cache_file}: {e}")
    
    async def clear_today_cache(self) -> None:
        """Clear today's cached data."""
        async with self._lock:
            cache_file = self._get_cache_file_path()
            if cache_file.exists():
                try:
                    cache_file.unlink()
                    print(f"Deleted today's cache file: {cache_file}")
                except Exception as e:
                    print(f"Error deleting today's cache file {cache_file}: {e}")

    def list_archive_dates(self) -> list[str]:
        """Return available cache dates (YYYY-MM-DD) found in the cache directory."""
        cache_dir = Path(self.cache_dir)
        if not cache_dir.exists():
            return []
        dates: list[str] = []
        pattern = re.compile(r"^newsletter_(\d{4}-\d{2}-\d{2})\.json$")
        for p in cache_dir.iterdir():
            if not p.is_file():
                continue
            m = pattern.match(p.name)
            if m:
                dates.append(m.group(1))
        dates.sort(reverse=True)
        return dates

    def get_newsletter_by_date(self, date_str: str):
        """Load a cached newsletter by date (YYYY-MM-DD). Returns NewsletterData or None."""
        file_path = Path(self.cache_dir) / f"newsletter_{date_str}.json"
        if not file_path.exists():
            return None
        try:
            with file_path.open("r", encoding="utf-8") as f:
                payload = json.load(f)
            # payload may be entire API wrapper or raw newsletter; handle both
            if isinstance(payload, dict) and "newsletter" in payload:
                data = payload["newsletter"]
            else:
                data = payload
            return NewsletterData(**data)
        except Exception:
            return None


# Create global instance
cache_service = CacheService()
