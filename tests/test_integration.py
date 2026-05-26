from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from tendersa import TendersaClient
from tendersa.retry import retry_with_backoff_async


class TestAwardsResource:
    @pytest.mark.asyncio
    async def test_list(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": [{"award_id": "a1", "supplier_name": "Co"}],
                "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"},
            }
            mock_req.return_value = resp
            result = await c.awards.list()
            assert len(result.data) == 1
            assert result.data[0].award_id == "a1"
        await c.close()

    @pytest.mark.asyncio
    async def test_get(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": {"award_id": "a1", "supplier_name": "Co"},
                "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"},
            }
            mock_req.return_value = resp
            result = await c.awards.get("a1")
            assert result is not None
            assert result.award_id == "a1"
        await c.close()

    @pytest.mark.asyncio
    async def test_get_not_found(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": {},
                "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"},
            }
            mock_req.return_value = resp
            result = await c.awards.get("a1")
            assert result is None
        await c.close()

    @pytest.mark.asyncio
    async def test_analytics(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {"data": {"total": 100}, "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"}}
            mock_req.return_value = resp
            result = await c.awards.analytics({"year": 2026})
            assert result["data"]["total"] == 100
        await c.close()


class TestCompaniesResource:
    @pytest.mark.asyncio
    async def test_get(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": {"name": "BuildCorp", "total_awards": 5},
                "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"},
            }
            mock_req.return_value = resp
            result = await c.companies.get("comp_1")
            assert result is not None
            assert result.name == "BuildCorp"
        await c.close()

    @pytest.mark.asyncio
    async def test_get_not_found(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": {},
                "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"},
            }
            mock_req.return_value = resp
            result = await c.companies.get("comp_1")
            assert result is None
        await c.close()

    @pytest.mark.asyncio
    async def test_search(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": [{"name": "BuildCorp", "total_awards": 5}],
                "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"},
            }
            mock_req.return_value = resp
            result = await c.companies.search({"q": "Build"})
            assert result.data[0].name == "BuildCorp"
        await c.close()


class TestOrganizationsResource:
    @pytest.mark.asyncio
    async def test_get(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": {"id": "org_1", "name": "Dept Health"},
                "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"},
            }
            mock_req.return_value = resp
            result = await c.organizations.get("org_1")
            assert result is not None
            assert result.name == "Dept Health"
        await c.close()

    @pytest.mark.asyncio
    async def test_tenders(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": [{"tender_id": "t1", "title": "Roads"}],
                "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"},
            }
            mock_req.return_value = resp
            result = await c.organizations.tenders("org_1")
            assert result.data[0].tender_id == "t1"
        await c.close()


class TestMetaResource:
    @pytest.mark.asyncio
    async def test_status(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": {"healthy": True, "version": "v1", "last_sync": {}},
                "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"},
            }
            mock_req.return_value = resp
            result = await c.meta.status()
            assert result.healthy is True
        await c.close()

    @pytest.mark.asyncio
    async def test_provinces(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": [{"name": "Western Cape", "tender_count": 100}],
                "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"},
            }
            mock_req.return_value = resp
            result = await c.meta.provinces()
            assert result[0].name == "Western Cape"
        await c.close()

    @pytest.mark.asyncio
    async def test_categories(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": [{"name": "Construction", "count": 50}],
                "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"},
            }
            mock_req.return_value = resp
            result = await c.meta.categories()
            assert result[0].name == "Construction"
        await c.close()

    @pytest.mark.asyncio
    async def test_usage(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": {"daily": 10, "monthly": 300, "limit": {"daily": 100}},
                "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"},
            }
            mock_req.return_value = resp
            result = await c.meta.usage()
            assert result.daily == 10
        await c.close()


class TestClientPost:
    @pytest.mark.asyncio
    async def test_post(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {"success": True, "data": {}, "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"}}
            mock_req.return_value = resp
            result = await c.post("/test", body={"key": "val"})
            assert result["success"] is True
        await c.close()

    @pytest.mark.asyncio
    async def test_post_forwards_body(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {"success": True, "data": {}, "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v1"}}
            mock_req.return_value = resp
            await c.post("/test", body={"key": "val"})
            mock_req.assert_called_with(method="POST", url="https://api.tenders-sa.org/v1/test", params=None, json={"key": "val"})
        await c.close()


class TestClientContextManager:
    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "aclose", new_callable=AsyncMock) as mock_close:
            async with c as client:
                assert client is c
            mock_close.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_close(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "aclose", new_callable=AsyncMock) as mock_close:
            await c.close()
            mock_close.assert_awaited_once()


class TestRetry:
    @pytest.mark.asyncio
    async def test_does_not_retry_on_success(self):
        call_count = 0

        async def fn():
            nonlocal call_count
            call_count += 1
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            return resp

        await retry_with_backoff_async(fn, max_retries=3)
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_retries_on_timeout(self):
        call_count = 0

        async def fn():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise httpx.TimeoutException("timeout", request=None)
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            return resp

        result = await retry_with_backoff_async(fn, max_retries=3, base_delay=0.01)
        assert call_count == 3
        assert result.status_code == 200

    @pytest.mark.asyncio
    async def test_raises_after_max_retries(self):
        call_count = 0

        async def fn():
            nonlocal call_count
            call_count += 1
            raise httpx.TimeoutException("timeout", request=None)

        with pytest.raises(httpx.TimeoutException):
            await retry_with_backoff_async(fn, max_retries=2, base_delay=0.01)
        assert call_count == 3  # initial + 2 retries

    @pytest.mark.asyncio
    async def test_does_not_retry_on_4xx(self):
        call_count = 0

        async def fn():
            nonlocal call_count
            call_count += 1
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 400
            raise httpx.HTTPStatusError("bad request", request=MagicMock(), response=resp)

        with pytest.raises(httpx.HTTPStatusError):
            await retry_with_backoff_async(fn, max_retries=3, base_delay=0.01)
        assert call_count == 1

    @pytest.mark.asyncio
    async def test_retries_on_5xx(self):
        call_count = 0

        async def fn():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                resp = MagicMock(spec=httpx.Response)
                resp.status_code = 502
                raise httpx.HTTPStatusError("bad gateway", request=MagicMock(), response=resp)
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            return resp

        result = await retry_with_backoff_async(fn, max_retries=3, base_delay=0.01)
        assert call_count == 3
        assert result.status_code == 200

    @pytest.mark.asyncio
    async def test_paginated_async_iterator_pages(self):
        c = TendersaClient("test_key")
        call_count = 0

        async def mock_req(method, url, params, json):
            nonlocal call_count
            call_count += 1
            page = params.get("page", 1)
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": [{"tender_id": f"t{page}"}],
                "meta": {
                    "requestId": "r1",
                    "timestamp": "t",
                    "apiVersion": "v1",
                    "page": page,
                    "pageSize": 20,
                    "totalCount": 3,
                    "totalPages": 3,
                    "hasNext": call_count < 3,
                },
            }
            return resp

        with patch.object(c._client, "request", new_callable=AsyncMock, side_effect=mock_req):
            items = []
            async for page in c.paginated("/tenders", {"status": "OPEN"}):
                items.extend(page.items)
            assert len(items) == 3
        await c.close()
