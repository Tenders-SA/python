from __future__ import annotations

import builtins
from typing import Any

from .._types import ApiResponse, NewsletterEdition


class NewslettersResource:
    def __init__(self, client) -> None:
        self._client = client

    async def list(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[NewsletterEdition]]:
        raw = await self._client._get_list("/newsletters", params=params)
        items = [NewsletterEdition(**n) if isinstance(n, dict) else n for n in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get(self, edition_id: str) -> NewsletterEdition | None:
        raw = await self._client._get_single(f"/newsletters/{edition_id}")
        if not raw.data:
            return None
        return NewsletterEdition(**raw.data)
