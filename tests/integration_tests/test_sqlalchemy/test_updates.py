"""Tests for SQLAlchemy update operations with ClickHouse."""

from pytest import fixture

import sqlalchemy as db
from sqlalchemy import MetaData, text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from clickhouse_connect.integrations.sqla.datatypes.sqltypes import (
    LowCardinality,
    String,
    UInt64,
)
from clickhouse_connect.integrations.sqla.ddl.tableengine import engine_map
from clickhouse_connect.driver import Client


@fixture(scope="module", autouse=True, name="test_model")
def test_model_fixture(
    test_client: Client, test_engine: Engine, test_db: str, test_table_engine: str
):
    """Create a test model for update tests.

    Args:
        test_client: ClickHouse client
        test_engine: SQLAlchemy engine
        test_db: Test database name
        test_table_engine: Table engine to use

    Returns:
        SQLAlchemy model or None if version requirements not met
    """
    if not test_client.min_version("22.6.1"):
        yield None
        return

    engine_cls = engine_map[test_table_engine]
    Base = declarative_base(metadata=MetaData(schema=test_db))  # pylint: disable=invalid-name

    class Model(Base):
        """Test model for update operations."""

        __tablename__ = "update_model"
        __table_args__ = (engine_cls(order_by=["test_name", "value_1"]),)

        test_name = db.Column(LowCardinality(String), primary_key=True)
        value_1 = db.Column(String)
        metric_2 = db.Column(UInt64)
        description = db.Column(String)

    conn = test_engine.connect()
    conn.execute(text("DROP TABLE IF EXISTS update_model"))
    Base.metadata.create_all(test_engine)
    yield Model


def test_single_update(test_engine: Engine, test_model):
    """Test single row update using SQLAlchemy expressions.

    Args:
        test_engine: SQLAlchemy engine
        test_model: Test model class
    """
    if not test_model:
        return

    conn = test_engine.connect()

    # First insert data
    conn.execute(
        db.insert(test_model).values(
            test_name="single_update", value_1="v1", metric_2=1234, description="Desc"
        )
    )

    # Update data
    conn.execute(
        db.update(test_model)
        .where(test_model.test_name == "single_update")
        .values(metric_2=12345, description="Updated Desc")
    )


def test_multiple_update(test_engine: Engine, test_model):
    """Test multiple updates using ORM session.

    Args:
        test_engine: SQLAlchemy engine
        test_model: Test model class
    """
    if not test_model:
        return

    session = Session(test_engine)

    # First insert data
    session.add(
        test_model(
            test_name="multi_1",
            value_1="v1",
            metric_2=1234,
            description="First of Many",
        )
    )
    session.add(
        test_model(
            test_name="multi_2",
            value_1="v2",
            metric_2=1234,
            description="Second of Many",
        )
    )
    session.commit()

    # Update data
    session.query(test_model).where(test_model.test_name == "multi_1").update(
        {
            "value_1": "updated_v1",
            "metric_2": 54321,
            "description": "Updated First of Many",
        }
    )

    session.query(test_model).where(test_model.test_name == "multi_2").update(
        {
            "value_1": "updated_v2",
            "metric_2": 54321,
            "description": "Updated Second of Many",
        }
    )
    session.commit()

    # Verify updates
    results = session.query(test_model).all()
    assert len(results) == 2
    assert results[0].value_1 == "updated_v1"
    assert results[0].metric_2 == 54321
    assert results[0].description == "Updated First of Many"
    assert results[1].value_1 == "updated_v2"
    assert results[1].metric_2 == 54321
    assert results[1].description == "Updated Second of Many"


def test_bulk_update(test_engine: Engine, test_model):
    """Test bulk update using ORM session's bulk_update_mappings method.

    Args:
        test_engine: SQLAlchemy engine
        test_model: Test model class
    """
    if not test_model:
        return

    session = Session(test_engine)

    # Bulk update
    session.bulk_update_mappings(
        test_model,
        [
            {
                "test_name": "bulk_1",
                "value_1": "updated_v1",
                "metric_2": 12345,
                "description": "Updated First of Bulk",
            },
            {
                "test_name": "bulk_2",
                "value_1": "updated_v2",
                "metric_2": 12345,
                "description": "Updated Second of Bulk",
            },
            {
                "test_name": "bulk",
                "value_1": "updated_vb78",
                "metric_2": 98765,
                "description": "Updated Third of Bulk",
            },
        ],
    )
    session.commit()
