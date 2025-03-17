from typing import Any

from sqlalchemy.engine.interfaces import DBAPIConnection

from clickhouse_connect.cc_sqlalchemy.dialect import ClickHouseDialect

from clickhouse_connect.dbapi import async_dbapi


# A minimal async dialect that simply sets is_async=True.
class AsyncClickHouseDialect(ClickHouseDialect):
    driver = 'async'
    is_async = True

    def connect(self, *cargs: Any, **cparams: Any) -> DBAPIConnection:
        return super().connect(*cargs, **cparams)

    @classmethod
    def dbapi(cls):
        return async_dbapi
