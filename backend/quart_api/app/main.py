import logging
import os
import sys

from loguru import logger
from quart import Quart

from .config import config


class InterceptHandler(logging.Handler):

    def emit(self, record):
        # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


def create_app(mode: str = 'production') -> Quart:
    '''
    Application factory pattern
    '''
    app = Quart(__name__)
    mode = os.environ.get('ENV') or os.environ.get('QUART_ENV') or mode
    app.config.from_object(config[mode])

    # Logging
    log_level = app.config['LOG_LEVEL']
    backtrace = app.config['LOG_BACKTRACE']
    logger.remove()  # remove standard handler
    logger.add(
        sys.stderr, level=log_level, colorize=True, backtrace=backtrace, enqueue=True
    )  # reinsert it to make it run in a different thread
    log_filename = app.config.get('LOG_FILENAME')
    if log_filename:
        logger.add(log_filename, level=log_level, backtrace=backtrace, enqueue=True)
    handler = InterceptHandler()
    handler.setLevel(0)
    app.logger.addHandler(handler)

    logger.debug('Running in DEBUG mode')
    logger.debug(app.config)

    # blueprints
    from .api import api
    app.register_blueprint(api)

    return app
