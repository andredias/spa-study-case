import os
from pathlib import Path
from typing import AsyncIterable, Dict, Generator, List

from asgi_lifespan import LifespanManager
from dotenv import load_dotenv
from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture

from app import create_app  # isort:skip
from app import resources as res  # isort:skip
from app.utils import crypt_ctx  # isort:skip

load_dotenv(Path(__file__).parent / 'env')


@fixture(scope='session')
def docker() -> Generator:
    if os.environ['ENV'] == 'production':
        db_name = os.environ['DB_NAME']
        os.system(
            f'docker run -d --rm -e POSTGRES_DB={db_name} -e POSTGRES_PASSWORD=senha '
            '-p 5432:5432 --name postgres postgres:alpine > /dev/null'
        )
        os.system('docker run -d --rm -p 6379:6379 --name redis redis:alpine > /dev/null')
        try:
            yield
        finally:
            os.system('docker stop postgres redis > /dev/null')
    else:
        yield


@fixture
async def app(docker) -> AsyncIterable[FastAPI]:
    app = create_app()
    async with LifespanManager(app):
        yield app


@fixture
async def client(app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client


@fixture
async def users(app: FastAPI) -> List[Dict]:
    query = 'INSERT INTO "user" (name, email, password_hash, admin) VALUES (:name, :email, :password_hash, :admin)'
    password = 'Paulo Paulada Power'
    values = [
        dict(name='Fulano de Tal', email='fulano@email.com', password_hash=crypt_ctx.hash(password), admin=True),
        dict(name='Beltrano de Tal', email='beltrano@email.com', password_hash=crypt_ctx.hash(password), admin=False),
    ]
    await res.async_db.execute_many(query=query, values=values)
    for v in values:
        v['password'] = password
        del v['password_hash']
    return values
