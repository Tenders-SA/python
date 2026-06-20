from __future__ import annotations

import builtins
from typing import Any

from .._types import ApiResponse, IntelItem, IntelSource


class IntelligenceResource:
    def __init__(self, client) -> None:
        self._client = client

    async def list_sources(
        self,
    ) -> ApiResponse[builtins.list[IntelSource]]:
        raw = await self._client._get_list("/intel/sources")
        items = [IntelSource(**s) if isinstance(s, dict) else s for s in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get_source(self, source_id: str) -> IntelSource | None:
        raw = await self._client._get_single(f"/intel/sources/{source_id}")
        if not raw.data:
            return None
        return IntelSource(**raw.data)

    async def list_items(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[IntelItem]]:
        raw = await self._client._get_list("/intel/items", params=params)
        items = [IntelItem(**i) if isinstance(i, dict) else i for i in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get_item(self, item_id: str) -> IntelItem | None:
        raw = await self._client._get_single(f"/intel/items/{item_id}")
        if not raw.data:
            return None
        return IntelItem(**raw.data)
