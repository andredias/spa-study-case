import re
from typing import Mapping, MutableMapping, Tuple

from loguru import logger
from pony.orm.core import Query
from pony.orm.core import select as _select
from pydantic import BaseModel

from .. import resources as res


def _get_sql_and_values(query: Query) -> Tuple[str, Mapping]:
    '''
    Return a sql query and its values as required to execute an operation in encore/databases
    such as `fetch_one` or `fetch_all`.

    Although Query has a `get_sql` method, it only returns the sql without the arguments.
    The implementation actually calls `_construct_sql_and_arguments`
    which returns the sql text, arguments and other information not relevant.
    We use this additional information to reformat the SQL query with named params.
    '''

    # monkey patch to prevent pony orm to require a db.session
    # used in pony.orm.core.Query._construct_sql_and_arguments
    old_func = query._database._get_cache
    query._database._get_cache = lambda: None
    try:
        sql, arguments, *_ = query._construct_sql_and_arguments()
    finally:
        query._database._get_cache = old_func

    # Transform paramstyle to `:named` as used by encore/databases
    # PostgreSQL uses pyformat `... WHERE name=%(p1)s` and
    # SQLite uses qmark `...WHERE name=?`
    # see: https://www.python.org/dev/peps/pep-0249/#paramstyle
    if query._database.provider.dialect == 'PostgreSQL':
        sql = re.sub(r'%\((.*?)\)s', r':\1', sql)
    else:  # SQLite
        arguments = {f'p{i}': arg for i, arg in enumerate(arguments, 1)}
        sql = sql.replace('?', ':{}').format(*arguments.keys())
    return sql, arguments


def select(*args) -> Tuple[str, Mapping]:
    '''
    Wraps pony.orm.core.select to return the sql command and the related parameters
    '''
    q = _select(*args)
    query, values = _get_sql_and_values(q)
    logger.debug(f'\nquery: {query}\nvalues: {values}')
    return query, values


async def _insert(table_name: str, values: Mapping) -> None:
    fields = ', '.join(f'"{key}"' for key in values.keys())
    params = ', '.join(f':{key}' for key in values.keys())
    query = f'INSERT INTO "{table_name}" ({fields}) VALUES ({params})'
    logger.debug(f'\nquery: {query}\nvalues: {values}')
    await res.db.execute(query, values)
    return


async def insert(table_name: str, values: Mapping) -> None:
    assert 'id' not in [key.lower() for key in values.keys()], 'ID should not be in the values'
    assert values, 'values must contain at least one field and value'
    await _insert(table_name, values)
    return


async def update(table_name: str, values: Mapping, id: int) -> None:
    if not values:
        return
    assert 'id' not in [key.lower() for key in values.keys()], 'ID should not be in the values'
    attributions = ', '.join(f'"{key}" = :{key}' for key in values.keys())
    query = f'UPDATE "{table_name}" SET {attributions} WHERE id = :id'
    logger.debug(f'\nquery: {query}\nvalues: {values}\nid: {id}')
    await res.db.execute(query, {'id': id, **values})
    return


async def delete(table_name: str, id: int) -> None:
    query = f'DELETE FROM "{table_name}" WHERE id = :id'
    logger.debug(f'\nquery: {query}\nid: {id}')
    await res.db.execute(query, {'id': id})
    return


def diff_models(from_: BaseModel, to_: BaseModel) -> MutableMapping:
    '''
    Return a dict with differences of the second in relation to the first model.
    Useful for getting only the fields that have changed before an update, for example.
    '''
    from_dict = from_.dict()
    to_dict = to_.dict(exclude_unset=True)
    return {k: v for k, v in to_dict.items() if from_dict.get(k) != v}
