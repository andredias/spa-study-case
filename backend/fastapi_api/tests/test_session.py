from unittest.mock import AsyncMock, patch

from fastapi import Depends, FastAPI
from httpx import AsyncClient
from pytest import mark

from app.sessions import (  # isort:skip
    authenticated_session, create_csrf, create_session, delete_session, get_session, is_valid_csrf, session_exists
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


@mark.asyncio
async def test_authenticated_session(app: FastAPI, client: AsyncClient):

    @app.get('/test_session')
    async def test_session(session_data=Depends(authenticated_session)):
        return session_data

    data = {'user_id': 1}
    session_id = await create_session(data)
    csrf_token = create_csrf(session_id)
    cookies = {'session_id': session_id}
    headers = {'x-csrf-token': csrf_token}

    # ok: correct cookie and header
    resp = await client.get('/test_session', headers=headers, cookies=cookies)
    assert resp.status_code == 200
    assert resp.json() == data

    # no cookies or headers
    resp = await client.get('/test_session')
    assert resp.status_code == 401

    # only cookies
    resp = await client.get('/test_session', cookies=cookies)
    assert resp.status_code == 401

    # only headers
    resp = await client.get('/test_session', headers=headers)
    assert resp.status_code == 401

    # correct cookie, but wrong header
    wrong_header = {'x-csrf-token': '0' + csrf_token}
    resp = await client.get('/test_session', headers=wrong_header, cookies=cookies)
    assert resp.status_code == 401

    # x-csrf-token via cookie
    wrong_cookies = cookies.copy().update({'x-csrf-token': csrf_token})
    resp = await client.get('/test_session', cookies=wrong_cookies)
    assert resp.status_code == 401

    # correct cookies and headers, but session does not exist anymore
    await delete_session(session_id)
    resp = await client.get('/test_session', headers=headers, cookies=cookies)
    assert resp.status_code == 401
