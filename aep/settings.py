from dataclasses import dataclass
from os import environ


# Auth
@dataclass
class AuthConfig:
    jwt_private_key: str = None
    admin_username: str = None
    admin_password: str = None


AUTH = AuthConfig(
    jwt_private_key=environ.get('AUTH_JWT_PRIVATE_KEY'),
    admin_username=environ.get('AUTH_ADMIN_USERNAME'),
    admin_password=environ.get('AUTH_ADMIN_PASSWORD'),
)


# Database
@dataclass
class DBConfig:
    host: str = None
    port: int = None
    database: str = None
    username: str = None
    password: str = None


DB = DBConfig(
    host=environ.get('DB_HOST', "localhost"),
    port=int(environ.get('DB_PORT', 5432)),
    database=environ.get('DB_SCHEMA', "aep"),
    username=environ.get('DB_USERNAME', "aep"),
    password=environ.get('DB_PASSWORD', "aep")
)

# Cache
REDIS = DBConfig(
    host=environ.get('REDIS_HOST', "redis://localhost")
)
