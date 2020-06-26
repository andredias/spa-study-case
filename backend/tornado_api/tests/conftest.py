from pathlib import Path
from typing import Iterator

from pytest import fixture
from tornado.platform.asyncio import AsyncIOLoop
from tornado.web import Application

from app.main import create_app  # isort:skip


@fixture
def app(io_loop: AsyncIOLoop) -> Iterator[Application]:
    '''
    Return a Tornado.web.Application object with initialized resources
    '''
    with create_app(Path(__file__).parent / 'env.test') as app:
        yield app
