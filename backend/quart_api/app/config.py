import os
from pathlib import Path
from tempfile import gettempdir

APP_NAME = 'Quart API'

ENV = os.environ['ENV'].lower()
if ENV not in ('development', 'testing', 'production'):
    raise ValueError(f'ENV="{ENV}" but it should be "development", "testing" or "production"')
TESTING = ENV == 'testing'
DEBUG = ENV != 'production'

LOG_LEVEL = os.getenv('LOG_LEVEL') or DEBUG and 'DEBUG' or 'INFO'
LOG_BACKTRACE = DEBUG
LOG_FILENAME = Path(gettempdir(), 'quart_api.log')

SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(64)
