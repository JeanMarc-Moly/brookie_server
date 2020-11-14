from contextlib import contextmanager
from sqlite3 import connect as sqlite_connect

from databases import Database

from .configuration import CONFIGURATION

DATABASE = Database(CONFIGURATION.library.url)


async def connect():
    await DATABASE.connect()


async def disconnect():
    await DATABASE.disconnect()


@contextmanager
def get_sync_cursor():
    with sqlite_connect(DATABASE.url.database) as connection:
        yield connection.cursor()
