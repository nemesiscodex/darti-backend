import os
import asyncio
import aioredis

redis_host = os.environ.get('REDIS_HOST', "redis://localhost")


_loop = asyncio.get_event_loop()

redis_pool = _loop.run_until_complete(aioredis.create_redis_pool(
        redis_host))
