import sys
from loguru import logger
from . import config

# Logging
logger.remove()  # remove standard handler
logger.add(
    sys.stderr, level=config.LOG_LEVEL, colorize=True, backtrace=config.LOG_BACKTRACE, enqueue=True
)  # reinsert it to make it run in a different thread
logger.add(config.LOG_FILENAME, level=config.LOG_LEVEL, backtrace=config.LOG_BACKTRACE, enqueue=True)
logger.debug({key: getattr(config, key) for key in dir(config) if key == key.upper()})
