from pathlib import Path

from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture

from app import create_app  # isort:skip


@fixture(scope='session')
def app() -> FastAPI:
    app = create_app(Path(__file__).parent / 'env.test')
    return app


@fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client
