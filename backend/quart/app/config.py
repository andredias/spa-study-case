import os
from pathlib import Path
from tempfile import gettempdir

basedir = Path(__file__).parent


class ProductionConfig:
    APP_NAME = 'quart-backend'
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(64)
    LOG_LEVEL = 'INFO'
    LOG_BACKTRACE = False


class DevelopmentConfig(ProductionConfig):
    DEBUG = True
    LOG_FILENAME = Path(gettempdir(), f'{ProductionConfig.APP_NAME}.log')
    LOG_LEVEL = 'DEBUG'
    LOG_BACKTRACE = True


class TestingConfig(ProductionConfig):
    TESTING = True
    LOG_LEVEL = 'DEBUG'
    LOG_BACKTRACE = True


config = {
    'default': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
