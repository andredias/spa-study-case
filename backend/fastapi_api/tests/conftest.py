from pathlib import Path
from typing import AsyncIterable

from asgi_lifespan import LifespanManager
from dotenv import load_dotenv
from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture

from .common.fixtures import docker, users  # noqa:F401

from app import create_app  # isort:skip

load_dotenv(Path(__file__).parent / 'env')


@fixture
async def app(docker) -> AsyncIterable[FastAPI]:  # noqa: F811
    app = create_app()
    async with LifespanManager(app):
        yield app


@fixture
async def client(app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client
