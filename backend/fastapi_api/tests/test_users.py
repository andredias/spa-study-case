from typing import Dict, List

from pydantic import BaseModel
from pytest import mark

from app.models import get_user_by_login  # isort:skip


class UserCore(BaseModel):
    name: str
    email: str
    admin: bool


@mark.asyncio
async def test_get_user_by_login(users: List[Dict]) -> None:
    for user in users:
        result = await get_user_by_login(user['email'], user['password'])
        assert result and UserCore(**result.dict()) == UserCore(**user)
    # non existent user
    email = 'sicrano@email.com'
    password = 'medicamento generico'
    assert await get_user_by_login(email, password) is None
