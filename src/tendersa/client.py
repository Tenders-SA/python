from __future__ import annotations

from typing import Any, TypeVar

import httpx

from ._convert import convert_keys
from ._types import ApiResponse, Meta, RateLimit
from .errors import create_error_from_response
from .pagination import PaginatedAsyncIterator
from .resources.awards import AwardsResource
from .resources.categories import CategoriesResource
from .resources.cipc import CipcResource
from .resources.companies import CompaniesResource
from .resources.directors import DirectorsResource
from .resources.documents import DocumentsResource
from .resources.forensic import ForensicResource
from .resources.industry import IndustryResource
from .resources.intelligence import IntelligenceResource
from .resources.meta import MetaResource
from .resources.newsletters import NewslettersResource
from .resources.ocds import OcdsResource
from .resources.organizations import OrganizationsResource
from .resources.provinces import ProvincesResource
from .resources.seo import SeoResource
from .resources.services import ServicesResource
from .resources.tenders import TendersResource

T = TypeVar("T")

BASE_URL = "https://api.tenders-sa.org/v2"
DEFAULT_TIMEOUT = 30.0


class TendersaClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = 3,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=httpx.Timeout(timeout),
            headers=self._default_headers(),
        )
        self.last_rate_limit: RateLimit | None = None

        self.tenders = TendersResource(self)
        self.awards = AwardsResource(self)
        self.companies = CompaniesResource(self)
        self.organizations = OrganizationsResource(self)
        self.directors = DirectorsResource(self)
        self.categories = CategoriesResource(self)
        self.provinces = ProvincesResource(self)
        self.seo = SeoResource(self)
        self.industry = IndustryResource(self)
        self.services = ServicesResource(self)
        self.ocds = OcdsResource(self)
        self.intel = IntelligenceResource(self)
        self.forensic = ForensicResource(self)
        self.cipc = CipcResource(self)
        self.newsletters = NewslettersResource(self)
        self.documents = DocumentsResource(self)
        self.meta = MetaResource(self)

    def _default_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
            "User-Agent": "tendersa-sdk-python/0.2.0a0",
        }

    def _parse_rate_limit(self, resp: httpx.Response) -> RateLimit | None:
        try:
            return RateLimit(
                limit=int(resp.headers.get("X-RateLimit-Limit", 0)),
                remaining=int(resp.headers.get("X-RateLimit-Remaining", 0)),
                reset=resp.headers.get("X-RateLimit-Reset", ""),
                policy=resp.headers.get("X-RateLimit-Policy", ""),
            )
        except (ValueError, TypeError):
            return None

    async def request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> dict:
        url = f"{self._base_url}{path}"
        resp = await self._client.request(
            method=method,
            url=url,
            params=params,
            json=body,
        )

        self.last_rate_limit = self._parse_rate_limit(resp)

        if resp.status_code >= 400:
            try:
                err_body = resp.json()
            except Exception:
                err_body = {}
            err = err_body if isinstance(err_body, dict) else {}
            raise create_error_from_response(
                status=resp.status_code,
                error=err.get("error", ""),
                code=err.get("code", ""),
                message=err.get("message", ""),
                request_id=err.get("requestId", ""),
                details=err.get("details"),
            )

        body: dict = resp.json()
        return body

    async def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict:
        return await self.request("GET", path, params=params)

    async def post(
        self,
        path: str,
        body: dict[str, Any] | None = None,
    ) -> dict:
        return await self.request("POST", path, body=body)

    async def _get_list(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[list[dict]]:
        body = await self.get(path, params=params)
        meta = self._parse_meta(body.get("meta", {}))
        raw_data = body.get("data", [])
        data = [convert_keys(d) for d in (raw_data if isinstance(raw_data, list) else [raw_data])]
        return ApiResponse(
            success=body.get("success", True),
            data=data,
            meta=meta,
        )

    async def _get_single(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[dict]:
        body = await self.get(path, params=params)
        meta = self._parse_meta(body.get("meta", {}))
        raw_data = body.get("data", {})
        data = convert_keys(raw_data) if isinstance(raw_data, dict) else {}
        return ApiResponse(
            success=body.get("success", True),
            data=data,
            meta=meta,
        )

    def _parse_meta(self, raw: dict) -> Meta:
        rl_raw = raw.get("rateLimit") or raw.get("rate_limit")
        rate_limit: RateLimit | None = None
        if rl_raw:
            rate_limit = RateLimit(
                limit=rl_raw.get("limit", 0),
                remaining=rl_raw.get("remaining", 0),
                reset=rl_raw.get("reset", ""),
                policy=rl_raw.get("policy", ""),
            )
        return Meta(
            request_id=raw.get("requestId") or raw.get("request_id", ""),
            timestamp=raw.get("timestamp", ""),
            api_version=raw.get("apiVersion") or raw.get("api_version", ""),
            deprecation=raw.get("deprecation"),
            page=raw.get("page"),
            page_size=raw.get("pageSize") or raw.get("page_size"),
            total_count=raw.get("totalCount") or raw.get("total_count"),
            total_pages=raw.get("totalPages") or raw.get("total_pages"),
            has_next=raw.get("hasNext") or raw.get("has_next"),
            has_prev=raw.get("hasPrev") or raw.get("has_prev"),
            rate_limit=rate_limit,
            query=raw.get("query"),
        )

    def paginated(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        max_pages: int | None = None,
    ) -> PaginatedAsyncIterator[dict]:
        async def fetcher(p: dict) -> ApiResponse[list[dict]]:
            return await self._get_list(path, p)
        return PaginatedAsyncIterator(fetcher, params=params, max_pages=max_pages)

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> TendersaClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
