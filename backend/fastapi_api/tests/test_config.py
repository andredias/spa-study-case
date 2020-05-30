import os
from pathlib import Path
from unittest.mock import patch

from pytest import raises

import app.config  # isort:skip


@patch.dict('os.environ', clear=True)
def test_testing_config() -> None:
    app.config.init(Path(__file__).parent / 'env.test')
    assert app.config.ENV == 'testing'


@patch.dict('os.environ', clear=True)
def test_wrong_env() -> None:
    '''
    ENV is something different than development, testing or production
    '''
    os.environ['ENV'] = 'something_else'
    with raises(ValueError):
        app.config.init('/')


@patch.dict('os.environ', clear=True)
def test_no_env() -> None:
    '''
    ENV is not declared
    '''
    with raises(KeyError):
        app.config.init('/')
