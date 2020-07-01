import os
import secrets
from datetime import timedelta
from pathlib import Path
from typing import Union

from dotenv import load_dotenv

DEBUG: bool
ENV: str
LOG_LEVEL: str
REDIS_HOST: str
REDIS_PORT: str
SECRET_KEY: bytes
SESSION_ID_LENGTH: int
SESSION_LIFETIME: int
TESTING: bool


def init(env_filename: Union[str, Path] = '.env') -> None:
    global DEBUG
    global ENV
    global LOG_LEVEL
    global REDIS_HOST
    global REDIS_PORT
    global SECRET_KEY
    global SESSION_ID_LENGTH
    global SESSION_LIFETIME
    global TESTING

    # a .env file is not mandatory.
    # You can specify envvar parameters by other means
    load_dotenv(env_filename)

    ENV = os.environ['ENV'].lower()
    if ENV not in ('development', 'testing', 'production'):
        raise ValueError(f'ENV="{ENV}" but it should be "development", "testing" or "production"')
    TESTING = ENV == 'testing'
    DEBUG = ENV != 'production'

    LOG_LEVEL = os.getenv('LOG_LEVEL') or DEBUG and 'DEBUG' or 'INFO'

    SECRET_KEY = bytes(os.getenv('SECRET_KEY', ''), 'utf-8') or secrets.token_bytes(32)
    SESSION_ID_LENGTH = int(os.getenv('SESSION_ID_LENGTH', 16))
    SESSION_LIFETIME = int(timedelta(days=7).total_seconds())

    REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
    REDIS_PORT = os.getenv('REDIS_PORT', '6379')
