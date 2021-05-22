from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from io import BufferedReader
from pathlib import Path
from typing import ClassVar

from databases import Database, DatabaseURL

from ..abstract import Library


@dataclass
class CalibreLibrary(Library):
    DB_PROTOCOL: ClassVar[str] = "sqlite"
    DB_FILE: ClassVar[str] = "metadata.db"

    path: Path
    url: DatabaseURL = field(init=False)
    database: Database = field(init=False)

    def __post_init__(self):
        self.path = Path(self.path).resolve()
        self.url = url = DatabaseURL(
            f"{self.DB_PROTOCOL}:///{self.path / self.DB_FILE}"
        )
        self.database = Database(url)

    @asynccontextmanager
    async def get_book(self, id_: int) -> BufferedReader:
        with (await self._get_book_path(id_)).open("rb") as b:
            yield b

    async def get_book_cover(self, id_: int) -> Path:
        ...

    async def _get_book_path(self, id_: int) -> Path:
        r = await self.database.fetch_one(
            """
            SELECT path, name, format
            FROM (SELECT * FROM books WHERE id = :id) b
            JOIN data AS d ON b.id = d.book
            """,
            dict(id=id_),
        )
        if r is None:
            raise Exception(f"Book {id_} does not exist")
        path, name, ext = r
        return Path(f"{self.path / path / name}.{ext.lower()}")

    async def __aenter__(self) -> Path:
        await self.database.connect()
        return self

    async def __aexit__(self) -> Path:
        await self.database.disconnect
