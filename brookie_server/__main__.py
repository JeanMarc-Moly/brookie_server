#!./.venv/bin/python

from uvicorn import run

from .configuration import CONFIGURATION as CF

run(
    "brookie_server.api:API",
    host=CF.server.host,
    port=CF.server.port,
    log_level=CF.log.level.value,
)
