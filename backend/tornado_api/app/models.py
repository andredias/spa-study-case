from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    hashed_password: str


class UserInfo(BaseModel):
    name: str
    email: EmailStr
    admin: bool = False


async def get_user(email: str, password: str) -> Optional[UserInfo]:
    # get user by email
    # compare password
    return None
