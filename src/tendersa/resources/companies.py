from __future__ import annotations

import builtins
from typing import Any

from .._types import ApiResponse, Award, CompanyProfile, CompanyProfileResponse, CompanySearchResult


class CompaniesResource:
    def __init__(self, client) -> None:
        self._client = client

    async def list(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[CompanyProfile]]:
        raw = await self._client._get_list("/companies", params=params)
        items = [CompanyProfile(**c) if isinstance(c, dict) else c for c in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get(self, name: str) -> CompanyProfileResponse | None:
        raw = await self._client._get_single(f"/companies/{name}")
        if not raw.data:
            return None
        d = raw.data
        profile = CompanyProfile(**d.get("profile", d))
        awards = [Award(**a) if isinstance(a, dict) else a for a in d.get("awards", [])]
        directors = d.get("directors", [])
        return CompanyProfileResponse(profile=profile, awards=awards, directors=directors)

    async def search(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[CompanySearchResult]]:
        raw = await self._client._get_list("/companies/search", params=params)
        items = [CompanySearchResult(**c) if isinstance(c, dict) else c for c in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def top(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[CompanyProfile]]:
        raw = await self._client._get_list("/companies/top", params=params)
        items = [CompanyProfile(**c) if isinstance(c, dict) else c for c in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def by_registration(
        self,
        reg_number: str,
    ) -> CompanyProfileResponse | None:
        raw = await self._client._get_single(f"/companies/by-registration/{reg_number}")
        if not raw.data:
            return None
        d = raw.data
        profile = CompanyProfile(**d.get("profile", d))
        awards = [Award(**a) if isinstance(a, dict) else a for a in d.get("awards", [])]
        directors = d.get("directors", [])
        return CompanyProfileResponse(profile=profile, awards=awards, directors=directors)

    async def awards(
        self,
        name: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Award]]:
        raw = await self._client._get_list(f"/companies/{name}/awards", params=params)
        items = [Award(**a) if isinstance(a, dict) else a for a in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def contracts(
        self,
        name: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[dict]]:
        return await self._client._get_list(f"/companies/{name}/contracts", params=params)

    async def tenders(
        self,
        name: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[dict]]:
        return await self._client._get_list(f"/companies/{name}/tenders", params=params)

    async def directors(
        self,
        name: str,
    ) -> ApiResponse[builtins.list[dict]]:
        return await self._client._get_list(f"/companies/{name}/directors")
