import sys
from pathlib import Path
from typing import Any, Union

import orjson
from fastapi import FastAPI
from loguru import logger
from starlette.responses import JSONResponse

from . import config
from .resources import close_resources, start_resources
from .routers import hello, login, user

routers = [
    hello.router,
    login.router,
    user.router,
]


def create_app(env_filename: Union[str, Path] = '.env') -> FastAPI:
    config.init(env_filename)
    setup_logger()

    app = FastAPI(default_response_class=ORJSONResponse)
    for router in routers:
        app.include_router(router)

    @app.on_event('startup')
    async def startup_event():
        logger.debug('startup...')
        await start_resources()

    @app.on_event('shutdown')
    async def shutdown_event():
        logger.debug('...shutdown')
        await close_resources()

    return app


def setup_logger():
    '''
    Configure Loguru's logger
    '''
    logger.remove()  # remove standard handler
    logger.add(
        sys.stderr, level=config.LOG_LEVEL, colorize=True, backtrace=config.DEBUG, enqueue=True
    )  # reinsert it to make it run in a different thread
    logger.debug({key: getattr(config, key) for key in dir(config) if key == key.upper()})


class ORJSONResponse(JSONResponse):

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)
