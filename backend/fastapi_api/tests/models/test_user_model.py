from typing import Any, Dict, List
from unittest.mock import AsyncMock, patch

from loguru import logger
from pytest import mark

import app.resources as res  # isort:skip
from app.models import diff_models  # isort:skip
from app.models.user import get_user, get_user_by_login, User, UserInfo, UserRecordPatch, update, delete  # isort:skip

ListDictStrAny = List[Dict[str, Any]]


@mark.asyncio
async def test_get_user_by_login(users: ListDictStrAny) -> None:
    for user in users:
        result = await get_user_by_login(user['email'], user['password'])
        assert result and UserInfo(**result.dict()) == UserInfo(**user)
    # non existent user
    email = 'sicrano@email.com'
    password = 'medicamento generico'
    assert await get_user_by_login(email, password) is None


@mark.asyncio
async def test_get_user(users: ListDictStrAny) -> None:
    user_id: int = users[0]['id']  # type:ignore
    user_key = f'user:{user_id}'

    # get from the database
    assert await res.redis.get(user_key) is None  # not in Redis cache
    user = await get_user(user_id)
    assert user == UserInfo(**users[0])  # got the right user
    assert await res.redis.get(user_key)  # user is in Redis cache

    # get user from Redis
    with patch('app.resources.db', new_callable=AsyncMock) as db:
        user = await get_user(user_id)
    assert user == UserInfo(**users[0])  # got the right user
    assert db.called == 0  # did not reach the database

    # inexistent user
    id_ = user_id + 1
    assert await get_user(id_) is None


@mark.asyncio
async def test_update_user(users: ListDictStrAny) -> None:
    logger.info('Update password')
    table_name = User._table_
    user_data = users[0]
    orig_user = await res.db.fetch_one(f'SELECT * FROM "{table_name}" WHERE id = :id', dict(id=user_data['id']))
    new_data = user_data.copy()
    new_data['password'] = 'espionage prewashed recognize ducktail'
    fields = diff_models(UserInfo(**user_data), UserRecordPatch(**new_data))
    await update(fields, user_data['id'])
    new_user = await res.db.fetch_one(f'SELECT * FROM "{table_name}" WHERE id = :id', dict(id=user_data['id']))
    assert new_user['password_hash'] != orig_user['password_hash']

    logger.info('Update name, email and admin')
    user_data = users[1]
    orig_user = await res.db.fetch_one(f'SELECT * FROM "{table_name}" WHERE id = :id', dict(id=user_data['id']))
    patch = UserRecordPatch(name='Sicrano', email='sicrano@email.com', admin=True)
    fields = diff_models(UserInfo(**user_data), patch)
    await update(fields, user_data['id'])
    new_user = await res.db.fetch_one(f'SELECT * FROM "{table_name}" WHERE id = :id', dict(id=user_data['id']))
    assert new_user['password_hash'] == orig_user['password_hash']
    for field in ('name', 'email', 'admin'):
        assert new_user[field] != orig_user[field]


@mark.asyncio
async def test_delete(users: ListDictStrAny) -> None:
    await delete(users[0]['id'])
    assert await get_user(id=users[0]['id']) is None
