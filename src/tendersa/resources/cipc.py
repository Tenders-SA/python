from __future__ import annotations

import builtins
from typing import Any

from .._types import ApiResponse, CipcDirector, CipcEnrichment


class CipcResource:
    def __init__(self, client) -> None:
        self._client = client

    async def list_enrichments(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[CipcEnrichment]]:
        raw = await self._client._get_list("/cipc/enrichments", params=params)
        items = [CipcEnrichment(**e) if isinstance(e, dict) else e for e in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get_enrichment(self, enrichment_id: str) -> CipcEnrichment | None:
        raw = await self._client._get_single(f"/cipc/enrichments/{enrichment_id}")
        if not raw.data:
            return None
        return CipcEnrichment(**raw.data)

    async def list_directors(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[CipcDirector]]:
        raw = await self._client._get_list("/cipc/directors", params=params)
        items = [CipcDirector(**d) if isinstance(d, dict) else d for d in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get_director(self, director_id: str) -> CipcDirector | None:
        raw = await self._client._get_single(f"/cipc/directors/{director_id}")
        if not raw.data:
            return None
        return CipcDirector(**raw.data)
