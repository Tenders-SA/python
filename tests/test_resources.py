from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from tendersa.resources.tenders import TendersResource


@pytest.fixture
def mock_client():
    c = MagicMock()
    c._get_list = AsyncMock()
    c._get_single = AsyncMock()
    return c


@pytest.fixture
def tenders(mock_client):
    return TendersResource(mock_client)


class TestTendersList:
    @pytest.mark.asyncio
    async def test_returns_typed_tenders(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True,
            data=[
                {"tender_id": "t1", "title": "Road works", "status": "OPEN"},
                {"tender_id": "t2", "title": "Bridge repair", "status": "OPEN"},
            ],
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v1"),
        )
        result = await tenders.list()
        assert len(result.data) == 2
        assert result.data[0].tender_id == "t1"
        assert result.data[0].title == "Road works"

    @pytest.mark.asyncio
    async def test_empty_list(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True, data=[], meta=MagicMock(request_id="r1", timestamp="t", api_version="v1"),
        )
        result = await tenders.list()
        assert len(result.data) == 0


class TestTendersGet:
    @pytest.mark.asyncio
    async def test_returns_tender_detail(self, tenders, mock_client):
        mock_client._get_single.return_value = MagicMock(
            success=True,
            data={
                "tender_id": "t1",
                "title": "Road works",
                "province": "Western Cape",
                "awards": [{"award_id": "a1", "supplier_name": "BuildCorp"}],
            },
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v1"),
        )
        result = await tenders.get("t1")
        assert result.tender_id == "t1"
        assert result.title == "Road works"
        assert len(result.awards) == 1
        assert result.awards[0].award_id == "a1"


class TestTendersSearch:
    @pytest.mark.asyncio
    async def test_passes_params(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True, data=[], meta=MagicMock(request_id="r1", timestamp="t", api_version="v1"),
        )
        await tenders.search({"q": "roads", "province": "GP"})
        mock_client._get_list.assert_called_with("/tenders/search", params={"q": "roads", "province": "GP"})


class TestTendersDocuments:
    @pytest.mark.asyncio
    async def test_returns_documents(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True,
            data=[{"document_id": "d1", "file_name": "spec.pdf", "download_url": "https://docs.tenders-sa.org/t1/spec.pdf"}],
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v1"),
        )
        result = await tenders.documents("t1")
        assert result.data[0].document_id == "d1"
        assert result.data[0].file_name == "spec.pdf"


class TestTendersAnalysis:
    @pytest.mark.asyncio
    async def test_returns_analysis(self, tenders, mock_client):
        mock_client._get_single.return_value = MagicMock(
            success=True,
            data={"id": "an1", "tender_id": "t1", "quality_score": 0.85, "confidence": 0.9},
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v1"),
        )
        result = await tenders.analysis("t1")
        assert result is not None
        assert result.id == "an1"
        assert result.quality_score == 0.85

    @pytest.mark.asyncio
    async def test_no_analysis_returns_none(self, tenders, mock_client):
        mock_client._get_single.return_value = MagicMock(
            success=True, data={}, meta=MagicMock(request_id="r1", timestamp="t", api_version="v1"),
        )
        result = await tenders.analysis("t1")
        assert result is None


class TestTendersValueEstimate:
    @pytest.mark.asyncio
    async def test_returns_estimate(self, tenders, mock_client):
        mock_client._get_single.return_value = MagicMock(
            success=True,
            data={"id": "ve1", "tender_id": "t1", "estimated_min": 1000000.0, "estimated_max": 5000000.0},
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v1"),
        )
        result = await tenders.value_estimate("t1")
        assert result is not None
        assert result.estimated_min == 1000000.0

    @pytest.mark.asyncio
    async def test_no_estimate_returns_none(self, tenders, mock_client):
        mock_client._get_single.return_value = MagicMock(
            success=True, data={}, meta=MagicMock(request_id="r1", timestamp="t", api_version="v1"),
        )
        result = await tenders.value_estimate("t1")
        assert result is None


class TestTendersAwards:
    @pytest.mark.asyncio
    async def test_returns_awards(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True,
            data=[{"award_id": "a1", "supplier_name": "BuildCorp"}],
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v1"),
        )
        result = await tenders.awards("t1")
        assert result.data[0].award_id == "a1"


class TestTendersTimeline:
    @pytest.mark.asyncio
    async def test_returns_timeline(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True,
            data=[{"event": "published", "label": "Published", "date": "2026-05-01", "type": "milestone"}],
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v1"),
        )
        result = await tenders.timeline("t1")
        assert result.data[0].event == "published"
