from contextlib import suppress

# from io import BytesIO
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .configuration import CONFIGURATION

L = CONFIGURATION.library


TEMPLATE_DIR = Jinja2Templates(directory="webui")
# STYLE_DIR = StaticFiles(directory="webui/dist/style")
# SCRIPT_DIR = StaticFiles(directory="webui/dist/script")
TEMPLATE_RESPONSE = TEMPLATE_DIR.TemplateResponse

API = FastAPI()
# API.mount("/style", STYLE_DIR, name="style")
# API.mount("/script", SCRIPT_DIR, name="script")
# API.mount("/component", StaticFiles(directory="component"), name="component")

# EVENT = API.on_event
GET = API.get
POST = API.post
# WS = API.websocket


@GET("/")
async def _(request: Request):
    return TEMPLATE_RESPONSE("index.html", context=dict(request=request))


@GET("/api/search")
async def _(query: str):
    return dict(pattern=query)


@GET("/api/book/{library_id}/{book_id}")
async def _(library_id: int, book_id: int):
    return await LIBS[library_id].get_book(book_id)


@GET("/api/book/{book_id}/stream", response_class=StreamingResponse)
async def _(book_id: int):
    return StreamingResponse(read_file_stream_by_file(book_id),)


# @GET("/api/book/{book_id}/stream", response_class=StreamingResponse)
# async def _(book_id: int):
#     book = BOOKS.loc[book_id, :]
#     with SeekableArchive(Path(book.path).open("r")) as archive:
#         pages = book.pages
#         if pages is None:
#             pages = book.pages = tuple(sorted(e.pathname for e in archive))
#         for page in pages:
#             print(page)
#             print(archive.readstream(page) is not None)
#         print("done")
#         return (archive.readstream(page) for page in pages)


# def read_book(book_id):
#     book = BOOKS.loc[book_id, :]
#     with SeekableArchive(Path(book.path).open("rb")) as archive:
#         pages = book.pages
#         if pages is None:
#             pages = book.pages = tuple(sorted(e.pathname for e in archive))

#         for p in pages:
#             print(p)
#             yield archive.read(p)
#         # for page in pages:
#         #     for block in archive.readstream(page):
#         #         yield block


async def read_file_stream_by_line(book_id):
    book = await get_book_path(book_id)
    with Path(book.path).open("rb") as archive:
        with suppress(StopIteration):
            while line := next(archive):
                yield line


# def read_file_stream_by_file(book_id):
#     book = BOOKS.loc[book_id, :]
#     with SeekableArchive(Path(book.path).open("rb")) as archive:
#         pages = book.pages
#         if pages is None:
#             pages = book.pages = tuple(sorted(e.pathname for e in archive))

#         for p in pages:
#             print(p)
#             yield archive.read(p)


async def read_file_stream_by_file(book_id):
    path = await get_book_path(book_id)
    with SeekableArchive(path.open("rb")) as archive:
        pages = tuple(sorted(e.pathname for e in archive))
    for p in pages:
        # If not reopened, unable to read
        with SeekableArchive(path.open("rb")) as archive:
            yield archive.read(p)


@GET("/api/book/{library_id}/{book_id}/{page}")
async def _(library_id: int, book_id: int, page: int = 0):
    return StreamingResponse(
        await L[library_id].connection.get_book_page(book_id, page)
    )
