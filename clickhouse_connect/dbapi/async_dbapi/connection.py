from typing import Union

from clickhouse_connect.dbapi.async_dbapi.cursor import AsyncCursor
from clickhouse_connect.driver import create_client, AsyncClient
from clickhouse_connect.driver.query import QueryResult
from sqlalchemy.util.concurrency import await_only


class AsyncConnection:
    await_ = staticmethod(await_only)

    def __init__(
        self,
        dsn: str = None,
        username: str = "",
        password: str = "",
        host: str = None,
        database: str = None,
        interface: str = None,
        port: int = 0,
        secure: Union[bool, str] = False,
        **kwargs,
    ):
        self.client = create_client(
            host=host,
            username=username,
            password=password,
            database=database,
            interface=interface,
            port=port,
            secure=secure,
            dsn=dsn,
            generic_args=kwargs,
        )
        self.async_client = AsyncClient(client=self.client)
        self.timezone = self.client.server_tz

    def close(self):
        self.await_(self.async_client.close())

    def commit(self):
        pass

    def rollback(self):
        pass

    def command(self, cmd: str):
        return self.await_(self.async_client.command(cmd))

    def raw_query(self, query: str) -> QueryResult:
        return self.await_(self.async_client.query(query))

    def cursor(self):
        return AsyncCursor(self)
