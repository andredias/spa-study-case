import asyncio
from time import sleep, time
from typing import Any, Awaitable, Callable, Union

from passlib.context import CryptContext

crypt_ctx = CryptContext(schemes=['argon2'])


async def wait_until_responsive(
    function: Union[Awaitable, Callable], timeout: float = 3.0, interval: float = 0.1
) -> Any:
    ref = time()
    while (time() - ref) < timeout:
        try:
            if asyncio.iscoroutine(function):
                result = await function  # type:ignore
            else:
                result = function()  # type:ignore
            return result
        except:  # noqa: E722
            pass
        sleep(interval)
    raise TimeoutError()
