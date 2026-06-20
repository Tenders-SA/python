from __future__ import annotations

import builtins
from typing import Any

from .._types import ApiResponse, OrganizationProfile, OrganizationTenderSummary


class OrganizationsResource:
    def __init__(self, client) -> None:
        self._client = client

    async def list(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[OrganizationProfile]]:
        raw = await self._client._get_list("/organizations", params=params)
        items = [OrganizationProfile(**o) if isinstance(o, dict) else o for o in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get(self, org_id: str) -> OrganizationProfile | None:
        raw = await self._client._get_single(f"/organizations/{org_id}")
        if not raw.data:
            return None
        return OrganizationProfile(**raw.data)

    async def search(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[OrganizationProfile]]:
        raw = await self._client._get_list("/organizations/search", params=params)
        items = [OrganizationProfile(**o) if isinstance(o, dict) else o for o in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def by_slug(self, slug: str) -> OrganizationProfile | None:
        raw = await self._client._get_single(f"/organizations/by-slug/{slug}")
        if not raw.data:
            return None
        return OrganizationProfile(**raw.data)

    async def by_registration(self, reg_number: str) -> OrganizationProfile | None:
        raw = await self._client._get_single(f"/organizations/by-registration/{reg_number}")
        if not raw.data:
            return None
        return OrganizationProfile(**raw.data)

    async def counts_by_type(
        self,
    ) -> ApiResponse[builtins.list[dict]]:
        return await self._client._get_list("/organizations/counts-by-type")

    async def tenders(
        self,
        org_id: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[OrganizationTenderSummary]]:
        raw = await self._client._get_list(f"/organizations/{org_id}/tenders", params=params)
        items = [OrganizationTenderSummary(**t) if isinstance(t, dict) else t for t in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def directors(
        self,
        org_id: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[dict]]:
        return await self._client._get_list(f"/organizations/{org_id}/directors", params=params)
