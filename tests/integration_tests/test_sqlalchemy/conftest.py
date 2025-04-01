from typing import Iterator
from pytest import fixture

from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from tests.integration_tests.conftest import TestConfig


@fixture(scope='module', name='test_engine')
def test_engine_fixture(test_config: TestConfig) -> Iterator[Engine]:
    """Create and yield a SQLAlchemy engine for testing.
    
    Args:
        test_config: Test configuration with connection details
        
    Returns:
        SQLAlchemy Engine instance
    """
    test_engine: Engine = create_engine(
        f'clickhousedb://{test_config.username}:{test_config.password}@{test_config.host}:'
        f'{test_config.port}/{test_config.test_database}?ch_http_max_field_name_size=99999'
        '&use_skip_indexes=0&ca_cert=certifi&query_limit=2333&compression=zstd'
    )

    yield test_engine
    test_engine.dispose()


@fixture(scope='module', name='test_async_engine')
def test_async_engine_fixture(test_config: TestConfig) -> Iterator[AsyncEngine]:
    """Create and yield an async SQLAlchemy engine for testing.
    
    Args:
        test_config: Test configuration with connection details
        
    Returns:
        SQLAlchemy AsyncEngine instance
    """
    test_async_engine: AsyncEngine = create_async_engine(
        f'clickhousedb+async://{test_config.username}:{test_config.password}@{test_config.host}:'
        f'{test_config.port}/{test_config.test_database}?ch_http_max_field_name_size=99999'
        '&use_skip_indexes=0&ca_cert=certifi&query_limit=2333&compression=zstd'
    )

    yield test_async_engine
    test_async_engine.dispose()
