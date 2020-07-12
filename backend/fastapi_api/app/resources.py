from pathlib import Path

from aioredis import create_redis_pool
from aioredis.commands import Redis
from databases import Database as AsyncDatabase
from fakeredis.aioredis import create_redis_pool as fake_create_redis_pool
from pony.orm import Database as SyncDatabase

from . import config

redis: Redis = None
async_db: AsyncDatabase = None
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
        redis = await create_redis_pool((config.REDIS_HOST, config.REDIS_PORT), encoding='utf-8')
    else:
        redis = await fake_create_redis_pool(encoding='utf-8')


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
    global async_db
    kwargs = {}
    if config.ENV == 'production':
        provider = 'postgres'
    else:
        provider = 'sqlite'
        # both async_db and pony_db must use the same db
        filename = Path('/dev/shm/db.sqlite')
        filename.unlink(missing_ok=True)
        filename.touch()
        kwargs['filename'] = str(filename)
        connection_url = f'sqlite:///{filename}'

    pony_db.bind(provider=provider, **kwargs)
    pony_db.generate_mapping(create_tables=True)
    async_db = AsyncDatabase(connection_url)
    await async_db.connect()


async def _stop_database():
    await async_db.disconnect()
    # unbind pony_db database. Useful in tests
    pony_db.provider = pony_db.schema = None
