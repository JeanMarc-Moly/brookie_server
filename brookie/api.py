from io import BytesIO
from pathlib import Path

from fastapi import FastAPI
from libarchive import SeekableArchive
from pandas import DataFrame
from starlette.responses import StreamingResponse

from .configuration import CONFIGURATION
from .database import connect, disconnect, get_sync_cursor

API = FastAPI()
EVENT = API.on_event
GET = API.get
POST = API.post

EVENT("startup")(connect)
EVENT("shutdown")(disconnect)


# TODO: Make async
def get_books():
    with get_sync_cursor() as db:
        lib = CONFIGURATION.library.full_path
        return DataFrame(
            [
                (id, (lib / path / name).with_suffix("." + format.lower()))
                for id, path, name, format in db.execute(
                    "SELECT books.id AS id, path, name, format FROM books JOIN data ON books.id = data.book"
                )
            ],
            columns=("id", "path"),
        ).set_index("id")


BOOKS_PATH: DataFrame = get_books().path


@GET("/{book_id}")
@GET("/{book_id}/{page}")
async def _(book_id: int, page: int = 0):
    with SeekableArchive(Path(BOOKS_PATH[book_id]).open("r")) as book:
        return StreamingResponse(
            BytesIO(book.read(sorted(e.pathname for e in book)[page])),
            media_type="image/webp",
        )
