from typing import Optional

from clickhouse_connect.dbapi.async_dbapi.connection import AsyncConnection


apilevel = "2.0"  # PEP 249  DB API level
threadsafety = 2  # PEP 249  Threads may share the module and connections.
paramstyle = (
    "pyformat"  # PEP 249  Python extended format codes, e.g. ...WHERE name=%(name)s
)


class Error(Exception):
    pass


def connect(
    host: Optional[str] = None,
    database: Optional[str] = None,
    username: Optional[str] = "",
    password: Optional[str] = "",
    port: Optional[int] = None,
    **kwargs,
):
    secure = kwargs.pop("secure", False)
    return AsyncConnection(
        host=host,
        database=database,
        username=username,
        password=password,
        port=port,
        secure=secure,
        **kwargs,
    )
