from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Generic, TypeVar

from ._types import ApiResponse, Meta

T = TypeVar("T")


class PaginatedResponse(Generic[T]):
    def __init__(self, items: list[T], meta: Meta) -> None:
        self.items = items
        self.meta = meta

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __bool__(self):
        return bool(self.items)

    @property
    def total_count(self) -> int | None:
        return self.meta.total_count

    @property
    def total_pages(self) -> int | None:
        return self.meta.total_pages

    @property
    def has_next(self) -> bool:
        return self.meta.has_next or False

    @property
    def has_prev(self) -> bool:
        return self.meta.has_prev or False

    @property
    def page(self) -> int | None:
        return self.meta.page

    @property
    def page_size(self) -> int | None:
        return self.meta.page_size


class PaginatedAsyncIterator(Generic[T]):
    def __init__(
        self,
        fetcher,
        params: dict | None = None,
        max_pages: int | None = None,
    ) -> None:
        self._fetcher = fetcher
        self._params = dict(params) if params else {}
        self._max_pages = max_pages
        self._current_page = (
            self._params.pop("page", 1) or 1
        )
        self._fetched_pages = 0
        self._done = False
        self._current = None

    def __aiter__(self) -> AsyncIterator[PaginatedResponse[T]]:
        return self._pages()

    async def _pages(self) -> AsyncIterator[PaginatedResponse[T]]:
        if isinstance(self._current_page, str):
            self._current_page = int(self._current_page)
        while not self._done:
            if self._max_pages is not None and self._fetched_pages >= self._max_pages:
                break
            params = {**self._params, "page": self._current_page}
            resp: ApiResponse[list[T]] = await self._fetcher(params)
            page = PaginatedResponse(resp.data, resp.meta)
            self._current = page
            self._fetched_pages += 1
            yield page
            if not resp.meta.has_next:
                self._done = True
            self._current_page += 1
