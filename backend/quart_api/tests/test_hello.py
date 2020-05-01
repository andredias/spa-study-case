import pytest
from quart.testing import QuartClient

# All test coroutines will be treated as marked.
# see https://github.com/pytest-dev/pytest-asyncio#pytestmarkasyncio
pytestmark = pytest.mark.asyncio


async def test_hello(client: QuartClient) -> None:
    response = await client.get('/hello')
    assert response.status_code == 200
    assert await response.json == {'hello': 'world'}
