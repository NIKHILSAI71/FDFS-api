"""
Redis cache service.
"""
import redis.asyncio as redis
from typing import Optional, Callable, Any
from functools import wraps
import orjson
from app.core import config

_redis: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        _redis = redis.from_url(config.REDIS_URL, encoding="utf-8", decode_responses=False)
    return _redis


async def close_redis():
    global _redis
    if _redis:
        await _redis.close()
        _redis = None


async def get_cached(key: str) -> Optional[Any]:
    try:
        r = await get_redis()
        data = await r.get(key)
        if data:
            return orjson.loads(data)
    except Exception:
        pass
    return None


async def set_cached(key: str, value: Any, ttl: int = 300):
    try:
        r = await get_redis()
        await r.setex(key, ttl, orjson.dumps(value))
    except Exception:
        pass


def cached(key_prefix: str, ttl: int = 300):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key_parts = [key_prefix] + [str(v) for v in kwargs.values()]
            cache_key = ":".join(key_parts)

            cached_data = await get_cached(cache_key)
            if cached_data is not None:
                return cached_data

            result = await func(*args, **kwargs)
            await set_cached(cache_key, result, ttl)
            return result
        return wrapper
    return decorator
