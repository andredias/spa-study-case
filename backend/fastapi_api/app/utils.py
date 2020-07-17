import asyncio
import re
from time import sleep, time
from typing import Any, Awaitable, Callable, Mapping, Tuple, Union

from passlib.context import CryptContext
from pony.orm.core import Query
from pony.orm.core import select as _select

crypt_ctx = CryptContext(schemes=['argon2'])


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
    query = _select(*args)
    return _get_sql_and_values(query)


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
