from pathlib import Path

from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture

from app import create_app  # isort:skip


@fixture(scope='session')
def app() -> FastAPI:
    # Since there is a `from . import config` in create_app,
    # this import is done just once,
    # even if create_app is called several times.
    app = create_app(Path(__file__).parent / 'env.test')
    # one workaround would be to reload config import here
    return app


@fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client
