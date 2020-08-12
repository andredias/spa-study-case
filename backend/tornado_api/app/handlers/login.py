from pydantic import BaseModel, EmailStr, ValidationError
from tornado.web import HTTPError

from ..models.user import get_user_by_login
from ..sessions import create_csrf, create_session, delete_session
from .base import BaseHandler


class LoginInfo(BaseModel):
    email: EmailStr
    password: str


class LoginHandler(BaseHandler):

    async def post(self):
        try:
            rec = LoginInfo(**self.args)
        except ValidationError as error:
            raise HTTPError(400, reason=error)

        user = await get_user_by_login(rec.email, rec.password)
        if user is None:
            raise HTTPError(404, reason='invalid email or password')
        session_id = self.get_cookie('session_id')
        if session_id:
            await delete_session(session_id)
        session_id = await create_session({'user_id': user.id})
        csrf_token = create_csrf(session_id)
        self.set_cookie(name='session_id', value=session_id, httponly=True, secure=True, samesite="lax")
        self.set_cookie(name='csrf', value=csrf_token, secure=True, samesite="lax")
        self.write(vars(user))


class LogoutHandler(BaseHandler):

    async def post(self) -> None:
        session_id = self.get_cookie('session_id')
        if session_id is not None:
            await delete_session(session_id)
        self.set_status(204)
        self.clear_cookie(name='session_id')
        self.clear_cookie(name='csrf')
        return
