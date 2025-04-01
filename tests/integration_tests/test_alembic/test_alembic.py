from alembic.migration import MigrationContext
from alembic.operations import Operations

from clickhouse_connect.integrations.alembic.dialect import ClickHouseDialectImpl

ALEMBIC_INI_TEMPLATE = """
[alembic]
script_location = {script_location}
sqlalchemy.url = {sqlalchemy_url}

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = INFO
handlers = console
qualname =

[logger_sqlalchemy]
level = INFO
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %Y-%m-%d %H:%M:%S
"""


def test_rename_table(test_alembic_operations: Operations):
    test_alembic_operations.rename_table("t1", "t2")
    head = test_alembic_operations.get_context().get_current_heads()
    print(head)
    assert head == "rename_table"
