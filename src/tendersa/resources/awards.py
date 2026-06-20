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

    async def analytics_by_province(
        self,
        params: dict[str, Any] | None = None,
    ) -> dict:
        return await self._client.get("/awards/analytics/province", params=params)

    async def analytics_by_category(
        self,
        params: dict[str, Any] | None = None,
    ) -> dict:
        return await self._client.get("/awards/analytics/category", params=params)

    async def analytics_by_bee_level(
        self,
        params: dict[str, Any] | None = None,
    ) -> dict:
        return await self._client.get("/awards/analytics/bee-level", params=params)

    async def analytics_by_enterprise_type(
        self,
        params: dict[str, Any] | None = None,
    ) -> dict:
        return await self._client.get("/awards/analytics/enterprise-type", params=params)

    async def by_tender(
        self,
        tender_id: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Award]]:
        raw = await self._client._get_list(f"/awards/by-tender/{tender_id}", params=params)
        items = [Award(**a) if isinstance(a, dict) else a for a in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def by_supplier(
        self,
        name: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Award]]:
        raw = await self._client._get_list(f"/awards/by-supplier/{name}", params=params)
        items = [Award(**a) if isinstance(a, dict) else a for a in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def by_supplier_party(
        self,
        party_id: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Award]]:
        raw = await self._client._get_list(f"/awards/by-supplier-party/{party_id}", params=params)
        items = [Award(**a) if isinstance(a, dict) else a for a in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def by_date_range(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Award]]:
        raw = await self._client._get_list("/awards/by-date-range", params=params)
        items = [Award(**a) if isinstance(a, dict) else a for a in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def subcontractors(
        self,
        award_id: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[dict]]:
        return await self._client._get_list(f"/awards/{award_id}/subcontractors", params=params)
