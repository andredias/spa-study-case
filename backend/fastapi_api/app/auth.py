from typing import Any, Mapping

from fastapi import Depends, HTTPException

from .models.user import UserInfo, get_user
from .sessions import authenticated_session


async def authenticated_user(data: Mapping[str, Any] = Depends(authenticated_session)) -> UserInfo:
    user = await get_user(data['id'])
    if not user:
        raise HTTPException(status_code=401)
    return user


async def admin_user(user: UserInfo = Depends(authenticated_user)) -> UserInfo:
    if not user.admin:
        raise HTTPException(status_code=403)
    return user
