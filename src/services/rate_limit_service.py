import time


class RateLimiter:
    def __init__(self, redis_client, threshold: int, window_seconds: int):
        self.redis = redis_client
        self.threshold = threshold
        self.window = window_seconds

    async def allow_request(self, client_key: str) -> bool:
        current_time = int(time.time())
        window_start = current_time - self.window

        key = f"rate_limit:{client_key}"

        
        await self.redis.zremrangebyscore(key, "-inf", window_start)

        request_count = await self.redis.zcard(key)

        if request_count >= self.threshold:
            return False

        
        await self.redis.zadd(key, {str(current_time): current_time})

        
        await self.redis.expire(key, self.window)

        return True

    async def get_retry_after(self, client_key: str) -> int:
        key = f"rate_limit:{client_key}"

        
        oldest = await self.redis.zrange(key, 0, 0, withscores=True)

        if not oldest:
            return 0

        oldest_time = int(oldest[0][1])
        now = int(time.time())

        retry_after = self.window - (now - oldest_time)

        return max(retry_after, 0)
