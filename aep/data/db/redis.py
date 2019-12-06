import os
import asyncio
import aioredis

redis_host = os.environ.get('REDIS_HOST', "redis://localhost")


_loop = asyncio.get_event_loop()

redis_pool = _loop.run_until_complete(aioredis.create_redis_pool(
        redis_host))


async def delete_keys(pattern):
    cur = b'0'
    while cur:
        cur, keys = await redis_pool.scan(cur, match=pattern)
        for key in keys:
            await redis_pool.unlink(key)