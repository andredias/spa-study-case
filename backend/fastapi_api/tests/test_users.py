from typing import List
from unittest.mock import AsyncMock, patch

from pydantic import BaseModel
from pytest import mark

import app.resources as res  # isort:skip
from app.models.user import get_user, get_user_by_login, UserInfo, UserRecordIn  # isort:skip


class UserCore(BaseModel):
    name: str
    email: str
    admin: bool


@mark.asyncio
async def test_get_user_by_login(users: List[UserRecordIn]) -> None:
    for user in users:
        result = await get_user_by_login(user.email, user.password)
        assert result and UserCore(**result.dict()) == UserCore(**user.dict())
    # non existent user
    email = 'sicrano@email.com'
    password = 'medicamento generico'
    assert await get_user_by_login(email, password) is None


@mark.asyncio
async def test_get_user(users: List[UserRecordIn]) -> None:
    user_id: int = users[0].id  # type:ignore
    user_key = f'user:{user_id}'

    # get from the database
    assert await res.redis.get(user_key) is None  # not in Redis cache
    user = await get_user(user_id)
    assert user == UserInfo(**users[0].dict())  # got the right user
    assert await res.redis.get(user_key)  # user is in Redis cache

    # get user from Redis
    with patch('app.resources.async_db', new_callable=AsyncMock) as async_db:
        user = await get_user(user_id)
    assert user == UserInfo(**users[0].dict())  # got the right user
    assert async_db.called == 0  # did not reach the database

    # inexistent user
    id_ = user_id + 1
    assert await get_user(id_) is None
