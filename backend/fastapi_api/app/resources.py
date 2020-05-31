from aioredis import create_redis_pool
from aioredis.commands import Redis
from fakeredis.aioredis import create_redis_pool as fake_create_redis_pool

from . import config

redis: Redis = None


async def start_resources() -> None:
    '''
    Initialize resources such as Redis and Database connections
    '''
    global redis
    if config.ENV == 'production':
        redis = await create_redis_pool((config.REDIS_HOST, config.REDIS_PORT), encoding='utf-8')
    else:
        redis = await fake_create_redis_pool(encoding='utf-8')


async def close_resources() -> None:
    '''
    Release resources
    '''
    redis.close()
    await redis.wait_closed()
