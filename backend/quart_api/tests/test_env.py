from pathlib import Path
from unittest.mock import patch

import pytest
from app import create_app


@pytest.fixture
def env_file(tmp_path: Path) -> Path:
    return tmp_path / '.env'


def test_non_existent_env(env_file: Path) -> None:
    '''
    .env file does not exist
    '''
    with pytest.raises(FileNotFoundError):
        app = create_app(env_file)  # noqa: F841


@patch.dict('os.environ')  # prevents load_dotenv from modifying os.environ for other tests
def test_wrong_env(env_file: Path) -> None:
    '''
    ENV is something different than development, testing or production
    '''
    env_file.write_text('ENV=something_else')
    with pytest.raises(ValueError):
        app = create_app(env_file)  # noqa: F841