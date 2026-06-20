from __future__ import annotations

import builtins
from typing import Any

from .._types import ApiResponse, SourceDirector


class DirectorsResource:
    def __init__(self, client) -> None:
        self._client = client

    async def list(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[SourceDirector]]:
        raw = await self._client._get_list("/directors", params=params)
        items = [SourceDirector(**d) if isinstance(d, dict) else d for d in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get(self, director_id: str) -> SourceDirector | None:
        raw = await self._client._get_single(f"/directors/{director_id}")
        if not raw.data:
            return None
        return SourceDirector(**raw.data)

    async def search(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[SourceDirector]]:
        raw = await self._client._get_list("/directors/search", params=params)
        items = [SourceDirector(**d) if isinstance(d, dict) else d for d in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def by_organization(
        self,
        org_id: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[SourceDirector]]:
        raw = await self._client._get_list(f"/directors/by-organization/{org_id}", params=params)
        items = [SourceDirector(**d) if isinstance(d, dict) else d for d in raw.data]
        return ApiResponse(raw.success, items, raw.meta)
