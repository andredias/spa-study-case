import os
from pathlib import Path
from tempfile import gettempdir

# .env was already read in create_app

APP_NAME = 'Quart API'

ENV = os.environ['ENV'].lower()
if ENV not in ('development', 'testing', 'production'):
    raise ValueError(f'ENV="{ENV}" but it should be "development", "testing" or "production"')
TESTING = ENV == 'testing'
DEBUG = ENV != 'production'

LOG_LEVEL = DEBUG and 'DEBUG' or 'INFO'
LOG_BACKTRACE = DEBUG
LOG_FILENAME = Path(gettempdir(), 'quart_api.log')

SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(64)
