from unittest.mock import AsyncMock, patch

from fastapi import FastAPI
from pytest import mark

from app.sessions import (  # isort:skip
    create_csrf, create_session, delete_session, get_session, is_valid_csrf, session_exists
)


@mark.asyncio
async def test_session(app: FastAPI) -> None:
    data = {'user_id': 1}

    # create session
    session_id = await create_session(data)
    assert session_id
    assert await session_exists(session_id)

    # get_session
    resp_data = await get_session(session_id)
    assert resp_data == data

    # delete_session
    await delete_session(session_id)
    resp_data = await get_session(session_id)
    assert resp_data is None
    assert not await session_exists(session_id)


@patch('app.resources.redis', new_callable=AsyncMock)
@mark.asyncio
async def test_create_csrf(redis: AsyncMock, app: FastAPI) -> None:
    session_id = await create_session({'user_id': 12345})
    csrf = create_csrf(session_id)
    assert is_valid_csrf(session_id, csrf)


@patch('app.resources.redis', new_callable=AsyncMock)
@mark.asyncio
async def test_expired_session(redis: AsyncMock, app: FastAPI) -> None:
    data = {'user_id': 1}
    session_id = await create_session(data)
    assert redis.expire.call_count == 1
    redis.get.return_value = ('{"user_id": 1}')
    _ = await get_session(session_id)
    assert redis.expire.call_count == 2
