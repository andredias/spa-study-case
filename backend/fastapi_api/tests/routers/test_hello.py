from httpx import AsyncClient


async def test_hello(client: AsyncClient) -> None:
    resp = await client.get('/hello')
    assert resp.status_code == 200
    assert resp.json() == {'hello': 'world'}
