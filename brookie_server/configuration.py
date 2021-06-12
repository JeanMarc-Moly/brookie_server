from abc import ABC
from dataclasses import asdict, dataclass, field
from enum import Enum
from functools import cached_property
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING
from typing import Union

from datafiles import datafile

from brookie_plugins import Libraries
from brookie_plugins import Library as AbstractLibrary


@datafile("./configuration.yml")
class Configuration:
    @dataclass
    class Server:
        host: str = "0.0.0.0"
        port: int = 5000

    class Library(ABC):
        category: Libraries
        parameters: dataclass

        @cached_property
        def connection(self) -> AbstractLibrary:
            return self.category.get(asdict(self.parameters))

    @dataclass
    class CalibreLibrary(Library):
        @dataclass
        class Parameters:
            path: str  # TODO: Path converter

        parameters: Parameters
        category: Libraries = field(default=Libraries.CALIBRE)

    @dataclass
    class Log:
        class Level(Enum):
            NOTSET = NOTSET
            DEBUG = DEBUG
            INFO = INFO
            WARNING = WARNING
            ERROR = ERROR
            CRITICAL = CRITICAL

        level: Level = Level.INFO
        file: str = "journal.log"

    server: Server
    log: Log
    library: list[Union[CalibreLibrary]]


CONFIGURATION = Configuration.objects.get()
