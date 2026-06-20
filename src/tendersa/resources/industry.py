from __future__ import annotations

import builtins

from .._types import ApiResponse, IndustryBenchmark


class IndustryResource:
    def __init__(self, client) -> None:
        self._client = client

    async def list(
        self,
    ) -> ApiResponse[builtins.list[IndustryBenchmark]]:
        raw = await self._client._get_list("/industry/benchmarks")
        items = [IndustryBenchmark(**b) if isinstance(b, dict) else b for b in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get(self, benchmark_id: str) -> IndustryBenchmark | None:
        raw = await self._client._get_single(f"/industry/benchmarks/{benchmark_id}")
        if not raw.data:
            return None
        return IndustryBenchmark(**raw.data)
