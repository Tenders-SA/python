# Tenders-SA Python SDK

Official Python SDK for the [Tenders-SA Developer API](https://tenders-sa.org/developers) — enriched South African public procurement data.

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

## About the Developer API

The Tenders-SA Developer API exposes enriched procurement data through a set of RESTful endpoints. It serves from a dedicated infrastructure layer with its own database, synced from the main platform, ensuring the API remains fast and available independently of the main web application.

### API Base URL

```
https://api.tenders-sa.org/v1
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
    "apiVersion": "v1",
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
    base_url="https://api.tenders-sa.org",  # default
    timeout=30.0,                            # 30s (default)
    max_retries=3,                           # exponential backoff (default)
)
```

The client also supports async context manager usage:

```python
async with TendersaClient(api_key="tsa_prod_your_key") as client:
    result = await client.tenders.list({"status": "OPEN"})
```

### Resources

The SDK is organised into five resource classes, accessed as properties on the client.

#### Tenders

```python
# List with filters
result = await client.tenders.list({
    "status": "OPEN",
    "category": "Construction",
    "province": "Gauteng",
    "sort": "-closingDate",
})

# Get detail
detail = await client.tenders.get("tender_001")

# Sub-resources
docs = await client.tenders.documents("tender_001")
awards = await client.tenders.awards("tender_001")
timeline = await client.tenders.timeline("tender_001")

# AI analysis
analysis = await client.tenders.analysis("tender_001")
estimate = await client.tenders.value_estimate("tender_001")

# Search
results = await client.tenders.search({"q": "road construction"})
```

#### Awards

```python
result = await client.awards.list({
    "province": "Western Cape",
    "beeLevel": "Level 1",
    "minAmount": 1_000_000,
})

award = await client.awards.get("award_001")

analytics = await client.awards.analytics({
    "groupBy": "province",
    "from": "2025-01-01",
    "to": "2025-12-31",
})
```

#### Companies

```python
company = await client.companies.get("BuildCorp SA")

results = await client.companies.search({
    "q": "Construction",
    "beeLevel": "Level 1",
    "province": "Gauteng",
})
```

#### Organisations (Procurement Bodies)

```python
org = await client.organizations.get("org_001")
tenders = await client.organizations.tenders("org_001", {"status": "OPEN"})
```

#### Meta

```python
status = await client.meta.status()
provinces = await client.meta.provinces()
categories = await client.meta.categories()
usage = await client.meta.usage()
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

| Resource | Method | Endpoint |
|----------|--------|----------|
| `client.tenders` | `list(params?)` | `GET /v1/tenders` |
| | `get(id)` | `GET /v1/tenders/{id}` |
| | `search(params)` | `GET /v1/tenders/search` |
| | `documents(id)` | `GET /v1/tenders/{id}/documents` |
| | `awards(id)` | `GET /v1/tenders/{id}/awards` |
| | `timeline(id)` | `GET /v1/tenders/{id}/timeline` |
| | `analysis(id)` | `GET /v1/tenders/{id}/analysis` |
| | `value_estimate(id)` | `GET /v1/tenders/{id}/value-estimate` |
| | `paginated(params?)` | (async iterator) |
| `client.awards` | `list(params?)` | `GET /v1/awards` |
| | `get(id)` | `GET /v1/awards/{id}` |
| | `analytics(params?)` | `GET /v1/awards/analytics` |
| `client.companies` | `get(name)` | `GET /v1/companies/{name}` |
| | `search(params)` | `GET /v1/companies/search` |
| `client.organizations` | `get(id)` | `GET /v1/organizations/{id}` |
| | `tenders(id)` | `GET /v1/organizations/{id}/tenders` |
| `client.meta` | `status()` | `GET /v1/meta/status` |
| | `provinces()` | `GET /v1/meta/provinces` |
| | `categories()` | `GET /v1/meta/categories` |
| | `usage()` | `GET /v1/meta/usage` |

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
