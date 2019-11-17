import asyncio

import asyncpg
# Settings
from asyncpg.pool import Pool

DB = {
    "host": "localhost",
    "port": 5432,
    "database": "aep",
    "username": "aep",
    "password": "aep"
}


async def get_conn_pool():
    return await asyncpg.create_pool(
        host=DB["host"],
        port=DB["port"],
        user=DB["username"],
        password=DB["password"],
        database=DB["database"])


_loop = asyncio.get_event_loop()

pool: Pool = _loop.run_until_complete(get_conn_pool())
