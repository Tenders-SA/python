from __future__ import annotations

import builtins
from typing import Any

from .._types import (
    ApiResponse,
    Award,
    CountItem,
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
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
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

    async def closing_soon(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Tender]]:
        raw = await self._client._get_list("/tenders/closing-soon", params=params)
        items = [Tender(**t) if isinstance(t, dict) else t for t in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def new_tenders(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Tender]]:
        raw = await self._client._get_list("/tenders/new", params=params)
        items = [Tender(**t) if isinstance(t, dict) else t for t in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def bbbee_required(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Tender]]:
        raw = await self._client._get_list("/tenders/bbbee-required", params=params)
        items = [Tender(**t) if isinstance(t, dict) else t for t in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def value_range(
        self,
        min_value: float,
        max_value: float,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Tender]]:
        p = dict(params or {})
        p["min"] = min_value
        p["max"] = max_value
        raw = await self._client._get_list("/tenders/value-range", params=p)
        items = [Tender(**t) if isinstance(t, dict) else t for t in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def by_province(
        self,
        province: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Tender]]:
        raw = await self._client._get_list(f"/tenders/by-province/{province}", params=params)
        items = [Tender(**t) if isinstance(t, dict) else t for t in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def by_organization(
        self,
        org_id: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Tender]]:
        raw = await self._client._get_list(f"/tenders/by-organization/{org_id}", params=params)
        items = [Tender(**t) if isinstance(t, dict) else t for t in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def by_publication_type(
        self,
        pub_type: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Tender]]:
        raw = await self._client._get_list(f"/tenders/by-publication-type/{pub_type}", params=params)
        items = [Tender(**t) if isinstance(t, dict) else t for t in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def by_category(
        self,
        category: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Tender]]:
        raw = await self._client._get_list(f"/tenders/by-category/{category}", params=params)
        items = [Tender(**t) if isinstance(t, dict) else t for t in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def counts_by_province(
        self,
    ) -> ApiResponse[builtins.list[CountItem]]:
        raw = await self._client._get_list("/tenders/counts/province")
        items = [CountItem(**c) if isinstance(c, dict) else c for c in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def counts_by_category(
        self,
    ) -> ApiResponse[builtins.list[CountItem]]:
        raw = await self._client._get_list("/tenders/counts/category")
        items = [CountItem(**c) if isinstance(c, dict) else c for c in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def counts_by_organization(
        self,
    ) -> ApiResponse[builtins.list[CountItem]]:
        raw = await self._client._get_list("/tenders/counts/organization")
        items = [CountItem(**c) if isinstance(c, dict) else c for c in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def counts_by_status(
        self,
    ) -> ApiResponse[builtins.list[CountItem]]:
        raw = await self._client._get_list("/tenders/counts/status")
        items = [CountItem(**c) if isinstance(c, dict) else c for c in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def documents(self, tender_id: str) -> ApiResponse[builtins.list[TenderDocument]]:
        raw = await self._client._get_list(f"/tenders/{tender_id}/documents")
        items = [TenderDocument(**d) if isinstance(d, dict) else d for d in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def contracts(self, tender_id: str) -> ApiResponse[builtins.list[dict]]:
        return await self._client._get_list(f"/tenders/{tender_id}/contracts")

    async def milestones(self, tender_id: str) -> ApiResponse[builtins.list[dict]]:
        return await self._client._get_list(f"/tenders/{tender_id}/milestones")

    async def bidders(self, tender_id: str) -> ApiResponse[builtins.list[dict]]:
        return await self._client._get_list(f"/tenders/{tender_id}/bidders")

    async def submission_requirements(self, tender_id: str) -> ApiResponse[builtins.list[dict]]:
        return await self._client._get_list(f"/tenders/{tender_id}/submission-requirements")

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

    async def seo(self, tender_id: str) -> dict:
        raw = await self._client._get_single(f"/tenders/{tender_id}/seo")
        return raw.data

    async def slug(self, tender_id: str) -> dict:
        raw = await self._client._get_single(f"/tenders/{tender_id}/slug")
        return raw.data

    async def related(
        self,
        tender_id: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Tender]]:
        raw = await self._client._get_list(f"/tenders/{tender_id}/related", params=params)
        items = [Tender(**t) if isinstance(t, dict) else t for t in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    def paginated(
        self,
        params: dict[str, Any] | None = None,
        max_pages: int | None = None,
    ) -> PaginatedAsyncIterator[Tender]:
        async def fetcher(p: dict) -> ApiResponse[list[Tender]]:
            return await self.list(p)
        return PaginatedAsyncIterator(fetcher, params=params, max_pages=max_pages)
