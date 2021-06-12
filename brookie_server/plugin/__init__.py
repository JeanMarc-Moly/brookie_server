from contextlib import suppress
from inspect import getmembers
from typing import Generator, Type, Union

from brookie_plugin_library_abstract import Library
from pkg_resources import working_set

from .error import NoLibrary

PREFIX = "brookie-plugin-library"


def get_plugins() -> Generator[Type, None, None]:
    for d in working_set:
        if (d_ := d._key).startswith(PREFIX) and not d_.endswith("abstract"):
            for m in getmembers(__import__(d_.replace("-", "_"))):
                with suppress(TypeError):
                    if (cls := m[1]) is not Library and issubclass(cls, Library):
                        yield cls


try:
    Libraries: Type[Library] = Union[tuple(get_plugins())]
except TypeError as e:
    raise NoLibrary from e
