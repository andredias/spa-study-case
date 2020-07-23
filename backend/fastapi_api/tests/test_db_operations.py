from unittest.mock import AsyncMock, patch

from pydantic import BaseModel
from pytest import mark, raises

from app.models import insert, update, delete, diff_models  # isort:skip


@patch('app.resources.async_db', new_callable=AsyncMock)
@mark.asyncio
async def test_insert(async_db):
    # ok
    values = {'name': 'fulano', 'email': 'fulano@email.com'}
    await insert('test', values)
    expected_query = 'INSERT INTO "test" ("name", "email") VALUES (:name, :email)'
    async_db.execute.assert_called_with(expected_query, values)

    # empty values
    with raises(AssertionError):
        await insert('test', {})

    # id into values
    with raises(AssertionError):
        await insert('test', {'id': 1, **values})


@patch('app.resources.async_db', new_callable=AsyncMock)
@mark.asyncio
async def test_update(async_db):
    # ok
    values = {'name': 'fulano', 'email': 'fulano@email.com'}
    await update('test', values, 1)
    expected_query = 'UPDATE "test" SET "name" = :name, "email" = :email WHERE id = :id'
    async_db.execute.assert_called_with(expected_query, {'id': 1, **values})

    # empty values
    with raises(AssertionError):
        await update('test', {}, 0)

    # id into values
    with raises(AssertionError):
        await update('test', {'id': 1, **values}, 1)


@patch('app.resources.async_db', new_callable=AsyncMock)
@mark.asyncio
async def test_delete(async_db):
    await delete('test', 1)
    expected_query = 'DELETE FROM "test" WHERE id = :id'
    async_db.execute.assert_called_with(expected_query, {'id': 1})


def test_diff_models():

    class A(BaseModel):
        id: int
        name: str
        value: int

    class B(BaseModel):
        id: int
        name: str
        email: str

    a1 = A(id=1, name='A', value=2)
    a2 = A(id=1, name='B', value=3)
    assert diff_models(a1, a2) == dict(name='B', value=3)
    assert diff_models(a2, a1) == dict(name='A', value=2)

    b = B(id=1, name='A', email='a@email.com')
    with raises(AssertionError):
        diff_models(a1, b)
