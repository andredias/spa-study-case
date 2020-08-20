from pathlib import Path
from typing import Any, Union

import orjson
from fastapi import FastAPI
from starlette.responses import JSONResponse

from . import config
from .resources import shutdown, startup
from .routers import hello, login, user

routers = [
    hello.router,
    login.router,
    user.router,
]


def create_app(env_filename: Union[str, Path] = '.env') -> FastAPI:
    config.init(env_filename)

    app = FastAPI(default_response_class=ORJSONResponse)
    for router in routers:
        app.include_router(router)

    @app.on_event('startup')
    async def startup_event():
        await startup()

    @app.on_event('shutdown')
    async def shutdown_event():
        await shutdown()

    return app


class ORJSONResponse(JSONResponse):

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)
