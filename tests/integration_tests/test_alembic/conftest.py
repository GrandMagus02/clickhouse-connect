from typing import Iterator
from pytest import Config, fixture

from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from alembic.migration import MigrationContext
from alembic.operations import Operations
from clickhouse_connect.integrations.alembic.dialect import ClickHouseDialectImpl
from tests.integration_tests.conftest import TestConfig


@fixture(scope="module", name="test_engine")
def test_engine_fixture(test_config: TestConfig) -> Iterator[Engine]:
    """Create and yield a SQLAlchemy engine for testing.

    Args:
        test_config: Test configuration with connection details

    Returns:
        SQLAlchemy Engine instance
    """
    test_engine: Engine = create_engine(
        f"clickhousedb://{test_config.username}:{test_config.password}@{test_config.host}:"
        f"{test_config.port}/{test_config.test_database}?ch_http_max_field_name_size=99999"
        "&use_skip_indexes=0&ca_cert=certifi&query_limit=2333&compression=zstd"
    )

    yield test_engine
    test_engine.dispose()


@fixture(scope="module", name="test_alembic_context")
def test_alembic_context_fixture(test_engine: Engine) -> Iterator[MigrationContext]:
    """Create and yield an Alembic context for testing.

    Args:
        test_engine: SQLAlchemy Engine instance

    Returns:
        Alembic Context instance
    """
    ctx = MigrationContext.configure(test_engine.connect())
    yield ctx


def test_alembic_operations(test_alembic_context: MigrationContext):
    """Create and yield an Alembic operations for testing.

    Args:
        test_alembic_context: Alembic Context instance

    Returns:
        Alembic Operations instance
    """
    op = Operations(test_alembic_context, ClickHouseDialectImpl)
    yield op
