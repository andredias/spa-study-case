import hmac
from base64 import b64encode
from hashlib import sha256
from secrets import token_urlsafe
from typing import Any, Dict, Optional

import ujson as json
from fastapi import Cookie, Header, HTTPException

from . import config
from . import resources as res


async def create_session(data: Dict[str, Any]) -> str:
    '''
    Creates a random session_id and stores the related data into Redis.
    '''
    session_id: str = token_urlsafe(config.SESSION_ID_LENGTH)
    await res.redis.set(session_id, json.dumps(data))
    await res.redis.expire(session_id, config.SESSION_LIFETIME)
    return session_id


async def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    payload = await res.redis.get(session_id)
    data = None
    if payload is not None:
        data = json.loads(payload)
        await res.redis.expire(session_id, config.SESSION_LIFETIME)  # renew expiration date
    return data


async def delete_session(session_id: str) -> None:
    await res.redis.delete(session_id)


async def session_exists(session_id: str) -> bool:
    return await res.redis.exists(session_id)


def create_csrf(session_id: str) -> str:
    '''
    Based on
    https://www.jokecamp.com/blog/examples-of-creating-base64-hashes-using-hmac-sha256-in-different-languages/#python3
    '''
    message = bytes(session_id, 'utf-8')
    token = b64encode(hmac.new(config.SECRET_KEY, message, sha256).digest())  # type: ignore
    return token.decode('utf-8')


def is_valid_csrf(session_id: str, csrf: str) -> bool:
    return create_csrf(session_id) == csrf


async def authenticated_session(session_id: str = Cookie(None), x_csrf_token: str = Header(None)) -> Dict[str, Any]:
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
