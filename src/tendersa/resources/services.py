from __future__ import annotations

import builtins

from .._types import ApiResponse, ServiceType


class ServicesResource:
    def __init__(self, client) -> None:
        self._client = client

    async def list(
        self,
    ) -> ApiResponse[builtins.list[ServiceType]]:
        raw = await self._client._get_list("/services")
        items = [ServiceType(**s) if isinstance(s, dict) else s for s in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get(self, service_slug: str) -> ServiceType | None:
        raw = await self._client._get_single(f"/services/{service_slug}")
        if not raw.data:
            return None
        return ServiceType(**raw.data)
