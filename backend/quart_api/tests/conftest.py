from pathlib import Path
from typing import AsyncIterable

from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from pytest import fixture
from quart import Quart

from app import create_app  # isort:skip


@fixture
async def app() -> AsyncIterable[Quart]:
    app = create_app(Path(__file__).parent / 'env.test')
    async with LifespanManager(app):
        yield app


@fixture
async def client(app: Quart) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client
