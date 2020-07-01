import os
import secrets
from datetime import timedelta

ENV: str = os.environ['ENV'].lower()
if ENV not in ('development', 'testing', 'production'):
    raise ValueError(f'ENV="{ENV}" but it should be "development", "testing" or "production"')
TESTING: bool = ENV == 'testing'
DEBUG: bool = ENV != 'production'

LOG_LEVEL: str = os.getenv('LOG_LEVEL') or DEBUG and 'DEBUG' or 'INFO'
LOG_BACKTRACE: bool = DEBUG

SECRET_KEY: bytes = bytes(os.getenv('SECRET_KEY', ''), 'utf-8') or secrets.token_bytes(32)
SESSION_ID_LENGTH = int(os.getenv('SESSION_ID_LENGTH', 16))
SESSION_LIFETIME = int(timedelta(days=7).total_seconds())

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
