from typing import Any, Dict, List

from httpx import AsyncClient
from loguru import logger

from ..utils import logged_session

from app.models.user import UserInfo, UserRecordIn, get_user, insert  # isort:skip

ListDictStrAny = List[Dict[str, Any]]


async def test_get_users(users: ListDictStrAny, client: AsyncClient) -> None:
    admin_id = users[0]['id']
    user_id = users[1]['id']
    url = '/user'

    await logged_session(client, admin_id)
    resp = await client.get(url)
    assert resp.status_code == 200
    assert len(resp.json()) == 2

    await logged_session(client, user_id)
    resp = await client.get(url)
    assert resp.status_code == 403

    await logged_session(client)
    resp = await client.get(url)
    assert resp.status_code == 401


async def test_get_user(users: ListDictStrAny, client: AsyncClient) -> None:
    admin_id = users[0]['id']
    user_id = users[1]['id']
    url = '/user/{}'

    logger.info('normal user try to access its own info')
    await logged_session(client, user_id)
    resp = await client.get(url.format(user_id))
    assert resp.status_code == 200
    assert UserInfo(**resp.json()) == UserInfo(**users[1])

    logger.info('normal user try to access another user info')
    resp = await client.get(url.format(admin_id))
    assert resp.status_code == 403

    logger.info('admin access to another user info')
    await logged_session(client, admin_id)
    resp = await client.get(url.format(user_id))
    assert resp.status_code == 200
    assert UserInfo(**resp.json()) == UserInfo(**users[1])

    logger.info('admin access to inexistent user')
    resp = await client.get(url.format(user_id + 1))
    assert resp.status_code == 404

    logger.info('anonymous acess to user account')
    await logged_session(client)
    resp = await client.get(url.format(user_id))
    assert resp.status_code == 401


async def test_update_user(users: ListDictStrAny, client: AsyncClient) -> None:
    admin_id = users[0]['id']
    user_id = users[1]['id']
    url = '/user/{}'
    email = 'beltrano@pronus.io'
    name = 'Belafonte'

    logger.info('anonymous tries to update a user account')
    resp = await client.put(url.format(user_id))
    assert resp.status_code == 401

    logger.info('normal user tries to update another account')
    await logged_session(client, user_id)
    resp = await client.put(url.format(admin_id), json={'email': email})
    assert resp.status_code == 403

    logger.info('normal user tries to update his own account')
    resp = await client.put(url.format(user_id), json={'email': email})
    assert resp.status_code == 204
    user = await get_user(user_id)
    assert user and user.email == email

    logger.info('admin updates a user')
    await logged_session(client, admin_id)
    resp = await client.put(url.format(user_id), json={'name': name})
    assert resp.status_code == 204
    user = await get_user(user_id)
    assert user and user.name == name

    logger.info('admin tries to update inexistent user')
    resp = await client.put(url.format(user_id + 1), json={'name': name})
    assert resp.status_code == 404


async def test_delete_user(users: ListDictStrAny, client: AsyncClient) -> None:
    admin_id = users[0]['id']
    user_id = users[1]['id']
    third_id = await insert(UserRecordIn(name='Sicrano', email='sicrano@email.com', password='Sicrano Tralalá'))
    url = '/user/{}'

    logger.info('anonymous tries to delete a user account')
    resp = await client.delete(url.format(user_id))
    assert resp.status_code == 401

    logger.info('sicrano tries to delete another account')
    await logged_session(client, third_id)
    resp = await client.delete(url.format(admin_id))
    assert resp.status_code == 403

    logger.info('sicrano tries to delete his own account')
    resp = await client.delete(url.format(third_id))
    assert resp.status_code == 204
    assert await get_user(third_id) is None

    logger.info('admin deletes a user')
    await logged_session(client, admin_id)
    resp = await client.delete(url.format(user_id))
    assert resp.status_code == 204

    logger.info('admin tries to delete inexistent user')
    resp = await client.delete(url.format(user_id + 1))
    assert resp.status_code == 404
