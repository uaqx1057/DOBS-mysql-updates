import time
from functools import lru_cache
from typing import Iterable, Tuple

# Lightweight in-memory TTL cache helpers; per-process only.


def _ttl_key(ttl_seconds: int) -> int:
    return int(time.time() // ttl_seconds) if ttl_seconds else 0


def ttl_cache(ttl_seconds: int = 60, maxsize: int = 128):
    """Decorator: cache function results with a coarse TTL bucket.
    Note: cache key includes a time bucket to invalidate after TTL.
    """

    def decorator(fn):
        @lru_cache(maxsize=maxsize)
        def cached(bucket, *args, **kwargs):
            return fn(*args, **kwargs)

        def wrapper(*args, **kwargs):
            bucket = _ttl_key(ttl_seconds)
            return cached(bucket, *args, **kwargs)

        wrapper.cache_clear = cached.cache_clear  # type: ignore[attr-defined]
        return wrapper

    return decorator
