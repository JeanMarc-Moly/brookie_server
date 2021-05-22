from enum import Enum

from .abstract import Library
from .calibre import CalibreLibrary


class Libraries(Enum):
    CALIBRE = "calibre"

    def get(self, parameters: dict[str, str]) -> Library:
        try:
            return _LIBRARIES[self](**parameters)
        except KeyError as e:
            raise Exception(f"Unknown library category {e.args[0]} in configuration")


_LIBRARIES: dict[Libraries, Library] = {
    Libraries.CALIBRE: CalibreLibrary,
}
