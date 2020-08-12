from typing import Any, Mapping, Union

import orjson as json
from tornado.web import HTTPError, RequestHandler

from ..models.user import UserInfo, get_user
from ..sessions import get_session, is_valid_csrf


class BaseHandler(RequestHandler):

    @property
    def args(self):
        return json.loads(self.request.body)

    def clear_cookie(self, name: str, path: str = "/", domain: str = None) -> None:
        '''
        Overwrites default implementation to set max-age=0 instead of only using expires
        see: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#Attributes
        '''
        self.set_cookie(name, value='', path=path, domain=domain, max_age=0)
        return

    async def authenticated_session(self) -> Mapping[str, Any]:
        session_id = self.get_cookie('session_id')
        x_csrf_token = self.request.headers.get('x-csrf-token')
        if (
            session_id and x_csrf_token and is_valid_csrf(session_id, x_csrf_token) and
            (data := await get_session(session_id))
        ):
            return data
        else:
            raise HTTPError(status_code=401)

    # use some kind of lru_cache later for improve this
    # maybe https://asyncstdlib.readthedocs.io/en/latest/source/api/functools.html
    async def get_current_user(self) -> UserInfo:
        data = await self.authenticated_session()
        user = await get_user(data['id'])
        if not user:
            raise HTTPError(401)
        return user

    def write(self, chunk: Union[str, bytes, dict]) -> None:
        '''
        Overwrite default write to accept lists
        '''
        data = json.dumps(chunk)
        self.set_header("Content-Type", "application/json")
        self._write_buffer.append(data)
