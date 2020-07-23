from typing import List

from pydantic import BaseModel
from pytest import mark

from app.models.user import get_user_by_login, UserRecordIn  # isort:skip


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
