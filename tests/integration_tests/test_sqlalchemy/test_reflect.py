"""Tests for SQLAlchemy reflection with ClickHouse."""
# pylint: disable=no-member

import sqlalchemy as db
from sqlalchemy import text
from sqlalchemy.engine import Engine

from clickhouse_connect import common
from clickhouse_connect.integrations.sqla.datatypes.sqltypes import (
    UInt32,
    SimpleAggregateFunction,
    Point,
)


def test_basic_reflection(test_engine: Engine):
    """Test basic reflection functionality from system tables.

    Args:
        test_engine: SQLAlchemy engine
    """
    common.set_setting("invalid_setting_action", "drop")
    conn = test_engine.connect()

    metadata = db.MetaData(schema="system")
    table = db.Table("tables", metadata, autoload_with=test_engine)

    query = db.select(*[table.columns.create_table_query])
    result = conn.execute(query)
    rows = result.fetchmany(100)

    assert rows


def test_full_table_reflection(test_engine: Engine, test_db: str):
    """Test full table reflection including column types and engine.

    Args:
        test_engine: SQLAlchemy engine
        test_db: Test database name
    """
    common.set_setting("invalid_setting_action", "drop")
    conn = test_engine.connect()

    # Drop and recreate test table
    conn.execute(text(f"DROP TABLE IF EXISTS {test_db}.reflect_test"))
    conn.execute(
        text(
            f"CREATE TABLE {test_db}.reflect_test (key UInt32, value FixedString(20), "
            "agg SimpleAggregateFunction(anyLast, String)) "
            "ENGINE AggregatingMergeTree ORDER BY key"
        )
    )

    # Reflect table
    metadata = db.MetaData(schema=test_db)
    table = db.Table("reflect_test", metadata, autoload_with=test_engine)

    # Verify reflection
    assert table.columns.key.type.__class__ == UInt32
    assert table.columns.agg.type.__class__ == SimpleAggregateFunction
    assert "MergeTree" in table.engine.name


def test_types_reflection(test_engine: Engine, test_db: str):
    """Test reflection of specific column types including Point.

    Args:
        test_engine: SQLAlchemy engine
        test_db: Test database name
    """
    common.set_setting("invalid_setting_action", "drop")
    conn = test_engine.connect()

    # Drop and recreate test table
    conn.execute(text(f"DROP TABLE IF EXISTS {test_db}.sqlalchemy_types_test"))
    conn.execute(
        text(
            f"CREATE TABLE {test_db}.sqlalchemy_types_test (key UInt32, pt Point) "
            "ENGINE MergeTree ORDER BY key"
        )
    )

    # Reflect table
    metadata = db.MetaData(schema=test_db)
    table = db.Table("sqlalchemy_types_test", metadata, autoload_with=test_engine)

    # Verify reflection
    assert table.columns.key.type.__class__ == UInt32
    assert table.columns.pt.type.__class__ == Point
    assert "MergeTree" in table.engine.name


def test_table_exists(test_engine: Engine):
    """Test table existence check functionality.

    Args:
        test_engine: SQLAlchemy engine
    """
    common.set_setting("invalid_setting_action", "drop")
    conn = test_engine.connect()

    assert test_engine.dialect.has_table(conn, "columns", "system")
    assert not test_engine.dialect.has_table(conn, "nope", "fake_db")
