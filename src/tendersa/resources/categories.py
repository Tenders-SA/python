from __future__ import annotations

import builtins

from .._types import ApiResponse, TenderCategory


class CategoriesResource:
    def __init__(self, client) -> None:
        self._client = client

    async def list(
        self,
    ) -> ApiResponse[builtins.list[TenderCategory]]:
        raw = await self._client._get_list("/categories")
        items = [TenderCategory(**c) if isinstance(c, dict) else c for c in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get(self, category_id: str) -> TenderCategory | None:
        raw = await self._client._get_single(f"/categories/{category_id}")
        if not raw.data:
            return None
        return TenderCategory(**raw.data)

    async def by_slug(self, slug: str) -> dict:
        raw = await self._client._get_single(f"/categories/by-slug/{slug}")
        return raw.data
