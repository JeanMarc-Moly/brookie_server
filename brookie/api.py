from io import BytesIO
from pathlib import Path

from fastapi import FastAPI
from libarchive import SeekableArchive
from pandas import DataFrame
from starlette.responses import StreamingResponse

from .configuration import CONFIGURATION
from .database import connect, disconnect, get_sync_cursor

LIBRARY_PATH = CONFIGURATION.library.full_path

API = FastAPI()
EVENT = API.on_event
GET = API.get
POST = API.post
WS = API.websocket

EVENT("startup")(connect)
EVENT("shutdown")(disconnect)


# TODO: Make async
def get_books():
    with get_sync_cursor() as db:
        lib = LIBRARY_PATH
        return DataFrame(
            [
                (id, (lib / path / name).with_suffix("." + format_.lower()), None)
                for id, path, name, format_ in db.execute(
                    "SELECT books.id AS id, path, name, format FROM books JOIN data ON books.id = data.book"
                )
            ],
            columns=("id", "path", "pages"),
        ).set_index("id")


BOOKS: DataFrame = get_books()


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
