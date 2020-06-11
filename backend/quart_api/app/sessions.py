import hmac
from base64 import b64encode
from hashlib import sha256
from secrets import token_urlsafe
from typing import Any, Dict, Optional, Tuple

import ujson as json
from quart import current_app

from . import resources as res


async def create_session(data: Dict[str, Any]) -> Tuple[str, str]:
    '''
    Creates a random session_id and stores its correspondent csrf
    and related data into Redis
    '''
    config = current_app.config
    session_id: str = token_urlsafe(config['SESSION_ID_LENGTH'])
    csrf_token: str = create_csrf(session_id)
    await res.redis.hmset(session_id, 'data', json.dumps(data), 'csrf', csrf_token)
    await res.redis.expire(session_id, config['SESSION_LIFETIME'])
    return session_id, csrf_token


async def get_session(session_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    payload: str
    csrf: str
    payload, csrf = await res.redis.hmget(session_id, 'data', 'csrf')
    data = None
    if payload is not None and csrf is not None:
        data = json.loads(payload)
        await res.redis.expire(session_id, current_app.config['SESSION_LIFETIME'])  # renew expiration date
    return data, csrf


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
    token = b64encode(hmac.new(current_app.config['SECRET_KEY'], message, sha256).digest())  # type: ignore
    length = min(len(session_id), len(token))
    return token[:length].decode('utf-8')


def is_valid_csrf(session_id: str, csrf: str) -> bool:
    return create_csrf(session_id) == csrf
