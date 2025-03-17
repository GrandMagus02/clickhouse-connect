from typing import Union

from clickhouse_connect.dbapi.async_dbapi.cursor import AsyncCursor
from clickhouse_connect.driver import create_client, AsyncClient
from clickhouse_connect.driver.query import QueryResult


class AsyncConnection:
    def __init__(self,
                 dsn: str = None,
                 username: str = '',
                 password: str = '',
                 host: str = None,
                 database: str = None,
                 interface: str = None,
                 port: int = 0,
                 secure: Union[bool, str] = False,
                 **kwargs):
        self.client = create_client(host=host,
                                    username=username,
                                    password=password,
                                    database=database,
                                    interface=interface,
                                    port=port,
                                    secure=secure,
                                    dsn=dsn,
                                    generic_args=kwargs)
        self.async_client = AsyncClient(client=self.client)
        self.timezone = self.client.server_tz

    async def close(self):
        await self.client.close()

    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def command(self, cmd: str):
        return await self.async_client.command(cmd)

    async def raw_query(self, query: str) -> QueryResult:
        return await self.async_client.query(query)

    def cursor(self):
        return AsyncCursor(self.client)
