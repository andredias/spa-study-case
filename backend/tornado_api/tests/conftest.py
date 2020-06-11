from pathlib import Path

from pytest import fixture
from tornado.web import Application

from app.main import create_app  # isort:skip


@fixture
def app() -> Application:
    app = create_app(Path(__file__).parent / 'env.test')
    return app
