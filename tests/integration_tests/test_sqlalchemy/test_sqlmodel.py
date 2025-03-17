# tests/integration_tests/test_sqlmodel/test_sqlmodel_integration.py
from uuid import uuid4

from sqlalchemy import text, Column
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, Field, Session, select

from clickhouse_connect.cc_sqlalchemy.datatypes.sqltypes import LowCardinality, String, UInt64
from clickhouse_connect.cc_sqlalchemy.ddl.tableengine import MergeTree


# Define the model


def test_sqlmodel(test_engine: Engine):
    class TestModel(SQLModel, table=True):
        __tablename__ = 'test_model'
        __table_args__ = (
            MergeTree(order_by='id'),
        )
        id: int = Field(default=None, primary_key=True)
        name: str = Field(sa_column=Column(LowCardinality(String)))
        value: int = Field(sa_column=Column(UInt64))

    SQLModel.metadata.create_all(test_engine)
    # Insert data into the table
    with Session(test_engine) as session:
        test_data = TestModel(id=uuid4().int, name='test_name', value=12345)
        session.add(test_data)
        session.commit()

    # Query the data from the table
    with Session(test_engine) as session:
        statement = select(TestModel).where(TestModel.name == 'test_name')
        results = session.exec(statement)
        for result in results:
            print(result)

    # Drop the table after the tests
    with test_engine.connect() as conn:
        conn.execute(text('DROP TABLE IF EXISTS test_model'))
