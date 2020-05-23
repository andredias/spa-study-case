import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

APP_NAME: str = 'TornadoAPI Backend'

ENV: str = os.environ['ENV'].lower()
if ENV not in ('development', 'testing', 'production'):
    raise ValueError(f'ENV="{ENV}" but it should be "development", "testing" or "production"')
TESTING: bool = ENV == 'testing'
DEBUG: bool = ENV != 'production'

LOG_LEVEL: str = os.getenv('LOG_LEVEL') or DEBUG and 'DEBUG' or 'INFO'
LOG_BACKTRACE: bool = DEBUG
LOG_FILENAME: Path = Path('/dev/shm') / (APP_NAME.lower().replace(' ', '_') + '.log')

SECRET_KEY: str = os.getenv('SECRET_KEY') or secrets.token_urlsafe(32)
