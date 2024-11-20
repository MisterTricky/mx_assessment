from typing import Any, Optional
import time
from functools import wraps
from datetime import datetime

class CacheService:
    """Simple in-memory cache service with TTL support."""
    
    def __init__(self, default_ttl: int = 3600):  # 1 hour default TTL
        self._cache = {}
        self._default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache if it exists and hasn't expired."""
        if key in self._cache:
            value, expiry = self._cache[key]
            if expiry > time.time():
                return value
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in cache with optional TTL."""
        expiry = time.time() + (ttl if ttl is not None else self._default_ttl)
        self._cache[key] = (value, expiry)

    def delete(self, key: str) -> None:
        """Delete a value from cache."""
        self._cache.pop(key, None)

    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()

def cache_response(ttl: Optional[int] = None):
    """Decorator to cache function responses."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get cache instance
            cache = cache_service

            # Create cache key from function name and arguments
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # Try to get from cache
            cached_value = cache.get(key)
            if cached_value is not None:
                return cached_value

            # If not in cache, call function and cache result
            result = await func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result

        return wrapper
    return decorator

# Global cache instance
cache_service = CacheService()
