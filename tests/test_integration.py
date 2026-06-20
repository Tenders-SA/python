from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from tendersa import TendersaClient
from tendersa.retry import retry_with_backoff_async


def _mock_response(status_code=200, json_data=None, headers=None):
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.headers = headers or {}
    resp.json.return_value = json_data or {
        "success": True, "data": {}, "meta": {"requestId": "r1", "timestamp": "t", "apiVersion": "v2"},
    }
    return resp


def _meta(overrides=None):
    m = {"requestId": "r1", "timestamp": "t", "apiVersion": "v2"}
    if overrides:
        m.update(overrides)
    return m


class TestTendersResource:
    @pytest.mark.asyncio
    async def test_list(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"tender_id": "t1", "title": "Roads"}],
                "meta": _meta(),
            })
            result = await c.tenders.list()
            assert len(result.data) == 1
            assert result.data[0].tender_id == "t1"
        await c.close()

    @pytest.mark.asyncio
    async def test_get(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": {"tender_id": "t1", "title": "Roads", "awards": [{"award_id": "a1"}]},
                "meta": _meta(),
            })
            result = await c.tenders.get("t1")
            assert result is not None
            assert result.tender_id == "t1"
        await c.close()

    @pytest.mark.asyncio
    async def test_closing_soon(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True, "data": [], "meta": _meta(),
            })
            result = await c.tenders.closing_soon()
            assert result is not None
        await c.close()

    @pytest.mark.asyncio
    async def test_new_tenders(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True, "data": [], "meta": _meta(),
            })
            result = await c.tenders.new_tenders()
            assert result is not None
        await c.close()

    @pytest.mark.asyncio
    async def test_by_province(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True, "data": [], "meta": _meta(),
            })
            result = await c.tenders.by_province("Gauteng")
            assert result is not None
        await c.close()

    @pytest.mark.asyncio
    async def test_seo(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": {"canonical_url": "https://tenders-sa.org/...", "meta_description": "..."},
                "meta": _meta(),
            })
            result = await c.tenders.seo("t1")
            assert result["canonical_url"] == "https://tenders-sa.org/..."
        await c.close()

    @pytest.mark.asyncio
    async def test_slug(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": {"slug": "road-construction-cpt-2026"},
                "meta": _meta(),
            })
            result = await c.tenders.slug("t1")
            assert result["slug"] == "road-construction-cpt-2026"
        await c.close()


class TestAwardsResource:
    @pytest.mark.asyncio
    async def test_list(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"award_id": "a1", "supplier_name": "Co"}],
                "meta": _meta(),
            })
            result = await c.awards.list()
            assert len(result.data) == 1
            assert result.data[0].award_id == "a1"
        await c.close()

    @pytest.mark.asyncio
    async def test_get(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": {"award_id": "a1", "supplier_name": "Co"},
                "meta": _meta(),
            })
            result = await c.awards.get("a1")
            assert result is not None
            assert result.award_id == "a1"
        await c.close()

    @pytest.mark.asyncio
    async def test_get_not_found(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True, "data": {}, "meta": _meta(),
            })
            result = await c.awards.get("a1")
            assert result is None
        await c.close()

    @pytest.mark.asyncio
    async def test_analytics_by_province(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "data": [{"province": "Gauteng", "total_award_value": 1e7}],
                "meta": _meta(),
            })
            result = await c.awards.analytics_by_province()
            assert result["data"][0]["province"] == "Gauteng"
        await c.close()

    @pytest.mark.asyncio
    async def test_by_tender(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True, "data": [], "meta": _meta(),
            })
            result = await c.awards.by_tender("t1")
            assert result is not None
        await c.close()

    @pytest.mark.asyncio
    async def test_subcontractors(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"award_id": "a1", "subcontractors": [{"name": "SubCo"}]}],
                "meta": _meta(),
            })
            result = await c.awards.subcontractors("a1")
            assert len(result.data) > 0
        await c.close()


