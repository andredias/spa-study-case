from unittest.mock import AsyncMock, patch

from pytest import mark
from quart import Quart

from app.sessions import (  # isort:skip
    create_csrf, create_session, delete_session, get_session, is_valid_csrf, session_exists
)


@mark.asyncio
async def test_session(app: Quart) -> None:
    data = {'user_id': 1}
    async with app.app_context():
        session_id, csrf = await create_session(data)
        assert session_id
        assert csrf
        assert len(session_id) == len(csrf)
        assert is_valid_csrf(session_id, csrf)

        resp_data, resp_csrf = await get_session(session_id)
        assert resp_data == data
        assert resp_csrf == csrf
        assert await session_exists(session_id)

        await delete_session(session_id)
        resp_data, resp_csrf = await get_session(session_id)
        assert resp_data is None
        assert resp_csrf is None
        assert not await session_exists(session_id)


@mark.asyncio
async def test_create_csrf(app: Quart) -> None:
    session_id = 'abcd1234'
    async with app.app_context():
        csrf = create_csrf(session_id)
    assert len(csrf) == len(session_id)


@patch('app.resources.redis', new_callable=AsyncMock)
@mark.asyncio
async def test_expired_session(redis: AsyncMock, app: Quart) -> None:
    data = {'user_id': 1}
    async with app.app_context():
        session_id, csrf = await create_session(data)
    assert redis.expire.call_count == 1
    redis.hmget.return_value = ('{"user_id": 1}', csrf)
    async with app.app_context():
        _, __ = await get_session(session_id)
    assert redis.expire.call_count == 2
