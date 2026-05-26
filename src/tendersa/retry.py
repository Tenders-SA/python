from __future__ import annotations

import asyncio
from collections.abc import Awaitable
from typing import Callable

import httpx

from .errors import RateLimitError


async def retry_with_backoff_async(
    request_fn: Callable[[], Awaitable[httpx.Response]],
    max_retries: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 30.0,
) -> httpx.Response:
    last_exc: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            return await request_fn()
        except RateLimitError:
            raise
        except (httpx.TimeoutException, httpx.TransportError) as exc:
            last_exc = exc
        except httpx.HTTPStatusError as exc:
            code = exc.response.status_code
            if code in (429, 502, 503, 504):
                last_exc = exc
            else:
                raise

        if attempt < max_retries:
            delay = min(base_delay * (2 ** attempt), max_delay)
            await asyncio.sleep(delay)

    raise last_exc or RuntimeError("Retry exhausted with no exception")