class TestCompaniesResource:
    @pytest.mark.asyncio
    async def test_get(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": {
                    "profile": {"name": "BuildCorp", "registration_number": "2020/123456/07"},
                    "awards": [],
                    "directors": [],
                },
                "meta": _meta(),
            })
            result = await c.companies.get("BuildCorp")
            assert result is not None
            assert result.profile.name == "BuildCorp"
        await c.close()

    @pytest.mark.asyncio
    async def test_get_not_found(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True, "data": {}, "meta": _meta(),
            })
            result = await c.companies.get("NotFound")
            assert result is None
        await c.close()

    @pytest.mark.asyncio
    async def test_search(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"name": "BuildCorp", "registration_number": "2020/123456/07"}],
                "meta": _meta(),
            })
            result = await c.companies.search({"q": "Build"})
            assert result.data[0].name == "BuildCorp"
        await c.close()

    @pytest.mark.asyncio
    async def test_top(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"name": "BuildCorp", "total_awards": 50}],
                "meta": _meta(),
            })
            result = await c.companies.top()
            assert result.data[0].name == "BuildCorp"
        await c.close()

    @pytest.mark.asyncio
    async def test_awards(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True, "data": [], "meta": _meta(),
            })
            result = await c.companies.awards("BuildCorp")
            assert result is not None
        await c.close()

    @pytest.mark.asyncio
    async def test_tenders(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True, "data": [], "meta": _meta(),
            })
            result = await c.companies.tenders("BuildCorp")
            assert result is not None
        await c.close()

    @pytest.mark.asyncio
    async def test_directors(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"name": "John Doe", "position": "Director"}],
                "meta": _meta(),
            })
            result = await c.companies.directors("BuildCorp")
            assert len(result.data) > 0
        await c.close()

    @pytest.mark.asyncio
    async def test_contracts(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True, "data": [], "meta": _meta(),
            })
            result = await c.companies.contracts("BuildCorp")
            assert result is not None
        await c.close()

    @pytest.mark.asyncio
    async def test_by_registration(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": {"name": "BuildCorp", "registration_number": "2020/123456/07"},
                "meta": _meta(),
            })
            result = await c.companies.by_registration("2020/123456/07")
            assert result.profile.name == "BuildCorp"
        await c.close()


class TestOrganizationsResource:
    @pytest.mark.asyncio
    async def test_get(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": {"id": "org_1", "name": "Dept Health"},
                "meta": _meta(),
            })
            result = await c.organizations.get("org_1")
            assert result is not None
            assert result.name == "Dept Health"
        await c.close()

    @pytest.mark.asyncio
    async def test_tenders(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"tender_id": "t1", "title": "Roads"}],
                "meta": _meta(),
            })
            result = await c.organizations.tenders("org_1")
            assert result.data[0].tender_id == "t1"
        await c.close()

    @pytest.mark.asyncio
    async def test_list(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True, "data": [], "meta": _meta(),
            })
            result = await c.organizations.list()
            assert result is not None
        await c.close()

    @pytest.mark.asyncio
    async def test_directors(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"name": "Jane Gov", "position": "CFO"}],
                "meta": _meta(),
            })
            result = await c.organizations.directors("org_1")
            assert len(result.data) > 0
        await c.close()


class TestMetaResource:
    @pytest.mark.asyncio
    async def test_status(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": {"healthy": True, "version": "v2", "timestamp": "2026-06-01T00:00:00Z"},
                "meta": _meta(),
            })
            result = await c.meta.status()
            assert result.healthy is True
        await c.close()

    @pytest.mark.asyncio
    async def test_usage(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": {"daily": 10, "monthly": 300, "limit": {"daily": 100}},
                "meta": _meta(),
            })
            result = await c.meta.usage()
            assert result.daily == 10
        await c.close()

    @pytest.mark.asyncio
    async def test_industries(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"id": "ind_1", "industry_name": "Construction", "median_value": 500000.0}],
                "meta": _meta(),
            })
            result = await c.meta.industries()
            assert result is not None
        await c.close()


