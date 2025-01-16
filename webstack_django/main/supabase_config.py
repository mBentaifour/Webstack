from supabase import create_client
from django.conf import settings
from functools import wraps
import time
import logging
from django.core.cache import cache
from typing import Any, Callable

logger = logging.getLogger(__name__)

class SupabaseConnectionError(Exception):
    pass

def retry_on_failure(max_retries: int = 3, delay: int = 1) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Failed after {max_retries} attempts: {str(e)}")
                        raise SupabaseConnectionError(f"Failed to connect to Supabase: {str(e)}")
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay} seconds...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

class SupabaseClient:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._client:
            self._initialize_client()

    @retry_on_failure(max_retries=3, delay=1)
    def _initialize_client(self):
        url = settings.SUPABASE_URL
        key = settings.SUPABASE_KEY
        self._client = create_client(url, key)

    def get_client(self):
        return self._client

    @retry_on_failure(max_retries=3, delay=1)
    def query(self, cache_key: str = None, cache_timeout: int = 300, *args, **kwargs):
        """
        Execute a Supabase query with caching support
        """
        if cache_key:
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

        result = self._client.table(*args, **kwargs)
        
        if cache_key:
            cache.set(cache_key, result, cache_timeout)
        
        return result

def get_supabase_client():
    return SupabaseClient().get_client()
