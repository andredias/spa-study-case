import orjson as json
from pydantic import ValidationError
from tornado.web import HTTPError

from .. import resources as res
from ..models import diff_models
from ..models.user import User, UserInfo, UserRecordPatch, delete, get_user, update
from .base import BaseHandler


class UserHandler(BaseHandler):

    async def _common_validation(self, id: int) -> UserInfo:
        current_user = await self.current_user
        if id != current_user.id and not current_user.admin:
            raise HTTPError(403)
        user = current_user if id == current_user.id else await get_user(id)
        if not user:
            raise HTTPError(404)
        return user

    async def _get_one(self, id):
        id = int(id)
        user = await self._common_validation(id)
        self.write(user.dict())

    async def _get_all(self):
        current_user = await self.current_user
        if not current_user.admin:
            raise HTTPError(403)
        query = User.select()
        result = (record async for record in res.db.iterate(query))
        self.write([UserInfo(**record).dict() async for record in result])

    async def get(self, id=None) -> None:
        if id is not None:
            await self._get_one(id)
        else:
            await self._get_all()

    async def put(self, id) -> None:
        user = await self._common_validation(int(id))
        data = json.loads(self.request.body)
        try:
            patch = UserRecordPatch(**data)
        except ValidationError as error:
            raise HTTPError(400, reason=error)
        fields = diff_models(user, patch)
        await update(fields, id)
        self.set_status(204)
        return

    async def delete(self, id) -> None:
        id = int(id)
        await self._common_validation(id)
        await delete(id)
        self.set_status(204)
