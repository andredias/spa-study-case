import os
from pathlib import Path
from subprocess import DEVNULL, check_call
from typing import AsyncIterable, Generator

from asgi_lifespan import LifespanManager
from dotenv import load_dotenv
from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture

from .common.fixtures import users  # noqa:F401

from app import create_app  # isort:skip

load_dotenv(Path(__file__).parent / 'env')


@fixture(scope='session')
def docker() -> Generator:
    if os.environ['ENV'] == 'production':
        check_call(
            f'docker run -d --rm -e POSTGRES_DB={os.environ["DB_NAME"]} '
            f'-e POSTGRES_PASSWORD={os.environ["DB_PASSWORD"]} '
            '-p 5432:5432 --name postgres postgres:alpine',
            stdout=DEVNULL,
            shell=True
        )
        check_call('docker run -d --rm -p 6379:6379 --name redis redis:alpine', stdout=DEVNULL, shell=True)
        try:
            yield
        finally:
            check_call('docker stop postgres redis', stdout=DEVNULL, shell=True)
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
