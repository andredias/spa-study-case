from pathlib import Path

from app import create_app
from pytest import fixture
from quart import Quart
from quart.testing import QuartClient


@fixture
def app() -> Quart:
    app = create_app(Path(__file__).parent / 'env.test')
    return app


@fixture
def client(app: Quart) -> QuartClient:
    return app.test_client()
