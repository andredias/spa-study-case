import sys
from pathlib import Path
from typing import Union

from dotenv import load_dotenv
from fastapi import FastAPI
from loguru import logger

from .routers import router


def create_app(env_filename: Union[str, Path] = '.env') -> FastAPI:

    # a .env file is not mandatory.
    # You can specify envvar parameters by other means
    # as long as they are available before config is imported
    load_dotenv(env_filename)

    from . import config

    # config logger
    logger.remove()  # remove standard handler
    logger.add(
        sys.stderr, level=config.LOG_LEVEL, colorize=True, backtrace=config.DEBUG, enqueue=True
    )  # reinsert it to make it run in a different thread
    logger.debug({key: getattr(config, key) for key in dir(config) if key == key.upper()})

    # App
    app = FastAPI()

    app.include_router(router)

    return app
