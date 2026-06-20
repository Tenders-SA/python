# Tenders-SA Python SDK

Official Python SDK for the [Tenders-SA Developer API v2](https://tenders-sa.org/developers) — enriched South African public procurement data.

---

## About Tenders-SA

[Tenders-SA.org](https://www.tenders-sa.org) is an **AI-powered tender matching and application platform** for South African businesses. It aggregates tenders from national, provincial, and municipal government departments, SOEs (Eskom, Transnet, SANRAL), and public entities — sourced directly from official OCDS (Open Contracting Data Standard) feeds.

The platform goes beyond simple aggregation: AI enrichment extracts key requirements, generates summaries, estimates tender values, classifies categories, and calculates compatibility scores between your company profile and each opportunity. The result is a unified intelligence layer over South Africa's fragmented public procurement landscape.

### Key Platform Features

- **Tender Discovery** — Search and filter thousands of active, closed, and awarded tenders across all provinces and categories
- **AI Enrichment** — Every tender is processed through AI pipelines for summarisation, requirement extraction, value estimation, and classification
- **Company Intelligence** — Research award histories, track supplier performance, and perform due diligence
- **Organisation Profiles** — Procurement body profiles enriched with Google and Wikidata data
- **Award Analytics** — Analyse award patterns by enterprise type, BEE level, province, and category
- **Tender Toolkit** — BBBEE Calculator, Readiness Assessment, Market Heatmap, AI Proposal Generator

### Use Cases

- **Market Research** — Analyse tender volumes, award patterns, and spending trends across provinces and sectors
- **Competitive Intelligence** — Track which companies are winning contracts in your industry
- **Supplier Discovery** — Find subcontractors and partners by analysing award histories
- **Compliance Monitoring** — Monitor procurement opportunities in specific categories or regions

---

## About the Developer API v2

The Tenders-SA Developer API v2 exposes enriched procurement data through a comprehensive set of RESTful endpoints. It serves from a dedicated infrastructure layer with its own database, synced from the main platform, ensuring the API remains fast and available independently of the main web application.

### API Base URL

```
https://api.tenders-sa.org/v2
```

### Authentication

All API requests require a Bearer token passed via the `Authorization` header:

```
Authorization: Bearer tsa_prod_YOUR_API_KEY
```

API keys are generated through the [Developer Portal](https://tenders-sa.org/developers/api-keys). Keys use the format `tsa_prod_` followed by a unique generated string.

**Access Requirements:** API access requires a [Professional or Enterprise subscription](https://tenders-sa.org/pricing).

| Plan | Max Keys | Daily Limit | Monthly Limit |
|------|----------|-------------|---------------|
| Professional | 3 | 500 | 15,000 |
| Enterprise | 25 | 10,000 | 300,000 |

### Response Format

All API responses follow a consistent envelope:

**Success:**
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "requestId": "req_uuid",
    "timestamp": "2026-01-01T00:00:00Z",
    "apiVersion": "v2",
    "page": 1,
    "pageSize": 20,
    "totalCount": 142,
    "totalPages": 8,
    "hasNext": true,
    "hasPrev": false,
    "rateLimit": {
      "limit": 500,
      "remaining": 498,
      "reset": "2026-01-02T00:00:00Z",
      "policy": "daily"
    }
  }
}
```

### Rate Limiting

Rate limit status is returned in both response headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `X-RateLimit-Policy`) and the response body's `meta.rateLimit` object. When exceeded, a `429` status is returned.

### Error Codes

| Status | Code | Description |
|--------|------|-------------|
| 400 | `BAD_REQUEST` | Invalid request parameters |
| 401 | `UNAUTHORIZED` | Missing or invalid API key |
| 403 | `FORBIDDEN` / `KEY_NOT_ACTIVE` / `KEY_EXPIRED` | Key not active or expired |
| 404 | `NOT_FOUND` | Resource not found |
| 409 | `CONFLICT` / `KEY_LIMIT_REACHED` | Key limit reached for plan |
| 429 | `RATE_LIMIT_DAILY_EXCEEDED` / `RATE_LIMIT_MONTHLY_EXCEEDED` | Rate limit exceeded |
| 500 | `INTERNAL_ERROR` | Server error |
| 502 | `SERVICE_UNAVAILABLE` | Service temporarily unavailable |

---

## Installation

```bash
pip install tendersa-sdk
```

### Requirements

- Python 3.9+
- httpx 0.27+

---

## Quick Start

```python
import asyncio
from tendersa import TendersaClient

async def main():
    client = TendersaClient(api_key="tsa_prod_your_key")

    # List open tenders
    tenders = await client.tenders.list({"status": "OPEN", "province": "Western Cape"})
    for t in tenders.data:
        print(t.title, t.status)

    # Get tender detail
    detail = await client.tenders.get("tender_001")
    print(detail.title, detail.estimated_value)

    # AI-powered search
    results = await client.tenders.search({"q": "road construction"})

    await client.close()

asyncio.run(main())
```

---

## Usage

### Creating a Client

```python
from tendersa import TendersaClient

client = TendersaClient(
    api_key="tsa_prod_your_key",
    base_url="https://api.tenders-sa.org/v2",  # default
    timeout=30.0,                               # 30s (default)
    max_retries=3,                              # exponential backoff (default)
)
```

The client also supports async context manager usage:

```python
async with TendersaClient(api_key="tsa_prod_your_key") as client:
    result = await client.tenders.list({"status": "OPEN"})
```

### Resources

The SDK is organised into **16 resource classes**, accessed as properties on the client.

#### Tenders — `client.tenders`

Full tender discovery, filtering, search, and detail.

```python
# List with filters
result = await client.tenders.list({
    "status": "OPEN",
    "category": "Construction",
    "province": "Gauteng",
    "sort": "-closingDate",
})

# Search
results = await client.tenders.search({"q": "road construction"})

# Filtered lists
closing = await client.tenders.closing_soon()
new = await client.tenders.new_tenders()
bbbee = await client.tenders.bbbee_required()
by_province = await client.tenders.by_province("Gauteng", {"status": "OPEN"})
by_org = await client.tenders.by_organization("org_001")

# Value range
range_results = await client.tenders.value_range(1_000_000, 10_000_000)

# Counts
prov_counts = await client.tenders.counts_by_province()
cat_counts = await client.tenders.counts_by_category()
org_counts = await client.tenders.counts_by_organization()
status_counts = await client.tenders.counts_by_status()

# Sub-resources
detail = await client.tenders.get("tender_001")
docs = await client.tenders.documents("tender_001")
awards = await client.tenders.awards("tender_001")
timeline = await client.tenders.timeline("tender_001")
contracts = await client.tenders.contracts("tender_001")
milestones = await client.tenders.milestones("tender_001")
bidders = await client.tenders.bidders("tender_001")
sub_req = await client.tenders.submission_requirements("tender_001")
related = await client.tenders.related("tender_001")

# AI analysis
analysis = await client.tenders.analysis("tender_001")
estimate = await client.tenders.value_estimate("tender_001")

# SEO and slug
seo_data = await client.tenders.seo("tender_001")
slug_data = await client.tenders.slug("tender_001")
```

#### Awards — `client.awards`

Award data and market analytics.

```python
result = await client.awards.list({"province": "Western Cape", "beeLevel": "Level 1"})
award = await client.awards.get("award_001")

# Filtered lists
by_tender = await client.awards.by_tender("tender_001")
by_supplier = await client.awards.by_supplier("BuildCorp SA")
by_date = await client.awards.by_date_range({"from": "2025-01-01", "to": "2025-12-31"})

# Analytics
analytics = await client.awards.analytics({"groupBy": "province"})
by_prov = await client.awards.analytics_by_province({"from": "2025-01-01"})
by_cat = await client.awards.analytics_by_category()
by_bee = await client.awards.analytics_by_bee_level()
by_ent = await client.awards.analytics_by_enterprise_type()

# Subcontractors
subs = await client.awards.subcontractors("award_001")
```

#### Companies — `client.companies`

Supplier/contractor intelligence.

```python
# Profile (includes awards + directors)
company = await client.companies.get("BuildCorp SA")
print(company.profile.name, company.profile.total_awards)
print(company.awards[0].supplier_name)

# Search
results = await client.companies.search({"q": "Construction", "beeLevel": "Level 1"})

# List all companies
all_companies = await client.companies.list({"province": "Gauteng"})

# Top companies
top = await client.companies.top()

# Lookup by registration number
by_reg = await client.companies.by_registration("2020/123456/07")

# Sub-resources
awards = await client.companies.awards("BuildCorp SA")
contracts = await client.companies.contracts("BuildCorp SA")
tenders = await client.companies.tenders("BuildCorp SA")
directors = await client.companies.directors("BuildCorp SA")
```

#### Organizations — `client.organizations`

Government departments and procurement bodies.

```python
org = await client.organizations.get("org_001")
tenders = await client.organizations.tenders("org_001", {"status": "OPEN"})

# List, search, and lookups
orgs = await client.organizations.list()
results = await client.organizations.search({"q": "Health"})
by_slug = await client.organizations.by_slug("dept-health")
by_reg = await client.organizations.by_registration("123456")
counts = await client.organizations.counts_by_type()
directors = await client.organizations.directors("org_001")
```

#### Directors — `client.directors`

Company director information from CIPC sources.

```python
directors = await client.directors.list({"fullName": "John"})
director = await client.directors.get("dir_001")
results = await client.directors.search({"q": "Smith"})
by_org = await client.directors.by_organization("org_001")
```

#### Categories — `client.categories`

Tender category reference data.

```python
categories = await client.categories.list()
category = await client.categories.get("cat_001")
by_slug = await client.categories.by_slug("construction")
```

#### Provinces — `client.provinces`

Province data with health scores.

```python
provinces = await client.provinces.list()
province = await client.provinces.get("gauteng")
scores = await client.provinces.health_scores("gauteng")
```

#### SEO & Content — `client.seo`

SEO metadata and content.

```python
cat_seo = await client.seo.category("construction")
prov_seo = await client.seo.province("gauteng")
articles = await client.seo.list_articles({"limit": 10})
article = await client.seo.get_article("article_001")
author = await client.seo.get_author("author_001")
```

#### Industry — `client.industry`

Industry value benchmarks.

```python
benchmarks = await client.industry.list()
benchmark = await client.industry.get("bench_001")
```

#### Services — `client.services`

Service type classifications.

```python
services = await client.services.list()
service = await client.services.get("consulting")
```

#### OCDS — `client.ocds`

Open Contracting Data Standard parties.

```python
parties = await client.ocds.list_parties({"role": "buyer"})
party = await client.ocds.get_party("party_001")
```

#### Intelligence — `client.intel`

Market alerts and sector insights.

```python
sources = await client.intel.list_sources()
source = await client.intel.get_source("src_001")
items = await client.intel.list_items({"category": "energy"})
item = await client.intel.get_item("item_001")
```

#### Forensic — `client.forensic`

Restricted supplier screening.

```python
suppliers = await client.forensic.list_restricted_suppliers()
supplier = await client.forensic.get_restricted_supplier("rs_001")
matches = await client.forensic.match_restricted_supplier({"name": "Acme Corp"})
result = await client.forensic.check_restricted_supplier({"name": "Acme Corp"})
```

#### CIPC — `client.cipc`

Companies and Intellectual Property Commission data.

```python
enrichments = await client.cipc.list_enrichments({"supplierName": "Build"})
enrichment = await client.cipc.get_enrichment("enr_001")
directors = await client.cipc.list_directors({"companyName": "BuildCorp"})
director = await client.cipc.get_director("dir_001")
```

#### Newsletters — `client.newsletters`

Newsletter editions.

```python
editions = await client.newsletters.list()
edition = await client.newsletters.get("nl_001")
```

#### Documents — `client.documents`

Tender document metadata and download URLs.

```python
doc = await client.documents.get("doc_001")
url = await client.documents.download_url("doc_001", {"requireR2": "1"})
```

#### Meta — `client.meta`

API status, usage, and reference data.

```python
status = await client.meta.status()
provinces = await client.meta.provinces()
categories = await client.meta.categories()
usage = await client.meta.usage()
industries = await client.meta.industries()
```

### Pagination

List endpoints support async iteration through pages:

```python
async for page in client.tenders.paginated({
    "status": "OPEN",
    "category": "Construction",
}):
    for tender in page:
        print(tender.title, tender.closing_date)
```

Each page is a `PaginatedResponse` object with convenience properties:

```python
async for page in client.awards.paginated({"province": "Gauteng"}, max_pages=5):
    print(f"Page {page.page}: {len(page)} items")
    print(f"  Total: {page.total_count}, Has next: {page.has_next}")
```

### Error Handling

The SDK throws typed exceptions for every API response status:

```python
from tendersa.errors import (
    TendersaError,
    AuthError,
    NotFoundError,
    RateLimitError,
    BadRequestError,
    ForbiddenError,
    ConflictError,
    InternalError,
    ServiceUnavailableError,
)

try:
    tender = await client.tenders.get("nonexistent")
except AuthError:
    print("Invalid API key. Get one at https://tenders-sa.org/developers/api-keys")
except NotFoundError:
    print("Tender not found")
except RateLimitError as e:
    print(f"Rate limited: {e.used}/{e.limit}. Resets at {e.resets_at}")
except TendersaError as e:
    print(f"API error [{e.code}]: {e.message} (request: {e.request_id})")
```

Every exception exposes:
- `status` — HTTP status code
- `code` — Machine-readable error code
- `message` — Human-readable description
- `request_id` — For tracing with support
- `docs` — Link to error documentation

### Rate Limit Tracking

```python
rl = client.last_rate_limit
if rl:
    print(f"{rl.remaining}/{rl.limit} requests remaining ({rl.policy})")
```

---

## Resources API Reference

### Tenders — `client.tenders`
| Method | Endpoint |
|--------|----------|
| `list(params?)` | `GET /v2/tenders` |
| `get(id)` | `GET /v2/tenders/{id}` |
| `search(params)` | `GET /v2/tenders/search` |
| `closing_soon(params?)` | `GET /v2/tenders/closing-soon` |
| `new_tenders(params?)` | `GET /v2/tenders/new` |
| `bbbee_required(params?)` | `GET /v2/tenders/bbbee-required` |
| `value_range(min, max, params?)` | `GET /v2/tenders/value-range` |
| `by_province(province, params?)` | `GET /v2/tenders/by-province/{province}` |
| `by_organization(orgId, params?)` | `GET /v2/tenders/by-organization/{orgId}` |
| `by_publication_type(type, params?)` | `GET /v2/tenders/by-publication-type/{type}` |
| `by_category(category, params?)` | `GET /v2/tenders/by-category/{category}` |
| `counts_by_province()` | `GET /v2/tenders/counts/province` |
| `counts_by_category()` | `GET /v2/tenders/counts/category` |
| `counts_by_organization()` | `GET /v2/tenders/counts/organization` |
| `counts_by_status()` | `GET /v2/tenders/counts/status` |
| `contracts(id)` | `GET /v2/tenders/{id}/contracts` |
| `milestones(id)` | `GET /v2/tenders/{id}/milestones` |
| `bidders(id)` | `GET /v2/tenders/{id}/bidders` |
| `submission_requirements(id)` | `GET /v2/tenders/{id}/submission-requirements` |
| `documents(id)` | `GET /v2/tenders/{id}/documents` |
| `awards(id)` | `GET /v2/tenders/{id}/awards` |
| `timeline(id)` | `GET /v2/tenders/{id}/timeline` |
| `analysis(id)` | `GET /v2/tenders/{id}/analysis` |
| `value_estimate(id)` | `GET /v2/tenders/{id}/value-estimate` |
| `seo(id)` | `GET /v2/tenders/{id}/seo` |
| `slug(id)` | `GET /v2/tenders/{id}/slug` |
| `related(id, params?)` | `GET /v2/tenders/{id}/related` |
| `paginated(params?)` | (async iterator) |

### Awards — `client.awards`
| Method | Endpoint |
|--------|----------|
| `list(params?)` | `GET /v2/awards` |
| `get(id)` | `GET /v2/awards/{id}` |
| `by_tender(tenderId, params?)` | `GET /v2/awards/by-tender/{tenderId}` |
| `by_supplier(name, params?)` | `GET /v2/awards/by-supplier/{name}` |
| `by_supplier_party(partyId, params?)` | `GET /v2/awards/by-supplier-party/{partyId}` |
| `by_date_range(params)` | `GET /v2/awards/by-date-range` |
| `analytics(params)` | `GET /v2/awards/analytics` |
| `analytics_by_province(params?)` | `GET /v2/awards/analytics/province` |
| `analytics_by_category(params?)` | `GET /v2/awards/analytics/category` |
| `analytics_by_bee_level(params?)` | `GET /v2/awards/analytics/bee-level` |
| `analytics_by_enterprise_type(params?)` | `GET /v2/awards/analytics/enterprise-type` |
| `subcontractors(id, params?)` | `GET /v2/awards/{id}/subcontractors` |

### Companies (Suppliers) — `client.companies`
| Method | Endpoint |
|--------|----------|
| `list(params?)` | `GET /v2/companies` |
| `get(name)` | `GET /v2/companies/{name}` |
| `search(params)` | `GET /v2/companies/search` |
| `top(params?)` | `GET /v2/companies/top` |
| `by_registration(reg)` | `GET /v2/companies/by-registration/{reg}` |
| `awards(name, params?)` | `GET /v2/companies/{name}/awards` |
| `contracts(name, params?)` | `GET /v2/companies/{name}/contracts` |
| `tenders(name, params?)` | `GET /v2/companies/{name}/tenders` |
| `directors(name)` | `GET /v2/companies/{name}/directors` |

### Organizations — `client.organizations`
| Method | Endpoint |
|--------|----------|
| `list(params?)` | `GET /v2/organizations` |
| `get(id)` | `GET /v2/organizations/{id}` |
| `search(params)` | `GET /v2/organizations/search` |
| `by_slug(slug)` | `GET /v2/organizations/by-slug/{slug}` |
| `by_registration(reg)` | `GET /v2/organizations/by-registration/{reg}` |
| `counts_by_type()` | `GET /v2/organizations/counts-by-type` |
| `tenders(id, params?)` | `GET /v2/organizations/{id}/tenders` |
| `directors(id, params?)` | `GET /v2/organizations/{id}/directors` |

### Directors — `client.directors`
| Method | Endpoint |
|--------|----------|
| `list(params?)` | `GET /v2/directors` |
| `get(id)` | `GET /v2/directors/{id}` |
| `search(params)` | `GET /v2/directors/search` |
| `by_organization(orgId, params?)` | `GET /v2/directors/by-organization/{orgId}` |

### Categories — `client.categories`
| Method | Endpoint |
|--------|----------|
| `list()` | `GET /v2/categories` |
| `get(id)` | `GET /v2/categories/{id}` |
| `by_slug(slug)` | `GET /v2/categories/by-slug/{slug}` |

### Provinces — `client.provinces`
| Method | Endpoint |
|--------|----------|
| `list()` | `GET /v2/provinces` |
| `get(slug)` | `GET /v2/provinces/{slug}` |
| `health_scores(slug)` | `GET /v2/provinces/{slug}/health-scores` |

### SEO & Content — `client.seo`
| Method | Endpoint |
|--------|----------|
| `category(slug)` | `GET /v2/seo/category/{slug}` |
| `province(slug)` | `GET /v2/seo/province/{slug}` |
| `list_articles(params?)` | `GET /v2/articles` |
| `get_article(id)` | `GET /v2/articles/{id}` |
| `get_author(id)` | `GET /v2/authors/{id}` |

### Industry — `client.industry`
| Method | Endpoint |
|--------|----------|
| `list()` | `GET /v2/industry/benchmarks` |
| `get(id)` | `GET /v2/industry/benchmarks/{id}` |

### Services — `client.services`
| Method | Endpoint |
|--------|----------|
| `list()` | `GET /v2/services` |
| `get(slug)` | `GET /v2/services/{slug}` |

### OCDS — `client.ocds`
| Method | Endpoint |
|--------|----------|
| `list_parties(params?)` | `GET /v2/ocds/parties` |
| `get_party(id)` | `GET /v2/ocds/parties/{id}` |

### Intelligence — `client.intel`
| Method | Endpoint |
|--------|----------|
| `list_sources()` | `GET /v2/intel/sources` |
| `get_source(id)` | `GET /v2/intel/sources/{id}` |
| `list_items(params?)` | `GET /v2/intel/items` |
| `get_item(id)` | `GET /v2/intel/items/{id}` |

### Forensic — `client.forensic`
| Method | Endpoint |
|--------|----------|
| `list_restricted_suppliers(params?)` | `GET /v2/forensic/restricted-suppliers` |
| `get_restricted_supplier(id)` | `GET /v2/forensic/restricted-suppliers/{id}` |
| `match_restricted_supplier(params)` | `GET /v2/forensic/restricted-suppliers/match` |
| `check_restricted_supplier(params)` | `GET /v2/forensic/restricted-suppliers/check` |

### CIPC — `client.cipc`
| Method | Endpoint |
|--------|----------|
| `list_enrichments(params?)` | `GET /v2/cipc/enrichments` |
| `get_enrichment(id)` | `GET /v2/cipc/enrichments/{id}` |
| `list_directors(params?)` | `GET /v2/cipc/directors` |
| `get_director(id)` | `GET /v2/cipc/directors/{id}` |

### Newsletters — `client.newsletters`
| Method | Endpoint |
|--------|----------|
| `list(params?)` | `GET /v2/newsletters` |
| `get(id)` | `GET /v2/newsletters/{id}` |

### Documents — `client.documents`
| Method | Endpoint |
|--------|----------|
| `get(id)` | `GET /v2/documents/{id}` |
| `download_url(id, params?)` | `GET /v2/documents/{id}/download-url` |

### Meta — `client.meta`
| Method | Endpoint |
|--------|----------|
| `status()` | `GET /v2/meta/status` |
| `provinces()` | `GET /v2/meta/provinces` |
| `categories()` | `GET /v2/meta/categories` |
| `usage()` | `GET /v2/meta/usage` |
| `industries(params?)` | `GET /v2/meta/industries` |

---

## Links

- [Tenders-SA Platform](https://www.tenders-sa.org) — Main website
- [Developer Portal](https://tenders-sa.org/developers) — API keys, docs, and pricing
- [API Documentation](https://tenders-sa.org/developers/docs) — Full API reference
- [API Key Management](https://tenders-sa.org/developers/api-keys) — Create and manage keys
- [Pricing](https://tenders-sa.org/pricing) — Subscription plans
- [GitHub](https://github.com/Tenders-SA/python) — Source code & issues
- [Support](mailto:support@tenders-sa.org) — Email support
- [Developer Contact](mailto:developers@tenders-sa.org) — API & SDK feedback

---

## License

MIT
