#!./.python_env/bin/python

from uvicorn import run

from brookie_server.configuration import CONFIGURATION as CF

if __name__ == "__main__":
    run(
        "brookie_server.api:API",
        host=CF.server.host,
        port=CF.server.port,
        log_level=CF.log.level.value,
    )
