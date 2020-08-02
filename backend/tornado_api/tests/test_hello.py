from httpx import AsyncClient


async def test_hello(client: AsyncClient) -> None:
    response = await client.get('/hello')
    assert response.json() == {'hello': 'world'}
