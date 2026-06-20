from __future__ import annotations

import builtins
from typing import Any

from .._types import ApiResponse, Article, Author


class SeoResource:
    def __init__(self, client) -> None:
        self._client = client

    async def category(self, slug: str) -> dict:
        raw = await self._client._get_single(f"/seo/category/{slug}")
        return raw.data

    async def province(self, slug: str) -> dict:
        raw = await self._client._get_single(f"/seo/province/{slug}")
        return raw.data

    async def list_articles(
        self,
        params: dict[str, Any] | None = None,
    ) -> ApiResponse[builtins.list[Article]]:
        raw = await self._client._get_list("/articles", params=params)
        items = [Article(**a) if isinstance(a, dict) else a for a in raw.data]
        return ApiResponse(raw.success, items, raw.meta)

    async def get_article(self, article_id: str) -> Article | None:
        raw = await self._client._get_single(f"/articles/{article_id}")
        if not raw.data:
            return None
        return Article(**raw.data)

    async def get_author(self, author_id: str) -> Author | None:
        raw = await self._client._get_single(f"/authors/{author_id}")
        if not raw.data:
            return None
        return Author(**raw.data)
