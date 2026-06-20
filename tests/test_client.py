from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from tendersa import TendersaClient
from tendersa._types import ApiResponse, Meta
from tendersa.errors import (
    AuthError,
    BadRequestError,
    ConflictError,
    ForbiddenError,
    InternalError,
    NotFoundError,
    RateLimitError,
    ServiceUnavailableError,
    TendersaError,
    create_error_from_response,
)
from tendersa.pagination import PaginatedAsyncIterator, PaginatedResponse

# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def api_key() -> str:
    return "tsa_test_key123"


@pytest.fixture
def client(api_key: str) -> TendersaClient:
    return TendersaClient(api_key)


@pytest.fixture
def sample_meta() -> dict:
    return {
        "requestId": "req_001",
        "timestamp": "2026-05-25T12:00:00Z",
        "apiVersion": "v2",
        "page": 1,
        "pageSize": 20,
        "totalCount": 100,
        "totalPages": 5,
        "hasNext": True,
        "hasPrev": False,
        "rateLimit": {
            "limit": 100,
            "remaining": 95,
            "reset": "2026-05-25T13:00:00Z",
            "policy": "sliding_window",
        },
    }


@pytest.fixture
def sample_tender() -> dict:
    return {
        "tender_id": "tender_001",
        "title": "Infrastructure upgrade",
        "description": "Road construction in Cape Town",
        "province": "Western Cape",
        "closing_date": "2026-06-30T23:59:00Z",
        "status": "OPEN",
        "publication_date": "2026-05-01T08:00:00Z",
    }


@pytest.fixture
def sample_award() -> dict:
    return {
        "award_id": "award_001",
        "tender_id": "tender_001",
        "title": "Road construction award",
        "status": "ACTIVE",
        "amount": 5000000.0,
        "supplier_name": "BuildCorp SA",
        "currency": "ZAR",
    }


# ── Client Initialization ───────────────────────────────────────────────────

class TestClientInit:
    def test_creates_client_with_api_key(self, api_key: str) -> None:
        c = TendersaClient(api_key)
        assert c._api_key == api_key
        assert c._base_url == "https://api.tenders-sa.org/v2"
        assert c._timeout == 30.0

    def test_custom_base_url(self, api_key: str) -> None:
        c = TendersaClient(api_key, base_url="https://staging.api.tenders-sa.org/v2")
        assert c._base_url == "https://staging.api.tenders-sa.org/v2"

    def test_has_resource_attributes(self, client: TendersaClient) -> None:
        assert client.tenders is not None
        assert client.awards is not None
        assert client.companies is not None
        assert client.organizations is not None
        assert client.directors is not None
        assert client.categories is not None
        assert client.provinces is not None
        assert client.seo is not None
        assert client.industry is not None
        assert client.services is not None
        assert client.ocds is not None
        assert client.intel is not None
        assert client.forensic is not None
        assert client.cipc is not None
        assert client.newsletters is not None
        assert client.documents is not None
        assert client.meta is not None

    def test_default_headers(self, api_key: str) -> None:
        c = TendersaClient(api_key)
        headers = c._default_headers()
        assert headers["Authorization"] == f"Bearer {api_key}"
        assert headers["Accept"] == "application/json"
        assert "tendersa-sdk-python" in headers["User-Agent"]


# ── Error Classes ────────────────────────────────────────────────────────────

