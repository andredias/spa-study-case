import secrets
from typing import Dict, Optional

from pony.orm import PrimaryKey, Required
from pydantic import BaseModel, EmailStr

from .. import resources as res
from ..utils import crypt_ctx, select
from . import _insert
from . import update as _update

MAX_ID = 2**32


class UserRecordIn(BaseModel):
    name: str
    email: EmailStr
    password: str
    admin: bool = False


class UserInfo(BaseModel):
    id: int
    name: str
    email: EmailStr
    admin: bool = False


class User(res.pony_db.Entity):
    # Auto-incremented IDs are not particularly good for users as primary keys.
    # 1. Sequential IDs are guessable. One might guess that admin is always user with ID 1, for example.
    # 2. Tests end up using fixed ID values such as 1 or 2 instead of real values.
    #    This leads to poor test designs that should be avoided.
    id = PrimaryKey(int, auto=False, unsigned=True)
    name = Required(str)
    email = Required(str, unique=True)
    password_hash = Required(str)
    admin = Required(bool)


async def get_user_by_login(email: str, password: str) -> Optional[UserInfo]:
    sql, values = select(user for user in User if user.email == email)  # type: ignore
    result = await res.async_db.fetch_one(sql, values)
    if result and crypt_ctx.verify(password, result['password_hash']):
        return UserInfo(**result)
    return None


async def insert(user: UserRecordIn) -> int:
    fields = user.dict()
    fields['id'] = secrets.randbelow(MAX_ID)
    password = fields.pop('password')
    fields['password_hash'] = crypt_ctx.hash(password)
    await _insert('user', fields)
    return fields['id']


async def update(fields: Dict, id: int) -> None:
    if 'password' in fields:
        password = fields.pop('password')
        fields['password_hash'] = crypt_ctx.hash(password)
    await _update('user', fields, id)
