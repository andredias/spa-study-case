from pytest import fixture
from app import create_app
from pathlib import Path


@fixture
def app():
    app = create_app(Path(__file__).parent / 'env.test')
    return app


@fixture
def client(app):
    return app.test_client()