class TestErrors:
    def test_base_error(self) -> None:
        err = TendersaError(500, "INTERNAL_ERROR", "Something broke", "req_001")
        assert err.status == 500
        assert err.code == "INTERNAL_ERROR"
        assert str(err) == "Something broke"
        assert err.request_id == "req_001"

    def test_bad_request(self) -> None:
        err = BadRequestError("Invalid params", "req_001")
        assert err.status == 400
        assert str(err) == "Invalid params"

    def test_auth_error(self) -> None:
        err = AuthError("Missing key", "req_001")
        assert err.status == 401

    def test_forbidden(self) -> None:
        err = ForbiddenError("No access", "req_001")
        assert err.status == 403

    def test_not_found(self) -> None:
        err = NotFoundError("Not found", "req_001")
        assert err.status == 404

    def test_conflict(self) -> None:
        err = ConflictError("Already exists", "req_001")
        assert err.status == 409

    def test_rate_limit(self) -> None:
        err = RateLimitError("Too many", "req_001", limit=100, used=100, resets_at="12:00", tier="free")
        assert err.status == 429
        assert err.limit == 100
        assert err.used == 100

    def test_internal(self) -> None:
        err = InternalError("Server error", "req_001")
        assert err.status == 500

    def test_service_unavailable(self) -> None:
        err = ServiceUnavailableError("Down", "req_001")
        assert err.status == 502

    def test_factory_creates_correct_type(self) -> None:
        assert isinstance(create_error_from_response(400, message="bad"), BadRequestError)
        assert isinstance(create_error_from_response(401, message="bad"), AuthError)
        assert isinstance(create_error_from_response(403, message="bad"), ForbiddenError)
        assert isinstance(create_error_from_response(404, message="bad"), NotFoundError)
        assert isinstance(create_error_from_response(409, message="bad"), ConflictError)
        assert isinstance(create_error_from_response(500, message="bad"), InternalError)
        assert isinstance(create_error_from_response(502, message="bad"), ServiceUnavailableError)
        assert isinstance(create_error_from_response(429, message="bad", details={"limit": 100}), RateLimitError)

    def test_factory_unknown_status_uses_base(self) -> None:
        err = create_error_from_response(418, message="teapot")
        assert isinstance(err, TendersaError)
        assert err.status == 418


# ── Pagination ──────────────────────────────────────────────────────────────

class TestPaginatedResponse:
    def test_basic_properties(self, sample_meta: dict) -> None:
        meta = Meta(
            request_id=sample_meta["requestId"],
            timestamp=sample_meta["timestamp"],
            api_version=sample_meta["apiVersion"],
            page=sample_meta["page"],
            page_size=sample_meta["pageSize"],
            total_count=sample_meta["totalCount"],
            total_pages=sample_meta["totalPages"],
            has_next=sample_meta["hasNext"],
            has_prev=sample_meta["hasPrev"],
        )
        resp = PaginatedResponse(["a", "b", "c"], meta)
        assert len(resp) == 3
        assert resp[0] == "a"
        assert list(resp) == ["a", "b", "c"]
        assert resp.has_next is True
        assert resp.has_prev is False
        assert resp.page == 1
        assert resp.page_size == 20
        assert resp.total_count == 100
        assert resp.total_pages == 5


class TestPaginatedAsyncIterator:
    @pytest.mark.asyncio
    async def test_single_page(self) -> None:
        async def fetcher(p: dict) -> ApiResponse:
            return ApiResponse(
                success=True,
                data=["a", "b"],
                meta=Meta(
                    request_id="r",
                    timestamp="t",
                    api_version="v2",
                    page=1,
                    page_size=20,
                    has_next=False,
                ),
            )
        pages = []
        async for page in PaginatedAsyncIterator(fetcher):
            pages.append(page.items)
        assert pages == [["a", "b"]]

    @pytest.mark.asyncio
    async def test_multiple_pages(self) -> None:
        call_count = 0

        async def fetcher(p: dict) -> ApiResponse:
            nonlocal call_count
            call_count += 1
            page_num = p["page"]
            return ApiResponse(
                success=True,
                data=[f"item_{page_num}"],
                meta=Meta(
                    request_id="r",
                    timestamp="t",
                    api_version="v2",
                    page=page_num,
                    page_size=20,
                    has_next=call_count < 3,
                ),
            )
        items = []
        async for page in PaginatedAsyncIterator(fetcher):
            items.extend(page.items)
        assert items == ["item_1", "item_2", "item_3"]

    @pytest.mark.asyncio
    async def test_max_pages(self) -> None:
        call_count = 0

        async def fetcher(p: dict) -> ApiResponse:
            nonlocal call_count
            call_count += 1
            page_num = p["page"]
            return ApiResponse(
                success=True,
                data=[f"item_{page_num}"],
                meta=Meta(
                    request_id="r",
                    timestamp="t",
                    api_version="v2",
                    page=page_num,
                    page_size=20,
                    has_next=True,
                ),
            )
        items = []
        async for page in PaginatedAsyncIterator(fetcher, max_pages=2):
            items.extend(page.items)
        assert items == ["item_1", "item_2"]
        assert call_count == 2


# ── Rate Limit Parsing ──────────────────────────────────────────────────────

