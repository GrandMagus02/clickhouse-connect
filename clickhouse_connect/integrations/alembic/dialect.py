try:
    from alembic.ddl import impl
    from alembic.ddl.base import (
        compiles,
        ColumnComment,
        format_table_name,
        format_column_name,
    )
except ImportError:
    raise RuntimeError("alembic must be installed")

from sqlalchemy.sql.ddl import DropTable
from sqlalchemy import types

class ClickHouseDialectImpl(impl.DefaultImpl):
    __dialect__ = "clickhouse"
    transactional_ddl = False

    def drop_table(self, table):
        table.dispatch.before_drop(
            table, self.connection, checkfirst=False, _ddl_runner=self
        )

        self._exec(DropTable(table))

        table.dispatch.after_drop(
            table, self.connection, checkfirst=False, _ddl_runner=self
        )


@compiles(ColumnComment, "clickhouse")
def visit_column_comment(element, compiler, **kw):
    ddl = "ALTER TABLE {table_name} COMMENT COLUMN {column_name} {comment}"
    comment = compiler.sql_compiler.render_literal_value(
        element.comment or "", types.String()
    )

    return ddl.format(
        table_name=format_table_name(compiler, element.table_name, element.schema),
        column_name=format_column_name(compiler, element.column_name),
        comment=comment,
    )
