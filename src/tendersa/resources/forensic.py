from __future__ import annotations

import builtins
from typing import Any

from .._types import ApiResponse, RestrictedSupplier, RestrictedSupplierMatch


class ForensicResource:
    def __init__(self, client) -> None:
        self._client = client

    async def list_restricted_suppliers(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[RestrictedSupplier]]:
        raw = await self._client._get_list("/forensic/restricted-suppliers", params=params)
        items = [RestrictedSupplier(**s) if isinstance(s, dict) else s for s in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get_restricted_supplier(self, supplier_id: str) -> RestrictedSupplier | None:
        raw = await self._client._get_single(f"/forensic/restricted-suppliers/{supplier_id}")
        if not raw.data:
            return None
        return RestrictedSupplier(**raw.data)

    async def match_restricted_supplier(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[dict]]:
        return await self._client._get_list("/forensic/restricted-suppliers/match", params=params)

    async def check_restricted_supplier(
        self,
        params: dict[str, Any] | None = None,
    ) -> RestrictedSupplierMatch | None:
        raw = await self._client._get_single("/forensic/restricted-suppliers/check", params=params)
        if not raw.data:
            return None
        d = raw.data
        match = RestrictedSupplier(**d["match"]) if d.get("match") else None
        return RestrictedSupplierMatch(restricted=d.get("restricted", False), match=match)
