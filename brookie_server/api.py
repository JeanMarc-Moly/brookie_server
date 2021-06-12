from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from .configuration import CONFIGURATION

L = CONFIGURATION.library

API = FastAPI()
GET = API.get


@GET("/api/book/{library_id}/{book_id}/{page}")
async def _(library_id: int, book_id: int, page: int = 0):
    async with L[library_id] as l:
        return StreamingResponse(
            await l.get_book_page(book_id, page), 200, {"Cache-Control": "immutable"}
        )
