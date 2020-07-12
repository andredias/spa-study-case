from pathlib import Path
from typing import AsyncIterable, Dict, List

from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture

from app import create_app  # isort:skip
from app import resources as res  # isort:skip
from app.utils import crypt_ctx  # isort:skip


@fixture
async def app() -> AsyncIterable[FastAPI]:
    app = create_app(Path(__file__).parent / 'env.test')
    async with LifespanManager(app):
        yield app


@fixture
async def client(app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client


@fixture
async def users(app: FastAPI) -> List[Dict]:
    query = 'INSERT INTO User (name, email, password_hash, admin) VALUES (:name, :email, :password_hash, :admin)'
    password = 'Paulo Paulada Power'
    values = [
        dict(name='Fulano de Tal', email='fulano@email.com', password_hash=crypt_ctx.hash(password), admin=True),
        dict(name='Beltrano de Tal', email='beltrano@email.com', password_hash=crypt_ctx.hash(password), admin=False),
    ]
    await res.async_db.execute_many(query=query, values=values)
    for v in values:
        v['password'] = password
    return values
