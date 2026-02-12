from fastapi import FastAPI
import redis.asyncio as redis

from src.api import metrics as metrics_module
from src.services.cache_service import CacheService
from src.services.rate_limit_service import RateLimiter
from src.services.circuit_breaker_service import CircuitBreaker
from src.config.settings import settings

app = FastAPI(title="Real-Time Analytics Backend", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    redis_client = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        decode_responses=True,
    )

    metrics_module.redis_client = redis_client
    metrics_module.cache_service = CacheService(redis_client)

    metrics_module.rate_limiter = RateLimiter(
        redis_client,
        threshold=settings.rate_limit_threshold,
        window_seconds=settings.rate_limit_window,
    )

    metrics_module.circuit_breaker = CircuitBreaker(
        settings.circuit_breaker_failure_threshold,
        settings.circuit_breaker_reset_timeout,
    )


app.include_router(metrics_module.router)
