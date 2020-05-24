from pathlib import Path

from pytest import fixture
from quart import Quart
from quart.testing import QuartClient

from app import create_app  # isort:skip


@fixture
def app() -> Quart:
    app = create_app(Path(__file__).parent / 'env.test')
    return app


@fixture
def client(app: Quart) -> QuartClient:
    return app.test_client()
