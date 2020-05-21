from app import create_app
from fastapi import FastAPI
from httpx import AsyncClient
from pytest import fixture


@fixture
def app() -> FastAPI:
    return create_app()


@fixture
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://testserver') as client:
        yield client
