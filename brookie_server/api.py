from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse

from .configuration import CONFIGURATION

L = CONFIGURATION.library

API = FastAPI()
GET = API.get


@GET("/api/book/{library_id}/{book_id}/cover")
async def _(library_id: int, book_id: int):
    async with L[library_id] as l:
        return StreamingResponse(
            await l.get_book_cover(book_id), 200, {"Cache-Control": "immutable"}
        )


@GET("/api/book/{library_id}/{book_id}/pages")
async def _(library_id: int, book_id: int):
    async with L[library_id] as l:
        pages = []
        async for p in l.get_book_pages(book_id):
            pages.append(p)
        return JSONResponse(pages)


@GET("/api/book/{library_id}/{book_id}/{page}")
async def _(library_id: int, book_id: int, page: int = 0):
    async with L[library_id] as l:
        return StreamingResponse(
            await l.get_book_page(book_id, page), 200, {"Cache-Control": "immutable"}
        )
