import os
from subprocess import DEVNULL, check_call
from typing import Any, Dict, Generator, List

from pytest import fixture

from app.models.user import UserRecordIn, insert  # isort:skip


@fixture
async def users(app) -> List[Dict[str, Any]]:
    users = [
        dict(name='Fulano de Tal', email='fulano@email.com', password='Paulo Paulada Power', admin=True),
        dict(name='Beltrano de Tal', email='beltrano@email.com', password='abcd1234', admin=False),
    ]
    for user in users:
        user['id'] = await insert(UserRecordIn(**user))
    return users


@fixture(scope='session')
def docker() -> Generator:
    check_call(
        f'docker run -d --rm -e POSTGRES_DB={os.environ["DB_NAME"]} '
        f'-e POSTGRES_PASSWORD={os.environ["DB_PASSWORD"]} '
        f'-p {os.environ["DB_PORT"]}:5432 --name postgres-testing postgres:alpine',
        stdout=DEVNULL,
        shell=True
    )
    check_call(
        f'docker run -d --rm -p {os.environ["REDIS_PORT"]}:6379 --name redis-testing redis:alpine',
        stdout=DEVNULL,
        shell=True
    )
    try:
        yield
    finally:
        check_call('docker stop postgres-testing redis-testing', stdout=DEVNULL, shell=True)
