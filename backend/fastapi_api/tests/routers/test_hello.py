from httpx import AsyncClient
from pytest import mark


@mark.asyncio
async def test_hello(client: AsyncClient) -> None:
    resp = await client.get('/hello')
    assert resp.status_code == 200
    assert resp.json() == {'hello': 'world'}
