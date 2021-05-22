from io import BytesIO
from pathlib import Path

from fastapi import FastAPI
from libarchive import SeekableArchive
from pandas import DataFrame
from starlette.responses import StreamingResponse

from .configuration import CONFIGURATION
from .database import connect, disconnect, DATABASE

LIBRARY_PATH = CONFIGURATION.library.full_path

EVENT = API.on_event
GET = API.get
POST = API.post
WS = API.websocket

BOOKS: DataFrame


async def load_books():
    lib = LIBRARY_PATH
    global BOOKS
    BOOKS = DataFrame(
        [
            (id, str(lib / path / name) + "." + format_.lower(), None)
            for id, path, name, format_ in await DATABASE.fetch_all(
                "SELECT books.id AS id, path, name, format FROM books JOIN data ON books.id = data.book"
            )
        ],
        columns=("id", "path", "pages"),
    ).set_index("id")


API = FastAPI(on_startup=[connect, load_books], on_shutdown=[disconnect])


@GET("/api/book/{book_id}")
async def _(book_id: int):
    return BOOKS.loc[book_id, :]


@GET("/api/book/{book_id}/{page}")
async def _(book_id: int, page: int = 0):
    book = BOOKS.loc[book_id, :]
    with SeekableArchive(Path(book.path).open("r")) as archive:
        pages = book.pages
        if pages is None:
            pages = book.pages = tuple(sorted(e.pathname for e in archive))
        # TODO manage IndexError
        return StreamingResponse(BytesIO(archive.read(pages[page])))
