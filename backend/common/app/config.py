import os
import secrets
from datetime import timedelta

DATABASE_URL: str
DEBUG: bool
ENV: str
LOG_LEVEL: str
REDIS_URL: str
SECRET_KEY: bytes
SESSION_ID_LENGTH: int
SESSION_LIFETIME: int
TESTING: bool


def init() -> None:
    global DATABASE_URL
    global DEBUG
    global ENV
    global LOG_LEVEL
    global REDIS_URL
    global SECRET_KEY
    global SESSION_ID_LENGTH
    global SESSION_LIFETIME
    global TESTING

    ENV = os.environ['ENV'].lower()
    if ENV not in ('development', 'testing', 'production'):
        raise ValueError(f'ENV="{ENV}" but it should be "development", "testing" or "production"')
    TESTING = ENV == 'testing'
    DEBUG = ENV != 'production'

    LOG_LEVEL = os.getenv('LOG_LEVEL') or DEBUG and 'DEBUG' or 'INFO'

    SECRET_KEY = bytes(os.getenv('SECRET_KEY', ''), 'utf-8') or secrets.token_bytes(32)
    SESSION_ID_LENGTH = int(os.getenv('SESSION_ID_LENGTH', 16))
    SESSION_LIFETIME = int(timedelta(days=7).total_seconds())

    DATABASE_URL = os.getenv('DATABASE_URL') or \
        f'postgresql://postgres:{os.environ["DB_PASSWORD"]}' \
        f'@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'
    REDIS_URL = os.environ['REDIS_URL']
