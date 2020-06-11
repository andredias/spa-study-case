import os
import secrets
from pathlib import Path
from typing import Union

from dotenv import load_dotenv

DEBUG: bool
ENV: str
LOG_LEVEL: str
SECRET_KEY: bytes
TESTING: bool


def init(env_filename: Union[str, Path] = '.env') -> None:
    global DEBUG
    global ENV
    global LOG_LEVEL
    global SECRET_KEY
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