class TestRateLimitParsing:
    def test_parse_valid_headers(self, client: TendersaClient) -> None:
        resp = MagicMock(spec=httpx.Response)
        resp.headers = {
            "X-RateLimit-Limit": "100",
            "X-RateLimit-Remaining": "95",
            "X-RateLimit-Reset": "2026-05-25T13:00:00Z",
            "X-RateLimit-Policy": "sliding_window",
        }
        rl = client._parse_rate_limit(resp)
        assert rl is not None
        assert rl.limit == 100
        assert rl.remaining == 95
        assert rl.policy == "sliding_window"

    def test_parse_missing_headers_returns_none(self, client: TendersaClient) -> None:
        resp = MagicMock(spec=httpx.Response)
        resp.headers = {}
        rl = client._parse_rate_limit(resp)
        assert rl is not None
        assert rl.limit == 0

    def test_parse_invalid_header_values(self, client: TendersaClient) -> None:
        resp = MagicMock(spec=httpx.Response)
        resp.headers = {"X-RateLimit-Limit": "abc"}
        rl = client._parse_rate_limit(resp)
        assert rl is None


# ── Meta Parsing ────────────────────────────────────────────────────────────

class TestMetaParsing:
    def test_parse_full_meta(self, client: TendersaClient, sample_meta: dict) -> None:
        meta = client._parse_meta(sample_meta)
        assert meta.request_id == "req_001"
        assert meta.page == 1
        assert meta.page_size == 20
        assert meta.total_count == 100
        assert meta.has_next is True
        assert meta.rate_limit is not None
        assert meta.rate_limit.limit == 100

    def test_parser_with_underscore_keys(self, client: TendersaClient) -> None:
        raw = {
            "request_id": "r1",
            "timestamp": "now",
            "api_version": "v2",
        }
        meta = client._parse_meta(raw)
        assert meta.request_id == "r1"
        assert meta.api_version == "v2"

    def test_parse_empty_meta(self, client: TendersaClient) -> None:
        meta = client._parse_meta({})
        assert meta.request_id == ""


# ── API Request Error Handling ──────────────────────────────────────────────

class TestRequestErrorHandling:
    def _make_mock_resp(self, status_code: int, json_data: dict) -> MagicMock:
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = status_code
        resp.json.return_value = json_data
        resp.headers = {}
        return resp

    @pytest.mark.asyncio
    async def test_http_400_raises_bad_request(self, client: TendersaClient) -> None:
        with patch.object(client._client, "request", new_callable=AsyncMock) as mock_req:
            resp = self._make_mock_resp(400, {
                "error": "Bad Request",
                "message": "Invalid parameters",
                "requestId": "req_001",
                "code": "BAD_REQUEST",
            })
            mock_req.return_value = resp
            with pytest.raises(BadRequestError) as exc:
                await client.get("/test")
            assert "Invalid parameters" in str(exc.value)

    @pytest.mark.asyncio
    async def test_http_401_raises_auth_error(self, client: TendersaClient) -> None:
        with patch.object(client._client, "request", new_callable=AsyncMock) as mock_req:
            resp = self._make_mock_resp(401, {"message": "Invalid API key", "requestId": "req_001"})
            mock_req.return_value = resp
            with pytest.raises(AuthError):
                await client.get("/test")

    @pytest.mark.asyncio
    async def test_http_404_raises_not_found(self, client: TendersaClient) -> None:
        with patch.object(client._client, "request", new_callable=AsyncMock) as mock_req:
            resp = self._make_mock_resp(404, {"message": "Not found", "requestId": "req_001"})
            mock_req.return_value = resp
            with pytest.raises(NotFoundError):
                await client.get("/test")

    @pytest.mark.asyncio
    async def test_http_429_raises_rate_limit_error(self, client: TendersaClient) -> None:
        with patch.object(client._client, "request", new_callable=AsyncMock) as mock_req:
            resp = self._make_mock_resp(429, {
                "message": "Rate limit exceeded",
                "requestId": "req_001",
                "details": {"limit": 100, "used": 100, "resetsAt": "13:00", "tier": "free"},
            })
            mock_req.return_value = resp
            with pytest.raises(RateLimitError) as exc:
                await client.get("/test")
            assert exc.value.limit == 100
