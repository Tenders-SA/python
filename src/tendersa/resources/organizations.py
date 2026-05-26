from __future__ import annotations

from typing import Any

from .._types import ApiResponse, OrganizationProfile, OrganizationTenderSummary


class OrganizationsResource:
    def __init__(self, client) -> None:
        self._client = client

    async def get(self, org_id: str) -> OrganizationProfile | None:
        raw = await self._client._get_single(f"/organizations/{org_id}")
        if not raw.data:
            return None
        return OrganizationProfile(**raw.data)

    async def tenders(
        self,
        org_id: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[list[OrganizationTenderSummary]]:
        raw = await self._client._get_list(f"/organizations/{org_id}/tenders", params=params)
        items = [OrganizationTenderSummary(**t) if isinstance(t, dict) else t for t in raw.data]
        return ApiResponse(raw.success, items, raw.meta)
