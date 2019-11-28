import asyncio
import os
import asyncpg
# Settings
from asyncpg.pool import Pool

DB = {
    "host": os.environ.get('DB_HOST', "localhost"),
    "port":  int(os.environ.get('DB_PORT', 5432)),
    "database": os.environ.get('DB_SCHEMA', "aep"),
    "username": os.environ.get('DB_USERNAME', "aep"),
    "password": os.environ.get('DB_PASSWORD', "aep")
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
