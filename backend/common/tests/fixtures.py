from typing import Any, Dict, List

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
