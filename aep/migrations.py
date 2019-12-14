from yoyo import get_backend
from yoyo import read_migrations

from aep.settings import DB


def migrate():
    uri = 'postgres://{username}:{password}@{host}:{port}/{database}' \
        .format(username=DB.username,
                password=DB.password,
                host=DB.host,
                port=str(DB.port),
                database=DB.database)
    backend = get_backend(uri)
    migrations = read_migrations('./migrations/')
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
