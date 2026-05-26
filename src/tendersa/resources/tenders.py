from __future__ import annotations

import builtins
from typing import Any

from .._types import (
    ApiResponse,
    Award,
    EstimatedValue,
    Tender,
    TenderAnalysis,
    TenderDetail,
    TenderDocument,
    TimelineEvent,
    ValueEstimate,
)
from ..pagination import PaginatedAsyncIterator


class TendersResource:
    def __init__(self, client) -> None:
        self._client = client

    async def list(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Tender]]:
        raw = await self._client._get_list("/tenders", params=params)
        items = [Tender(**t) if isinstance(t, dict) else t for t in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get(self, tender_id: str) -> TenderDetail:
        raw = await self._client._get_single(f"/tenders/{tender_id}")
        data = raw.data
        awards = [Award(**a) if isinstance(a, dict) else a for a in (data.get("awards") or [])]
        return TenderDetail(
            tender_id=data.get("tender_id", ""),
            title=data.get("title"),
            description=data.get("description"),
            province=data.get("province"),
            category=data.get("category") or [],
            estimated_value=EstimatedValue(**data["estimated_value"]) if data.get("estimated_value") else None,
            closing_date=data.get("closing_date"),
            status=data.get("status"),
            publication_date=data.get("publication_date"),
            publication_type=data.get("publication_type"),
            ai_summary=data.get("ai_summary"),
            ai_key_requirements=data.get("ai_key_requirements"),
            ai_confidence=data.get("ai_confidence"),
            classification_confidence=data.get("classification_confidence"),
            source_organization=data.get("source_organization"),
            reference_number=data.get("reference_number"),
            site_url=data.get("site_url"),
            municipality=data.get("municipality"),
            department=data.get("department"),
            institution=data.get("institution"),
            data_source=data.get("data_source"),
            awards=awards,
        )

    async def search(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Tender]]:
        raw = await self._client._get_list("/tenders/search", params=params)
        items = [Tender(**t) if isinstance(t, dict) else t for t in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def documents(self, tender_id: str) -> ApiResponse[builtins.list[TenderDocument]]:
        raw = await self._client._get_list(f"/tenders/{tender_id}/documents")
        items = [TenderDocument(**d) if isinstance(d, dict) else d for d in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def awards(self, tender_id: str) -> ApiResponse[builtins.list[Award]]:
        raw = await self._client._get_list(f"/tenders/{tender_id}/awards")
        items = [Award(**a) if isinstance(a, dict) else a for a in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def timeline(self, tender_id: str) -> ApiResponse[builtins.list[TimelineEvent]]:
        raw = await self._client._get_list(f"/tenders/{tender_id}/timeline")
        items = [TimelineEvent(**e) if isinstance(e, dict) else e for e in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def analysis(self, tender_id: str) -> TenderAnalysis | None:
        raw = await self._client._get_single(f"/tenders/{tender_id}/analysis")
        if not raw.data:
            return None
        return TenderAnalysis(**raw.data)

    async def value_estimate(self, tender_id: str) -> ValueEstimate | None:
        raw = await self._client._get_single(f"/tenders/{tender_id}/value-estimate")
        if not raw.data:
            return None
        return ValueEstimate(**raw.data)

    def paginated(
        self,
        params: dict[str, Any] | None = None,
        max_pages: int | None = None,
    ) -> PaginatedAsyncIterator[Tender]:
        async def fetcher(p: dict) -> ApiResponse[list[Tender]]:
            return await self.list(p)
        return PaginatedAsyncIterator(fetcher, params=params, max_pages=max_pages)
