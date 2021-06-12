from dataclasses import dataclass
from enum import Enum
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING
from pathlib import Path

from pydantic import parse_obj_as
from yaml import full_load

from .plugin import Libraries


@dataclass
class Configuration:
    @dataclass
    class Server:
        host: str = "0.0.0.0"
        port: int = 5000

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
        file: Path = Path("journal.log")

    server: Server
    log: Log
    library: list[Libraries]


with Path("configuration.yml").open("rb") as c:
    CONFIGURATION = parse_obj_as(Configuration, full_load(c))
