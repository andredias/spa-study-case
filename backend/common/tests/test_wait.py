from unittest.mock import AsyncMock, Mock

from pytest import raises

from app.resources import wait_until_responsive  # isort:skip


async def test_wait_until_responsive():
    sentinel = object()

    amock = AsyncMock(side_effect=(AssertionError(), sentinel))
    with raises(TimeoutError):
        await wait_until_responsive(amock(), timeout=0.01)
    assert await wait_until_responsive(amock()) == sentinel

    mock = Mock(side_effect=(AssertionError(), sentinel))
    with raises(TimeoutError):
        await wait_until_responsive(mock, timeout=0.01)
    assert await wait_until_responsive(mock) == sentinel
