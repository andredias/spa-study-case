from typing import Any, Mapping

from fastapi import Cookie, Depends, Header, HTTPException

from .models.user import UserInfo, get_user
from .sessions import get_session, is_valid_csrf


async def authenticated_session(session_id: str = Cookie(None), x_csrf_token: str = Header(None)) -> Mapping[str, Any]:
    '''
    FastAPI Dependency to get authenticated session data.
    If no valid session is found, it raises an HTTP Error 401
    '''
    if (
        session_id and x_csrf_token and is_valid_csrf(session_id, x_csrf_token) and
        (data := await get_session(session_id))
    ):
        return data
    else:
        raise HTTPException(status_code=401)


async def authenticated_user(data: Mapping[str, Any] = Depends(authenticated_session)) -> UserInfo:
    user = await get_user(data['id'])
    if not user:
        raise HTTPException(status_code=401)
    return user


async def admin_user(user: UserInfo = Depends(authenticated_user)) -> UserInfo:
    if not user.admin:
        raise HTTPException(status_code=403)
    return user
