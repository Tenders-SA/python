# Tenders-SA Python SDK

Official Python SDK for the [Tenders-SA Developer API](https://tenders-sa.org/developers) — enriched South African public procurement data.

## Installation

```bash
pip install tendersa-sdk
```

## Quick Start

```python
from tendersa import TendersaClient

client = TendersaClient(api_key="tsa_prod_your_key")

# List open tenders
tenders = await client.tenders.list({"status": "OPEN", "province": "Western Cape"})
for t in tenders.data:
    print(t.title, t.status)

# Get tender detail
detail = await client.tenders.get("tender_001")
print(detail.title, detail.estimated_value)

# Search
results = await client.tenders.search({"q": "road construction"})

# Pagination
async for page in client.tenders.paginated({"status": "OPEN"}):
    for t in page.items:
        print(t.title)
```

## API

### Resources

| Resource | Methods |
|----------|---------|
| `client.tenders` | `list`, `get`, `search`, `documents`, `awards`, `timeline`, `analysis`, `value_estimate`, `paginated` |
| `client.awards` | `list`, `get`, `analytics` |
| `client.companies` | `get`, `search` |
| `client.organizations` | `get`, `tenders` |
| `client.meta` | `status`, `provinces`, `categories`, `usage` |

### Error Handling

```python
from tendersa.errors import AuthError, NotFoundError, RateLimitError

try:
    tender = await client.tenders.get("nonexistent")
except AuthError:
    print("Check your API key")
except NotFoundError:
    print("Tender not found")
except RateLimitError as e:
    print(f"Rate limited. Resets at: {e.resets_at}")
```

## Requirements

- Python 3.9+
- httpx 0.27+

## License

MIT
