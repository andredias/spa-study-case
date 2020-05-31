from typing import Dict, Optional

from fastapi import APIRouter, Cookie, HTTPException, Response
from pydantic import BaseModel, EmailStr

from ..models import User
from ..sessions import create_session, delete_session

router = APIRouter()


class UserInfo(BaseModel):
    name: str
    email: EmailStr
    admin: bool = False


class LoginInfo(BaseModel):
    email: EmailStr
    password: str


async def get_user(email: str, password: str) -> Optional[User]:
    # get user by email
    # compare password
    return None


@router.post('/login', response_model=UserInfo)
async def login(rec: LoginInfo, response: Response, session_id: str = Cookie(None)) -> Dict:
    user = await get_user(rec.email, rec.password)
    if user is None:
        raise HTTPException(status_code=404, detail='invalid email or password')
    if session_id:
        await delete_session(session_id)
    session_id, csrf_token = await create_session({'user_id': user.id})
    response.set_cookie(key='session_id', value=session_id, httponly=True)
    response.set_cookie(key='csrf', value=csrf_token, max_age=1)
    return vars(user)


@router.post('/logout', responses={204: {"model": None}})
async def logout(response: Response, session_id: str = Cookie(None)) -> None:
    if session_id is not None:
        await delete_session(session_id)
    response.status_code = 204
    response.delete_cookie(key='session_id')
    response.delete_cookie(key='csrf')
    return
