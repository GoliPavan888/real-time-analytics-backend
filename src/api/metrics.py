from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from src.services.cache_service import CacheService
from src.services.rate_limit_service import RateLimiter
from src.services.circuit_breaker_service import CircuitBreaker, CircuitBreakerOpenError
from src.services.external_data_simulator import fetch_risky_external_data
import redis.asyncio as redis
from src.config.settings import settings

router = APIRouter()

class Metric(BaseModel):
    timestamp: datetime
    value: float
    type: str

# In-memory store for metrics
metrics_db: List[Metric] = []

# Initialize services (will be set in main.py)
redis_client: redis.Redis = None
cache_service: CacheService = None
rate_limiter: RateLimiter = None
circuit_breaker: CircuitBreaker = None

@router.post("/api/metrics", status_code=201)
async def create_metric(metric: Metric, request: Request):
    client_ip = request.client.host
    if not await rate_limiter.allow_request(client_ip):
        retry_after = await rate_limiter.get_retry_after(client_ip)
        raise HTTPException(status_code=429, detail="Rate limit exceeded", headers={"Retry-After": str(retry_after)})

    metrics_db.append(metric)
    return {"message": "Metric received"}

@router.get("/api/metrics/summary")
async def get_metrics_summary(type: str, period: str):
    # Compute summary key
    key = f"summary:{type}:{period}"

    async def compute_summary():
        # Filter metrics by type
        filtered = [m for m in metrics_db if m.type == type]
        if not filtered:
            return {"type": type, "period": period, "average_value": 0.0, "count": 0}

        # Simple aggregation: average value
        total = sum(m.value for m in filtered)
        count = len(filtered)
        average = total / count

        # Try to fetch external data with circuit breaker
        external_data = {"external_source": "fallback", "value": 0}
        try:
            external_data = await circuit_breaker.call(fetch_risky_external_data)
        except CircuitBreakerOpenError:
            pass  # Use fallback

        return {
            "type": type,
            "period": period,
            "average_value": average,
            "count": count,
            "external_data": external_data
        }

    return await cache_service.get_or_set(key, compute_summary)

@router.get("/health")
async def health_check():
    try:
        await redis_client.ping()
        return {"status": "healthy"}
    except:
        raise HTTPException(status_code=503, detail="Service unhealthy")

