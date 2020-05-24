from pathlib import Path

from pytest import fixture
from tornado.web import Application

from app.main import create_app  # isort:skip


@fixture(scope='session')
def app() -> Application:
    # Since there is a `from . import config` in create_app,
    # this import is done just once,
    # even if create_app is called several times.
    app = create_app(Path(__file__).parent / 'env.test')
    # one workaround would be to reload config import here
    return app
