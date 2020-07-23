from typing import Dict

from pydantic import BaseModel

from .. import resources as res


async def _insert(table_name: str, values: Dict) -> None:
    fields = ', '.join(f'"{key}"' for key in values.keys())
    params = ', '.join(f':{key}' for key in values.keys())
    query = f'INSERT INTO "{table_name}" ({fields}) VALUES ({params})'
    await res.async_db.execute(query, values)
    return


async def insert(table_name: str, values: Dict) -> None:
    assert 'id' not in [key.lower() for key in values.keys()], 'ID should not be in the values'
    await _insert(table_name, values)
    return


async def update(table_name: str, values: Dict, id: int) -> None:
    assert 'id' not in [key.lower() for key in values.keys()], 'ID should not be in the values'
    attributions = ', '.join(f'"{key}" = :{key}' for key in values.keys())
    query = f'UPDATE "{table_name}" SET {attributions} WHERE id = :id'
    await res.async_db.execute(query, {'id': id, **values})
    return


async def delete(table_name: str, id: int) -> None:
    query = f'DELETE FROM "{table_name}" WHERE id = :id'
    await res.async_db.execute(query, {'id': id})
    return


def diff_models(from_: BaseModel, to_: BaseModel) -> Dict:
    '''
    Return a dict with differences of the second in relation to the first model.
    Useful for getting only the fields that have changed before an update, for example.
    '''
    assert from_.__class__ == to_.__class__
    from_dict = from_.dict()
    to_dict = to_.dict()
    return {k: v for k, v in to_dict.items() if from_dict.get(k) != v}
