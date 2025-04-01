"""Basic SQLAlchemy functionality tests for ClickHouse."""

from sqlalchemy import text
from sqlalchemy.engine import Engine

from clickhouse_connect import common

# Test queries with comments to identify in ClickHouse logs
TEST_QUERY = """
   -- 6dcd92a04feb50f14bbcf07c661680ba
   WITH dummy = 2
   SELECT database, name FROM system.tables LIMIT 2
   -- 6dcd92a04feb50f14bbcf07c661680ba
   """

TEST_QUERY_VER19 = """
   -- 6dcd92a04feb50f14bbcf07c661680ba
   SELECT database, name FROM system.tables LIMIT 2
   -- 6dcd92a04feb50f14bbcf07c661680ba
   """


def test_dsn_config(test_engine: Engine):
    """Test DSN configuration parameters are passed correctly."""
    common.set_setting("invalid_setting_action", "drop")
    client = test_engine.raw_connection().connection.client

    assert client.http.connection_pool_kw["cert_reqs"] == "CERT_REQUIRED"
    assert "use_skip_indexes" in client.params
    assert client.params["http_max_field_name_size"] == "99999"
    assert client.query_limit == 2333
    assert client.compression == "zstd"


def test_cursor(test_engine: Engine):
    """Test cursor functionality."""
    common.set_setting("invalid_setting_action", "drop")
    raw_conn = test_engine.raw_connection()
    cursor = raw_conn.cursor()

    sql = TEST_QUERY
    if not raw_conn.connection.client.min_version("21"):
        sql = TEST_QUERY_VER19

    cursor.execute(sql)

    assert cursor.description[0][0] == "database"
    assert cursor.description[1][1] == "String"
    assert len(getattr(cursor, "data")) == 2
    assert cursor.summary[0]["read_rows"] == "2"

    raw_conn.close()


def test_execute(test_engine: Engine):
    """Test execute functionality with various queries."""
    common.set_setting("invalid_setting_action", "drop")

    with test_engine.begin() as conn:
        sql = TEST_QUERY
        if not conn.connection.connection.client.min_version("21"):
            sql = TEST_QUERY_VER19

        rows = list(row for row in conn.execute(text(sql)))
        assert len(rows) == 2

        rows = list(
            row for row in conn.execute(text("DROP TABLE IF EXISTS dummy_table"))
        )
        assert len(rows) > 0  # This is just the metadata from the "command" QueryResult

        rows = list(row for row in conn.execute(text("describe TABLE system.columns")))
        assert len(rows) > 5
