from pathlib import Path
from typing import AsyncIterable, Iterator

from httpx import AsyncClient
from pytest import fixture
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.platform.asyncio import AsyncIOLoop
from tornado.testing import bind_unused_port
from tornado.web import Application

from .common.fixtures import users  # noqa: F401

from app.main import create_app  # isort:skip


@fixture
def io_loop() -> AsyncIOLoop:
    loop = IOLoop()
    loop.make_current()
    try:
        yield loop
    finally:
        loop.clear_current()
        loop.close(all_fds=True)


@fixture
def app(io_loop: AsyncIOLoop) -> Iterator[Application]:
    """
    Return a Tornado.web.Application object with initialized resources
    """
    with create_app(Path(__file__).parent / "env.test") as app:
        yield app


@fixture
async def client(app: Application) -> AsyncIterable[AsyncClient]:
    """
    Return a client to be used in async tests
    """
    http_server = HTTPServer(app)
    port = bind_unused_port()[1]
    http_server.listen(port)
    async with AsyncClient(base_url=f"http://localhost:{port}") as _client:
        yield _client
