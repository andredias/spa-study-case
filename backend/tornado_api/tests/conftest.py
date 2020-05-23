from pytest import fixture
from tornado.web import Application

from app.main import create_app


@fixture
def app() -> Application:
    return create_app()
