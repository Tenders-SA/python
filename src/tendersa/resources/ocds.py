from __future__ import annotations

import builtins
from typing import Any

from .._types import ApiResponse, OcdsParty


class OcdsResource:
    def __init__(self, client) -> None:
        self._client = client

    async def list_parties(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[OcdsParty]]:
        raw = await self._client._get_list("/ocds/parties", params=params)
        items = [OcdsParty(**p) if isinstance(p, dict) else p for p in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get_party(self, party_id: str) -> OcdsParty | None:
        raw = await self._client._get_single(f"/ocds/parties/{party_id}")
        if not raw.data:
            return None
        return OcdsParty(**raw.data)
