import os
from typing import Optional

class Settings:
    def __init__(self):
        self.redis_host: str = os.getenv("REDIS_HOST", "redis")
        self.redis_port: int = int(os.getenv("REDIS_PORT", "6379"))
        self.app_port: int = int(os.getenv("APP_PORT", "8000"))
        self.cache_ttl: int = int(os.getenv("CACHE_TTL_SECONDS", "300"))
        self.rate_limit_threshold: int = int(os.getenv("RATE_LIMIT_THRESHOLD", "5"))
        self.rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
        self.circuit_breaker_failure_threshold: int = int(os.getenv("CIRCUIT_BREAKER_FAILURE_THRESHOLD", "3"))
        self.circuit_breaker_reset_timeout: int = int(os.getenv("CIRCUIT_BREAKER_RESET_TIMEOUT", "10"))
        self.external_service_failure_rate: float = float(os.getenv("EXTERNAL_SERVICE_FAILURE_RATE", "0.1"))

settings = Settings()
