from io import BytesIO

from fastapi import FastAPI
from starlette.responses import StreamingResponse
from libarchive import SeekableArchive

from .configuration import CONFIGURATION

from .database import DATABASE as DB
from .database import connect, disconnect

API = FastAPI()
EVENT = API.on_event
GET = API.get
POST = API.post

EVENT("startup")(connect)
EVENT("shutdown")(disconnect)


@GET("/{book_id}")
@GET("/{book_id}/{page}")
async def _(book_id: int, page: int = 0):
    path, name, format = await DB.fetch_one(
        "SELECT path, name, format FROM (SELECT id, path FROM books WHERE id=:id) b JOIN data ON b.id = data.book",
        values=dict(id=book_id),
    )
    with SeekableArchive(
        (CONFIGURATION.library.path / path / name)
        .with_suffix("." + format.lower())
        .open(mode="r")
    ) as book:
        return StreamingResponse(
            BytesIO(book.read(sorted(e.pathname for e in book)[page])),
            media_type="image/webp",
        )
