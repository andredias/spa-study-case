from typing import Optional

from pony.orm import Required
from pydantic import BaseModel, EmailStr

from . import resources as res
from .utils import crypt_ctx, select


class UserRecord(BaseModel):
    id: int
    name: str
    email: EmailStr
    password_hash: str
    admin: bool = False


class UserInfo(BaseModel):
    id: int
    name: str
    email: EmailStr
    admin: bool = False


class User(res.pony_db.Entity):
    name = Required(str)
    email = Required(str)
    password_hash = Required(str)
    admin = Required(bool)


async def get_user_by_login(email: str, password: str) -> Optional[UserInfo]:
    sql, values = select(user for user in User if user.email == email)  # type: ignore
    result = await res.async_db.fetch_one(sql, values)
    if result and crypt_ctx.verify(password, result['password_hash']):
        return UserInfo(**result)
    return None
