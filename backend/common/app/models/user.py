import secrets
from typing import MutableMapping, Optional

import orjson as json
from loguru import logger
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import BigInteger, Boolean, Column, Table, Unicode

from .. import config
from .. import resources as res
from . import metadata

crypt_ctx = CryptContext(schemes=['argon2'])
MAX_ID = 2**32


class UserRecordIn(BaseModel):
    name: str
    email: EmailStr
    password: str
    admin: bool = False


class UserRecordPatch(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    admin: Optional[bool]


class UserInfo(BaseModel):
    id: int
    name: str
    email: EmailStr
    admin: bool


User = Table(
    'user',
    metadata,
    # Auto-incremented IDs are not particularly good for users as primary keys.
    # 1. Sequential IDs are guessable. One might guess that admin is always user with ID 1, for example.
    # 2. Tests end up using fixed ID values such as 1 or 2 instead of real values.
    #    This leads to poor test designs that should be avoided.
    Column('id', BigInteger, primary_key=True, autoincrement=False),
    Column('name', Unicode, nullable=False),
    Column('email', Unicode, nullable=False, unique=True),
    Column('password_hash', Unicode, nullable=False),
    Column('admin', Boolean, default=False)
)


async def get_user_by_login(email: str, password: str) -> Optional[UserInfo]:
    query = User.select(User.c.email == email)
    result = await res.db.fetch_one(query)
    if result and crypt_ctx.verify(password, result['password_hash']):
        return UserInfo(**result)
    return None


async def get_user(id: int) -> Optional[UserInfo]:
    user_id = f'user:{id}'
    # search on Redis first
    result = await res.redis.get(user_id)
    if result:
        logger.debug(f'user {id} is cached')
        return UserInfo(**json.loads(result))

    # search in the database
    logger.debug(f'user {id} not cached')
    query = User.select(User.c.id == id)
    result = await res.db.fetch_one(query)
    if result:
        user = UserInfo(**result)
        # update Redis with the record
        await res.redis.set(user_id, user.json())
        await res.redis.expire(user_id, config.SESSION_LIFETIME)
        return user
    return None


async def insert(user: UserRecordIn) -> int:
    fields = user.dict()
    fields['id'] = secrets.randbelow(MAX_ID)
    password = fields.pop('password')
    fields['password_hash'] = crypt_ctx.hash(password)
    query = User.insert().values(fields)
    await res.db.execute(query)
    return fields['id']


async def update(fields: MutableMapping, id: int) -> None:
    if 'password' in fields:
        password = fields.pop('password')
        fields['password_hash'] = crypt_ctx.hash(password)
    query = User.update().where(User.c.id == id).values(**fields)
    await res.db.execute(query)
    await res.redis.delete(f'user:{id}')  # invalidate cache


async def delete(id: int) -> None:
    query = User.delete().where(User.c.id == id)
    await res.db.execute(query)
    await res.redis.delete(f'user:{id}')
