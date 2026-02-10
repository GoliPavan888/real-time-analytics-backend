import json
import redis.asyncio as redis
from typing import Any, Callable, Awaitable
from src.config.settings import settings

class CacheService:
    def __init__(self, redis_client: redis.Redis, default_ttl_seconds: int = settings.cache_ttl):
        self.redis = redis_client
        self.default_ttl = default_ttl_seconds

    async def get_or_set(self, key: str, data_fetch_func: Callable[[], Awaitable[Any]], ttl_seconds: int = None) -> Any:
        cached_data = await self.redis.get(key)
        if cached_data:
            return json.loads(cached_data)

        data = await data_fetch_func()
        ttl = ttl_seconds or self.default_ttl
        await self.redis.setex(key, ttl, json.dumps(data))
        return data
