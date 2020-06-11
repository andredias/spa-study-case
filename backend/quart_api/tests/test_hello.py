import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_hello(client: AsyncClient) -> None:
    response = await client.get('/hello')
    assert response.status_code == 200
    assert response.json() == {'hello': 'world'}
