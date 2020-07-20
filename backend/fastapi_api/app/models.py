import secrets
from typing import Optional

from pony.orm import PrimaryKey, Required
from pydantic import BaseModel, EmailStr

from . import resources as res
from .utils import crypt_ctx, select

MAX_ID = 2**32


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


async def insert_user(name: str, email: str, password: str, admin: bool = False) -> None:
    user = UserRecord(
        id=secrets.randbelow(MAX_ID),
        name=name,
        password_hash=crypt_ctx.hash(password),
        email=email,
        admin=admin,
    )
    query = 'INSERT INTO "user" (id, name, email, password_hash, admin) ' \
            'VALUES (:id, :name, :email, :password_hash, :admin)'
    await res.async_db.execute(query, user.dict())
    return
