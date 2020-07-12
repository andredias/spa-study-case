from typing import Dict, List
from unittest.mock import AsyncMock, patch

from httpx import AsyncClient
from pytest import mark


@mark.asyncio
async def test_successful_login(users: List[Dict], client: AsyncClient) -> None:
    email = users[0]['email']
    password = users[0]['password']
    resp = await client.post('/login', json={'email': email, 'password': password})
    assert resp.status_code == 200
    csrf, session_id = [set(cookie.split('; ')) for cookie in sorted(resp.headers.getlist('set-cookie'))]
    assert {'HttpOnly', 'Secure', 'SameSite=lax'} <= session_id
    assert {'Secure', 'SameSite=lax'} <= csrf
    assert 'HttpOnly' not in csrf


@patch('app.login.delete_session')
@mark.asyncio
async def test_successful_login_with_session_id(
    delete_session: AsyncMock, users: List[Dict], client: AsyncClient
) -> None:
    '''
    A user log in with an existing session_id which can be from the same user or not
    '''
    session_id = 'abcd1234'
    cookies = {'session_id': session_id}
    email = users[0]['email']
    password = users[0]['password']
    resp = await client.post('/login', json={'email': email, 'password': password}, cookies=cookies)
    assert resp.status_code == 200
    assert resp.cookies['session_id'] != session_id
    assert resp.cookies['csrf']
    delete_session.assert_awaited_once_with(session_id)


@mark.asyncio
async def test_unsuccessful_login(client: AsyncClient) -> None:
    email = 'sicrano@email.com'
    password = '12345'
    resp = await client.post('/login', json={'email': email, 'password': password})
    assert resp.status_code == 404
    assert not bool(resp.headers.get('set-cookie'))


@patch('app.login.delete_session')
@mark.parametrize('cookies,called', [({}, False), ({'session_id': 'abcd1234'}, True)])
@mark.asyncio
async def test_logout(delete_session: AsyncMock, cookies: Dict[str, str], called: bool, client: AsyncClient) -> None:
    resp = await client.post('/logout', cookies=cookies)
    cookies_headers = resp.headers.get('set-cookie')

    assert resp.status_code == 204
    assert 'session_id=""' in cookies_headers
    assert 'csrf=""' in cookies_headers
    assert 'Max-Age=0' in cookies_headers
    assert delete_session.called is called
