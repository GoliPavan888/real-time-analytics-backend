import asyncio
import time
from enum import Enum
from typing import Callable, Any, Awaitable

import asyncio
import time
from enum import Enum
from typing import Callable, Any, Awaitable

class CircuitState(Enum):
    CLOSED = 1
    OPEN = 2
    HALF_OPEN = 3

class CircuitBreakerOpenError(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int, reset_timeout_seconds: int):
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None
        self._threshold = failure_threshold
        self._reset_timeout = reset_timeout_seconds
        self._lock = asyncio.Lock()

    async def call(self, func: Callable[..., Awaitable[Any]], *args, **kwargs) -> Any:
        async with self._lock:
            if self._state == CircuitState.OPEN:
                if time.time() > self._last_failure_time + self._reset_timeout:
                    self._transition_to_half_open()
                else:
                    raise CircuitBreakerOpenError("Circuit is open, returning fallback.")

            elif self._state == CircuitState.HALF_OPEN:
                try:
                    result = await func(*args, **kwargs)
                    self._record_success()
                    self._transition_to_closed()
                    return result
                except Exception as e:
                    self._record_failure()
                    self._transition_to_open()
                    raise CircuitBreakerOpenError("Test request failed, circuit remains open.") from e

            # CircuitState.CLOSED
            try:
                result = await func(*args, **kwargs)
                self._record_success()
                return result
            except Exception as e:
                self._record_failure()
                if self._failure_count >= self._threshold:
                    self._transition_to_open()
                raise e

    def _record_failure(self):
        self._failure_count += 1
        self._last_failure_time = time.time()

    def _record_success(self):
        self._failure_count = 0

    def _transition_to_open(self):
        self._state = CircuitState.OPEN

    def _transition_to_closed(self):
        self._state = CircuitState.CLOSED

    def _transition_to_half_open(self):
        self._state = CircuitState.HALF_OPEN
