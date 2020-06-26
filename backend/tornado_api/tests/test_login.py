import json
from typing import Dict
from unittest.mock import AsyncMock, patch

from pydantic.dataclasses import dataclass
from pytest import mark
from tornado.simple_httpclient import SimpleAsyncHTTPClient


@dataclass
class User:
    id: int = 1
    name: str = 'Fulano'
    email: str = 'fulano@email.com'
    password: str = 'abc1234'


user = User()
get_user_mock = AsyncMock(return_value=user)


@patch('app.handlers.login.get_user', get_user_mock)
@mark.gen_test
async def test_login_missing_parameter(http_client: SimpleAsyncHTTPClient, base_url: str) -> None:
    data = json.dumps({'email': user.email})
    resp = await http_client.fetch(f'{base_url}/login', method='POST', body=data, raise_error=False)
    assert resp.code == 400


@patch('app.handlers.login.get_user', get_user_mock)
@mark.gen_test
async def test_successful_login(http_client: SimpleAsyncHTTPClient, base_url: str) -> None:
    resp = await http_client.fetch(
        f'{base_url}/login', method='POST', body=json.dumps({
            'email': user.email,
            'password': user.password
        })
    )
    assert resp.code == 200
    csrf, session_id = [set(cookie.split('; ')) for cookie in sorted(resp.headers.get_list('set-cookie'))]
    assert {'HttpOnly', 'Secure', 'SameSite=lax'} <= session_id
    assert {'Secure', 'SameSite=lax'} <= csrf
    assert 'HttpOnly' not in csrf


@patch('app.handlers.login.get_user', get_user_mock)
@mark.gen_test
async def test_successful_login_with_session_id(http_client: SimpleAsyncHTTPClient, base_url: str) -> None:
    '''
    A user log in with an existing session_id which can be from the same user or not
    '''
    session_id = 'abcd1234'
    cookies = {'Cookie': f'session_id={session_id}'}
    data = json.dumps({'email': user.email, 'password': user.password})
    with patch('app.main.login.delete_session') as delete_session:
        resp = await http_client.fetch(f'{base_url}/login', body=data, method='POST', headers=cookies)
    assert resp.code == 200
    cookies = sorted(resp.headers.get_list('set-cookie'))
    assert f'session_id={session_id}' not in cookies[1]
    delete_session.assert_awaited_once_with(session_id)


@mark.gen_test
async def test_unsuccessful_login(http_client: SimpleAsyncHTTPClient, base_url: str) -> None:
    data = json.dumps({'email': user.email, 'password': user.password})
    resp = await http_client.fetch(f'{base_url}/login', body=data, method='POST', raise_error=False)
    assert resp.code == 404
    assert not bool(resp.headers.get_list('set-cookie'))


@mark.parametrize('cookies,called', [({}, False), ({'Cookie': 'session_id=abcd1234'}, True)])
@mark.gen_test
async def test_logout(cookies: Dict[str, str], called: bool, http_client: SimpleAsyncHTTPClient, base_url: str) -> None:
    with patch('app.main.login.delete_session') as delete_session:
        resp = await http_client.fetch(
            f'{base_url}/logout', method='POST', headers=cookies, raise_error=False, allow_nonstandard_methods=True
        )

    assert resp.code == 204
    cookies_headers = ''.join(resp.headers.get_list('set-cookie'))
    assert 'session_id=""' in cookies_headers
    assert 'csrf=""' in cookies_headers
    assert delete_session.called is called
