import os
from pathlib import Path
from unittest.mock import patch

import pytest
from app import create_app


@pytest.fixture
def env_file(tmp_path: Path) -> Path:
    return tmp_path / '.env'


@patch.dict('os.environ', clear=True)  # prevents load_dotenv from modifying os.environ for other tests
def test_non_existent_env(env_file) -> None:
    '''
    .env file does not exist but ENV does
    '''
    os.environ['ENV'] = 'testing'
    os.environ['LOG_LEVEL'] = 'INFO'  # prevents create_app from logging durint testing
    app = create_app(env_file)
    assert app


@patch.dict('os.environ', clear=True)
def test_no_env_envvar(env_file: Path) -> None:
    '''
    ENV environment variable is not defined at all
    '''
    os.environ['LOG_LEVEL'] = 'INFO'  # prevents create_app from logging during testing
    with pytest.raises(KeyError):
        app = create_app(env_file)  # noqa: F841


@patch.dict('os.environ', clear=True)  # prevents load_dotenv from modifying os.environ for other tests
def test_wrong_env(env_file: Path) -> None:
    '''
    ENV is something different than development, testing or production
    '''
    env_file.write_text('ENV=something_else')
    with pytest.raises(ValueError):
        app = create_app(env_file)  # noqa: F841
