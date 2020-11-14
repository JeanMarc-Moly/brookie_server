from databases import Database

from .configuration import CONFIGURATION

DATABASE = Database(CONFIGURATION.library.url)


async def connect():
    await DATABASE.connect()


async def disconnect():
    await DATABASE.disconnect()
