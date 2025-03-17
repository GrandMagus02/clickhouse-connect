# tests/integration_tests/test_sqlmodel/test_sqlmodel_integration.py
from uuid import uuid4

import pytest
from sqlalchemy import Column, text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlmodel import SQLModel, Field, select

from clickhouse_connect import common
from clickhouse_connect.cc_sqlalchemy.datatypes.sqltypes import LowCardinality, String, UInt64
from clickhouse_connect.cc_sqlalchemy.ddl.tableengine import MergeTree

# Define the model


test_query = '''
   -- 6dcd92a04feb50f14bbcf07c661680ba
   WITH dummy = 2
   SELECT database, name FROM system.tables LIMIT 2
   -- 6dcd92a04feb50f14bbcf07c661680ba
   '''

test_query_ver19 = """
   -- 6dcd92a04feb50f14bbcf07c661680ba
   SELECT database, name FROM system.tables LIMIT 2
   -- 6dcd92a04feb50f14bbcf07c661680ba
   """


@pytest.mark.asyncio
async def test_async_cursor(test_async_engine: AsyncEngine):
    common.set_setting('invalid_setting_action', 'drop')
    raw_conn = await test_async_engine.raw_connection()
    cursor = raw_conn.cursor()
    sql = test_query
    if not raw_conn.connection.client.min_version('21'):
        sql = test_query_ver19

    cursor.execute(sql)
    assert cursor.description[0][0] == 'database'
    assert cursor.description[1][1] == 'String'
    assert len(getattr(cursor, 'data')) == 2
    assert cursor.summary[0]["read_rows"] == '2'
    raw_conn.close()


@pytest.mark.asyncio
async def test_async_sqlmodel(test_async_engine: AsyncEngine):
    class TestModel(SQLModel, table=True):
        __tablename__ = 'test_model'
        __table_args__ = (
            MergeTree(order_by='id'),
        )
        id: int = Field(default=None, primary_key=True)
        name: str = Field(sa_column=Column(LowCardinality(String)))
        value: int = Field(sa_column=Column(UInt64))

    async with test_async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Insert data into the table
    async with AsyncSession(test_async_engine) as session:
        test_data = TestModel(id=uuid4().int, name='test_name', value=12345)
        session.add(test_data)
        await session.commit()

    # Query the data from the table
    async with AsyncSession(test_async_engine) as session:
        statement = select(TestModel).where(TestModel.name == 'test_name')
        results = (await session.execute(statement)).all()
        for result in results:
            print(result)

    # Drop the table after the tests
    async with AsyncSession(test_async_engine) as session:
        await session.execute(text('DROP TABLE IF EXISTS test_model'))
        await session.commit()