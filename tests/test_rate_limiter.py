import time
from typing import Optional


class RateLimiter:
    """
    Redis-backed sliding window rate limiter.

    Uses Redis sorted sets:
      key: rate_limit:<client>
      score: timestamp
      member: timestamp

    Old entries outside the window are removed.
    """

    def __init__(self, redis_client, threshold: int, window_seconds: int):
        self.redis = redis_client
        self.threshold = threshold
        self.window = window_seconds

    async def allow_request(self, client_key: str) -> bool:
        """
        Returns True if request is allowed.
        Returns False if rate limit exceeded.
        """
        current_time = int(time.time())
        window_start = current_time - self.window

        key = f"rate_limit:{client_key}"

        # Remove old entries
        await self.redis.zremrangebyscore(key, "-inf", window_start)

        # Count requests in current window
        request_count = await self.redis.zcard(key)

        if request_count >= self.threshold:
            return False

        # Add current request timestamp
        await self.redis.zadd(key, {str(current_time): current_time})

        # Ensure key expires eventually
        await self.redis.expire(key, self.window)

        return True

    async def get_retry_after(self, client_key: str) -> int:
        """
        Returns seconds until next request is allowed.
        """
        key = f"rate_limit:{client_key}"

        # Get oldest request in window
        oldest = await self.redis.zrange(key, 0, 0, withscores=True)

        if not oldest:
            return 0

        oldest_timestamp = int(oldest[0][1])
        current_time = int(time.time())

        retry_after = self.window - (current_time - oldest_timestamp)

        return max(retry_after, 0)
