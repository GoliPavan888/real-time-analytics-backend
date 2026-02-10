import pytest
import asyncio
from src.services.circuit_breaker_service import CircuitBreaker, CircuitBreakerOpenError

@pytest.mark.asyncio
async def test_circuit_breaker_transitions():
    # failure_threshold 2 means two consecutive failures will open the circuit
    cb = CircuitBreaker(failure_threshold=2, reset_timeout_seconds=1)

    async def failing():
        raise RuntimeError("fail")

    async def succeeding():
        return "ok"

    # two failures -> open
    with pytest.raises(RuntimeError):
        await cb.call(failing)
    with pytest.raises(RuntimeError):
        await cb.call(failing)

    # Circuit should now be open; calls should raise CircuitBreakerOpenError
    with pytest.raises(CircuitBreakerOpenError):
        await cb.call(succeeding)

    # wait for reset timeout to allow half-open
    await asyncio.sleep(1.1)

    # In half-open, first test succeeds and should close the circuit
    result = await cb.call(succeeding)
    assert result == "ok"

    # After success, circuit is closed and should allow normal calls
    result = await cb.call(succeeding)
    assert result == "ok"
