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
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        result = await tenders.list()
        assert len(result.data) == 2
        assert result.data[0].tender_id == "t1"
        assert result.data[0].title == "Road works"

    @pytest.mark.asyncio
    async def test_empty_list(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True, data=[], meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
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
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
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
            success=True, data=[], meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        await tenders.search({"q": "roads", "province": "GP"})
        mock_client._get_list.assert_called_with("/tenders/search", params={"q": "roads", "province": "GP"})


class TestTendersFilteredLists:
    @pytest.mark.asyncio
    async def test_closing_soon(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True, data=[], meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        await tenders.closing_soon({"limit": 5})
        mock_client._get_list.assert_called_with("/tenders/closing-soon", params={"limit": 5})

    @pytest.mark.asyncio
    async def test_new_tenders(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True, data=[], meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        await tenders.new_tenders()
        mock_client._get_list.assert_called_with("/tenders/new", params=None)

    @pytest.mark.asyncio
    async def test_bbbee_required(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True, data=[], meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        await tenders.bbbee_required()
        mock_client._get_list.assert_called_with("/tenders/bbbee-required", params=None)

    @pytest.mark.asyncio
    async def test_value_range(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True, data=[], meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        await tenders.value_range(1000, 5000)
        mock_client._get_list.assert_called_with("/tenders/value-range", params={"min": 1000, "max": 5000})

    @pytest.mark.asyncio
    async def test_by_province(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True, data=[], meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        await tenders.by_province("Gauteng")
        mock_client._get_list.assert_called_with("/tenders/by-province/Gauteng", params=None)

    @pytest.mark.asyncio
    async def test_counts_by_province(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True,
            data=[{"name": "Gauteng", "count": 50}],
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        result = await tenders.counts_by_province()
        assert result.data[0].name == "Gauteng"
        assert result.data[0].count == 50


class TestTendersSubResources:
    @pytest.mark.asyncio
    async def test_contracts(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True, data=[], meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        result = await tenders.contracts("t1")
        assert result is not None

    @pytest.mark.asyncio
    async def test_milestones(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True, data=[], meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        result = await tenders.milestones("t1")
        assert result is not None

    @pytest.mark.asyncio
    async def test_bidders(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True, data=[], meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        result = await tenders.bidders("t1")
        assert result is not None

    @pytest.mark.asyncio
    async def test_submission_requirements(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True, data=[], meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        result = await tenders.submission_requirements("t1")
        assert result is not None

    @pytest.mark.asyncio
    async def test_seo(self, tenders, mock_client):
        mock_client._get_single.return_value = MagicMock(
            success=True, data={"canonical_url": "https://..."},
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        result = await tenders.seo("t1")
        assert result["canonical_url"] == "https://..."

    @pytest.mark.asyncio
    async def test_slug(self, tenders, mock_client):
        mock_client._get_single.return_value = MagicMock(
            success=True, data={"slug": "road-construction"},
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        result = await tenders.slug("t1")
        assert result["slug"] == "road-construction"

    @pytest.mark.asyncio
    async def test_related(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True, data=[], meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        await tenders.related("t1", {"limit": 5})
        mock_client._get_list.assert_called_with("/tenders/t1/related", params={"limit": 5})


class TestTendersDocuments:
    @pytest.mark.asyncio
    async def test_returns_documents(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True,
            data=[{"document_id": "d1", "file_name": "spec.pdf", "download_url": "https://docs.tenders-sa.org/t1/spec.pdf"}],
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
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
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        result = await tenders.analysis("t1")
        assert result is not None
        assert result.id == "an1"
        assert result.quality_score == 0.85

    @pytest.mark.asyncio
    async def test_no_analysis_returns_none(self, tenders, mock_client):
        mock_client._get_single.return_value = MagicMock(
            success=True, data={}, meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        result = await tenders.analysis("t1")
        assert result is None


class TestTendersValueEstimate:
    @pytest.mark.asyncio
    async def test_returns_estimate(self, tenders, mock_client):
        mock_client._get_single.return_value = MagicMock(
            success=True,
            data={"id": "ve1", "tender_id": "t1", "estimated_min": 1000000.0, "estimated_max": 5000000.0},
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        result = await tenders.value_estimate("t1")
        assert result is not None
        assert result.estimated_min == 1000000.0

    @pytest.mark.asyncio
    async def test_no_estimate_returns_none(self, tenders, mock_client):
        mock_client._get_single.return_value = MagicMock(
            success=True, data={}, meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        result = await tenders.value_estimate("t1")
        assert result is None


class TestTendersAwards:
    @pytest.mark.asyncio
    async def test_returns_awards(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True,
            data=[{"award_id": "a1", "supplier_name": "BuildCorp"}],
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        result = await tenders.awards("t1")
        assert result.data[0].award_id == "a1"


class TestTendersTimeline:
    @pytest.mark.asyncio
    async def test_returns_timeline(self, tenders, mock_client):
        mock_client._get_list.return_value = MagicMock(
            success=True,
            data=[{"event": "published", "label": "Published", "date": "2026-05-01", "type": "milestone"}],
            meta=MagicMock(request_id="r1", timestamp="t", api_version="v2"),
        )
        result = await tenders.timeline("t1")
        assert result.data[0].event == "published"
