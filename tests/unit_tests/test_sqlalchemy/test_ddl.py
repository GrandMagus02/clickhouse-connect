import sqlalchemy as db
from sqlalchemy.sql.ddl import CreateTable

from clickhouse_connect.integrations.sqla.datatypes.sqltypes import UInt64, UInt32, DateTime
from clickhouse_connect.integrations.sqla.ddl.tableengine import (
    CollapsingMergeTree,
    GraphiteMergeTree,
    MergeTree,
    ReplicatedMergeTree,
    ReplacingMergeTree,
    VersionedCollapsingMergeTree,
)
from clickhouse_connect.integrations.sqla.dialect import ClickHouseDialect

dialect = ClickHouseDialect()

mergetree_mt_ddl = """\
CREATE TABLE `mergetree_mt_test` (`key` UInt64) Engine MergeTree ORDER BY key\
"""

replicated_mt_ddl = """\
CREATE TABLE `replicated_mt_test` (`key` UInt64) Engine ReplicatedMergeTree('/clickhouse/tables/repl_mt_test', '{replica}') ORDER BY key\
"""

replacing_mt_ddl = """\
CREATE TABLE `replacing_mt_test` (`key` UInt32, `date` DateTime) Engine ReplacingMergeTree(date) ORDER BY key\
"""

collapsing_mt_ddl = """\
CREATE TABLE `collapsing_mt_test` (`key` UInt32, `date` DateTime) Engine CollapsingMergeTree(key) ORDER BY key\
"""

versioned_collapsing_mt_ddl = """\
CREATE TABLE `versioned_collapsing_mt_test` (`key` UInt32, `date` DateTime) Engine VersionedCollapsingMergeTree(key, date) ORDER BY key\
"""

graphite_mt_ddl = """\
CREATE TABLE `graphite_mt_test` (`key` UInt32, `date` DateTime) Engine GraphiteMergeTree(date) ORDER BY key\
"""


def test_table_def():
    metadata = db.MetaData()

    table = db.Table(
        "mergetree_mt_test",
        metadata,
        db.Column("key", UInt64),
        MergeTree(order_by="key"),
    )

    ddl = str(CreateTable(table).compile("", dialect=dialect))
    assert ddl == mergetree_mt_ddl

    table = db.Table(
        "replicated_mt_test",
        metadata,
        db.Column("key", UInt64),
        ReplicatedMergeTree(
            order_by="key",
            zk_path="/clickhouse/tables/repl_mt_test",
            replica="{replica}",
        ),
    )
    ddl = str(CreateTable(table).compile("", dialect=dialect))
    assert ddl == replicated_mt_ddl

    table = db.Table(
        "replacing_mt_test",
        metadata,
        db.Column("key", UInt32),
        db.Column("date", DateTime),
        ReplacingMergeTree(ver="date", order_by="key"),
    )

    ddl = str(CreateTable(table).compile("", dialect=dialect))
    assert ddl == replacing_mt_ddl

    table = db.Table(
        "collapsing_mt_test",
        metadata,
        db.Column("key", UInt32),
        db.Column("date", DateTime),
        CollapsingMergeTree(sign="key", order_by="key"),
    )

    ddl = str(CreateTable(table).compile("", dialect=dialect))
    assert ddl == collapsing_mt_ddl

    table = db.Table(
        "versioned_collapsing_mt_test",
        metadata,
        db.Column("key", UInt32),
        db.Column("date", DateTime),
        VersionedCollapsingMergeTree(
            sign="key",
            version="date", 
            order_by="key"
        ),
    )

    ddl = str(CreateTable(table).compile("", dialect=dialect))
    assert ddl == versioned_collapsing_mt_ddl

    table = db.Table(
        "graphite_mt_test",
        metadata,
        db.Column("key", UInt32),
        db.Column("date", DateTime),
        GraphiteMergeTree(order_by="key"),
    )

    ddl = str(CreateTable(table).compile("", dialect=dialect))
    assert ddl == graphite_mt_ddl
