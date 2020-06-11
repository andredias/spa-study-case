import logging
import sys
from pathlib import Path
from typing import Union

from dotenv import load_dotenv
from loguru import logger
from quart import Quart


def set_logger(app: Quart) -> None:

    class InterceptHandler(logging.Handler):

        def emit(self, record):
            # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
            logger_opt = logger.opt(depth=6, exception=record.exc_info)
            logger_opt.log(record.levelno, record.getMessage())

    # Logging
    log_level = app.config['LOG_LEVEL']
    backtrace = app.config['LOG_BACKTRACE']
    logger.remove()  # remove standard handler
    logger.add(
        sys.stderr, level=log_level, colorize=True, backtrace=backtrace, enqueue=True
    )  # reinsert it to make it run in a different thread
    handler = InterceptHandler()
    handler.setLevel(0)
    app.logger.addHandler(handler)


def create_app(env_filename: Union[str, Path] = '.env') -> Quart:
    '''
    Application factory pattern
    '''
    app = Quart(__name__)

    # a .env file is not mandatory.
    # You can specify envvar parameters by other means
    # as long as they are available before app.config.from_pyfile is called
    load_dotenv(env_filename)
    app.config.from_pyfile('config.py')

    set_logger(app)
    logger.debug('Running in DEBUG mode')
    logger.debug(app.config)

    # blueprints
    from .routes import hello
    app.register_blueprint(hello.api)

    from .resources import close_resources, start_resources

    # startup e shutdown
    @app.before_serving
    async def startup_event():
        logger.debug('startup...')
        await start_resources()

    @app.after_serving
    async def shutdown_event():
        logger.debug('...shutdown')
        await close_resources()

    return app
