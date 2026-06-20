from __future__ import annotations

import builtins

from .._types import ApiResponse, ProvinceHealthScore, ProvinceInfo


class ProvincesResource:
    def __init__(self, client) -> None:
        self._client = client

    async def list(
        self,
    ) -> ApiResponse[builtins.list[ProvinceInfo]]:
        raw = await self._client._get_list("/provinces")
        items = [ProvinceInfo(**p) if isinstance(p, dict) else p for p in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get(self, province_slug: str) -> dict:
        raw = await self._client._get_single(f"/provinces/{province_slug}")
        return raw.data

    async def health_scores(
        self,
        province_slug: str,
    ) -> ApiResponse[builtins.list[ProvinceHealthScore]]:
        raw = await self._client._get_list(f"/provinces/{province_slug}/health-scores")
        items = [ProvinceHealthScore(**h) if isinstance(h, dict) else h for h in raw.data]
        return ApiResponse(raw.success, items, raw.meta)
