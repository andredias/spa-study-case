from typing import Dict

from fastapi import APIRouter, Cookie, HTTPException, Response
from pydantic import BaseModel, EmailStr

from ..models import UserInfo, get_user
from ..sessions import create_csrf, create_session, delete_session

router = APIRouter()


class LoginInfo(BaseModel):
    email: EmailStr
    password: str


@router.post('/login', response_model=UserInfo)
async def login(rec: LoginInfo, response: Response, session_id: str = Cookie(None)) -> Dict:
    user = await get_user(rec.email, rec.password)
    if user is None:
        raise HTTPException(status_code=404, detail='invalid email or password')
    if session_id:
        await delete_session(session_id)
    session_id = await create_session({'user_id': user.id})
    csrf_token = create_csrf(session_id)
    response.set_cookie(key='session_id', value=session_id, httponly=True, secure=True)
    response.set_cookie(key='csrf', value=csrf_token, secure=True)
    return vars(user)


@router.post('/logout', responses={204: {"model": None}})
async def logout(response: Response, session_id: str = Cookie(None)) -> None:
    if session_id is not None:
        await delete_session(session_id)
    response.status_code = 204
    response.delete_cookie(key='session_id')
    response.delete_cookie(key='csrf')
    return
