from app.main import app as _app
from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture


@fixture
def app() -> FastAPI:
    return _app


@fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client
