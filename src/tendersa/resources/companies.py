from __future__ import annotations

from typing import Any

from .._types import ApiResponse, CompanyProfile, CompanySearchResult


class CompaniesResource:
    def __init__(self, client) -> None:
        self._client = client

    async def get(self, company_id: str) -> CompanyProfile | None:
        raw = await self._client._get_single(f"/companies/{company_id}")
        if not raw.data:
            return None
        return CompanyProfile(**raw.data)

    async def search(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[list[CompanySearchResult]]:
        raw = await self._client._get_list("/companies/search", params=params)
        items = [CompanySearchResult(**c) if isinstance(c, dict) else c for c in raw.data]
        return ApiResponse(raw.success, items, raw.meta)
