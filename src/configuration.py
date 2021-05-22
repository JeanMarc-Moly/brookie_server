from dataclasses import dataclass
from enum import Enum
from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING
from pathlib import Path

from datafiles import datafile


@datafile("../configuration.yml", defaults=True)
class Configuration:
    @dataclass
    class Server:
        host: str = "0.0.0.0"
        port: int = 5000

    @dataclass
    class Library:
        path: str = "/media/Data/Lecture/Magazines/"
        protocol: str = "sqlite"

        @property
        def url(self) -> str:
            return f"{self.protocol}:///{self.db_path}"

        @property
        def full_path(self) -> Path:
            return Path(self.path).resolve()

        @property
        def db_path(self) -> Path:
            return self.full_path / "metadata.db"

    @dataclass
    class Log:
        class LogLevel(Enum):
            NOTSET = NOTSET
            DEBUG = DEBUG
            INFO = INFO
            WARNING = WARNING
            ERROR = ERROR
            CRITICAL = CRITICAL

        level: LogLevel = LogLevel.INFO
        file: str = "journal.log"

    server: Server = Server()
    log: Log = Log()
    # library: str = "/media/Data/Lecture/Magazines/metadata.db"
    library: Library = Library()


CONFIGURATION = Configuration()