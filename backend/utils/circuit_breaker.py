import pybreaker
import logging

logger = logging.getLogger("circuit_breaker")

class LogListener(pybreaker.CircuitBreakerListener):
    def state_change(self, cb, old_state, new_state):
        logger.warning(f"Circuit Breaker state changed from {old_state.name} to {new_state.name}")

# Trip after 5 failures, reset after 60 seconds
external_api_breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=60,
    listeners=[LogListener()]
)
