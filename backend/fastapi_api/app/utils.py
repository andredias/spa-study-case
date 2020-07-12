from typing import Mapping, Tuple

from passlib.context import CryptContext
from pony.orm.core import Query
from pony.orm.core import select as _select

crypt_ctx = CryptContext(schemes=['argon2'])


def _get_sql_and_values(query: Query) -> Tuple[str, Mapping]:
    '''
    Return a sql query and its values as required to execute an operation in encore/databases
    such as `fetch_one` or `fetch_all`.

    Although Query has a `get_sql` method, it returns the sql without the arguments
    and with ? as the parameter marker.
    However, encore/databases requires named param markers instead.
    Pony's get_sql implementation actually calls `_construct_sql_and_arguments`
    which returns the sql text, arguments and other information not relevant.
    We use this additional information to reformat the SQL query with named params
    '''
    # monkey patch to prevent pony orm to require a db.session
    # used in pony.orm.core.Query._construct_sql_and_arguments
    old_func = query._database._get_cache
    query._database._get_cache = lambda: None
    try:
        sql, arguments, *_ = query._construct_sql_and_arguments()
    finally:
        query._database._get_cache = old_func
    values = {str(i): arg for i, arg in enumerate(arguments, 1)}  # encode/databases requires str keys
    sql = sql.replace('?', ':{}').format(*values.keys())  # what if the provider is Postgres?
    return sql, values


def select(*args) -> Tuple[str, Mapping]:
    '''
    Wraps pony.orm.core.select to return the sql command and the related parameters
    '''
    query = _select(*args)
    return _get_sql_and_values(query)
