# tendersa-sdk (Python) — Agent Instructions

**Path**: `api-sdk-packages/python/` | **Published**: [PyPI](https://pypi.org/project/tendersa-sdk/) | **Repo**: [github.com/Tenders-SA/python](https://github.com/Tenders-SA/python)

## What It Is
Async Python SDK for the Tenders-SA Developer API. Uses `httpx.AsyncClient`. Currently in alpha (0.1.0a0).

## Quick Start
```bash
pip install -e .          # or: uv pip install -e .
pytest                    # run tests
ruff check src/ tests/    # lint
mypy src/                 # type check
hatch build               # build wheel
hatch publish             # publish to PyPI
```

## Key Files
| File | Purpose |
|------|---------|
| `src/tendersa/client.py` | `TendersaClient` — async context manager, rate limiting, pagination |
| `src/tendersa/resources/*.py` | Resource modules: tenders, awards, companies, organizations, meta |
| `src/tendersa/_types.py` | Type definitions: `ApiResponse`, `Meta`, `RateLimit` |
| `src/tendersa/_convert.py` | Snake_case ↔ camelCase key conversion |
| `src/tendersa/errors.py` | Error hierarchy (9 classes) |
| `src/tendersa/pagination.py` | `PaginatedAsyncIterator` |
| `src/tendersa/retry.py` | Retry logic |
| `src/tendersa/py.typed` | PEP 561 marker |

## Architecture Notes
- **Async-only** — uses `httpx.AsyncClient` (not `requests`)
- **Key conversion**: auto camelCase → snake_case on API responses
- **Resource pattern**: `client.tenders.list()`, `client.companies.get(name)`
- **Rate limiting**: tracked via `client.last_rate_limit`
- **Context manager**: `async with TendersaClient(api_key) as client:`
- **Alpha status**: v0.1.0a0, no automated publish in CI

## Published
- v0.1.0a0 (alpha)
