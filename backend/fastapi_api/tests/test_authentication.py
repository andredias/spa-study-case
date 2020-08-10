from fastapi import Depends, FastAPI
from httpx import AsyncClient
from loguru import logger

from app.auth import authenticated_session  # isort:skip
from app.sessions import create_csrf, create_session, delete_session


async def test_authenticated_session(app: FastAPI, client: AsyncClient):

    @app.get('/test_session')
    async def test_session(session_data=Depends(authenticated_session)):
        return session_data

    data = {'user_id': 1}
    session_id = await create_session(data)
    csrf_token = create_csrf(session_id)
    cookies = {'session_id': session_id}
    headers = {'x-csrf-token': csrf_token}

    logger.info('ok: correct cookie and header')
    resp = await client.get('/test_session', headers=headers, cookies=cookies)
    assert resp.status_code == 200
    assert resp.json() == data

    logger.info('no cookies or headers')
    resp = await client.get('/test_session')
    assert resp.status_code == 401

    logger.info('only cookies')
    resp = await client.get('/test_session', cookies=cookies)
    assert resp.status_code == 401

    logger.info('only headers')
    resp = await client.get('/test_session', headers=headers)
    assert resp.status_code == 401

    logger.info('correct cookie, but wrong header')
    wrong_header = {'x-csrf-token': '0' + csrf_token}
    resp = await client.get('/test_session', headers=wrong_header, cookies=cookies)
    assert resp.status_code == 401

    logger.info('x-csrf-token via cookie')
    wrong_cookies = cookies.copy().update({'x-csrf-token': csrf_token})
    resp = await client.get('/test_session', cookies=wrong_cookies)
    assert resp.status_code == 401

    logger.info('correct cookies and headers, but session does not exist anymore')
    await delete_session(session_id)
    resp = await client.get('/test_session', headers=headers, cookies=cookies)
    assert resp.status_code == 401
