from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException

from .. import resources as res
from ..auth import admin_user, authenticated_user
from ..models import diff_models, select
from ..models.user import User, UserInfo, UserRecordPatch, delete, get_user, update

router = APIRouter()


@router.get('/user', response_model=Sequence[UserInfo])
async def get_users(admin: UserInfo = Depends(admin_user)) -> Sequence:
    query, values = select(user for user in User)  # type: ignore
    result = (record async for record in res.async_db.iterate(query, values))
    return [UserInfo(**record) async for record in result]


async def _common_validation(id: int, current_user: UserInfo) -> UserInfo:
    if id != current_user.id and not current_user.admin:
        raise HTTPException(403)
    user = current_user if id == current_user.id else await get_user(id)
    if not user:
        raise HTTPException(404)
    return user


@router.get('/user/{id}', response_model=UserInfo)
async def get_user_info(id: int, current_user: UserInfo = Depends(authenticated_user)):
    return await _common_validation(id, current_user)


@router.put('/user/{id}', status_code=204)
async def update_user(id: int, patch: UserRecordPatch, current_user: UserInfo = Depends(authenticated_user)):
    user = await _common_validation(id, current_user)
    fields = diff_models(user, patch)
    await update(fields, id)
    return


@router.delete('/user/{id}', status_code=204)
async def delete_user(id: int, current_user: UserInfo = Depends(authenticated_user)):
    await _common_validation(id, current_user)
    await delete(id)


@router.post('/user')
async def create_user():
    # retornar uma url do novo recurso
    # retornar 201 (Created)
    pass
