from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from io import BufferedReader, BytesIO
from pathlib import Path
from typing import Iterator

from libarchive import SeekableArchive


class Library(ABC):
    @abstractmethod
    async def __aenter__(self) -> Path:
        ...

    @abstractmethod
    async def __aexit__(self) -> Path:
        ...

    @abstractmethod
    async def get_book(self, id_: int) -> BufferedReader:
        ...

    @abstractmethod
    async def get_book_cover(self, id_: int) -> BufferedReader:
        ...

    async def get_book_pages(self, id_: int, sort=True) -> Iterator[str]:
        async with self.get_archive(id_) as a:
            for p in self._get_book_pages(a, sort):
                yield p

    async def get_book_page(self, book_id: int, page_id: int) -> BytesIO:
        async with self.get_archive(book_id) as a:
            return self._get_book_page(a, page_id)

    def _get_book_pages(self, archive: SeekableArchive, sort=True) -> Iterator[str]:
        pages = (e.pathname for e in archive)
        if sort:
            pages = sorted(pages)
        yield from pages

    def _get_book_page(self, archive: SeekableArchive, page_id: int) -> BytesIO:
        count = page_id
        for p in self._get_book_pages(archive):
            if not count:
                page = p
                break
            count -= 1
        else:
            raise KeyError(page_id)

        return BytesIO(archive.read(page))

    @asynccontextmanager
    async def get_archive(self, id_: str) -> SeekableArchive:
        async with self.get_book(id_) as b:
            with SeekableArchive(b) as a:
                yield a
