import os
from functools import partial
from pathlib import Path

from aioredis import create_redis_pool
from aioredis.commands import Redis
from databases import Database as AsyncDatabase
from fakeredis.aioredis import create_redis_pool as fake_create_redis_pool
from pony.orm import Database as SyncDatabase

from . import config
from .utils import wait_until_responsive

redis: Redis = None
db: AsyncDatabase = None
pony_db: SyncDatabase = SyncDatabase()


async def start_resources() -> None:
    '''
    Initialize resources such as Redis and Database connections
    '''
    await _init_redis()
    await _init_database()


async def close_resources() -> None:
    '''
    Release resources
    '''
    await _stop_redis()
    await _stop_database()


async def _init_redis():
    global redis
    if config.ENV == 'production':
        function = create_redis_pool(config.REDIS_URL)
        redis = await wait_until_responsive(function)
    else:
        redis = await fake_create_redis_pool()


async def _stop_redis():
    redis.close()
    await redis.wait_closed()


async def _init_database():
    '''
    Ideally, we would only use Pony ORM, but it is not asynchronous unfortunately.
    Therefore, Pony will only be used to generate SQL commands
    but the actual SQL commands will be executed asynchronously by the encore database,
    which is asynchronous.
    '''
    global db
    if config.ENV == 'production':
        connection_url = config.DATABASE_URL
        provider = 'postgres'
        function = partial(pony_db.bind, provider=provider, dsn=connection_url)
        await wait_until_responsive(function)
    else:
        provider = 'sqlite'
        filename = Path('/dev/shm/db.sqlite')
        filename.unlink(missing_ok=True)
        filename.touch()
        pony_db.bind(provider, filename=str(filename))
        connection_url = f'sqlite:///{filename}'

    pony_db.generate_mapping(create_tables=True)
    force_rollback = bool(os.getenv('FORCE_ROLLBACK'))
    db = AsyncDatabase(connection_url, force_rollback=force_rollback)
    await db.connect()


async def _stop_database():
    await db.disconnect()
    # unbind pony_db database. Useful in tests
    pony_db.provider = pony_db.schema = None
