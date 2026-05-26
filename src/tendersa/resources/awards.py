from __future__ import annotations

import builtins
from typing import Any

from .._types import ApiResponse, Award


class AwardsResource:
    def __init__(self, client) -> None:
        self._client = client

    async def list(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Award]]:
        raw = await self._client._get_list("/awards", params=params)
        items = [Award(**a) if isinstance(a, dict) else a for a in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get(self, award_id: str) -> Award | None:
        raw = await self._client._get_single(f"/awards/{award_id}")
        if not raw.data:
            return None
        return Award(**raw.data)

    async def analytics(
        self,
        params: dict[str, Any] | None = None,
    ) -> dict:
        return await self._client.get("/awards/analytics", params=params)
