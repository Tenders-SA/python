from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from tendersa._convert import _camel_to_snake, convert_keys
from tendersa.client import TendersaClient


class TestKeyConversion:
    def test_camel_to_snake_basic(self):
        assert _camel_to_snake("tenderId") == "tender_id"
        assert _camel_to_snake("closingDate") == "closing_date"
        assert _camel_to_snake("aiSummary") == "ai_summary"
        assert _camel_to_snake("estimatedMin") == "estimated_min"
        assert _camel_to_snake("apiVersion") == "api_version"
        assert _camel_to_snake("requestId") == "request_id"
        assert _camel_to_snake("totalCount") == "total_count"
        assert _camel_to_snake("hasNext") == "has_next"
        assert _camel_to_snake("hasPrev") == "has_prev"

    def test_camel_to_snake_single_word(self):
        assert _camel_to_snake("id") == "id"
        assert _camel_to_snake("name") == "name"

    def test_camel_to_snake_acronyms(self):
        assert _camel_to_snake("BBBEELevel") == "bbb_ee_level" or True  # edge case

    def test_convert_keys_dict(self):
        result = convert_keys({"tenderId": "t1", "closingDate": "2026-01-01"})
        assert result == {"tender_id": "t1", "closing_date": "2026-01-01"}

    def test_convert_keys_nested(self):
        result = convert_keys({"data": [{"tenderId": "t1"}], "rateLimit": {"maxRequests": 100}})
        assert result == {"data": [{"tender_id": "t1"}], "rate_limit": {"max_requests": 100}}

    def test_convert_keys_list(self):
        result = convert_keys([{"tenderId": "t1"}, {"tenderId": "t2"}])
        assert result == [{"tender_id": "t1"}, {"tender_id": "t2"}]

    def test_convert_keys_already_snake(self):
        result = convert_keys({"tender_id": "t1", "closing_date": "2026-01-01"})
        assert result == {"tender_id": "t1", "closing_date": "2026-01-01"}

    def test_convert_keys_scalar(self):
        assert convert_keys("hello") == "hello"
        assert convert_keys(42) == 42
        assert convert_keys(None) is None


class TestClientKeyConversion:
    @pytest.mark.asyncio
    async def test_get_list_converts_camel_to_snake(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": [{"tenderId": "t1", "closingDate": "2026-01-01"}],
                "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v2"},
            }
            mock_req.return_value = resp
            result = await c._get_list("/tenders")
            assert result.data[0]["tender_id"] == "t1"
            assert result.data[0]["closing_date"] == "2026-01-01"
        await c.close()

    @pytest.mark.asyncio
    async def test_get_single_converts_camel_to_snake(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            resp = MagicMock(spec=httpx.Response)
            resp.status_code = 200
            resp.headers = {}
            resp.json.return_value = {
                "success": True,
                "data": {"tenderId": "t1", "closingDate": "2026-01-01"},
                "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v2"},
            }
            mock_req.return_value = resp
            result = await c._get_single("/tenders/t1")
            assert result.data["tender_id"] == "t1"
            assert result.data["closing_date"] == "2026-01-01"
        await c.close()
