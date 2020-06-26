from unittest.mock import AsyncMock, patch

from loguru import logger
from pytest import mark
from tornado.web import Application

from app.sessions import (  # isort:skip
    create_csrf, create_session, delete_session, get_session, is_valid_csrf, session_exists
)


@mark.gen_test
async def test_session(app: Application) -> None:
    data = {'user_id': 1}
    logger.debug('antes de create_session...')
    session_id, csrf = await create_session(data)
    assert session_id
    assert csrf
    assert len(session_id) == len(csrf)
    assert is_valid_csrf(session_id, csrf)

    logger.debug('get_session...')
    resp_data, resp_csrf = await get_session(session_id)
    assert resp_data == data
    assert resp_csrf == csrf
    assert await session_exists(session_id)

    await delete_session(session_id)
    resp_data, resp_csrf = await get_session(session_id)
    assert resp_data is None
    assert resp_csrf is None
    assert not await session_exists(session_id)


@mark.gen_test
async def test_create_csrf(app: Application) -> None:
    session_id = 'abcd1234'
    csrf = create_csrf(session_id)
    assert len(csrf) == len(session_id)


@mark.gen_test
async def test_expired_session(app: Application) -> None:
    data = {'user_id': 1}
    with patch('app.resources.redis', new=AsyncMock()) as redis:
        session_id, csrf = await create_session(data)
        assert redis.expire.call_count == 1
        redis.hmget.return_value = ('{"user_id": 1}', csrf)
        _, __ = await get_session(session_id)
        assert redis.expire.call_count == 2
