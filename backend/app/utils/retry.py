"""
Retry utilities with exponential backoff for resilient API calls.

Usage:
    from app.utils.retry import retry_with_backoff

    @retry_with_backoff(max_attempts=3, exceptions=(ConnectionError,))
    def call_api():
        ...
"""

import time
import logging
import functools
from typing import Tuple, Type, Callable, Optional, Any

logger = logging.getLogger(__name__)


def retry_with_backoff(
    max_attempts: int = 3,
    backoff_seconds: Tuple[float, ...] = (2, 4, 8),
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    fallback: Optional[Callable[..., Any]] = None
):
    """
    Decorator for retrying functions with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts (default 3)
        backoff_seconds: Tuple of wait times between retries (default 2, 4, 8)
        exceptions: Tuple of exception types to catch and retry
        fallback: Optional function to call if all retries fail.
                  Will receive the same args/kwargs as the original function.

    Returns:
        Decorated function with retry logic

    Example:
        @retry_with_backoff(
            max_attempts=3,
            exceptions=(httpx.TimeoutException, httpx.HTTPStatusError),
            fallback=lambda *args, **kwargs: {"fallback": True}
        )
        def fetch_data(url):
            return httpx.get(url).json()
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt < max_attempts:
                        # Get backoff time (use last value if we exceed the tuple)
                        backoff_idx = min(attempt - 1, len(backoff_seconds) - 1)
                        wait_time = backoff_seconds[backoff_idx]

                        logger.warning(
                            f"[Retry] {func.__name__} attempt {attempt}/{max_attempts} failed: {e}. "
                            f"Retrying in {wait_time}s..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(
                            f"[Retry] {func.__name__} failed after {max_attempts} attempts: {e}"
                        )

            # All retries exhausted
            if fallback is not None:
                logger.info(f"[Retry] {func.__name__}: Using fallback function")
                return fallback(*args, **kwargs)

            # No fallback - re-raise the last exception
            raise last_exception

        return wrapper
    return decorator


class RetryableError(Exception):
    """Exception that signals the operation should be retried."""
    pass