class TestNewResources:
    @pytest.mark.asyncio
    async def test_categories_list(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"slug": "construction", "name": "Construction", "tender_count": 50}],
                "meta": _meta(),
            })
            result = await c.categories.list()
            assert len(result.data) > 0
        await c.close()

    @pytest.mark.asyncio
    async def test_categories_by_slug(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": {"slug": "construction", "name": "Construction"},
                "meta": _meta(),
            })
            result = await c.categories.by_slug("construction")
            assert result is not None
        await c.close()

    @pytest.mark.asyncio
    async def test_provinces_list(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"name": "Western Cape", "tender_count": 100}],
                "meta": _meta(),
            })
            result = await c.provinces.list()
            assert len(result.data) > 0
        await c.close()

    @pytest.mark.asyncio
    async def test_provinces_health_scores(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"province": "GP", "score": 0.92, "year": 2026}],
                "meta": _meta(),
            })
            result = await c.provinces.health_scores("Gauteng")
            assert len(result.data) > 0
        await c.close()

    @pytest.mark.asyncio
    async def test_directors_list(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"director_id": "d1", "full_name": "John Doe", "organization_id": "org_1"}],
                "meta": _meta(),
            })
            result = await c.directors.list()
            assert len(result.data) > 0
        await c.close()

    @pytest.mark.asyncio
    async def test_directors_get(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": {"director_id": "d1", "full_name": "John Doe", "organization_id": "org_1"},
                "meta": _meta(),
            })
            result = await c.directors.get("dir_1")
            assert result is not None
        await c.close()

    @pytest.mark.asyncio
    async def test_seo_list_articles(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True, "data": [], "meta": _meta(),
            })
            result = await c.seo.list_articles()
            assert result is not None
        await c.close()

    @pytest.mark.asyncio
    async def test_industry_list(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"id": "b1", "industry_name": "Construction", "sample_size": 100}],
                "meta": _meta(),
            })
            result = await c.industry.list()
            assert len(result.data) > 0
        await c.close()

    @pytest.mark.asyncio
    async def test_services_list(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"id": "svc_1", "name": "PDF Extraction", "slug": "pdf-extraction"}],
                "meta": _meta(),
            })
            result = await c.services.list()
            assert len(result.data) > 0
        await c.close()

    @pytest.mark.asyncio
    async def test_ocds_package(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"id": "p1", "name": "Acme Corp", "role": "buyer"}],
                "meta": _meta(),
            })
            result = await c.ocds.list_parties()
            assert len(result.data) > 0
        await c.close()

    @pytest.mark.asyncio
    async def test_intel_list(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"id": "src_1", "name": "Gov Gazette"}],
                "meta": _meta(),
            })
            result = await c.intel.list_sources()
            assert len(result.data) > 0
        await c.close()

    @pytest.mark.asyncio
    async def test_forensic_list(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"id": "fr_1", "supplier_name": "SuspiciousCo", "restriction_type": "Misrepresentation"}],
                "meta": _meta(),
            })
            result = await c.forensic.list_restricted_suppliers()
            assert len(result.data) > 0
        await c.close()

    @pytest.mark.asyncio
    async def test_cipc_enrichment(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": {"id": "enr_1", "name": "BuildCorp", "registration_number": "2020/123456/07"},
                "meta": _meta(),
            })
            result = await c.cipc.get_enrichment("enr_1")
            assert result is not None
        await c.close()

    @pytest.mark.asyncio
    async def test_newsletters_list(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": [{"id": "nl_1", "title": "June 2026", "edition_number": 6, "published_at": "2026-06-01"}],
                "meta": _meta(),
            })
            result = await c.newsletters.list()
            assert len(result.data) > 0
        await c.close()

    @pytest.mark.asyncio
    async def test_documents_get(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": {"id": "d1", "file_name": "spec.pdf"},
                "meta": _meta(),
            })
            result = await c.documents.get("d1")
            assert result is not None
            assert result.id == "d1"
        await c.close()

    @pytest.mark.asyncio
    async def test_documents_download_url(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response(json_data={
                "success": True,
                "data": {"id": "d1", "download_url": "https://docs.tenders-sa.org/t1/spec.pdf"},
                "meta": _meta(),
            })
            result = await c.documents.download_url("d1")
            assert result is not None
        await c.close()


class TestClientPost:
    @pytest.mark.asyncio
    async def test_post(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response()
            result = await c.post("/test", body={"key": "val"})
            assert result["success"] is True
        await c.close()

    @pytest.mark.asyncio
    async def test_post_forwards_body(self):
        c = TendersaClient("test_key")
        with patch.object(c._client, "request", new_callable=AsyncMock) as mock_req:
            mock_req.return_value = _mock_response()
            await c.post("/test", body={"key": "val"})
            mock_req.assert_called_with(
                method="POST",
                url="https://api.tenders-sa.org/v2/test",
                params=None,
                json={"key": "val"},
            )
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
                    "apiVersion": "v2",
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
