import asyncio

import aioredis

from aep.settings import REDIS

_loop = asyncio.get_event_loop()

redis_pool = _loop.run_until_complete(aioredis.create_redis_pool(
    REDIS.host))


async def delete_keys(pattern):
    cur = b'0'
    while cur:
        cur, keys = await redis_pool.scan(cur, match=pattern)
        for key in keys:
            await redis_pool.unlink(key)
