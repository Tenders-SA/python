from __future__ import annotations

from typing import Any

from .._types import DocumentDetail


class DocumentsResource:
    def __init__(self, client) -> None:
        self._client = client

    async def get(self, document_id: str) -> DocumentDetail | None:
        raw = await self._client._get_single(f"/documents/{document_id}")
        if not raw.data:
            return None
        return DocumentDetail(**raw.data)

    async def download_url(
        self,
        document_id: str,
        params: dict[str, Any] | None = None,
    ) -> DocumentDetail | None:
        raw = await self._client._get_single(f"/documents/{document_id}/download-url", params=params)
        if not raw.data:
            return None
        return DocumentDetail(**raw.data)
