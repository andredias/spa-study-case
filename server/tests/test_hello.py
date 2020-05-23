from pytest import mark
from httpx import AsyncClient


@mark.parametrize('api', ('api', 'fastapi_api', 'quart_api', 'tornado_api'))
@mark.asyncio
async def test_api_hello(client: AsyncClient, api: str) -> None:
    response = await client.get(f'/{api}/hello')
    assert response.status_code == 200
    assert response.json() == {'hello': 'world'}


@mark.asyncio
async def test_localhost(client: AsyncClient) -> None:
    response = await client.get('/')
    assert response.status_code == 200
    assert b'caddy' not in response.content.lower()
