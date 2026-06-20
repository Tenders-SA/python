from __future__ import annotations

from typing import Any

from .._types import ApiStatus, CategoryCount, IndustryBenchmarkSummary, ProvinceCount, UsageStats


class MetaResource:
    def __init__(self, client) -> None:
        self._client = client

    async def status(self) -> ApiStatus:
        raw = await self._client._get_single("/meta/status")
        return ApiStatus(**raw.data)

    async def provinces(self) -> list[ProvinceCount]:
        raw = await self._client._get_list("/meta/provinces")
        return [ProvinceCount(**p) if isinstance(p, dict) else p for p in raw.data]

    async def categories(self) -> list[CategoryCount]:
        raw = await self._client._get_list("/meta/categories")
        return [CategoryCount(**c) if isinstance(c, dict) else c for c in raw.data]

    async def usage(self) -> UsageStats:
        raw = await self._client._get_single("/meta/usage")
        return UsageStats(**raw.data)

    async def industries(
        self,
        params: dict[str, Any] | None = None,
    ) -> list[IndustryBenchmarkSummary]:
        raw = await self._client._get_list("/meta/industries", params=params)
        return [IndustryBenchmarkSummary(**i) if isinstance(i, dict) else i for i in raw.data]
